import pygame
from os import remove as removefile
from shutil import copyfile
from time import time, localtime, asctime
from pickle import load as pickleLoad
from pickle import dump as pickleDump
from datetime import datetime
from pygame.locals import *
from pygame.time import Clock
from random import randint
from screeninfo import get_monitors

assetspath = "assets/"
ufpath = "userfiles/"

pausetime = 4

# logging function
def log(content:str):
    newcontent = '[game.py] - '+asctime(localtime(time())) +': '+str(content)
    with open (assetspath+'log.txt', 'at') as f: f.write(newcontent+'\n')
    print(newcontent)

# clear log.txt
with open (assetspath+'log.txt', 'wt') as f: f.write('')
log('log.txt cleared.')

# datetime function
def date(): return(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

log('setting up save/load functions')
def load_options():
    with open (assetspath+'options.sf', 'rb') as f: return pickleLoad(f)

def load_save():
    with open (assetspath+'save.sf', 'rb') as f: return pickleLoad(f)

def save_options():
    with open (assetspath+'options.sf', 'wb') as f: pickleDump(options, f)

def save_save():
    with open (assetspath+'save.sf', 'wb') as f: pickleDump(savedata, f)

log('loading files...')

# load options file
try:
    options = load_options()
    log('options loaded!')
except:
    log('Failed to load options - starting afresh with following values:')
    options = [640, 360, 5, 'UnnamedPlayer'+str(randint(1000, 9999)), 12, 12, 12, assetspath+'defaultTextures/']
    try: save_options()
    except: pass
    log(options)

# load save file
try:
    savedata = load_save()
    log('save data loaded!')
except:
    log('Failed to import data - starting afresh with following values:')
    savedata = ['0', '0', time()]
    log(savedata)

# set screen resoltution
primaryFound = False
primaryWidth = 0
primaryHeight = 0
for m in get_monitors():
    log(str(m))
    if m.is_primary:
        log("primary monitor found! using this monitor's screen resolution of "+str(m.width)+"x"+str(m.height)+".")
        primaryFound = True
        primaryWidth = m.width
        primaryHeight = m.height
    else: log("not primary monitor, checking for other monitors...")
if primaryFound:
    log('returning dimensions of primary monitor...')
    primaryDimensions = (int(primaryWidth), int(primaryHeight))
else:
    log("unable to find primary monitor's screen resolution, using default of 640x360.")
    primaryDimensions = (640, 360)

try:
    windowwidth = primaryDimensions[0]
    windowheight = primaryDimensions[1]

except:
    try:
        windowwidth = options[0]
        windowheight = options[1]
        log('using window height from options.sf')

    except:
        windowwidth = 640
        windowheight = 360
        log('no window size specified, using default: 640x360')

width = windowwidth
height = windowheight

game_name = 'game'

(width, height) = (windowwidth, windowheight)
log('window size: '+str(width)+'x'+str(height))

# setup stuff
gameopen = True
log('initialising pygame, variables and clock')
pygame.init()
pygame.mixer.init()
playersize = (width/640)*32
clock = Clock()
log('creating window')
DISPLAY = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption(game_name)
log('importing textures, other assets, and other visual stuff')
backgroundColour = (55, 55, 55)

if options[7]: # load custom textures (if enabled)
    log('using custom textures')

    # Player texture
    try:
        player = pygame.image.load(options[8]+'player.png')
        log('player texture imported')
    except:
        player = pygame.image.load(assetspath+'defaultTextures/player.png')
        log('player texture not found, using default')

    # Player glow
    try:
        playerGlow = pygame.image.load(options[8]+'playerGlow.png')
        log('playerGlow texture imported')
    except:
        playerGlow = pygame.image.load(assetspath+'defaultTextures/playerGlow.png')
        log('playerGlow texture not found, using default')

    # Enemy texture
    try:
        enemytex = pygame.image.load(options[8]+'enemy.png')
        log('enemy texture imported')
    except:
        enemytex = pygame.image.load(assetspath+'defaultTextures/enemy.png')
        log('enemy texture not found, using default')

    # Enemy glow
    try:
        enemyGlow = pygame.image.load(options[8]+'enemyGlow.png')
        log('enemyGlow texture imported')
    except:
        enemyGlow = pygame.image.load(assetspath+'defaultTextures/enemyGlow.png')
        log('enemyGlow texture not found, using default')

    # Music
    try:
        pygame.mixer.music.load(options[8]+'music.mp3')
        log('music imported')
    except:
        pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
        log('music not found, using default')

    # Main font
    try:
        mainfont = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*32))
        log('main font imported')
    except:
        mainfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
        log('main font not found, using default')

    # Small font
    try:
        smallfont = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*12))
        log('small font imported')
    except:
        smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))
        log('small font not found, using default')

