import pygame
import sys
import time


def cleanup():
    pygame.quit()
    sys.exit()

def main():
    canplay = True
    line1 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",


    }
    line2 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line3 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line4 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line5 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line6 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line7 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line8 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line9 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line10 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line11 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line12 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line13 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line14 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line15 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line16 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line17 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line18 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    line19 = {
        1: "blank",
        2: "blank",
        3: "blank",
        4: "blank",
        5: "blank",
        6: "blank",
        7: "blank",
        8: "blank",
        9: "blank",
        10: "blank",
        11: "blank",
        12: "blank",
        13: "blank",
        14: "blank",
        15: "blank",
        16: "blank",
        17: "blank",
        18: "blank",
        19: "blank",

    }
    colour_turn = 1
    white = (255, 255, 255)
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", " I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S"]
    numbers = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
    black = (0, 0, 0)
    brown = (128, 82, 22)
    pygame.init()
    red = (255, 0, 0)
    size = (630, 660)
    global small_side
    small_side = 1
    global large_side
    large_side = 1
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    width = screen.get_width()
    height = screen.get_height()
    if height > width:
        small_side = width
        large_side = height
    else:
        small_side = height
        large_side = width

    pygame.display.set_caption('Go game board thing')
    screen.fill(brown)
    font = pygame.font.Font('freesansbold.ttf', int(height / 33))
    wrong_place = font.render("Hey! You can't play there!", False, red)
    wrong_place_erase = font.render("Hey! You can't play there!", False, brown)
    colour = black


    #icon = pygame.image.load('Go.jpg')
    #pygame.display.set_icon(icon)
    is_running = True

    def draw_board ():
        if height > width:
            small_side = width
            large_side = height
        else:
            small_side = height
            large_side = width
        global line_length
        line_length = small_side / 1.165 + 1
        font = pygame.font.Font('freesansbold.ttf', int(small_side / 33))
        letter_pos = width / 2 - small_side / 21 * 17.02 / 2 + 0.1
        number_pos = height / 2 - small_side / 21 * 17.02 / 2 + 0.1 + (small_side / 1.295)
        numbers_letters = 0
        xpos = width / 2 - small_side / 21 * 17.02 / 2 + 0.1
        ypos = height / 2 - small_side / 21 * 20.05 / 2

        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 3.15,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 3.18), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 9.47,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 3.18), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 15.78,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 3.18), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 3.15,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 9.47), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 9.47,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 9.47), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 15.78,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 9.47), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 3.15,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 15.83), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 9.47,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 15.83), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 15.78,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 15.83), small_side / 100,
                           0)




        for i in range(19):
            #vertical lines
            pygame.draw.rect(screen, black, pygame.Rect(xpos, height / 2 - small_side / 21 * 20 / 2, small_side / 350 + 1, line_length))
            #horizontal lines
            pygame.draw.rect(screen, black, pygame.Rect(width / 2 - small_side / 21 * 17 / 2, ypos, line_length, small_side / 350 + 1))
            

            letter = letters[numbers_letters]
            number = numbers[numbers_letters]
            numbers_letters = numbers_letters + 1
            Letters = font.render(letter, False, black)
            Numbers = font.render(number, False, black)
            screen.blit(Letters, (letter_pos - 2, height / 2 - small_side / 21 * 17.02 / 2 + 0.1 + (small_side / 1.22)))
            screen.blit(Numbers, (width / 2 - small_side / 21 * 17.02 / 2 + 0.1 - small_side / 16.45, number_pos ))

            letter_pos = letter_pos + (small_side / 21.14)
            number_pos = number_pos - (small_side / 21.14)

            xpos = xpos + (small_side / 21)
            ypos = ypos + (small_side / 21)

    draw_board()


    while is_running:

        #print(line1)
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.VIDEORESIZE:
                width = screen.get_width()
                height = screen.get_height()
                if height > width:
                    small_side = width
                    large_side = height
                else:
                    small_side = height
                    large_side = width
                size = event.size
                if small_side < 480:
                    small_side = 480
                    if width > height:
                        screen = pygame.display.set_mode((width, 480), pygame.RESIZABLE)
                        screen.fill(brown)
                        draw_board()
                    else:
                        screen = pygame.display.set_mode((480, height), pygame.RESIZABLE)
                        screen.fill(brown)
                        draw_board()
                else:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    screen.fill(brown)
                    draw_board()


            if event.type == pygame.MOUSEBUTTONDOWN:
                canplay = True
                colour_turn  = colour_turn + 1
                if mouse_x > width / 2 - small_side / 21 * 17.02 / 2 + 0.1 - line_length / 20 and mouse_y > height / 2 - small_side / 21 * 20.05 / 2 - line_length / 20 and mouse_x < width / 2 - small_side / 21 * 17.02 / 2 + 0.1 + line_length + line_length / 20 and mouse_y < height / 2 - small_side / 21 * 20.05 / 2 + line_length + line_length / 20:
                    if colour_turn % 2 == 0:
                        colour = "black"
                    else:
                        colour = "white"
                    if mouse_y < height / 2 - small_side / 21 * 20 / 2 + line_length / 38:
                        mouse_y = height / 2 - small_side / 21 * 20 / 2
                        if mouse_x < 75 and line1[1] == "blank":
                            mouse_x = 60
                            line1[1] = colour
                        elif mouse_x < 105 and line1[2] == "blank" and mouse_x >= 75:
                            mouse_x = 90
                            line1[2] = colour
                        elif mouse_x < 135 and line1[3] == "blank" and mouse_x >= 105:
                            mouse_x = 120
                            line1[3] = colour
                        elif mouse_x < 165 and line1[4] == "blank" and mouse_x >= 135:
                            mouse_x = 150
                            line1[4] = colour
                        elif mouse_x < 195 and line1[5] == "blank" and mouse_x >= 165:
                            mouse_x = 180
                            line1[5] = colour
                        elif mouse_x < 225 and line1[6] == "blank" and mouse_x >= 195:
                            mouse_x = 210
                            line1[6] = colour
                        elif mouse_x < 255 and line1[7] == "blank" and mouse_x >= 225:
                            mouse_x = 240
                            line1[7] = colour
                        elif mouse_x < 285 and line1[8] == "blank" and mouse_x >= 255:
                            mouse_x = 270
                            line1[8] = colour
                        elif mouse_x < 315 and line1[9] == "blank" and mouse_x >= 285:
                            mouse_x = 300
                            line1[9] = colour
                        elif mouse_x < 345 and line1[10] == "blank" and mouse_x >= 315:
                            mouse_x = 330
                            line1[10] = colour
                        elif mouse_x < 375 and line1[11] == "blank" and mouse_x >= 345:
                            mouse_x = 360
                            line1[11] = colour
                        elif mouse_x < 405 and line1[12] == "blank" and mouse_x >= 375:
                            mouse_x = 390
                            line1[12] = colour
                        elif mouse_x < 435 and line1[13] == "blank" and mouse_x >= 405:
                            mouse_x = 420
                            line1[13] = colour
                        elif mouse_x < 465 and line1[14] == "blank" and mouse_x >= 435:
                            mouse_x = 450
                            line1[14] = colour
                        elif mouse_x < 495 and line1[15] == "blank" and mouse_x >= 465:
                            mouse_x = 480
                            line1[15] = colour
                        elif mouse_x < 525 and line1[16] == "blank" and mouse_x >= 495:
                            mouse_x = 510
                            line1[16] = colour
                        elif mouse_x < 555 and line1[17] == "blank" and mouse_x >= 525:
                            mouse_x = 540
                            line1[17] = colour
                        elif mouse_x < 585 and line1[18] == "blank" and mouse_x >= 555:
                            mouse_x = 570
                            line1[18] = colour
                        elif mouse_x < 615 and line1[19] == "blank" and mouse_x >= 585:
                            mouse_x = 600
                            line1[19] = colour
                        else:
                            canplay = False
                            screen.blit(wrong_place, (210, 630))
                            colour_turn = colour_turn - 1
                    if canplay == True:
                        pygame.draw.circle(screen, colour, (mouse_x, mouse_y), small_side / 47 + 1, 0)

        if size != screen.get_size():
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)

        pygame.display.flip()

    cleanup()

if __name__ == "__main__":
    main()


