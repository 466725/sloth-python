import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((1300, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

move_num = 1
moves = [(-100, -100)]
click_x, click_y = -1000, -1000

board = []
for x in range(21):
    row = []
    for y in range(21):
        if 0 < x < 20 and 0 < y < 20:
            row.append("none")
        else:
            row.append("edge")
    board.append(row)

def check_liberties(colour, pos_x, pos_y, visited = None):
    if visited is None:
        visited = set()

    visited.add((pos_x, pos_y))

    for i in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if board[pos_x + i[0]][pos_y + i[1]] == "none":
            return True, []
        elif board[pos_x + i[0]][pos_y + i[1]] == colour and (pos_x + i[0], pos_y + i[1]) not in visited:
            visited.add((pos_x + i[0], pos_y + i[1]))
            if check_liberties(colour, pos_x + i[0], pos_y + i[1], visited)[0]:
                return True, []
    return False, visited


while True:
    board_width = min(screen.get_width(), screen.get_height()) * 0.8
    board_x = screen.get_width() / 2 - board_width / 2
    board_y = screen.get_height() / 2 - board_width / 2

    mouse_x, mouse_y = pygame.mouse.get_pos()
    temp_x = round((max(min(mouse_x, board_x + board_width), board_x) - board_x) / (board_width / 18)) + 1
    temp_y = round((max(min(mouse_y, board_y + board_width), board_y) - board_y) / (board_width / 18)) + 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((max(300, event.w), max(300, event.h)), pygame.RESIZABLE)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if len(moves) > 1:
                    remove = moves.pop()
                    board[remove[0]][remove[1]] = "none"
                    for cell in remove[2]:
                        board[cell[0]][cell[1]] = "black" if move_num % 2 == 1 else "white"
                    click_x, click_y = moves[-1][:2]
                    move_num -= 1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                legal = False

                if board[temp_x][temp_y] == "none":
                    board[temp_x][temp_y] = "black" if move_num % 2 == 1 else "white"

                    captured = []
                    for i in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        alive = True
                        dead_cells = set()
                        opp_colour = "white" if move_num % 2 == 1 else "black"
                        if board[temp_x + i[0]][temp_y + i[1]] == opp_colour:
                            alive, dead_cells = check_liberties(opp_colour, temp_x + i[0], temp_y + i[1])
                            if not alive:
                                legal = True
                                for cell in dead_cells:
                                    board[cell[0]][cell[1]] = "none"
                                    captured.append(cell)

                    if not legal:
                        if check_liberties("black" if move_num % 2 == 1 else "white", temp_x, temp_y)[0]:
                            legal = True
                        else:
                            board[temp_x][temp_y] = "none"

                    if legal:
                        click_x, click_y = temp_x, temp_y
                        moves.append((click_x, click_y, captured))
                        pygame.mixer.music.load("Move.WAV")
                        pygame.mixer.music.play(1)
                        move_num += 1


    #draw board

    for i in range(19):
        pygame.draw.rect(screen, (0, 0, 0), (board_x,
                                             board_y + i * (board_width / 18) - (board_width / 600),
                                             board_width, board_width / 300))
        pygame.draw.rect(screen, (0, 0, 0), (board_x + i * (board_width / 18) - (board_width / 600),
                                             board_y,
                                             board_width / 300, board_width))
    for i in [3, 9, 15]:
        for j in [3, 9, 15]:
            pygame.draw.circle(screen, (0, 0, 0), (board_x + i * (board_width / 18),
                                             board_y + j * (board_width / 18)), board_width / 150)

    ghost_colour = (0, 0, 0, 100) if move_num % 2 == 1 else (255, 255, 255, 100)
    pygame.draw.circle(screen, ghost_colour,
                       (board_x + (temp_x - 1) * (board_width / 18), board_y + (temp_y - 1) * (board_width / 18)),
                       board_width / 37)

    for row in range (1, 20):
        for column in range (1, 20):
            if board[row][column] == "black":
                pygame.draw.circle(screen, (0, 0, 0),
                                   (board_x + (row - 1) * (board_width / 18),
                                    board_y + (column - 1) * (board_width / 18)), board_width / 37)
            elif board[row][column] == "white":
                pygame.draw.circle(screen, (255, 255, 255),
                                   (board_x + (row - 1) * (board_width / 18),
                                    board_y + (column - 1) * (board_width / 18)), board_width / 37)

    pygame.draw.circle(screen, (255, 0, 0),
                       (board_x + (click_x - 1) * (board_width / 18), board_y + (click_y - 1) * (board_width / 18)),
                       board_width / 75)



    pygame.display.update()
    screen.fill((128, 82, 22))
    clock.tick(120)