from math import ceil
import turtle
import numpy as np
from environment import BLOCKED

COLOR_START_POINT = '#3333FF'
COLOR_END_POINT = '#FF0054'
COLOR_BLOCK_POINT = '#FF9933' 
COLOR_VISITED_POINT = '#97E9EF'
COLOR_VISITED_POINT_IDS = '#3D8389'
COLOR_FINISHED_POINT = '#D3008A'
COLOR_PICKUP_POINT = '#FFD700'
ICON_TURTLE = './robot.gif'

screen = turtle.Screen()
screen.setup(width= 1.0,height= 1.0)
try:
    screen.addshape(ICON_TURTLE)
except:
    pass

class Maze:
    def __init__(self,origin =(0,0)) -> None:
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.size = 40
        self.leftmostPos = origin
        self.pen.hideturtle()

    
    def draw(self,matrix):
        screen.tracer(0)
        pos = list(self.leftmostPos)    #origin

        if matrix.shape[1] > 22:
            self.size = 40 - (matrix.shape[1] - 22)*2
        else:self.size = 40 - (matrix.shape[0] - 16)*1.5
        
        self.size = ceil(self.size)
        #draw a row
        for y in range(matrix.shape[0]):
            for x in range(matrix.shape[1]):
                self.drawSquareMatrix(pos,matrix[y][x])
                pos[0] += self.size
            pos[0] = self.leftmostPos[0]
            pos[1] += self.size


        for x in range(matrix.shape[1]):
            pos = (self.leftmostPos[0] + self.size*x + self.size/2 - 2,self.leftmostPos[1] - 30)
            self.pen.up()
            self.pen.setpos(pos)
            self.pen.down()
            self.pen.write(x,font=('Arial', 11, 'normal'))

        for y in range(matrix.shape[0]):
            pos = (self.leftmostPos[0] -20 ,self.leftmostPos[1] + self.size*y + self.size/2 - 2)
            self.pen.up()
            self.pen.setpos(pos)
            self.pen.down()
            self.pen.write(y,align= 'right',font=('Arial', 11, 'normal'))

        self.pen.hideturtle()
        screen.update()
        screen.tracer(1)

    def drawSquareMatrix(self,pos,IsBlock):
        self.pen.up()
        self.pen.setpos(pos)
        self.pen.down()

        if IsBlock == BLOCKED:
            self.pen.fillcolor(COLOR_BLOCK_POINT)
            self.pen.begin_fill()

            for i in range(4):
                self.pen.forward(self.size)           
                self.pen.left(90)
            self.pen.end_fill()
            self.pen.fillcolor('Black')
        else:
            for i in range(4):
                self.pen.forward(self.size)           
                self.pen.left(90)

    def drawStartGoal(self,start,goal,start_color=COLOR_START_POINT,goal_color=COLOR_END_POINT):
        screen.tracer(0)
        self.drawSquare(start,start_color)
        self.drawSquare(goal,goal_color)
        screen.update()
        screen.tracer(1)

    def drawPickUp(self,pickup,pen_color = COLOR_PICKUP_POINT):
        screen.tracer(0)
        for x in pickup:
            self.drawSquare(x,pen_color)
        screen.update()
        screen.tracer(1)

    def drawSquare(self,pos,pen_color):
        screen.tracer(0)
        start_pos = (self.leftmostPos[0] + self.size*pos[0],self.leftmostPos[1] + self.size*pos[1])
        self.pen.speed(0)
        self.pen.pencolor('Black')
        self.pen.width(1)
        self.pen.up()
        self.pen.setpos(start_pos)
        self.pen.down()

        self.pen.fillcolor(pen_color)
        self.pen.begin_fill()

        for i in range(4):
            self.pen.forward(self.size)           
            self.pen.left(90)
        self.pen.end_fill()
        self.pen.fillcolor('Black')
        #screen.update()
        screen.tracer(1)

    
