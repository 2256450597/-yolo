# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e1e2e, stop:1 #16213e);\n"
"}\n"
"\n"
"QStackedWidget {\n"
"    background-color: #0f1419;\n"
"    border-radius: 12px;\n"
"    border: 1px solid #2a2d3a;\n"
"}\n"
"\n"
"QLabel {\n"
"    background-color: #1a1d29;\n"
"    border: 2px solid #2a2d3a;\n"
"    border-radius: 8px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6366f1, stop:1 #4f46e5);\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 12px 24px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    min-height: 40px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #818cf8, stop:1 #6366f1);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4f46e5, stop:1 #4338ca);\n"
"}\n"
"\n"
"QComboBox {\n"
"    background-color: #1a1d29;\n"
"    color: #e0e7ff;"
                        "\n"
"    border: 2px solid #3b3f54;\n"
"    border-radius: 8px;\n"
"    padding: 10px 15px;\n"
"    font-size: 13px;\n"
"    min-height: 30px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border-color: #6366f1;\n"
"    background-color: #252837;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 30px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"    border-left: 5px solid transparent;\n"
"    border-right: 5px solid transparent;\n"
"    border-top: 6px solid #e0e7ff;\n"
"    margin-right: 8px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1a1d29;\n"
"    color: #e0e7ff;\n"
"    border: 2px solid #6366f1;\n"
"    border-radius: 8px;\n"
"    selection-background-color: #6366f1;\n"
"    selection-color: white;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #2a2d3a;\n"
"    height: 10px;\n"
"    background: #1a1d29;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background:"
                        " qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #818cf8, stop:1 #6366f1);\n"
