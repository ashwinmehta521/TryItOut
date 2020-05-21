import numpy as np
#import re
#import platform
#import argparse as ap

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.h = 0
        self.g = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
#path function
def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # Return reversed path as we need to show from start to end path
    path = path[::-1]
    return path

def generateString(problemSize1,path):
    solution=''
    pathtest = path.copy()
    path1 = path.copy()
    mapSize=np.copy(problemSize1)
    mapSize1=np.copy(problemSize1)
    positionDict = {(-1,  0):'U', # U
                    ( 0, -1):'L', # go l
                    ( 1,  0):'D', # go D
                    ( 0,  1):'R', #go R
                    ( 1,  1):'RD', #go RD
                    ( 1, -1):'LD', #go LD
                    (-1,  1):'RU', #go RU
                    (-1, -1):'LU'} #go LU
    
    costDict = {(-1,  0):2, # U
                ( 0, -1):2, # go l
                ( 1,  0):2, # go D
                ( 0,  1):2, #go R
                ( 1,  1):1, #go RD
                ( 1, -1):1, #go LD
                (-1,  1):1, #go RU
                (-1, -1):1} #go LU
    pathtest.pop(0)
    pathtest.pop(len(pathtest)-1)
    cost=0
    totCost = 0
    cumDirc = ''
    for idx, pth in enumerate(path1):
#        print('Now :', pth)
        if pth in pathtest :
            mapSize[pth[0]][pth[1]]='*'
        ft1='\n'.join(''.join('%s' %a for a in line) for line in mapSize)
        solution = solution + ft1
        solution = solution + '\n'
        solution = solution + '\n'
        
        
        if idx==0:
            cost = 0
            dirc = 'S'
            cumDirc = cumDirc + dirc

        else:
            lookUpAt = tuple(np.subtract(path1[idx], path1[idx-1]))
            cost = costDict[lookUpAt]
            totCost = totCost + cost
            
            dirc = positionDict[lookUpAt]
            cumDirc = cumDirc + '-' + dirc
        
        if idx == len(path1)-1:
            cumDirc=cumDirc+'-' + 'G'
        
        solution = solution + cumDirc + '   ' + np.str(totCost)
        
        solution = solution + '\n'
        solution = solution + '\n'

        mapSize = np.copy(mapSize1)
        
    return solution   

def write_to_file(file_name, solution):

    file_handle = open(file_name, 'w')

    file_handle.write(solution) 
    