class Robot:
    def __init__(self,pos_matrix,size_block) -> None:
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(3)
        self.pen.pencolor('Green')
        self.pen.width(5)
        self.size = size_block
        self.leftmostPos = pos_matrix

    
    def play(self,path):
        try:
            self.pen.shape(ICON_TURTLE)
        except:
            pass
        self.pen.showturtle()
        self.pen.forward(0)
        temp = path.pop()

        self.pen.up()
        cur_pos = (self.leftmostPos[0] + self.size*temp[1] + self.size/2,
                    self.leftmostPos[1] + self.size*temp[0] + self.size/2)
        self.pen.setpos(cur_pos)
        self.pen.down()
        while path:
            temp = path.pop()
            
            next_pos = (self.leftmostPos[0] + self.size*temp[1] + self.size/2,
                    self.leftmostPos[1] + self.size*temp[0] + self.size/2)
            
            self.pen.setheading(self.pen.towards(next_pos))
            self.pen.forward(self.size)


        return True


    def reset(self):
        self.pen.clear()
        self.pen.hideturtle()
        self.pen.shape('classic')



class Button:
    FONT_SIZE = 12
    FONT = ('Arial', FONT_SIZE, 'bold')
    CURRENT_COLOR = "White"

    def __init__(self,origin,message,shape = 'circle',onetime = True) -> None:
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.fillcolor('White')
        self.leftmostPos = origin
        self.IsClick = False
        self.text = message
        self.pen.shape(shape)
        self.onetime = onetime

    def create(self,pos):
        screen.tracer(0)
        self.pen.hideturtle()
        self.pos = pos
        self.textOnButton()

        self.pen.showturtle()
        screen.tracer(1)

    def textOnButton(self):
        self.pen.up()
        self.pen.setpos(self.leftmostPos[0] + self.pos[0] + 25,self.leftmostPos[1] + self.pos[1] - 20)
        self.pen.down()

        self.pen.write(self.text,font=self.FONT)
        self.pen.up()
        self.pen.setpos(self.leftmostPos[0] + self.pos[0],self.leftmostPos[1] + self.pos[1] - 10)
        self.pen.down()

    def update(self):
        if self.onetime:
            self.pen.onclick(self.eventClickOnetime)
        else:self.pen.onclick(self.eventClick)

    def result(self):
        return self.IsClick

    def eventClickOnetime(self,x,y):
        if not self.IsClick:
            self.eventClickAnimation()
            self.IsClick = True
            
    def eventClick(self,x,y):
        self.eventClickAnimation()
        self.IsClick = not self.IsClick

    def eventClickAnimation(self):
        if self.onetime:
            self.pen.fillcolor('Green')
        else:
            if self.CURRENT_COLOR != "Green":
                self.CURRENT_COLOR = "Green"
            else: 
                self.CURRENT_COLOR = "White"

            self.pen.fillcolor(self.CURRENT_COLOR)

    def resetButton(self):
        self.IsClick = False
        self.pen.fillcolor('White')
        self.CURRENT_COLOR = 'White'
        self.textOnButton()
        self.pen.showturtle()
        

    def disable(self):
        self.pen.hideturtle()
        self.pen.clear()


class Text:
    def __init__(self,origin) -> None:
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.leftmostPos = origin
        self.pen.hideturtle()

    def printText(self,pos,message : str,FONT_SIZE = 12,mode = 'normal'):
        screen.tracer(0)
        self.pen.up()
        self.pen.setpos(self.leftmostPos[0] + pos[0] + 25,self.leftmostPos[1] + pos[1] - 20)
        self.pen.down()

        
        self.pen.write(message,font= ('Arial', FONT_SIZE, mode))
        screen.tracer(1)

class Block(Text):
    def __init__(self, origin,shape='square') -> None:
        super().__init__(origin)
        self.pen.shape(shape)
    

    def printBlock(self,pos,color_block : str,size :int,message : str,FONT_SIZE = 12,mode = 'normal'):
        self.pen.hideturtle()
        self.printText(pos,message,FONT_SIZE,mode)

        screen.tracer(0)
        self.pen.width(1)
        self.pen.up()
        self.pen.setpos(self.leftmostPos[0] + pos[0] - size + 15,self.leftmostPos[1] + pos[1] -25)
        self.pen.down()

        self.pen.fillcolor(color_block)
        self.pen.begin_fill()

        for i in range(4):
            self.pen.forward(size)           
            self.pen.left(90)
        self.pen.end_fill()
        self.pen.fillcolor('Black')
        screen.tracer(1)