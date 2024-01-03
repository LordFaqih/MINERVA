from PyQt5.QtCore import QThread, pyqtSignal
import cv2

import os

class count_white_point_noise(QThread):
    def __init__(self, image_path, output_Noise_Preview, idx_noise):
        super().__init__()
        self.image_path = image_path
        self.output_Noise_Preview = output_Noise_Preview
        self.idx_noise = idx_noise

    def run(self):
        # Load image
        threshold = 200
        image = cv2.imread(self.image_path)
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

        # Find contours of white regions
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw circles with a hole in the center around white regions
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            center = (x + w // 2, y + h // 2)
            radius = 20
            cv2.circle(image, center, radius, (255, 0, 0), 2)
            #cv2.circle(image, center, radius // 2, (0, 0, 0), 2)

        # Convert image from BGR to RGB for plt display
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        size = (600,600)
        image_rgb = cv2.resize(image_rgb, size)
        out_Img_Prev_Noise = f"{self.output_Noise_Preview}/NoisePrev{self.idx_noise}.png"
        cv2.imwrite(out_Img_Prev_Noise, image_rgb)
        return len(contours)
    
class NoiseGen(QThread):
    progress_noise = pyqtSignal(int)
    finished_noise = pyqtSignal()
    file_noise = pyqtSignal(str)
    img_input_noise = pyqtSignal(str)
    img_output_noise = pyqtSignal(str)

    def __init__(self, folder_noiseInput_path, folder_noiseOutput_path, outputNameNoise, inputNameNoise, extensionNoise, total_images_noise):
        super().__init__()
        self.folder_noiseInput_path = folder_noiseInput_path
        self.folder_noiseOutput_path = folder_noiseOutput_path
        self.outputNameNoise = outputNameNoise
        self.inputNameNoise = inputNameNoise
        self.extensionNoise = extensionNoise
        self.total_images_noise = total_images_noise
    
    def run(self):
        self.folder_noiseInput_path = self.folder_noiseInput_path
        self.folder_noiseOutput_path = self.folder_noiseOutput_path
        self.outputNameNoise = self.outputNameNoise
        self.inputNameNoise = self.inputNameNoise
        self.extensionNoise = self.extensionNoise
        self.total_images_noise = int(self.total_images_noise) - 2

        bright_path_den = os.path.join(self.folder_noiseInput_path, "0Bright.tiff")
        dark_path_den = os.path.join(self.folder_noiseInput_path, "0Dark.tiff")
        bright_img_den = cv2.imread(bright_path_den, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
        dark_img_den = cv2.imread(dark_path_den, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
        bright_img_den = cv2.medianBlur(bright_img_den, 3)
        dark_img_den = cv2.medianBlur(dark_img_den, 3)

        cv2.imwrite(f"{self.folder_noiseOutput_path}/0Bright.tiff", bright_img_den)
        cv2.imwrite(f"{self.folder_noiseOutput_path}/0Dark.tiff", dark_img_den)

        for i in range (self.total_images_noise):

            img_path_den = os.path.join(self.folder_noiseInput_path, f"{self.inputNameNoise}{i}.{self.extensionNoise}")
            img_den = cv2.imread(img_path_den, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
            img_den = cv2.medianBlur(img_den, 3)
            imgOutputPath = os.path.join(self.folder_noiseOutput_path, f"{self.outputNameNoise}{i}.{self.extensionNoise}")
            
            cv2.imwrite(imgOutputPath, img_den)
            self.file_noise.emit(imgOutputPath)

            threshold = 200
            idx_noise = i
            ################################################################################################
            image = cv2.imread(img_path_den)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply threshold to get binary image
            _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

            # Find contours of white regions
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw circles with a hole in the center around white regions
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                center = (x + w // 2, y + h // 2)
                radius = 20
                cv2.circle(image, center, radius, (255, 0, 0), 2)
                #cv2.circle(image, center, radius // 2, (0, 0, 0), 2)

            # Convert image from BGR to RGB for plt display
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            size = (600,600)
            image_rgb = cv2.resize(image_rgb, size)
            out_Img_Prev_Noise = f"Images/Dummy/Preview Noise/Before/NoisePrev{idx_noise}.png"
            cv2.imwrite(out_Img_Prev_Noise, image_rgb)

            ################################################################################################
            image = cv2.imread(imgOutputPath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply threshold to get binary image
            _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

            # Find contours of white regions
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw circles with a hole in the center around white regions
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                center = (x + w // 2, y + h // 2)
                radius = 20
                cv2.circle(image, center, radius, (255, 0, 0), 2)
                #cv2.circle(image, center, radius // 2, (0, 0, 0), 2)

            # Convert image from BGR to RGB for plt display
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            size = (600,600)
            image_rgb = cv2.resize(image_rgb, size)
            out_Img_Prev_Noise = f"Images/Dummy/Preview Noise/After/NoisePrev{idx_noise}.png"
            cv2.imwrite(out_Img_Prev_Noise, image_rgb)
            ################################################################################################

            out_Img_Prev_Noise1 = f"Images/Dummy/Preview Noise/Before/NoisePrev{idx_noise}.png"
            self.img_input_noise.emit(out_Img_Prev_Noise1)
            out_Img_Prev_Noise2 = f"Images/Dummy/Preview Noise/After/NoisePrev{idx_noise}.png"
            self.img_output_noise.emit(out_Img_Prev_Noise2)

            progress = int((i + 1) / self.total_images_noise * 100)  # Menghitung persentase progress
            self.progress_noise.emit(progress)
            self.msleep(100)  # Contoh simulasi proses yang sedang berjalan

        self.finished_noise.emit()