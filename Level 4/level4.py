import numpy as np
import cv2 as cv
import math
import time
import collections
import random
import ctypes

# row ~ y axis ; column ~ x axis
# point P in input ~ maze[P[1], P[0]]
# value in Maze and Color in BGR
# -1  | border       | (115, 115, 115) 
#  0  | none         | (0, 0, 0)
#  1  | start point  | (6, 255, 248)
#  2  | goal point   | (0, 0, 255)
#  3  | pickup point | (0, 255, 255)
#  4  | route        | (255, 210, 77)
# >=5 | polygon      | random color


# === READ INPUT ===
nameInfile = input("Input file name: ")
inFile = open(nameInfile, "r")
col, row = list(map(int, inFile.readline().split(',')))
line = list(map(int, inFile.readline().split(',')))
S = (line[1], line[0]) 
G = (line[3], line[2])
Pi = line[4:]
nPo = list(map(int, inFile.readline().split()))[0]
Po = [[]] * nPo
for i in range(nPo):
    Po[i] = list(map(int, inFile.readline().split(',')))
speed = list(map(int, inFile.readline().split()))[0]
inFile.close()

boxSize = 27
img = np.ones(((row + 1) * boxSize, (col + 1) * boxSize, 3), 'uint8') * 255
maze = np.zeros((row + 1, col + 1), dtype='int8')

# === HELPER ===
def renderPoint(x_coord, y_coord, value):
    y_coord = row - y_coord
    v1 = (x_coord * boxSize, y_coord * boxSize)
    v2 = ((x_coord + 1) * boxSize, (y_coord + 1) * boxSize)
    color = (0, 0, 0)
    cv.rectangle(img, v1, v2, color)
    if value != 0:
        t1 = list(v1); t2 = list(v2)
        t1[0] += 1; t1[1] += 1
        t2[0] -= 1; t2[1] -= 1
        v1 = tuple(t1)
        v2 = tuple(t2)
        color = (0, 222, 255)
        font = cv.FONT_HERSHEY_SIMPLEX
        org = (x_coord * boxSize + 5, y_coord * boxSize + 21)
        if value == -1:
            color = (255, 115, 115)
            cv.rectangle(img, v1, v2, color, -1)
        elif value == 1:
            color=(255, 255, 0)
            cv.rectangle(img, v1, v2, color, -1)
            cv.putText(img, 'S', org, font, 0.75, (0, 0, 0), 2, cv.LINE_AA)
        elif value == 2:
            color = (84, 0, 255)
            cv.rectangle(img, v1, v2, color, -1)
            cv.putText(img, 'G', org, font, 0.75, (0, 0, 0), 2, cv.LINE_AA)
        elif value == 3:
            color = (0, 255, 255)
            cv.rectangle(img, v1, v2, color, -1)
        elif value == 4:
            color = (204, 0, 204)
            cv.rectangle(img, v1, v2, color, -1)
            cv.putText(img, "r", org, font, 0.75, (0, 0, 0), 2, cv.LINE_AA)
        elif value >= 5:
            color=(0, 204, 0)
            cv.rectangle(img, v1, v2, color, -1)

def round(x):
    if x - math.floor(x) >= math.ceil(x) - x:
        return math.ceil(x)
    return math.floor(x)

def drawLine(point1, point2, value):
    if (point1[0] == point2[0]):
        for i in range(min(point1[1], point2[1]), max(point1[1], point2[1]) + 1):
            maze[i, point1[0]] = value
        return
    if (point1[1] == point2[1]):
        for i in range(min(point1[0], point2[0]), max(point1[0], point2[0]) + 1):
            maze[point1[1], i] = value
        return
    slope = (point1[1] - point2[1]) / (point1[0] - point2[0])
    intercept = point1[1] - slope * point1[0]
    for i in range(min(point1[0], point2[0]), max(point1[0], point2[0]) + 1):
       maze[round(slope * i + intercept), i] = value
    for i in range(min(point1[1], point2[1]), max(point1[1], point2[1]) + 1):
       maze[i, round((i - intercept) / slope)] = value


