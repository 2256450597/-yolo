from ultralytics import YOLO

#无论训练识别什么物体的模型 模型的内部架构都是一样的
model = YOLO('yolo11n.pt')

#模型训练
model.train (
  #配置文件路径
  data = 'myModel.yaml',
  #模型训练轮数 默认100轮，此处可以减小
  epochs = 50,
  #降低数据加载的工作线程数量
  workers = 2
)
