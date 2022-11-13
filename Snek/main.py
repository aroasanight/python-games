import curses
from time import sleep, time
from random import randint
from datetime import datetime

import pickle

# N - Name
# S - Score
# H - Height
# W - Width
# T - Time run ended

#           N          S   H   W   T  Wall  Tail
# save = [['Testuser', 16, 15, 15, 0, True, True]]

try:
  with open('saves.dmp', 'rb') as file: thisIsNeverUsed = pickle.load(file)
except:
  with open('saves.dmp', 'wb') as file: pickle.dump([['Phil', 0, 43, 79, datetime.now(), True, True]], file)

# with open('saves.dmp', 'rb') as save2:
#   save = pickle.load(save2)
#   print(save)
#   for loadsave in range(0, len(save)):
#     print(str(save[loadsave][0])+"'s save:")
#     print(' - Score:', save[loadsave][1])
#     print(' - % of grid covered: '+str(round((100/(save[loadsave][2]*save[loadsave][3]))*(save[loadsave][1]+2))))
#     print(' - Walldeath: '+str(save[loadsave][5]))
#     print(' - Taildeath: '+str(save[loadsave][6]))
#     print('Played on '+save[loadsave][4].strftime("%b %d %Y %H:%M:%S")+' on a '+str(save[loadsave][2])+'x'+str(save[loadsave][3])+' grid.')

# sleep(5)

