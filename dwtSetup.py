from PyQt5.QtCore import QThread, pyqtSignal
import dwtFunc as dwt

class dwtGen(QThread):
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
        startCom = "[DWT]Image Fusion Start..."
        self.startFusion.emit(startCom)
        self.generatedImage = dwt.fusion(self.folder_inputFusion1, self.folder_inputFusion2, self.outputNameFusion, self.extensionFileFusion, self.folder_fusionOutput_path)
        fusionPath = f"{self.folder_fusionOutput_path}/{self.outputNameFusion}.{self.extensionFileFusion}"   
        self.viewFusionOut.emit(fusionPath)
        finishCom = "[DWT]Image Fusion Finish"
        self.finishedFusion.emit(finishCom)
    