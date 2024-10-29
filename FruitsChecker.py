import cv2
import pandas as pd
import os
from FruitsDetector import FruitsDetector
from AppleEvaluator import AppleEvaluator

class FruitsChecker:
    def __init__(self, input_image_path, output_image_path=None, csv_output_path=None, type=None):
        self.input_image_path  = input_image_path
        self.output_image_path = output_image_path or "evaluated_" + os.path.basename(input_image_path)
        self.csv_output_path   = csv_output_path   or "evaluated_" + os.path.splitext(os.path.basename(input_image_path))[0] + ".csv"
        self.type              = type
        self.detector          = FruitsDetector()
        self.evaluator         = AppleEvaluator()

    def process(self):
        # 入力画像を読み込む
        image = cv2.imread(self.input_image_path)
        if image is None:
            print(f"画像が見つかりません: {self.input_image_path}")
            return

        # 入力画像から対象の果物の座標を取得する
        fruits_boxes = self.detector.detect(image, self.type)
        output_data  = []

        # 各果物を1つずつ評価する
        for _, row in fruits_boxes.iterrows():
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            fruits_roi     = image[y1:y2, x1:x2]

            # 果物を評価する
            evaluation = self.evaluator.evaluate(fruits_roi)

            # 評価結果を画像に重畳する
            cv2.putText(image, f"{AppleEvaluator.COLOR_KEY}: {evaluation[AppleEvaluator.COLOR_KEY]}", (x1, y2+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            cv2.putText(image, f"{AppleEvaluator.SHINE_KEY}: {evaluation[AppleEvaluator.SHINE_KEY]}", (x1, y2+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            if evaluation[AppleEvaluator.TOTAL_KEY] == AppleEvaluator.GOOD_VALUE:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4) # 緑、太い
            else:
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3) # 青、細い

            # CSVに保存する評価結果データを作成する
            output_data.append({
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                AppleEvaluator.COLOR_KEY: evaluation[AppleEvaluator.COLOR_KEY],
                AppleEvaluator.SHINE_KEY: evaluation[AppleEvaluator.SHINE_KEY]
            })

        # 評価結果を頂上表示した画像を保存する
        cv2.imwrite(self.output_image_path, image)

        # 座標と評価結果をCSVに保存する
        df = pd.DataFrame(output_data)
        df.to_csv(self.csv_output_path, index=False, encoding="utf-8-sig")
