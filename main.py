import cv2
import numpy as np
from process import Process
from position import Position


reef = cv2.imread('./img/samples/reef/6.jpg')
reef = cv2.resize(reef, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_CUBIC)

reef = Process(reef).scale()

hsv = cv2.cvtColor(reef, cv2.COLOR_BGR2HSV)
kernel = np.ones((4, 4), np.uint8)
kernel2 = np.ones((7, 7), np.uint8)

rf = Position(reef)
planter = rf.planter()
coral = rf.coral()
star = rf.star()
sponge = rf.sponge()

grid = np.zeros([300, 900, 3], dtype=np.uint8)
grid[:] = 255

for i in range(1, 9):
    x = i * 100
    grid = cv2.line(grid, (x, 0), (x, 300), (0, 0, 0), 1)
    if i < 3:
        y = i * 100
        grid = cv2.line(grid, (0, y), (900, y), (0, 0, 0), 1)

for pos in planter:
    center = [pos[i] * 100 + 50 for i in range(2)]
    grid = cv2.circle(grid, center, 40, (0, 242, 255), 4)

for pos in star:
    center = [pos[i] * 100 + 50 for i in range(2)]
    grid = cv2.circle(grid, center, 40, (204, 72, 63), 4)

grid = cv2.ellipse(grid, (coral[0]*100, coral[1]*100+50), (90, 40), 0, 0, 360, (36, 28, 237), 4)
grid = cv2.circle(grid, [sponge[i]*100+50 for i in range(2)], 40, (76, 177, 34), 4)


cv2.imshow('reef', reef)
cv2.imshow('grid', grid)
cv2.waitKey(0)
cv2.destroyAllWindows()
