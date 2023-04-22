

board = [[0 for i in range(9)] for j in range(9)]

def isvalid(bo, num, pos) : 

    for i in range(len(bo[0])): #every column in rows
	
        if bo[pos[0]][i] == num and pos[1] != i: 
            return False
        
    for i in range(len(bo)): #every row in column
        if bo[i][pos[1]] == num and pos[0] != i: 
            return False
   
    box_x = pos[1] // 3   #column
    box_y = pos[0] // 3   #row

    
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False 

    return True

def solve(bo):
    find = find_empty(bo)
    if not find: 
        return True 
    else:
        row, col = find
    
    for i in range(1,10): 
        if isvalid(bo, i, (row, col)): 
            bo[row][col] = i 

            if solve(bo): 
                return True

            bo[row][col] = 0 

    return False


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])): 
            if bo[i][j] == 0:
                return (i, j) 
    
    return None 


solve(board)
