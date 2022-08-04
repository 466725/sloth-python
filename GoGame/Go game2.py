import pygame
import sys
import time

#soundObj = pygame.mixer.Sound('Move.WAV')
#soundObj.play()



def cleanup():
    pygame.quit()
    sys.exit()

def main():
    canplay = True
    line1 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line2 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line3 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line4 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line5 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line6 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line7 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line8 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line9 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line10 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line11 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line12 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line13 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line14 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line15 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line16 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line17 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line18 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}
    line19 = {1: "blank", 2: "blank", 3: "blank", 4: "blank", 5: "blank", 6: "blank", 7: "blank", 8: "blank", 9: "blank",
             10: "blank", 11: "blank", 12: "blank", 13: "blank", 14: "blank", 15: "blank", 16: "blank", 17: "blank",
             18: "blank", 19: "blank"}

    line_1_data = list(line1.values())
    line_2_data = list(line2.values())
    line_3_data = list(line3.values())
    line_4_data = list(line4.values())
    line_5_data = list(line5.values())
    line_6_data = list(line6.values())
    line_7_data = list(line7.values())
    line_8_data = list(line8.values())
    line_9_data = list(line9.values())
    line_10_data = list(line10.values())
    line_11_data = list(line11.values())
    line_12_data = list(line12.values())
    line_13_data = list(line13.values())
    line_14_data = list(line14.values())
    line_15_data = list(line15.values())
    line_16_data = list(line16.values())
    line_17_data = list(line17.values())
    line_18_data = list(line18.values())
    line_19_data = list(line19.values())
    board_data = [line_1_data, line_2_data, line_3_data, line_4_data, line_5_data, line_6_data, line_7_data,
                  line_8_data, line_9_data, line_10_data, line_11_data, line_12_data, line_13_data, line_14_data,
                  line_15_data, line_16_data, line_17_data, line_18_data, line_19_data, ]


    global whos_turn
    whos_turn = "It's the black players turn"
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
    global stone_size
    stone_size = small_side / 47 + 1

    pygame.display.set_caption('Go game board thing')
    screen.fill(brown)
    font = pygame.font.Font('freesansbold.ttf', int(height / 33))
    wrong_place = font.render("Hey! You can't play there!", False, red)
    wrong_place_erase = font.render("Hey! You can't play there!", False, brown)
    colour = black


    #icon = pygame.image.load('Go.jpg')
    #pygame.display.set_icon(icon)
    is_running = True
    def draw_stones():
        stone_size = small_side / 47 + 1
        for lineNum in range (19):
            for columnNum in range (19):
                line = board_data[lineNum]
                xpos = left_x + (line_length / 19 * ((columnNum + 1) + 0.05 * (columnNum + 1)) - line_length / 19)
                ypos = top_y + (line_length / 19 * ((lineNum + 1) + 0.05 * (lineNum + 1)) - line_length / 19)
                if line[columnNum] == "black":

                    pygame.draw.circle(screen, black, (xpos, ypos), stone_size)
                elif line[columnNum] == "white":
                    pygame.draw.circle(screen, white, (xpos, ypos), stone_size)



    def draw_board ():
        global small_side
        global top_y
        global left_x
        global line_length

        stone_size = small_side / 47 + 1

        if height > width:
            small_side = width
            large_side = height
        else:
            small_side = height
            large_side = width

        top_y = height / 2 - small_side / 21 * 20 / 2
        left_x = width / 2 - small_side / 21 * 17 / 2

        line_length = small_side / 1.165 + 1

        font = pygame.font.Font('freesansbold.ttf', int(height / 33))
        turn = font.render(whos_turn, False, black)
        screen.blit(turn, (left_x, top_y + line_length * 1.07))

        font = pygame.font.Font('freesansbold.ttf', int(small_side / 33))
        letter_pos = width / 2 - small_side / 21 * 17.02 / 2 + 0.1
        number_pos = height / 2 - small_side / 21 * 17.02 / 2 + 0.1 + (small_side / 1.295)
        numbers_letters = 0
        xpos = int(width / 2 - small_side / 21 * 17.02 / 2 + 0.1)
        ypos = int(height / 2 - small_side / 21 * 20.05 / 2)

        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 3.15,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 3.18), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 9.47,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 3.18), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 15.76,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 3.18), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 3.15,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 9.47), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 9.47,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 9.47), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 15.76,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 9.47), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 3.15,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 15.83), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 9.47,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 15.83), small_side / 100,
                           0)
        pygame.draw.circle(screen, black, (width / 2 - small_side / 21 * 17.02 / 2 + 1.1 + line_length / 19 * 15.76,
                                           height / 2 - small_side / 21 * 20.05 / 2 + 1 + line_length / 19 * 15.83), small_side / 100,
                           0)




        for i in range(19):
            #vertical lines
            pygame.draw.rect(screen, black, pygame.Rect(xpos, top_y, small_side / 350 + 1, line_length))
            #horizontal lines
            pygame.draw.rect(screen, black, pygame.Rect(left_x, ypos, line_length, small_side / 350 + 1))
            

            letter = letters[numbers_letters]
            number = numbers[numbers_letters]
            numbers_letters = numbers_letters + 1
            Letters = font.render(letter, False, black)
            Numbers = font.render(number, False, black)
            screen.blit(Letters, (letter_pos - 2, height / 2 - small_side / 21 * 17.02 / 2 + 0.1 + small_side / 1.22))
            screen.blit(Numbers, (width / 2 - small_side / 21 * 17.02 / 2 + 0.1 - small_side / 16.45, number_pos ))

            letter_pos = letter_pos + small_side / 21.14
            number_pos = number_pos - small_side / 21.14

            xpos = xpos + small_side / 21
            ypos = ypos + small_side / 21
            draw_stones()


    draw_board()


    while is_running:
        #draw_stones()
        line_1_data = list(line1.values())
        line_2_data = list(line2.values())
        line_3_data = list(line3.values())
        line_4_data = list(line4.values())
        line_5_data = list(line5.values())
        line_6_data = list(line6.values())
        line_7_data = list(line7.values())
        line_8_data = list(line8.values())
        line_9_data = list(line9.values())
        line_10_data = list(line10.values())
        line_11_data = list(line11.values())
        line_12_data = list(line12.values())
        line_13_data = list(line13.values())
        line_14_data = list(line14.values())
        line_15_data = list(line15.values())
        line_16_data = list(line16.values())
        line_17_data = list(line17.values())
        line_18_data = list(line18.values())
        line_19_data = list(line19.values())
        board_data = [line_1_data, line_2_data, line_3_data, line_4_data, line_5_data, line_6_data, line_7_data,
                      line_8_data, line_9_data, line_10_data, line_11_data, line_12_data, line_13_data, line_14_data,
                      line_15_data, line_16_data, line_17_data, line_18_data, line_19_data, ]
        
        #pygame.draw.circle(screen, black, (300, top_y), 20,0)

        #print(line_1_data)
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.VIDEORESIZE:

                stone_size = small_side / 47 + 1
                if event.w < 480:
                    screen = pygame.display.set_mode((480, event.h), pygame.RESIZABLE)
                elif event.h < 480:
                    screen = pygame.display.set_mode((event.w, 480), pygame.RESIZABLE)
                else:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                if height > width:
                    small_side = width
                    large_side = height
                else:
                    small_side = height
                    large_side = width

                stone_size = small_side / 47 + 1
                width = screen.get_width()
                height = screen.get_height()
                screen.fill(brown)
                draw_board()
                size = event.size


                #screen.fill(brown)
                #draw_board()



            if event.type == pygame.MOUSEBUTTONDOWN:

                stone_size = small_side / 47 + 1

                canplay = True
                colour_turn  = colour_turn + 1
                if mouse_x > left_x - line_length / 30 and mouse_y > top_y - line_length / 30 and mouse_x < width / 2 - small_side / 21 * 17.02 / 2 + 0.1 + line_length + line_length / 20 and mouse_y < height / 2 - small_side / 21 * 20.05 / 2 + line_length + line_length / 20:
                    if colour_turn % 2 == 0:
                        colour = "black"
                        whos_turn = "It's the white players turn"
                    else:
                        colour = "white"
                        whos_turn = "It's the black players turn"
                    screen.fill(brown)
                    draw_board()


                    line_num = 19 - ((((mouse_y - (top_y + line_length))) / (line_length / 18)) * -1)
                    if line_num - int(line_num) > 0.5:
                        line_num = line_num + 1
                    if line_num < 1:
                        line_num = 1
                    elif line_num > 19:
                        line_num = 19

                    column_num = 19 - ((((mouse_x - (left_x + line_length))) / (line_length / 18)) * -1)
                    if column_num - int(column_num) > 0.5:
                        column_num = column_num + 1
                    if column_num < 1:
                        column_num = 1
                    elif column_num > 19:
                        column_num = 19

                    print(int(line_num), int(column_num))
                    line_dict = 1
                    if int(line_num) == 1:
                        line_dict = line1
                    elif int(line_num) == 2:
                        line_dict = line2
                    elif int(line_num) == 3:
                        line_dict = line3
                    elif int(line_num) == 4:
                        line_dict = line4
                    elif int(line_num) == 5:
                        line_dict = line5
                    elif int(line_num) == 6:
                        line_dict = line6
                    elif int(line_num) == 7:
                        line_dict = line7
                    elif int(line_num) == 8:
                        line_dict = line8
                    elif int(line_num) == 9:
                        line_dict = line9
                    elif int(line_num) == 10:
                        line_dict = line10
                    elif int(line_num) == 11:
                        line_dict = line11
                    elif int(line_num) == 12:
                        line_dict = line12
                    elif int(line_num) == 13:
                        line_dict = line13
                    elif int(line_num) == 14:
                        line_dict = line14
                    elif int(line_num) == 15:
                        line_dict = line15
                    elif int(line_num) == 16:
                        line_dict = line16
                    elif int(line_num) == 17:
                        line_dict = line17
                    elif int(line_num) == 18:
                        line_dict = line18
                    elif int(line_num) == 19:
                        line_dict = line19

                    #canplay = False
                    #screen.blit(wrong_place, (210, 630))
                    #colour_turn = colour_turn - 1
                    mouse_x = left_x + (line_length / 19 * (int(column_num) + 0.05 * int(column_num))) - line_length / 19
                    mouse_y = top_y + (line_length / 19 * (int(line_num) + 0.05 * int(line_num))) - line_length / 19

                    if line_dict[int(column_num)] != "blank":
                        canplay = False
                    else:

                        line_dict[int(column_num)] = colour

                        if int(line_num) == 1:
                            line1 = line_dict
                        elif int(line_num) == 2:
                            line2 = line_dict
                        elif int(line_num) == 3:
                            line3 = line_dict
                        elif int(line_num) == 4:
                            line4 = line_dict
                        elif int(line_num) == 5:
                            line5 = line_dict
                        elif int(line_num) == 6:
                            line6 = line_dict
                        elif int(line_num) == 7:
                            line7 = line_dict
                        elif int(line_num) == 8:
                            line8 = line_dict
                        elif int(line_num) == 9:
                            line9 = line_dict
                        elif int(line_num) == 10:
                            line10 = line_dict
                        elif int(line_num) == 11:
                            line11 = line_dict
                        elif int(line_num) == 12:
                            line12 = line_dict
                        elif int(line_num) == 13:
                            line13 = line_dict
                        elif int(line_num) == 14:
                            line14 = line_dict
                        elif int(line_num) == 15:
                            line15 = line_dict
                        elif int(line_num) == 16:
                            line16 = line_dict
                        elif int(line_num) == 17:
                            line17 = line_dict
                        elif int(line_num) == 18:
                            line18 = line_dict
                        elif int(line_num) == 19:
                            line19 = line_dict

                    if canplay == True:
                        pygame.mixer.music.load('move.wav')
                        pygame.mixer.music.play()
                        pygame.draw.circle(screen, colour, (mouse_x, mouse_y), stone_size, 0)
                    else:
                        colour_turn = colour_turn - 1

        #if size != screen.get_size():
            #screen = pygame.display.set_mode(size, pygame.RESIZABLE)

        pygame.display.flip()

    cleanup()

if __name__ == "__main__":
    main()


