#导入YOLO模块
from ultralytics import YOLO

#初始化用于图像检测的模型 括号内写模型文件的路径
model = YOLO("yolo11n.pt")

#把检测源作为参数传参给model
#model(source="ultralytics/assets",save = True)
model(source=0,show=True)