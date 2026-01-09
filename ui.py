import sys
import cv2
import numpy as np
import json
import socket
import threading
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QMessageBox, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QTimer
from ultralytics import YOLO
from main_window_ui import Ui_MainWindow

# 封装三维矩阵转QImage的函数
def convert2QImage(img):
    # 使用三个变量保存三维矩阵的三个维度具体值
    height, width, channel = img.shape
    # 将获取到的三维矩阵参数作为QImage的构造函数传参
    return QImage(img, width, height, channel * width, QImage.Format.Format_BGR888)

# 为了让界面能够显示 需要自行封装一个类 既可以调用show函数 又可以访问界面
# 所以我需要继承两个类
class mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # 还需要手动调用QMainwindow的构造函数
        super(mainwindow, self).__init__()
        # 页面绘制
        self.setupUi(self)
        # 初始化基础模型
        self.model = YOLO('yolo11n.pt')
        # 信号与槽绑定，将按钮被按下产生的信号和对应的槽函数进行绑定
        self.pushButton.clicked.connect(self.get_image_path) 
        # 页面初始化
        self.page_init()
        # 摄像头初始化
        self.cap_init()
        # 模型选择初始化
        self.model_init()
        # 视频初始化
        self.video_init()
        #模型conf初始化
        self.model_conf_setting()
        # 网络通信初始化
        self.network_init()
        # 存储当前显示的图像数据，用于窗口大小改变时重新显示
        self.current_images = {}  # key: label id, value: np.ndarray 原始图像
        # 初始化图像显示设置
        self.init_image_display()
        # 美化UI界面
        self.apply_modern_style()
        # 让程序运行的初始界面处于第一页
        self.stackedWidget.setCurrentIndex(0)

    # 键盘按键事件，用空格控制视频播放/暂停
    def keyPressEvent(self, event):
        # 只在视频检测这一页（索引2）时响应空格
        if event.key() == Qt.Key.Key_Space and self.stackedWidget.currentIndex() == 2:
            # 如果已经选择并加载过视频（有 video 属性）
            if hasattr(self, "video") and self.video is not None:
                self.video_play_pause()
                event.accept()
                return
        # 其它情况交给父类处理，避免影响全局快捷键
        super().keyPressEvent(event)
    
    # 应用现代化样式
    def apply_modern_style(self):
        """应用现代化的UI样式,美化界面"""
        # 设置窗口标题
        self.setWindowTitle("YOLO目标检测系统")
        
        # 主窗口背景色 - 深色主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            /* StackedWidget 背景 */
            QStackedWidget {
                background-color: #1e1e1e;
                border-radius: 8px;
            }
            /* 图像显示Label样式 */
            QLabel[name="orig_img_label"],
            QLabel[name="det_img_label"],
            QLabel[name="orig_cap_label"],
            QLabel[name="det_cap_label"],
            QLabel[name="orig_video_label"],
            QLabel[name="det_video_label"],
            QLabel[name="det_sit_label"],
            QLabel[name="orig_sit_label"],
            QLabel[name="det_video_label_3"],
            QLabel[name="orig_video_label_3"] {
                background-color: #1e1e1e;
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                padding: 5px;
            }
            /* 按钮样式 - 现代化渐变效果 */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2, stop:1 #4080cd);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #357abd, stop:1 #2a6aa8);
            }
            /* ComboBox样式 */
            QComboBox {
                background-color: #3d3d3d;
                color: white;
                border: 2px solid #4a90e2;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                min-height: 25px;
            }
            QComboBox:hover {
                border-color: #5ba0f2;
                background-color: #454545;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #3d3d3d;
                color: white;
                border: 2px solid #4a90e2;
                border-radius: 6px;
                selection-background-color: #4a90e2;
                selection-color: white;
                padding: 4px;
            }
            /* Slider样式 */
            QSlider::groove:horizontal {
                border: 1px solid #3d3d3d;
                height: 8px;
                background: #2b2b2b;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                border: 2px solid white;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2, stop:1 #4080cd);
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #5ba0f2);
                border-radius: 4px;
            }
            /* Label文本样式 */
            QLabel[name="label_conf"] {
                background-color: transparent;
                color: #e0e0e0;
                font-size: 12px;
                padding: 5px;
            }
        """)
        
        # 单独设置各个按钮的文字
        if hasattr(self, 'pushButton'):
            self.pushButton.setText('📁 选择图片')
        if hasattr(self, 'pushButton_cap'):
            self.pushButton_cap.setText('📷 开启摄像头')
        if hasattr(self, 'pushButton_video'):
            self.pushButton_video.setText('🎬 选择视频')
        
        # 设置图像Label的初始文本
        image_labels = [
            'orig_img_label', 'det_img_label', 'orig_cap_label', 'det_cap_label',
            'orig_video_label', 'det_video_label', 'det_sit_label', 'orig_sit_label',
            'det_video_label_3', 'orig_video_label_3'
        ]
        for label_name in image_labels:
            label = getattr(self, label_name, None)
            if label is not None:
                label.setText("")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # 页面初始化函数，填充combox控件的内容
    def page_init(self):
        self.comboBox_page.addItem('图像检测')
        self.comboBox_page.addItem('摄像头检测')
        self.comboBox_page.addItem('视频检测')
        # 将combox页码变化信号和翻页函数进行绑定
        self.comboBox_page.currentIndexChanged.connect(self.page_choose)

    # 翻页函数
    def page_choose(self):
        # 先打印翻页函数调用后 combox_page的当前页码
        page = self.comboBox_page.currentIndex()
        # 将stackedwidget的页码强行切换为和combox一致的页码
        self.stackedWidget.setCurrentIndex(page)

    # 模型切换初始化
    def model_init(self):
        # 添加模型的可选条目信息
        self.comboBox_model.addItem('基础模型')
        self.comboBox_model.addItem('火影识别模型')
        self.comboBox_model.addItem('坐姿识别模型')
        self.comboBox_model.addItem('自训练模型3')
        # 信号与槽绑定模型选择函数
        self.comboBox_model.currentIndexChanged.connect(self.model_choose)

    # 模型切换的实现操作
    def model_choose(self):
        # 先获取对应模型的文字信息索引号
        page = self.comboBox_model.currentIndex()
        # 根据页码索引号初始化对应的模型
        # 第一页是基础模型
        if page == 0:
            self.model = YOLO('yolo11n.pt')
            print('基础模型')
        # 第二页是自训练模型1
        elif page == 1:
            self.model = YOLO('runs/detect/train/weights/best.pt')
            print('自训练模型1')
        # 第三页是自训练模型sit
        elif page == 2:
            self.model = YOLO('runs/detect/train2/weights/best.pt')
            print('自训练模型sit')
        # 第四页是自训练模型3
        elif page == 1:
            self.model = YOLO('runs/detect/train/weights/best.pt')
            print('自训练模型3')

    #模型置信度阈值实时修改
    def model_conf_setting(self):
        #先自行设置一个conf的初始值
        self.model_conf = 0.25
        #在指定位置显示初始的conf值
        self.label_conf.setText(f'模型置信度阈值：0.25')
        #滑动条在滑动的时候，会产生数值变化信号，将这个信号和conf修改函数进行绑定
        self.horizontalSlider_model.valueChanged.connect(self.conf_value_change)
 
    #滑动条数值变化槽函数
    def conf_value_change(self):
        #获取滑动条的数值
        value = self.horizontalSlider_model.value()
        #将滑动条的value除以100 用于模型检测conf值的使用
        #将conf的值初始化为页面类的一个属性
        self.model_conf = value / 100
        #将conf变化值设置到label上
        self.label_conf.setText(f'模型置信度阈值：{value/100}')

    # 图像路径获取函数
    def get_image_path(self):
        print('图像检测')
        # 调用获取文件路径函数
        path = QFileDialog.getOpenFileName(self, "选择图像文件", "", "图片文件 (*.jpg *.png)")
        # 判断path的第一个成员是不是空（用户是不是选择了文件）
        if path[0]:
            # 提取出元组中的文件路径
            image_path = path[0]
            # 将图像路径传参给model对象
            result = self.model(source=image_path, verbose=False,conf=self.model_conf)
            # 将检测结果提取，作为参数进行格式化打印
            self.detection_format_print(result[0])
            # 获取检测结果返回值中的图像矩阵
            orig_arr = result[0].orig_img
            det_arr = result[0].plot()
            # 把两个图像矩阵显示在指定画布上
            self.detection_img_show(orig_arr, self.orig_img_label)
            self.detection_img_show(det_arr, self.det_img_label)
        # 如果path[0]为空 代表用户没选择文件，打印信息
        else:
            print('未选择图像')
            QMessageBox.information(self,"消息","用户未选择图像")

    # 初始化图像显示设置
    def init_image_display(self):
        """初始化所有图像label的显示设置，使其能够自适应窗口大小"""
        labels = [
            getattr(self, "orig_img_label", None),
            getattr(self, "det_img_label", None),
            getattr(self, "orig_cap_label", None),
            getattr(self, "det_cap_label", None),
            getattr(self, "orig_video_label", None),
            getattr(self, "det_video_label", None),
        ]
        for label in labels:
            if label is not None:
                # 设置图片居中显示
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                # 不自动拉伸，我们手动控制缩放以保持宽高比
                label.setScaledContents(False)
    
    # 检测结果显示 将传入的图像矩阵显示到指定的画布上 限制函数的传参类型
    def detection_img_show(self, arr: np.ndarray, place: QLabel):
        """
        将图像显示到指定的label上，自动适应label的大小
        当窗口大小改变时，图片会自动缩放以适应新的尺寸
        """
        # 存储原始图像数据，用于窗口大小改变时重新显示
        self.current_images[id(place)] = arr.copy()
        
        # 更新显示
        self._update_image_display(arr, place)
    
    # 更新图像显示
    def _update_image_display(self, arr: np.ndarray, place: QLabel):
        """更新label上的图像显示，自动适应label的当前大小"""
        # 将图像矩阵转化为QImage
        qimage_arr = convert2QImage(arr)
        # 将QImage格式图像数据转化为QPixmap
        qpixmap_arr = QPixmap.fromImage(qimage_arr)
        
        # 获取label的实际大小
        label_width = max(1, place.width())
        label_height = max(1, place.height())
        
        # 如果label尺寸太小，尝试使用geometry
        if label_width <= 1 or label_height <= 1:
            rect = place.geometry()
            label_width = max(1, rect.width())
            label_height = max(1, rect.height())
        
        # 将图片缩放到label的大小，保持等比例，确保完整显示
        scaled_pixmap = qpixmap_arr.scaled(
            label_width,
            label_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        # 在指定的label画布显示缩放后的图像
        place.setPixmap(scaled_pixmap)
    
    # 窗口大小改变事件处理
    def resizeEvent(self, event):
        """窗口大小改变时，重新显示所有图片以适应新的窗口大小"""
        super().resizeEvent(event)
        # 延迟刷新，确保布局更新完成
        QTimer.singleShot(50, self._refresh_all_images)
    
    # 刷新所有已显示的图片
    def _refresh_all_images(self):
        """刷新所有已存储的图像，使其适应当前的窗口大小"""
        labels = [
            getattr(self, "orig_img_label", None),
            getattr(self, "det_img_label", None),
            getattr(self, "orig_cap_label", None),
            getattr(self, "det_cap_label", None),
            getattr(self, "orig_video_label", None),
            getattr(self, "det_video_label", None),
        ]
        for label in labels:
            if label is None:
                continue
            label_id = id(label)
            if label_id in self.current_images:
                img_arr = self.current_images[label_id]
                self._update_image_display(img_arr, label)

    # 摄像头初始化函数
    def cap_init(self):
        # 初始化摄像头 此时无需传参
        self.cap = cv2.VideoCapture()
        # 初始化摄像头图像获取用的计时器
        self.cap_timer = QTimer()
        # 初始化定时器的计时间隔
        self.cap_timer.setInterval(1)
        # 摄像头控制按钮绑定对应的操作函数
        self.pushButton_cap.clicked.connect(self.cap_operation)
        # 将定时器计时一次结束后产生的信号和图像采集函数进行绑定
        self.cap_timer.timeout.connect(self.cap_image_detect)
    
    # 摄像头开关操作函数
    def cap_operation(self):
        # 判断摄像头的状态 如果为关闭状态 此时按按钮就应该开启摄像头
        if self.cap.isOpened() == False:
            print('摄像头开启')
            # 打开本地摄像头
            # 在 macOS/Linux 上通常不需要指定后端，或者使用 cv2.CAP_AVFOUNDATION / cv2.CAP_V4L2
            # 移除 cv2.CAP_DSHOW 以实现跨平台兼容
            ret = self.cap.open(0)
            # 判断摄像头是否开启成功
            if ret:
                print('开启成功')
                # 开启成功后 修改按钮的文本信息为关闭 因为你下一次按按钮就是关闭操作了
                self.pushButton_cap.setText('关闭摄像头')
                # 开启定时器
                self.cap_timer.start()
            else:
                print('开启失败')
                # 如果开启失败，就调用该释放函数
                self.cap.release()
                # 摄像头状态有误 定时器也需要关闭
                self.cap_timer.stop()
        # 如果摄像头处于开启状态 本次按钮的操作就应该关闭摄像头
        else:
            print('摄像头关闭')
            self.cap.release()
            # 如果正常摄像头 按钮文本改为开启
            self.pushButton_cap.setText('开启摄像头')
            # 摄像头正常关闭 定时器也需要关闭
            self.cap_timer.stop()
            # 显示画布需要清空
            self.orig_cap_label.clear()
            self.det_cap_label.clear()

    # 摄像头图像采集函数
    def cap_image_detect(self):
        # 使用read函数获取图像矩阵
        # 返回值1：是否成功捕获到图像矩阵
        # 返回值2：图像矩阵
        ret, arr = self.cap.read()
        # 判断图像矩阵是否被读到
        if ret:
            # 将摄像头采集到的单帧图像数据显示到左侧画布上
            self.detection_img_show(arr, self.orig_cap_label)
            # 将图像矩阵作为模型检测的传参进行检测
            result = self.model(source=arr, verbose=False,conf=self.model_conf)
            self.detection_format_print(result[0])
            # 提取出检测图像矩阵
            det_arr = result[0].plot()
            # 将检测图像显示到右侧画布
            self.detection_img_show(det_arr, self.det_cap_label)

    # 检测结果格式化打印函数：只打印锚框坐标信息，不进行数量统计
    # 功能模块：检测结果格式化打印逻辑
    def detection_format_print(self, det_result):
        """
        格式化打印每个检测目标的锚框坐标信息
        
        参数:
            det_result: YOLO检测结果对象
        """
        # 获取存放检测对象的字典（类别索引到类别名称的映射）
        det_dict = det_result.names
        # 获取所有检测结果的综合
        det_boxes = det_result.boxes
        # 获取检测结果中的类别索引矩阵
        det_cls = det_boxes.cls
        # 获取检测框的坐标信息（x_center, y_center, width, height格式）
        det_xywh = det_boxes.xywh
        # 将cls矩阵转化为能够正常提取成员的numpy矩阵
        det_cls_arr = det_cls.numpy()
        # 将xywh坐标矩阵转化为numpy矩阵
        det_xywh_arr = det_xywh.numpy()
        
        # 遍历每个检测结果，单独打印每个物体的类别和坐标信息
        # 即使同一类别，只要坐标不同，也分别输出
        for i in range(len(det_cls_arr)):
            # 获取类别索引
            cls_index = int(det_cls_arr[i])
            # 使用索引号访问字典，得到检测的物体名称
            cls_obj = det_dict[cls_index]
            # 获取该物体的坐标信息（x_center, y_center, width, height）
            x = float(det_xywh_arr[i][0])
            y = float(det_xywh_arr[i][1])
            w = float(det_xywh_arr[i][2])
            h = float(det_xywh_arr[i][3])
            # 格式化打印每个物体的坐标信息，格式：person: x=..., y=..., w=..., h=...
            print(f'{cls_obj}: x={x:.2f} y={y:.2f} w={w:.2f} h={h:.2f}')

    # 视频初始化函数
    # 功能模块：视频控制逻辑
    def video_init(self):
        # 视频图像显示定时器初始化
        self.video_timer = QTimer()
        self.video_timer.setInterval(33)  # 约30fps的播放速度
        # 视频相关变量初始化
        self.video_total_frames = 0  # 视频总帧数
        self.video_current_frame = 0  # 当前播放帧号
        self.video_is_playing = False  # 视频播放状态
        self.video_paused_frame = 0  # 暂停时的帧号
        
        # 视频选择信号与槽
        self.pushButton_video.clicked.connect(self.video_choose)
        # 定时器信号与槽
        self.video_timer.timeout.connect(self.video_image_detect)
        
        # 获取 page_3 的布局（应该已经存在 videoVerticalLayout）
        # 从 UI 文件可以看到，page_3 已经有一个 QVBoxLayout 名为 videoVerticalLayout
        page_3_layout = self.page_3.layout()
        if page_3_layout is None:
            # 如果没有布局，创建一个
            page_3_layout = QVBoxLayout(self.page_3)
            page_3_layout.setSpacing(15)
            page_3_layout.setContentsMargins(10, 10, 10, 10)
        
        # 动态创建视频进度条（不使用固定位置 setGeometry，而是添加到布局中以实现自适应）
        self.video_slider = QSlider(Qt.Orientation.Horizontal, self.page_3)
        self.video_slider.setMinimum(0)
        self.video_slider.setMaximum(0)
        # 设置进度条的大小策略，使其可以水平扩展，垂直固定
        self.video_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.video_slider.setMinimumHeight(20)
        # 绑定进度条拖动事件（注意：需要阻止播放时自动更新进度条触发的跳转）
        self.video_slider_being_dragged = False
        self.video_slider.valueChanged.connect(self.video_slider_changed)
        self.video_slider.sliderPressed.connect(lambda: setattr(self, 'video_slider_being_dragged', True))
        self.video_slider.sliderReleased.connect(self.video_slider_released)
        # 避免进度条获得焦点后按空格触发其它控件
        self.video_slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # 将进度条添加到布局末尾（会在 pushButton_video 之后显示）
        page_3_layout.addWidget(self.video_slider)
        
        # 创建播放控制按钮的水平布局容器
        play_control_layout = QHBoxLayout()
        play_control_layout.setSpacing(10)
        
        # 动态创建播放/暂停按钮（不使用固定位置 setGeometry，而是添加到布局中以实现自适应）
        self.video_play_pause_button = QPushButton('播放', self.page_3)
        self.video_play_pause_button.setStyleSheet("background-color: rgb(147, 255, 84); border-radius: 6px; font-weight: bold;")
        self.video_play_pause_button.clicked.connect(self.video_play_pause)
        # 设置按钮的大小策略，使其可以水平扩展，垂直固定
        self.video_play_pause_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.video_play_pause_button.setMinimumHeight(30)
        # 避免按钮被空格触发文件选择
        self.video_play_pause_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # 将按钮添加到水平布局中
        play_control_layout.addWidget(self.video_play_pause_button)
        # 将水平布局添加到 page_3 的垂直布局末尾（会在进度条之后显示）
        page_3_layout.addLayout(play_control_layout)
        
        # 将视频选择按钮改为"选择视频"
        self.pushButton_video.setText('选择视频')
        # 避免按空格触发文件选择
        self.pushButton_video.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    # 视频选择函数
    # 功能模块：视频控制逻辑
    def video_choose(self):
        """
        选择视频文件并初始化视频播放相关参数
        """
        # 先获取视频文件的路径 限制打开文件的格式为视频格式
        path = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi *.mov)")
        video_path = path[0]
        # 判断用户是不是真的选择了视频
        if video_path:
            # 如果选到了视频，才初始化对应的视频对象
            self.video = cv2.VideoCapture(video_path)
            # 检查视频是否成功打开
            if not self.video.isOpened():
                QMessageBox.warning(self, "错误", "无法打开视频文件")
                return
            
            # 获取视频总帧数
            self.video_total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
            # 初始化当前帧号为0
            self.video_current_frame = 0
            self.video_paused_frame = 0
            self.video_is_playing = False
            
            # 设置进度条范围：最小值为0，最大值为总帧数-1
            self.video_slider.setMinimum(0)
            self.video_slider.setMaximum(max(0, self.video_total_frames - 1))
            self.video_slider.setValue(0)
            
            # 将视频设置到第一帧
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # 读取第一帧显示
            ret, arr = self.video.read()
            if ret:
                self.detection_img_show(arr, self.orig_video_label)
                # 对第一帧进行检测
                result = self.model(source=arr, verbose=False, conf=self.model_conf)
                det_arr = result[0].plot()
                self.detection_img_show(det_arr, self.det_video_label)
                self.detection_format_print(result[0])
                # 打包并发送检测结果
                self.pack_and_send_detection_result(result[0], 0)

                # 将当前帧号推进到下一帧，避免第一帧重复播放
                if self.video_total_frames > 1:
                    self.video_current_frame = 1
                    self.video_paused_frame = 1
                    self.video_slider.setValue(1)
                else:
                    self.video_current_frame = 0
                    self.video_paused_frame = 0

                # 自动开始播放
                self.video_play()
            else:
                QMessageBox.warning(self, "错误", "无法读取视频第一帧")
                return

            print(f'视频已加载，总帧数：{self.video_total_frames}')
        else:
            print('用户未选择视频')
    
    # 网络通信初始化函数
    # 功能模块：网络通信逻辑
    def network_init(self):
        """
        初始化网络通信相关参数
        """
        # 服务器地址和端口（纯 Socket，不使用任何 Web 服务）
        # ❌ 不使用 Flask/FastAPI/HTTP/WebSocket，只使用纯 TCP Socket
        self.server_host = 'localhost'
        # 使用高位端口 50000（避免权限问题和端口占用）
        self.server_port = 50000
        # Socket连接对象
        self.client_socket = None
        # 连接状态标记（初始化为 False）
        self.socket_connected = False
        # 是否启用网络发送（这里默认启用，直接向服务器发送检测结果）
        self.network_enabled = True
        # 连接重试计数器（避免频繁打印错误）
        self.connection_retry_count = 0
    
    # 检测结果打包函数
    # 功能模块：网络通信逻辑
    def pack_detection_result(self, det_result, frame_id):
        """
        将检测结果打包为JSON格式
        
        参数:
            det_result: YOLO检测结果对象
            frame_id: 当前帧号
            
        返回:
            dict: 打包后的检测结果字典
        """
        # 获取存放检测对象的字典
        det_dict = det_result.names
        # 获取所有检测结果
        det_boxes = det_result.boxes
        # 获取类别索引矩阵
        det_cls = det_boxes.cls
        # 获取检测框的坐标信息（x_center, y_center, width, height格式）
        det_xywh = det_boxes.xywh
        # 转换为numpy数组
        det_cls_arr = det_cls.numpy()
        det_xywh_arr = det_xywh.numpy()
        
        # 构建对象列表
        objects = []
        for i in range(len(det_cls_arr)):
            # 获取类别索引
            cls_index = int(det_cls_arr[i])
            # 获取类别名称
            cls_obj = det_dict[cls_index]
            # 获取坐标信息
            x = float(det_xywh_arr[i][0])
            y = float(det_xywh_arr[i][1])
            w = float(det_xywh_arr[i][2])
            h = float(det_xywh_arr[i][3])
            
            # 添加到对象列表
            objects.append({
                "class": cls_obj,
                "x": x,
                "y": y,
                "w": w,
                "h": h
            })
        
        # 构建完整的检测结果数据包
        detection_data = {
            "frame_id": int(frame_id),
            "objects": objects
        }
        
        return detection_data
    
    # 打包并发送检测结果函数
    # 功能模块：网络通信逻辑
    def pack_and_send_detection_result(self, det_result, frame_id):
        """
        打包检测结果并发送到服务器
        
        参数:
            det_result: YOLO检测结果对象
            frame_id: 当前帧号
        """
        # 如果网络功能未启用，直接返回
        if not self.network_enabled:
            return
        
        try:
            # 打包检测结果
            detection_data = self.pack_detection_result(det_result, frame_id)
            # 转换为JSON字符串
            json_data = json.dumps(detection_data, ensure_ascii=False)
            # 发送数据
            self.send_detection_data(json_data)
        except Exception as e:
            print(f'打包并发送检测结果时出错：{e}')
    
    # 发送检测数据函数
    # 功能模块：网络通信逻辑（纯 Socket TCP 通信，不涉及任何 Web 服务）
    def send_detection_data(self, json_data):
        """
        通过纯 TCP Socket 发送检测数据到服务器
        
        客户端职责：只发送数据，不监听端口，不启动服务
        
        参数:
            json_data: JSON格式的字符串数据
        """
        try:
            # 如果Socket连接不存在或已断开，创建新连接
            # 注意：客户端只 connect，不 bind/listen（符合纯 Socket 客户端要求）
            # 检查连接状态
            is_connected = getattr(self, 'socket_connected', False)
            if self.client_socket is None or not is_connected:
                try:
                    # 创建 TCP Socket（客户端只连接，不 bind/listen）
                    # ❌ 客户端不应该有 bind() 或 listen()
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # 设置连接超时（3秒）
                    self.client_socket.settimeout(3.0)
                    # 设置 TCP_NODELAY 以减少延迟
                    self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    # 连接到服务器（纯 TCP Socket 连接）
                    if self.connection_retry_count == 0:
                        print(f'正在尝试连接到服务器 {self.server_host}:{self.server_port}...')
                    self.client_socket.connect((self.server_host, self.server_port))
                    self.socket_connected = True
                    self.connection_retry_count = 0  # 连接成功，重置计数器
                    print(f'✅ 已连接到服务器 {self.server_host}:{self.server_port}（纯 Socket TCP）')
                except (ConnectionRefusedError, socket.timeout, OSError) as e:
                    # 连接失败，重置状态
                    self.socket_connected = False
                    if self.client_socket:
                        try:
                            self.client_socket.close()
                        except:
                            pass
                        self.client_socket = None
                    
                    # 限制错误信息打印频率（每10次连接失败才打印一次）
                    self.connection_retry_count += 1
                    if self.connection_retry_count % 10 == 1:
                        error_msg = str(e)
                        error_type = type(e).__name__
                        print(f'\n⚠ 无法连接到服务器 {self.server_host}:{self.server_port} ({self.connection_retry_count} 次尝试)')
                        print(f'   错误类型：{error_type}')
                        print(f'   错误详情：{error_msg}')
                        print(f'   解决方案：')
                        print(f'   1. 确保服务器已启动：python detection_server.py')
                        print(f'   2. 检查服务器是否监听在端口 {self.server_port}')
                        print(f'   3. 检查防火墙是否阻止连接')
                        print(f'   4. 如果端口被占用，请关闭占用端口的程序或使用其他端口')
                    return  # 连接失败，直接返回
            
            # 发送数据（添加换行符作为分隔符，方便服务器按行解析）
            message = json_data + '\n'
            self.client_socket.sendall(message.encode('utf-8'))
            
        except (ConnectionResetError, BrokenPipeError, OSError) as e:
            # 连接断开，重置状态
            print(f'⚠ 与服务器的连接已断开：{e}')
            self.socket_connected = False
            if self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = None
        except Exception as e:
            print(f'✗ 发送数据时出错：{e}')
            # 出错时重置连接状态
            self.socket_connected = False
            if self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = None

    # 视频进度条拖动跳转函数
    # 功能模块：视频控制逻辑
    def video_slider_changed(self, value):
        """
        当进度条值改变时调用（包括拖动和自动更新）
        只在用户拖动时执行跳转操作
        """
        # 只有在拖动状态下才执行跳转，避免自动更新时触发跳转
        if self.video_slider_being_dragged:
            # 记录跳转目标帧号
            target_frame = value
            # 如果视频已加载
            if self.video and self.video.isOpened():
                # 确保帧号在有效范围内
                target_frame = max(0, min(target_frame, self.video_total_frames - 1))
                # 更新当前帧号
                self.video_current_frame = target_frame
                self.video_paused_frame = target_frame
                # 设置视频到目标帧
                self.video.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
                # 读取并显示该帧
                ret, arr = self.video.read()
                if ret:
                    self.detection_img_show(arr, self.orig_video_label)
                    # 对该帧进行检测
                    result = self.model(source=arr, verbose=False, conf=self.model_conf)
                    det_arr = result[0].plot()
                    self.detection_img_show(det_arr, self.det_video_label)
                    self.detection_format_print(result[0])
                    # 打包并发送检测结果
                    self.pack_and_send_detection_result(result[0], target_frame)
    
    # 进度条拖动释放函数
    # 功能模块：视频控制逻辑
    def video_slider_released(self):
        """
        进度条拖动释放时调用
        """
        self.video_slider_being_dragged = False
    
    # 视频播放/暂停控制函数
    # 功能模块：视频控制逻辑
    def video_play_pause(self):
        """
        视频播放/暂停切换函数
        """
        # 检查视频是否已加载
        if not hasattr(self, 'video') or not self.video or not self.video.isOpened():
            QMessageBox.information(self, "提示", "请先选择视频文件")
            return
        
        # 如果当前正在播放，则暂停
        if self.video_is_playing:
            self.video_pause()
        else:
            # 如果当前暂停，则继续播放
            self.video_play()
    
    # 视频播放函数
    # 功能模块：视频控制逻辑
    def video_play(self):
        """
        开始播放视频（从记录的帧号开始继续播放）
        """
        # 如果视频已结束，则从0开始
        if self.video_current_frame >= self.video_total_frames:
            self.video_current_frame = 0
            self.video_paused_frame = 0
        else:
            # 从记录的暂停帧号开始播放
            self.video_current_frame = self.video_paused_frame
        
        # 设置播放状态为True
        self.video_is_playing = True
        # 更新按钮文本
        self.video_play_pause_button.setText('暂停')
        # 启动定时器
        self.video_timer.start()
    
    # 视频暂停函数
    # 功能模块：视频控制逻辑
    def video_pause(self):
        """
        暂停视频播放，记录当前帧号
        """
        # 记录当前播放到的帧号
        self.video_paused_frame = self.video_current_frame
        # 设置播放状态为False
        self.video_is_playing = False
        # 更新按钮文本
        self.video_play_pause_button.setText('播放')
        # 停止定时器
        self.video_timer.stop()
    
    # 视频图像检测
    # 功能模块：视频控制逻辑 + 检测逻辑
    def video_image_detect(self):
        """
        视频播放时每帧调用的函数：读取帧、检测、更新进度条
        """
        # 如果视频没有播放，直接返回
        if not self.video_is_playing:
            return
        
        # 检查是否到达视频末尾
        if self.video_current_frame >= self.video_total_frames:
            # 视频播放完毕，停止播放
            self.video_pause()
            return
        
        # 设置视频到当前帧号
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.video_current_frame)
        # 读取视频对象的视频帧
        ret, arr = self.video.read()
        
        # 先判断视频是不是读完了
        if ret:
            # 将原始视频显示到左侧
            self.detection_img_show(arr, self.orig_video_label)
            # 将图像矩阵进行检测
            result = self.model(source=arr, verbose=False, conf=self.model_conf)
            # 提取带检测框的图像矩阵
            det_arr = result[0].plot()
            # 右侧画布显示带检测框的检测结果
            self.detection_img_show(det_arr, self.det_video_label)
            # 将检测结果返回值作为参数传给格式化打印函数
            self.detection_format_print(result[0])
            # 打包并发送检测结果
            self.pack_and_send_detection_result(result[0], self.video_current_frame)
            
            # 更新进度条值（播放时进度条联动）
            # 只有在非拖动状态下才更新进度条，避免拖动时冲突
            if not self.video_slider_being_dragged:
                self.video_slider.setValue(self.video_current_frame)
            
            # 当前帧号递增
            self.video_current_frame += 1
        # 如果ret为假 代表视频读取出错或已结束
        else:
            self.video_pause()
            self.orig_video_label.clear()
            self.det_video_label.clear()
    
    # 程序关闭事件处理函数
    # 功能模块：资源清理逻辑
    def closeEvent(self, event):
        """
        程序关闭时清理资源
        
        参数:
            event: 关闭事件对象
        """
        # 停止视频定时器
        if hasattr(self, 'video_timer') and self.video_timer.isActive():
            self.video_timer.stop()
        
        # 停止摄像头定时器
        if hasattr(self, 'cap_timer') and self.cap_timer.isActive():
            self.cap_timer.stop()
        
        # 释放摄像头资源
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        
        # 释放视频资源
        if hasattr(self, 'video') and self.video and self.video.isOpened():
            self.video.release()
        
        # 关闭网络连接
        if hasattr(self, 'client_socket') and self.client_socket:
            self.client_socket.close()
            self.client_socket = None
        
        # 接受关闭事件
        event.accept()

# main函数
if __name__ == "__main__":
    # 要先准备一个QApplication对象
    app = QApplication(sys.argv)
    # 实例化一个ui对象
    ui = mainwindow()
    # 显示界面
    ui.show()
    # 使用事件循环机制让程序不退出
    app.exec()