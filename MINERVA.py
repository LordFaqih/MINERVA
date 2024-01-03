import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QSplitter, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QFileDialog, QRadioButton, QGridLayout, QSlider, QLineEdit, QTextEdit, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie, QFont
from PyQt5 import QtWidgets, QtCore
from qtawesome import icon
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
import os 
import cv2
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from reconSetup import RecImg
from sinoSetup import SinoGen
from normSetup import NormImg
from noiseSetup import NoiseGen
from dwtSetup import dwtGen
import glob
import re
class LoadingPage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Mengatur ukuran jendela dan posisi tengah
        self.setGeometry(400, 200, 300, 300)
        #self.setFixedSize(1000, 1000)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Loading Page")

        self.loading_widget = QWidget()
        self.loading_widget.setStyleSheet("background-color: #ffffff")
        self.loading_layout = QGridLayout()

        #top_layout.setContentsMargins(0,0,0,0)
        self.loading_layout.setAlignment(Qt.AlignTop)
        self.loading_widget.setLayout(self.loading_layout)
        self.setCentralWidget(self.loading_widget)

        # Menambahkan label untuk menampilkan animasi
        self.loading_label = QLabel(self)
        self.loading_label.setGeometry(0, 0, 200, 200)
        self.loading_label.setAlignment(Qt.AlignCenter)

        # Membaca file animasi (misalnya, 'loading.gif')
        self.movie = QMovie('Images/Loading.gif')
        self.loading_label.setMovie(self.movie)
        self.loading_layout.addWidget(self.loading_label, 0, 0, Qt.AlignCenter)

        self.Qloading_label = QLabel("Loading...")
        self.Qloading_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #0e0e0e;")
        self.Qloading_label.setAlignment(Qt.AlignCenter)
        self.loading_layout.addWidget(self.Qloading_label, 1, 0, Qt.AlignCenter)

        # Mengatur timer untuk menunda animasi sebelum memulai
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_animation)
        self.timer.start(500)  # Menunggu setengah detik (500 ms) sebelum memulai animasi

    def start_animation(self):
        # Memulai animasi
        self.movie.start()

        # Mengatur timer untuk menunggu beberapa detik sebelum menampilkan jendela utama
        self.timer.timeout.disconnect(self.start_animation)
        self.timer.timeout.connect(self.show_main_window)
        self.timer.start(5000)  # Menunggu 5 detik (5000 ms) sebelum menampilkan jendela utama

    def show_main_window(self):
        # Menampilkan jendela utama
        self.main_window = MainWindow()
        self.main_window.resize(1366, 768)
        self.main_window.setWindowTitle("MINERVA V1.2")
        self.main_window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.main_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.main_window.setStyleSheet(style)
        self.main_window.show()

        # Menutup jendela loading
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Membuat tombol minimize, maximize, dan exit
        self.minimize_button = QtWidgets.QPushButton(icon('fa.minus', color='white'), "")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setObjectName("minimizeButton")

        self.maximize_button = QtWidgets.QPushButton(icon('fa.square-o', color='white'), "")
        self.maximize_button.clicked.connect(self.toggleMaximized)
        self.maximize_button.setObjectName("maximizeButton")

        self.exit_button = QtWidgets.QPushButton(icon('fa.times', color='white'), "")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setObjectName("exitButton")

        # Membuat QLabel untuk ikon dan nama perangkat lunak
        self.logo_label = QLabel(self)
        self.pixmap = QPixmap("Images/Sampel Minerva Logo.png")
        self.pixmap_resized = self.pixmap.scaled(40, 40)
        # Mengatur ikon menggunakan metode setPixmap()
        self.logo_label.setPixmap(self.pixmap_resized)
        # Mengatur nama perangkat lunak menggunakan metode setText()
        self.icon_label = QLabel(self)
        self.icon_label.setText("MINERVA")
        self.icon_label.setStyleSheet("font-size: 20pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb;")

        # Membuat tata letak horizontal untuk tombol-tombol
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.logo_label)
        self.button_layout.addWidget(self.icon_label)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.minimize_button)
        self.button_layout.addWidget(self.maximize_button)
        self.button_layout.addWidget(self.exit_button)

        # Membuat layout utama
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName('mainLayout')
        self.main_layout.addLayout(self.button_layout)
        # Membuat widget utama
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("centralWidget")
        self.central_widget.setStyleSheet("font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Membuat splitter utama
        self.main_splitter = QSplitter()
        self.main_splitter.setStyleSheet("QSplitter::handle { background-color: black; }, font-size: 14pt; font-family: Montserrat; color: #e4f0fb;")
        self.main_layout.addWidget(self.main_splitter)

        self.vertical_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.addWidget(self.vertical_splitter)

        # Membuat widget-layout atas
        self.top_widget = QWidget()
        self.top_widget.setStyleSheet("background-color: #1b2a32")
        self.top_layout = QVBoxLayout()
        #top_layout.setContentsMargins(0,0,0,0)
        self.top_layout.setAlignment(Qt.AlignTop)
        self.top_widget.setLayout(self.top_layout)
        self.top_label = QLabel("Select Mode:")
        self.top_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb;")
        self.top_layout.addWidget(self.top_label)
        self.vertical_splitter.addWidget(self.top_widget)

        self.radio_mode_widget = QWidget()
        self.top_layout.addWidget(self.radio_mode_widget)
        self.radio_mode_layout = QGridLayout()
        self.radio_mode_widget.setLayout(self.radio_mode_layout)

        # Mengatur efek bayangan pada widget

        # Membuat Radio Button dengan gaya kustom
        noise_button = QRadioButton("Noise Removal")
        noise_button.setFont(QFont("Montserrat", 8))
        noise_button.setObjectName("sqButton1")
        noise_button.setStyleSheet(style)
        noise_button.toggled.connect(self.show_noise_layout)

        # Membuat Radio Button dengan gaya kustom
        norm_button = QRadioButton("Normalize")
        norm_button.setFont(QFont("Montserrat", 8))
        norm_button.setObjectName("sqButton2")
        norm_button.setStyleSheet(style)
        norm_button.toggled.connect(self.show_norm_layout)

        # Membuat Radio Button dengan gaya kustom
        sino_button = QRadioButton("Generate Sinogram")
        sino_button.setFont(QFont("Montserrat", 8))
        sino_button.setObjectName("sqButton3")
        sino_button.setStyleSheet(style)
        sino_button.toggled.connect(self.show_sino_layout)

        # Membuat Radio Button dengan gaya kustom
        recon_button = QRadioButton("Reconstruction")
        recon_button.setFont(QFont("Montserrat", 8))
        recon_button.setObjectName("sqButton4")
        recon_button.setStyleSheet(style)
        recon_button.setChecked(True)
        recon_button.toggled.connect(self.show_recon_layout)

        # Membuat Radio Button dengan gaya kustom
        fusion_button = QRadioButton("Image Fusion")
        fusion_button.setFont(QFont("Montserrat", 8))
        fusion_button.setObjectName("sqButton5")
        fusion_button.setStyleSheet(style)
        fusion_button.toggled.connect(self.show_fusion_layout)

        # Membuat Radio Button dengan gaya kustom
        analyst_button = QRadioButton("Image Analysis")
        analyst_button.setFont(QFont("Montserrat", 8))
        analyst_button.setObjectName("sqButton6")
        analyst_button.setStyleSheet(style)
        analyst_button.toggled.connect(self.show_analyst_layout)

        # Membuat layout utama
        self.radio_mode_layout.addWidget(noise_button, 0, 0, Qt.AlignLeft)
        self.radio_mode_layout.addWidget(norm_button, 1, 0, Qt.AlignLeft)
        self.radio_mode_layout.addWidget(sino_button, 2, 0, Qt.AlignLeft)
        self.radio_mode_layout.addWidget(recon_button, 0, 1, Qt.AlignLeft)
        self.radio_mode_layout.addWidget(fusion_button, 1, 1, Qt.AlignLeft)
        self.radio_mode_layout.addWidget(analyst_button, 2, 1, Qt.AlignLeft)
        
        # Membuat widget-layout setting
        self.setting_widget = QWidget()
        self.setting_widget.setStyleSheet("background-color: #1b2a32")
        self.setting_layout = QVBoxLayout()
        #top_layout.setContentsMargins(0,0,0,0)
        self.setting_layout.setAlignment(Qt.AlignTop)
        self.setting_widget.setLayout(self.setting_layout)
        self.setting_label = QLabel("Setting:")
        self.setting_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb;")
        self.setting_layout.addWidget(self.setting_label)
        self.vertical_splitter.addWidget(self.setting_widget)

        # ANALYST SETTING MODE ############################################################################################################
        # Membuat widget-layout image analysis
        self.analyst_setting = QWidget()
        self.setting_layout.addWidget(self.analyst_setting)
        self.analyst_setting_layout = QGridLayout()
        self.analyst_setting.setLayout(self.analyst_setting_layout)
        self.analyst_setting_label = QLabel("Image Analysis Setting:")
        self.analyst_setting_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb; border-bottom: 5px solid #0091A1; padding-bottom: 5px;")
        self.analyst_setting_layout.addWidget(self.analyst_setting_label)
        self.analyst_setting.hide()

        ###################################################################################################################################

        # FUSION SETTING MODE #############################################################################################################
        # Membuat widget-layout image analysis
        self.fusion_setting = QWidget()
        self.setting_layout.addWidget(self.fusion_setting)
        self.fusion_setting_layout = QVBoxLayout()
        self.fusion_setting.setLayout(self.fusion_setting_layout)
        self.fusion_setting_label = QLabel("Fusion Method:")
        self.fusion_setting_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb; border-bottom: 5px solid #0091A1; padding-bottom: 5px;")
        self.fusion_setting_layout.addWidget(self.fusion_setting_label)
        self.fusion_setting.hide()

        self.radio_fusion_widget = QWidget()
        self.fusion_setting_layout.addWidget(self.radio_fusion_widget)
        self.radio_fusion_layout = QGridLayout()
        self.radio_fusion_widget.setLayout(self.radio_fusion_layout)

        # Membuat Radio Button dengan gaya kustom
        self.dwt_button = QRadioButton("DWT")
        self.dwt_button.setFont(QFont("Montserrat", 8))
        self.dwt_button.setObjectName("sqButton1")
        self.dwt_button.setStyleSheet(style)
        self.dwt_button.setChecked(True)
        self.dwt_button.toggled.connect(self.fusionMethod1)

        # Membuat Radio Button dengan gaya kustom
        self.vgg_button = QRadioButton("VGG19[Grayscale Only]")
        self.vgg_button.setFont(QFont("Montserrat", 8))
        self.vgg_button.setObjectName("sqButton1")
        self.vgg_button.setStyleSheet(style)
        self.vgg_button.toggled.connect(self.fusionMethod2)

        # Membuat Radio Button dengan gaya kustom
        self.dense_button = QRadioButton("DENSE FUSE")
        self.dense_button.setFont(QFont("Montserrat", 8))
        self.dense_button.setObjectName("sqButton1")
        self.dense_button.setStyleSheet(style)
        self.dense_button.setEnabled(False)
        self.dense_button.hide()
        self.dense_button.toggled.connect(self.fusionMethod3)

        # Membuat Radio Button dengan gaya kustom
        self.sesf_button = QRadioButton("SESF")
        self.sesf_button.setFont(QFont("Montserrat", 8))
        self.sesf_button.setObjectName("sqButton1")
        self.sesf_button.setStyleSheet(style)
        self.sesf_button.setEnabled(False)
        self.sesf_button.hide()
        self.sesf_button.toggled.connect(self.fusionMethod4)

        # Membuat layout utama
        self.radio_fusion_layout.addWidget(self.dwt_button, 0, 0, Qt.AlignLeft)
        self.radio_fusion_layout.addWidget(self.vgg_button, 1, 0, Qt.AlignLeft)
        self.radio_fusion_layout.addWidget(self.dense_button, 2, 0, Qt.AlignLeft)
        self.radio_fusion_layout.addWidget(self.sesf_button, 0, 1, Qt.AlignLeft)

        self.fusion_out_setting_label = QLabel("Output Folder Setting:")
        self.fusion_out_setting_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb; border-bottom: 5px solid #0091A1; padding-bottom: 5px;")
        self.fusion_setting_layout.addWidget(self.fusion_out_setting_label)

        

        self.change_name_fusion_widget = QWidget()
        self.fusion_setting_layout.addWidget(self.change_name_fusion_widget)
        self.change_name_fusion_layout = QVBoxLayout()
        self.change_name_fusion_widget.setLayout(self.change_name_fusion_layout)

        # Membuat Radio Button dengan gaya kustom
        self.change_name_fusion = QRadioButton("Change Output Name")
        self.change_name_fusion.setFont(QFont("Montserrat", 8))
        self.change_name_fusion.setObjectName("sqButton1")
        self.change_name_fusion.setStyleSheet(style)
        self.change_name_fusion.toggled.connect(self.ChangeFusionFunc)
        self.change_name_fusion_layout.addWidget(self.change_name_fusion)

        self.label_file_name_fusion = QLineEdit()
        self.label_file_name_fusion.setFixedSize(225,27)
        self.label_file_name_fusion.setPlaceholderText("File Name")
        self.label_file_name_fusion.setStyleSheet("background: #2C3E50")
        self.label_file_name_fusion.textChanged.connect(self.on_object_nameFusion_Changed)
        self.label_file_name_fusion.hide()
        self.label_file_name_fusion.setEnabled(False)
        #self.label_file_name.textChanged.connect(self.check_variables)
        self.fusion_setting_layout.addWidget(self.label_file_name_fusion)
        self.idx_change_name_fusion = None

        # Membuat tombol "Insert Folder"
        self.output_folder_fusion_button = QPushButton("Output Folder")
        self.output_folder_fusion_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.output_folder_fusion_button.setFixedSize(225,27)
        self.output_folder_fusion_button.clicked.connect(self.output_fusion_dialog)
        #self.output_folder_button.clicked.connect(self.check_variables)
        self.fusion_setting_layout.addWidget(self.output_folder_fusion_button)

        # Membuat QLabel untuk menampilkan direktori terpilih
        self.output_fusion_label = QLabel("Selected Folder: ")
        self.fusion_setting_layout.addWidget(self.output_fusion_label)
        # Variabel yang menyimpan direktori folder terpilih
        self.output_fusion_selected_folder = ""

        self.MetodeDWT = True
        self.MetodeVGG = False
        self.MetodeDENSE = False
        self.MetodeSESF = False

        self.idxFusionMethod = 1
        self.nameFusion = None
        self.outputFusion = None
        self.input1Fusion_idx = None
        self.input2Fusion_idx = None
        self.is_first_selection_fusion_output = True
        self.is_first_selection_fusion_input1Fusion = True
        self.is_first_selection_fusion_input2Fusion = True

        ###################################################################################################################################

        # RECON SETTING MODE ##############################################################################################################
        # Membuat widget-layout image analysis
        self.recon_setting = QWidget()
        #self.recon_setting.setStyleSheet("border: 1px solid")
        self.setting_layout.addWidget(self.recon_setting)
        self.recon_setting_layout = QVBoxLayout()
        self.recon_setting.setLayout(self.recon_setting_layout)
        self.recon_setting_label = QLabel("Recontruction Setting")
        self.recon_setting_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb; border-bottom: 5px solid #0091A1; padding-bottom: 5px;")
        self.recon_setting_layout.addWidget(self.recon_setting_label)
        

        # Membuat tombol "Insert Folder"
        self.insert_folder_button = QPushButton("Insert Folder")
        self.insert_folder_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.insert_folder_button.setFixedSize(225,27)
        self.insert_folder_button.clicked.connect(self.open_folder_dialog)
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.recon_setting_layout.addWidget(self.insert_folder_button)
        
        # Membuat QLabel untuk menampilkan direktori terpilih
        self.folder_label = QLabel("Selected Folder: ")
        self.recon_setting_layout.addWidget(self.folder_label)
        # Variabel yang menyimpan direktori folder terpilih
        self.selected_folder = ""

        self.radioNameRecWidget = QWidget()
        #self.recon_setting.setStyleSheet("border: 1px solid")
        self.recon_setting_layout.addWidget(self.radioNameRecWidget)
        self.radioNameReclayout = QVBoxLayout()
        self.radioNameRecWidget.setLayout(self.radioNameReclayout)

        # Membuat Radio Button dengan gaya kustom
        self.change_name_recon = QRadioButton("Change Output Name")
        self.change_name_recon.setFont(QFont("Montserrat", 8))
        self.change_name_recon.setObjectName("sqButton1")
        self.change_name_recon.setStyleSheet(style)
        self.change_name_recon.toggled.connect(self.ChangeReconFunc)
        self.radioNameReclayout.addWidget(self.change_name_recon)

        self.label_file_name = QLineEdit()
        self.label_file_name.setFixedSize(225,27)
        self.label_file_name.setPlaceholderText("File Name")
        self.label_file_name.setStyleSheet("background: #2C3E50")
        self.label_file_name.textChanged.connect(self.on_object_name_Changed)
        self.label_file_name.hide()
        self.label_file_name.setEnabled(False)
        #self.label_file_name.textChanged.connect(self.check_variables)
        self.recon_setting_layout.addWidget(self.label_file_name)
        self.idx_change_name_recon = None

        self.label_Theta = QLineEdit()
        self.label_Theta.setFixedSize(225,27)
        self.label_Theta.setPlaceholderText("Theta")
        self.label_Theta.setStyleSheet("background: #2C3E50")
        self.label_Theta.textChanged.connect(self.on_Theta_Changed)
        #self.label_Theta.textChanged.connect(self.check_variables)
        self.recon_setting_layout.addWidget(self.label_Theta)

        self.label_dTheta = QLineEdit()
        self.label_dTheta.setFixedSize(225,27)
        self.label_dTheta.setPlaceholderText("dTheta")
        self.label_dTheta.setStyleSheet("background: #2C3E50")
        self.label_dTheta.textChanged.connect(self.on_dTheta_Changed)
        #self.label_dTheta.textChanged.connect(self.check_variables)
        self.recon_setting_layout.addWidget(self.label_dTheta)

        # Membuat tombol "Insert Folder"
        self.output_folder_button = QPushButton("Output Folder")
        self.output_folder_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.output_folder_button.setFixedSize(225,27)
        self.output_folder_button.clicked.connect(self.output_folder_dialog)
        #self.output_folder_button.clicked.connect(self.check_variables)
        self.recon_setting_layout.addWidget(self.output_folder_button)

        # Membuat QLabel untuk menampilkan direktori terpilih
        self.output_folder_label = QLabel("Selected Folder: ")
        self.recon_setting_layout.addWidget(self.output_folder_label)
        # Variabel yang menyimpan direktori folder terpilih
        self.ouput_selected_folder = ""

        self.radioRotWidget = QWidget()
        #self.recon_setting.setStyleSheet("border: 1px solid")
        self.recon_setting_layout.addWidget(self.radioRotWidget)
        self.radioRotlayout = QVBoxLayout()
        self.radioRotWidget.setLayout(self.radioRotlayout)
        
        # Membuat Radio Button dengan gaya kustom
        self.change_rot_recon = QRadioButton("Change Rotation Point")
        self.change_rot_recon.setFont(QFont("Montserrat", 8))
        self.change_rot_recon.setObjectName("sqButton1")
        self.change_rot_recon.setStyleSheet(style)
        self.change_rot_recon.toggled.connect(self.ChangeRotReconFunc)
        self.radioRotlayout.addWidget(self.change_rot_recon)

        self.label_rot_point = QLineEdit()
        self.label_rot_point.setFixedSize(225,27)
        self.label_rot_point.setPlaceholderText("Rotation Point")
        self.label_rot_point.setStyleSheet("background: #2C3E50")
        self.label_rot_point.textChanged.connect(self.on_rot_point_Changed)
        #self.label_rot_point.hide()
        self.label_rot_point.setEnabled(False)
        #self.label_file_name.textChanged.connect(self.check_variables)
        self.recon_setting_layout.addWidget(self.label_rot_point)
        self.idx_change_rot_recon = None

        # Variabel untuk status variabel-variabel yang perlu diatur
        #self.recon_setting.hide()
        self.stepSinoValue = 0
        self.nameRecon = None
        self.thetaRecon = None
        self.dthetaRecon = None
        self.inputRecon = None
        self.outputRecon = None
        self.is_first_selection_recon_input = True
        self.is_first_selection_recon_output = True
        ###################################################################################################################################

        # SINO SETTING MODE ###############################################################################################################
        # Membuat widget-layout image analysis
        self.sino_setting = QWidget()
        self.setting_layout.addWidget(self.sino_setting)
        self.sino_setting_layout = QVBoxLayout()
        self.sino_setting.setLayout(self.sino_setting_layout)
        self.sino_setting_label = QLabel("Sinogram Setting")
        self.sino_setting_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb; border-bottom: 5px solid #0091A1; padding-bottom: 5px;")
        self.sino_setting_layout.addWidget(self.sino_setting_label)
        self.sino_setting.hide()

        # Membuat tombol "Insert Folder"
        self.input_sino_button = QPushButton("Input Folder")
        self.input_sino_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.input_sino_button.setFixedSize(225,27)
        self.input_sino_button.clicked.connect(self.input_sino_dialog)
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.sino_setting_layout.addWidget(self.input_sino_button)

        # Membuat QLabel untuk menampilkan direktori terpilih
        self.input_sino_label = QLabel("Selected Folder: ")
        self.sino_setting_layout.addWidget(self.input_sino_label)
        # Variabel yang menyimpan direktori folder terpilih
        self.input_sino_selected_folder = ""

        # Membuat tombol "Insert Folder"
        self.output_sino_button = QPushButton("Output Folder")
        self.output_sino_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.output_sino_button.setFixedSize(225,27)
        self.output_sino_button.clicked.connect(self.output_sino_dialog)
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.sino_setting_layout.addWidget(self.output_sino_button)

        # Membuat QLabel untuk menampilkan direktori terpilih
        self.output_sino_label = QLabel("Selected Folder: ")
        self.sino_setting_layout.addWidget(self.output_sino_label)
        # Variabel yang menyimpan direktori folder terpilih
        self.output_sino_selected_folder = ""

        # Membuat Radio Button dengan gaya kustom
        self.change_name_sino = QRadioButton("Change Output Name")
        self.change_name_sino.setFont(QFont("Montserrat", 8))
        self.change_name_sino.setObjectName("sqButton1")
        self.change_name_sino.setStyleSheet(style)
        self.change_name_sino.toggled.connect(self.ChangeSinoFunc)
        self.sino_setting_layout.addWidget(self.change_name_sino)

        self.label_output_sino = QLineEdit(self)
        self.label_output_sino.setFixedSize(225,27)
        self.label_output_sino.setPlaceholderText("Output File Name")
        self.label_output_sino.textChanged.connect(self.on_object_nameSino_Changed)
        self.label_output_sino.hide()
        self.label_output_sino.setEnabled(False)
        self.sino_setting_layout.addWidget(self.label_output_sino)

        self.idx_change_name_sino = None

        # Membuat tombol "Insert Folder"
        self.start_sino_button = QPushButton("Generate Sinogram")
        self.start_sino_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.start_sino_button.setFixedSize(225,27)
        #self.start_sino_button.clicked.connect(self.open_folder_dialog)
        #self.start_sino_button.clicked.connect(self.on_input_folder_recon_Changed)
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.start_sino_button.clicked.connect(self.check_sino)
        self.start_sino_button.clicked.connect(self.start_sino_process)
        self.sino_setting_layout.addWidget(self.start_sino_button)

        self.nameSino = None
        self.inputSino = None
        self.outputSino = None
        self.is_first_selection_sino_input = True
        self.is_first_selection_sino_output = True
        
        ###################################################################################################################################

        # NORM SETTING MODE ###############################################################################################################
        # Membuat widget-layout image analysis
        self.norm_setting = QWidget()
        self.setting_layout.addWidget(self.norm_setting)
        self.norm_setting_layout = QVBoxLayout()
        self.norm_setting.setLayout(self.norm_setting_layout)
        self.norm_setting_label = QLabel("Normalize Setting")
        self.norm_setting_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb; border-bottom: 5px solid #0091A1; padding-bottom: 5px;")
        self.norm_setting_layout.addWidget(self.norm_setting_label)
        self.norm_setting.hide()

        # Membuat tombol "Insert Folder"
        self.input_norm_button = QPushButton("Input Folder")
        self.input_norm_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.input_norm_button.setFixedSize(225,27)
        self.input_norm_button.clicked.connect(self.input_norm_dialog)
        
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.norm_setting_layout.addWidget(self.input_norm_button)

        # Membuat QLabel untuk menampilkan direktori terpilih
        self.input_norm_label = QLabel("Selected Folder: ")
        self.norm_setting_layout.addWidget(self.input_norm_label)
        # Variabel yang menyimpan direktori folder terpilih
        self.input_norm_selected_folder = ""

        # Membuat tombol "Output Folder"
        self.output_norm_button = QPushButton("Output Folder")
        self.output_norm_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.output_norm_button.setFixedSize(225,27)
        self.output_norm_button.clicked.connect(self.output_norm_dialog)
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.norm_setting_layout.addWidget(self.output_norm_button)

        # Membuat QLabel untuk menampilkan direktori terpilih
        self.output_norm_label = QLabel("Selected Folder: ")
        self.norm_setting_layout.addWidget(self.output_norm_label)
        # Variabel yang menyimpan direktori folder terpilih
        self.output_norm_selected_folder = ""

        # Membuat Radio Button dengan gaya kustom
        self.change_name_norm = QRadioButton("Change Output Name")
        self.change_name_norm.setFont(QFont("Montserrat", 8))
        self.change_name_norm.setObjectName("sqButton1")
        self.change_name_norm.setStyleSheet(style)
        self.change_name_norm.toggled.connect(self.ChangeNormFunc)
        self.norm_setting_layout.addWidget(self.change_name_norm)

        self.label_output_norm = QLineEdit(self)
        self.label_output_norm.setFixedSize(225,27)
        self.label_output_norm.setPlaceholderText("Output File Name")
        self.label_output_norm.textChanged.connect(self.on_object_nameNorm_Changed)
        self.label_output_norm.hide()
        self.label_output_norm.setEnabled(False)
        self.norm_setting_layout.addWidget(self.label_output_norm)

        self.idx_change_name_norm = None
        # Membuat tombol "Insert Folder"
        self.start_norm_button = QPushButton("Normalize Images")
        self.start_norm_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.start_norm_button.setFixedSize(225,27)
        #self.start_sino_button.clicked.connect(self.open_folder_dialog)
        #self.start_sino_button.clicked.connect(self.on_input_folder_recon_Changed)
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.start_norm_button.clicked.connect(self.check_norm)
        self.start_norm_button.clicked.connect(self.start_norm_process)
        self.norm_setting_layout.addWidget(self.start_norm_button)

        self.nameNorm = None
        self.inputNorm = None
        self.outputNorm = None
        self.is_first_selection_norm_input = True
        self.is_first_selection_norm_output = True
        ###################################################################################################################################

        # NOISE SETTING MODE ##############################################################################################################
        # Membuat widget-layout image analysis
        self.noise_setting = QWidget()
        self.setting_layout.addWidget(self.noise_setting)
        self.noise_setting_layout = QVBoxLayout()
        self.noise_setting.setLayout(self.noise_setting_layout)
        self.noise_setting_label = QLabel("Noise Removal Setting")
        self.noise_setting_label.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb; border-bottom: 5px solid #0091A1; padding-bottom: 5px;")
        self.noise_setting_layout.addWidget(self.noise_setting_label)
        self.noise_setting.hide()

        # Membuat tombol "Insert Folder"
        self.input_noise_button = QPushButton("Input Folder")
        self.input_noise_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.input_noise_button.setFixedSize(225,27)
        self.input_noise_button.clicked.connect(self.input_noise_dialog)
        
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.noise_setting_layout.addWidget(self.input_noise_button)

        # Membuat QLabel untuk menampilkan direktori terpilih
        self.input_noise_label = QLabel("Selected Folder: ")
        self.noise_setting_layout.addWidget(self.input_noise_label)
        # Variabel yang menyimpan direktori folder terpilih
        self.input_noise_selected_folder = ""

        # Membuat tombol "Output Folder"
        self.output_noise_button = QPushButton("Output Folder")
        self.output_noise_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.output_noise_button.setFixedSize(225,27)
        self.output_noise_button.clicked.connect(self.output_noise_dialog)
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.noise_setting_layout.addWidget(self.output_noise_button)

        # Membuat QLabel untuk menampilkan direktori terpilih
        self.output_noise_label = QLabel("Selected Folder: ")
        self.noise_setting_layout.addWidget(self.output_noise_label)
        # Variabel yang menyimpan direktori folder terpilih
        self.output_noise_selected_folder = ""

        # Membuat Radio Button dengan gaya kustom
        self.change_name_noise = QRadioButton("Change Output Name")
        self.change_name_noise.setFont(QFont("Montserrat", 8))
        self.change_name_noise.setObjectName("sqButton1")
        self.change_name_noise.setStyleSheet(style)
        self.change_name_noise.toggled.connect(self.ChangeNoiseFunc)
        self.noise_setting_layout.addWidget(self.change_name_noise)

        self.label_output_noise = QLineEdit(self)
        self.label_output_noise.setFixedSize(225,27)
        self.label_output_noise.setPlaceholderText("Output File Name")
        self.label_output_noise.textChanged.connect(self.on_object_nameNoise_Changed)
        self.label_output_noise.hide()
        self.label_output_noise.setEnabled(False)
        self.noise_setting_layout.addWidget(self.label_output_noise)

        self.idx_change_name_noise = None
        # Membuat tombol "Insert Folder"
        self.start_noise_button = QPushButton("Remove Noise")
        self.start_noise_button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")
        self.start_noise_button.setFixedSize(225,27)
        #self.start_sino_button.clicked.connect(self.open_folder_dialog)
        #self.start_sino_button.clicked.connect(self.on_input_folder_recon_Changed)
        #self.insert_folder_button.clicked.connect(self.check_variables)
        self.start_noise_button.clicked.connect(self.check_noise)
        self.start_noise_button.clicked.connect(self.start_noise_process)
        self.noise_setting_layout.addWidget(self.start_noise_button)

        self.nameNoise = None
        self.inputNoise = None
        self.outputNoise = None
        self.is_first_selection_noise_input = True
        self.is_first_selection_noise_output = True
        ###################################################################################################################################

        # LOGO INSTITUSI ##################################################################################################################
        bottomLeft_widget = QWidget()
        bottomLeft_widget.setStyleSheet("background-color: #1b2a32")
        bottomLeft_layout = QGridLayout()
        bottomLeft_widget.setLayout(bottomLeft_layout)
        self.vertical_splitter.addWidget(bottomLeft_widget)
        
        bottomLeft_widget_bound = QWidget()
        bottomLeft_widget_bound.setFixedSize(500,140)
        #bottomLeft_widget_bound.setStyleSheet("border: 1px solid")
        bottomLeft_layout_bound = QGridLayout()
        bottomLeft_widget_bound.setLayout(bottomLeft_layout_bound)
        bottomLeft_layout.addWidget(bottomLeft_widget_bound)

        self.instituttion1_label = QLabel(self)
        bottomLeft_layout_bound.addWidget(self.instituttion1_label, 0, 0, Qt.AlignCenter)

        self.instituttion1_pixmap = QPixmap("Images/Ui.png")
        self.instituttion1_pixmap_resize = self.instituttion1_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.instituttion1_label.setPixmap(self.instituttion1_pixmap_resize)

        self.instituttion2_label = QLabel(self)
        bottomLeft_layout_bound.addWidget(self.instituttion2_label, 0, 1, Qt.AlignCenter)

        self.instituttion2_pixmap = QPixmap("Images/Alt_Logo_BRIN.png")
        self.instituttion2_pixmap_resize = self.instituttion2_pixmap.scaledToHeight(90)
        self.instituttion2_label.setPixmap(self.instituttion2_pixmap_resize)

        
        ###################################################################################################################################

        # Membuat splitter kiri-kanan
        self.vertical_splitter2 = QSplitter(Qt.Vertical)
        self.inner_splitter = QSplitter()
        self.main_splitter.addWidget(self.vertical_splitter2)

        # LAYOUT IMAGE ANALYSIS ###########################################################################################################
        # Membuat widget-layout image analysis
        self.analyst_widget = QWidget()
        self.analyst_widget.setStyleSheet("background-color: #1b2a32")
        self.analyst_layout = QGridLayout()
        self.analyst_widget.setLayout(self.analyst_layout)
        self.analyst_label = QLabel("Image Analysis Mode")
        self.analyst_layout.addWidget(self.analyst_label)
        self.vertical_splitter2.addWidget(self.analyst_widget)
        self.analyst_widget.hide()
        ###################################################################################################################################

        # LAYOUT FUSION ###################################################################################################################
        # Membuat widget-layout image fusion
        self.fusion_widget = QWidget()
        self.fusion_widget.setStyleSheet("background-color: #1b2a32")
        self.fusion_layout = QGridLayout()
        self.fusion_widget.setLayout(self.fusion_layout)
        self.vertical_splitter2.addWidget(self.fusion_widget)
        self.fusion_widget.hide()

        self.fusion_widget_grid1 = QWidget()
        self.fusion_widget_grid1.setFixedSize(800,500)
        #self.sino_widget_grid1.setStyleSheet("border: 1px solid")
        self.fusion_layout_grid1 = QGridLayout()
        self.fusion_layout_grid1.setContentsMargins(20,0,0,0)
        self.fusion_widget_grid1.setLayout(self.fusion_layout_grid1)
        self.fusion_layout.addWidget(self.fusion_widget_grid1, 0, 0, Qt.AlignCenter)

        # Membuat QLabel untuk menampilkan gambar
        self.inputFuse1 = QLabel(self)
        self.inputFuse1.setAlignment(Qt.AlignCenter)
        self.inputFuse1.setText("No Image")
        self.inputFuse1.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; font-family: Montserrat; font-weight: bold; font-size: 12pt;")
        self.inputFuse1.setScaledContents(True)
        self.inputFuse1.setFixedSize(170, 170)
        self.inputFuse1.setObjectName("Gambar Input Fuse 1")

        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.inputFuse1.setGraphicsEffect(self.shadow_effect)

        self.fusion_layout_grid1.addWidget(self.inputFuse1, 2, 0, Qt.AlignCenter)

        # Membuat QLabel untuk menampilkan gambar
        self.inputFuse2 = QLabel(self)
        self.inputFuse2.setAlignment(Qt.AlignCenter)
        self.inputFuse2.setText("No Image")
        self.inputFuse2.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; font-family: Montserrat; font-weight: bold; font-size: 12pt;")
        self.inputFuse2.setScaledContents(True)
        self.inputFuse2.setFixedSize(170, 170)
        self.inputFuse2.setObjectName("Gambar Input Fuse 2")
    
        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.inputFuse2.setGraphicsEffect(self.shadow_effect)

        self.fusion_layout_grid1.addWidget(self.inputFuse2, 5, 0, Qt.AlignCenter)

        self.fuse_tag1 = QLabel("Image 1:")
        self.fuse_tag1.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 12pt; background: #1b2a32;")
        self.fuse_tag1.setAlignment(Qt.AlignCenter)
        self.fuse_tag1.setFixedSize(180,27)
        self.fusion_layout_grid1.addWidget(self.fuse_tag1, 0, 0, Qt.AlignCenter)

        self.inputFuse1Button = QPushButton("Select Image")
        self.inputFuse1Button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")  # Terapkan gaya pada awalnya

        self.inputFuse1Button.setFixedSize(180,27)
        self.inputFuse1Button.clicked.connect(self.input1Fusion)
        self.fusion_layout_grid1.addWidget(self.inputFuse1Button, 1, 0, Qt.AlignCenter)

        self.original_pixmap_fuse1 = QPixmap("Images/Dummy/No Image.png")
        self.pixmap_fuse1 = self.original_pixmap_fuse1.scaled(1000, 1000, Qt.AspectRatioMode.KeepAspectRatio)

        self.fuse_tag2 = QLabel("Image 2:")
        self.fuse_tag2.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 12pt; background: #1b2a32;")
        self.fuse_tag2.setAlignment(Qt.AlignCenter)
        self.fuse_tag2.setFixedSize(180,27)
        self.fusion_layout_grid1.addWidget(self.fuse_tag2, 3, 0, Qt.AlignCenter)

        self.inputFuse2Button = QPushButton("Select Image")
        self.inputFuse2Button.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")  # Terapkan gaya pada awalnya

        self.inputFuse2Button.setFixedSize(180,27)
        self.inputFuse2Button.clicked.connect(self.input2Fusion)
        self.fusion_layout_grid1.addWidget(self.inputFuse2Button, 4, 0, Qt.AlignCenter)

        self.original_pixmap_fuse2 = QPixmap("Images/Dummy/No Image.png")
        self.pixmap_fuse2 = self.original_pixmap_fuse2.scaled(1000, 1000, Qt.AspectRatioMode.KeepAspectRatio)

        # Mengatur posisi QLabel (image_label) di tengah main window
        self.inputFuse1.setAlignment(Qt.AlignCenter)
        self.inputFuse1.setPixmap(self.pixmap_fuse1)

        self.inputFuse2.setAlignment(Qt.AlignCenter)
        self.inputFuse2.setPixmap(self.pixmap_fuse2)

        self.FuseButton = QPushButton("Fuse")
        self.FuseButton.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")  # Terapkan gaya pada awalnya

        self.FuseButton.setFixedSize(180,27)
        self.FuseButton.clicked.connect(self.check_fusion)
        self.FuseButton.clicked.connect(self.fusion_process)
        self.fusion_layout_grid1.addWidget(self.FuseButton, 1, 2, Qt.AlignCenter)

        # Membuat QLabel untuk menampilkan gambar
        self.Fuse = QLabel(self)
        self.Fuse.setAlignment(Qt.AlignCenter)
        self.Fuse.setText("No Image")
        self.Fuse.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; font-family: Montserrat; font-weight: bold; font-size: 12pt;")
        self.Fuse.setScaledContents(True)
        self.Fuse.setFixedSize(415, 415)
        self.Fuse.setObjectName("Gambar Fused")

        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.Fuse.setGraphicsEffect(self.shadow_effect)

        self.fusion_layout_grid1.addWidget(self.Fuse, 2, 2, 4, 1, Qt.AlignTop | Qt.AlignCenter)

        self.original_pixmap_fuse1 = QPixmap("Images/Dummy/No Image.png")
        self.pixmap_fuse1 = self.original_pixmap_fuse1.scaled(1000, 1000, Qt.AspectRatioMode.KeepAspectRatio)

        self.dummySpace3 = QWidget()
        #self.dummySpace1.setStyleSheet("border: 1px solid")
        self.dummySpace3_layout = QGridLayout()
        self.dummySpace3.setLayout(self.dummySpace3_layout)
        self.fusion_layout_grid1.addWidget(self.dummySpace3, 0, 1, 5, 1, Qt.AlignCenter)

        self.dummySpace4 = QWidget()
        #self.dummySpace1.setStyleSheet("border: 1px solid")
        self.dummySpace4_layout = QGridLayout()
        self.dummySpace4.setLayout(self.dummySpace4_layout)
        self.fusion_layout_grid1.addWidget(self.dummySpace4, 0, 3, 5, 1, Qt.AlignCenter)

        self.dummySpace5 = QWidget()
        #self.dummySpace1.setStyleSheet("border: 1px solid")
        self.dummySpace5_layout = QGridLayout()
        self.dummySpace5.setLayout(self.dummySpace5_layout)
        self.fusion_layout_grid1.addWidget(self.dummySpace5, 6, 1, Qt.AlignCenter)

        ###################################################################################################################################

        # LAYOUT REKONSTRUKSI #############################################################################################################
        # Membuat widget-layout rekonstruksi
        self.recon_widget = QWidget()
        self.recon_widget.setStyleSheet("background-color: #1b2a32")
        self.recon_layout = QGridLayout()
        self.recon_widget.setLayout(self.recon_layout)

        self.recon_widget_grid1 = QWidget()
        self.recon_widget_grid1.setFixedSize(270,300)
        #self.recon_widget_grid1.setStyleSheet("border: 1px solid")
        self.recon_layout_grid1 = QGridLayout()
        self.recon_widget_grid1.setLayout(self.recon_layout_grid1)
        self.recon_layout.addWidget(self.recon_widget_grid1, 1, 0, Qt.AlignCenter)

        self.RecSliceButton = QPushButton("Reconstruct Slice")
        self.RecSliceButton.setStyleSheet("background-color: #0091A1; font-size: 12pt; font-family: Montserrat; color: #EFF6F9;")  # Terapkan gaya pada awalnya

        self.RecSliceButton.setFixedSize(225,27)
        self.RecSliceButton.clicked.connect(self.rec_process)
        self.recon_layout_grid1.addWidget(self.RecSliceButton, 0, 1, Qt.AlignCenter)
        #self.RecSliceButton.clicked.connect(self.on_RecSliceButton_clicked)
        self.image_label = QLabel(self)
        self.image_label.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px;")
        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.image_label.setGraphicsEffect(self.shadow_effect)

        self.recon_layout_grid1.addWidget(self.image_label, 1, 1, Qt.AlignCenter)


        self.slider = QSlider(Qt.Vertical, self)  # Mengubah orientasi slider menjadi vertical
        self.slider.setFixedSize(20,230)
        self.recon_layout_grid1.addWidget(self.slider, 1, 0, Qt.AlignCenter)


        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedSize(225,27)
        self.line_edit.setStyleSheet("background: #1b2a32")
        self.recon_layout_grid1.addWidget(self.line_edit, 2, 1, Qt.AlignCenter)


        self.original_pixmap = QPixmap("Images/Dummy/No Image.png")
        self.pixmap = self.original_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.original_pixmap.height() - 1)  # Mengatur ukuran maksimum slider
        self.slider.valueChanged.connect(self.on_slider_value_changed)
        self.line_edit.textChanged.connect(self.on_line_edit_text_changed)

        self.slider_value = 0
        self.line_edit_value = 0

        # Mengatur posisi QLabel (image_label) di tengah main window
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(self.pixmap)

        self.vertical_splitter2.addWidget(self.recon_widget)

        self.recon_widget_grid2 = QWidget()
        self.recon_widget_grid2.setFixedSize(540,390)
        #self.recon_widget_grid2.setStyleSheet("border: 1px solid")
        self.recon_layout_grid2 = QGridLayout()
        self.recon_widget_grid2.setLayout(self.recon_layout_grid2)
        self.recon_layout.addWidget(self.recon_widget_grid2, 1, 1, Qt.AlignCenter)
        
        self.recon_widget_grid2_1 = QWidget()
        self.recon_widget_grid2_1.setFixedSize(540,300)
        #self.recon_widget_grid2_1.setStyleSheet("border: 1px solid")
        self.recon_layout_grid2_1 = QGridLayout()
        self.recon_layout_grid2_1.setAlignment(Qt.AlignCenter)
        self.recon_widget_grid2_1.setLayout(self.recon_layout_grid2_1)
        self.recon_layout_grid2.addWidget(self.recon_widget_grid2_1, 1, 1, Qt.AlignCenter)

        self.sino_tag = QLabel("Sinogram:")
        self.sino_tag.setAlignment(Qt.AlignCenter)
        self.sino_tag.setFixedSize(230,27)
        self.sino_tag.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 14pt; background: #1b2a32;")
        #self.Theta1.setStyleSheet("border: 1px solid #324f61; font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.recon_layout_grid2_1.addWidget(self.sino_tag, 0, 0, Qt.AlignCenter)

        self.Theta1 = QLineEdit()
        self.Theta1.setFixedHeight(27)
        self.Theta1.setFixedWidth(150)
        self.Theta1.setAlignment(Qt.AlignCenter)
        self.Theta1.setStyleSheet("background: #1b2a32; border: none; font-family: Montserrat; font-weight: bold; font-size: 14pt;")
        #self.Theta1.setStyleSheet("border: 1px solid #324f61; font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.Theta1.setReadOnly(True)
        self.recon_layout_grid2_1.addWidget(self.Theta1, 0, 2, Qt.AlignCenter)

        # Membuat QLabel untuk menampilkan gambar
        self.sino2_label = QLabel(self)
        self.sino2_label.setAlignment(Qt.AlignCenter)
        self.sino2_label.setText("No Image")
        self.sino2_label.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; font-family: Montserrat; font-weight: bold; font-size: 12pt;")
        self.sino2_label.setScaledContents(True)
        self.sino2_label.setFixedSize(210, 210)
        #self.image_label.move(500, 110)
        self.sino2_label.setObjectName("Gambar Rec")

        self.shadow_effect7 = QGraphicsDropShadowEffect()
        self.shadow_effect7.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect7.setBlurRadius(10)  # Radius blur
        self.shadow_effect7.setOffset(5, 5)  # Offset bayangan
        self.sino2_label.setGraphicsEffect(self.shadow_effect7)
        self.recon_layout_grid2_1.addWidget(self.sino2_label, 1, 0, Qt.AlignCenter)
        
        # Membuat QLabel untuk menampilkan gambar
        self.rec1_label = QLabel(self)
        self.rec1_label.setAlignment(Qt.AlignCenter)
        self.rec1_label.setText("No Image")
        self.rec1_label.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; font-family: Montserrat; font-weight: bold; font-size: 12pt;")
        self.rec1_label.setScaledContents(True)
        self.rec1_label.setFixedSize(210, 210)
        #self.image_label.move(500, 110)
        self.rec1_label.setObjectName("Gambar Rec")
        
        self.shadow_effect8 = QGraphicsDropShadowEffect()
        self.shadow_effect8.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect8.setBlurRadius(10)  # Radius blur
        self.shadow_effect8.setOffset(5, 5)  # Offset bayangan
        self.rec1_label.setGraphicsEffect(self.shadow_effect8)
        self.recon_layout_grid2_1.addWidget(self.rec1_label, 1, 2, Qt.AlignCenter)

        # Menambahkan progress bar
        self.rec_slice_progress_bar = QProgressBar()
        self.rec_slice_progress_bar.setFixedSize(230,27)
        #self.rec_slice_progress_bar.setStyleSheet("background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; QProgressBar::chunk { background-color: #0091A1; }")
        self.rec_slice_progress_bar.setStyleSheet("QProgressBar { background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; } QProgressBar::chunk { background-color: #0091A1; }")

        self.rec_slice_progress_bar.setAlignment(Qt.AlignCenter)
        self.recon_layout_grid2_1.addWidget(self.rec_slice_progress_bar, 2, 2, Qt.AlignCenter)


        #self.original2_pixmap = QPixmap("Images/Dummy/No Image.png")
        #self.pixmap2 = self.original2_pixmap.scaled(230, 230, Qt.AspectRatioMode.KeepAspectRatio)
        #self.line_edit_value2 = 0
        #self.sino2_label.setPixmap(self.pixmap2)

        #self.original3_pixmap = QPixmap("Images/Dummy/No Image.png")
        #self.pixmap3 = self.original3_pixmap.scaled(230, 230, Qt.AspectRatioMode.KeepAspectRatio)
        #self.rec1_label.setPixmap(self.pixmap3)

        #self.label_file_name = None
        #self.label_Theta = None
        #self.label_dTheta = None


        self.slider.valueChanged.connect(self.check_variables)
        self.line_edit.textChanged.connect(self.check_variables)
        self.RecSliceButton.clicked.connect(self.check_variables)
        ###################################################################################################################################
        
        # LAYOUT GENERATE SINOGRAM ########################################################################################################
        # Membuat widget-layout image fusion
        self.sino_widget = QWidget()
        self.sino_widget.setStyleSheet("background-color: #1b2a32")
        self.sino_layout = QGridLayout()
        self.sino_widget.setLayout(self.sino_layout)
        self.vertical_splitter2.addWidget(self.sino_widget)
        self.sino_widget.hide()

        self.sino_widget_grid1 = QWidget()
        self.sino_widget_grid1.setFixedSize(800,400)
        #self.sino_widget_grid1.setStyleSheet("border: 1px solid")
        self.sino_layout_grid1 = QGridLayout()
        self.sino_widget_grid1.setLayout(self.sino_layout_grid1)
        self.sino_layout.addWidget(self.sino_widget_grid1, 1, 0, Qt.AlignCenter)

        self.projPrev1_tag = QLabel("Projection:")
        self.projPrev1_tag.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 14pt; background: #1b2a32")
        self.projPrev1_tag.setAlignment(Qt.AlignCenter)
        self.projPrev1_tag.setFixedSize(230,27)
        #self.Theta1.setStyleSheet("border: 1px solid #324f61; font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.sino_layout_grid1.addWidget(self.projPrev1_tag, 0, 0, Qt.AlignCenter)

        #self.RecSliceButton.clicked.connect(self.on_RecSliceButton_clicked)
        self.sino_input_image_label = QLabel(self)
        self.sino_input_image_label.setAlignment(Qt.AlignCenter)
        self.sino_input_image_label.setScaledContents(True)
        self.sino_input_image_label.setFixedSize(210, 210)
        self.sino_input_image_label.setText("No Image")
        self.sino_input_image_label.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; font-family: Montserrat; font-weight: bold; font-size: 12pt;")
        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.sino_input_image_label.setGraphicsEffect(self.shadow_effect)

        self.sino_layout_grid1.addWidget(self.sino_input_image_label, 1, 0, Qt.AlignCenter)

        self.sinoPrev1_tag = QLabel("Sinogram:")
        self.sinoPrev1_tag.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 14pt; background: #1b2a32")
        self.sinoPrev1_tag.setAlignment(Qt.AlignCenter)
        self.sinoPrev1_tag.setFixedSize(230,27)
        #self.Theta1.setStyleSheet("border: 1px solid #324f61; font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.sino_layout_grid1.addWidget(self.sinoPrev1_tag, 0, 1, Qt.AlignCenter)

        #self.RecSliceButton.clicked.connect(self.on_RecSliceButton_clicked)
        self.sino_output_image_label = QLabel(self)
        self.sino_output_image_label.setAlignment(Qt.AlignCenter)
        self.sino_output_image_label.setScaledContents(True)
        self.sino_output_image_label.setFixedSize(210, 210)
        self.sino_output_image_label.setText("No Image")
        self.sino_output_image_label.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; font-family: Montserrat; font-weight: bold; font-size: 12pt;")
        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.sino_output_image_label.setGraphicsEffect(self.shadow_effect)

        self.sino_layout_grid1.addWidget(self.sino_output_image_label, 1, 1, Qt.AlignCenter)

        self.sinoStatus_tag = QLabel("Status:")
        self.sinoStatus_tag.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 14pt; background: #1b2a32;")
        self.sinoStatus_tag.setAlignment(Qt.AlignCenter)
        self.sinoStatus_tag.setFixedSize(230,27)
        self.sino_layout_grid1.addWidget(self.sinoStatus_tag, 0, 2, Qt.AlignCenter)

        self.sinoStatus_log = QTextEdit()
        self.sinoStatus_log.setText("No Process Running")
        self.sinoStatus_log.setFixedHeight(30)
        self.sinoStatus_log.setFixedWidth(210)
        #self.sinoStatus_log.setAlignment(Qt.AlignCenter)
        self.sinoStatus_log.setStyleSheet("font-family: Montserrat; font-size: 10pt; background: #1b2a32; border: 1px solid #E9ECEF; border-radius: 5px;")
        #self.Theta1.setStyleSheet("border: 1px solid #324f61; font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.sinoStatus_log.setReadOnly(True)
        self.sino_layout_grid1.addWidget(self.sinoStatus_log, 1, 2, Qt.AlignTop)

        # Menambahkan progress bar
        self.sinoInput_progress_bar = QProgressBar()
        self.sinoInput_progress_bar.setFixedSize(230,27)
        #self.rec_slice_progress_bar.setStyleSheet("background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; QProgressBar::chunk { background-color: #0091A1; }")
        self.sinoInput_progress_bar.setStyleSheet("QProgressBar { background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; } QProgressBar::chunk { background-color: #0091A1; }")

        self.sinoInput_progress_bar.setAlignment(Qt.AlignCenter)
        self.sino_layout_grid1.addWidget(self.sinoInput_progress_bar, 2, 0, Qt.AlignCenter)

        # Menambahkan progress bar
        self.sino_progress_bar = QProgressBar()
        self.sino_progress_bar.setFixedSize(230,27)
        #self.rec_slice_progress_bar.setStyleSheet("background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; QProgressBar::chunk { background-color: #0091A1; }")
        self.sino_progress_bar.setStyleSheet("QProgressBar { background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; } QProgressBar::chunk { background-color: #0091A1; }")

        self.sino_progress_bar.setAlignment(Qt.AlignCenter)
        self.sino_layout_grid1.addWidget(self.sino_progress_bar, 2, 1, Qt.AlignCenter)
        ###################################################################################################################################

        # LAYOUT NORMALIZE ################################################################################################################
        # Membuat widget-layout normalize
        self.norm_widget = QWidget()
        self.norm_widget.setStyleSheet("background-color: #1b2a32")
        self.norm_layout = QGridLayout()
        self.norm_widget.setLayout(self.norm_layout)
        self.vertical_splitter2.addWidget(self.norm_widget)
        self.norm_widget.hide()

        self.norm_widget_grid1 = QWidget()
        self.norm_widget_grid1.setFixedSize(800,500)
        #self.sino_widget_grid1.setStyleSheet("border: 1px solid")
        self.norm_layout_grid1 = QGridLayout()
        self.norm_layout_grid1.setContentsMargins(20,0,0,0)
        self.norm_widget_grid1.setLayout(self.norm_layout_grid1)
        self.norm_layout.addWidget(self.norm_widget_grid1, 0, 0, Qt.AlignCenter)

        #self.RecSliceButton.clicked.connect(self.on_RecSliceButton_clicked)
        self.unNormImg = QLabel(self)
        self.unNormImg.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px;")
        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.unNormImg.setGraphicsEffect(self.shadow_effect)

        self.norm_layout_grid1.addWidget(self.unNormImg, 1, 1, Qt.AlignCenter)

        #self.RecSliceButton.clicked.connect(self.on_RecSliceButton_clicked)
        self.NormImg = QLabel(self)
        self.NormImg.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px;")
        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.NormImg.setGraphicsEffect(self.shadow_effect)

        self.norm_layout_grid1.addWidget(self.NormImg, 3, 1, Qt.AlignCenter)


        self.sliderNorm = QSlider(Qt.Vertical, self)  # Mengubah orientasi slider menjadi vertical
        self.sliderNorm.setFixedSize(20,180)
        self.norm_layout_grid1.addWidget(self.sliderNorm, 1, 0, Qt.AlignCenter)


        self.line_edit_Norm = QLineEdit(self)
        self.line_edit_Norm.setFixedSize(180,27)
        self.line_edit_Norm.setStyleSheet("background: #1b2a32")
        self.norm_layout_grid1.addWidget(self.line_edit_Norm, 4, 1, Qt.AlignCenter)

        self.unNorm_tag1 = QLabel("Before Normalize:")
        self.unNorm_tag1.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 12pt; background: #1b2a32;")
        self.unNorm_tag1.setAlignment(Qt.AlignCenter)
        self.unNorm_tag1.setFixedSize(180,27)
        self.norm_layout_grid1.addWidget(self.unNorm_tag1, 0, 1, Qt.AlignCenter)

        self.original_pixmap_unNorm = QPixmap("Images/Dummy/No Image.png")
        self.pixmap_unNorm = self.original_pixmap_unNorm.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio)
        self.sliderNorm.setMinimum(0)
        self.sliderNorm.setMaximum(self.original_pixmap.height() - 1)  # Mengatur ukuran maksimum slider
        self.sliderNorm.valueChanged.connect(self.on_sliderNorm_value_changed)
        self.line_edit_Norm.textChanged.connect(self.on_line_edit_Norm_text_changed)

        self.Norm_tag1 = QLabel("After Normalize:")
        self.Norm_tag1.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 12pt; background: #1b2a32;")
        self.Norm_tag1.setAlignment(Qt.AlignCenter)
        self.Norm_tag1.setFixedSize(180,27)
        self.norm_layout_grid1.addWidget(self.Norm_tag1, 2, 1, Qt.AlignCenter)

        self.original_pixmap_Norm = QPixmap("Images/Dummy/No Image.png")
        self.pixmap_Norm = self.original_pixmap_Norm.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio)

        self.sliderNorm_value = 0
        self.line_edit_Norm_value = 0

        # Mengatur posisi QLabel (image_label) di tengah main window
        self.unNormImg.setAlignment(Qt.AlignCenter)
        self.unNormImg.setPixmap(self.pixmap_unNorm)

        self.NormImg.setAlignment(Qt.AlignCenter)
        self.NormImg.setPixmap(self.pixmap_Norm)

        self.dummySpace1 = QWidget()
        #self.dummySpace1.setStyleSheet("border: 1px solid")
        self.dummySpace1_layout = QGridLayout()
        self.dummySpace1.setLayout(self.dummySpace1_layout)
        self.norm_layout_grid1.addWidget(self.dummySpace1, 0, 2, 4, 1, Qt.AlignCenter)
        
        self.dummySpace2 = QWidget()
        #self.dummySpace1.setStyleSheet("border: 1px solid")
        self.dummySpace2_layout = QGridLayout()
        self.dummySpace2.setLayout(self.dummySpace2_layout)
        self.norm_layout_grid1.addWidget(self.dummySpace2, 0, 4, 4, 1, Qt.AlignCenter)

        self.boxProfileUnNorm_widget = QWidget()
        self.boxProfileUnNorm_widget.setFixedSize(500,215)
        self.boxProfileUnNorm_widget.setStyleSheet("border: 1px solid")
        self.boxProfileUnNorm_layout = QGridLayout()
        self.boxProfileUnNorm_widget.setLayout(self.boxProfileUnNorm_layout)
        self.boxProfileUnNorm_widget.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px;")
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan
        self.boxProfileUnNorm_widget.setGraphicsEffect(self.shadow_effect)
        self.norm_layout_grid1.addWidget(self.boxProfileUnNorm_widget, 0, 3, 2, 1, Qt.AlignBottom | Qt.AlignLeft)

        self.boxProfileNorm_widget = QWidget()
        self.boxProfileNorm_widget.setFixedSize(500,215)
        self.boxProfileNorm_widget.setStyleSheet("border: 1px solid")
        self.boxProfileNorm_layout = QGridLayout()
        self.boxProfileNorm_widget.setLayout(self.boxProfileNorm_layout)
        self.boxProfileNorm_widget.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px;")
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan
        self.boxProfileNorm_widget.setGraphicsEffect(self.shadow_effect)
        self.norm_layout_grid1.addWidget(self.boxProfileNorm_widget, 2, 3, 2, 1, Qt.AlignBottom | Qt.AlignLeft)
        
        self.folder_selected_norm = False

        # Buat objek Figure dan Canvas untuk menampilkan plot
        self.profile1 = Figure()
        self.canvas1 = FigureCanvas(self.profile1)
        self.boxProfileUnNorm_layout.addWidget(self.canvas1)

        # Buat objek Figure dan Canvas untuk menampilkan plot
        self.profile2 = Figure()
        self.canvas2 = FigureCanvas(self.profile2)
        self.boxProfileNorm_layout.addWidget(self.canvas2)

        # Menambahkan progress bar
        self.norm_progress_bar = QProgressBar()
        self.norm_progress_bar.setFixedSize(500,27)
        #self.rec_slice_progress_bar.setStyleSheet("background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; QProgressBar::chunk { background-color: #0091A1; }")
        self.norm_progress_bar.setStyleSheet("QProgressBar { background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; } QProgressBar::chunk { background-color: #0091A1; }")

        self.norm_progress_bar.setAlignment(Qt.AlignCenter)
        self.norm_layout_grid1.addWidget(self.norm_progress_bar, 4, 3, Qt.AlignLeft)

        ###################################################################################################################################

        # LAYOUT NOISE REMOVAL ############################################################################################################
        # Membuat widget-layout noise removal
        self.noise_widget = QWidget()
        self.noise_widget.setStyleSheet("background-color: #1b2a32")
        self.noise_layout = QGridLayout()
        self.noise_widget.setLayout(self.noise_layout)
        self.vertical_splitter2.addWidget(self.noise_widget)
        self.noise_widget.hide()

        self.noise_widget_grid1 = QWidget()
        self.noise_widget_grid1.setFixedSize(800,500)
        #self.sino_widget_grid1.setStyleSheet("border: 1px solid")
        self.noise_layout_grid1 = QGridLayout()
        self.noise_widget_grid1.setLayout(self.noise_layout_grid1)
        self.noise_layout.addWidget(self.noise_widget_grid1, 1, 0, Qt.AlignCenter)

        self.noisePrev1_tag = QLabel("Before Noise Removal:")
        self.noisePrev1_tag.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 14pt; background: #1b2a32")
        self.noisePrev1_tag.setAlignment(Qt.AlignCenter)
        self.noisePrev1_tag.setFixedSize(230,27)
        #self.Theta1.setStyleSheet("border: 1px solid #324f61; font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.noise_layout_grid1.addWidget(self.noisePrev1_tag, 0, 0, Qt.AlignCenter)

        #self.RecSliceButton.clicked.connect(self.on_RecSliceButton_clicked)
        self.noise_input_image_label = QLabel(self)
        self.noise_input_image_label.setAlignment(Qt.AlignCenter)
        self.noise_input_image_label.setScaledContents(True)
        self.noise_input_image_label.setFixedSize(300, 300)
        self.noise_input_image_label.setText("No Image")
        self.noise_input_image_label.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; font-family: Montserrat; font-weight: bold; font-size: 12pt;")
        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.noise_input_image_label.setGraphicsEffect(self.shadow_effect)

        self.noise_layout_grid1.addWidget(self.noise_input_image_label, 1, 0, Qt.AlignCenter)

        self.noisePrev2_tag = QLabel("After Noise Removal:")
        self.noisePrev2_tag.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 14pt; background: #1b2a32")
        self.noisePrev2_tag.setAlignment(Qt.AlignCenter)
        self.noisePrev2_tag.setFixedSize(230,27)
        #self.Theta1.setStyleSheet("border: 1px solid #324f61; font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.noise_layout_grid1.addWidget(self.noisePrev2_tag, 0, 1, Qt.AlignCenter)

        #self.RecSliceButton.clicked.connect(self.on_RecSliceButton_clicked)
        self.noise_output_image_label = QLabel(self)
        self.noise_output_image_label.setAlignment(Qt.AlignCenter)
        self.noise_output_image_label.setScaledContents(True)
        self.noise_output_image_label.setFixedSize(300, 300)
        self.noise_output_image_label.setText("No Image")
        self.noise_output_image_label.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; font-family: Montserrat; font-weight: bold; font-size: 12pt;")
        # Membuat instance dari QGraphicsDropShadowEffect
        self.shadow_effect = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect.setBlurRadius(10)  # Radius blur
        self.shadow_effect.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.noise_output_image_label.setGraphicsEffect(self.shadow_effect)

        self.noise_layout_grid1.addWidget(self.noise_output_image_label, 1, 1, Qt.AlignCenter)

        self.fileNoiseProcessed = QLineEdit()
        self.fileNoiseProcessed.setText("No File")
        #self.fileNoiseProcessed.setFixedHeight(27)
        self.fileNoiseProcessed.setFixedWidth(695)
        self.fileNoiseProcessed.setAlignment(Qt.AlignCenter)
        self.fileNoiseProcessed.setStyleSheet("border:3px solid #E9ECEF; border-radius: 5px; background: #1b2a32; font-family: Montserrat; font-size: 14pt; padding: 5px;")
        #self.Theta1.setStyleSheet("border: 1px solid #324f61; font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.fileNoiseProcessed.setReadOnly(True)
        self.noise_layout_grid1.addWidget(self.fileNoiseProcessed, 2, 0, 1, 2, Qt.AlignCenter)

        self.noiseProcess_tag = QLabel("Process:")
        self.noiseProcess_tag.setStyleSheet("font-family: Montserrat; font-weight: bold; font-size: 14pt; background: #1b2a32")
        self.noiseProcess_tag.setAlignment(Qt.AlignCenter)
        self.noiseProcess_tag.setFixedSize(230,27)
        #self.Theta1.setStyleSheet("border: 1px solid #324f61; font-size: 10pt; font-family: Montserrat; color: #e4f0fb;")
        self.noise_layout_grid1.addWidget(self.noiseProcess_tag, 3, 0, 1, 2, Qt.AlignCenter)

        # Menambahkan progress bar
        self.noiseInput_progress_bar = QProgressBar()
        self.noiseInput_progress_bar.setFixedSize(695,35)
        #self.rec_slice_progress_bar.setStyleSheet("background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; QProgressBar::chunk { background-color: #0091A1; }")
        self.noiseInput_progress_bar.setStyleSheet("QProgressBar { background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF; font-size: 10pt; font-family: Montserrat; color: #e4f0fb; } QProgressBar::chunk { background-color: #0091A1; }")

        self.noiseInput_progress_bar.setAlignment(Qt.AlignCenter)
        self.noise_layout_grid1.addWidget(self.noiseInput_progress_bar, 4, 0, 1, 2, Qt.AlignCenter)

        ###################################################################################################################################

        # Membuat widget-layout kanan
        self.botomRight_widget = QWidget()
        self.botomRight_widget.setStyleSheet("background-color: #1b2a32")
        self.botomRight_layout = QGridLayout()
        self.botomRight_widget.setLayout(self.botomRight_layout)
        self.vertical_splitter2.addWidget(self.botomRight_widget)

        self.logTitle = QLabel("Log Box:")
        self.logTitle.setFixedSize(230,35)
        self.logTitle.setStyleSheet("font-size: 14pt; font-family: Montserrat; font-weight: bold; color: #e4f0fb; border-bottom: 5px solid #0091A1; padding-bottom: 5px;")
        self.logTitle.setAlignment(Qt.AlignCenter)
        self.botomRight_layout.addWidget(self.logTitle, 0, 0, Qt.AlignCenter)

        # Membuat textbox untuk menampilkan nama file yang sedang diproses
        self.textBoxLog = QTextEdit()
        self.textBoxLog.setFixedHeight(100)
        self.textBoxLog.setFixedWidth(800)
        self.textBoxLog.setStyleSheet("background: #2C3E50; border-radius: 10px; border: 3px solid #E9ECEF;")
        self.shadow_effect4 = QGraphicsDropShadowEffect()

        # Mengatur properti-properti efek bayangan
        self.shadow_effect4.setColor(QColor("#0091A1"))  # Warna bayangan (hitam)
        self.shadow_effect4.setBlurRadius(10)  # Radius blur
        self.shadow_effect4.setOffset(5, 5)  # Offset bayangan

        # Mengatur efek bayangan pada widget
        self.textBoxLog.setGraphicsEffect(self.shadow_effect4)
        self.textBoxLog.setReadOnly(True)
        self.botomRight_layout.addWidget(self.textBoxLog, 1, 0, Qt.AlignCenter)

        self.draggable = False
        self.resize_direction = None
        self.resize_start_position = None

    def show_noise_layout(self):
        self.noise_widget.show()
        self.norm_widget.hide()
        self.sino_widget.hide()
        self.recon_widget.hide()
        self.fusion_widget.hide()
        self.analyst_widget.hide()
        self.noise_setting.show()
        self.norm_setting.hide()
        self.sino_setting.hide()
        self.recon_setting.hide()
        self.fusion_setting.hide()
        self.analyst_setting.hide()

    def show_norm_layout(self):
        self.noise_widget.hide()
        self.norm_widget.show()
        self.sino_widget.hide()
        self.recon_widget.hide()
        self.fusion_widget.hide()
        self.analyst_widget.hide()
        self.noise_setting.hide()
        self.norm_setting.show()
        self.sino_setting.hide()
        self.recon_setting.hide()
        self.fusion_setting.hide()
        self.analyst_setting.hide()
    
    def show_sino_layout(self):
        self.noise_widget.hide()
        self.norm_widget.hide()
        self.sino_widget.show()
        self.recon_widget.hide()
        self.fusion_widget.hide()
        self.analyst_widget.hide()
        self.noise_setting.hide()
        self.norm_setting.hide()
        self.sino_setting.show()
        self.recon_setting.hide()
        self.fusion_setting.hide()
        self.analyst_setting.hide()

    def show_recon_layout(self):
        self.noise_widget.hide()
        self.norm_widget.hide()
        self.sino_widget.hide()
        self.recon_widget.show()
        self.fusion_widget.hide()
        self.analyst_widget.hide()
        self.noise_setting.hide()
        self.norm_setting.hide()
        self.sino_setting.hide()
        self.recon_setting.show()
        self.fusion_setting.hide()
        self.analyst_setting.hide()

    def show_fusion_layout(self):
        self.noise_widget.hide()
        self.norm_widget.hide()
        self.sino_widget.hide()
        self.recon_widget.hide()
        self.fusion_widget.show()
        self.analyst_widget.hide()
        self.noise_setting.hide()
        self.norm_setting.hide()
        self.sino_setting.hide()
        self.recon_setting.hide()
        self.fusion_setting.show()
        self.analyst_setting.hide()

    def show_analyst_layout(self):
        self.noise_widget.hide()
        self.norm_widget.hide()
        self.sino_widget.hide()
        self.recon_widget.hide()
        self.fusion_widget.hide()
        self.analyst_widget.show()
        self.noise_setting.hide()
        self.norm_setting.hide()
        self.sino_setting.hide()
        self.recon_setting.hide()
        self.fusion_setting.hide()
        self.analyst_setting.show()
            

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # Menentukan apakah harus menggeser jendela atau meresize
            window_rect = self.geometry()
            if event.pos().y() <= 30:  # Misalnya, menggunakan tinggi 30 pixel untuk area geser
                self.draggable = True
                self.drag_start_position = event.globalPos()
            elif event.pos().x() >= window_rect.width() - 5:
                self.resize_direction = "right"
                self.resize_start_position = event.globalPos()
            elif event.pos().x() <= 5:
                self.resize_direction = "left"
                self.resize_start_position = event.globalPos()
            elif event.pos().y() >= window_rect.height() - 5:
                self.resize_direction = "bottom"
                self.resize_start_position = event.globalPos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            if self.draggable:
                # Menggeser jendela
                diff = event.globalPos() - self.drag_start_position
                self.move(self.pos() + diff)
                self.drag_start_position = event.globalPos()
            elif self.resize_direction:
                # Meresize jendela
                diff = event.globalPos() - self.resize_start_position
                window_rect = self.geometry()

                if self.resize_direction == "right":
                    new_width = window_rect.width() + diff.x()
                    self.resize(new_width, window_rect.height())
                elif self.resize_direction == "left":
                    new_width = window_rect.width() - diff.x()
                    self.resize(new_width, window_rect.height())
                    self.move(self.x() + diff.x(), self.y())
                elif self.resize_direction == "bottom":
                    new_height = window_rect.height() + diff.y()
                    self.resize(window_rect.width(), new_height)
                self.resize_start_position = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # Mereset posisi klik awal dan arah resize
            self.draggable = False
            self.resize_direction = None
            self.resize_start_position = None

    
    ########################################################################################################################

    # FUNGSI ANALYSIS ######################################################################################################

    ########################################################################################################################

    # FUNGSI FUSION ########################################################################################################
    def fusionMethod1(self):
        self.MetodeDWT = True
        self.MetodeVGG = False
        self.MetodeDENSE = False
        self.MetodeSESF = False
        print(f"DWT:{self.MetodeDWT}")
        print(f"VGG:{self.MetodeVGG}")
        print(f"DENSE:{self.MetodeDENSE}")
        print(f"SESF:{self.MetodeSESF}")

    def fusionMethod2(self):
        self.MetodeDWT = False
        self.MetodeVGG = True
        self.MetodeDENSE = False
        self.MetodeSESF = False
        print(f"DWT:{self.MetodeDWT}")
        print(f"VGG:{self.MetodeVGG}")
        print(f"DENSE:{self.MetodeDENSE}")
        print(f"SESF:{self.MetodeSESF}")

    def fusionMethod3(self):
        self.MetodeDWT = False
        self.MetodeVGG = False
        self.MetodeDENSE = True
        self.MetodeSESF = False
        print(f"DWT:{self.MetodeDWT}")
        print(f"VGG:{self.MetodeVGG}")
        print(f"DENSE:{self.MetodeDENSE}")
        print(f"SESF:{self.MetodeSESF}")

    def fusionMethod4(self):
        self.MetodeDWT = False
        self.MetodeVGG = False
        self.MetodeDENSE = False
        self.MetodeSESF = True
        print(f"DWT:{self.MetodeDWT}")
        print(f"VGG:{self.MetodeVGG}")
        print(f"DENSE:{self.MetodeDENSE}")
        print(f"SESF:{self.MetodeSESF}")

    def output_fusion_dialog(self):
        if self.is_first_selection_fusion_output:
            self.fusion_dialogOutput1 = QFileDialog()
            self.fusion_dialogOutput1.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_fusionOutput_path1 = self.fusion_dialogOutput1.getExistingDirectory(self, "Select Folder") 
            if not self.folder_fusionOutput_path1:
                # Pengguna membatalkan pemilihan folder
                self.outputFusion = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputFusion)
                return
            self.outputFusion = 1
            self.is_first_selection_fusion_output = False
            self.folder_fusionOutput_path = self.folder_fusionOutput_path1
        else:
            self.fusion_dialogOutput2 = QFileDialog()
            self.fusion_dialogOutput2.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_fusionOutput_path2 = self.fusion_dialogOutput2.getExistingDirectory(self, "Select Folder") 
            if not self.folder_fusionOutput_path2:
                # Pengguna membatalkan pemilihan folder
                self.outputFusion = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputFusion)
                self.folder_fusionOutput_path = self.folder_fusionOutput_path1
                return
            self.outputFusion = 1
            self.folder_fusionOutput_path = self.folder_fusionOutput_path2

        # Memperbarui label dengan direktori terpilih
        self.output_fusion_selected_folder = self.folder_fusionOutput_path
        self.output_fusion_label.setText("Selected Folder: " + self.folder_fusionOutput_path)

    def ChangeFusionFunc(self, checked):
        if checked:
            self.label_file_name_fusion.show()
            self.label_file_name_fusion.setEnabled(True)
            self.idx_change_name_fusion = 1  
        else:
            self.label_file_name_fusion.hide()
            self.label_file_name_fusion.setEnabled(False)
            self.idx_change_name_fusion = None

    def input1Fusion(self):
        if self.is_first_selection_fusion_input1Fusion:
            self.file_dialog_input1Fusion1 = QFileDialog()
            self.file_dialog_input1Fusion1.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.tiff *.tif)")
            self.file_dialog_input1Fusion1.setFileMode(QFileDialog.ExistingFile)
            if not self.file_dialog_input1Fusion1.exec_():
                # Pengguna membatalkan pemilihan folder
                self.input1Fusion_idx = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                return
            self.input1Fusion_idx = 1
            self.is_first_selection_fusion_input1Fusion = False
            self.selected_file_input1Fusion = self.file_dialog_input1Fusion1.selectedFiles()[0]
            print(self.selected_file_input1Fusion)
        else:
            self.file_dialog_input1Fusion2 = QFileDialog()
            self.file_dialog_input1Fusion2.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.tiff *.tif)")
            self.file_dialog_input1Fusion2.setFileMode(QFileDialog.ExistingFile)
            if not self.file_dialog_input1Fusion2.exec_():
                # Pengguna membatalkan pemilihan folder
                self.input1Fusion_idx = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                self.selected_file_input1Fusion = self.file_dialog_input1Fusion1.selectedFiles()[0]
                print(self.selected_file_input1Fusion)
                return
            self.input1Fusion_idx = 1
            self.selected_file_input1Fusion = self.file_dialog_input1Fusion2.selectedFiles()[0]
            print(self.selected_file_input1Fusion)

        self.file_name_fusion_input = self.selected_file_input1Fusion.split('/')[-1].split('.')[0]
        self.file_extension_fusion_input1 = self.selected_file_input1Fusion.split('/')[-1].split('.')[1]

        self.show_input1Fusion(self.selected_file_input1Fusion)

    def show_input1Fusion(self, selected_file_input1Fusion):
        pixmapInput1Fusion = QPixmap(selected_file_input1Fusion)
        pixmapInput1Fusion = pixmapInput1Fusion.scaled(200, 200)
        self.inputFuse1.setPixmap(pixmapInput1Fusion)
        return

    def input2Fusion(self):
        if self.is_first_selection_fusion_input2Fusion:
            self.file_dialog_input2Fusion1 = QFileDialog()
            self.file_dialog_input2Fusion1.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.tiff *.tif)")
            self.file_dialog_input2Fusion1.setFileMode(QFileDialog.ExistingFile)
            if not self.file_dialog_input2Fusion1.exec_():
                # Pengguna membatalkan pemilihan folder
                self.input2Fusion_idx = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                return
            self.input2Fusion_idx = 1
            self.is_first_selection_fusion_input2Fusion = False
            self.selected_file_input2Fusion = self.file_dialog_input2Fusion1.selectedFiles()[0]
            print(self.selected_file_input2Fusion)
        else:
            self.file_dialog_input2Fusion2 = QFileDialog()
            self.file_dialog_input2Fusion2.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.tiff *.tif)")
            self.file_dialog_input2Fusion2.setFileMode(QFileDialog.ExistingFile)
            if not self.file_dialog_input2Fusion2.exec_():
                # Pengguna membatalkan pemilihan folder
                self.input2Fusion_idx = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                self.selected_file_input2Fusion = self.file_dialog_input2Fusion1.selectedFiles()[0]
                print(self.selected_file_input2Fusion)
                return
            self.input2Fusion_idx = 1
            self.selected_file_input2Fusion = self.file_dialog_input2Fusion2.selectedFiles()[0]
            print(self.selected_file_input2Fusion)

        self.file_name_fusion_input = self.selected_file_input1Fusion.split('/')[-1].split('.')[0]
        self.file_extension_fusion_input2 = self.selected_file_input1Fusion.split('/')[-1].split('.')[1]

        self.show_input2Fusion(self.selected_file_input2Fusion)

    def show_input2Fusion(self, selected_file_input2Fusion):
        pixmapInput2Fusion = QPixmap(selected_file_input2Fusion)
        pixmapInput2Fusion = pixmapInput2Fusion.scaled(200, 200)
        self.inputFuse2.setPixmap(pixmapInput2Fusion)
        return
    
    def on_object_nameFusion_Changed(self, text):
        if text:
            self.nameFusion = 1
        else:
            self.nameFusion = None
        print(self.nameFusion)

    def check_fusion(self):
        # Periksa apakah variabel-variabel yang perlu diatur sudah diatur
        if self.outputFusion is None or self.input1Fusion_idx is None or self.input2Fusion_idx is None:
            # Tampilkan pesan peringatan jika ada variabel yang belum diatur
            QMessageBox.warning(self, "Warning", "Please set all required variables before fuse image!")
            # Nonaktifkan slider dan input number
            return False
        else:
            #self.FuseButton.setEnabled(True)
            return True
        
    def check_extension_fusion(self):
        if self.file_extension_fusion_input1 != self.file_extension_fusion_input2:
            return False
        else:
            return True
       
    def fusion_process(self):
        if not self.check_fusion():
            return
        if not self.check_extension_fusion():
            return
        # Menonaktifkan tombol Start agar tidak dapat diklik selama proses berjalan
        self.inputFuse1Button.setEnabled(False)
        self.inputFuse2Button.setEnabled(False)
        self.FuseButton.setEnabled(False)
        self.change_name_fusion.setEnabled(False)
        self.label_file_name_fusion.setEnabled(False)
        self.output_folder_fusion_button.setEnabled(False)
        self.dwt_button.setEnabled(False)
        self.vgg_button.setEnabled(False)
        self.dense_button.setEnabled(False)
        self.sesf_button.setEnabled(False)

        self.extensionFileFusion = self.file_extension_fusion_input1

        self.folder_inputFusion1 = self.selected_file_input1Fusion
        self.folder_inputFusion2 = self.selected_file_input2Fusion
        self.folder_fusionOutput_path = self.folder_fusionOutput_path

        if self.idx_change_name_fusion is None:
            self.outputNameFusion = self.file_name_fusion_input
        else:
            if self.nameFusion is None:
                QMessageBox.warning(self, "Warning", "You select change name option. Please set output name before generate sinogram!")
                self.FuseButton.setEnabled(True)
                return False
            else:
                self.outputNameFusion = self.label_file_name_fusion.text()
                self.FuseButton.setEnabled(False)

        # Membersihkan textbox
        self.textBoxLog.clear()

        if self.MetodeDWT:
            self.dwt_gen = dwtGen(self.folder_inputFusion1, self.folder_inputFusion2, self.outputNameFusion, self.extensionFileFusion, self.folder_fusionOutput_path)
            self.dwt_gen.startFusion.connect(self.update_textbox)
            self.dwt_gen.viewFusionOut.connect(self.previewFusedImg)
            self.dwt_gen.finishedFusion.connect(self.update_textbox)
            self.dwt_gen.finishedFusion.connect(self.finishFuse)
            self.dwt_gen.start()

        if self.MetodeDENSE:
            #self.dense_gen = denseGen(self.folder_inputFusion1, self.folder_inputFusion2, self.outputNameFusion, self.extensionFileFusion, self.folder_fusionOutput_path)
            #self.dense_gen.startFusion.connect(self.update_textbox)
            #self.dense_gen.viewFusionOut.connect(self.previewFusedImg)
            #self.dense_gen.finishedFusion.connect(self.update_textbox)
            #self.dense_gen.finishedFusion.connect(self.finishFuse)
            #self.dense_gen.start()
            pass
        if self.MetodeSESF:
            pass
    def previewFusedImg(self, fusedPath):
        # Mengubah array gambar menjadi QImage
        fusedImg = QPixmap(fusedPath)
        fusedImg = fusedImg.scaled(1400, 1400)
        # Menampilkan gambar pada QLabel
        self.Fuse.setPixmap(fusedImg)
        # Memastikan pembaruan tampilan
        self.repaint()
    def finishFuse(self, fusedPath):
        self.inputFuse1Button.setEnabled(True)
        self.inputFuse2Button.setEnabled(True)
        self.FuseButton.setEnabled(True)
        self.change_name_fusion.setEnabled(True)
        self.label_file_name_fusion.setEnabled(True)
        self.output_folder_fusion_button.setEnabled(True)
        self.dwt_button.setEnabled(True)
        self.vgg_button.setEnabled(True)
        #self.dense_button.setEnabled(True)
        #self.sesf_button.setEnabled(True)
    ########################################################################################################################

    # FUNGSI RECON #########################################################################################################
    def open_folder_dialog(self):
        if self.is_first_selection_recon_input:
            self.recon_dialogInput1 = QFileDialog()
            self.recon_dialogInput1.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_reconInput_path1 = self.recon_dialogInput1.getExistingDirectory(self, "Select Folder") 
            if not self.folder_reconInput_path1:
                # Pengguna membatalkan pemilihan folder
                self.inputRecon = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder. Tolong pilih folder yang tepat')
                print(self.inputRecon)
                return
            bright_file_pattern = os.path.join(self.folder_reconInput_path1, "0Bright.*")
            dark_file_pattern = os.path.join(self.folder_reconInput_path1, "0Dark.*")
            bright_files = glob.glob(bright_file_pattern)
            dark_files = glob.glob(dark_file_pattern)
            if (bright_files or dark_files):
                QMessageBox.warning(self, 'Peringatan', 'File 0Bright.tiff atau 0Dark.tiff tidak diperlukan. Pilih folder lain yang tepat')
                return
            # Memeriksa apakah folder kosong
            if not os.listdir(self.folder_reconInput_path1):
                QMessageBox.warning(self, 'Peringatan', 'Folder yang dipilih kosong.')
                return
            self.inputRecon = 1
            self.is_first_selection_recon_input = False
            self.folder_reconInput_path = self.folder_reconInput_path1

        else:
            self.recon_dialogInput2 = QFileDialog()
            self.recon_dialogInput2.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_reconInput_path2 = self.recon_dialogInput2.getExistingDirectory(self, "Select Folder") 
            if not self.folder_reconInput_path2:
                # Pengguna membatalkan pemilihan folder
                self.inputRecon = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder. Tolong pilih folder yang tepat')
                print(self.inputRecon)
                self.folder_reconInput_path = self.folder_reconInput_path1
                return
            bright_file_pattern = os.path.join(self.folder_reconInput_path1, "0Bright.*")
            dark_file_pattern = os.path.join(self.folder_reconInput_path1, "0Dark.*")
            bright_files = glob.glob(bright_file_pattern)
            dark_files = glob.glob(dark_file_pattern)
            if (bright_files or dark_files):
                QMessageBox.warning(self, 'Peringatan', 'File 0Bright.tiff atau 0Dark.tiff tidak diperlukan. Pilih folder lain yang tepat')
                return
            if not os.listdir(self.folder_reconInput_path2):
                QMessageBox.warning(self, 'Peringatan', 'Folder yang dipilih kosong.')
                return
            self.inputRecon = 1
            self.folder_reconInput_path = self.folder_reconInput_path2

        configFile = (f"{self.folder_reconInput_path}/"+ "0Config.txt")
        config_file_path = os.path.join(self.folder_reconInput_path, '0config.txt')
        if not os.path.isfile(config_file_path):
            # File 0config.txt tidak ditemukan di dalam folder
            QMessageBox.warning(self, 'Peringatan', 'File config tidak ditemukan di dalam folder yang dipilih.')
            return
        
        file_list_recon = os.listdir(self.folder_reconInput_path)
        self.files_only_recon = [file for file in file_list_recon if os.path.isfile(os.path.join(self.folder_reconInput_path, file))]
        # Mengurutkan file berdasarkan nama
        sorted_files_recon = sorted(self.files_only_recon)

        self.file_count_recon = (len(self.files_only_recon))
        self.total_images_recon = self.file_count_recon
        print("total file:", self.total_images_recon)

        # Memeriksa apakah ada file dalam folder
        if len(sorted_files_recon) > 0:
            first_file_recon = sorted_files_recon[2]
            print(first_file_recon)
            # Menghapus nomor dalam nama file ketiga
            first_file_recon_re = re.sub(r'\d+', '', first_file_recon)

            print("Nama file sino (setelah penghapusan):", first_file_recon_re)
            self.file_name_recon = os.path.splitext(os.path.basename(first_file_recon_re))[0]
            print("Nama file:", self.file_name_recon)
            self.file_extension_recon = first_file_recon_re.split('.')[-1]
            print("Format file:", self.file_extension_recon)
        
        # Memperbarui label dengan direktori terpilih
        self.selected_folder = self.folder_reconInput_path
        self.folder_label.setText("Selected Folder: " + self.folder_reconInput_path)
        
        with open(configFile, 'r') as file:
            alamat_gambar = file.read().strip()
        self.change_image(alamat_gambar)
        return alamat_gambar

    def output_folder_dialog(self):
        if self.is_first_selection_recon_output:
            self.recon_dialogOutput1 = QFileDialog()
            self.recon_dialogOutput1.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_reconOutput_path1 = self.recon_dialogOutput1.getExistingDirectory(self, "Select Folder") 
            if not self.folder_reconOutput_path1:
                # Pengguna membatalkan pemilihan folder
                self.outputRecon = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputRecon)
                return
            self.outputRecon = 1
            self.is_first_selection_recon_output = False
            self.folder_reconOutput_path = self.folder_reconOutput_path1
        else:
            self.recon_dialogOutput2 = QFileDialog()
            self.recon_dialogOutput2.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_reconOutput_path2 = self.recon_dialogOutput2.getExistingDirectory(self, "Select Folder") 
            if not self.folder_reconOutput_path2:
                # Pengguna membatalkan pemilihan folder
                self.outputRecon = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputRecon)
                self.folder_reconOutput_path = self.folder_reconOutput_path1
                return
            self.outputRecon = 1
            self.folder_reconOutput_path = self.folder_reconOutput_path2

        # Memperbarui label dengan direktori terpilih
        self.output_selected_folder = self.folder_reconOutput_path
        self.output_folder_label.setText("Selected Folder: " + self.folder_reconOutput_path)
    
    def on_rot_point_Changed(self, text):
        if text == str((self.original_pixmap.width())/2):
            self.nameRecon = None
        else:
            self.nameRecon = 1
            
    def on_object_name_Changed(self, text):
        if text:
            self.nameRecon = 1
        else:
            self.nameRecon = None
        print(self.nameRecon)

    def on_Theta_Changed(self, text):
        if text:
            self.thetaRecon = 1
        else:
            self.thetaRecon = None
        print(self.thetaRecon)

    def on_dTheta_Changed(self, text):
        if text:
            self.dthetaRecon = 1
        else:
            self.dthetaRecon = None
        print(self.thetaRecon)

    def check_variables(self):
        # Periksa apakah variabel-variabel yang perlu diatur sudah diatur
        if self.inputRecon is None or self.outputRecon is None or self.thetaRecon is None or self.dthetaRecon is None:
            # Tampilkan pesan peringatan jika ada variabel yang belum diatur
            QMessageBox.warning(self, "Warning", "Please set all required variables before adjusting the slider or input number!")
            # Nonaktifkan slider dan input number
            return False
        else:
            #self.slider.setEnabled(True)
            #self.line_edit.setEnabled(True)
            #self.RecSliceButton.setEnabled(True)
            return True
        
    def ChangeReconFunc(self, checked):
        if checked:
            self.label_file_name.show()
            self.label_file_name.setEnabled(True)
            self.idx_change_name_recon = 1  
        else:
            self.label_file_name.hide()
            self.label_file_name.setEnabled(False)
            self.idx_change_name_recon = None
    def ChangeRotReconFunc(self, checked):
        if checked:
            #self.label_rot_point.show()
            self.label_rot_point.setEnabled(True)
            self.idx_change_rot_recon = 1  
        else:
            #self.label_rot_point.hide()
            self.label_rot_point.setEnabled(False)
            self.idx_change_rot_recon = None

    def change_image(self, alamat_gambar):
        self.original_pixmap = QPixmap(alamat_gambar) if os.path.isfile(alamat_gambar) else QPixmap("Images/Dummy/No Image.png")
        self.pixmap = self.original_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.label_rot_point.setText(str((self.original_pixmap.width())/2))
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.original_pixmap.height() - 1)  # Mengatur ukuran maksimum slider
        self.slider.valueChanged.connect(self.on_slider_value_changed)
        self.line_edit.textChanged.connect(self.on_line_edit_text_changed)

        self.slider_value = 0
        self.line_edit_value = 0

        # Mengatur posisi QLabel (image_label) di tengah main window
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(self.pixmap)
    
    def paintEvent(self, event):
        painter = QPainter(self.image_label.pixmap())
        painter.drawPixmap(0, 0, self.pixmap)

        # Menggambar garis pada pixmap
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)

        y = self.pixmap.height() - round((self.slider_value / (self.original_pixmap.height() - 1)) * self.pixmap.height())
        painter.drawLine(0, y, self.pixmap.width(), y)
        #self.sinogramLoad.emit(y)

    def on_slider_value_changed(self, value):
        # Periksa variabel-variabel yang perlu diatur
        if not self.check_variables():
            return
    
        self.slider_value = value
        self.line_edit_value = round(((self.original_pixmap.height() - 1) - value) / (self.original_pixmap.height() - 1) * (self.original_pixmap.height() - 1))
        
        folder_path = self.folder_reconInput_path
        objectName = self.file_name_recon
        idx = self.line_edit_value
        self.sinoIdx = idx
        sinogramData = (f"{folder_path}/"+ f"{objectName}{idx}.{self.file_extension_recon}")
        self.original_sino_pixmap = QPixmap(sinogramData) if os.path.isfile(sinogramData) else QPixmap("Images/Dummy/No Image.png")
        self.sino_pixmap = self.original_sino_pixmap.scaled(230, 230)
        #print(self.slider_value)
        #self.stepSinoValue = round((self.slider_value/self.original_pixmap.height())*360)

        self.sino2_label.setAlignment(Qt.AlignCenter)
        self.sino2_label.setPixmap(self.sino_pixmap)
        self.sino2_label.update()
        self.paintEventSino()
        self.line_edit.setText(str(self.line_edit_value))
        self.image_label.update()

    def on_line_edit_text_changed(self, text):
        # Periksa variabel-variabel yang perlu diatur
        if not self.check_variables():
            return
        try:
            self.line_edit_value = int(text)
        except ValueError:
            self.line_edit_value = 0
        self.slider_value = round(((self.original_pixmap.height() - 1) - self.line_edit_value) / (self.original_pixmap.height() - 1) * (self.original_pixmap.height() - 1))
        self.slider.setValue(self.slider_value)
        self.image_label.update()

    def rec_process(self):
        if not self.check_variables():
            return

        self.insert_folder_button.setEnabled(False)
        self.output_folder_button.setEnabled(False)
        self.RecSliceButton.setEnabled(False)
        self.slider.setEnabled(False)
        self.line_edit.setEnabled(False)
        self.change_name_recon.setEnabled(False)
        self.label_file_name.setEnabled(False)
        self.label_Theta.setEnabled(False)
        self.label_dTheta.setEnabled(False)
        self.change_rot_recon.setEnabled(False)
        self.label_rot_point.setEnabled(False)

        # Membersihkan textbox
        self.textBoxLog.clear()

        folder_path = self.folder_reconInput_path
        objectName = self.file_name_recon
        idx = self.line_edit_value
        sinogramData = (f"{folder_path}/"+ f"{objectName}{idx}.{self.file_extension_recon}")
        sinoPath = sinogramData

        if self.idx_change_name_recon is None:
            outputNameRecon = objectName
        else:
            if self.nameRecon is None:
                QMessageBox.warning(self, "Warning", "You select change name option. Please set output name before normalize images!")
                self.insert_folder_button.setEnabled(True)
                self.output_folder_button.setEnabled(True)
                self.RecSliceButton.setEnabled(True)
                self.slider.setEnabled(True)
                self.line_edit.setEnabled(True)
                self.change_name_recon.setEnabled(True)
                self.label_file_name.setEnabled(True)
                self.label_Theta.setEnabled(True)
                self.label_dTheta.setEnabled(True)
                self.change_rot_recon.setEnabled(True)
                self.label_rot_point.setEnabled(True)
                return False
            else:
                outputNameRecon = self.label_file_name.text()
                self.insert_folder_button.setEnabled(False)
                self.output_folder_button.setEnabled(False)
                self.RecSliceButton.setEnabled(False)
                self.slider.setEnabled(False)
                self.line_edit.setEnabled(False)
                self.change_name_recon.setEnabled(False)
                self.label_file_name.setEnabled(False)
                self.label_Theta.setEnabled(False)
                self.label_dTheta.setEnabled(False)
                self.change_rot_recon.setEnabled(False)
                self.label_rot_point.setEnabled(False)

        defaultRotation = (self.original_pixmap.width())/2
        
        if self.idx_change_rot_recon is None:
            rotPointRecon = defaultRotation
        else:
            if self.nameRecon is None:
                QMessageBox.warning(self, "Warning", "You select change name option. Please set output name before normalize images!")
                self.insert_folder_button.setEnabled(True)
                self.output_folder_button.setEnabled(True)
                self.RecSliceButton.setEnabled(True)
                self.slider.setEnabled(True)
                self.line_edit.setEnabled(True)
                self.change_name_recon.setEnabled(True)
                self.label_file_name.setEnabled(True)
                self.label_Theta.setEnabled(True)
                self.label_dTheta.setEnabled(True)
                self.change_rot_recon.setEnabled(True)
                self.label_rot_point.setEnabled(True)
                return False
            else:
                defaultRotation = self.label_rot_point.text()
                self.insert_folder_button.setEnabled(False)
                self.output_folder_button.setEnabled(False)
                self.RecSliceButton.setEnabled(False)
                self.slider.setEnabled(False)
                self.line_edit.setEnabled(False)
                self.change_name_recon.setEnabled(False)
                self.label_file_name.setEnabled(False)
                self.label_Theta.setEnabled(False)
                self.label_dTheta.setEnabled(False)
                self.change_rot_recon.setEnabled(False)
                self.label_rot_point.setEnabled(False)

        Theta = int(self.label_Theta.text())
        dTheta = int(self.label_dTheta.text())
        output_path = self.folder_reconOutput_path
        extensionRecon = self.file_extension_recon

        self.rec_gen = RecImg(Theta, dTheta, sinoPath, output_path, idx, outputNameRecon, extensionRecon, rotPointRecon)
        
        self.rec_gen.progress_updated_recon.connect(self.update_progress4)
        self.rec_gen.finished_recon.connect(self.process_finished4)

        self.rec_gen.thetaUpdate.connect(self.update_textbox)
        
        self.rec_gen.img_processed_recon.connect(self.update_image4)
        self.rec_gen.sudut.connect(self.update_status_sudut)
        self.rec_gen.stepSinoRead.connect(self.stepSinoReadFunc)
        # Memulai worker thread
        self.rec_gen.start()

    def paintEventSino(self):
        painter4 = QPainter(self.sino2_label.pixmap())
        painter4.drawPixmap(0, 0, self.sino_pixmap)

        # Menggambar garis pada pixmap
        pen4 = QPen(QColor(255, 0, 0))
        pen4.setWidth(2)
        painter4.setPen(pen4)

        x = round((self.stepSinoValue / (self.original_sino_pixmap.width() - 1)) * self.sino_pixmap.width())
        print("step:", self.stepSinoValue)
        print("ori:", self.original_sino_pixmap.width())
        print("pix:", self.sino_pixmap.width())
        print("nilai x:", x)
        painter4.drawLine(x, 0, x, self.sino_pixmap.height())
        #self.sinogramLoad.emit(y)

    def stepSinoReadFunc(self, value):
        self.stepSinoValue = value
        sinogramData = (f"{self.folder_reconInput_path}/"+ f"{self.file_name_recon}{self.sinoIdx}.{self.file_extension_recon}")
        self.original_sino_pixmap = QPixmap(sinogramData) if os.path.isfile(sinogramData) else QPixmap("Images/Dummy/No Image.png")
        self.sino_pixmap = self.original_sino_pixmap.scaled(230, 230)

        self.sino2_label.setAlignment(Qt.AlignCenter)
        self.sino2_label.setPixmap(self.sino_pixmap)
        self.sino2_label.update()
        self.paintEventSino()
        #print(self.stepSinoValue)
        self.sino2_label.update() 


    def update_progress4(self, value):
        # Memperbarui nilai progress bar
        self.rec_slice_progress_bar.setValue(value)

    def update_status_sudut(self, derajat):
        self.Theta1.clear()
        self.Theta1.setText(str(derajat))
    
    def process_finished4(self):
        self.update_textbox("Image Reconstruction Complete")
        self.insert_folder_button.setEnabled(True)
        self.output_folder_button.setEnabled(True)
        self.RecSliceButton.setEnabled(True)
        self.slider.setEnabled(True)
        self.line_edit.setEnabled(True)
        self.change_name_recon.setEnabled(True)
        self.label_file_name.setEnabled(True)
        self.label_Theta.setEnabled(True)
        self.label_dTheta.setEnabled(True)
        self.change_rot_recon.setEnabled(True)
        self.label_rot_point.setEnabled(True)
    
    def update_image4(self, recMatrixFolder):
        # Mengubah array gambar menjadi QImage
        pixmap3 = QPixmap(recMatrixFolder)
        pixmap3 = pixmap3.scaled(1400, 1400)
        # Menampilkan gambar pada QLabel
        self.rec1_label.setPixmap(pixmap3)
        # Memastikan pembaruan tampilan
        self.repaint()
    ########################################################################################################################

    # FUNGSI SINO ########################################################################################################## 
    def input_sino_dialog(self):
        if self.is_first_selection_sino_input:
            self.sino_dialogInput1 = QFileDialog()
            self.sino_dialogInput1.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_sinoInput_path1 = self.sino_dialogInput1.getExistingDirectory(self, "Select Folder") 
            if not self.folder_sinoInput_path1:
                # Pengguna membatalkan pemilihan folder
                self.inputSino = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder. Tolong pilih folder yang tepat')
                print(self.inputSino)
                return
            bright_file_pattern = os.path.join(self.folder_sinoInput_path1, "0Bright.*")
            dark_file_pattern = os.path.join(self.folder_sinoInput_path1, "0Dark.*")
            bright_files = glob.glob(bright_file_pattern)
            dark_files = glob.glob(dark_file_pattern)
            if (bright_files or dark_files):
                QMessageBox.warning(self, 'Peringatan', 'File 0Bright.tiff atau 0Dark.tiff tidak diperlukan. Pilih folder lain yang tepat')
                return
  
            config_file_path = os.path.join(self.folder_sinoInput_path1, '0config.txt')
            if os.path.isfile(config_file_path):
                # File 0config.txt tidak ditemukan di dalam folder
                QMessageBox.warning(self, 'Peringatan', 'File config ditemukan di dalam folder yang dipilih. File config tidak diperlukan dalam tahap ini. Tolong pilih folder lain.')
                return
            
            self.inputSino = 1
            self.is_first_selection_sino_input = False
            self.folder_sinoInput_path = self.folder_sinoInput_path1
        else:
            self.sino_dialogInput2 = QFileDialog()
            self.sino_dialogInput2.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_sinoInput_path2 = self.sino_dialogInput2.getExistingDirectory(self, "Select Folder") 
            if not self.folder_sinoInput_path2:
                # Pengguna membatalkan pemilihan folder
                self.inputSino = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder. Tolong pilih folder yang tepat')
                print(self.inputSino)
                self.folder_sinoInput_path = self.folder_sinoInput_path1
                return
            bright_file_pattern = os.path.join(self.folder_sinoInput_path2, "0Bright.*")
            dark_file_pattern = os.path.join(self.folder_sinoInput_path2, "0Dark.*")
            bright_files = glob.glob(bright_file_pattern)
            dark_files = glob.glob(dark_file_pattern)
            if (bright_files or dark_files):
                QMessageBox.warning(self, 'Peringatan', 'File 0Bright.tiff atau 0Dark.tiff tidak diperlukan. Pilih folder lain yang tepat')
                return
            config_file_path = os.path.join(self.folder_sinoInput_path2, '0config.txt')
            if os.path.isfile(config_file_path):
                # File 0config.txt tidak ditemukan di dalam folder
                QMessageBox.warning(self, 'Peringatan', 'File config ditemukan di dalam folder yang dipilih. File config tidak diperlukan dalam tahap ini. Tolong pilih folder lain.')
                return
            if not os.listdir(self.folder_sinoInput_path2):
                QMessageBox.warning(self, 'Peringatan', 'Folder yang dipilih kosong.')
                return
            self.inputSino = 1
            self.folder_sinoInput_path = self.folder_sinoInput_path2

        file_list_sino = os.listdir(self.folder_sinoInput_path)
        self.files_only_sino = [file for file in file_list_sino if os.path.isfile(os.path.join(self.folder_sinoInput_path, file))]
        # Mengurutkan file berdasarkan nama
        sorted_files_sino = sorted(self.files_only_sino)

        self.file_count_sino = (len(self.files_only_sino))
        self.total_images_sino = self.file_count_sino
        print("total file:", self.total_images_sino)

        # Memeriksa apakah ada file dalam folder
        if len(sorted_files_sino) > 0:
            first_file_sino = sorted_files_sino[0]
            print(first_file_sino)
            # Menghapus nomor dalam nama file ketiga
            first_file_sino_re = re.sub(r'\d+', '', first_file_sino)

            print("Nama file sino (setelah penghapusan):", first_file_sino_re)
            self.file_name_sino = os.path.splitext(os.path.basename(first_file_sino_re))[0]
            print("Nama file:", self.file_name_sino)
            self.file_extension_sino = first_file_sino_re.split('.')[-1]
            print("Format file:", self.file_extension_sino)

        # Memperbarui label dengan direktori terpilih
        self.input_sino_selected_folder = self.folder_sinoInput_path
        self.input_sino_label.setText("Selected Folder: " + self.input_sino_selected_folder)

    def output_sino_dialog(self):
        if self.is_first_selection_sino_output:
            self.sino_dialogOutput1 = QFileDialog()
            self.sino_dialogOutput1.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_sinoOutput_path1 = self.sino_dialogOutput1.getExistingDirectory(self, "Select Folder") 
            if not self.folder_sinoOutput_path1:
                # Pengguna membatalkan pemilihan folder
                self.outputSino = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputSino)
                return
            self.outputSino = 1
            self.is_first_selection_sino_output = False
            self.folder_sinoOutput_path = self.folder_sinoOutput_path1
        else:
            self.sino_dialogOutput2 = QFileDialog()
            self.sino_dialogOutput2.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_sinoOutput_path2 = self.sino_dialogOutput2.getExistingDirectory(self, "Select Folder") 
            if not self.folder_sinoOutput_path2:
                # Pengguna membatalkan pemilihan folder
                self.outputSino = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputSino)
                self.folder_sinoOutput_path = self.folder_sinoOutput_path1
                return
            self.outputSino = 1
            self.folder_sinoOutput_path = self.folder_sinoOutput_path2

        self.output_sino_selected_folder = self.folder_sinoOutput_path
        self.output_sino_label.setText("Selected Folder: " + self.output_sino_selected_folder)

    def on_object_nameSino_Changed(self, text):
        if text:
            self.nameSino = 1
        else:
            self.nameSino = None
        print(self.nameNorm)

    def check_sino(self):
        # Periksa apakah variabel-variabel yang perlu diatur sudah diatur
        if self.inputSino is None or self.outputSino is None:
            # Tampilkan pesan peringatan jika ada variabel yang belum diatur
            QMessageBox.warning(self, "Warning", "Please set all required variables before generating sinogram!")
            # Nonaktifkan slider dan input number
            return False
        else:
            #self.start_sino_button.setEnabled(True)
            return True
        
    def ChangeSinoFunc(self, checked):
        if checked:
            self.label_output_sino.show()
            self.label_output_sino.setEnabled(True)
            self.idx_change_name_sino = 1  
        else:
            self.label_output_sino.hide()
            self.label_output_sino.setEnabled(False)
            self.idx_change_name_sino = None

    def start_sino_process(self):
        if not self.check_sino():
            return
            
        # Menonaktifkan tombol Start agar tidak dapat diklik selama proses berjalan
        self.input_sino_button.setEnabled(False)
        self.output_sino_button.setEnabled(False)
        self.start_sino_button.setEnabled(False)
        self.change_name_sino.setEnabled(False)
        self.label_output_sino.setEnabled(False)

        folder_sinoInput_path = self.folder_sinoInput_path
        folder_sinoOutput_path = self.folder_sinoOutput_path

        if self.idx_change_name_sino is None:
            outputNameSino = self.file_name_sino
        else:
            if self.nameSino is None:
                QMessageBox.warning(self, "Warning", "You select change name option. Please set output name before generate sinogram!")
                self.start_sino_button.setEnabled(True)
                return False
            else:
                outputNameSino = self.label_output_sino.text()
                self.start_sino_button.setEnabled(False)

        # Membersihkan textbox
        self.textBoxLog.clear()
        self.sinoStatus_log.clear()
        self.sinoStatus_log.append("Import Images Process")
        inputNameSino = self.file_name_sino
        extensionSino = self.file_extension_sino
        total_images_sino = self.total_images_sino
        # Membuat worker thread untuk menjalankan proses
        self.sino_gen = SinoGen(folder_sinoInput_path, folder_sinoOutput_path, outputNameSino, inputNameSino, extensionSino, total_images_sino)
        self.sino_gen.progress_inputSino.connect(self.update_progress_InputSino)
        self.sino_gen.finishedInputSino.connect(self.process_finished_InputSino)

        self.sino_gen.progress_outputSino.connect(self.update_progress_OutputSino)
        self.sino_gen.finishedOutputSino.connect(self.process_finished_OutputSino)

        self.sino_gen.progress_statusSino.connect(self.update_progress_StatusSino)
        self.sino_gen.finishedStatusSino.connect(self.process_finished_StatusSino)

        self.sino_gen.file_InputSino.connect(self.update_textbox)
        self.sino_gen.file_OutputSino.connect(self.update_textbox)
        
        self.sino_gen.img_InputSino.connect(self.update_imageInputSino)
        self.sino_gen.img_OutputSino.connect(self.update_imageOutputSino)

        # Memulai worker thread
        self.sino_gen.start()
    def update_progress_InputSino(self, value):
        self.sinoInput_progress_bar.setValue(value)

    def update_progress_OutputSino(self, value):
        self.sino_progress_bar.setValue(value)
    
    def update_progress_StatusSino(self, value):
        self.sinoStatus_log.clear()
        self.update_imgStackStatus("Image Stack Loading...")

    def update_imgStackStatus(self, message):
        # Menambahkan pesan ke dalam QTextEdit
        self.sinoStatus_log.append(message)

    def process_finished_InputSino(self):
        self.update_textbox("Loading Normalized Image Complete")

    def process_finished_OutputSino(self):
        self.sinoStatus_log.clear()
        # Mengaktifkan kembali tombol Start setelah proses selesai
        self.input_sino_button.setEnabled(True)
        self.output_sino_button.setEnabled(True)
        self.start_sino_button.setEnabled(True)
        self.change_name_sino.setEnabled(True)
        self.label_output_sino.setEnabled(True)

        # Menampilkan pesan selesai pada output QTextEdit
        self.update_imgStackStatus("Sinogram Generation Complete")
        self.update_textbox("Proses generate sinogram selesai.")

    def process_finished_StatusSino(self):
        # Membersihkan textbox
        self.sinoStatus_log.clear()
        # Menampilkan pesan selesai pada output QTextEdit
        self.update_imgStackStatus("Image Stack Complete")

    def update_imageInputSino(self, img_path):
        # Mengubah array gambar menjadi QImage
        pixmapInputSino = QPixmap(img_path)
        pixmapInputSino = pixmapInputSino.scaled(1400, 1400)
        # Menampilkan gambar pada QLabel
        self.sino_input_image_label.setPixmap(pixmapInputSino)
        # Memastikan pembaruan tampilan
        self.repaint()

    def update_imageOutputSino(self, output_path_sino):
        # Mengubah array gambar menjadi QImage
        pixmapOutputSino = QPixmap(output_path_sino)
        pixmapOutputSino = pixmapOutputSino.scaled(1400, 1400)
        # Menampilkan gambar pada QLabel
        self.sino_output_image_label.setPixmap(pixmapOutputSino)
        # Memastikan pembaruan tampilan
        self.repaint()
    ########################################################################################################################

    # FUNGSI NORM ##########################################################################################################
    def input_norm_dialog(self):
        if self.is_first_selection_norm_input:
            self.norm_dialogInput1 = QFileDialog()
            self.norm_dialogInput1.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_normInput_path1 = self.norm_dialogInput1.getExistingDirectory(self, "Select Folder") 
            if not self.folder_normInput_path1:
                # Pengguna membatalkan pemilihan folder
                self.inputNorm = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder. Tolong pilih folder yang tepat')
                print(self.inputNorm)
                return
            bright_file_pattern = os.path.join(self.folder_normInput_path1, "0Bright.*")
            dark_file_pattern = os.path.join(self.folder_normInput_path1, "0Dark.*")
            bright_files = glob.glob(bright_file_pattern)
            dark_files = glob.glob(dark_file_pattern)
            if not (bright_files or dark_files):
                QMessageBox.warning(self, 'Peringatan', 'File 0Bright.tiff atau 0Dark.tiff tidak ditemukan. Pilih folder lain yang tepat')
                return
            config_file_path = os.path.join(self.folder_normInput_path1, '0config.txt')
            if os.path.isfile(config_file_path):
                # File 0config.txt tidak ditemukan di dalam folder
                QMessageBox.warning(self, 'Peringatan', 'File config ditemukan di dalam folder yang dipilih. File config tidak diperlukan dalam tahap ini. Tolong pilih folder lain.')
                return
            if not os.listdir(self.folder_normInput_path1):
                QMessageBox.warning(self, 'Peringatan', 'Folder yang dipilih kosong.')
                return
            self.inputNorm = 1
            self.is_first_selection_norm_input = False
            self.folder_normInput_path = self.folder_normInput_path1
        else:
            self.norm_dialogInput2 = QFileDialog()
            self.norm_dialogInput2.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_normInput_path2 = self.norm_dialogInput2.getExistingDirectory(self, "Select Folder") 
            if not self.folder_normInput_path2:
                # Pengguna membatalkan pemilihan folder
                self.inputNorm = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder. Tolong pilih folder yang tepat')
                print(self.inputNorm)
                self.folder_normInput_path = self.folder_normInput_path1
                return
            bright_file_pattern = os.path.join(self.folder_normInput_path2, "0Bright.*")
            dark_file_pattern = os.path.join(self.folder_normInput_path2, "0Dark.*")
            bright_files = glob.glob(bright_file_pattern)
            dark_files = glob.glob(dark_file_pattern)
            if not (bright_files or dark_files):
                QMessageBox.warning(self, 'Peringatan', 'File 0Bright.tiff atau 0Dark.tiff tidak ditemukan. Pilih folder lain yang tepat')
                return
            config_file_path = os.path.join(self.folder_normInput_path2, '0config.txt')
            if os.path.isfile(config_file_path):
                # File 0config.txt tidak ditemukan di dalam folder
                QMessageBox.warning(self, 'Peringatan', 'File config ditemukan di dalam folder yang dipilih. File config tidak diperlukan dalam tahap ini. Tolong pilih folder lain.')
                return
            if not os.listdir(self.folder_normInput_path2):
                QMessageBox.warning(self, 'Peringatan', 'Folder yang dipilih kosong.')
                return
            self.inputNorm = 1
            self.folder_normInput_path = self.folder_normInput_path2

        print(self.inputNorm)
        # Memperbarui label dengan direktori terpilih
        # Mendapatkan daftar file dalam folder
        file_list_norm = os.listdir(self.folder_normInput_path)
        self.files_only_norm = [file for file in file_list_norm if os.path.isfile(os.path.join(self.folder_normInput_path, file))]
        # Mengurutkan file berdasarkan nama
        sorted_files = sorted(self.files_only_norm)

        self.file_count_norm = (len(self.files_only_norm)-2)
        self.total_images_norm = self.file_count_norm
        print("total file:", self.total_images_norm)

        # Memeriksa apakah ada file dalam folder
        if len(sorted_files) > 0:
            bright_file = sorted_files[0]
            dark_file = sorted_files[1]
            first_file = sorted_files[2]
            print(first_file)
            # Menghapus nomor dalam nama file ketiga
            first_file_re = re.sub(r'\d+', '', first_file)

            print("Nama file ketiga (setelah penghapusan):", first_file_re)
            self.file_name_norm = os.path.splitext(os.path.basename(first_file_re))[0]
            print("Nama file:", self.file_name_norm)
            self.file_extension_norm = first_file_re.split('.')[-1]
            print("Format file:", self.file_extension_norm)

            first_file_path = os.path.join(self.folder_normInput_path, first_file)
            dark_file_path = os.path.join(self.folder_normInput_path, dark_file)
            bright_file_path = os.path.join(self.folder_normInput_path, bright_file)
  
        self.dark_file_path = dark_file_path
        self.bright_file_path = bright_file_path
        proj = cv2.imread(first_file_path, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
        darkImg = cv2.imread(dark_file_path, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
        brightImg = cv2.imread(bright_file_path, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)

        correction_factor = ((brightImg - darkImg) / np.mean(brightImg - darkImg)) * 65535

        if np.any(correction_factor == 0):
            correction_factor[correction_factor == 0] = 1

        img_corr = np.divide((proj - darkImg), correction_factor)
        img_corr = np.clip(img_corr, 0, 1)
        img_corr = np.uint16(img_corr * 65535)

        normPrev_folder_name = "Preview Normalize"
        normPrevPath = os.path.join("Images/Dummy", normPrev_folder_name)
        
        if not os.path.exists(normPrevPath):
            os.makedirs(normPrevPath)
            print(f"Folder '{normPrev_folder_name}' berhasil dibuat.")
        else:
            print(f"Folder '{normPrev_folder_name}' sudah ada.")
        
        normPrevFile = "normPrevFile.tiff"
        normPrevFile_path = os.path.join(normPrevPath, normPrevFile)

        self.first_file_path = first_file_path
        self.normPrevFile_path = normPrevFile_path

        print(normPrevFile_path)
        cv2.imwrite(normPrevFile_path, img_corr)

        self.change_image2(first_file_path)

        self.change_image3(normPrevFile_path)

        self.folder_selected_norm = True

        self.input_norm_selected_folder = self.folder_normInput_path
        self.input_norm_label.setText("Selected Folder: " + self.input_norm_selected_folder)
    
    def output_norm_dialog(self):
        if self.is_first_selection_norm_output:
            self.norm_dialogOutput1 = QFileDialog()
            self.norm_dialogOutput1.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_normOutput_path1 = self.norm_dialogOutput1.getExistingDirectory(self, "Select Folder") 
            if not self.folder_normOutput_path1:
                # Pengguna membatalkan pemilihan folder
                self.outputNorm = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputNorm)
                return
            self.outputNorm = 1
            self.is_first_selection_norm_output = False
            self.folder_normOutput_path = self.folder_normOutput_path1
        else:
            self.norm_dialogOutput2 = QFileDialog()
            self.norm_dialogOutput2.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_normOutput_path2 = self.norm_dialogOutput2.getExistingDirectory(self, "Select Folder") 
            if not self.folder_normOutput_path2:
                # Pengguna membatalkan pemilihan folder
                self.outputNorm = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputNorm)
                self.folder_normOutput_path = self.folder_normOutput_path1
                return
            self.outputNorm = 1
            self.folder_normOutput_path = self.folder_normOutput_path2

        self.output_norm_selected_folder = self.folder_normOutput_path
        self.output_norm_label.setText("Selected Folder: " + self.output_norm_selected_folder)

    def on_object_nameNorm_Changed(self, text):
        if text:
            self.nameNorm = 1
        else:
            self.nameNorm = None
        print(self.nameNorm)

    def check_norm(self):
        # Periksa apakah variabel-variabel yang perlu diatur sudah diatur
        if self.inputNorm is None or self.outputNorm is None:
            # Tampilkan pesan peringatan jika ada variabel yang belum diatur
            QMessageBox.warning(self, "Warning", "Please set all required variables before normalize images!")
            # Nonaktifkan slider dan input number
            print(self.inputNorm)
            print(self.outputNorm)
            print(self.nameNorm)
            return False
        else:
            #self.line_edit_Norm.setEnabled(True)
            #self.sliderNorm.setEnabled(True)
            #self.start_norm_button.setEnabled(True)
            return True
        
    def ChangeNormFunc(self, checked):
        if checked:
            self.label_output_norm.show()
            self.label_output_norm.setEnabled(True)
            self.idx_change_name_norm = 1  
        else:
            self.label_output_norm.hide()
            self.label_output_norm.setEnabled(False)
            self.idx_change_name_norm = None

    def start_norm_process(self):
        if not self.check_norm():
            return
        
        # Menonaktifkan tombol Start agar tidak dapat diklik selama proses berjalan
        self.sliderNorm.setEnabled(False)
        self.line_edit_Norm.setEnabled(False)
        self.start_norm_button.setEnabled(False)
        self.input_norm_button.setEnabled(False) 
        self.output_norm_button.setEnabled(False)
        self.change_name_norm.setEnabled(False)
        self.label_output_norm.setEnabled(False)

        # Membersihkan textbox
        self.textBoxLog.clear()
        self.update_textbox("Normalized Images Start")

        inputNormPath = self.folder_normInput_path
        outputNormPath = self.folder_normOutput_path
        
        if self.idx_change_name_norm is None:
            outputNameNorm = self.file_name_norm
        else:
            if self.nameNorm is None:
                QMessageBox.warning(self, "Warning", "You select change name option. Please set output name before normalize images!")
                self.sliderNorm.setEnabled(True)
                self.line_edit_Norm.setEnabled(True)
                self.start_norm_button.setEnabled(True)
                return False
            else:
                outputNameNorm = self.label_output_norm.text()
                print(outputNameNorm)
                self.sliderNorm.setEnabled(False)
                self.line_edit_Norm.setEnabled(False)
                self.start_norm_button.setEnabled(False)

            
        darkImgPath = self.dark_file_path
        brightImgPath = self.bright_file_path
        file_name_norm = self.file_name_norm
        file_extension_norm = self.file_extension_norm
        total_images_norm = self.total_images_norm

        # Membuat worker thread untuk menjalankan proses
        self.norm_gen = NormImg(inputNormPath, outputNormPath, outputNameNorm, darkImgPath, brightImgPath, file_name_norm, file_extension_norm, total_images_norm)
        self.norm_gen.progress_norm.connect(self.update_progress_norm)
        self.norm_gen.finished_norm.connect(self.process_finished_norm)

        self.norm_gen.file_norm.connect(self.update_textbox)
        
        self.norm_gen.img_input_norm.connect(self.update_imageInputNorm)
        self.norm_gen.img_output_norm.connect(self.update_imageOutputNorm)

        self.paintEventNorm()
        self.plot_line_profile1()
        self.plot_line_profile2()
        self.unNormImg.update()
        self.NormImg.update()

        # Memulai worker thread
        self.norm_gen.start()
    
    def update_progress_norm(self, value):
        self.norm_progress_bar.setValue(value)
    
    def process_finished_norm(self):
        self.update_textbox("Normalize Images Complete")
        #self.sliderNorm.setEnabled(True)
        #self.line_edit_Norm.setEnabled(True)
        self.start_norm_button.setEnabled(True)
        self.input_norm_button.setEnabled(True) 
        self.output_norm_button.setEnabled(True)
        self.change_name_norm.setEnabled(True)
        self.label_output_norm.setEnabled(True)


        self.sliderNorm_value = 0
        self.line_edit_Norm_value = 0  

        self.sliderNorm.valueChanged.connect(self.on_sliderNorm_value_changed)
        self.line_edit_Norm.textChanged.connect(self.on_line_edit_Norm_text_changed)
        self.paintEventNorm()
        self.plot_line_profile1()
        self.plot_line_profile2()
        self.unNormImg.update()
        self.NormImg.update()
    
    def change_image2(self, first_file):
        self.original_pixmap_unNorm = QPixmap(first_file) if os.path.isfile(first_file) else QPixmap("Images/Dummy/No Image.png")
        self.pixmap_unNorm = self.original_pixmap_unNorm.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        # Mengatur posisi QLabel (image_label) di tengah main window
        self.unNormImg.setAlignment(Qt.AlignCenter)
        self.unNormImg.setPixmap(self.pixmap_unNorm)

        self.sliderNorm.setMinimum(0)
        self.sliderNorm.setMaximum(self.original_pixmap_unNorm.height() - 1)  # Mengatur ukuran maksimum slider
        self.sliderNorm.valueChanged.connect(self.on_sliderNorm_value_changed)
        self.line_edit_Norm.textChanged.connect(self.on_line_edit_Norm_text_changed)

        self.sliderNorm_value = 0
        self.line_edit_Norm_value = 0

    def change_image3(self, normPrevPath):

        self.original_pixmap_Norm = QPixmap(normPrevPath) if os.path.isfile(normPrevPath) else QPixmap("Images/Dummy/No Image.png")
        self.pixmap_Norm = self.original_pixmap_Norm.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)

        # Mengatur posisi QLabel (image_label) di tengah main window
        self.NormImg.setAlignment(Qt.AlignCenter)
        self.NormImg.setPixmap(self.pixmap_Norm)

        self.sliderNorm.setMinimum(0)
        self.sliderNorm.setMaximum(self.original_pixmap_Norm.height() - 1)  # Mengatur ukuran maksimum slider
        self.sliderNorm.valueChanged.connect(self.on_sliderNorm_value_changed)
        self.line_edit_Norm.textChanged.connect(self.on_line_edit_Norm_text_changed)

        self.sliderNorm_value = 0
        self.line_edit_Norm_value = 0

    def update_imageInputNorm(self, img_path):
        self.original_pixmap_unNorm = QPixmap(img_path) if os.path.isfile(img_path) else QPixmap("Images/Dummy/No Image.png")
        self.pixmap_unNorm = self.original_pixmap_unNorm.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        # Mengatur posisi QLabel (image_label) di tengah main window
        self.unNormImg.setAlignment(Qt.AlignCenter)
        self.unNormImg.setPixmap(self.pixmap_unNorm)

        self.sliderNorm.setMinimum(0)
        self.sliderNorm.setMaximum(self.original_pixmap_unNorm.height() - 1)  # Mengatur ukuran maksimum slider
        self.sliderNorm.valueChanged.connect(self.on_sliderNorm_value_changed)
        self.line_edit_Norm.textChanged.connect(self.on_line_edit_Norm_text_changed)
        
        self.first_file_path = img_path
        self.plot_line_profile1()

    def update_imageOutputNorm(self, imgOutputPath):
        self.original_pixmap_Norm = QPixmap(imgOutputPath) if os.path.isfile(imgOutputPath) else QPixmap("Images/Dummy/No Image.png")
        self.pixmap_Norm = self.original_pixmap_Norm.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)

        # Mengatur posisi QLabel (image_label) di tengah main window
        self.NormImg.setAlignment(Qt.AlignCenter)
        self.NormImg.setPixmap(self.pixmap_Norm)

        self.sliderNorm.setMinimum(0)
        self.sliderNorm.setMaximum(self.original_pixmap_Norm.height() - 1)  # Mengatur ukuran maksimum slider
        self.sliderNorm.valueChanged.connect(self.on_sliderNorm_value_changed)
        self.line_edit_Norm.textChanged.connect(self.on_line_edit_Norm_text_changed)
        
        self.normPrevFile_path = imgOutputPath
        self.plot_line_profile2()

    def paintEventNorm(self):
        painterNorm = QPainter(self.unNormImg.pixmap())
        painterNorm.drawPixmap(0, 0, self.pixmap_unNorm)

        painterNorm2 = QPainter(self.NormImg.pixmap())
        painterNorm2.drawPixmap(0, 0, self.pixmap_Norm)

        penNorm2 = QPen(QColor(255, 0, 0))
        penNorm2.setWidth(2)
        painterNorm2.setPen(penNorm2)

        # Menggambar garis pada pixmap
        penNorm = QPen(QColor(255, 0, 0))
        penNorm.setWidth(2)
        painterNorm.setPen(penNorm)

        y = self.pixmap_unNorm.height() - round((self.sliderNorm_value / (self.original_pixmap_unNorm.height() - 1)) * self.pixmap_unNorm.height())
        painterNorm.drawLine(0, y, self.pixmap_unNorm.width(), y)

        y = self.pixmap_Norm.height() - round((self.sliderNorm_value / (self.original_pixmap_Norm.height() - 1)) * self.pixmap_Norm.height())
        painterNorm2.drawLine(0, y, self.pixmap_Norm.width(), y)

    def on_sliderNorm_value_changed(self, value):
        # Periksa variabel-variabel yang perlu diatur
        if not self.check_norm():
            return
    
        self.sliderNorm_value = value
        self.line_edit_Norm_value = round(((self.original_pixmap_unNorm .height() - 1) - value) / (self.original_pixmap_unNorm .height() - 1) * (self.original_pixmap_unNorm .height() - 1))
        
        self.line_edit_Norm.setText(str(self.line_edit_Norm_value))
        self.paintEventNorm()
        self.plot_line_profile1()
        self.plot_line_profile2()
        self.unNormImg.update()
        self.NormImg.update()

    def on_line_edit_Norm_text_changed(self, text):
        # Periksa variabel-variabel yang perlu diatur
        if not self.check_norm():
            return
        try:
            self.line_edit_Norm_value = int(text)
        except ValueError:
            self.line_edit_Norm_value = 0
        self.sliderNorm_value = round(((self.original_pixmap_unNorm.height() - 1) - self.line_edit_Norm_value) / (self.original_pixmap_unNorm.height() - 1) * (self.original_pixmap_unNorm.height() - 1))
        self.sliderNorm.setValue(self.sliderNorm_value)
        self.paintEventNorm()
        self.unNormImg.update()
        self.NormImg.update()

    def plot_line_profile1(self):
        if not self.folder_selected_norm:
            # Pengguna membatalkan pemilihan folder
            print("Silakan pilih folder terlebih dahulu.")
            return
        # Baca gambar menggunakan OpenCV
        self.profile1.clear()
        image1 = cv2.imread(self.first_file_path, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
        # Ambil line profile
        line_profile1 = image1[self.line_edit_Norm_value, :]

        # Buat plot menggunakan Matplotlib
        ax = self.profile1.add_subplot(111)
        ax.plot(line_profile1, color='red', linewidth=0.2)
        ax.set_xlabel('Posisi X', fontsize=8)
        ax.set_ylabel('Intensitas', fontsize=8)
        ax.set_title('Line Profile Before Normalize', fontsize=8)
        ax.tick_params(axis='both', labelsize=8)
        
        self.canvas1.draw()   
        self.paintEventNorm()
        self.unNormImg.update()
        self.NormImg.update()

    def plot_line_profile2(self):
        if not self.folder_selected_norm:
            # Pengguna membatalkan pemilihan folder
            print("Silakan pilih folder terlebih dahulu.")
            return
        # Baca gambar menggunakan OpenCV
        self.profile2.clear()
        image2 = cv2.imread(self.normPrevFile_path, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
        # Ambil line profile
        line_profile2 = image2[self.line_edit_Norm_value, :]

        # Buat plot menggunakan Matplotlib
        ax = self.profile2.add_subplot(111)
        ax.plot(line_profile2, color='red', linewidth=0.2)
        ax.set_xlabel('Posisi X', fontsize=8)
        ax.set_ylabel('Intensitas', fontsize=8)
        ax.set_title('Line Profile After Normalize', fontsize=8)
        ax.tick_params(axis='both', labelsize=8)
        
        self.canvas2.draw() 
        self.paintEventNorm()
        self.unNormImg.update()
        self.NormImg.update()
    ########################################################################################################################
    
    # FUNGSI NOISE ##########################################################################################################
    def input_noise_dialog(self):
        if self.is_first_selection_noise_input:
            self.noise_dialogInput1 = QFileDialog()
            self.noise_dialogInput1.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_noiseInput_path1 = self.noise_dialogInput1.getExistingDirectory(self, "Select Folder") 
            if not self.folder_noiseInput_path1:
                # Pengguna membatalkan pemilihan folder
                self.inputNoise = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.inputNoise)
                return
            # Memeriksa keberadaan file 0Bright.tiff dan 0Dark.tiff
            bright_file_pattern = os.path.join(self.folder_noiseInput_path1, "0Bright.*")
            dark_file_pattern = os.path.join(self.folder_noiseInput_path1, "0Dark.*")
            bright_files = glob.glob(bright_file_pattern)
            dark_files = glob.glob(dark_file_pattern)
            if not (bright_files or dark_files):
                QMessageBox.warning(self, 'Peringatan', 'File 0Bright.tiff atau 0Dark.tiff tidak ditemukan.')
                return
            config_file_path = os.path.join(self.folder_noiseInput_path1, '0config.txt')
            if os.path.isfile(config_file_path):
                # File 0config.txt tidak ditemukan di dalam folder
                QMessageBox.warning(self, 'Peringatan', 'File config ditemukan di dalam folder yang dipilih. File config tidak diperlukan dalam tahap ini. Tolong pilih folder lain.')
                return
            if not os.listdir(self.folder_noiseInput_path1):
                QMessageBox.warning(self, 'Peringatan', 'Folder yang dipilih kosong.')
                return
            self.inputNoise = 1
            self.is_first_selection_noise_input = False
            self.folder_noiseInput_path = self.folder_noiseInput_path1
        else:
            self.noise_dialogInput2 = QFileDialog()
            self.noise_dialogInput2.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_noiseInput_path2 = self.noise_dialogInput2.getExistingDirectory(self, "Select Folder") 
            if not self.folder_noiseInput_path2:
                # Pengguna membatalkan pemilihan folder
                self.inputNoise = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.inputNoise)
                self.folder_noiseInput_path = self.folder_noiseInput_path1
                return
            bright_file_pattern = os.path.join(self.folder_noiseInput_path2, "0Bright.*")
            dark_file_pattern = os.path.join(self.folder_noiseInput_path2, "0Dark.*")
            bright_files = glob.glob(bright_file_pattern)
            dark_files = glob.glob(dark_file_pattern)
            if not (bright_files or dark_files):
                QMessageBox.warning(self, 'Peringatan', 'File 0Bright.tiff atau 0Dark.tiff tidak ditemukan.')
                return
            config_file_path = os.path.join(self.folder_noiseInput_path2, '0config.txt')
            if os.path.isfile(config_file_path):
                # File 0config.txt tidak ditemukan di dalam folder
                QMessageBox.warning(self, 'Peringatan', 'File config ditemukan di dalam folder yang dipilih. File config tidak diperlukan dalam tahap ini. Tolong pilih folder lain.')
                return
            if not os.listdir(self.folder_noiseInput_path2):
                QMessageBox.warning(self, 'Peringatan', 'Folder yang dipilih kosong.')
                return
            self.inputNoise = 1
            self.folder_noiseInput_path = self.folder_noiseInput_path2

        file_list_noise = os.listdir(self.folder_noiseInput_path)
        self.files_only_noise = [file for file in file_list_noise if os.path.isfile(os.path.join(self.folder_noiseInput_path, file))]
        # Mengurutkan file berdasarkan nama
        sorted_files_noise = sorted(self.files_only_noise)

        self.file_count_noise = (len(self.files_only_noise))
        self.total_images_noise = self.file_count_noise
        print("total file:", self.total_images_noise)

        # Memeriksa apakah ada file dalam folder
        if len(sorted_files_noise) > 2:
            first_file_noise = sorted_files_noise[2]
            print(first_file_noise)
            # Menghapus nomor dalam nama file ketiga
            first_file_noise_re = re.sub(r'\d+', '', first_file_noise)

            print("Nama file sino (setelah penghapusan):", first_file_noise_re)
            self.file_name_noise = os.path.splitext(os.path.basename(first_file_noise_re))[0]
            print("Nama file:", self.file_name_noise)
            self.file_extension_noise = first_file_noise_re.split('.')[-1]
            print("Format file:", self.file_extension_noise)

        # Memperbarui label dengan direktori terpilih
        self.input_noise_selected_folder = self.folder_noiseInput_path
        self.input_noise_label.setText("Selected Folder: " + self.input_noise_selected_folder)

    def output_noise_dialog(self):
        if self.is_first_selection_noise_output:
            self.noise_dialogOutput1 = QFileDialog()
            self.noise_dialogOutput1.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_noiseOutput_path1 = self.noise_dialogOutput1.getExistingDirectory(self, "Select Folder") 
            if not self.folder_noiseOutput_path1:
                # Pengguna membatalkan pemilihan folder
                self.outputNoise = None
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputNoise)
                return
            self.outputNoise = 1
            self.is_first_selection_noise_output = False
            self.folder_noiseOutput_path = self.folder_noiseOutput_path1
        else:
            self.noise_dialogOutput2 = QFileDialog()
            self.noise_dialogOutput2.setFileMode(QFileDialog.DirectoryOnly)
            self.folder_noiseOutput_path2 = self.noise_dialogOutput2.getExistingDirectory(self, "Select Folder") 
            if not self.folder_noiseOutput_path2:
                # Pengguna membatalkan pemilihan folder
                self.outputNoise = 1
                QMessageBox.warning(self, 'Peringatan', 'Anda membatalkan pemilihan folder.')
                print(self.outputNoise)
                self.folder_noiseOutput_path = self.folder_noiseOutput_path1
                return
            self.outputNoise = 1
            self.folder_noiseOutput_path = self.folder_noiseOutput_path2

        self.output_noise_selected_folder = self.folder_noiseOutput_path
        self.output_noise_label.setText("Selected Folder: " + self.output_noise_selected_folder)

    def on_object_nameNoise_Changed(self, text):
        if text:
            self.nameNoise = 1
        else:
            self.nameNoise = None
        print(self.nameNoise)

    def check_noise(self):
        # Periksa apakah variabel-variabel yang perlu diatur sudah diatur
        if self.inputNoise is None or self.outputNoise is None:
            # Tampilkan pesan peringatan jika ada variabel yang belum diatur
            QMessageBox.warning(self, "Warning", "Please set all required variables before generating sinogram!")
            # Nonaktifkan slider dan input number
            return False
        else:
            #self.start_noise_button.setEnabled(True)
            return True
        
    def ChangeNoiseFunc(self, checked):
        if checked:
            self.label_output_noise.show()
            self.label_output_noise.setEnabled(True)
            self.idx_change_name_noise = 1  
        else:
            self.label_output_noise.hide()
            self.label_output_noise.setEnabled(False)
            self.idx_change_name_noise = None
    
    def start_noise_process(self):
        if not self.check_noise():
            return
            
        # Menonaktifkan tombol Start agar tidak dapat diklik selama proses berjalan
        self.input_noise_button.setEnabled(False)
        self.output_noise_button.setEnabled(False)
        self.start_noise_button.setEnabled(False)
        self.change_name_noise.setEnabled(False)
        self.label_output_noise.setEnabled(False)

        folder_noiseInput_path = self.folder_noiseInput_path
        folder_noiseOutput_path = self.folder_noiseOutput_path

        if self.idx_change_name_noise is None:
            outputNameNoise = self.file_name_noise
        else:
            if self.nameNoise is None:
                QMessageBox.warning(self, "Warning", "You select change name option. Please set output name before generate sinogram!")
                self.start_noise_button.setEnabled(True)
                return False
            else:
                outputNameNoise = self.label_output_noise.text()
                self.start_noise_button.setEnabled(False)

        # Membersihkan textbox
        self.textBoxLog.clear()
        inputNameNoise = self.file_name_noise
        extensionNoise = self.file_extension_noise
        total_images_noise = self.total_images_noise

        # Membuat worker thread untuk menjalankan proses
        self.noise_gen = NoiseGen(folder_noiseInput_path, folder_noiseOutput_path, outputNameNoise, inputNameNoise, extensionNoise, total_images_noise)
        self.noise_gen.progress_noise.connect(self.update_progress_noise)
        self.noise_gen.finished_noise.connect(self.process_finished_noise)
        self.noise_gen.file_noise.connect(self.update_textbox)
        self.noise_gen.file_noise.connect(self.update_file_noise_tag)
        self.noise_gen.img_input_noise.connect(self.update_imageInputNoise)
        self.noise_gen.img_output_noise.connect(self.update_imageOutputNoise)

        # Memulai worker thread
        self.noise_gen.start()

    def update_progress_noise(self, value):
        self.noiseInput_progress_bar.setValue(value)

    def process_finished_noise(self):
        self.update_textbox("Noise Removal Complete")
        #self.sliderNorm.setEnabled(True)
        #self.line_edit_Norm.setEnabled(True)
        self.input_noise_button.setEnabled(True)
        self.output_noise_button.setEnabled(True)
        self.start_noise_button.setEnabled(True)
        self.change_name_noise.setEnabled(True)
        self.label_output_noise.setEnabled(True)

        self.noise_input_image_label.update()
        self.noise_output_image_label.update()
    def update_file_noise_tag(self, text):
        self.fileNoiseProcessed.clear()
        self.fileNoiseProcessed.setText(str(text))
    def update_imageInputNoise(self, img_path):
        # Mengubah array gambar menjadi QImage
        pixmapInputNoise = QPixmap(img_path)
        pixmapInputNoise = pixmapInputNoise.scaled(600, 600)
        # Menampilkan gambar pada QLabel
        self.noise_input_image_label.setPixmap(pixmapInputNoise)
        # Memastikan pembaruan tampilan
        self.repaint()
    def update_imageOutputNoise(self, img_path):
        # Mengubah array gambar menjadi QImage
        pixmapInputNoise = QPixmap(img_path)
        pixmapInputNoise = pixmapInputNoise.scaled(600, 600)
        # Menampilkan gambar pada QLabel
        self.noise_output_image_label.setPixmap(pixmapInputNoise)
        # Memastikan pembaruan tampilan
        self.repaint()
    ########################################################################################################################
    
    def update_textbox(self, message):
        # Menambahkan pesan ke dalam QTextEdit
        self.textBoxLog.append(message)
    