def main():     
    #
    flag = 0
    solution=''    
    file_handle = open("input2.txt")
    
    fileContent = file_handle.readlines()
    #
    #print(map)
    for idx, line in enumerate(fileContent):
        if idx == 0:
            squareMatrixSize = np.int(line)
            problemSize = np.array(np.zeros([squareMatrixSize, squareMatrixSize]), dtype='<U1')
        else:
            for i in range(0, squareMatrixSize):
    #            print("idx",idx-1)
    #            print("i:", i)
    #            print(line)
    #            print(list(fileContent[idx][i]))
                problemSize[idx-1, i] = line[i]
    #print(problemSize)
    
    out = np.where(problemSize == 'S')
    ans=(zip(out[0],out[1]))
    start = sum(ans, ())
    #print(start)
    check = np.where(problemSize == 'G')
    val=(zip(check[0],check[1]))
    end = (sum(val, ()))
    #print(end)
    ############
    a=np.array(start)
    b=np.array(end)
    start_h = np.floor(np.sqrt(np.linalg.norm(a-b)))
    #############
    #print(start_h)
    startNode = Node(None,start)
    startNode.h = start_h
    #print(startNode.h)
    a=np.array(end)
    b=np.array(end)
    end_h = np.floor(np.sqrt(np.linalg.norm(a-b)))
    endNode = Node(None,end)
    endNode.h = end_h
    
    forx = np.where(problemSize == 'X')
    va=list(zip(forx[0],forx[1]))
    #print(va)
    
    #print(endNode.h)
    #open
    yetToVisitList=[]
    #closed
    visitedList=[]    
    yetToVisitList.append(startNode)
    #Bakchodi
    #outer_iterations = 0
    #max_iterations = (len(problemSize) // 2) ** 10
    #Continue kar
    move  =  [[-1, 0], # U
                  [0, -1], # go l
                  [1, 0], # go D
                  [0, 1], #go R
                  [1, 1], #go RD
                  [1,-1], #go LD
                  [-1,1], #go RU
                  [-1,-1]] #go LU
    move1 = [[-1, 0], # U
                  [0, -1], # go l
                  [1, 0], # go D
                  [0, 1]] #go R
    noRows, noColumns = np.shape(problemSize)
    visitedPositions=[]
    #print(len(yetToVisitList))
    diagonalMove=[(-1,1),(1,1),(-1,-1),(1,-1)]
    while len(yetToVisitList) > 0:
            
            # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
    #        outer_iterations += 1    
            tieBreaker=[]
            yetToVisitList.sort(key=lambda x: x.f)
            
            for i in yetToVisitList:
                if yetToVisitList[0].f == i.f:
                    tieBreaker.append(i)
                    
            tieBreaker.sort(key=lambda x: x.h)
            if len(tieBreaker) == 0:
                tieBreaker.append(yetToVisitList[0])
            # Get the current node
            current_node = tieBreaker[0]
            current_index = 0
            yetToVisitList.pop(current_index)
            visitedList.append(current_node)
            visitedPositions.append(current_node.position)
     #       print(visitedPositions)   
            if current_node == endNode:
                path = return_path(current_node)
    #            print(current_node.g)
    #            print(path)
                solution = generateString(problemSize,path)
                #print(solution)
                ans = 1
                print(solution)
                break
            #Generate children
            children=[]
            #restrict diagonal movement incase of x besides
            restrict=[]
            for n_position in move1:
                check_position = (current_node.position[0] + n_position[0], current_node.position[1] + n_position[1])
                if (check_position[0] > (noRows - 1) or 
                    check_position[0] < 0 or 
                    check_position[1] > (noColumns -1) or 
                    check_position[1] < 0):
                    continue
                if problemSize[check_position[0]][check_position[1]]=='X':
                    #based on the position of mountain we decide the deiagonal movement
                    if check_position[0] == current_node.position[0]:
                        #upward
                        r_pos1 = (check_position[0] - 1, check_position[1] + 0)
                        #downward
                        r_pos2 = (check_position[0] + 1, check_position[1] + 0)
                        restrict.append(r_pos1)
                        restrict.append(r_pos2)
                    if check_position[1] == current_node.position[1]:
                        #right
                        r_pos3 = (check_position[0] + 0, check_position[1] + 1)
                        #left
                        r_pos4 = (check_position[0] + 0, check_position[1] - 1)
                        restrict.append(r_pos3)
                        restrict.append(r_pos4)                   
    #        print(restrict)    
            for new_position in move: 
    
                # Get node position
                
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
               
                # Make sure within range (check if within maze boundary)
                if (node_position[0] > (noRows - 1) or 
                    node_position[0] < 0 or 
                    node_position[1] > (noColumns -1) or 
                    node_position[1] < 0):
                    continue
    
                # Make sure not a mountain
                if node_position in va:
                    continue
                
                if node_position in restrict:
                    continue
                
                if node_position in visitedPositions:
                    continue
                
                #print(node_position)
                # Create new node#
                new_node = Node(current_node, node_position)
    
                # Append
                children.append(new_node)
                
            for child in children:
                # Child is on the visited list (search entire visited list)
                #if len([visited_child for visited_child in visitedList if visited_child == child]) > 0:
                    #continue
    #           #new added    
                p1 = current_node.position
                p2 = child.position
                if tuple(np.subtract(p2,p1)) in diagonalMove:
                    child.g = current_node.g + 1
                else:
                    child.g = current_node.g + 2
                #new added end    
                # Create the f, g, and h values
                #child.g = current_node.g + cost
                ## Heuristic costs calculated here, this is using eucledian distance
                a=np.array(child.position)
                b=np.array(endNode.position)
                child.h = np.floor(np.sqrt(np.linalg.norm(a-b)))
                child.f = child.g + child.h
    
                for checkChild in yetToVisitList:
                    if checkChild == child and child. f < checkChild.f:
                        checkChild.g=child.g
                        checkChild.parent=child.parent
                        checkChild.f=checkChild.g+checkChild.h
                        continue
                    if checkChild == child and child.g > checkChild.g:
                        continue
                        
                # Child is already in the yet_to_visit list and g cost is already lower
    #            if len([i for i in yetToVisitList if child == i) > 0:
    #                continue
    
                # Add the child to the yet_to_visit list
                yetToVisitList.append(child)
            if flag >= 1:
                print('Node ' + str(current_node.position))
                print('g:' + str(current_node.g) + ' h:' + str(current_node.h) + ' f:' +  str(current_node.f))
                print('\n')
                for i in children:
                    print('Parent ' + str(i.parent.position))
                    print('Child '+ str(i.position))
                    print('g:' + str(i.g) + ' h:' + str(i.h) + ' f:' +  str(i.f))
                    print('\n')                
                    yvp=[]
                    vp=[]
                for j in yetToVisitList:
                    yvp.append(j.position)
                print('Open Positions: ' + str(yvp) )
                for k in visitedList:
                    vp.append(k.position)
                print('Closed Positions: ' + str(vp) ) 
                flag=flag-1
                
                
    if ans==0:
        solution='No path found'
        write_to_file(output_file_name,solution)           
if __name__ == "__main__":

    main()
    
