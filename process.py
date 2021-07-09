import cv2
import numpy as np
import math


def get_rect(cnt):
    x, y, w, h = cnt
    tl = (x, y)
    tr = (x+w, y)
    bl = (x, y+h)
    br = (x+w, y+h)
    return tl, tr, bl, br


def transform(img, pts):
    pts = np.float32(pts)
    dst = np.float32(get_rect([0, 0, 900, 300]))
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(img, M, (900, 300))
    return warped


class Process:
    def __init__(self, img):
        self.img = img
        self.hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def scale(self):
        lower1 = np.array([0, 0, 0])
        upper1 = np.array([40, 80, 255])
        mask1 = cv2.inRange(self.hsv, lower1, upper1)
        lower2 = np.array([140, 0, 0])
        upper2 = np.array([180, 40, 255])
        mask2 = cv2.inRange(self.hsv, lower2, upper2)
        mask = cv2.bitwise_not(mask1 + mask2)
        kernel = np.ones((7, 7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        dst = cv2.cornerHarris(mask, 2, 3, 0.04)

        dst_norm = np.empty(dst.shape, dtype=np.float32)
        cv2.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        dst_norm_scaled = cv2.convertScaleAbs(dst_norm)
        self.img[dst_norm_scaled > 100] = (0, 0, 255)
        points = []
        for i in range(dst_norm.shape[0]):
            for j in range(dst_norm.shape[1]):
                if dst_norm_scaled[i][j] > 100:
                    points.append((j, i))

        maxComb = ['' for i in range(4)]
        h, w = self.img.shape[:2]
        ref = [[0, 0], [w, 0], [0, h], [w, h]]
        for i in range(4):
            distances = [math.dist(pt, ref[i]) for pt in points]
            maxComb[i] = points[np.argmin(distances)]

        trans = transform(self.img, maxComb)

        return trans