def main(screen):

  loop = True

  walldeath = True
  taildeath = True

  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # 1 - Green (snake)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # 2 - Red (food)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) # 3 - White (grid)
  curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # 4 - Cyan (accent)

  rows, cols = screen.getmaxyx()

  maxgridheight = rows-6
  if maxgridheight / 2 == round(maxgridheight / 2): maxgridheight = maxgridheight - 1
  if not (round(rows/2) == rows/2): maxgridheight = maxgridheight - 2
  maxgridwidth = round((cols-2)/2)-1
  if maxgridwidth / 2 == round(maxgridwidth / 2): maxgridwidth = maxgridwidth - 1

  if maxgridheight >= 15: height = 15
  else: height = maxgridheight

  if maxgridwidth >= 15: width = 15
  else: width = maxgridwidth

  toosmall = False

  if cols < 94: deathtruemsg = "It is reccommended that at least one of these is true."
  elif cols < 58: toosmall = True
  else: deathtruemsg = "It is reccommended that at least one of these is true, otherwise it's impossible to die."

  if rows < 20: toosmall = True

  if toosmall and rows > 3 and cols >= 24:
    while screen.getmaxyx()[1] < 58:
      screen.addstr(0, 0, "Your screen's too small.")
      screen.addstr(1, 0, "Press CMD - to shrink")
      screen.addstr(2, 0, "your font size until the")
      screen.addstr(3, 0, "game starts.")
      screen.refresh()
    toosmall = False
  elif toosmall: screen.addstr(60,0,'e') # ---> If this fails, your screen is too small. <---

  if not toosmall:

    def viewSaves():
      with open('saves.dmp', 'rb') as save2:
        save = pickle.load(save2)
        loadsave = len(save)-1
        saveviewing = True
        screen.nodelay(False)
        while saveviewing:
          screen.clear()
          screen.addstr(1, 2, "Viewing save "+str(len(save)-loadsave)+" of "+str(len(save)), curses.color_pair(1))
          screen.addstr(2, 2, str(save[loadsave][0])+"'s save:", curses.color_pair(4))
          screen.addstr(4, 4, '- Score: '+str(save[loadsave][1]))
          screen.addstr(5, 4, '- % of grid covered: '+str(round((100/(save[loadsave][2]*save[loadsave][3]))*(save[loadsave][1]+2))))
          screen.addstr(6, 4, '- Walldeath: '+str(save[loadsave][5]))
          screen.addstr(7, 4, '- Taildeath: '+str(save[loadsave][6]))
          screen.addstr(9, 2, 'Played on '+save[loadsave][4].strftime("%b %d %Y %H:%M:%S")+' on a '+str(save[loadsave][2])+'x'+str(save[loadsave][3])+' grid.', curses.color_pair(4))
          screen.addstr(11, 2, "Use left/right arrows to navigate between saves.")
          screen.addstr(12, 2, "Press P to view the save with the highest % covered.")
          screen.addstr(13, 2, "Press ESC to exit.")
          screen.refresh()
          Key = screen.getch()

          if Key == curses.KEY_LEFT:
            if loadsave >= len(save)-1: loadsave = 0
            else: loadsave = loadsave + 1
          elif Key == curses.KEY_RIGHT:
            if loadsave <= 0: loadsave = len(save)-1
            else: loadsave = loadsave - 1
          elif Key == ord('p'):
            tmp = 0
            largest = 0
            for i in range(0,len(save)-1):
              if round((100/(save[i][2]*save[i][3]))*(save[i][1]+2)) > tmp:
                tmp = round((100/(save[i][2]*save[i][3]))*(save[i][1]+2))
                largest = i
            loadsave = largest
          elif Key == 27: saveviewing = False
        screen.nodelay(True)

    while loop:

      cont = False
      screen.nodelay(False)
      while cont == False:
        screen.clear()
        screen.addstr(1, 2, 'SNEK', curses.color_pair(1))
        screen.addstr(2, 2, 'Adjust game options, then press SPACE to start.')
        screen.addstr(2, 34, 'SPACE', curses.color_pair(4))
        screen.addstr(4, 4, 'Up: Q | Down: A', curses.color_pair(4))
        screen.addstr(5, 4, 'Height: '+str(height)+'  ')
        screen.addstr(7, 4, 'Up: W | Down: S', curses.color_pair(4))
        screen.addstr(8, 4, 'Width: '+str(width)+'  ')
        if walldeath: screen.addstr(10, 4, '(Z) Wall death: True ', curses.color_pair(1))
        else: screen.addstr(10, 4, '(Z) Wall death: False', curses.color_pair(2))
        if taildeath: screen.addstr(11, 4, '(X) Tail death: True ', curses.color_pair(1))
        else: screen.addstr(11, 4, '(X) Tail death: False', curses.color_pair(2))
        if (not walldeath) and (not taildeath): screen.addstr(12, 4, deathtruemsg, curses.color_pair(2))
        screen.addstr(14, 2, "Press P to view saves.", curses.color_pair(4))
        screen.addstr(16, 2, 'CONTROLS', curses.color_pair(1))
        screen.addstr(17, 4, 'ARROW KEYS - Move', curses.color_pair(4))
        screen.addstr(18, 4, 'ESC - Quit/Pause', curses.color_pair(4))

        Key = screen.getch()

        if Key == ord('q') and height < maxgridheight: height = height + 2
        elif Key == ord('a') and height > 5: height = height - 2
        elif Key == ord('w') and width < maxgridwidth: width = width + 2
        elif Key == ord('s') and width > 5: width = width - 2
        elif Key == ord('z'): walldeath = not walldeath
        elif Key == ord('x'): taildeath = not taildeath
        elif Key == ord('p'): viewSaves()
        elif Key == ord(' '): cont = True

      screen.clear()

      if cont:
        # figure out coordinates of top, bottom, left and right of play area, if the middle is (0,0)
        maxHeight = int((height-1)/2)
        minHeight = int(0-((height-1)/2))
        maxWidth = int((width-1)/2)
        minWidth = int(0-((width-1)/2))

        # create list of positions
        positions = []
        for i in range(0,height):
          # create new row
          positions.append([])
          for j in range(0,width):
            # add -2 to each x position in that row
            positions[i].append(-2)

        # the next 2 functions are needed for the way the game deals coordinates - (0,0) is the middle,
        # and if these functions weren't
        # update function - updates a position in the list to a new count value by returning an updated list
        def update(inp, x, y, count):
          inp[(0-y)+maxHeight][x+maxWidth] = count
          return inp

        # get the count value for a given coordinate
        def getcount(inp, x, y): return(inp[(0-y)+maxHeight][x+maxWidth])

        def death(score):
          timefinished = datetime.now()
          screen.clear()
          screen.addstr(1, 2, "You died!", curses.color_pair(4))
          screen.addstr(2, 4, "Your final score was: "+str(score))
          screen.addstr(4, 2, "Would you like to save? (Y/N)", curses.color_pair(1))
          screen.refresh()
          screen.nodelay(False)
          pressed = False
          while not pressed:
            Key = screen.getch()
            if Key == ord('y'):
              curses.echo()
              screen.addstr(5, 4, "Enter your name:", curses.color_pair(4))
              name = screen.getstr(5, 21)
              pressed = True
              with open('saves.dmp', 'rb') as file:
                save = pickle.load(file)
              save.append([str(name).replace("b'", "").replace("'", ""), score, height, width, timefinished, walldeath, taildeath])
              with open('saves.dmp', 'wb') as file:
                pickle.dump(save, file)
              curses.noecho()
            elif Key == ord('n'): pressed = True
          screen.nodelay(True)

        playerX = minWidth+2 # x position of player - start near the left edge
        playerY = 0          # y position of player - start in the middle of the screen
        direction = 0
        c = 0
        count = 5

        score = 0
        tempScore = -1 # when this is not equal to score, a new position for the food will be generated, and it will be updated to the same value of score

        foodX = 0 # x position of food - will be regenerated instantly, so these don't matter,
        foodY = 0 # y position of food   they just need to be declared

        screen.nodelay(True) # don't wait for a key to be pressed at 'Key = screen.getch()'

        screen.clear()

        while True:
          t_end = time()+0.425-(score/150)
          while time() < t_end:
            Key = screen.getch()
            if Key == curses.KEY_RIGHT: direction = 0
            elif Key == curses.KEY_DOWN: direction = 1
            elif Key == curses.KEY_LEFT: direction = 2
            elif Key == curses.KEY_UP: direction = 3
            elif Key == ord('d'): direction = 0
            elif Key == ord('s'): direction = 1
            elif Key == ord('a'): direction = 2
            elif Key == ord('w'): direction = 3
            elif Key == 27:
              screen.nodelay(False)
              screen.clear()
              screen.addstr(1, 2, 'PAUSED', curses.color_pair(4))
              screen.addstr(2, 2, 'Press ESC to quit, or any other key to continue.')
              screen.refresh()
              Key = screen.getch()
              if Key == 27:
                screen.clear()
                screen.addstr(1,2,'Bye!')
                screen.refresh()
                sleep(1)
                loop = False
                break
              else:
                screen.nodelay(True)
                screen.clear()

          if not loop: break

          # generate food
          if tempScore != score:
            tempScore = score
            foodX = randint(minWidth, maxWidth)
            foodY = randint(minHeight, maxHeight)

          # movement bit
          if direction == 0:
            if playerX < maxWidth: playerX = playerX + 1
            else:
              if walldeath:
                death(score)
                break
              else: playerX = minWidth
          if direction == 2:
            if playerX > minWidth: playerX = playerX - 1
            else:
              if walldeath:
                death(score)
                break
              else: playerX = maxWidth
          if direction == 3:
            if playerY < maxHeight: playerY = playerY + 1
            else:
              if walldeath:
                death(score)
                break
              else: playerY = minHeight
          if direction == 1:
            if playerY > minHeight: playerY = playerY - 1
            else:
              if walldeath:
                death(score)
                break
              else: playerY = maxHeight

          count += 1
          if getcount(positions, playerX, playerY) > count - (score+2) and taildeath:
            death(score)
            break
          else: update(positions, playerX, playerY, count)

          # draw screen
          screen.clear()
          for screenY in range(maxHeight, minHeight-1, -1):
            for screenX in range(minWidth, maxWidth+1, 1):
              if getcount(positions, screenX, screenY) > count - (score + 2):
                if screenX == playerX and screenY == playerY and getcount(positions, screenX, screenY) != count:
                  death(score)
                  break
                if screenX == foodX and screenY == foodY: score = score + 1
                screen.addstr(2+(0-(screenY-maxHeight)), 2+(screenX+maxWidth)*2, '■', curses.color_pair(1))
              elif screenX == foodX and screenY == foodY: screen.addstr(2+(0-(screenY-maxHeight)), 2+(screenX+maxWidth)*2, '▧', curses.color_pair(2))
              else: screen.addstr(2+(0-(screenY-maxHeight)), 2+(screenX+maxWidth)*2, '□', curses.color_pair(3))
          screen.addstr(1, 2, 'Score:', curses.color_pair(4))
          screen.addstr(1, 9, str(score))
          screen.addstr(1, 12+len(str(score)), '% filled:', curses.color_pair(4))
          screen.addstr(1, 22+len(str(score)), str(round((100/(height*width))*(score+2))))
          screen.addstr(height+3, 2, 'CONTROLS:', curses.color_pair(4))
          screen.addstr(height+4, 4, 'ARROW KEYS - Move')
          screen.addstr(height+5, 4, 'Q - Quit/Pause')
          screen.refresh()

curses.wrapper(main)