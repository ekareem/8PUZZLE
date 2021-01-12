from copy import deepcopy
from Board import Board
import heapq

up = [-1,0]
down = [1,0]
left = [0,-1]
right = [0,1]

class ANode:
    def __init__(self,board,parent = None):
        self._board = board
        self._parent = parent
        self._children = []
        
        '''
        _g number of moved made from initial state
        _h numver of misplaced tiles
        _f _g + _h
        '''
        self._g = 0
        self._h = 0
        self._f = 0
        self.set_cost()
        
    def set_cost(self):
        '''
        purpose: set _g,_h and _f
        '''
        if self._parent != None : 
            self._g = self._parent._g + 1    
        self._h = self._board.misplaced()
        self._f = self._g + self._h
        
    def is_closed(self,node,close):
        '''
        purpose: checks if node is in closed list
        param[out] bool
        '''
        str_node = str(node)
        if str_node in close:
            return True
            
        return False
        
    def create_children(self,close):
        '''
        purpose: creates adjacent node
        param[out]  list : ANode
        '''
        if (len(self._children) != 0):
            return
            
        if str(self) in close:
            return
  
        possible_move = self._board.possible_move()
        child = Board()
        
        #print(possible_move)
        for move in possible_move:
            if(move == up):
               child = deepcopy(self._board.up(child))
            if(move == down):
               child = deepcopy(self._board.down(child))
            if(move == left):
               child =  deepcopy(self._board.left(child))
            if(move == right):
                child = deepcopy(self._board.right(child))
        
            if (self.is_closed(child,close) == False):
                #child._parent = self
                
                self._children.append(deepcopy(ANode(child,self)))
                
        
        return self._children
        
        

    def move_made(self):
        '''
        purpose: gets move made to get form _parent to self
        param[out] list : int
        '''
        if (self._parent is not None):
            return self._parent._board.move_made(self._board)
            
    def is_goal(self):
        '''
        purpose: checks if node is goal
        param[out] bool
        '''
        return self._board.is_goal()
        
    def path (self):
        '''
        purpose: creates path for solving puzzle
        param[out]  list : list : int
        '''
        path = []
        node = self
        while(node is not None):
            move = node.move_made()
            if (move is not None):
                path[0:0] = [node.move_made()]
            node = node._parent
            
        return path
        
    def __lt__(self,other):
        '''
        purpose: checks if self is less then other Anode
        param[in]   Anode
        param[out]  bool
        '''
        if self._f == other._f:
            if self._h == other._h:
                return self._g < other._g
            return self._h < other._h
            
        return self._f < other._f
            
        
    def __eq__(self, other):
        '''
        putpose: checks if two ANode are equal
        param[out] bool
        '''
        if other == None:
            return False
        return self._board == other._board
    
    def print(self):
        '''
        if (self._parent is not None):
            print("parent: ")
            self._parent._board.print()
            print("move: ",self._board.move_made(self._parent._board))
            
        '''
        
        print("self: ")
        print("g: ",self._g)
        print("h: ",self._h)
        print("f: ",self._f)
        self._board.print()
            
    def __str__(self):
        return str(self._board)  
        
class ASTAR:
    def __init__(self,board):
        self._board = board
        self._root = ANode(board)
        '''
        open list is a heap / priority queue where the the lower the f cost the higher the priority
        this makes finding the Board state with lowest f cost constant time
        '''
        self._open = []
        self._close = {}
        
    def search(self,board = None):
        '''
        purpose: search for solution
        param[out] BNode
        '''
        
        if board is not None:
            self._board = board

        self._root = ANode(self._board)
        self._open = []
        self._close = {}
        self._open.append(self._root)

        while(True):
            if (len(self._open) == 0):
                return None
            
            #get the Anode with loest f which is always at position 0
            curr = self._open[0]
            curr.create_children(self._close)
            
            for i in curr._children:
                heapq.heappush(self._open,i)

            if (curr.is_goal()):
                return curr

            self._open.remove(curr)
            self._close[str(curr)] = [curr]
                