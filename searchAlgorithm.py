import random
from visualization import COLOR_VISITED_POINT_IDS, Matrix,COLOR_VISITED_POINT,COLOR_FINISHED_POINT
from environment import BLOCKED,VISITED,np
from sys import maxsize
from itertools import permutations
from graph import Graph

class SearchAlgorithm:
    
    def __init__(self,graph,visual) -> None:
        self.moveset = [self.right,self.down,self.left,self.up]
        random.shuffle(self.moveset)
        self.visited = np.copy(graph)
        self.original_graph = graph
        self.frontier = []
        self.visual = Matrix(visual.leftmost_pos)
        self.visual.size = visual.size
        self.allpaths = {}

    #Breath First Search
    def findBFS(self,start_point : tuple,goal_point : tuple):
        '''
        Breath First Search
        '''

        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])

        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")
        
        if (start == goal):
            return [start],0,0

        self.visited[start] = VISITED
        self.frontier = []
        self.frontier.append((start,(-1,-1)))           #the second point is the previous of the first point
        expanded_cost = 0

        while self.frontier:
            current_move = self.frontier.pop(0)
            self.allpaths[current_move[0]] = current_move[1]
            expanded_cost += 1
            if current_move[0] != start:
                self.visual.drawSquare((current_move[0][1],current_move[0][0]),COLOR_VISITED_POINT)
            if current_move[0] == goal:
                self.visual.drawSquare((current_move[0][1],current_move[0][0]),COLOR_FINISHED_POINT)
                break

            for movefrom in self.moveset:
                posible_move = movefrom(current_move)
                if self.isvalid_move(posible_move[0]):
                    self.visited[posible_move[0]] = VISITED
                    self.frontier.append(posible_move)
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
        return result,cost,expanded_cost

    #Uniform Cost Search
    def findUCS(self,start_point : tuple,goal_point : tuple):
        '''
        Uniform Cost Search
        '''

        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")

        if (start == goal):
            return [start],0,0

        self.visited[start] = VISITED
        self.frontier = {}
        self.frontier[start] = (0,(-1,-1))
        #self.frontier.append((0,start,(-1,-1)))     #(cost to current point,current point,previous point)
        expanded_cost = 0

        while self.frontier:
            
            current_move = min(self.frontier, key=self.frontier.get)
            self.visited[current_move] = VISITED
            expanded_cost += 1
            if current_move != start:
                self.visual.drawSquare((current_move[1],current_move[0]),COLOR_VISITED_POINT)
            self.allpaths[current_move] = self.frontier[current_move]
            
            if current_move == goal:
                self.visual.drawSquare((current_move[1],current_move[0]),COLOR_FINISHED_POINT)
                break

            for movefrom in self.moveset:
                cost = 1    #cost in each step
                posible_move_newmove,posible_move_oldmove = movefrom((current_move,self.frontier[current_move][1]))  
                posible_move = (self.frontier[current_move][0] + cost,posible_move_newmove,posible_move_oldmove)   #Ex: posible_move = (12,(7,8),(7,7))
                if self.isvalid_move(posible_move[1]):
                    if not posible_move[1] in self.frontier:
                        self.frontier[posible_move[1]] = (posible_move[0],posible_move[2])
                    elif posible_move[0] < self.frontier[posible_move[1]][0]:
                        self.frontier[posible_move[1]] = (posible_move[0],posible_move[2])
            self.frontier.pop(current_move)
            random.shuffle(self.moveset)

        #self.frontier.clear()
        path = goal
        result = []
        result.append(path)
        if path in self.allpaths:
            path_cost = self.allpaths[path][0]
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
        return result,path_cost,expanded_cost
    
    #Iterative deepening Search
    def findIDS(self,start_point,goal_point,visualize = True):
        '''
        Iterative Deepening Search
        '''
        self.list_color = [COLOR_VISITED_POINT,COLOR_VISITED_POINT_IDS]
        self.INDEX = False


        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")

        if (start == goal):
            return [start],0,0

        expanded_cost = 0
        depth = 1
        MAX_DEPTH = self.visited.shape[0]*self.visited.shape[1]
        self.frontier = []

        while depth <= MAX_DEPTH:
            finish,expanded_cost = self.DLS(start,goal,depth,visualize)
            if finish: break
            self.visited = np.copy(self.original_graph)
            self.allpaths.clear()
            self.frontier.clear()
            depth *= 2
            #self.INDEX = not self.INDEX
            self.visual.pen.clear()
            expanded_cost = 0

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
            
        return result,cost,expanded_cost
        

    def DLS(self,start,goal,limit_depth,visualize):
        #self.visited[start] = VISITED
        
        self.frontier.append((start,(-1,-1)))           #the second point is the previous of the first point

        depth = -1
        reached = False
        success = False
        expanded_cost = 0
        previous_point = [self.frontier[0][1],(-2,-2)]

        while self.frontier:
            current_move = self.frontier.pop()
            if current_move[1] == previous_point[0]:
                depth += 1
                previous_point[0] = current_move[0]
                previous_point[1] = current_move[1]
            elif current_move[1] == previous_point[1]:
                pass
            else:
                depth -= 1
                previous_point[0] = current_move[0]
                previous_point[1] = current_move[1]

            self.allpaths[current_move[0]] = current_move[1]
            self.visited[current_move[0]] = VISITED
            expanded_cost += 1
            if current_move[0] == goal:
                self.visual.drawSquare((current_move[0][1],current_move[0][0]),COLOR_FINISHED_POINT)
                success = True
                break
            if visualize and current_move[0] != start:
                self.visual.drawSquare((current_move[0][1],current_move[0][0]),self.list_color[self.INDEX])
            
            for movefrom in self.moveset:
                posible_move = movefrom(current_move)
                if self.isvalid_move(posible_move[0]) and depth < limit_depth:
                    self.frontier.append(posible_move)
        
        return success,expanded_cost

    #Greedy Best First Search
    def findGBFS(self,start_point,goal_point):
        '''
        Greedy Best First Search
        '''
        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        reached = False
        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")
        
        if (start == goal):
            return [start],0,0


        self.visited[start] = VISITED
        self.frontier = []
        self.frontier.append((start,(-1,-1))) 
        expanded_cost = 0
        reached = False

        while self.frontier:
            self.frontier.sort(key= lambda move: self.heuristic(move[0],goal))
            current_move = self.frontier.pop(0)
            #current_move = min(self.frontier,key= lambda move: self.heuristic(move[0],goal))
            
            self.allpaths[current_move[0]] = current_move[1]
            if current_move[0] == goal:
                self.visual.drawSquare((current_move[0][1],current_move[0][0]),COLOR_FINISHED_POINT)
                break
            self.visited[current_move[0]] = VISITED
            expanded_cost += 1
            if current_move[0] != start:
                self.visual.drawSquare((current_move[0][1],current_move[0][0]),COLOR_VISITED_POINT)


            #self.frontier.clear()
            for movefrom in self.moveset:
                posible_move = movefrom(current_move)
                if self.isvalid_move(posible_move[0]):
                    self.frontier.append(posible_move)
            
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
            
        return result,cost,expanded_cost

    #A* Search
    def findASS(self,start_point,goal_point):
        '''
        A* Search
        '''

        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        reached = False
        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")
        
        if (start == goal):
            return [start],0,0

        self.visited[start] = VISITED
        self.frontier = {}
        self.frontier[start] = (0,(-1,-1))
        expanded_cost = 0

        while self.frontier:
            current_move = self.bestway(goal)
            self.allpaths[current_move[0]] = current_move[1]
            self.visited[current_move[0]] = VISITED
            expanded_cost += 1
            if current_move[0] != start:
                self.visual.drawSquare((current_move[0][1],current_move[0][0]),COLOR_VISITED_POINT)
            
            if current_move[0] == goal:
                self.visual.drawSquare((current_move[0][1],current_move[0][0]),COLOR_FINISHED_POINT)
                break
            
            for movefrom in self.moveset:
                cost = 1    #cost in each step
                posible_move_newmove,posible_move_oldmove = movefrom((current_move[0],current_move[1][1]))  
                posible_move = (current_move[1][0] + cost,posible_move_newmove,posible_move_oldmove)
                if self.isvalid_move(posible_move[1]):
                    if not posible_move[1] in self.frontier:
                        self.frontier[posible_move[1]] = (posible_move[0],posible_move[2])
                    else:
                        move_in_frontier = self.frontier[posible_move[1]]
                        f_cost_current = self.f((posible_move[0],posible_move[1]),goal)
                        f_cost_old = self.f((move_in_frontier[0],posible_move[1]),goal)
                        if f_cost_current < f_cost_old:
                            self.frontier[posible_move[1]] = (posible_move[0],posible_move[2])
    
            self.frontier.pop(current_move[0])
            random.shuffle(self.moveset)
                    
        path = goal
        result = []
        result.append(path)
        if(path in self.allpaths):  
            path_cost = self.allpaths[path][0]
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

        return result,path_cost,expanded_cost

    def heuristic(self,point,goal):     #the Manhattan distance
        return abs(point[0] - goal[0]) + abs(point[1] - goal[1])


    def f(self,move : tuple,goal):    
        g = move[0]
        h = self.heuristic(move[1],goal)
        print(g+h)
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
    def isvalid_move(self,point):
        return (0 <= point[0] < self.visited.shape[0]  #go out of maze
            and 0 <= point[1] < self.visited.shape[1]
            and not self.visited[point])               #obstacle or already visited

    #reset
    def clear(self):
        self.visual.pen.clear()
        self.visited = np.copy(self.original_graph)
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
        min_path = maxsize
        min_path_sequence = None
        next_permutation=permutations(vertex)
        adj=graph.graphAdj()
        for i in next_permutation:
    
            # store current Path weight(cost)
            current_pathweight = 0
    
            # compute current path weight
            k = s
            for j in i:
                temp=adj[k]
                for l in temp:
                    if (l[0]==j):
                        current_pathweight += l[1]
                        k = j

            for j in adj[k]:
                if (j[0]==V-1):
                    current_pathweight += j[1]
                    
                # current_pathweight += adj[k][V-1][1]
            # current_pathweight += graph[V-1][s]

            # Chuyển đổi các tuple trong danh sách i sang list
            
            # update minimum
            if (current_pathweight<min_path):
                min_path = current_pathweight
                min_path_sequence=[s] + list(i) + [V-1]
            
        return min_path, min_path_sequence
    
    def convert_points(self,start_point, pick_up_points, goal_point):
        converted_points = {}
        converted_points[0] = start_point
        for i, point in enumerate(pick_up_points, start=1):
            converted_points[i] = point
        converted_points[len(pick_up_points) + 1] = goal_point
        return converted_points

    def findTSP(self,startPoint,goalPoint,pickUpPoint):
        graph=Graph(len(pickUpPoint)+2)
        points=self.convert_points(startPoint,pickUpPoint,goalPoint)
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



            
        


        
        
            

        