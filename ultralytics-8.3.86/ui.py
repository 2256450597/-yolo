import sys
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication,QMainWindow, QFileDialog,QLabel
from PySide6.QtGui import QPixmap,QImage
from PySide6.QtCore import Qt,QTimer
from ultralytics import YOLO
#YOLO模块导入必须在页面内之前
from main_window_ui import Ui_MainWindow

#封装三维矩阵转Qimage函数
def convert_3dmat_to_Qimage(img):
    #使用三个变量保存图像的三维具体尺寸
    height,width,channels = img.shape
    #将获取到的三维矩阵参数作为Qimage的构造函数传参
    return QImage(img,width,height,channels * width,QImage.Format_BGR888)

#为了让界面能够显示，需要自行封装一个类既可以调用show函数，又可以访问界面
#所以需要继承2个类，一个是QMainWindow，另一个是Ui_MainWindow.有对象实例化自动调用
class mainwindow(QMainWindow,Ui_MainWindow):
    #构造函数
    def __init__(self):
        #还需要手动调用QMainWindow的构造函数才能用里面的东西
        super(mainwindow,self).__init__()
        #页面绘制
        self.setupUi(self)
        #初始化基础YOLO模型
        self.model = YOLO("yolo11n.pt")
        #信号与槽绑定，将按钮按下产生的信号与自定义的槽函数进行绑定
        self.pushButton.clicked.connect(self.get_image_path)
        #页面初始化函数调用   
        self.page_init()
        #摄像头初始化
        self.cap_init()

        #模型选择初始化
        self.model_init()

        #视频初始化
        self.video_init()
        #让程序运行的初始界面为图像检测页面

        #模型conf初始化
        self.model_conf_setting()


        self.stackedWidget.setCurrentIndex(0)


        # 画布上加图像
        # self.orig_img_label.setPixmap('')

    #页面初始化函数
    def page_init(self):
        self.comboBox_page.addItem("图像检测")
        self.comboBox_page.addItem('摄像头检测')
        self.comboBox_page.addItem('视频检测')
        #将combox_page的当前索引变化信号与翻页函数进行绑定
        self.comboBox_page.currentIndexChanged.connect(self.page_choose)

    #翻页函数
    def page_choose(self):
        #先打印翻页函数调用后 combox_page的当前页码
        page = self.comboBox_page.currentIndex()
        #print(f"当前combox_page页码为{page}页")
        #将stackedwidget的页码设置为当前combox_page的页码
        self.stackedWidget.setCurrentIndex(page)

    #模型切换初始化
    def model_init(self):
        #添加模型的可选条目信息
        self.comboBox_model.addItem('基础模型')
        self.comboBox_model.addItem('自训练模型1')
        #信号与槽绑定模型选择函数
        self.comboBox_model.currentIndexChanged.connect(self.model_choose)

    
    #模型切换实现操作
    def model_choose(self):
        #先获取对应模型的文字信息索引号
        page = self.comboBox_model.currentIndex()
        #根据页码索引号初始化对应的模型
        #第一页是基础模型
        if page == 0:
            self.model = YOLO('yolo11n.pt')
            print('基础模型')

        #第二页是自训练模型2
        elif page == 1:
            self.model = YOLO('runs/detect/train/weights/best.pt')
            print('自训练模型1')


    #模型的置信度阈值实时修改
    def model_conf_setting(self):
        #先自行设置一个conf的初始值
        self.model_conf = 0.25
        #在制定位置显示初始conf值
        self.label_conf.setText(f'模型置信度阈值:0.25')

        #滑动条在滑动时会产生数值变化，将这个信号和conf修改函数进行绑定
        self.horizontalSlider_model.valueChanged.connect(self.conf_value_change)

    #滑动条数值变化槽函数
    def conf_value_change(self):
        #获取滑动条的数值
        value = self.horizontalSlider_model.value()
        #将滑动条的的数值除100用于模型检测conf值使用
        #将conf的值初始化为页面的一个属性
        self.model_conf = value/100

        #将conf变化值设置到label上
        self.label_conf.setText(f'模型置信度阈值:{value/100}')

    #图像路径获取函数
    def get_image_path(self):
        #print("图像检测路径获取")
        #调用获取文件路径函数.可以使用filter限制文件类型
        path = QFileDialog.getOpenFileName(filter ='*.jpg;*.png;')
    
        #判断path的第一个成员是不是空（用户是否选择文件） 没有必要强行判断第一个成员是不是假
        if path[0]:
            #提取出元祖中的文件路径
            image_path = path[0]
            #将图像路径传参给model对象
            result = self.model(source=image_path,verbose=False,conf = self.model_conf)
            #将结果提取，作为参数进行格式化打印
            #self.detection_format_print(result[0])
            #将图片路径传递给模型进行检测
            result = self.model(source=image_path)
            #label需要QPixmap格式的图像,所以需要转换Qimage格式转换，Qimage需要手动用三维矩阵转换
            #获取检测结果返回值中的图像矩阵
            orig_arr = result[0].orig_img

            #显示带框的图像
            #orig_arr = result[0].plot()
            #将图像矩阵转换为Qimage格式
            #qimage_arr = convert_3dmat_to_Qimage(orig_arr)
            #将Qimage格式转换为Qpixmap格式
            #qpixmap_arr = QPixmap.fromImage(qimage_arr)
            #剪裁获取到的图像，使其适应label的大小
            #orig_img = qpixmap_arr.scaled(self.orig_img_label.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
            #在指定画布将转换好的Qpixmap格式图像显示在label上
            #self.orig_img_label.setPixmap(orig_img)
