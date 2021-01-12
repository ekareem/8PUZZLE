from copy import deepcopy
import random
#from BNode import 
import os
try:
    from BFS import BFS
    from ASTAR import ASTAR
except ImportError:
    pass
    
up = [-1,0]
down = [1,0]
left = [0,-1]
right = [0,1]

class Board:
    #purpose: creates the board and its properties
    def __init__(self,width = 3):
        self._width = width
        self._grid_size =  self._width *  self._width
        self._grid = self.goal()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    purpose: moves the free space
    param[in]: doesnt change self but board
    pram[out]: return self
    '''
    def up(self, board = None):
        if (board is None):
            free_1d = self.free_index()
            free_2d = self.one_2_two(free_1d)
            if (free_2d[0] <= 0):
                return None
                
            coordinate = [free_2d[0] + up[0] ,free_2d[1] + up[1]]
            adj = self.two_2_one(coordinate)
            self._grid[free_1d], self._grid[adj] = self._grid[adj], self._grid[free_1d]
        
            return self
        if (board is not None):
            board = deepcopy(self)
            return board.up()
        

    def down(self, board = None):
        if (board is None):
            free_1d = self.free_index()
            free_2d = self.one_2_two(free_1d)
            if (free_2d[0] >= self._width-1):
                return None
                
            coordinate = [free_2d[0] + down[0] ,free_2d[1] + down[1]]
            adj = self.two_2_one(coordinate)
            self._grid[free_1d], self._grid[adj] = self._grid[adj], self._grid[free_1d]
            
            return self
        if (board is not None):
            board = deepcopy(self)
            return board.down()
        
    def left(self, board = None):
        if (board is None): 
            free_1d = self.free_index()
            free_2d = self.one_2_two(free_1d)
            if (free_2d[1] <= 0):
                return None
                
            coordinate = [free_2d[0] + left[0] ,free_2d[1] + left[1]]
            adj = self.two_2_one(coordinate)
            self._grid[free_1d], self._grid[adj] = self._grid[adj], self._grid[free_1d]
       
            return self
        if (board is not None):
            board = deepcopy(self)
            return board.left()
        
    def right(self, board = None):
        if (board is None):
            free_1d = self.free_index()
            free_2d = self.one_2_two(free_1d)
            if (free_2d[1] >= self._width-1):
                return None
                
            coordinate = [free_2d[0] + right[0] ,free_2d[1] + right[1]]
            adj = self.two_2_one(coordinate)
            self._grid[free_1d], self._grid[adj] = self._grid[adj], self._grid[free_1d]
        
            return self
        if (board is not None):
            board = deepcopy(self)
            return board.right()
   
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        
    def path(self,goal):
        '''
        purpose: describes the steps to solve the puzzle
        param[out]  BNode
        param[out]  Board
        param[out]  list : list : int
        param[out]  list : string
        '''
        board = goal._board
        path = goal.path()
        path_str = []
        
        path_str.append("INITAL")
        
        for i in path:
            if i == up : path_str.append("UP")
            if i == down : path_str.append("DOWN")
            if i == left : path_str.append("LEFT")
            if i == right : path_str.append("RIGHT")
        
        
        path_str.append("GOAL")
        return [goal,board,path,path_str]
        

       
        
    def control(self,move):
        '''
        purpose: possible controls
        '''
        if (move == "w/"): self.up()
            
        elif (move == "s/"): self.down()
            
        elif (move == "a/"): self.left()
                
        elif (move == "d/"): self.right()
        
        elif (move == "shuffle" or move == "0"): self.scramble()
        
        elif (move == "reset" or move == "1"): 
            self.reset()
            return 1
        
        elif (move == "bfs" or move == "2"): self.search_bfs()
        
        elif (move == "astar" or move == "3"): self.search_astar()
        
        elif (move == "help" or move == "6"):
            print("[0] shuffle  [shuffles puzzle]")
            print("[1] reset    [reset puzzle back to goal state")
            print("[2] bfs      [solves puzzle using breath first search algorithm]")
            print("[3] astar    [solves puzzle using astar algorithm]")
            print("[4] exit     [ends program]")
            print("[5] clear    [clears console]")
            print("[6] help     [list of command]\n")
            
        elif(move == "clear"or move == "5"):
            try:
                os.system("clear")
            except:
                os.system("cls")
                
        else:
            return 1
                
    def possible_move(self):
        '''
        purpose: returns a list of possible move that can be made
        param[out]  list : list
        '''
        
        free_2d = self.one_2_two(self.free_index())
        move = []
        
        up_ = [ free_2d[0] + up[0], free_2d[1] + up[1] ]
        if (self.valid(up_)): move.append(up)
        
        down_ = [ free_2d[0] + down[0], free_2d[1] + down[1] ]
        if (self.valid(down_)): move.append(down)
        
        left_ = [ free_2d[0] + left[0], free_2d[1] + left[1] ]
        if (self.valid(left_)): move.append(left)

        down_ = [ free_2d[0] + right[0], free_2d[1] + right[1] ]
        if (self.valid(down_)): move.append(right)          

        return move
    
    def move_made(self,grid):
        '''
        purpose: move_mode to get from self to grid
        param[out] list : int
        '''
        
        self_free_2d = self.one_2_two(self.free_index())
        grid_free_2d = grid.one_2_two(grid.free_index())
        
        row = self_free_2d[0] - grid_free_2d[0]
        col = self_free_2d[1] - grid_free_2d[1]
        move = [row,col]
        
        return self.opposite(deepcopy(move))
        
    
    def one_2_two(self,index):
        '''
        purpose: transfer one demetional indexing to two dimesional indexing
        param[in] int index to be transfer
        param[out] row 
        param[out] col
        '''
        if (index< 0 or index >=self._grid_size):
            return [-1,-1]
            
        row = int(index/self._width)
        col = index % self._width
        
        return [row,col]
            
    def two_2_one(self,coordinate):
        '''
        purpose: transfer two demetional indexing to one dimesional indexing
        param[in] int row
        param[in] int col
        param[out] index
        '''
        row = coordinate[0]
        col = coordinate[1]
        
        if (row < 0 or row >= self._width):
            return -1
        if (col < 0 or col >= self._width):
            return -1
            
        return row * self._width + col
    
    def goal(self):
        '''
        purpose: creats a goal state
        '''
        grid = []
        for index in range(self._grid_size):
            grid.append((index + 1) % self._grid_size)
        
        return grid
        
    def reset(self):
        '''
        purpose: resets board back to goal state
        '''
        self._grid = self.goal()
        
    def scramble(self):
        '''
        purpose: scrambles board
        '''
        self.reset()
        #number of moves to be made is _width^2
        iteration = self._width * self._width
        first = iteration
        prev = None
        
        while(iteration != 0):
            possible_move = self.possible_move()
            if(iteration != first):
                possible_move.remove(prev)
            move = random.choice(possible_move)
            
            if(move == up):
                self.up()
                prev = self.opposite(deepcopy(move))
            elif(move == down):
                self.down()
                prev = self.opposite(deepcopy(move))
            elif(move == left):
                self.left()
                prev = self.opposite(deepcopy(move))
            elif(move == right):
                self.right()
                prev = self.opposite(deepcopy(move))
            iteration -= 1
            
    
    def free_index(self):
        '''
        purpose: get 0 index position which represents free space
        param[out] int index
        '''
        for i in range(len(self._grid)):
            if (self._grid[i] == 0):
                return i
                
        return -1
        
    def valid(self,coordinate):
        '''
        purpose: checks if coordinate is valid
        param[out] bool  
        '''
        row = coordinate[0]
        col = coordinate[1]
        
        if(row < 0 or row >= self._width):
            return False
        if(col < 0 or col >= self._width):
            return False
        
        return True
        
    def opposite(self,coordinate):
        '''
        purpose: finds the opposite of a direction
        param[out]  list : int
        '''
        coordinate[0] *= -1
        coordinate[1] *= -1
        
        return coordinate
        
    def misplaced(self):
        '''
        purpose: finds number of misplaced tiles
        '''
        count = 0
        for index in range(self._grid_size):
            if (self._grid[index] != (index + 1) % self._grid_size):
                count += 1
        
        if count == 0: count = 1
        return count - 1
                
    def at(self,row,col=None):
        '''
        purpose: return stat at _grid[at]
        param[in] int
        param[out] int
        '''
        if col is None:
            if (row < 0 or row >=self._grid_size):
                return -1
            return self._grid[row]
        
        if col is not None:
            if (row < 0 or row >= self._width):
                return -1
            if (col < 0 or col >= self._width):
                return -1
                
            return self._grid[self._width * row + col]
            
    def is_goal(self):
        '''
        purpose checks if board is goal
        param[out]  bool
        '''
        return self == Board(self._width)
            
    def __eq__(self, other):
        '''
        purpose overload = operator
        param[out] bool
        '''
        return self._grid == other._grid
        
    def print(self):
        '''
        Purpose : prints the board and its state to console return prints at string
        param[out]: string
        '''
        grid = ""
        for i in range(self._grid_size):
            num  = str(self._grid[i])
            
            if num == "0":
                num = " "
            grid += "[" + num + "]"
            
            if ( i % self._width == self._width - 1 ):
                grid += "\n"
                
        print(grid)
        
        return grid
        
    def __str__(self):
        '''
        purpose : str overload
        '''
        grid = str(self._grid)   
        
        return grid

if __name__ == "__main__":
    
    print("[0] shuffle  [shuffles puzzle]")
    print("[1] reset    [reset puzzle back to goal state")
    print("[2] bfs      [solves puzzle using breath first search algorithm]")
    print("[3] astar    [solves puzzle using astar algorithm]")
    print("[4] exit     [ends program]")
    print("[5] clear    [clears console]")
    print("[6] help     [list of commands]\n")
    
    b = Board()
    b.scramble()
    c = ""
    r = None
    
    while(c != "exit" and c != "4"):
        print("current board state:")
        if r is None:
            b.scramble()
        b.print()
        c = input().lower()
        r = b.control(c)
        