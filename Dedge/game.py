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
from sys import exit

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


# load save file
try:
    savedata = load_save()
    log('save data loaded!')
except:
    log('Failed to import data - starting afresh with following values:')
    savedata = ['0', '0', time()]
    log(savedata)

pygame.init()
print(pygame.display.Info().current_w)
# load options file
try:
    options = load_options()
    log('options loaded!')
    log(options)
except:
    log('Failed to load options - starting afresh with following values:')
    #          0           1                                          2.0  2.1  2.2  3                4                5           6              7             8                    9.0                               9.1
    #          Difficulty  Username                                   R    G    B    Textures toggle  Texture pack     Fullscreen  Master volume  Music volume  Death sound volume   Width                             Height
    options = [2,          'UnnamedPlayer'+str(randint(1000, 9999)), [12,  12,  12], False,           'fakecomicsans', True,       1.0,           0.3,          0.5,                [pygame.display.Info().current_w,  pygame.display.Info().current_h]]
    try: save_options()
    except: pass
    log(options)
if options[5]: 
    DISPLAY = pygame.display.set_mode((options[9][0], options[9][1]), pygame.FULLSCREEN)
    width, height = DISPLAY.get_size()
else: DISPLAY = pygame.display.set_mode((options[9][0], options[9][1]))
log('window size: '+str(width)+'x'+str(height))


game_name = 'game'

# setup stuff
gameopen = True
log('initialising pygame, variables and clock')
pygame.mixer.init()
playersize = (width/640)*32
clock = Clock()
log('creating window')


pygame.display.set_caption(game_name)
log('importing textures, other assets, and other visual stuff')
backgroundColour = (55, 55, 55)

# import textures that are always the same (not in pack)
playerGlow = pygame.image.load(assetspath+'defaultTextures/playerGlow.png')
pygame.display.set_icon(pygame.image.load(assetspath+'defaultTextures/appicon.png'))
enemyGlow = pygame.image.load(assetspath+'defaultTextures/enemyGlow.png')
playerGlow = pygame.transform.scale(playerGlow, (playersize*1.325, playersize*1.325))
enemyGlow = pygame.transform.scale(enemyGlow, (playersize*1.325, playersize*1.325))

menurainbow = True
gamerainbow = True

numberkeys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

if options[3]: # load custom textures (if enabled)
    log('using custom textures')

    # Player texture
    try:
        player = pygame.image.load('userfiles/textures/'+options[4]+'/player.png')
        log('player texture imported')
    except:
        player = pygame.image.load(assetspath+'defaultTextures/player.png')
        log('player texture not found, using default')

    # Enemy texture
    try:
        enemytex = pygame.image.load('userfiles/textures/'+options[4]+'/enemy.png')
        log('enemy texture imported')
    except:
        enemytex = pygame.image.load(assetspath+'defaultTextures/enemy.png')
        log('enemy texture not found, using default')

    # settingsbutton texture
    try:
        settingsbutton = pygame.image.load('userfiles/textures/'+options[4]+'/options.png')
        log('settingsbutton texture imported')
    except:
        settingsbutton = pygame.image.load(assetspath+'defaultTextures/options.png')
        log('settingsbutton texture not found, using default')

    # menubutton texture
    try:
        menubutton = pygame.image.load('userfiles/textures/'+options[4]+'/menu.png')
        log('menubutton texture imported')
    except:
        menubutton = pygame.image.load(assetspath+'defaultTextures/menu.png')
        log('menubutton texture not found, using default')

    # exitbutton texture
    try:
        exitbutton = pygame.image.load('userfiles/textures/'+options[4]+'/exit.png')
        log('exitbutton texture imported')
    except:
        exitbutton = pygame.image.load(assetspath+'defaultTextures/exit.png')
        log('exitbutton texture not found, using default')

    # statsbutton texture
    try:
        statsbutton = pygame.image.load('userfiles/textures/'+options[4]+'/stats.png')
        log('statsbutton texture imported')
    except:
        statsbutton = pygame.image.load(assetspath+'defaultTextures/stats.png')
        log('statsbutton texture not found, using default')

    # playbutton texture
    try:
        playbutton = pygame.image.load('userfiles/textures/'+options[4]+'/play.png')
        log('playbutton texture imported')
    except:
        playbutton = pygame.image.load(assetspath+'defaultTextures/play.png')
        log('playbutton texture not found, using default')

    # helpbutton texture
    try:
        helpbutton = pygame.image.load('userfiles/textures/'+options[4]+'/help.png')
        log('helpbutton texture imported')
    except:
        helpbutton = pygame.image.load(assetspath+'defaultTextures/help.png')
        log('helpbutton texture not found, using default')

    # Menu texture
    try:
        menuwallpaper = pygame.image.load('userfiles/textures/'+options[4]+'/menu.png')
        menurainbow = False
        log('menu texture imported')
    except:
        menurainbow = True
        log('menu texture not found, using rainbow')

    # Game texture
    try:
        gamewallpaper = pygame.image.load('userfiles/textures/'+options[4]+'/game.png')
        gamerainbow = False
        log('game texture imported')
    except:
        gamerainbow = True
        log('game texture not found, using rainbow')

    # Music
    try:
        pygame.mixer.music.load('userfiles/textures/'+options[4]+'/music.mp3')
        log('music imported')
    except:
        pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
        log('music not found, using default')

    # Death sound
    try:
        deathSound = pygame.mixer.Sound('userfiles/textures/'+options[4]+'/death.mp3')
        log('death sound imported')
    except:
        deathSound = pygame.mixer.Sound(assetspath+'defaultTextures/death.mp3')
        log('death sound not found, using default')

    # Main font
    try:
        mainfont = pygame.font.Font('userfiles/textures/'+options[4]+'/font.ttf', int((width/640)*32))
        log('main font imported')
    except:
        mainfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((width/640)*32))
        log('main font not found, using default')

    # Small font
    try:
        smallfont = pygame.font.Font('userfiles/textures/'+options[4]+'/smallfont.ttf', int((width/640)*12))
        log('small font imported')
    except:
        smallfont = pygame.font.Font(assetspath+'defaultTextures/smallfont.ttf', int((width/640)*12))
        log('small font not found, using default')

