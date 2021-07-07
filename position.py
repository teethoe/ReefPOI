import cv2
import numpy as np


def center(mask, n):
    cnts, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in cnts]
    max_index1 = np.argmax(areas)
    M1 = cv2.moments(cnts[max_index1])
    center1 = [int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00'])]
    if n == 1:
        return center1
    else:
        areas.pop(max_index1)
        cnts.pop(max_index1)
        max_index2 = np.argmax(areas)
        M2 = cv2.moments(cnts[max_index2])
        center2 = [int(M2['m10'] / M2['m00']), int(M2['m01'] / M2['m00'])]
        return center1, center2


class Position:
    def __init__(self, img):
        self.img = img
        self.hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        self.located = []

    def planter(self):
        lower = np.array([16, 100, 100])
        upper = np.array([36, 255, 255])
        mask = cv2.inRange(self.hsv, lower, upper)
        centers = center(mask, 2)
        positions = [['' for i in range(2)] for i in range(2)]
        for i in range(2):
            for j in range(2):
                positions[i][j] = centers[i][j] // 100
            self.located.append(positions[i])
        return positions

    def coral(self):
        kernel = np.ones((4, 4), np.uint8)
        lower = np.array([145, 50, 50])
        upper = np.array([175, 255, 255])
        mask = cv2.inRange(self.hsv, lower, upper)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        c = center(mask, 1)
        if c[0] % 100 > 50:
            position = [c[0]//100 + 1, c[1]//100]
        else:
            position = [c[0]//100, c[1]//100]
        self.located.append(position)
        self.located.append([position[0]-1, position[1]])
        return position

    def star(self):
        kernel = np.ones((4, 4), np.uint8)
        kernel2 = np.ones((7, 7), np.uint8)
        lower = np.array([110, 50, 50])
        upper = np.array([130, 255, 255])
        mask = cv2.inRange(self.hsv, lower, upper)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel2)
        centers = center(mask, 2)
        positions = [['' for i in range(2)] for i in range(2)]
        for i in range(2):
            for j in range(2):
                positions[i][j] = centers[i][j] // 100
            self.located.append(positions[i])
        return positions

    def sponge(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        ret, th = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        kernel = np.ones((4, 4), np.uint8)
        kernel2 = np.ones((2, 2), np.uint8)
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
        th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel2)
        cnts, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = [cnt for cnt in cnts if cv2.contourArea(cnt) > 100]

        centers = ['' for i in range(len(cnts))]
        for i in range(len(cnts)):
            M = cv2.moments(cnts[i])
            centers[i] = [int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])]
        i = 0
        while i < len(centers):
            x, y = centers[i]
            if x < 25 or y < 25 or x > 875 or y > 275:
                centers.pop(i)
            else:
                i += 1

        found = False
        i = 0
        while not found and i < len(centers):
            c = [centers[i][a]//100 for a in range(2)]
            print(i)
            if c not in self.located:
                position = c
                found = True
            i += 1
        return position
