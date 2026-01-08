#导入YOLO模块
from ultralytics import YOLO

#初始化用于图像检测的YOLO模型,括号内写入模型的路径（相对或绝对路径）
model = YOLO("/Users/liukairui/Desktop/环境搭建/ultralytics-8.3.86/runs/detect/train/weights/best.pt")

#把检测元作为参数给model
model(source="/Users/liukairui/Desktop/环境搭建/ultralytics-8.3.86/datasets/images/train/30.jpg", save= True, show = True,conf = 0.7)

#代码形式进行目标检测，此时不会将检测结果的图像保存。想保存show。摄像头source=0，（对应的设备号）show=True,实时看到结果

