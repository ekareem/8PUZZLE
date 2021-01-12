from copy import deepcopy
from ASTAR import ASTAR
from BFS import BFS 
from Board import Board 

goal = 0
path = 3

def main():
    board = Board()
    a = ASTAR(board)
    b = BFS(board)
    for i in range(3):
        print("________________________________trial_",i+1,"_______________________________")
        print("initial state:")
        board.scramble()
        board.print()
        
        
        print("astar solution:")
        temp = a.search(board)
        board.path(temp)[goal]._board.print()
        print(board.path(temp)[path])
        print()
        
        print("bfs solution:")
        temp = a.search(board)
        board.path(temp)[goal]._board.print()
        print(board.path(temp)[path])
        print()
        
        
        
        

if __name__ == "__main__":
    main()