#导入YOLO模块
from ultralytics import YOLO

#初始化用于图像检测的模型 括号内写模型文件的路径
model = YOLO("C:/Users/Leo/Desktop/ultralytics-8.3.86/runs/detect/train2/weights/best.pt")

#把检测源作为参数传参给model
model(source="C:/Users/Leo/Desktop/ultralytics-8.3.86/sitting_pose/train/images/1_jpg.rf.9ea96f3e606c9e8c53d2a0bd0758217b.jpg")
#model(source=0,show=True)                                      