else: # import default textures if texture packs are disabled
    log('using default textures')
    player = pygame.image.load(assetspath+'defaultTextures/player.png')
    enemytex = pygame.image.load(assetspath+'defaultTextures/enemy.png')
    pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
    deathSound = pygame.mixer.Sound(assetspath+'defaultTextures/death.mp3')
    mainfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((width/640)*32))
    smallfont = pygame.font.Font(assetspath+'defaultTextures/smallfont.ttf', int((width/640)*12))
    settingsbutton = pygame.image.load(assetspath+'defaultTextures/options.png')
    menubutton = pygame.image.load(assetspath+'defaultTextures/menu.png')
    exitbutton = pygame.image.load(assetspath+'defaultTextures/exit.png')
    statsbutton = pygame.image.load(assetspath+'defaultTextures/stats.png')
    playbutton = pygame.image.load(assetspath+'defaultTextures/play.png')
    helpbutton = pygame.image.load(assetspath+'defaultTextures/help.png')

# resize textures for window size
player = pygame.transform.scale(player, (playersize, playersize))
enemytex = pygame.transform.scale(enemytex, (playersize, playersize))
settingsbutton = pygame.transform.scale(settingsbutton, (round(width/14)*6, round(width/14)*0.75))
menubutton = pygame.transform.scale(menubutton, (round(width/14)*6, round(width/14)*0.75))
exitbutton = pygame.transform.scale(exitbutton, (round(width/14)*6, round(width/14)*0.75))
statsbutton = pygame.transform.scale(statsbutton, (round(width/14)*6, round(width/14)*0.75))
playbutton = pygame.transform.scale(playbutton, (round(width/14)*6, round(width/14)*0.75))
helpbutton = pygame.transform.scale(helpbutton, (round(width/14)*6, round(width/14)*0.75))
if not menurainbow: menuwallpaper = pygame.transform.scale(menuwallpaper, (width, height))
if not gamerainbow: gamewallpaper = pygame.transform.scale(gamewallpaper, (width, height))

# sound stuff
deathSound.set_volume(options[8]*options[6])
pygame.mixer.music.set_volume(options[7]*options[6])
pygame.mixer.music.play()
log('music started')

colourcycle = 0

