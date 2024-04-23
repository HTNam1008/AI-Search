import random
from visualization import COLOR_VISITED_POINT_IDS, Maze,COLOR_VISITED_POINT,COLOR_FINISHED_POINT
from environment import BLOCKED,VISITED,np
from sys import maxsize
from itertools import permutations
from graph import Graph

class SearchAlgorithm:
    
    def __init__(self,graph,visual) -> None:
        self.moveset = [self.right,self.down,self.left,self.up]
        random.shuffle(self.moveset)
        self.visited = np.copy(graph)
        self.originalGraph = graph
        self.frontier = []
        self.visual = Maze(visual.leftmostPos)
        self.visual.size = visual.size
        self.allpaths = {}

    #Breath First Search
    def findBFS(self,startPoint : tuple,goalPoint : tuple):
        '''
        Breath First Search
        '''

        start = (startPoint[1],startPoint[0])
        goal = (goalPoint[1],goalPoint[0])

        if not (self.isValidMove(start) and self.isValidMove(goal)):  
            raise Exception("Invalid start or goal point")
        
        if (start == goal):
            return [start],0,0

        self.visited[start] = VISITED
        self.frontier = []
        self.frontier.append((start,(-1,-1)))           #the second point is the previous of the first point
        expandedCost = 0

        while self.frontier:
            currentMove = self.frontier.pop(0)
            self.allpaths[currentMove[0]] = currentMove[1]
            expandedCost += 1
            if currentMove[0] != start:
                self.visual.drawSquare((currentMove[0][1],currentMove[0][0]),COLOR_VISITED_POINT)
            if currentMove[0] == goal:
                self.visual.drawSquare((currentMove[0][1],currentMove[0][0]),COLOR_FINISHED_POINT)
                break

            for movefrom in self.moveset:
                posibleMove = movefrom(currentMove)
                if self.isValidMove(posibleMove[0]):
                    self.visited[posibleMove[0]] = VISITED
                    self.frontier.append(posibleMove)
            random.shuffle(self.moveset)
                    
        path = goal
        result = []
        result.append(path)
        cost = -1
        while self.allpaths:
            if path in self.allpaths:
                path = self.allpaths[path]
                cost += 1
                if path[0] == -1:
                    break
                result.append(path)
            else:
                result.clear()
                break
        return result,cost,expandedCost

    #Uniform Cost Search
    def findUCS(self,startPoint : tuple,goalPoint : tuple):
        '''
        Uniform Cost Search
        '''

        start = (startPoint[1],startPoint[0])
        goal = (goalPoint[1],goalPoint[0])
        if not (self.isValidMove(start) and self.isValidMove(goal)):  
            raise Exception("Invalid start or goal point")

        if (start == goal):
            return [start],0,0

        self.visited[start] = VISITED
        self.frontier = {}
        self.frontier[start] = (0,(-1,-1))
        #self.frontier.append((0,start,(-1,-1)))     #(cost to current point,current point,previous point)
        expandedCost = 0

        while self.frontier:
            
            currentMove = min(self.frontier, key=self.frontier.get)
            self.visited[currentMove] = VISITED
            expandedCost += 1
            if currentMove != start:
                self.visual.drawSquare((currentMove[1],currentMove[0]),COLOR_VISITED_POINT)
            self.allpaths[currentMove] = self.frontier[currentMove]
            
            if currentMove == goal:
                self.visual.drawSquare((currentMove[1],currentMove[0]),COLOR_FINISHED_POINT)
                break

            for movefrom in self.moveset:
                cost = 1    #cost in each step
                posibleMove_newmove,posibleMove_oldmove = movefrom((currentMove,self.frontier[currentMove][1]))  
                posibleMove = (self.frontier[currentMove][0] + cost,posibleMove_newmove,posibleMove_oldmove)   #Ex: posibleMove = (12,(7,8),(7,7))
                if self.isValidMove(posibleMove[1]):
                    if not posibleMove[1] in self.frontier:
                        self.frontier[posibleMove[1]] = (posibleMove[0],posibleMove[2])
                    elif posibleMove[0] < self.frontier[posibleMove[1]][0]:
                        self.frontier[posibleMove[1]] = (posibleMove[0],posibleMove[2])
            self.frontier.pop(currentMove)
            random.shuffle(self.moveset)

        #self.frontier.clear()
        path = goal
        result = []
        result.append(path)
        if path in self.allpaths:
            pathCost = self.allpaths[path][0]
        else:
            result.clear()
            return result,0,0
        while self.allpaths:
            # if path in self.allpaths[path][1]:
                path = self.allpaths[path][1]
                if path[0] == -1:
                    break
                result.append(path)
            # else:
            #     result.clear()
            #     break
        return result,pathCost,expandedCost
    
    #Iterative deepening Search
    def findIDS(self,startPoint,goalPoint,visualize = True):
        '''
        Iterative Deepening Search
        '''
        self.listColor = [COLOR_VISITED_POINT,COLOR_VISITED_POINT_IDS]
        self.INDEX = False


        start = (startPoint[1],startPoint[0])
        goal = (goalPoint[1],goalPoint[0])
        if not (self.isValidMove(start) and self.isValidMove(goal)):  
            raise Exception("Invalid start or goal point")

        if (start == goal):
            return [start],0,0

        expandedCost = 0
        depth = 1
        MAX_DEPTH = self.visited.shape[0]*self.visited.shape[1]
        self.frontier = []

        while depth <= MAX_DEPTH:
            finish,expandedCost = self.DLS(start,goal,depth,visualize)
            if finish: break
            self.visited = np.copy(self.originalGraph)
            self.allpaths.clear()
            self.frontier.clear()
            depth *= 2
            #self.INDEX = not self.INDEX
            self.visual.pen.clear()
            expandedCost = 0

        path = goal
        result = []
        cost = -1
        result.append(path)
        while self.allpaths:
            if path in self.allpaths:
                path = self.allpaths[path]
                cost += 1
                if path[0] == -1:
                    break
                result.append(path)
            else:
                result.clear()
                break
            
        return result,cost,expandedCost
        

    def DLS(self,start,goal,limit_depth,visualize):
        #self.visited[start] = VISITED
        
        self.frontier.append((start,(-1,-1)))           #the second point is the previous of the first point

        depth = -1
        reached = False
        success = False
        expandedCost = 0
        previous_point = [self.frontier[0][1],(-2,-2)]

        while self.frontier:
            currentMove = self.frontier.pop()
            if currentMove[1] == previous_point[0]:
                depth += 1
                previous_point[0] = currentMove[0]
                previous_point[1] = currentMove[1]
            elif currentMove[1] == previous_point[1]:
                pass
            else:
                depth -= 1
                previous_point[0] = currentMove[0]
                previous_point[1] = currentMove[1]

            self.allpaths[currentMove[0]] = currentMove[1]
            self.visited[currentMove[0]] = VISITED
            expandedCost += 1
            if currentMove[0] == goal:
                self.visual.drawSquare((currentMove[0][1],currentMove[0][0]),COLOR_FINISHED_POINT)
                success = True
                break
            if visualize and currentMove[0] != start:
                self.visual.drawSquare((currentMove[0][1],currentMove[0][0]),self.listColor[self.INDEX])
            
            for movefrom in self.moveset:
                posibleMove = movefrom(currentMove)
                if self.isValidMove(posibleMove[0]) and depth < limit_depth:
                    self.frontier.append(posibleMove)
        
        return success,expandedCost

    #Greedy Best First Search
    def findGBFS(self,startPoint,goalPoint):
        '''
        Greedy Best First Search
        '''
        start = (startPoint[1],startPoint[0])
        goal = (goalPoint[1],goalPoint[0])
        reached = False
        if not (self.isValidMove(start) and self.isValidMove(goal)):  
            raise Exception("Invalid start or goal point")
        
        if (start == goal):
            return [start],0,0


        self.visited[start] = VISITED
        self.frontier = []
        self.frontier.append((start,(-1,-1))) 
        expandedCost = 0
        reached = False

        while self.frontier:
            self.frontier.sort(key= lambda move: self.heuristic(move[0],goal))
            currentMove = self.frontier.pop(0)
            #currentMove = min(self.frontier,key= lambda move: self.heuristic(move[0],goal))
            
            self.allpaths[currentMove[0]] = currentMove[1]
            if currentMove[0] == goal:
                self.visual.drawSquare((currentMove[0][1],currentMove[0][0]),COLOR_FINISHED_POINT)
                break
            self.visited[currentMove[0]] = VISITED
            expandedCost += 1
            if currentMove[0] != start:
                self.visual.drawSquare((currentMove[0][1],currentMove[0][0]),COLOR_VISITED_POINT)


            #self.frontier.clear()
            for movefrom in self.moveset:
                posibleMove = movefrom(currentMove)
                if self.isValidMove(posibleMove[0]):
                    self.frontier.append(posibleMove)
            
            random.shuffle(self.moveset)
        path = goal
        result = []
        cost = -1
        result.append(path)
        while self.allpaths:
            if path in self.allpaths:
                path = self.allpaths[path]
                cost += 1
                if path[0] == -1:
                    break
                result.append(path)
            else:
                result.clear()
                break
            
        return result,cost,expandedCost

    #A* Search
    def findASS(self,startPoint,goalPoint):
        '''
        A* Search
        '''

        start = (startPoint[1],startPoint[0])
        goal = (goalPoint[1],goalPoint[0])
        reached = False
        if not (self.isValidMove(start) and self.isValidMove(goal)):  
            raise Exception("Invalid start or goal point")
        
        if (start == goal):
            return [start],0,0

        self.visited[start] = VISITED
        self.frontier = {}
        self.frontier[start] = (0,(-1,-1))
        expandedCost = 0

        while self.frontier:
            currentMove = self.bestway(goal)
            self.allpaths[currentMove[0]] = currentMove[1]
            self.visited[currentMove[0]] = VISITED
            expandedCost += 1
            if currentMove[0] != start:
                self.visual.drawSquare((currentMove[0][1],currentMove[0][0]),COLOR_VISITED_POINT)
            
            if currentMove[0] == goal:
                self.visual.drawSquare((currentMove[0][1],currentMove[0][0]),COLOR_FINISHED_POINT)
                break
            
            for movefrom in self.moveset:
                cost = 1    #cost in each step
                posibleMove_newmove,posibleMove_oldmove = movefrom((currentMove[0],currentMove[1][1]))  
                posibleMove = (currentMove[1][0] + cost,posibleMove_newmove,posibleMove_oldmove)
                if self.isValidMove(posibleMove[1]):
                    if not posibleMove[1] in self.frontier:
                        self.frontier[posibleMove[1]] = (posibleMove[0],posibleMove[2])
                    else:
                        move_in_frontier = self.frontier[posibleMove[1]]
                        f_cost_current = self.f((posibleMove[0],posibleMove[1]),goal)
                        f_cost_old = self.f((move_in_frontier[0],posibleMove[1]),goal)
                        if f_cost_current < f_cost_old:
                            self.frontier[posibleMove[1]] = (posibleMove[0],posibleMove[2])
    
            self.frontier.pop(currentMove[0])
            random.shuffle(self.moveset)
                    
        path = goal
        result = []
        result.append(path)
        if(path in self.allpaths):  
            pathCost = self.allpaths[path][0]
        else:
            result.clear()
            return result,0,0
        while self.allpaths:
            if path in self.allpaths:
                path = self.allpaths[path][1]
                if path[0] == -1:
                    break
                result.append(path)
            else:
                result.clear()
                break

        return result,pathCost,expandedCost

    def heuristic(self,point,goal):     #the Manhattan distance
        return abs(point[0] - goal[0]) + abs(point[1] - goal[1])


    def f(self,move : tuple,goal):    
        g = move[0]
        h = self.heuristic(move[1],goal)
        return g + h

    def bestway(self,goal):
        result = 0  #dump value
        minValue = self.visited.shape[0]*self.visited.shape[1] + 1
        for move in self.frontier:
            f_cost = self.f((self.frontier[move][0],move),goal)
            if f_cost < minValue:
                minValue = f_cost
                result = move
            elif f_cost == minValue:
                if self.heuristic(move,goal) < self.heuristic(result,goal):
                    result = move

        return (result, self.frontier[result])
        


    #direction
    def right(self,move):
        newpoint = list(move[0])
        newpoint[1] += 1
        newpoint = tuple(newpoint)
        result = (newpoint,move[0])
        return result
        
    def left(self,move):
        newpoint = list(move[0])
        newpoint[1] -= 1
        newpoint = tuple(newpoint)
        result = (newpoint,move[0])
        return result

    def up(self,move):
        newpoint = list(move[0])
        newpoint[0] += 1
        newpoint = tuple(newpoint)
        result = (newpoint,move[0])
        return result

    def down(self,move):
        newpoint = list(move[0])
        newpoint[0] -= 1
        newpoint = tuple(newpoint)
        result = (newpoint,move[0])
        return result

    #check next move
    def isValidMove(self,point):
        return (0 <= point[0] < self.visited.shape[0]  #go out of maze
            and 0 <= point[1] < self.visited.shape[1]
            and not self.visited[point])               #obstacle or already visited

    #reset
    def clear(self):
        self.visual.pen.clear()
        self.visited = np.copy(self.originalGraph)
        self.frontier.clear()
        self.allpaths.clear()
    
    # implementation of traveling Salesman Problem
    def travellingSalesmanSearch(self,graph: Graph, s: int, V: int):
        # store all vertex apart from source vertex
        vertex = []
        for i in range(V):
            if i != s and i!=V-1:
                vertex.append(i)
    
        # store minimum weight Hamiltonian Cycle
        minPath = maxsize
        minPathSequence = None
        nextPermutation=permutations(vertex)
        adj=graph.graphAdj()
        for i in nextPermutation:
    
            # store current Path weight(cost)
            currentPathWeight = 0
    
            # compute current path weight
            k = s
            for j in i:
                temp=adj[k]
                for l in temp:
                    if (l[0]==j):
                        currentPathWeight += l[1]
                        k = j

            for j in adj[k]:
                if (j[0]==V-1):
                    currentPathWeight += j[1]
                    
                # currentPathWeight += adj[k][V-1][1]
            # currentPathWeight += graph[V-1][s]

            # Chuyển đổi các tuple trong danh sách i sang list
            
            # update minimum
            if (currentPathWeight<minPath):
                minPath = currentPathWeight
                minPathSequence=[s] + list(i) + [V-1]
            
        return minPath, minPathSequence
    
    def convertPoints(self,startPoint, pickUpPoints, goalPoint):
        converted_points = {}
        converted_points[0] = startPoint
        for i, point in enumerate(pickUpPoints, start=1):
            converted_points[i] = point
        converted_points[len(pickUpPoints) + 1] = goalPoint
        return converted_points

    def findTSP(self,startPoint,goalPoint,pickUpPoint):
        graph=Graph(len(pickUpPoint)+2)
        points=self.convertPoints(startPoint,pickUpPoint,goalPoint)
        path=[]
        for key,value in points.items():
            if (key!=0 and key!=len(points)-1):
                pathToGoal,costPath,costExpanded = self.findBFS(startPoint,value)
                temp=[0,key,pathToGoal]
                path.append(temp)
                graph.addEdge(0,key,costPath)
                self.clear()
                for i in range(key+1,len(points)):
                    p=tuple(points.items())
                   
                    pathToGoal,costPath,costExpanded = self.findBFS(value,p[i][1])
                    temp=[key,i,pathToGoal,costPath]
                    path.append(temp)
                    graph.addEdge(key,i,costPath)
                    self.clear()


        minCostPath, pathSequence =self.travellingSalesmanSearch(graph,0,len(pickUpPoint)+2)
        minPath=[]
        for i in range(len(pathSequence)-1):
            for j in range(len(path)-1):
                if (path[j][1]==pathSequence[i+1] and path[j][0]==pathSequence[i]):
                    temp=path[j][2]
                    if (len(temp)==0):
                        return [],0,0
                    if (i!=0):
                        temp.pop(len(temp)-1)
                    minPath=temp +minPath
                    break

                elif (path[j][1]==pathSequence[i] and path[j][0]==pathSequence[i+1]):
                    temp=path[j][2]
                    if (len(temp)==0):
                        return [],0,0
                    start = len(temp) - 1
                    reversed_temp = [temp[i] for i in range(start, -1, -1)]
                    if (i!=0):
                        reversed_temp.pop(len(temp)-1)
                    minPath=reversed_temp +minPath
                    break

        # unique_tuples = []

        # for tup in minPath:
        #     if tup not in unique_tuples:
        #         unique_tuples.append(tup)
        return minPath,minCostPath,0



            
        


        
        
            

        