"    border: 2px solid white;\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    margin: -6px 0;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a5b4fc, stop:1 #818cf8);\n"
"    width: 22px;\n"
"    height: 22px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #818cf8);\n"
"    border-radius: 5px;\n"
"}\n"
"")
        self.centralwidget_model = QWidget(MainWindow)
        self.centralwidget_model.setObjectName(u"centralwidget_model")
        self.mainVerticalLayout = QVBoxLayout(self.centralwidget_model)
        self.mainVerticalLayout.setSpacing(15)
        self.mainVerticalLayout.setObjectName(u"mainVerticalLayout")
        self.mainVerticalLayout.setContentsMargins(20, 20, 20, 20)
        self.stackedWidget = QStackedWidget(self.centralwidget_model)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, 500))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.orig_img_label = QLabel(self.page)
        self.orig_img_label.setObjectName(u"orig_img_label")
        self.orig_img_label.setMinimumSize(QSize(200, 200))
        self.orig_img_label.setAlignment(Qt.AlignCenter)
        self.orig_img_label.setScaledContents(False)

        self.horizontalLayout.addWidget(self.orig_img_label)

        self.det_img_label = QLabel(self.page)
        self.det_img_label.setObjectName(u"det_img_label")
        self.det_img_label.setMinimumSize(QSize(200, 200))
        self.det_img_label.setAlignment(Qt.AlignCenter)
        self.det_img_label.setScaledContents(False)

        self.horizontalLayout.addWidget(self.det_img_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pushButton = QPushButton(self.page)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_5 = QVBoxLayout(self.page_2)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(15)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.orig_cap_label = QLabel(self.page_2)
        self.orig_cap_label.setObjectName(u"orig_cap_label")
        self.orig_cap_label.setMinimumSize(QSize(200, 200))
        self.orig_cap_label.setAlignment(Qt.AlignCenter)
        self.orig_cap_label.setScaledContents(False)

        self.horizontalLayout_6.addWidget(self.orig_cap_label)

        self.det_cap_label = QLabel(self.page_2)
        self.det_cap_label.setObjectName(u"det_cap_label")
        self.det_cap_label.setMinimumSize(QSize(200, 200))
        self.det_cap_label.setAlignment(Qt.AlignCenter)
        self.det_cap_label.setScaledContents(False)

        self.horizontalLayout_6.addWidget(self.det_cap_label)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.pushButton_cap = QPushButton(self.page_2)
        self.pushButton_cap.setObjectName(u"pushButton_cap")

        self.verticalLayout_5.addWidget(self.pushButton_cap)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.videoVerticalLayout = QVBoxLayout(self.page_3)
        self.videoVerticalLayout.setSpacing(15)
        self.videoVerticalLayout.setObjectName(u"videoVerticalLayout")
        self.videoVerticalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.det_video_label = QLabel(self.page_3)
        self.det_video_label.setObjectName(u"det_video_label")
        self.det_video_label.setMinimumSize(QSize(200, 200))
        self.det_video_label.setAlignment(Qt.AlignCenter)
        self.det_video_label.setScaledContents(False)

        self.horizontalLayout_2.addWidget(self.det_video_label)

        self.orig_video_label = QLabel(self.page_3)
        self.orig_video_label.setObjectName(u"orig_video_label")
        self.orig_video_label.setMinimumSize(QSize(200, 200))
        self.orig_video_label.setAlignment(Qt.AlignCenter)
        self.orig_video_label.setScaledContents(False)

        self.horizontalLayout_2.addWidget(self.orig_video_label)


        self.videoVerticalLayout.addLayout(self.horizontalLayout_2)

        self.pushButton_video = QPushButton(self.page_3)
        self.pushButton_video.setObjectName(u"pushButton_video")

        self.videoVerticalLayout.addWidget(self.pushButton_video)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_sit = QVBoxLayout(self.page_4)
        self.verticalLayout_sit.setSpacing(15)
        self.verticalLayout_sit.setObjectName(u"verticalLayout_sit")
        self.verticalLayout_sit.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(15)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.det_sit_label = QLabel(self.page_4)
        self.det_sit_label.setObjectName(u"det_sit_label")
        self.det_sit_label.setMinimumSize(QSize(200, 200))
        self.det_sit_label.setAlignment(Qt.AlignCenter)
        self.det_sit_label.setScaledContents(False)

        self.horizontalLayout_3.addWidget(self.det_sit_label)

        self.orig_sit_label = QLabel(self.page_4)
        self.orig_sit_label.setObjectName(u"orig_sit_label")
        self.orig_sit_label.setMinimumSize(QSize(200, 200))
        self.orig_sit_label.setAlignment(Qt.AlignCenter)
        self.orig_sit_label.setScaledContents(False)

        self.horizontalLayout_3.addWidget(self.orig_sit_label)


        self.verticalLayout_sit.addLayout(self.horizontalLayout_3)

        self.pushButton_sit = QPushButton(self.page_4)
        self.pushButton_sit.setObjectName(u"pushButton_sit")

        self.verticalLayout_sit.addWidget(self.pushButton_sit)

        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_5_video = QVBoxLayout(self.page_5)
        self.verticalLayout_5_video.setSpacing(15)
        self.verticalLayout_5_video.setObjectName(u"verticalLayout_5_video")
        self.verticalLayout_5_video.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(15)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.det_video_label_3 = QLabel(self.page_5)
        self.det_video_label_3.setObjectName(u"det_video_label_3")
        self.det_video_label_3.setMinimumSize(QSize(200, 200))
        self.det_video_label_3.setAlignment(Qt.AlignCenter)
        self.det_video_label_3.setScaledContents(False)

        self.horizontalLayout_4.addWidget(self.det_video_label_3)

        self.orig_video_label_3 = QLabel(self.page_5)
        self.orig_video_label_3.setObjectName(u"orig_video_label_3")
        self.orig_video_label_3.setMinimumSize(QSize(200, 200))
        self.orig_video_label_3.setAlignment(Qt.AlignCenter)
        self.orig_video_label_3.setScaledContents(False)

        self.horizontalLayout_4.addWidget(self.orig_video_label_3)


        self.verticalLayout_5_video.addLayout(self.horizontalLayout_4)

        self.pushButton_video_3 = QPushButton(self.page_5)
        self.pushButton_video_3.setObjectName(u"pushButton_video_3")

        self.verticalLayout_5_video.addWidget(self.pushButton_video_3)

        self.stackedWidget.addWidget(self.page_5)

        self.mainVerticalLayout.addWidget(self.stackedWidget)

        self.controlHorizontalLayout = QHBoxLayout()
        self.controlHorizontalLayout.setSpacing(15)
        self.controlHorizontalLayout.setObjectName(u"controlHorizontalLayout")
        self.comboBox_page = QComboBox(self.centralwidget_model)
        self.comboBox_page.setObjectName(u"comboBox_page")
        self.comboBox_page.setMinimumSize(QSize(150, 0))

        self.controlHorizontalLayout.addWidget(self.comboBox_page)

        self.comboBox_model = QComboBox(self.centralwidget_model)
        self.comboBox_model.setObjectName(u"comboBox_model")
        self.comboBox_model.setMinimumSize(QSize(150, 0))

        self.controlHorizontalLayout.addWidget(self.comboBox_model)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlHorizontalLayout.addItem(self.horizontalSpacer)


        self.mainVerticalLayout.addLayout(self.controlHorizontalLayout)

        self.sliderVerticalLayout = QVBoxLayout()
        self.sliderVerticalLayout.setSpacing(8)
        self.sliderVerticalLayout.setObjectName(u"sliderVerticalLayout")
        self.horizontalSlider_model = QSlider(self.centralwidget_model)
        self.horizontalSlider_model.setObjectName(u"horizontalSlider_model")
        self.horizontalSlider_model.setOrientation(Qt.Horizontal)

        self.sliderVerticalLayout.addWidget(self.horizontalSlider_model)

        self.label_conf = QLabel(self.centralwidget_model)
        self.label_conf.setObjectName(u"label_conf")
        self.label_conf.setAlignment(Qt.AlignCenter)
        self.label_conf.setStyleSheet(u"QLabel {\n"
"    background-color: transparent;\n"
"    color: #cbd5e1;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}")

        self.sliderVerticalLayout.addWidget(self.label_conf)


        self.mainVerticalLayout.addLayout(self.sliderVerticalLayout)

        MainWindow.setCentralWidget(self.centralwidget_model)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        self.menubar.setStyleSheet(u"QMenuBar {\n"
"    background-color: #1a1d29;\n"
"    color: #e0e7ff;\n"
"    border-bottom: 1px solid #2a2d3a;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    background-color: transparent;\n"
"    padding: 8px 15px;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background-color: #6366f1;\n"
"    border-radius: 4px;\n"
"}\n"
"")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"QStatusBar {\n"
"    background-color: #1a1d29;\n"
"    color: #cbd5e1;\n"
"    border-top: 1px solid #2a2d3a;\n"
"}\n"
"")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"YOLO\u76ee\u6807\u68c0\u6d4b\u7cfb\u7edf", None))
        self.orig_img_label.setText("")
        self.det_img_label.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c1 \U00009009\U000062e9\U000056fe\U00007247", None))
        self.orig_cap_label.setText("")
        self.det_cap_label.setText("")
        self.pushButton_cap.setText(QCoreApplication.translate("MainWindow", u"\U0001f4f7 \U00005f00\U0000542f\U00006444\U000050cf\U00005934", None))
        self.det_video_label.setText("")
        self.orig_video_label.setText("")
        self.pushButton_video.setText(QCoreApplication.translate("MainWindow", u"\U0001f3ac \U00009009\U000062e9\U000089c6\U00009891", None))
        self.det_sit_label.setText("")
        self.orig_sit_label.setText("")
        self.pushButton_sit.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.det_video_label_3.setText("")
        self.orig_video_label_3.setText("")
        self.pushButton_video_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_conf.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u7f6e\u4fe1\u5ea6\u9608\u503c\uff1a0.25", None))
    # retranslateUi

