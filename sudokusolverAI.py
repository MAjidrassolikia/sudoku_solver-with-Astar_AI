import time

start_time = time.perf_counter()

N = 9
class SudokuNode:
    def __init__(self, puzzle, cost):
        self.puzzle = puzzle
        self.cost = cost 
        self.heuristic = self.calculate_heuristic() 
        self.f = self.cost + self.heuristic

    def calculate_heuristic(self):
        min_options = N + 1 
        # zeros = -1
        for i in range(N):
            for j in range(N):
                if self.puzzle[i][j] == 0:  
                    options = 0
                    # zeros += 1
                    for num in range(1, N+1):  
                        if self.is_valid_number(i, j, num): 
                            options += 1
                        min_options = min(min_options, options)
                
        # print("zeros is:" , zeros ,"\n")
        return min_options 
        # return zeros
    
    def is_goal_state(self):
        for row in self.puzzle:
            if 0 in row:
                return False
        return True
        # return self.heuristic == 0
    
    def is_valid_number(self, row, col, num):
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        
        return (
            num not in self.puzzle[row] and
            num not in [self.puzzle[i][col] for i in range(9)] and
            num not in [self.puzzle[start_row + i][start_col + j] for i in range(3) for j in range(3)]
        )
    
    def expand(self):
        successors = []
        
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid_number(i, j, num):
                            successor = SudokuNode([row[:] for row in self.puzzle], self.cost + 1) # Increase the cost by one
                            successor.puzzle[i][j] = num
                            successors.append(successor)
                    
                    
                    return successors
 


def A_star(puzzle):
    
    start_node = SudokuNode(puzzle, 0) 
    fringe_list = [start_node]
    open_list = []
    while fringe_list:
        
        fringe_list.sort(key=lambda node: node.f)
        current_node = fringe_list.pop(0)
        open_list.append(current_node)
        
        if current_node.is_goal_state():
            return current_node.puzzle
        
        successors = current_node.expand()
        for successor in successors:
            if successor not in fringe_list and successor and open_list:
                fringe_list.append(successor)
        # print(current_node.f , current_node.heuristic , current_node.cost)
    
    return None

def read_sudoku_file(file_path):
    sudoku = []
    with open(file_path, 'r') as file:
        for line in file:
            row = [int(num) for num in line.strip().split(',')]
            sudoku.append(row)
    return sudoku

def write_sudoku_file(file_path, sudoku):
    with open(file_path, 'w') as file:
        for row in sudoku:
            line = ','.join(str(num) for num in row)
            file.write(line + '\n')

sudoku = read_sudoku_file('input.txt')
solution = A_star(sudoku)
write_sudoku_file('output.txt', solution)

print("success")
end_time = time.perf_counter()
print(f"done in {end_time - start_time}")
