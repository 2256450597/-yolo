from ultralytics import YOLO

# 加载模型
# yolov8n.pt 是一个轻量级的预训练模型，会自动下载
model = YOLO("yolov8n.pt")

# 对图片进行预测
# source 可以是本地图片路径，也可以是网络图片 URL
print("正在进行预测...")
results = model.predict(source="https://ultralytics.com/images/bus.jpg", save=True)

print("预测完成！")
print(f"结果保存在: {results[0].save_dir}")
