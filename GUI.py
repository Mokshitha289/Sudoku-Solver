import pygame
from solver import solve, isvalid 
import time
pygame.font.init()


class Grid: 
    board = [[0 for i in range(9)] for j in range(9)]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        
        self.selected = None 
		

    def update_model(self): 
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val): 
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if isvalid(self.model, val, (row,col)) and solve(self.model): 
                return True
            self.cubes[row][col].set(0)
            self.cubes[row][col].set_temp(0)
            self.update_model()
            return False

    def temp(self, val): 
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    
    def draw(self, window):
        
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 3 
            else:
                thick = 1 
            pygame.draw.line(window, (0,0,0), (0, i*gap), (self.width, i*gap), thick) 
            pygame.draw.line(window, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick) 

        
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(window) 

    def select(self, row, col):  
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False 

        self.cubes[row][col].selected = True 
        self.selected = (row, col)

    def clear(self): 
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)
		

    def click(self, pos): 
        
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube: 
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height): 
        self.value = value 
        self.temp = 0  
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, window): 
        fnt = pygame.font.SysFont("comicsans", 30)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0: 
            text = fnt.render(str(self.temp), 1, (128,138,135)) #coldgrey
            window.blit(text, (x+2, y+1)) 
        elif self.value != 0:
            text = fnt.render(str(self.value), 1, (255,127,80)) #coral
            window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(window, (205,170,125), (x,y, gap ,gap),3) #burlywood3

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(window, board, time, strikes):
    window.fill((180,238,180)) #darkseagreen2
    
   
    fnt = pygame.font.SysFont("calibri", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0)) #black
    window.blit(text, (400, 530))
   
    text = fnt.render("X " * strikes, 1, (128,0,0)) #maroon
    window.blit(text, (50, 530))
	
	
    board.draw(window) 



def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    return " " + str(minute) + ":" + str(sec)


def main():   
    window = pygame.display.set_mode((650,620))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 530, 530)
    
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                   

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.temp(key)

        redraw_window(window, board, play_time, strikes)
        pygame.display.update()


main()
