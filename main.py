from environment import Matrix,ReadFile
import visualization as vs,searchAlgorithm as sa

inputResource = ReadFile('../Search/input.txt')
print(inputResource.pickUpPoint())
ORIGIN_MATRIX = (-150,-300)
ORIGIN_MENU = (-700,-300)


#set up matrix
mat = Matrix(inputResource.matrixSize())
mat.addBlocks(inputResource.blocks())
mapMatrix= vs.Matrix(ORIGIN_MATRIX)
mapMatrix.draw(mat.matrix)
mapMatrix.drawStartGoal(inputResource.source(),inputResource.goal())
mapMatrix.drawPickUp(inputResource.pickUpPoint())
robot = vs.Robot(ORIGIN_MATRIX,mapMatrix.size)
costText = vs.Text(ORIGIN_MENU)
search = sa.SearchAlgorithm(mat.matrix,mapMatrix)
pathToGoal = []
costPath = 0
costExpanded = 0

#set up buttons and corresponding functions
button = (vs.Button(ORIGIN_MENU,'Breadth-first search'),
        vs.Button(ORIGIN_MENU,'Uniform-cost search'),
        vs.Button(ORIGIN_MENU,'Iterative deepening search'),
        vs.Button(ORIGIN_MENU,'Greedy-best first search'),
        vs.Button(ORIGIN_MENU,'Graph-search A*'),
        vs.Button(ORIGIN_MENU,'Dijkstra-search')

        )

function_run = { 0:search.findBFS,
                1:search.findUCS,
                2:search.findIDS,
                3:search.findGBFS,
                4:search.findASS,
                5:search.findTSP,
            }


#set up buttons UI
firstPosButton = (50,380)
for i,butt in enumerate(button):
    butt.create((firstPosButton[0],firstPosButton[1] - 50*i))



textPen = vs.Text(ORIGIN_MENU)
# text_pen.print_text((100,680),'University of Science - VNUHCM',FONT_SIZE=11)
# text_pen.print_text((0,640),'PROJECT 1: The Searching Algorithm',FONT_SIZE=19,mode='bold')
# text_pen.print_text((0,610),'Subject: Fundamentals of Artificial Intelligence')
# text_pen.print_text((0,585),'Implemented by : Thai Chi Hien')
# text_pen.print_text((0,560),'Lecture: Pham Trong Nghia')
# text_pen.print_text((0,535),'TA: Nguyen Thai Vu')

# text_pen.print_text((0,500),'Please edit the matrix, starting point, ending point and',FONT_SIZE=14)
# text_pen.print_text((138,478),'input.txt',FONT_SIZE=14,mode='underline')
# text_pen.print_text((0,478),'obstacles in the               file located in the same',FONT_SIZE=14)
# text_pen.print_text((0,456),'directory as this source file',FONT_SIZE=14)

textPen.printText((0,425),'Choose one of the algorithms below to find the path:',FONT_SIZE=14)

noteBlock = vs.Block(ORIGIN_MENU)
noteBlock.printBlock((50,80),vs.COLOR_START_POINT,30,'Starting Point')
noteBlock.printBlock((250,80),vs.COLOR_END_POINT,30,'Goal Point')
noteBlock.printBlock((50,40),vs.COLOR_BLOCK_POINT,30,'Block Point')
noteBlock.printBlock((250,40),vs.COLOR_VISITED_POINT,30,'Visited Point')
noteBlock.printBlock((50,0),vs.COLOR_PICKUP_POINT,30,'Pick Up Point')


def disableAllbuttons(currentButton,search,robot):
    costText.pen.clear()
    if search != None:
        search.clear()
        robot.reset()
    for butt in button:
        if butt == currentButton:continue
        butt.disable()

def enableAllbuttons():
    for butt in button:
        butt.resetButton()


while True:
    # try:
        for i,butt in enumerate(button):
            butt.update()
            if butt.result():
                disableAllbuttons(butt,search,robot)
                if (i!=5):
                    pathToGoal,costPath,costExpanded = function_run[i](inputResource.source(),inputResource.goal())
                    print(pathToGoal)
                else:
                    pathToGoal,costPath,costExpanded = function_run[i](inputResource.source(),inputResource.goal(),inputResource.pickUpPoint())
                    print(pathToGoal)
                # print(pathToGoal.len())
                if pathToGoal :
                    robot.play(pathToGoal)
                    costText.printText((0,-30),'Cost of the path : {0}'.format(costPath),FONT_SIZE=15,mode = 'bold')
                    costText.printText((0,-80),'Cost of the expanded node : {0}'.format(costExpanded),FONT_SIZE=15,mode = 'bold')
                    enableAllbuttons()
                else :
                    costText.printText((0,-30),'No path found',FONT_SIZE=15,mode = 'bold')
                    enableAllbuttons()
    # except Exception as e:
    #     print(e)
    #     break
    # except:
    #     break