# Mengatur gaya dengan QSS
style = """
    QMainWindow {
        background-color: #0f171c;
    }
    #label_file_name {
        background-color: #3498DB;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 8px;
    }

    #sqButton1::indicator,
    #sqButton2::indicator,
    #sqButton3::indicator,
    #sqButton4::indicator,
    #sqButton5::indicator,
    #sqButton6::indicator {
        width: 10px;
        height: 10px;
        border: 3px solid #E9ECEF;
        border-radius: 5px;
        font-size: 16pt;
    }
        
    #sqButton1::indicator:checked,
    #sqButton2::indicator:checked,
    #sqButton3::indicator:checked,
    #sqButton4::indicator:checked,
    #sqButton5::indicator:checked,
    #sqButton6::indicator:checked {
        background-color: #0091A1;
    }

    #top_widget {
        background-color: #34495E;
        border: 1px solid #fff;
        border-radius: 5px;
        padding: 10px;
        font-size: 20pt; 
        font-family: Montserrat; 
        color: #e4f0fb;
    }

    #contentLabel {
        color: white;
        font-size: 24px;
    }

    #minimizeButton, #maximizeButton, #exitButton {
        background-color: transparent;
        border: none;
        color: #fff;
        font-size: 20px;
        padding: 5px;
        margin-right: 5px;
        border-radius: 20px;
    }

    #minimizeButton:hover {
        background-color: #FFB845;  /* Warna kuning */
        border: 2px solid #FFB845;
        border-radius: 10px;
    }

    #maximizeButton:hover {
        background-color: #0091A1;  /* Warna hijau */
        border: 2px solid #0091A1;
        border-radius: 10px;
    }

    #exitButton:hover {
        background-color: #CC0038;  /* Warna merah */
        border: 2px solid #CC0038;
        border-radius: 10px;
    }

   
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loading_page = LoadingPage()
     # Mendapatkan ukuran layar desktop
    desktop = QtWidgets.QApplication.desktop()
    screen_rect = desktop.screenGeometry(desktop.primaryScreen())
    screen_center = screen_rect.center()

    # Menghitung posisi jendela loading yang tepat
    loading_rect = loading_page.geometry()
    loading_rect.moveCenter(screen_center)
    loading_page.setGeometry(loading_rect)
    
    loading_page.show()
    sys.exit(app.exec_())