else: # import default textures if texture packs are disabled
    log('using default textures')
    player = pygame.image.load(assetspath+'defaultTextures/player.png')
    playerGlow = pygame.image.load(assetspath+'defaultTextures/playerGlow.png')
    enemytex = pygame.image.load(assetspath+'defaultTextures/enemy.png')
    enemyGlow = pygame.image.load(assetspath+'defaultTextures/enemyGlow.png')
    pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
    mainfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
    smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))

# set app icon - this is outside the if/else loop because it isn't able to be changed by the texture pack
pygame.display.set_icon(pygame.image.load(assetspath+'defaultTextures/appicon.png'))

# resize player + enemy textures for window size
player = pygame.transform.scale(player, (playersize, playersize))
playerGlow = pygame.transform.scale(playerGlow, (playersize*1.25, playersize*1.25))
enemytex = pygame.transform.scale(enemytex, (playersize, playersize))
enemyGlow = pygame.transform.scale(enemyGlow, (playersize*1.25, playersize*1.25))

# music stuff
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()
log('music started')

colourcycle = 0

r = 55
g = 55
b = 255

screen = 1
gameGen = False

status = ''

def bool_to_humanreadable(input):
    if input: return('On')
    else: return('Off')

# how to get info about options boxes:
# optionsBoxes[i][j]
# where i is the box you want info for (0-4)
# and j is what you want about it (0 = active:bool, 1 = text:str)
optionsBoxes = [
    [False, str(options[2])], # Options box 1
    [False, str(options[3])], # Options box 2
    [False, str(options[4])+', '+str(options[5])+', '+str(options[6])], # Options box 3
    [False, str(bool_to_humanreadable(options[7]))], # Options box 4
    [False, str(options[8])] # Options box 5
]

t_end = time() - 1 # a time in the past so there's no delay when starting
keeprendering = True

