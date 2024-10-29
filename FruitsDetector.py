import torch

class FruitsDetector:
    X1 = "x1"
    Y1 = "y1"
    X2 = "x2"
    Y2 = "y2"

    _DEFAULT_TYPE = "apple"

    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def detect(self, image, type):
        type = type if type is not None else FruitsDetector._DEFAULT_TYPE
        # YOLOでObject Detectionし、バウンディングボックスの座標を取得する
        results = self.model(image)
        boxes = results.pandas().xyxy[0]

        # 対象の果物のみを返却する
        target_fruits_boxes = boxes[boxes['name'] == type]
        return target_fruits_boxes