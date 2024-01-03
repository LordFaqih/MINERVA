from PyQt5.QtCore import QThread, pyqtSignal
import vggFunc as vgg
import numpy as np
import cv2

class vggGen(QThread):
    startFusion = pyqtSignal(str)
    finishedFusion = pyqtSignal(str)
    viewFusionOut = pyqtSignal(str)

    def __init__(self, folder_inputFusion1, folder_inputFusion2, outputNameFusion, extensionFileFusion, folder_fusionOutput_path):
        super().__init__()
        self.folder_inputFusion1 = folder_inputFusion1
        self.folder_inputFusion2 = folder_inputFusion2
        self.outputNameFusion = outputNameFusion
        self.extensionFileFusion = extensionFileFusion
        self.folder_fusionOutput_path = folder_fusionOutput_path

    def run(self):
        startCom = "[VGG19]Image Fusion Start..."
        self.startFusion.emit(startCom)

        img1 = cv2.imread(self.folder_inputFusion1, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
        img2 = cv2.imread(self.folder_inputFusion2, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
        self.generatedImage = vgg.fusion(img1, img2)
        self.img_normalized = (self.generatedImage - np.min(self.generatedImage)) / (np.max(self.generatedImage) - np.min(self.generatedImage))
        # Penskalaan gambar ke dalam rentang 0-65535 (range nilai uint16)
        self.img_scaled = (self.img_normalized * 255).astype(np.uint8)
        # Konversi tipe data gambar dari float64 menjadi uint16
        self.img_uint8 = np.round(self.img_scaled).astype(np.uint8)
        fusionPath = f"{self.folder_fusionOutput_path}/{self.outputNameFusion}.{self.extensionFileFusion}"  
        cv2.imwrite(fusionPath, self.img_uint8) 
        self.viewFusionOut.emit(fusionPath)
        finishCom = "[VGG19]Image Fusion Finish"
        self.finishedFusion.emit(finishCom)
    