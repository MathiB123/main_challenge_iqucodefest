from IPython.display import clear_output
from math import ceil
import os

class Renderer:

    TEXT_LINES = 2 
    CELL_HEIGHT = 6
    CELL_WIDTH = 8
    NUM_CELL_PER_ROW = 5
    MIN_NB_CHAR = NUM_CELL_PER_ROW * (CELL_WIDTH + 1)

    def __init__(self, num_cells: int):
        self.num_cells = num_cells
        self.nb_lines = int(ceil((self.num_cells /Renderer.NUM_CELL_PER_ROW)))  * Renderer.CELL_HEIGHT + Renderer.TEXT_LINES
        self.char_matrix =[[] for _ in range(self.nb_lines)]
        self.char_matrix[0] = ["\n"]
        self.char_matrix[1] = ["\n"]
        self.clear_render()

    def clear_text(self):
        self.char_matrix[0] = ["\n"]

    def clear_tempo_text(self):
        self.char_matrix[1] = ["\n"]

    def clear_map(self):
        for i in range(2, self.nb_lines):
            self.char_matrix[i] = [" " for _ in range(Renderer.MIN_NB_CHAR)]
        self.draw_map()

    def clear_render(self):
        self.clear_text()
        self.clear_tempo_text()
        self.clear_map()
    
    def add_text(self, text:str):
        line = self.char_matrix[0]
        if line == ["\n"]:
            self.char_matrix[0] = []
            line = self.char_matrix[0]

        for char in text:
            line.append(char)
        line.append("\n")

    def add_tempo_text(self, text:str):
        line = self.char_matrix[1]
        if line == ["\n"]:
            self.char_matrix[1] = []
            line = self.char_matrix[1]

        for char in text:
            line.append(char)

        line.append("\n")
            

    def draw_map(self):
        """
        Draws this per cell
        ________
        |      |
        |      |
        |      |
        |______|

        """
        for i in range(self.num_cells):
            start_x = (i % Renderer.NUM_CELL_PER_ROW) * (Renderer.CELL_WIDTH + 1)
            start_y = i // Renderer.NUM_CELL_PER_ROW * Renderer.CELL_HEIGHT
            for j in range(Renderer.CELL_HEIGHT):
                curr_y = start_y + j + 2 
                line = self.char_matrix[curr_y]
                for k in range(Renderer.CELL_WIDTH + 1):
                    curr_x = start_x + k

                    if k == Renderer.CELL_WIDTH:
                        line[curr_x] = " "
                    elif j == 0:
                        line[curr_x] = "_"
                    elif k == 0 or k == Renderer.CELL_WIDTH - 1:
                        line[curr_x] = "|"
                    elif j == Renderer.CELL_HEIGHT - 1:
                        line[curr_x] = "_"

        for i in range(2, self.nb_lines):
            line = self.char_matrix[i]
            line[len(line) - 1] = "\n"
    
    def draw_groundhog(self, cell_num : int, player_num : int):
        start_x = (cell_num % Renderer.NUM_CELL_PER_ROW) * (Renderer.CELL_WIDTH + 1)
        start_y = cell_num // Renderer.NUM_CELL_PER_ROW * Renderer.CELL_HEIGHT + 2
        
        """
        Draws this
        ^_____
        |  o /
        |   / 
        |___|n  
        """

        if self.char_matrix[start_y + 4][start_x +6] != " ":
            self.char_matrix[start_y + 4][start_x +6] = "n"
            return
        
        self.char_matrix[start_y + 1][start_x + 1] = "^"
        self.char_matrix[start_y + 1][start_x +2] = "_"
        self.char_matrix[start_y + 1][start_x +3] = "_"
        self.char_matrix[start_y + 1][start_x +4] = "_"
        self.char_matrix[start_y + 1][start_x +5] = "_"
        self.char_matrix[start_y + 1][start_x +6] = "_"

        self.char_matrix[start_y + 2][start_x +1] = "|"
        self.char_matrix[start_y + 2][start_x +4] = "o"
        self.char_matrix[start_y + 2][start_x +6] = "/"

        self.char_matrix[start_y + 3][start_x +1] = "|"
        self.char_matrix[start_y + 3][start_x +5] = "/"

        self.char_matrix[start_y + 4][start_x +1] = "|"
        self.char_matrix[start_y + 4][start_x +2] = "_"
        self.char_matrix[start_y + 4][start_x +3] = "_"
        self.char_matrix[start_y + 4][start_x +4] = "_"
        self.char_matrix[start_y + 4][start_x +5] = "|"
        self.char_matrix[start_y + 4][start_x +6] = str(player_num)

    
    def clear_any_output(self):
        clear_output(wait= True)

        # Check if the operating system is Windows ('nt') or Unix-like ('posix')
        if os.name == 'nt':
            os.system('cls')  # Command for Windows
        else:
            os.system('clear') # Command for Linux/macOS

    def render(self):
        self.clear_any_output()
        result = ""

        for i in range (self.nb_lines):
            line = self.char_matrix[i]
            for char in line:
                result += char
        
        print(result)
                