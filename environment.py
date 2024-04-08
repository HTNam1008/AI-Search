import numpy as np

BLOCKED = 2
VISITED = 1

class Matrix:
    def __init__(self,size) -> None:    
        self.matrix = np.zeros(size,dtype=int)


    def addBlocks(self,blockList):
        while blockList:
            block = blockList.pop(0)
            self.addBlock(block)

    def addBlock(self,points):
        for i in range(len(points)):
            if(i == len(points) - 1):
                self.drawLine(points[i],points[0])
            else: self.drawLine(points[i],points[i+1])


    def drawLine(self,pointA,pointB):  #A(x0,y0) ,B(x1,y1)
        xA = pointA[1]
        yA = pointA[0]
        xB = pointB[1]
        yB = pointB[0]

        if not ( 0 <= xA < self.matrix.shape[0] and 0 <= yA < self.matrix.shape[1]      #out of matrix
                and 0 <= xB < self.matrix.shape[0] and 0 <= yB < self.matrix.shape[1]):
                raise Exception("point is out of matrix")
    
        if pointA == pointB:      #the same point
            self.matrix[xA,yA] = BLOCKED
            return
            
        self.matrix[xA,yA] = BLOCKED
        self.matrix[xB,yB] = BLOCKED
        drawLineVertical = abs(xB - xA) < abs(yB-yA) 
        if drawLineVertical:
            xA,yA,xB,yB = yA,xA,yB,xB

        if xA > xB :     #draw from left to right
            xA,yA,xB,yB = xB,yB,xA,yA
        
        x = np.arange(xA + 1,xB)
        y = np.round(((yB - yA) / (xB - xA)) * (x - xA) + yA).astype(int)
        #x = x.tolist()
        #y = y.tolist()
        if drawLineVertical: x,y =y,x

        self.matrix[x,y] = BLOCKED



class ReadFile:
    def __init__(self,filename) -> None:
        file  = open(filename)
        self.resource = file.readlines()
        file.close()

        #First line
        temp = list(map(int,self.resource[0].split(' ')))
        m,n = temp[0],temp[1]
        self.size = (n,m)

        #Second line
        temp = list(map(int,self.resource[1].split(' '))) 
        self.pickUp=[]
        xS = temp.pop(0)
        yS = temp.pop(0)
        xG = temp.pop(0)
        yG = temp.pop(0)
        self.S = (xS,yS)
        self.G = (xG,yG)

        while temp:
                x = temp.pop(0)
                y = temp.pop(0)
                point = (x,y)
                self.pickUp.append(point)
        
        #Third line
        n = int(self.resource[2])
        self.blockList = []
        for i in range(n):
            temp = list(map(int,self.resource[3 + i].split(' '))) 
            blocks = []
            while temp:
                x = temp.pop(0)
                y = temp.pop(0)
                point = (x,y)
                blocks.append(point)
            self.blockList.append(blocks)
        
      
    
    
    def matrixSize(self):
        return self.size

    def source(self):
        return self.S

    def goal(self):
        return self.G

    def blocks(self):
        return self.blockList
    
    def pickUpPoint(self):
        return self.pickUp
    