# === INIT ===
# start point
maze[S] = 1
# goal point  
maze[G] = 2  
# pickup point
for i in range(0, len(Pi), 2):
    maze[Pi[i+1], Pi[i]] = 3
# polygon
for i in range(nPo):
    for j in range(0, len(Po[i]), 2):
        maze[Po[i][j + 1], Po[i][j]] = 5 + i
for i in range(nPo):
    for j in range(0, len(Po[i])-3, 2):
        drawLine(Po[i][j:j + 2], Po[i][j + 2:j + 4], i + 5)
    drawLine(Po[i][-2:], Po[i][0:2], i + 5)
# fill border in maze
for i in range(row + 1):
    maze[i, 0] = maze[i, col] = -1
for i in range(col + 1):
    maze[0, i] = maze[row, i] = -1
# draw graph
for i in range(0, col + 1):
    for j in range(0, row + 1):
        renderPoint(i, j, maze[j, i])

# Using breadthFirstSearch to find route
dx = [0,-1, 0, 1,-1,-1, 1, 1]
dy = [1, 0,-1, 0, 1,-1,-1, 1]


def breadthFirstSearch(maze, start_point):
    queue = collections.deque([[start_point]])
    visited = set()
    visited.add(start_point)
    while queue:
        path = queue.popleft()
        current_row, current_col = path[-1]
        if maze[current_row, current_col] == 2:
            return path
        for direction in range(8):
            new_row = current_row + dy[direction]
            new_col = current_col + dx[direction]
            if 0 < new_col < col and 0 < new_row < row:
                if (maze[new_row][new_col] == 0 or maze[new_row][new_col] == 2) and (new_row, new_col) not in visited:
                    # Skip steps that go through the polygon
                    if direction > 3:
                        if direction == 4 and maze[new_row, new_col + 1] == maze[new_row - 1, new_col] and maze[new_row - 1, new_col] >= 5:
                            continue
                        if direction == 5 and maze[new_row, new_col + 1] == maze[new_row + 1, new_col] and maze[new_row + 1, new_col] >= 5:
                            continue
                        if direction == 6 and maze[new_row, new_col - 1] == maze[new_row + 1, new_col] and maze[new_row + 1, new_col] >= 5:
                            continue
                        if direction == 7 and maze[new_row, new_col - 1] == maze[new_row - 1, new_col] and maze[new_row - 1, new_col] >= 5:
                            continue
                    queue.append(path + [(new_row, new_col)])
                    visited.add((new_row, new_col))



move = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        # up    left-top   left  left-bottom  down  right-bot  right  right-top
def movePolygons():
    for k in range(5, nPo + 5):
        step = random.randint(1, 100) % 4 * 2
        dr = move[step][0]
        dc = move[step][1]
        collision = False
        for r in range(1, row):
            for c in range(1, col):
                if maze[r][c] == k:
                    if 0 < r + dr < row and 0 < c + dc < col:
                        if maze[r + dr][c + dc] in [-1, 1, 2, 4] or (maze[r + dr][c + dc] >= 5 and maze[r + dr][c + dc] != k):
                            collision = True
                            break
                    else:
                        collision = True
                        break               
            if collision:
                break
        if collision == False:
            if step < 3:
                for r in range(row - 1, 0, -1):
                    for c in range(1, col):
                        if maze[r][c] == k and 0 < r + dr < row and 0 < c + dc < col:
                            maze[r][c] = 0
                            maze[r + dr][c + dc] = k
            elif step == 3:
                for r in range(1, row):
                    for c in range(1, col):
                        if maze[r][c] == k and 0 < r + dr < row and 0 < c + dc < col:
                            maze[r][c] = 0
                            maze[r + dr][c + dc] = k    
            elif step < 7:
                for r in range(1, row):
                    for c in range(col - 1, 0, -1):
                        if maze[r][c] == k and 0 < r + dr < row and 0 < c + dc < col:
                            maze[r][c] = 0
                            maze[r + dr][c + dc] = k
            else:
                for r in range(row - 1, 0, -1):
                    for c in range(col - 1, 0, -1):
                        if maze[r][c] == k and 0 < r + dr < row and 0 < c + dc < col:
                            maze[r][c] = 0
                            maze[r + dr][c + dc] = k


