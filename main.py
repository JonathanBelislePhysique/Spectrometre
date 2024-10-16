import sys

from PyQt5 import QtGui, QtWidgets, QtCore
import cv2
import pyqtgraph as pg
import numpy as np
import json

from mylabelroi import MyLabelROI
from utils import lbl_coord_to_img_coord


with open('calibration.json') as f:
    parameters = json.load(f)

TOP_WAVELENGTH_NM = parameters["TOP_WAVELENGTH_NM"]
TOP_WAVELENGTH_PIXEL = parameters["TOP_WAVELENGTH_PIXEL"]
BOTTOM_WAVELENGTH_NM = parameters["BOTTOM_WAVELENGTH_NM"]
BOTTOM_WAVELENGTH_PIXEL = parameters["BOTTOM_WAVELENGTH_PIXEL"]
LBL_SIZE_X = 640
LBL_SIZE_Y = 480

class MainApp(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spectrometre - Technologie du genie physique - La Pocatiere')
        self.resize(1200, 500)
        self.timer = QtCore.QTimer()
        self.setup_ui()
        self.populate_camera_list()
        self.start_wavelength = TOP_WAVELENGTH_NM
        self.stop_wavelength = BOTTOM_WAVELENGTH_NM
        self.pixel_start = TOP_WAVELENGTH_PIXEL
        self.pixel_stop = BOTTOM_WAVELENGTH_PIXEL
        self.pixel_bottom = 0
        self.frame = None

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.lbl_image = MyLabelROI()
        self.btn_acquisition = QtWidgets.QPushButton('Acquisition caméra')
        self.btn_stop = QtWidgets.QPushButton('Arrêter')
        self.btn_quitter = QtWidgets.QPushButton('Quitter')
        self.btn_charger = QtWidgets.QPushButton('Charger fichier')
        self.btn_calibrer = QtWidgets.QPushButton('Calibrer')
        self.graph_spectre = pg.PlotWidget()
        self.lbl_wl_top = QtWidgets.QLabel('Longueur d\'onde haut')
        self.lbl_wl_bottom = QtWidgets.QLabel('Longueur d\'onde bas')
        self.spn_top = QtWidgets.QSpinBox()
        self.spn_bottom = QtWidgets.QSpinBox()
        self.cmb_camera = QtWidgets.QComboBox()
        self.btn_camera_connect = QtWidgets.QPushButton('Connecter')
        self.btn_camera_disconnect = QtWidgets.QPushButton('Déconnecter')


    def modify_widgets(self):
        css_file = "style.css"
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        styles = {'color': '#799b3e', 'font-size': '14px'}
        self.graph_spectre.setBackground('#232323')
        self.graph_spectre.setLabel(axis='left', text='Intensité (u.a.)', **styles)
        self.graph_spectre.setLabel('bottom', 'Longueur d\'onde (nm)', **styles)
        self.graph_spectre.showGrid(x=True, y=True)
        self.btn_acquisition.setDisabled(True)
        self.btn_quitter.setDisabled(False)
        self.btn_charger.setDisabled(False)
        self.btn_calibrer.setDisabled(True)
        self.btn_camera_connect.setDisabled(False)
        self.btn_camera_disconnect.setDisabled(True)
        self.btn_stop.setDisabled(True)
        self.spn_top.setMaximum(1000)
        self.spn_bottom.setMaximum(1000)
        self.spn_top.setValue(400)
        self.spn_bottom.setValue(700)
        self.lbl_image.setScaledContents(True)

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lbl_image, 0, 0, 1, 3)
        self.main_layout.addWidget(self.graph_spectre, 0, 3, 1, 3)
        self.main_layout.addWidget(self.btn_acquisition, 1, 0, 1, 1)
        self.main_layout.addWidget(self.btn_stop, 1, 1, 1, 1)
        self.main_layout.addWidget(self.btn_charger, 1, 2, 1, 1)
        self.main_layout.addWidget(self.cmb_camera, 1, 3, 1, 1)
        self.main_layout.addWidget(self.btn_camera_connect, 1, 4, 1, 1)
        self.main_layout.addWidget(self.btn_camera_disconnect, 1, 5, 1, 1)
        self.main_layout.addWidget(self.btn_quitter, 2, 5, 1, 1)
        self.main_layout.addWidget(self.lbl_wl_top, 2, 0, 1, 1)
        self.main_layout.addWidget(self.spn_top, 2, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_wl_bottom, 2, 2, 1, 1)
        self.main_layout.addWidget(self.spn_bottom, 2, 3, 1, 1)
        self.main_layout.addWidget(self.btn_calibrer, 2, 4, 1, 1)

    def setup_connections(self):
        self.btn_quitter.clicked.connect(self.btn_quitter_clicked)
        self.btn_stop.clicked.connect(self.btn_stop_clicked)
        self.btn_acquisition.clicked.connect(self.btn_acquisition_clicked)
        self.btn_charger.clicked.connect(self.btn_charger_clicked)
        self.btn_calibrer.clicked.connect(self.btn_calibrer_clicked)
        self.btn_camera_connect.clicked.connect(self.btn_camera_connect_clicked)
        self.btn_camera_disconnect.clicked.connect(self.btn_camera_disconnect_clicked)
        self.timer.timeout.connect(self.video_stream)

    def btn_camera_connect_clicked(self):
        self.btn_camera_connect.setDisabled(True)
        self.btn_camera_disconnect.setDisabled(False)
        self.btn_acquisition.setDisabled(False)
        self.connect_camera()

    def btn_camera_disconnect_clicked(self):
        self.btn_camera_connect.setDisabled(False)
        self.btn_camera_disconnect.setDisabled(True)
        self.btn_acquisition.setDisabled(True)
        self.disconnect_camera()

    def populate_camera_list(self):
        index = 0
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if not cap.isOpened():
                break
            self.cmb_camera.addItem(f"Camera {index}", index)
            cap.release()
            index += 1

    def connect_camera(self):
        self.video_size = QtCore.QSize(LBL_SIZE_X, LBL_SIZE_Y)
        self.capture = cv2.VideoCapture(self.cmb_camera.currentIndex(), cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

    def disconnect_camera(self):
        self.capture.release()

    def btn_charger_clicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self,
                                                                 caption='Ouvrir fichier',
                                                                 directory='.',
                                                                 filter='Image (*.jpg *.png *.bmp)')

        if filename:
            self.frame = cv2.imread(filename)
            print(filename)
            print(self.frame.shape)
            self.display_frame()
            self.update_graph()
            self.btn_calibrer.setDisabled(False)


    def btn_acquisition_clicked(self):
        self.btn_acquisition.setDisabled(True)
        self.btn_quitter.setDisabled(True)
        self.btn_charger.setDisabled(True)
        self.btn_calibrer.setDisabled(True)
        self.btn_camera_disconnect.setDisabled(True)
        self.btn_stop.setDisabled(False)
        self.timer.start(30)

    def btn_stop_clicked(self):
        self.btn_acquisition.setDisabled(False)
        self.btn_quitter.setDisabled(False)
        self.btn_charger.setDisabled(False)
        self.btn_calibrer.setDisabled(False)
        self.btn_camera_disconnect.setDisabled(False)
        self.btn_stop.setDisabled(True)
        self.timer.stop()

    def video_stream(self):
        _, self.frame = self.capture.read()
        self.display_frame()
        self.update_graph()

    def display_frame(self):
        frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
        print(frame.shape)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0],
                             frame.strides[0], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)
        pixmap = pixmap.scaled(LBL_SIZE_X, LBL_SIZE_Y)
        self.lbl_image.setPixmap(pixmap)

    def update_graph(self):
        roi_image = lbl_coord_to_img_coord(self.lbl_image.roi_draw_data,
                                           LBL_SIZE_X,
                                           LBL_SIZE_Y,
                                           self.frame.shape[1],
                                           self.frame.shape[0])

        image_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        mean_value = np.mean(image_gray[:, roi_image[0]:roi_image[2]], axis=1)
        self.graph_spectre.clear()
        self.pixel_bottom = mean_value.shape[0]
        wavelength = np.linspace(start=self.start_wavelength, stop=self.stop_wavelength, num=self.pixel_bottom)
        print(mean_value.shape)
        print(wavelength.shape)
        self.graph_spectre.plot(x=wavelength, y=mean_value, fillLevel=0, brush='r', pen='r')

    def btn_calibrer_clicked(self):
        self.calibrate()
        self.update_graph()

    def calibrate(self):
        roi_image = lbl_coord_to_img_coord(self.lbl_image.roi_draw_data,
                                           LBL_SIZE_X,
                                           LBL_SIZE_Y,
                                           self.frame.shape[1],
                                           self.frame.shape[0])
        pixel_top = roi_image[1]
        pixel_bottom = roi_image[3]
        wavelength_top = self.spn_top.value()
        wavelength_bottom = self.spn_bottom.value()
        self.pixel_stop = self.frame.shape[0]
        slope = (wavelength_bottom-wavelength_top)/(pixel_bottom-pixel_top)
        print(f'Slope :{slope}')
        self.start_wavelength = wavelength_top - slope*(pixel_top-self.pixel_start)
        self.stop_wavelength = wavelength_bottom + slope*(self.pixel_stop-pixel_bottom)
        print(f'self.frame.shape[1] :{self.frame.shape[1]}')
        print(f'self.frame.shape[0] :{self.frame.shape[0]}')
        print(f'pixel_top :{pixel_top}')
        print(f'pixel_bottom :{pixel_bottom}')
        print(f'self.start_wavelength :{self.start_wavelength}')
        print(f'self.stop_wavelength :{self.stop_wavelength}')
        print(f'self.pixel_start :{self.pixel_start}')
        print(f'self.pixel_stop :{self.pixel_stop}')


    def btn_quitter_clicked(self):
        self.close()

    def mouseMoveEvent(self, QMouseEvent):
        if self.lbl_image.roi_start_draw:
            self.drawRectangle()

    def drawRectangle(self):
        print(self.lbl_image.roi_draw_data)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())