colours = [55, 55, 255]

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
    # column 1
    [False, str(options[0])], # Options box 1
    [False, str(options[1])], # Options box 2
    [False, str(options[2][0])+', '+str(options[2][1])+', '+str(options[2][2])], # Options box 3
    bool_to_humanreadable(options[3]), # Options box 4
    [False, str(options[4])], # Options box 5

    # column 2
    [False, str(round(options[6]*100))], # Options box 6
    [False, str(round(options[7]*100))], # Options box 7
    [False, str(round(options[8]*100))], # Options box 8
    bool_to_humanreadable(options[5]) # Options box 9
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
            exit()
    
    if not gameopen: break

    try: pygame.display.update()
    except: pass

    # -----> GAME <-----
    if screen == 0:

        if time() > t_end:
            keeprendering = True

            if not gameGen: # run once at the start of the game

                try: # get difficulty from options, or use default of 5
                    if options[0] == 1: difficulty = 4
                    elif options[0] == 2: difficulty = 6
                    elif options[0] == 3: difficulty = 9
                    else: difficulty = 4
                    log('using difficulty from options.sf')
                except:
                    difficulty = 4
                    log('no difficulty specified, using default: 4')
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

                # to read from array:
                # enemies[i][j]
                # where i is the direction (0 = down, 1 = up, 2 = left, 3 = right)
                # and j is what you want to know about it (0 = enabled:bool, 1 = enemies:list)
                enemies = [
                    [True,  []], # 0 - Down
                    [False, []], # 1 - Up
                    [False, []], # 2 - Left
                    [False, []]  # 3 - Right
                ]

                backgroundColour = (int(options[2][0]), int(options[2][1]), int(options[2][2]))

                for i in range(difficulty): enemies[0][1].append(Enemy(randint(0, int(width-playersize)), randint(int((0-playersize)*8), int(0-playersize))))

                gameGen = True

            # enable other directions for enemies at the appropriate times
            if score >= 25 and enemies[1][0] == False:
                for i in range(difficulty): enemies[1][1].append(Enemy(randint(0, int(width-playersize)), randint(height, int(height+playersize*8))))
                enemies[1][0] = True

            if score >= 50 and enemies[2][0] == False:
                for i in range(difficulty): enemies[2][1].append(Enemy(randint(width, int(width+playersize*8)), randint(0, int(height-playersize))))
                enemies[2][0] = True

            if score >= 75 and enemies[3][0] == False:
                for i in range(difficulty): enemies[3][1].append(Enemy(randint(int(0-playersize)*8, int(0-playersize)), randint(0, int(height-playersize))))
                enemies[3][0] = True

            # setup speeds in relation to window size - player moves slightly faster than enemies
            speed = (score/30 + (width/640)*3)+1.5
            enemyspeed = ((score/30 + (width/640))/2.5)+1.5

            DISPLAY.fill([int(options[2][0]), int(options[2][1]), int(options[2][2])])
            DISPLAY.blit(playerGlow, ((playerX-playersize*0.1625, playerY-playersize*0.1625)))
            DISPLAY.blit(player, (playerX, playerY))

            # downwards facing enemies
            if enemies[0][0] and keeprendering:
                for enemy in enemies[0][1]:
                    if enemy.ypos > height:
                        enemy.ypos = randint(int((0-playersize)*8), int(0-playersize))
                        enemy.xpos = randint(0, int(width-playersize))
                        score = score + 1
                        log('enemy moved to top, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.xpos)+', '+str(enemy.ypos))
                    else: enemy.ypos = enemy.ypos + enemyspeed

                    if keeprendering:
                        DISPLAY.blit(enemyGlow, ((enemy.xpos-playersize*0.1625, enemy.ypos-playersize*0.1625)))
                        DISPLAY.blit(enemytex, (enemy.xpos, enemy.ypos))

                    if playerX+playersize > enemy.xpos and playerX < enemy.xpos+playersize and playerY+playersize > enemy.ypos and playerY < enemy.ypos+playersize:
                            
                        deathSound.play()
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
                        keeprendering = False
                        t_end = time() + pausetime
                        gameGen = False

            # upwards facing enemies
            if enemies[1][0] and keeprendering:
                for enemy in enemies[1][1]:
                    if enemy.ypos < 0-playersize:
                        enemy.ypos = randint(height, int(height+(playersize*8)))
                        enemy.xpos = randint(0, int(width-playersize))
                        score = score + 1
                        log('enemy moved to bottom, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.xpos)+', '+str(enemy.ypos))
                    else: enemy.ypos = enemy.ypos - enemyspeed

                    if keeprendering:
                        DISPLAY.blit(enemyGlow, ((enemy.xpos-playersize*0.1625, enemy.ypos-playersize*0.1625)))
                        DISPLAY.blit(enemytex, (enemy.xpos, enemy.ypos))

                    if playerX+playersize > enemy.xpos and playerX < enemy.xpos+playersize and playerY+playersize > enemy.ypos and playerY < enemy.ypos+playersize:
                            
                        deathSound.play()
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
                        keeprendering = False
                        t_end = time() + pausetime
                        gameGen = False

            # left facing enemies
            if enemies[2][0] and keeprendering:
                for enemy in enemies[2][1]:
                    if enemy.xpos < 0-playersize:
                        enemy.xpos = randint(width, int(width+(playersize*8)))
                        enemy.ypos = randint(0, int(height-playersize))
                        score = score + 1
                        log('enemy moved to right, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.xpos)+', '+str(enemy.ypos))
                    else: enemy.xpos = enemy.xpos - enemyspeed
                    
                    if keeprendering:
                        DISPLAY.blit(enemyGlow, ((enemy.xpos-playersize*0.1625, enemy.ypos-playersize*0.1625)))
                        DISPLAY.blit(enemytex, (enemy.xpos, enemy.ypos))

                    if playerX+playersize > enemy.xpos and playerX < enemy.xpos+playersize and playerY+playersize > enemy.ypos and playerY < enemy.ypos+playersize:
                            
                        deathSound.play()
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
                        keeprendering = False
                        t_end = time() + pausetime
                        gameGen = False

            # right facing enemies
            if enemies[3][0] and keeprendering:
                for enemy in enemies[3][1]:
                    if enemy.xpos > width:
                        enemy.xpos = randint(int(0-playersize*8), int(0-playersize))
                        enemy.ypos = randint(0, int(height-playersize))
                        score = score + 1
                        log('enemy moved to left, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.xpos)+', '+str(enemy.ypos))
                    else: enemy.xpos = enemy.xpos + enemyspeed
                        
                    if keeprendering:
                        DISPLAY.blit(enemyGlow, ((enemy.xpos-playersize*0.1625, enemy.ypos-playersize*0.1625)))
                        DISPLAY.blit(enemytex, (enemy.xpos, enemy.ypos))

                    if playerX+playersize > enemy.xpos and playerX < enemy.xpos+playersize and playerY+playersize > enemy.ypos and playerY < enemy.ypos+playersize:
                            
                        deathSound.play()
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
                        keeprendering = False
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

        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]: 
                screen = 1
                t_end = time()-1

    # -----> MENU <-----
    elif screen == 1:

        inmenu = True

        while inmenu:
            if menurainbow:
                # rainbow background
                if colourcycle >= 0 and colourcycle < 200: colours[0] = colours[0] + 1
                elif colourcycle >= 200 and colourcycle < 400: colours[2] = colours[2] - 1
                elif colourcycle >= 400 and colourcycle < 600: colours[1] = colours[1] + 1
                elif colourcycle >= 600 and colourcycle < 800: colours[0] = colours[0] - 1
                elif colourcycle >= 800 and colourcycle < 1000: colours[2] = colours[2] + 1
                elif colourcycle >= 1000 and colourcycle < 1200: colours[1] = colours[1] - 1
                elif colourcycle >= 1200: colourcycle = 0
                DISPLAY.fill([int(colours[0]/3), int(colours[1]/3), int(colours[2]/3)])
                colourcycle += 1
            else: DISPLAY.blit(menuwallpaper, (0, 0))

            # menu text and images
            renderedText = mainfont.render('Welcome!', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))

            DISPLAY.blit(playbutton, ((width/2)-((width/14)*3), (height/6)*1.2))
            playrect = playbutton.get_rect().move((width/2)-((width/14)*3), (height/6)*1.2)
            DISPLAY.blit(settingsbutton, ((width/2)-((width/14)*3), (height/6)*1.9))
            settingsrect = settingsbutton.get_rect().move(((width/2)-((width/14)*3), (height/6)*1.9))
            DISPLAY.blit(statsbutton, ((width/2)-((width/14)*3), (height/6)*2.6))
            statsrect = statsbutton.get_rect().move(((width/2)-((width/14)*3), (height/6)*2.6))
            DISPLAY.blit(helpbutton, ((width/2)-((width/14)*3), (height/6)*3.3))
            helprect = helpbutton.get_rect().move(((width/2)-((width/14)*3), (height/6)*3.3))

            DISPLAY.blit(exitbutton, ((width/2)-((width/14)*3), height-(height/6)))
            exitrect = exitbutton.get_rect().move(((width/2)-((width/14)*3), height-(height/6)))

            # if pygame.mouse.get_pressed()[0] and singleplayer_image.collidepoint(mouse_pos):

            # keyboard input
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playrect.collidepoint(event.pos):
                        screen = 0
                        gameGen = False
                        inmenu = False
                    if settingsrect.collidepoint(event.pos):
                        screen = 2
                        gameGen = False
                        inmenu = False
                    if statsrect.collidepoint(event.pos):
                        screen = 3
                        gameGen = False
                        inmenu = False
                    if helprect.collidepoint(event.pos):
                        screen = 4
                        gameGen = False
                        inmenu = False
                    if exitrect.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                elif event.type==QUIT:
                    log('quitting')
                    pygame.quit()
                    exit()

            clock.tick(60)

            # restart music if it stops
            try:
                if pygame.mixer.music.get_busy() == False:
                    log('music finished, restarting')
                    pygame.mixer.music.play()
            except: pass

            try: pygame.display.update()
            except: pass


    # ----> OPTIONS <---
    elif screen == 2:

        inOptions = True
        reload = True
        
        while inOptions:

            # restart music if it stops
            try:
                if pygame.mixer.music.get_busy() == False:
                    log('music finished, restarting')
                    pygame.mixer.music.play()
            except: pass
            try: pygame.display.update()
            except: pass
            clock.tick(60)
            for event in pygame.event.get():
                if event.type==QUIT:
                    log('quitting')
                    pygame.quit()
                    gameopen = False
                    inOptions = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box1.collidepoint(event.pos): optionsBoxes[0][0] = True
                    if input_box2.collidepoint(event.pos): optionsBoxes[1][0] = True
                    if input_box3.collidepoint(event.pos): optionsBoxes[2][0] = True
                    if input_box4.collidepoint(event.pos):
                        options[3] = not options[3]
                        save_options()
                        if options[3]: status = 'Texture pack enabled'
                        else: status = 'Texture pack disabled'
                        optionsBoxes[3] = bool_to_humanreadable(options[3])
                    if options[3] and input_box5.collidepoint(event.pos): optionsBoxes[4][0] = True
                    if input_box6.collidepoint(event.pos): optionsBoxes[5][0] = True
                    if input_box7.collidepoint(event.pos): optionsBoxes[6][0] = True
                    if input_box8.collidepoint(event.pos): optionsBoxes[7][0] = True
                    if input_box9.collidepoint(event.pos):
                        options[5] = not options[5]
                        save_options()
                        if options[5]: status = 'Fullscreen mode enabled'
                        else: status = 'Fullscreen mode disabled'
                        optionsBoxes[8] = bool_to_humanreadable(options[5])
                    if exitrect.collidepoint(event.pos):
                        screen = 1
                        inOptions = False
                        reload = True
                    
                if event.type == pygame.KEYDOWN:
                    log('Key pressed')
                    if optionsBoxes[0][0]:
                        if event.key == pygame.K_RETURN:
                            log('Options box 0: '+str(optionsBoxes[0]))
                            if int(optionsBoxes[0][1]) >= 1 and int(optionsBoxes[0][1]) <= 3:
                                try:
                                    options[0] = int(optionsBoxes[0][1])
                                    save_options()
                                    status = 'Difficulty set to '+str(options[0])
                                    log('difficulty set to '+str(options[0]))
                                except:
                                    log('failed!')
                                    status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                    optionsBoxes[0][1] = str(options[0])
                            else:
                                optionsBoxes[0][1] = str(options[0])
                                status = 'Difficulty must be between 1 and 3.'
                            optionsBoxes[0][0] = False
                        elif event.key == pygame.K_1:
                            log('Options box 0: '+str(optionsBoxes[0]))
                            try:
                                options[0] = 1
                                save_options()
                                optionsBoxes[0][1] = '1'
                                status = 'Difficulty set to '+str(options[0])
                                log('difficulty set to '+str(options[0]))
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                optionsBoxes[0][1] = str(options[0])
                            optionsBoxes[0][0] = False
                        elif event.key == pygame.K_2:
                            log('Options box 0: '+str(optionsBoxes[0]))
                            try:
                                options[0] = 2
                                save_options()
                                optionsBoxes[0][1] = '2'
                                status = 'Difficulty set to '+str(options[0])
                                log('difficulty set to '+str(options[0]))
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                optionsBoxes[0][1] = str(options[0])
                            optionsBoxes[0][0] = False
                        elif event.key == pygame.K_3:
                            log('Options box 0: '+str(optionsBoxes[0]))
                            try:
                                options[0] = 3
                                save_options()
                                optionsBoxes[0][1] = '3'
                                status = 'Difficulty set to '+str(options[0])
                                log('difficulty set to '+str(options[0]))
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                optionsBoxes[0][1] = str(options[0])
                            optionsBoxes[0][0] = False
                        elif event.key == pygame.K_BACKSPACE: optionsBoxes[0][1] = optionsBoxes[0][1][:-1]

                    elif optionsBoxes[1][0]:
                        if event.key == pygame.K_RETURN:
                            log('Options box 1: '+str(optionsBoxes[1]))
                            try:
                                options[1] = optionsBoxes[1][1]
                                save_options()
                                log('username set to '+str(options[1]))
                                status = 'Username set to '+str(options[1])
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                optionsBoxes[1][1] = str(options[1])
                            optionsBoxes[1][0] = False
                        elif event.key == pygame.K_BACKSPACE: optionsBoxes[1][1] = optionsBoxes[1][1][:-1]
                        else: optionsBoxes[1][1] += event.unicode

                    elif optionsBoxes[2][0]:
                        if event.key == pygame.K_RETURN:
                            log('Options box 2: '+str(optionsBoxes[2]))
                            try:
                                temparray = optionsBoxes[2][1].split(', ')
                                options[2][0] = int(temparray[0])
                                options[2][1] = int(temparray[1])
                                options[2][2] = int(temparray[2])
                                save_options()
                                log('background colour set to '+str(options[2][0])+', '+str(options[2][1])+', '+str(options[2][2]))
                                status = 'Background colour set to '+str(options[2][0])+', '+str(options[2][1])+', '+str(options[2][2])
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                optionsBoxes[2][1] = str(options[2][0])+', '+str(options[2][1])+', '+str(options[2][2])
                            optionsBoxes[2][0] = False
                        elif event.key == pygame.K_BACKSPACE: optionsBoxes[2][1] = optionsBoxes[2][1][:-1]
                        else: optionsBoxes[2][1] += event.unicode

                    elif optionsBoxes[4][0] and options[3]:
                        if event.key == pygame.K_RETURN:
                            log('Options box 4: '+str(optionsBoxes[4]))
                            try:
                                options[4] = optionsBoxes[4][1]
                                save_options()
                                log('texture path set to '+str(options[4]))
                                status = 'Texture pack name set to '+str(optionsBoxes[4][1])
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                optionsBoxes[4][1] = str(options[4])
                            optionsBoxes[4][0] = False
                        elif event.key == pygame.K_BACKSPACE: optionsBoxes[4][1] = optionsBoxes[4][1][:-1]
                        else: optionsBoxes[4][1] += event.unicode

                    elif optionsBoxes[5][0]:
                        if event.key == pygame.K_RETURN:
                            log('Options box 5: '+str(optionsBoxes[5]))
                            try:
                                if int(optionsBoxes[5][1]) <= 100 and int(optionsBoxes[5][1]) >=0:
                                    try:
                                        options[6] = float(int(optionsBoxes[5][1])/100)
                                        save_options()
                                        log('master volume set to '+str(options[6]))
                                        status = 'Master volume set to '+str(optionsBoxes[5][1])
                                    except:
                                        log('failed!')
                                        status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                        optionsBoxes[5][1] = str(round(options[6]*100))
                                else:
                                    status = 'Please enter a number between 0 and 100.'
                                    optionsBoxes[5][1] = str(round(options[6]*100))
                            except:
                                status = 'Please enter a number between 0 and 100.'
                                optionsBoxes[5][1] = str(round(options[6]*100))
                            optionsBoxes[5][0] = False
                        elif event.key == pygame.K_BACKSPACE: optionsBoxes[5][1] = optionsBoxes[5][1][:-1]
                        elif event.key in numberkeys: optionsBoxes[5][1] += event.unicode

                    elif optionsBoxes[6][0]:
                        if event.key == pygame.K_RETURN:
                            log('Options box 6: '+str(optionsBoxes[6]))
                            try:
                                if int(optionsBoxes[6][1]) <= 100 and int(optionsBoxes[6][1]) >=0:
                                    try:
                                        options[7] = float(int(optionsBoxes[6][1])/100)
                                        save_options()
                                        log('music volume set to '+str(options[7]))
                                        status = 'Music volume set to '+str(optionsBoxes[6][1])
                                    except:
                                        log('failed!')
                                        status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                        optionsBoxes[6][1] = str(round(options[7]*100))
                                else:
                                    status = 'Please enter a number between 0 and 100.'
                                    optionsBoxes[6][1] = str(round(options[7]*100))
                            except:
                                status = 'Please enter a number between 0 and 100.'
                                optionsBoxes[6][1] = str(round(options[7]*100))
                            optionsBoxes[6][0] = False
                        elif event.key == pygame.K_BACKSPACE: optionsBoxes[6][1] = optionsBoxes[6][1][:-1]
                        elif event.key in numberkeys: optionsBoxes[6][1] += event.unicode

                    elif optionsBoxes[7][0]:
                        if event.key == pygame.K_RETURN:
                            log('Options box 7: '+str(optionsBoxes[7]))
                            try:
                                if int(optionsBoxes[7][1]) <= 100 and int(optionsBoxes[7][1]) >=0:
                                    try:
                                        options[8] = float(int(optionsBoxes[7][1])/100)
                                        save_options()
                                        log('death sound volume set to '+str(options[8]))
                                        status = 'Death sound volume set to '+str(optionsBoxes[7][1])
                                    except:
                                        log('failed!')
                                        status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                                        optionsBoxes[7][1] = str(round(options[8]*100))
                                else:
                                    status = 'Please enter a number between 0 and 100.'
                                    optionsBoxes[7][1] = str(round(options[8]*100))
                            except:
                                status = 'Please enter a number between 0 and 100.'
                                optionsBoxes[7][1] = str(round(options[8]*100))
                            optionsBoxes[7][0] = False
                        elif event.key == pygame.K_BACKSPACE: optionsBoxes[7][1] = optionsBoxes[7][1][:-1]
                        elif event.key in numberkeys: optionsBoxes[7][1] += event.unicode


            if menurainbow:
                # rainbow background
                if colourcycle >= 0 and colourcycle < 200: colours[0] = colours[0] + 1
                elif colourcycle >= 200 and colourcycle < 400: colours[2] = colours[2] - 1
                elif colourcycle >= 400 and colourcycle < 600: colours[1] = colours[1] + 1
                elif colourcycle >= 600 and colourcycle < 800: colours[0] = colours[0] - 1
                elif colourcycle >= 800 and colourcycle < 1000: colours[2] = colours[2] + 1
                elif colourcycle >= 1000 and colourcycle < 1200: colours[1] = colours[1] - 1
                elif colourcycle >= 1200: colourcycle = 0
                DISPLAY.fill([int(colours[0]/3), int(colours[1]/3), int(colours[2]/3)])
                colourcycle += 1
            else: DISPLAY.blit(menuwallpaper, (0, 0))

            # menu text and images
            renderedText = mainfont.render('Options', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))

            renderedText = smallfont.render('Changes will be applied after restart.', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, height/9))

            # exit button
            DISPLAY.blit(exitbutton, ((width/2)-((width/14)*3), height-(height/8)))
            exitrect = exitbutton.get_rect().move((width/2)-((width/14)*3), height-(height/8))

            # Options 1 - Difficulty
            renderedText = smallfont.render('Difficulty', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, height/6))
            input_box1 = pygame.Rect(width/22+renderedText.get_width()+(width/44), height/6, width/2, height/24)
            renderedText = smallfont.render(' '+optionsBoxes[0][1]+' ', True, (245, 245, 245))
            input_box1.w = max(350, renderedText.get_width()+10)
            DISPLAY.blit(renderedText, (input_box1.x+5, input_box1.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box1, 2)

            # Options 2 - Username
            renderedText = smallfont.render('Username', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2)))
            input_box2 = pygame.Rect(width/22+renderedText.get_width()+(width/44), (height/6)+(renderedText.get_height()*1.2), width/2, height/24)
            renderedText = smallfont.render(' '+optionsBoxes[1][1]+' ', True, (245, 245, 245))
            input_box2.w = max(350, renderedText.get_width()+10)
            DISPLAY.blit(renderedText, (input_box2.x+5, input_box2.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box2, 2)

            # Options 3 - Background colour
            renderedText = smallfont.render('Background colour', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*2)))
            input_box3 = pygame.Rect(width/22+renderedText.get_width()+(width/44), (height/6)+(renderedText.get_height()*1.2*2), width/2, height/24)
            renderedText = smallfont.render(' '+optionsBoxes[2][1]+' ', True, (245, 245, 245))
            input_box3.w = max(350, renderedText.get_width()+10)
            DISPLAY.blit(renderedText, (input_box3.x+5, input_box3.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box3, 2)

            # Options 4 - Texture pack toggle
            renderedText = smallfont.render('Texture pack on/off', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*3)))
            input_box4 = pygame.Rect(width/22+renderedText.get_width()+(width/44), (height/6)+(renderedText.get_height()*1.2*3), width/2, height/24)
            renderedText = smallfont.render(' '+optionsBoxes[3]+' ', True, (245, 245, 245))
            input_box4.w = max(350, renderedText.get_width()+10)
            DISPLAY.blit(renderedText, (input_box4.x+5, input_box4.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box4, 2)

            renderedText = smallfont.render('Texture pack name', True, (245, 245, 245))
            input_box5 = pygame.Rect(width/22+renderedText.get_width()+(width/44), (height/6)+(renderedText.get_height()*1.2*4), width/2, height/24)
            if options[3]:
                # Options 5 - Texture pack path
                DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*4)))
                renderedText = smallfont.render(' '+optionsBoxes[4][1]+' ', True, (245, 245, 245))
                input_box5.w = max(350, renderedText.get_width()+10)
                DISPLAY.blit(renderedText, (input_box5.x+5, input_box5.y+5))
                pygame.draw.rect(DISPLAY, (245, 245, 245), input_box5, 2)

                renderedText = smallfont.render('Press Escape to Restart the game & save your changes.', True, (245, 245, 245))
                DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*6)))
            else:
                renderedText = smallfont.render('Press Escape to Restart the game & save your changes.', True, (245, 245, 245))
                DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*5)))

            # Options 6 - Master volume (0-100)
            renderedText = smallfont.render('Master volume', True, (245, 245, 245))
            DISPLAY.blit(renderedText, ((width/2), (height/6)))
            input_box6 = pygame.Rect(renderedText.get_width()+(width/44)+(width/2), (height/6), width/2, height/24)
            renderedText = smallfont.render(' '+optionsBoxes[5][1]+' ', True, (245, 245, 245))
            input_box6.w = max(350, renderedText.get_width()+10)
            DISPLAY.blit(renderedText, (input_box6.x+5, input_box6.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box6, 2)

            # Options 7 - Music volume (0-100)
            renderedText = smallfont.render('Music volume', True, (245, 245, 245))
            DISPLAY.blit(renderedText, ((width/2), (height/6)+(renderedText.get_height()*1.2)))
            input_box7 = pygame.Rect(renderedText.get_width()+(width/44)+(width/2), (height/6)+(renderedText.get_height()*1.2), width/2, height/24)
            renderedText = smallfont.render(' '+optionsBoxes[6][1]+' ', True, (245, 245, 245))
            input_box7.w = max(350, renderedText.get_width()+10)
            DISPLAY.blit(renderedText, (input_box7.x+5, input_box7.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box7, 2)

            # Options 8 - Death sound volume (0-100)
            renderedText = smallfont.render('Death sound volume', True, (245, 245, 245))
            DISPLAY.blit(renderedText, ((width/2), (height/6)+(renderedText.get_height()*1.2*2)))
            input_box8 = pygame.Rect(renderedText.get_width()+(width/44)+(width/2), (height/6)+(renderedText.get_height()*1.2*2), width/2, height/24)
            renderedText = smallfont.render(' '+optionsBoxes[7][1]+' ', True, (245, 245, 245))
            input_box8.w = max(350, renderedText.get_width()+10)
            DISPLAY.blit(renderedText, (input_box8.x+5, input_box8.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box8, 2)

            # Options 9 - Fullscreen toggle
            renderedText = smallfont.render('Fullscreen', True, (245, 245, 245))
            DISPLAY.blit(renderedText, ((width/2), (height/6)+(renderedText.get_height()*1.2*3)))
            input_box9 = pygame.Rect(renderedText.get_width()+(width/44)+(width/2), (height/6)+(renderedText.get_height()*1.2*3), width/2, height/24)
            renderedText = smallfont.render(' '+optionsBoxes[8]+' ', True, (245, 245, 245))
            input_box9.w = max(350, renderedText.get_width()+10)
            DISPLAY.blit(renderedText, (input_box9.x+5, input_box9.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box9, 2)

            renderedText = smallfont.render(status, True, (245, 245, 245))
            DISPLAY.blit(renderedText, ((width/2)-(renderedText.get_width()/2), height-(height/22)))

            # keyboard input
            keys = pygame.key.get_pressed()
            # if keys[pygame.K_p]: screen = 1
            if keys[pygame.K_TAB]:
                screen = 5
                inOptions = False
                reload = False

        if reload:
            if options[3]: # load custom textures (if enabled)
                log('using custom textures')

                # Player texture
                try:
                    player = pygame.image.load('userfiles/textures/'+options[4]+'/player.png')
                    log('player texture imported')
                except:
                    player = pygame.image.load(assetspath+'defaultTextures/player.png')
                    log('player texture not found, using default')

                # Enemy texture
                try:
                    enemytex = pygame.image.load('userfiles/textures/'+options[4]+'/enemy.png')
                    log('enemy texture imported')
                except:
                    enemytex = pygame.image.load(assetspath+'defaultTextures/enemy.png')
                    log('enemy texture not found, using default')

                # settingsbutton texture
                try:
                    settingsbutton = pygame.image.load('userfiles/textures/'+options[4]+'/options.png')
                    log('settingsbutton texture imported')
                except:
                    settingsbutton = pygame.image.load(assetspath+'defaultTextures/options.png')
                    log('settingsbutton texture not found, using default')

                # menubutton texture
                try:
                    menubutton = pygame.image.load('userfiles/textures/'+options[4]+'/menu.png')
                    log('menubutton texture imported')
                except:
                    menubutton = pygame.image.load(assetspath+'defaultTextures/menu.png')
                    log('menubutton texture not found, using default')

                # exitbutton texture
                try:
                    exitbutton = pygame.image.load('userfiles/textures/'+options[4]+'/exit.png')
                    log('exitbutton texture imported')
                except:
                    exitbutton = pygame.image.load(assetspath+'defaultTextures/exit.png')
                    log('exitbutton texture not found, using default')

                # statsbutton texture
                try:
                    statsbutton = pygame.image.load('userfiles/textures/'+options[4]+'/stats.png')
                    log('statsbutton texture imported')
                except:
                    statsbutton = pygame.image.load(assetspath+'defaultTextures/stats.png')
                    log('statsbutton texture not found, using default')

                # playbutton texture
                try:
                    playbutton = pygame.image.load('userfiles/textures/'+options[4]+'/play.png')
                    log('playbutton texture imported')
                except:
                    playbutton = pygame.image.load(assetspath+'defaultTextures/play.png')
                    log('playbutton texture not found, using default')

                # helpbutton texture
                try:
                    helpbutton = pygame.image.load('userfiles/textures/'+options[4]+'/help.png')
                    log('helpbutton texture imported')
                except:
                    helpbutton = pygame.image.load(assetspath+'defaultTextures/help.png')
                    log('helpbutton texture not found, using default')

                # Menu texture
                try:
                    menuwallpaper = pygame.image.load('userfiles/textures/'+options[4]+'/menu.png')
                    menurainbow = False
                    log('menu texture imported')
                except:
                    menurainbow = True
                    log('menu texture not found, using rainbow')

                # Game texture
                try:
                    gamewallpaper = pygame.image.load('userfiles/textures/'+options[4]+'/game.png')
                    gamerainbow = False
                    log('game texture imported')
                except:
                    gamerainbow = True
                    log('game texture not found, using rainbow')

                # Music
                try:
                    pygame.mixer.music.load('userfiles/textures/'+options[4]+'/music.mp3')
                    log('music imported')
                except:
                    pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
                    log('music not found, using default')

                # Death sound
                try:
                    deathSound = pygame.mixer.Sound('userfiles/textures/'+options[4]+'/death.mp3')
                    log('death sound imported')
                except:
                    deathSound = pygame.mixer.Sound(assetspath+'defaultTextures/death.mp3')
                    log('death sound not found, using default')

                # Main font
                try:
                    mainfont = pygame.font.Font('userfiles/textures/'+options[4]+'/font.ttf', int((width/640)*32))
                    log('main font imported')
                except:
                    mainfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((width/640)*32))
                    log('main font not found, using default')

                # Small font
                try:
                    smallfont = pygame.font.Font('userfiles/textures/'+options[4]+'/smallfont.ttf', int((width/640)*12))
                    log('small font imported')
                except:
                    smallfont = pygame.font.Font(assetspath+'defaultTextures/smallfont.ttf', int((width/640)*12))
                    log('small font not found, using default')

            else: # import default textures if texture packs are disabled
                log('using default textures')
                player = pygame.image.load(assetspath+'defaultTextures/player.png')
                enemytex = pygame.image.load(assetspath+'defaultTextures/enemy.png')
                pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
                deathSound = pygame.mixer.Sound(assetspath+'defaultTextures/death.mp3')
                mainfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((width/640)*32))
                smallfont = pygame.font.Font(assetspath+'defaultTextures/smallfont.ttf', int((width/640)*12))
                settingsbutton = pygame.image.load(assetspath+'defaultTextures/options.png')
                menubutton = pygame.image.load(assetspath+'defaultTextures/menu.png')
                exitbutton = pygame.image.load(assetspath+'defaultTextures/exit.png')
                statsbutton = pygame.image.load(assetspath+'defaultTextures/stats.png')
                playbutton = pygame.image.load(assetspath+'defaultTextures/play.png')
                helpbutton = pygame.image.load(assetspath+'defaultTextures/help.png')

            # resize textures for window size
            player = pygame.transform.scale(player, (playersize, playersize))
            enemytex = pygame.transform.scale(enemytex, (playersize, playersize))
            settingsbutton = pygame.transform.scale(settingsbutton, (round(width/14)*6, round(width/14)*0.75))
            menubutton = pygame.transform.scale(menubutton, (round(width/14)*6, round(width/14)*0.75))
            exitbutton = pygame.transform.scale(exitbutton, (round(width/14)*6, round(width/14)*0.75))
            statsbutton = pygame.transform.scale(statsbutton, (round(width/14)*6, round(width/14)*0.75))
            playbutton = pygame.transform.scale(playbutton, (round(width/14)*6, round(width/14)*0.75))
            helpbutton = pygame.transform.scale(helpbutton, (round(width/14)*6, round(width/14)*0.75))
            if not menurainbow: menuwallpaper = pygame.transform.scale(menuwallpaper, (width, height))
            if not gamerainbow: gamewallpaper = pygame.transform.scale(gamewallpaper, (width, height))

            # sound stuff
            deathSound.set_volume(options[8]*options[6])
            pygame.mixer.music.set_volume(options[7]*options[6])

    # -----> STATS <----
    elif screen == 3:

        if menurainbow:
            # rainbow background
            if colourcycle >= 0 and colourcycle < 200: colours[0] = colours[0] + 1
            elif colourcycle >= 200 and colourcycle < 400: colours[2] = colours[2] - 1
            elif colourcycle >= 400 and colourcycle < 600: colours[1] = colours[1] + 1
            elif colourcycle >= 600 and colourcycle < 800: colours[0] = colours[0] - 1
            elif colourcycle >= 800 and colourcycle < 1000: colours[2] = colours[2] + 1
            elif colourcycle >= 1000 and colourcycle < 1200: colours[1] = colours[1] - 1
            elif colourcycle >= 1200: colourcycle = 0
            DISPLAY.fill([int(colours[0]/3), int(colours[1]/3), int(colours[2]/3)])
            colourcycle += 1
        else: DISPLAY.blit(menuwallpaper, (0, 0))
        
        # menu text and images
        renderedText = mainfont.render('Stats', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))
        try:
            renderedText = smallfont.render('Difficulty 1', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, height/6))
            renderedText = smallfont.render('Highscore: '+str(savedata[0]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*1)))
            renderedText = smallfont.render('Date: '+str(savedata[2]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*2)))
        except: pass
        try:
            renderedText = smallfont.render('Difficulty 2', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*3.5)))
            renderedText = smallfont.render('Highscore: '+str(savedata[0]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*4.5)))
            renderedText = smallfont.render('Date: '+str(savedata[2]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*5.5)))
        except: pass
        try:
            renderedText = smallfont.render('Difficulty 3', True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*7)))
            renderedText = smallfont.render('Highscore: '+str(savedata[0]), True, (245, 245, 245))
            DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*8)))
            renderedText = smallfont.render('Date: '+str(savedata[2]), True, (245, 245, 245))
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

        if menurainbow:
            # rainbow background
            if colourcycle >= 0 and colourcycle < 200: colours[0] = colours[0] + 1
            elif colourcycle >= 200 and colourcycle < 400: colours[2] = colours[2] - 1
            elif colourcycle >= 400 and colourcycle < 600: colours[1] = colours[1] + 1
            elif colourcycle >= 600 and colourcycle < 800: colours[0] = colours[0] - 1
            elif colourcycle >= 800 and colourcycle < 1000: colours[2] = colours[2] + 1
            elif colourcycle >= 1000 and colourcycle < 1200: colours[1] = colours[1] - 1
            elif colourcycle >= 1200: colourcycle = 0
            DISPLAY.fill([int(colours[0]/3), int(colours[1]/3), int(colours[2]/3)])
            colourcycle += 1
        else: DISPLAY.blit(menuwallpaper, (0, 0))

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

        if menurainbow:
            # rainbow background
            if colourcycle >= 0 and colourcycle < 200: colours[0] = colours[0] + 1
            elif colourcycle >= 200 and colourcycle < 400: colours[2] = colours[2] - 1
            elif colourcycle >= 400 and colourcycle < 600: colours[1] = colours[1] + 1
            elif colourcycle >= 600 and colourcycle < 800: colours[0] = colours[0] - 1
            elif colourcycle >= 800 and colourcycle < 1000: colours[2] = colours[2] + 1
            elif colourcycle >= 1000 and colourcycle < 1200: colours[1] = colours[1] - 1
            elif colourcycle >= 1200: colourcycle = 0
            DISPLAY.fill([int(colours[0]/3), int(colours[1]/3), int(colours[2]/3)])
            colourcycle += 1
        else: DISPLAY.blit(menuwallpaper, (0, 0))

        # menu text and images
        renderedText = mainfont.render('Options help', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/2 - renderedText.get_width()/2, 10))

        renderedText = smallfont.render('To edit a value, click in the box next to it, and change it\'s value by typing a new one.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*1)))

        renderedText = smallfont.render('Press enter to submit.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*2)))

        renderedText = smallfont.render('When editing the Difficulty value, Press 1, 2, or 3. You don\'t need to press enter.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*3.5)))

        renderedText = smallfont.render('When editing the Background value, type 3 numbers that are above 0 and less than 255, ', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*5)))

        renderedText = smallfont.render('seperated by commas (e.g. 45, 255, 0).', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*6)))

        renderedText = smallfont.render('Click a toggle (on/off) to toggle it.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*7.5)))

        renderedText = smallfont.render('Any volume fields can be any whole number between 0 and 100.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, (height/6)+(renderedText.get_height()*1.2*9)))

        renderedText = smallfont.render('Press P to return to the options menu, or 1 to return to the main menu.', True, (245, 245, 245))
        DISPLAY.blit(renderedText, (width/22, height-renderedText.get_height()*2))

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