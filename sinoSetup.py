from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
import os


class SinoGen(QThread):
    progress_inputSino = pyqtSignal(int)
    progress_outputSino = pyqtSignal(int)
    progress_statusSino = pyqtSignal(int)
    finishedInputSino = pyqtSignal()
    finishedOutputSino = pyqtSignal()
    finishedStatusSino = pyqtSignal()
    file_InputSino = pyqtSignal(str)
    file_OutputSino = pyqtSignal(str)
    img_InputSino = pyqtSignal(str)
    img_OutputSino = pyqtSignal(str)

    def __init__(self, folder_sinoInput_path, folder_sinoOutput_path, outputNameSino, inputNameSino, extensionSino, total_images_sino):
        super().__init__()
        self.folder_sinoInput_path = folder_sinoInput_path
        self.folder_sinoOutput_path = folder_sinoOutput_path
        self.outputNameSino = outputNameSino
        self.inputNameSino = inputNameSino
        self.extensionSino = extensionSino
        self.total_images_sino = total_images_sino
     
    def run(self):
        self.folder_sinoInput_path = self.folder_sinoInput_path
        self.folder_sinoOutput_path = self.folder_sinoOutput_path
        self.outputNameSino = self.outputNameSino
        self.inputNameSino = self.inputNameSino
        self.extensionSino = self.extensionSino
        self.total_images_sino = self.total_images_sino
        
        print("Start Reading File...")
        images = []
        for i in range (self.total_images_sino):
            img_path = os.path.join(self.folder_sinoInput_path, f"{self.inputNameSino}{i}.{self.extensionSino}")
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
            #print(img_path)
            self.file_InputSino.emit(img_path)
            images.append(img)
            progressInputSino = int((i + 1) / self.total_images_sino * 100)  # Menghitung persentase progress
            self.progress_inputSino.emit(progressInputSino)
            self.img_InputSino.emit(img_path)
            self.msleep(100)
        self.finishedInputSino.emit()

        print("Image Stack")
        stackStart = "Images Stack Process Loading..."
        self.progress_statusSino.emit(stackStart)
        projData = np.stack(images, axis=2)
        self.finishedStatusSino.emit()
        print("Generate Sinogram")

        for i in range(projData.shape[0]):
            slice_3d = projData[i, :, :]
            totalSlice = projData.shape[0]
            output_filename = f"{self.outputNameSino}{i}.{self.extensionSino}"
            output_path_sino = os.path.join(self.folder_sinoOutput_path, output_filename)
            cv2.imwrite(output_path_sino, slice_3d, [cv2.IMWRITE_TIFF_COMPRESSION, 1])
            self.file_OutputSino.emit(output_path_sino)
            print("Sinogram:", i)
            progress2 = int((i + 1) / totalSlice * 100)  # Menghitung persentase progress
            self.progress_outputSino.emit(progress2)
            self.img_OutputSino.emit(output_path_sino)
            self.msleep(100)
        self.finishedOutputSino.emit()

        print("Generating Sinogram Complete")
        print("Exporting configuration file...")
        first_image = os.path.join(self.folder_sinoInput_path, sorted(os.listdir(self.folder_sinoInput_path))[0])  # Ambil gambar pertama dalam folder input
        config_file_path = os.path.join(self.folder_sinoOutput_path, "0config.txt")
        with open(config_file_path, 'w') as f:
            f.write(first_image)
        print("Configuration file exported.")