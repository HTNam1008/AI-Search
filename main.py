from environment import Matrix, ReadFile
import visualization as vs
import searchAlgorithm as sa
import time

# Khởi tạo các biến và đối tượng
inputResource = ReadFile('./input.txt')
ORIGIN_MATRIX = (-700, -300)
ORIGIN_MENU = (150, -300)

mat = Matrix(inputResource.matrixSize())
mat.addBlocks(inputResource.blocks())
mapMatrix = vs.Maze(ORIGIN_MATRIX)
mapMatrix.draw(mat.matrix)
mapMatrix.drawStartGoal(inputResource.source(), inputResource.goal())
robot = vs.Robot(ORIGIN_MATRIX, mapMatrix.size)
costText = vs.Text(ORIGIN_MENU)
search = sa.SearchAlgorithm(mat.matrix, mapMatrix)
pathToGoal = []
costPath = 0
costExpanded = 0

button = (
    vs.Button(ORIGIN_MENU, 'Breadth-first Search'),
    vs.Button(ORIGIN_MENU, 'Uniform-cost Search'),
    vs.Button(ORIGIN_MENU, 'Iterative Deepening Search'),
    vs.Button(ORIGIN_MENU, 'Greedy-best First Search'),
    vs.Button(ORIGIN_MENU, 'Graph Search A*'),
    vs.Button(ORIGIN_MENU, 'Travelling Sales Man Search')
)

function_run = {
    0: search.findBFS,
    1: search.findUCS,
    2: search.findIDS,
    3: search.findGBFS,
    4: search.findASS,
    5: search.findTSP,
}

firstPosButton = (50, 380)
for i, butt in enumerate(button):
    butt.create((firstPosButton[0], firstPosButton[1] - 50 * i))

textPen = vs.Text(ORIGIN_MENU)
textPen.printText((120, 680), 'University of Science - VNUHCM', FONT_SIZE=11)
textPen.printText((0, 640), 'PROJECT 1: The Searching Algorithm', FONT_SIZE=19, mode='bold')
textPen.printText((180, 610), 'Group: 07', mode='bold', FONT_SIZE=15)

textPen.printText((0, 425), 'Choose one of the algorithms below to find the path:', FONT_SIZE=14)

noteBlock = vs.Block(ORIGIN_MENU)
noteBlock.printBlock((50, 80), vs.COLOR_START_POINT, 30, 'Starting Point')
noteBlock.printBlock((250, 80), vs.COLOR_END_POINT, 30, 'Goal Point')
noteBlock.printBlock((50, 40), vs.COLOR_BLOCK_POINT, 30, 'Block Point')
noteBlock.printBlock((250, 40), vs.COLOR_VISITED_POINT, 30, 'Visited Point')
noteBlock.printBlock((50, 0), vs.COLOR_PICKUP_POINT, 30, 'Pick Up Point')


def disableAllbuttons(currentButton, search, robot):
    costText.pen.clear()
    if search != None:
        search.clear()
        robot.reset()
    for butt in button:
        if butt == currentButton:
            continue
        butt.disable()


def enableAllbuttons():
    for butt in button:
        butt.resetButton()


while True:
    for i, butt in enumerate(button):
        butt.update()
        if butt.result():
            disableAllbuttons(butt, search, robot)
            if i != 5:
                pathToGoal, costPath, costExpanded = function_run[i](inputResource.source(), inputResource.goal())
            else:
                mapMatrix.drawPickUp(inputResource.pickUpPoint())
                time.sleep(1)
                pathToGoal, costPath, costExpanded = function_run[i](inputResource.source(), inputResource.goal(),
                                                                      inputResource.pickUpPoint())
            if pathToGoal:
                robot.play(pathToGoal)
                costText.printText((-10, -40), 'Cost of the path : {0}'.format(costPath), FONT_SIZE=15, mode='bold')
                costText.printText((-10, -90), 'Cost of the expanded node : {0}'.format(costExpanded), FONT_SIZE=15,
                                   mode='bold')
                enableAllbuttons()
            else:
                costText.printText((-10, -40), 'No path found', FONT_SIZE=15, mode='bold')
                enableAllbuttons()
