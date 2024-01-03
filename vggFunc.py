import numpy as np
from sporco.util import tikhonov_filter
import sporco 
import torch
import warnings


# Menonaktifkan peringatan
warnings.filterwarnings("ignore")
from torchvision.models.vgg import vgg19, VGG19_Weights
# Menyalakan kembali peringatan
warnings.filterwarnings("default")

def lowpass(s, lda, npad):
    return sporco.signal.tikhonov_filter(s, lda, npad)

def c3(s):
    if s.ndim == 2:
        s3 = np.dstack([s, s, s])
    else:
        s3 = s
    return np.rollaxis(s3, 2, 0)[None, :, :, :]

def l1_features(out):
    h, w, d = out.shape
    A_temp = np.zeros((h+2, w+2))
    
    l1_norm = np.sum(np.abs(out), axis=2)
    A_temp[1:h+1, 1:w+1] = l1_norm
    return A_temp

def fusion_strategy(feat_a, feat_b, source_a, source_b, unit):
    
    m, n = feat_a.shape
    m1, n1 = source_a.shape[:2]
    weight_ave_temp1 = np.zeros((m1, n1))
    weight_ave_temp2 = np.zeros((m1, n1))
    
    for i in range(1, m):
        for j in range(1, n):
            A1 = feat_a[i-1:i+1, j-1:j+1].sum() / 9
            A2 = feat_b[i-1:i+1, j-1:j+1].sum() / 9
            
            weight_ave_temp1[(i-2)*unit+1:(i-1)*unit+1, (j-2)*unit+1:(j-1)*unit+1] = A1 / (A1+A2)
            weight_ave_temp2[(i-2)*unit+1:(i-1)*unit+1, (j-2)*unit+1:(j-1)*unit+1] = A2 / (A1+A2)

    if source_a.ndim == 3:
        weight_ave_temp1 = weight_ave_temp1[:, :, None]
    source_a_fuse = source_a * weight_ave_temp1
    if source_b.ndim == 3:
        weight_ave_temp2 = weight_ave_temp2[:, :, None]
    source_b_fuse = source_b * weight_ave_temp2
    
    if source_a.ndim == 3 or source_b.ndim == 3:
        gen = np.atleast_3d(source_a_fuse) + np.atleast_3d(source_b_fuse)
    else:
        gen = source_a_fuse + source_b_fuse
    
    return gen

def get_activation(model, layer_numbers, input_image):
    outs = []
    out = input_image
    for i in range(max(layer_numbers)+1):
        with torch.no_grad():
            out = model.features[i](out)
        if i in layer_numbers:
            outs.append(np.rollaxis(out.detach().cpu().numpy()[0], 0, 3))
    return outs

def fusion(img1, img2, model=None):
    npad = 16
    lda = 5
    img1_low, img1_high = lowpass(img1.astype(np.float32)/255, lda, npad)
    img2_low, img2_high = lowpass(img2.astype(np.float32)/255, lda, npad)
    
    if model is None:
        model = vgg19(weights=VGG19_Weights.DEFAULT)
    model.cpu().eval()
    relus = [2, 7, 12, 21]
    unit_relus = [1, 2, 4, 8]
    
    img1_in = torch.from_numpy(c3(img1_high)).cpu()
    img2_in = torch.from_numpy(c3(img2_high)).cpu()
    
    relus_img1 = get_activation(model, relus, img1_in)
    relus_img2 = get_activation(model, relus, img2_in)
    
    img1_feats = [l1_features(out) for out in relus_img1]
    img2_feats = [l1_features(out) for out in relus_img2]
    
    saliencies = []
    saliency_max = None
    for idx in range(len(relus)):
        saliency_current = fusion_strategy(img1_feats[idx], img2_feats[idx], img1_high, img2_high, unit_relus[idx])
        saliencies.append(saliency_current)

        if saliency_max is None:
            saliency_max = saliency_current
        else:
            saliency_max = np.maximum(saliency_max, saliency_current)
            
    if img1_low.ndim == 3 or img2_low.ndim == 3:
        low_fused = np.atleast_3d(img1_low) + np.atleast_3d(img2_low)
    else:
        low_fused = img1_low + img2_low
    low_fused = low_fused / 2
    high_fused = saliency_max
    return low_fused + high_fused
    
    