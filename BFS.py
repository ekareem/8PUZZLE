from copy import deepcopy
from Board import Board

up = [-1,0]
down = [1,0]
left = [0,-1]
right = [0,1]

class BNode:
    def __init__(self,board,parent = None):
        #Breath first search node
        self._board = board
        self._parent = parent
        self._children = []
        
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
        param[out]  list : BNode
        '''
        if (len(self._children) != 0):
            return
            
        if str(self) in close:
            return
  
        possible_move = self._board.possible_move()
        child = Board()
        
        for move in possible_move:
            if(move == up): child = deepcopy(self._board.up(child))
            if(move == down): child = deepcopy(self._board.down(child))
            if(move == left): child =  deepcopy(self._board.left(child))
            if(move == right):  child = deepcopy(self._board.right(child))
        
            if (self.is_closed(child,close) == False):    
                self._children.append(deepcopy(BNode(child,self)))
                
        
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
        
        
    def __eq__(self, other):
        '''
        putpose: checks if two BNode are equal
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
        self._board.print()
            
    def __str__(self):
        return str(self._board)
        
class BFS:
    def __init__(self,board):
        self._board = board
        self._root = BNode(board)
        self._open = []
        '''
        closed list is a dictiionary where the key is the grid[][] state 
        this make cheking if a Board is closd constant time
        '''
        self._close = {}
        
    def search(self,board = None):
        '''
        purpose: search for solution
        param[out] BNode
        '''
        
        if board is not None:
            _board = board 
        
        
        self._root = BNode(self._board)
        self._open = []
        self._close = {}
        self._open.append(self._root)

        while(True):
            if (len(self._open) == 0):
                return None
            
            curr = self._open[0]
            curr.create_children(self._close)
            
            for i in curr._children:
                self._open.append(i)

            if (curr.is_goal()):
                return curr

            self._open.remove(curr)
            self._close[str(curr)] = [curr]
            