def updateGraph():
    for i in range(0, col + 1):
        for j in range(0, row + 1):
            renderPoint(i, j, maze[j, i])

# Check if can go from p1(r1, c1) to p2(r2, c2) or not
# p1, p2 is already in the maze 
def canGo(maze, p1, p2):
    d = (p2[1] - p1[1], p2[0] - p1[0])
    i, j = p2[0], p2[1]
    if maze[p2] == 0 or maze[p2] == 2:
        # Skip step that go through the polygon
        if (d == (-1, 1) and maze[i, j + 1] == maze[i - 1, j] and maze[i - 1, j] >= 5) or \
           (d == (-1,-1) and maze[i, j + 1] == maze[i + 1, j] and maze[i + 1, j] >= 5) or \
           (d == ( 1,-1) and maze[i, j - 1] == maze[i + 1, j] and maze[i + 1, j] >= 5) or \
           (d == ( 1, 1) and maze[i, j - 1] == maze[i - 1, j] and maze[i - 1, j] >= 5):
            return False
        return True
    return False

# cost between two point
def calCost(p1, p2):
        t = (route[0][0] - prevS[0], route[0][1] - prevS[1])
        if t in move[::2]:
            return 1.0
        return 1.5

# cost of route
cost = 0
count = 0
prevS = None
route = breadthFirstSearch(maze, S)
if route == None:
    count += 1
else:
    route = collections.deque(route)
    isDeque = True
    prevS = route.popleft()
    if len(route) < 2:
        ctypes.windll.user32.MessageBoxW(0, "GO TO GOAL SUCESSFULLY!", "Message", 1)
        cv.destroyAllWindows()
    elif canGo(maze, prevS, route[0]):  # go next
        cost += calCost(prevS, route[0])
        maze[route[0]] = 4
prev = route[0]

# cv.namedWindow("Robot find route", cv.WINDOW_NORMAL)
cv.imshow("Robot find route", img)
print("Press Enter to run...")
# wait until press Enter
while cv.waitKey(0) != 13:
    pass



updateGraph()
cv.imshow("Robot find route", img)

# cv.imwrite("pic0.jpg", img)



jump = False
while cv.waitKey(1000 // speed) != ord('q') and cv.getWindowProperty("Robot find route", 0) >= 0:
    if count > 1000:
        ctypes.windll.user32.MessageBoxW(0, "CAN'T FIND ROUTE!", "Message", 1)
        break
    if route == None: # got stuck
        count += 1
        route = breadthFirstSearch(maze, prevS) # find new route
        if route == None:
            movePolygons()
        else:
            count = 0
            route = collections.deque(route)
            jump = True
    else:
        jump = True
    if jump:
        jump = False
        movePolygons()
        prevS = route.popleft()
        if len(route) < 2:
            ctypes.windll.user32.MessageBoxW(0, "GO TO GOAL SUCESSFULLY!", "Message", 1)
            break
        if canGo(maze, prevS, route[0]):  # if can go to next point, delete prev, go next
            maze[prevS] = 0
            maze[route[0]] = 4
            cost += calCost(prevS, route[0])
        else: # stuck, clear old route
            route = None
    
    img = np.ones(((row + 1) * boxSize, (col + 1) * boxSize, 3), 'uint8') * 255
    updateGraph()
    cv.imshow("Robot find route", img)

# print total cost to output file
outFile = open("output.txt", "w+")
outFile.write("%f" % cost)
outFile.close()

cv.destroyAllWindows()