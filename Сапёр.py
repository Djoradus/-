import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры окна и игры
width, height = 600, 600
grid_size = 10
num_mines = 10
cell_size = width // grid_size

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (192, 192, 192)

# Создание окна
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Сапёр')

# Сетка и мины
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
mines = []
revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]
flags = [[False for _ in range(grid_size)] for _ in range(grid_size)]
game_over = False

def place_mines():
    global mines, grid, revealed, flags, game_over
    mines = []
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    flags = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    game_over = False
    for _ in range(num_mines):
        x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        while (x, y) in mines:
            x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        mines.append((x, y))
        grid[x][y] = -1
    
    # Расчет чисел вокруг мин
    for mx, my in mines:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= mx+i < grid_size and 0 <= my+j < grid_size and grid[mx+i][my+j] != -1:
                    grid[mx+i][my+j] += 1

def draw_grid():
    for x in range(grid_size):
        for y in range(grid_size):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if revealed[x][y]:
                if grid[x][y] == -1:
                    pygame.draw.rect(window, red, rect)
                else:
                    pygame.draw.rect(window, grey, rect)
                    if grid[x][y] > 0:
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(grid[x][y]), True, black)
                        window.blit(text, rect.move(15, 10))
            else:
                pygame.draw.rect(window, white, rect)
                if flags[x][y]:
                    pygame.draw.circle(window, green, rect.center, 10)
            pygame.draw.rect(window, black, rect, 1)

def reveal_cell(x, y):
    if revealed[x][y] or flags[x][y]:
        return
    revealed[x][y] = True
    if grid[x][y] == -1:
        global game_over
        game_over = True
        return
    if grid[x][y] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x+i < grid_size and 0 <= y+j < grid_size:
                    reveal_cell(x+i, y+j)

def toggle_flag(x, y):
    if revealed[x][y]:
        return
    flags[x][y] = not flags[x][y]

def game_over_screen():
    window.fill(black)
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over', True, red)
    window.blit(text, (width // 4, height // 3))
    font = pygame.font.Font(None, 36)
    text = font.render('Press R to Restart', True, white)
    window.blit(text, (width // 4, height // 2))
    pygame.display.flip()

# Основной цикл игры
place_mines()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = event.pos
            gx, gy = mx // cell_size, my // cell_size
            if event.button == 1:  # Левая кнопка мыши
                if grid[gx][gy] == -1:
                    revealed[gx][gy] = True
                    game_over = True
                else:
                    reveal_cell(gx, gy)
            elif event.button == 3:  # Правая кнопка мыши
                toggle_flag(gx, gy)
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                place_mines()
    
    if game_over:
        game_over_screen()
    else:
        window.fill(white)
        draw_grid()
        pygame.display.flip()