#det 图像
            #获取检测结果返回值中的图像矩阵
            #orig_arr = result[0].orig_img
            #显示带框的图像
            det_arr = result[0].plot(conf=self.model_conf)
            # #将图像矩阵转换为Qimage格式
            # qimage_arr = convert_3dmat_to_Qimage(det_arr)
            # #将Qimage格式转换为Qpixmap格式
            # qpixmap_arr = QPixmap.fromImage(qimage_arr)
            # #剪裁获取到的图像，使其适应label的大小
            # det_img = qpixmap_arr.scaled(self.det_img_label.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
            # #在指定画布将转换好的Qpixmap格式图像显示在label上
            # self.det_img_label.setPixmap(det_img)
            self.detection_img_show(orig_arr,self.orig_img_label)
            self.detection_img_show(det_arr,self.det_img_label)
        else:
            print("未选择图片")


#检测结果显示,将传入的图像矩阵指定到指定画布上 限制函数的传参类型
    def detection_img_show(self,arr:np.ndarray,place:QLabel):
        qimage_arr = convert_3dmat_to_Qimage(arr)
              #将Qimage格式转换为Qpixmap格式
        qpixmap_arr = QPixmap.fromImage(qimage_arr)
              #剪裁获取到的图像，使其适应label的大小
        det_img = qpixmap_arr.scaled(place.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
              #在指定画布将转换好的Qpixmap格式图像显示在label上
        place.setPixmap(det_img)


#摄像头初始化函数
    def cap_init(self):
        #初始化摄像头此时无需传参
        self.cap = cv2.VideoCapture()
        #摄像头图像获取用的定时去
        self.cap_timer = QTimer()
        #初始化定时器时间间隔
        self.cap_timer.setInterval(1)
        #摄像头控制按钮绑定对应的槽函数
        self.pushButton_cap.clicked.connect(self.cap_operation)
        #将计时器计时一次结束采集的信号与获取摄像头图像函数进行绑定
        self.cap_timer.timeout.connect(self.cap_img_detect)

#摄像头开关操作函数
    def cap_operation(self):
        #判断摄像头状态是否打开，如果是关闭，此时按按钮一个是打开摄像头
        if self.cap.isOpened() == False:
            #打开摄像头需要摄像头编号和采样模式
            
            ret = self.cap.open(0)
            #判断是否开启成功
            if ret:
                print("摄像头已开启")
                #开启成功后修改按钮文本信息为关闭摄像头
                self.pushButton_cap.setText("关闭摄像头")
                #开启定时器，开始循环获取摄像头图像
                self.cap_timer.start()
            else:
                print("摄像头开启失败")
                #如果开启失败，就释放函数
                self.cap.release()
                #摄像头状态有无，定时器关闭
                self.timer.stop()
        #如果摄像头没开，本次操作应该是摄像头关闭
        else:
            #关闭摄像头
            print("摄像头关闭")
            self.cap.release()
            #修改按钮文本信息为开启摄像头
            self.pushButton_cap.setText("开启摄像头")
            #摄像头正常关闭，定时器也需要关闭
            self.cap_timer.stop()
            #显示画布需要清空
            self.orig_cap_label.clear()
            self.det_cap_label.clear()

#获取摄像头采集图像函数
    def cap_img_detect(self):
        #使用read函数获取图像矩阵
        #返回值1:是否成功捕获到图像矩阵
        #返回值2：图像矩阵
        ret,arr = self.cap.read()
        #判断是否成功捕获图像矩阵
        if ret:
            #将摄像头采集到的单帧图像数据显示到左侧画布
            self.detection_img_show(arr,self.orig_cap_label)
            #将图像矩阵作为模型检测的传参进行检测
            result = self.model(source=arr,verbose=False,conf = self.model_conf)
            self.detection_format_print(result[0])
            #将图像矩阵作为model的传参进行检测
            #result = self.model(source=arr)
            #提取检测图像矩阵
            det_arr = result[0].plot(conf=self.model_conf)
            #将检测图像矩阵数据显示到右侧画布
            self.detection_img_show(det_arr,self.det_cap_label)
        
    def detection_format_print(self,det_result):
        det_dict = det_result.names
        #获取所有检测结果的综合
        det_boxes = det_result.boxes
        #或缺检测结果中的类别索引号矩阵
        det_cls = det_boxes.cls
        #将cls矩阵转化为能够正常提取的成员numpy矩阵
        det_cls_arr = det_cls.numpy()
        det_cls_unique_arr,det_cls_num_arr = np.unique(det_cls_arr, return_counts=True)
        #使用for循环遍历cls矩阵，把所有物体的类别都print出来
        size = int (len(det_cls_arr))
        size = int (len(det_cls_unique_arr))
        for i in range(size):
            cls_index = det_cls_unique_arr[i]
            #print(f'类别索引号为{det_cls_unique_arr[i]}')
            #使用每一轮得到的索引号访问字典 得到检测的物体
            cls_obj = det_dict[cls_index]
            #print(f'物体名称:[cls_obj]')
            #显示对应物体的数量
            cls_num = det_cls_num_arr[i]
            print(f'{cls_obj}物体数量:{cls_num}')

    # 视频初始化函数
    def video_init(self):
        #视频图像显示定时器的初始化
        self.video_timer = QTimer()
        self.video_timer.setInterval(1)
        #视频选择信号与槽
        self.pushButton_video.clicked.connect(self.video_choose)
        self.video_timer.timeout.connect(self.video_iamge_detect)

    #视频选择函数
    def video_choose(self):
        #先获取视频文件的路径 限制打开文件的格式为视频格式
        path = QFileDialog.getOpenFileName(filter='*.mp4')
        video_path = path[0]
        #判断用户是不是选择了视频
        if video_path:
            #如果选择了视频，才初始化对应的视频对象
            self.video = cv2.VideoCapture(video_path)
            #开启计时器 开始播放视频并检测
            self.video_timer.start()
        else:
            print('用户未选择')

    #视频图像检测
    def video_iamge_detect(self):
        #读取视频对象的视频帧
        ret,arr = self.video.read()
        #先判断视频是不是读完了
        if ret:
            #将原始视频显示到左侧
            self.detection_img_show(arr,self.orig_video_label)
            #将图像矩阵进行检测
            result = self.model(source=arr,verbose = False,conf = self.model_conf)
            #提取带检测的图像矩阵
            det_arr = result[0].plot(conf=self.model_conf)
            #右侧画布上显示带检测框的结果
            self.detection_img_show(det_arr,self.det_video_label)
            #将检测结果返回值作为参数传给格式化打印函数
            self.detection_format_print(result[0])
        #如果ret为假 代表视频播完了 需要关闭定时器 清空显示画布
        else:
            self.video_timer.stop()
            self.orig_video_label.clear()
            self.det_video_label.clear()
            

#main函数，程序的入口
if __name__ == "__main__":
    #要先准备一个QApplication对象，时间循环机制的一个函数
    app = QApplication(sys.argv)
    #示例化对象ui
    ui = mainwindow()
    #显示界面
    ui.show()
    app.exec()

