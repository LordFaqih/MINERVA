from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
from PIL import Image
from projFilter import projFilter
import os

class RecImg(QThread):
    progress_updated_recon = pyqtSignal(int)
    finished_recon = pyqtSignal()
    thetaUpdate = pyqtSignal(str)
    img_processed_recon = pyqtSignal(str)
    sudut = pyqtSignal(str)
    stepSinoRead = pyqtSignal(int)

    #idx, folder_out_sino, objectName, objectTag, folder_out_rec, numProj, dTheta
    def __init__(self,Theta, dTheta, sinoPath, output_path, idx, outputNameRecon, extensionRecon, rotPointRecon):
        super().__init__()
        self.sinoPath = sinoPath
        self.Theta = Theta
        self.dTheta = dTheta
        self.output_path = output_path
        self.idx = idx
        self.outputNameRecon = outputNameRecon
        self.extensionRecon = extensionRecon
        self.rotPointRecon = rotPointRecon
    def run(self):
        mySino = cv2.imread(self.sinoPath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
        filtSino = projFilter(mySino)
        
        imageLen = filtSino.shape[0]
        reconMatrix = np.zeros((imageLen, imageLen))
        
        x = np.arange(imageLen)-imageLen/2 #create coordinate system centered at (x,y = 0,0)
        y = x.copy()
        X, Y = np.meshgrid(x, y)

        theta = np.arange(0, (self.Theta + 1), self.dTheta)
        theta = theta*np.pi/180
        numAngles = len(theta)

        output_folder_name = "Reconstruction Matrix"
        output_path = os.path.join(self.output_path, output_folder_name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Folder '{output_path}' berhasil dibuat.")
        else:
            print(f"Folder '{output_path}' sudah ada.")

        for n in range(numAngles):
            Xrot = X*np.sin(theta[n])-Y*np.cos(theta[n]) #determine rotated x-coordinate about origin in mesh grid form
            XrotCor = np.round(Xrot+self.rotPointRecon) #shift back to original image coordinates, round values to make indices
            XrotCor = XrotCor.astype('int')
            projMatrix = np.zeros((imageLen, imageLen))
            m0, m1 = np.where((XrotCor >= 0) & (XrotCor <= (imageLen-1))) #after rotating, you'll inevitably have new coordinates that exceed the size of the original
            s = filtSino[:,n] #get projection
            projMatrix[m0, m1] = s[XrotCor[m0, m1]]  #backproject in-bounds data
            
            reconMatrix += projMatrix

            #reconstruction matix save command
            progress = np.round((reconMatrix-np.min(reconMatrix))/np.ptp(reconMatrix)*255) #convert values to integers 0-255
            progress = Image.fromarray(progress.astype('uint8'))

            progress.save(f'{output_path}/{self.outputNameRecon}_reconstruction matrix_{n}.{self.extensionRecon}')


            progressFolder = f"{output_path}/{self.outputNameRecon}_reconstruction matrix_{n}.{self.extensionRecon}"
            recMatrixFolder = f"{output_path}/{self.outputNameRecon}_reconstruction matrix_{n}.{self.extensionRecon}"
            self.img_processed_recon.emit(recMatrixFolder)
            
            stepRec = int(numAngles)
            self.thetaUpdate.emit(progressFolder)
            self.stepSinoRead.emit(n)
            progress = int((n + 1) / self.Theta * 100)  # Menghitung persentase progress
            derajat = f"Theta: {n} deg"
            self.progress_updated_recon.emit(progress)
            self.sudut.emit(derajat)
            self.msleep(100)  # Contoh simulasi proses yang sedang berjalan
            
        backprojArray = np.flipud(reconMatrix)
        recon2 = np.round((backprojArray - np.min(backprojArray)) / np.ptp(backprojArray) * 255)
        reconImg = Image.fromarray(recon2.astype('uint8'))
        reconImg.save(f"{self.output_path}/{self.outputNameRecon}_reconstruction{self.idx}.{self.extensionRecon}")
        self.finished_recon.emit()