from tkinter import messagebox, Tk
import pygame
import sys

width = 512
height = 512

screen = pygame.display.set_mode((width, height))

columns = 32
rows = 32

box_width = width // columns
box_height = height // rows

grid = []
queue = []
path = []
class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, scr, color):
        pygame.draw.rect(scr, color, (self.x * box_width, self.y * box_height, box_width - 1, box_height - 1))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x -1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()


start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)

def init():

    flag = False
    target_box_set = False
    searching = True
    target_box = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_width
                    grid[i][j].wall = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 and not target_box_set:
                        i = x // box_width
                        j = y // box_width
                        target_box = grid[i][j]
                        target_box.target = True
                        target_box_set = True

            if event.type == pygame.KEYDOWN and target_box_set:
                flag = True

        if flag:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True

                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)

            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No solution")
                    searching = False



        screen.fill([0, 0, 0])

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(screen, (40, 40, 40))
                if box.queued:
                    box.draw(screen, (200,0,200))
                if box.visited:
                    box.draw(screen, (0, 200, 0))
                if box in path:
                    box.draw(screen,(0,0,200))
                if box.start:
                    box.draw(screen, (0, 200, 200))
                if box.wall:
                    box.draw(screen, (90, 90, 90))
                if box.target:
                    box.draw(screen, (200, 200, 0))

        pygame.display.flip()


init()
