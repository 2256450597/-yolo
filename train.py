from ultralytics import YOLO

#无论你要训练一个识别什么物体的模型 模型的内部架构都是一样的
model = YOLO('yolo11n.pt')

#模型训练
model.train(
    #yaml配置文件路径
    data = 'C:/Users/Leo/Desktop/ultralytics-8.3.86/sitting_pose/data.yaml',
    #模型训练轮次 默认100轮 此处可以减小训练轮次
    epochs = 50,
    #降低数据加载的工作线程数量
    workers = 0 
)