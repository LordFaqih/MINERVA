from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
import os

class NormImg(QThread):
    progress_norm = pyqtSignal(int)
    finished_norm = pyqtSignal()
    file_norm = pyqtSignal(str)
    img_input_norm = pyqtSignal(str)
    img_output_norm = pyqtSignal(str)

    def __init__(self, inputNormPath, outputNormPath, outputNameNorm, darkImgPath, brightImgPath, file_name_norm, file_extension_norm, total_images_norm):
        super().__init__()
        self.inputNormPath = inputNormPath
        self.outputNormPath = outputNormPath
        self.objectNameNorm = outputNameNorm
        self.darkImgPath = darkImgPath
        self.brightImgPath = brightImgPath
        self.file_name_norm = file_name_norm
        self.file_extension_norm = file_extension_norm
        self.total_images_norm = total_images_norm

    def run(self):
        self.inputNormPath = self.inputNormPath
        self.outputNormPath = self.outputNormPath
        self.objectNameNorm = self.objectNameNorm
        self.darkImgPath = self.darkImgPath
        self.brightImgPath = self.brightImgPath
        self.file_name_norm = self.file_name_norm
        self.file_extension_norm = self.file_extension_norm
        self.total_images_norm = self.total_images_norm

        for i in range (self.total_images_norm):

            img_path = os.path.join(self.inputNormPath, f"{self.file_name_norm}{i}.{self.file_extension_norm}")
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
            dark = cv2.imread(self.darkImgPath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
            bright = cv2.imread(self.brightImgPath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)

            correction_factor = ((bright - dark) / np.mean(bright - dark)) * 65535

            if np.any(correction_factor == 0):
                correction_factor[correction_factor == 0] = 1

            img_corr = np.divide((img - dark), correction_factor)
            img_corr = np.clip(img_corr, 0, 1)
            img_corr = np.uint16(img_corr * 65535)

            imgOutputPath = os.path.join(self.outputNormPath, f"{self.objectNameNorm}{i}.{self.file_extension_norm}")
            cv2.imwrite(imgOutputPath, img_corr)
            self.file_norm.emit(imgOutputPath)
            self.img_input_norm.emit(img_path)
            self.img_output_norm.emit(imgOutputPath)

            progress = int((i + 1) / self.total_images_norm * 100)  # Menghitung persentase progress
            self.progress_norm.emit(progress)
            self.msleep(100)  # Contoh simulasi proses yang sedang berjalan

        self.finished_norm.emit()