while gameopen:

    clock.tick(60)

    # restart music if it stops
    try:
        if pygame.mixer.music.get_busy() == False:
            log('music finished, restarting')
            pygame.mixer.music.play()
    except: pass

    # quit
    for event in pygame.event.get():
        if event.type==QUIT:
            log('quitting')
            pygame.quit()
            gameopen = False
    
    if not gameopen: break

    try: pygame.display.update()
    except: pass

    # -----> GAME <-----
    if screen == 0:

        if time() > t_end:
            keeprendering = True

            if not gameGen: # run once at the start of the game

                try: # get difficulty from options, or use default of 5
                    difficulty = options[2]
                    log('using difficulty from options.sf')
                except:
                    difficulty = 5
                    log('no difficulty specified, using default: 5')
                log('difficulty: '+str(difficulty))

                log('creating class enemy')
                class Enemy():
                    def __init__(enemy, x, y):
                        enemy.xpos = x
                        enemy.ypos = y
                log('class enemy created!')

                score = 0
                playersize = (width/640)*32
                playerX = width/2 - playersize/2
                playerY = height/2 - playersize/2

                #             0     1      2      3
                #             Down  Up     Left   Right
                directions = [True, False, False, False]
                enemies =    [[],   [],    [],    []   ]

                backgroundColour = (int(options[4]), int(options[5]), int(options[6]))

                for i in range(difficulty): enemies[0].append(Enemy(randint(0, int(width-playersize)), randint(int((0-playersize)*8), int(0-playersize))))

                gameGen = True

            # enable other directions for enemies at the appropriate times
            if score >= 25 and directions[1] == False:
                for i in range(difficulty): enemies[1].append(Enemy(randint(0, int(width-playersize)), randint(height, int(height+playersize*8))))
                directions[1] = True

            if score >= 50 and directions[2] == False:
                for i in range(difficulty): enemies[2].append(Enemy(randint(width, int(width+playersize*8)), randint(0, int(height-playersize))))
                directions[2] = True

            if score >= 75 and directions[3] == False:
                for i in range(difficulty): enemies[3].append(Enemy(randint(int(0-playersize)*8, int(0-playersize)), randint(0, int(height-playersize))))
                directions[3] = True

            # setup speeds in relation to window size - player moves slightly faster than enemies
            speed = (score/30 + (windowwidth/640)*3)+1.5
            enemyspeed = ((score/30 + (windowwidth/640))/2.5)+1.5

            DISPLAY.fill([int(options[4]), int(options[5]), int(options[6])])
            DISPLAY.blit(playerGlow, ((playerX-playersize*0.125, playerY-playersize*0.125)))
            DISPLAY.blit(player, (playerX, playerY))

            # downwards facing enemies
            if directions[0] and keeprendering:
                for enemy in enemies[0]:
                    if enemy.ypos > height:
                        enemy.ypos = randint(int((0-playersize)*8), int(0-playersize))
                        enemy.xpos = randint(0, int(width-playersize))
                        score = score + 1
                        log('enemy moved to top, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.xpos)+', '+str(enemy.ypos))
                    else: enemy.ypos = enemy.ypos + enemyspeed

                    DISPLAY.blit(enemyGlow, ((enemy.xpos-playersize*0.125, enemy.ypos-playersize*0.125)))
                    DISPLAY.blit(enemytex, (enemy.xpos, enemy.ypos))

                    if playerX+playersize > enemy.xpos and playerX < enemy.xpos+playersize and playerY+playersize > enemy.ypos and playerY < enemy.ypos+playersize:
                            
                        log('rendering death screen - final score: '+str(score)+' - difficulty: '+str(difficulty)+' - highscore: '+str(savedata[0]))
                        DISPLAY.fill(backgroundColour)
                        renderedText = mainfont.render('Your score was '+str(score), True, (255-backgroundColour[0], 255-backgroundColour[1], 255-backgroundColour[2]))
                        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))
                        renderedText = mainfont.render('Your highscore is '+str(savedata[0]), True, (255-backgroundColour[0], 255-backgroundColour[1], 255-backgroundColour[2]))
                        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, height-10-renderedText.get_height()))
                        pygame.display.update()

                        if score > int(savedata[0]) and difficulty >= int(savedata[1]):
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            savedata[2] = date()
                            savedata = [str(score), str(difficulty), date()]
                            save_save()
                            log('save complete')

                        elif score > int(savedata[0])+15:
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            savedata[2] = date()
                            save_save()
                            log('save complete')

                        log('recording score in savefile...')
                        savedata.append(str(score))
                        savedata.append(str(difficulty))
                        savedata[2] = date()
                        save_save()
                        log('save complete')

                        log('waiting 4 seconds')
                        t_end = time() + pausetime
                        keeprendering = False
                        gameGen = False

            # upwards facing enemies
            if directions[1] and keeprendering:
                for enemy in enemies[1]:
                    if enemy.ypos < 0-playersize:
                        enemy.ypos = randint(height, int(height+(playersize*8)))
                        enemy.xpos = randint(0, int(width-playersize))
                        score = score + 1
                        log('enemy moved to bottom, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.xpos)+', '+str(enemy.ypos))
                    else: enemy.ypos = enemy.ypos - enemyspeed

                    DISPLAY.blit(enemyGlow, ((enemy.xpos-playersize*0.125, enemy.ypos-playersize*0.125)))
                    DISPLAY.blit(enemytex, (enemy.xpos, enemy.ypos))

                    if playerX+playersize > enemy.xpos and playerX < enemy.xpos+playersize and playerY+playersize > enemy.ypos and playerY < enemy.ypos+playersize:
                            
                        log('rendering death screen')
                        DISPLAY.fill(backgroundColour)
                        renderedText = mainfont.render('Your score was '+str(score), True, (255-backgroundColour[0], 255-backgroundColour[1], 255-backgroundColour[2]))
                        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))
                        renderedText = mainfont.render('Your highscore is '+str(savedata[0]), True, (255-backgroundColour[0], 255-backgroundColour[1], 255-backgroundColour[2]))
                        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, height-10-renderedText.get_height()))
                        pygame.display.update()

                        if score > int(savedata[0]) and difficulty >= int(savedata[1]):
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            savedata[2] = date()
                            save_save()
                            log('save complete')

                        elif score > int(savedata[0])+15:
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            savedata[2] = date()
                            save_save()
                            log('save complete')

                        log('recording score in savefile...')
                        savedata.append(str(score))
                        savedata.append(str(difficulty))
                        savedata[2] = date()
                        save_save()
                        log('save complete')

                        log('waiting 4 seconds')
                        t_end = time() + pausetime
                        keeprendering = False
                        gameGen = False

            # left facing enemies
            if directions[2] and keeprendering:
                for enemy in enemies[2]:
                    if enemy.xpos < 0-playersize:
                        enemy.xpos = randint(width, width+(playersize*8))
                        enemy.ypos = randint(0, int(height-playersize))
                        score = score + 1
                        log('enemy moved to right, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.xpos)+', '+str(enemy.ypos))
                    else: enemy.xpos = enemy.xpos - enemyspeed
                    
                    DISPLAY.blit(enemyGlow, ((enemy.xpos-playersize*0.125, enemy.ypos-playersize*0.125)))
                    DISPLAY.blit(enemytex, (enemy.xpos, enemy.ypos))

                    if playerX+playersize > enemy.xpos and playerX < enemy.xpos+playersize and playerY+playersize > enemy.ypos and playerY < enemy.ypos+playersize:
                            
                        log('rendering death screen')
                        DISPLAY.fill(backgroundColour)
                        renderedText = mainfont.render('Your score was '+str(score), True, (255-backgroundColour[0], 255-backgroundColour[1], 255-backgroundColour[2]))
                        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))
                        renderedText = mainfont.render('Your highscore is '+str(savedata[0]), True, (255-backgroundColour[0], 255-backgroundColour[1], 255-backgroundColour[2]))
                        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, height-10-renderedText.get_height()))
                        pygame.display.update()

                        if score > int(savedata[0]) and difficulty >= int(savedata[1]):
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            savedata[2] = date()
                            save_save()
                            log('save complete')

                        elif score > int(savedata[0])+15:
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            savedata[2] = date()
                            save_save()
                            log('save complete')

                        log('recording score in savefile...')
                        savedata.append(str(score))
                        savedata.append(str(difficulty))
                        savedata[2] = date()
                        save_save()
                        log('save complete')

                        log('waiting 4 seconds')
                        t_end = time() + pausetime
                        keeprendering = False
                        gameGen = False

            # right facing enemies
            if directions[3] and keeprendering:
                for enemy in enemies[3]:
                    if enemy.xpos > width:
                        enemy.xpos = randint(0-playersize*8, 0-playersize)
                        enemy.ypos = randint(0, int(height-playersize))
                        score = score + 1
                        log('enemy moved to left, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.xpos)+', '+str(enemy.ypos))
                    else: enemy.xpos = enemy.xpos + enemyspeed
                        
                    DISPLAY.blit(enemyGlow, ((enemy.xpos-playersize*0.125, enemy.ypos-playersize*0.125)))
                    DISPLAY.blit(enemytex, (enemy.xpos, enemy.ypos))

                    if playerX+playersize > enemy.xpos and playerX < enemy.xpos+playersize and playerY+playersize > enemy.ypos and playerY < enemy.ypos+playersize:
                            
                        log('rendering death screen')
                        DISPLAY.fill(backgroundColour)
                        renderedText = mainfont.render('Your score was '+str(score), True, (255-backgroundColour[0], 255-backgroundColour[1], 255-backgroundColour[2]))
                        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))
                        renderedText = mainfont.render('Your highscore is '+str(savedata[0]), True, (255-backgroundColour[0], 255-backgroundColour[1], 255-backgroundColour[2]))
                        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, height-10-renderedText.get_height()))
                        pygame.display.update()

                        if score > int(savedata[0]) and difficulty >= int(savedata[1]):
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            savedata[2] = date()
                            save_save()
                            log('save complete')

                        elif score > int(savedata[0])+15:
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            savedata[2] = date()
                            save_save()
                            log('save complete')

                        log('recording score in savefile...')
                        savedata.append(str(score))
                        savedata.append(str(difficulty))
                        savedata[2] = date()
                        save_save()
                        log('save complete')

                        log('waiting 4 seconds')
                        t_end = time() + pausetime
                        gameGen = False

            # score
            if keeprendering:
                renderedText = mainfont.render(str(score), True, (255-backgroundColour[0], 255-backgroundColour[1], 255-backgroundColour[2]))
                DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))

            # keybinds
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and playerX < width-playersize: playerX = playerX + speed
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and playerX > 0: playerX = playerX - speed
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and playerY > 0: playerY = playerY - speed
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and playerY < height-playersize: playerY = playerY + speed
            if keys[pygame.K_p]: screen = 1

    # -----> MENU <-----
    elif screen == 1:

        # rainbow background
        if colourcycle >= 0 and colourcycle < 200: r = r + 1
        elif colourcycle >= 200 and colourcycle < 400: b = b - 1
        elif colourcycle >= 400 and colourcycle < 600: g = g + 1
        elif colourcycle >= 600 and colourcycle < 800: r = r - 1
        elif colourcycle >= 800 and colourcycle < 1000: b = b + 1
        elif colourcycle >= 1000 and colourcycle < 1200: g = g - 1
        elif colourcycle >= 1200: colourcycle = 0
        DISPLAY.fill([int(r/3), int(g/3), int(b/3)])
        colourcycle += 1

        # menu text and images
        renderedText = mainfont.render('Welcome!', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))
        key = smallfont.render('Press a number on your keyboard to begin.', True, (245, 245, 245))
        DISPLAY.blit(key, (width/2 - key.get_width()/2, height/9))
        renderedText = smallfont.render('1 - Launch Game', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, height/6))
        renderedText = smallfont.render('2 - Edit Options', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2)))
        renderedText = smallfont.render('3 - View Stats', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*2)))
        renderedText = smallfont.render('4 - View Controls', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*3)))
        renderedText = smallfont.render('5 - Backup save files', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*4)))
        renderedText = smallfont.render('6 - Restore save files', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*5)))
        renderedText = smallfont.render('Press Q to Exit', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*7)))

        # keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]: 
            screen = 0
            gameGen = False
        if keys[pygame.K_2]: 
            screen = 2
            gameGen = False
        if keys[pygame.K_3]: 
            screen = 3
            gameGen = False
        if keys[pygame.K_4]: 
            screen = 4
            gameGen = False
        if keys[pygame.K_5]:
            try:
                removefile(ufpath+'options.sf')
                removefile(ufpath+'save.sf')
            except: pass
            copyfile(assetspath+'options.sf', ufpath+'options.sf')
            copyfile(assetspath+'save.sf', ufpath+'save.sf')
            while keys[pygame.K_5]:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    gameopen = False
                    pygame.quit()
        if keys[pygame.K_6]:
            removefile(assetspath+'options.sf')
            removefile(assetspath+'save.sf')
            copyfile(ufpath+'options.sf', assetspath+'options.sf')
            copyfile(ufpath+'save.sf', assetspath+'save.sf')
            while keys[pygame.K_6]:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    gameopen = False
                    pygame.quit()
        if keys[pygame.K_7]: screen = 9

        if keys[pygame.K_q]:
            gameopen = False
            pygame.quit()

    # ----> OPTIONS <---
    elif screen == 2:

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box1.collidepoint(event.pos): optionsBoxes[0][0] = not optionsBoxes[0][0]
            else: optionsBoxes[0][0] = False
                
            if input_box2.collidepoint(event.pos): optionsBoxes[1][0] = not optionsBoxes[1][0]
            else: optionsBoxes[1][0] = False
                
            if input_box3.collidepoint(event.pos): optionsBoxes[2][0] = not optionsBoxes[2][0]
            else: optionsBoxes[2][0] = False
                
            if input_box4.collidepoint(event.pos): optionsBoxes[3][0] = not optionsBoxes[3][0]
            else: optionsBoxes[3][0] = False
                
            if options[7]:
                if input_box5.collidepoint(event.pos): optionsBoxes[4][0] = not optionsBoxes[4][0]
                else: optionsBoxes[4][0] = False
                
        if event.type == pygame.KEYDOWN:
                if optionsBoxes[0][0]:
                    if event.key == pygame.K_RETURN:
                        print(optionsBoxes[0][1])
                        try:
                            options[2] = int(optionsBoxes[0][1])
                            log('difficulty set to '+str(options[2]))
                            status = 'Difficulty set to '+str(options[2])
                            save_options()
                        except:
                            log('failed!')
                            status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                        optionsBoxes[0][1] = str(options[2])
                    elif event.key == pygame.K_BACKSPACE:
                        optionsBoxes[0][1] = optionsBoxes[0][1][:-1]
                    else:
                        optionsBoxes[0][1] += event.unicode

                if optionsBoxes[1][0]:
                    if event.key == pygame.K_RETURN:
                        print(optionsBoxes[1][1])
                        try:
                            options[3] = optionsBoxes[1][1]
                            log('username set to '+str(options[3]))
                            status = 'Username set to '+str(options[3])
                            save_options()
                        except:
                            log('failed!')
                            status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                        optionsBoxes[1][1] = str(options[3])
                    elif event.key == pygame.K_BACKSPACE:
                        optionsBoxes[1][1] = optionsBoxes[1][1][:-1]
                    else:
                        optionsBoxes[1][1] += event.unicode

                if optionsBoxes[2][0]:
                    if event.key == pygame.K_RETURN:
                        print(optionsBoxes[2][1])
                        try:
                            temparray = optionsBoxes[2][1].split(', ')
                            options[4] = int(temparray[0])
                            options[5] = int(temparray[1])
                            options[6] = int(temparray[2])
                            log('background colour set to '+str(options[4])+', '+str(options[5])+', '+str(options[6]))
                            status = 'Background colour set to '+str(options[4])+', '+str(options[5])+', '+str(options[6])
                            save_options()
                        except:
                            log('failed!')
                            status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                        optionsBoxes[2][1] = str(options[4])+', '+str(options[5])+', '+str(options[6])
                    elif event.key == pygame.K_BACKSPACE:
                        optionsBoxes[2][1] = optionsBoxes[2][1][:-1]
                    else:
                        optionsBoxes[2][1] += event.unicode

                if optionsBoxes[3][0]:
                    if event.key == pygame.K_RETURN:
                        print(optionsBoxes[3][1])
                        try:
                            if optionsBoxes[3][1] == 'on' or optionsBoxes[3][1] == 'On' or optionsBoxes[3][1] == 'ON' or optionsBoxes[3][1] == '1' or optionsBoxes[3][1] == 'true' or optionsBoxes[3][1] == 'True' or optionsBoxes[3][1] == 'TRUE' or optionsBoxes[3][1] == 'yes' or optionsBoxes[3][1] == 'Yes' or optionsBoxes[3][1] == 'YES' or optionsBoxes[3][1] == 'y' or optionsBoxes[3][1] == 'Y':
                                options[7] = True
                                log('texture pack enabled')
                                status = 'Texture pack enabled'
                            elif optionsBoxes[3][1] == 'off' or optionsBoxes[3][1] == 'Off' or optionsBoxes[3][1] == 'OFF' or optionsBoxes[3][1] == '0' or optionsBoxes[3][1] == 'false' or optionsBoxes[3][1] == 'False' or optionsBoxes[3][1] == 'FALSE' or optionsBoxes[3][1] == 'no' or optionsBoxes[3][1] == 'No' or optionsBoxes[3][1] == 'NO' or optionsBoxes[3][1] == 'n' or optionsBoxes[3][1] == 'N':
                                options[7] = False
                                log('texture pack disabled')
                                status = 'Texture pack disabled'
                            else:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                            save_options()
                        except:
                            log('failed!')
                            status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                        if options[7]: optionsBoxes[3][1] = 'On'
                        else: optionsBoxes[3][1] = 'Off'
                    elif event.key == pygame.K_BACKSPACE:
                        optionsBoxes[3][1] = optionsBoxes[3][1][:-1]
                    else:
                        optionsBoxes[3][1] += event.unicode

                if optionsBoxes[4][0] and options[7]:
                    if event.key == pygame.K_RETURN:
                        print(optionsBoxes[4][1])
                        try:
                            options[8] = optionsBoxes[4][1]
                            log('texture path set to '+str(options[8]))
                            status = 'Texture pack path set to '+str(options[8])
                            save_options()
                        except:
                            log('failed!')
                            status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                        optionsBoxes[4][1] = str(options[8])
                    elif event.key == pygame.K_BACKSPACE: optionsBoxes[4][1] = optionsBoxes[4][1][:-1]
                    else: optionsBoxes[4][1] += event.unicode

        # rainbow background
        if colourcycle >= 0 and colourcycle < 200: r = r + 1
        elif colourcycle >= 200 and colourcycle < 400: b = b - 1
        elif colourcycle >= 400 and colourcycle < 600: g = g + 1
        elif colourcycle >= 600 and colourcycle < 800: r = r - 1
        elif colourcycle >= 800 and colourcycle < 1000: b = b + 1
        elif colourcycle >= 1000 and colourcycle < 1200: g = g - 1
        elif colourcycle >= 1200: colourcycle = 0
        DISPLAY.fill([int(r/3), int(g/3), int(b/3)])
        colourcycle += 1

        # menu text and images
        renderedText = mainfont.render('Options', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))

        renderedText = smallfont.render('Press a number on your keyboard to edit that option\'s value.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, height/9))

        renderedText = smallfont.render('1 - Difficulty', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, height/6))
        input_box1 = pygame.Rect(width/22+renderedText.get_width()+(width/44), height/6, width/2, height/24)

        renderedText = smallfont.render('2 - Username', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2)))
        input_box2 = pygame.Rect(width/22+renderedText.get_width()+(width/44), (height/6)+(renderedText.get_height()*1.2), width/2, height/24)

        renderedText = smallfont.render('3 - Background colour', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*2)))
        input_box3 = pygame.Rect(width/22+renderedText.get_width()+(width/44), (height/6)+(renderedText.get_height()*1.2*2), width/2, height/24)

        renderedText = smallfont.render('4 - Texture pack on/off', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*3)))
        input_box4 = pygame.Rect(width/22+renderedText.get_width()+(width/44), (height/6)+(renderedText.get_height()*1.2*3), width/2, height/24)

        if options[7]:
            renderedText = smallfont.render('5 - Texture pack path', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*4)))
            input_box5 = pygame.Rect(width/22+renderedText.get_width()+(width/44), (height/6)+(renderedText.get_height()*1.2*4), width/2, height/24)

            renderedText = smallfont.render('Press P to Exit', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*6)))
        else:
            renderedText = smallfont.render('Press P to Exit', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*5)))

        renderedText = smallfont.render(status, True, (245, 245, 245))
        DISPLAY.blit(renderedText, ((width/2)-(renderedText.get_width()/2), height-(height/22)))

        renderedText = smallfont.render(' '+optionsBoxes[0][1], True, (245, 245, 245))
        input_box1.w = max(350, renderedText.get_width()+10)
        DISPLAY.blit(renderedText, (input_box1.x+5, input_box1.y+5))
        pygame.draw.rect(DISPLAY, (245, 245, 245), input_box1, 2)

        renderedText = smallfont.render(' '+optionsBoxes[1][1], True, (245, 245, 245))
        input_box2.w = max(350, renderedText.get_width()+10)
        DISPLAY.blit(renderedText, (input_box2.x+5, input_box2.y+5))
        pygame.draw.rect(DISPLAY, (245, 245, 245), input_box2, 2)

        renderedText = smallfont.render(' '+optionsBoxes[2][1], True, (245, 245, 245))
        input_box3.w = max(350, renderedText.get_width()+10)
        DISPLAY.blit(renderedText, (input_box3.x+5, input_box3.y+5))
        pygame.draw.rect(DISPLAY, (245, 245, 245), input_box3, 2)

        renderedText = smallfont.render(' '+optionsBoxes[3][1], True, (245, 245, 245))
        input_box4.w = max(350, renderedText.get_width()+10)
        DISPLAY.blit(renderedText, (input_box4.x+5, input_box4.y+5))
        pygame.draw.rect(DISPLAY, (245, 245, 245), input_box4, 2)

        if options[7]:
            renderedText = smallfont.render(' '+optionsBoxes[4][1], True, (245, 245, 245))
            input_box5.w = max(350, renderedText.get_width()+10)
            DISPLAY.blit(renderedText, (input_box5.x+5, input_box5.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box5, 2)

        # keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]: screen = 1
        if keys[pygame.K_TAB]: screen = 5

    # -----> STATS <----
    elif screen == 3:

        # rainbow background
        if colourcycle >= 0 and colourcycle < 200: r = r + 1
        elif colourcycle >= 200 and colourcycle < 400: b = b - 1
        elif colourcycle >= 400 and colourcycle < 600: g = g + 1
        elif colourcycle >= 600 and colourcycle < 800: r = r - 1
        elif colourcycle >= 800 and colourcycle < 1000: b = b + 1
        elif colourcycle >= 1000 and colourcycle < 1200: g = g - 1
        elif colourcycle >= 1200: colourcycle = 0
        DISPLAY.fill([int(r/3), int(g/3), int(b/3)])
        colourcycle += 1
        
        # menu text and images
        renderedText = mainfont.render('Stats', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))
        try:
            renderedText = smallfont.render('Highscore: '+str(savedata[0]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, height/6))
            renderedText = smallfont.render('Highscore difficulty: '+str(savedata[1]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*1)))
            renderedText = smallfont.render('Highscore date: '+str(savedata[2]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*2)))
        except: pass
        try:
            renderedText = smallfont.render('Latest score: '+str(savedata[len(savedata)-2]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*3.5)))
            renderedText = smallfont.render('Latest difficulty: '+str(savedata[len(savedata)-1]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*4.5)))
            renderedText = smallfont.render('Latest date: '+str(savedata[len(savedata)]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*5.5)))
        except: pass
        try:
            renderedText = smallfont.render('Earliest score: '+str(savedata[3]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*7)))
            renderedText = smallfont.render('Earliest difficulty: '+str(savedata[4]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*8)))
            renderedText = smallfont.render('Earliest date: '+str(savedata[5]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*9)))
        except: pass
        renderedText = smallfont.render('Press P to Exit, or 1 to jump directly into the game.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*11)))

        # keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]: screen = 1
        if keys[pygame.K_1]: screen = 0

    # -----> HELP <-----
    elif screen == 4:

        # rainbow background
        if colourcycle >= 0 and colourcycle < 200: r = r + 1
        elif colourcycle >= 200 and colourcycle < 400: b = b - 1
        elif colourcycle >= 400 and colourcycle < 600: g = g + 1
        elif colourcycle >= 600 and colourcycle < 800: r = r - 1
        elif colourcycle >= 800 and colourcycle < 1000: b = b + 1
        elif colourcycle >= 1000 and colourcycle < 1200: g = g - 1
        elif colourcycle >= 1200: colourcycle = 0
        DISPLAY.fill([int(r/3), int(g/3), int(b/3)])
        colourcycle += 1

        # menu text and images
        renderedText = mainfont.render('Help', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))
        renderedText = smallfont.render('To move your character, use the arrow keys. Press P to return to the menu.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, height/6))
        renderedText = smallfont.render('The aim of the game is to avoid the enemies for as long as possible.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2)))
        renderedText = smallfont.render('The game ends when you first touch an enemy.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*2)))
        renderedText = smallfont.render('Good luck!', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*3)))
        renderedText = smallfont.render('Press P to Exit, or 1 to jump directly into the game.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*5)))

        # keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]: screen = 1
        if keys[pygame.K_1]: screen = 0

    # ---> OPT HELP <---
    elif screen == 5:

        # rainbow background
        if colourcycle >= 0 and colourcycle < 200: r = r + 1
        elif colourcycle >= 200 and colourcycle < 400: b = b - 1
        elif colourcycle >= 400 and colourcycle < 600: g = g + 1
        elif colourcycle >= 600 and colourcycle < 800: r = r - 1
        elif colourcycle >= 800 and colourcycle < 1000: b = b + 1
        elif colourcycle >= 1000 and colourcycle < 1200: g = g - 1
        elif colourcycle >= 1200: colourcycle = 0
        DISPLAY.fill([int(r/3), int(g/3), int(b/3)])
        colourcycle += 1

        # menu text and images
        renderedText = mainfont.render('Options help', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))
        renderedText = smallfont.render('To edit a value, click in the box next to it, and change it\'s value by typing a new one.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*1)))
        renderedText = smallfont.render('Press enter to submit.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*2)))
        renderedText = smallfont.render('When editing the Difficulty value, make sure you only type numbers, and no other characters.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*3.5)))
        renderedText = smallfont.render('You can type anything in the username field.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*5)))
        renderedText = smallfont.render('When editing the Background value, type 3 numbers that are above 0 and less than 255, ', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*6.5)))
        renderedText = smallfont.render('seperated by commas (e.g. 45, 255, 0).', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*8.5)))
        renderedText = smallfont.render('When editing the Custom Texture toggle value, type \'on\' or \'off\'. You can also type \'true\', ', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*10)))
        renderedText = smallfont.render('\'false\', \'y\', \'n\', \'yes\', or \'no\'.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*11)))
        renderedText = smallfont.render('When editing the Custom Texture path value, type the path of your texture pack in relation', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*12.5)))
        renderedText = smallfont.render('to the game\'s files. Make sure you put a \'/\' at the end of it.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*13.5)))
        renderedText = smallfont.render('Press P to return to the options menu, or 1 to return to the main menu.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, height-renderedText.get_height()*1.2))

        # keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]: screen = 2
        if keys[pygame.K_1]: screen = 1

# 0 - game
# 1 - menu
# 2 - options
# 3 - stats
# 4 - help
# 5 - options help
# 9 - Credits