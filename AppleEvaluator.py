import cv2
import numpy as np
from skimage import exposure

class AppleEvaluator:
    GOOD_VALUE = "Good"
    BAD_VALUE  = "Bad"
    COLOR_KEY  = "Color"
    SHINE_KEY  = "Shiny"
    TOTAL_KEY  = "Total"

    _RED_RATIO       = 0.4
    _SHINE_THRESHOLD = 0.7
    _SHINE_RATIO     = 0.3
    _EDGE_DENSITY    = 0.02
    _SHINE_STDDEV    = 30
    _FRESH_RATIO     = 0.05

    @staticmethod
    def is_vibrant_red(hsv_image):
        # HSVの赤色閾値
        red_lower1 = np.array([0, 100, 100])
        red_upper1 = np.array([10, 255, 255])
        red_lower2 = np.array([170, 100, 100])
        red_upper2 = np.array([180, 255, 255])

        # 赤い領域の割合を計算する
        red_mask1  = cv2.inRange(hsv_image, red_lower1, red_upper1)
        red_mask2  = cv2.inRange(hsv_image, red_lower2, red_upper2)
        red_mask   = cv2.bitwise_or(red_mask1, red_mask2)
        red_ratio  = np.sum(red_mask / 255) / (hsv_image.shape[0] * hsv_image.shape[1])
        #print(f"red_ratio:{red_ratio} red:{np.sum(red_mask)} all:{(hsv_image.shape[0] * hsv_image.shape[1])}")

        return red_ratio > AppleEvaluator._RED_RATIO

    @staticmethod
    def has_shine(image):
        # サイズ統一、グレースケール化
        resized_image = cv2.resize(image, (100, 100))
        gray_image    = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        # ヒストグラム平坦化後の輝度分布
        hist_eq         = exposure.equalize_hist(gray_image)
        shine_threshold = AppleEvaluator._SHINE_THRESHOLD
        shine_ratio     = np.sum(hist_eq > shine_threshold) / hist_eq.size

        # エッジ密度
        edges = cv2.Canny(gray_image, 100, 200)
        edge_density = np.sum(edges / 255) / edges.size

        # 輝度分散
        mean, stddev = cv2.meanStdDev(gray_image)
        #print(f"shine_ratio:{shine_ratio} edge_density:{edge_density} mean:{mean} stddev:{stddev}")

        return (shine_ratio > AppleEvaluator._SHINE_RATIO) and (edge_density > AppleEvaluator._EDGE_DENSITY) and (stddev[0][0] > AppleEvaluator._SHINE_STDDEV)

    @staticmethod
    def evaluate(image):
        hsv_image   = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        red_check   = AppleEvaluator.is_vibrant_red(hsv_image)
        shine_check = AppleEvaluator.has_shine(image)
        return {
            AppleEvaluator.COLOR_KEY: AppleEvaluator.GOOD_VALUE if red_check                 else AppleEvaluator.BAD_VALUE,
            AppleEvaluator.SHINE_KEY: AppleEvaluator.GOOD_VALUE if shine_check               else AppleEvaluator.BAD_VALUE,
            AppleEvaluator.TOTAL_KEY: AppleEvaluator.GOOD_VALUE if red_check and shine_check else AppleEvaluator.BAD_VALUE
        }
