import gc
import threading
import time
import cv2
import numpy as np
import torch
import requests
from ultralytics import YOLO
from config import start_time
from data_produce.data_keep import data_keep

model = YOLO("best.pt")
model.to('cuda' if torch.cuda.is_available() else 'cpu')  # 提前指定设备
model.eval()  # 设置为评估模式
qr_detector = cv2.QRCodeDetector()
qr_cache = dict()
CACHE_EXPIRE_SECONDS = 300


def simple_detect_and_show(pic):
    # 读取图像
    nparr = np.frombuffer(pic, np.uint8)
    # 解码为 OpenCV 图像
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # 执行检测
    res = []
    if img is None:
        print("无法解码图像数据")
        return
    results = model(source=img, conf=0.3, verbose=False, device=0 if torch.cuda.is_available() else "cpu")
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        roi = img[int(y1) - 10:int(y2) + 10, int(x1) - 10:int(x2) + 10]
        data, bbox, _ = qr_detector.detectAndDecode(roi)
        if data:
            res.append(data)
    del img  # 手动删除大对象
    gc.collect()  # 强制垃圾回收
    work_time = time.time() - start_time
    print(res)
    file_path = "./data/" + str(int(work_time / 30)) + '.txt'
    threading.Thread(target=data_keep, args=(file_path, res)).start()
    for data in res:
        if data is not None and data.startswith("http"):
            r = requests.get(data)
