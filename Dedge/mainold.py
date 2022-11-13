import pygame, sys, pickle, time, datetime, shutil, os
from pygame.locals import *
from pygame.time import Clock
from time import sleep
from random import randint
from screeninfo import get_monitors

assetspath = "assets"
ufpath = "userfiles"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_fs():
    try:
        with open (assetspath+'fs', 'rb') as f:
            array = pickle.load(f)
            return array
    except:
        return(False)

def save_fs(input):
    with open (assetspath+'fs', 'wb') as f:
        pickle.dump(input, f)
try:
    saved_fs = load_fs()
except:
    save_fs()
    try:
        saved_fs = load_fs(False)
    except:
        saved_fs = False

# WARNING: ENABLING THIS WILL MAKE LOG.TXT GROW IN SIZE INCREDIBLY QUICKLY. (around 1 megabyte every 15 seconds the game is running.) ONLY TURN THIS ON IF YOU ARE WILLING TO SACRIFICE YOUR DISK SPACE.
extreme = False

# logging functions (log() and xtr())
def log(content:str):
    newcontent = '[game.py] - '+time.asctime(time.localtime(time.time())) +': '+str(content)
    with open (assetspath+'log.txt', 'at') as f:
        f.write(newcontent+'\n')
    print(newcontent)
def xtr(content:str):
    if extreme:
        newcontent = '[game.py] [XTR] - '+time.asctime(time.localtime(time.time())) +': '+content
        with open (assetspath+'log.txt', 'at') as f:
            f.write(newcontent+'\n')
        print(newcontent)

# clear log.txt
def clearlog():
    with open (assetspath+'log.txt', 'wt') as f:
        f.write('')
    log('log.txt cleared.')

clearlog()

# datetime function
def date(): return(str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))

log('setting up dev stuff, if enabled in code...')
devstuffenabled = False
def devstuff():
    try:
        if devstuffenabled:
            log('\n\ndev mode enabled')
            action = input('What would you like to do?\n1. Delete save files\n2. Reset save files\n3. Customize save files\n4. Save log\n5. View save files\n6. Clear savebackups\n7. Clear all userfiles subfolders\n8. Prepare for sending\n9: Exit\n\n')
            if int(action) < 6 and int(action) > 0:
                log('copying save files')
                try:
                    shutil.copyfile(assetspath+'options.sf', assetspath+'dev/options.sf')
                    log('copied options file')
                except:
                    log('failed to copy options file')
                try:
                    shutil.copyfile(assetspath+'save.sf', assetspath+'dev/save.sf')
                    log('copied save file')
                except:
                    log('failed to copy save file')
                log('finished copying files, running appropriate script')
            if action == '1':
                try:
                    os.remove(assetspath+'options.sf')
                except:
                    log('failed to delete options file')
                try:
                    os.remove(assetspath+'save.sf')
                except:
                    log('failed to delete save file')
                log('done!')
            elif action == '2':
                with open (assetspath+'options.sf', 'wb') as f:
                    options = [640, 360, 1, 'OptReset1', 12, 12, 12, False, assetspath+'defaultTextures/']
                    pickle.dump(options, f)
                with open (assetspath+'save.sf', 'wb') as f:
                    savedata = [0, 1]
                    pickle.dump(savedata, f)
            elif action == '3':
                options0 = input('Enter window width (int): ')
                options1 = input('Enter window height (int): ')
                options2 = input('Enter difficulty (int): ')
                options3 = input('Enter username (str): ')
                options4 = input('Enter red background value (int): ')
                options5 = input('Enter green background value (int): ')
                options6 = input('Enter blue background value (int): ')
                options7 = input('Enter texture toggle (bool): ')
                options8 = input('Enter texture folder (str): ')
                with open (assetspath+'options.sf', 'wb') as f:
                    options = [int(options0), int(options1), int(options2), options3, int(options4), int(options5), int(options6), bool(options7), options8]
                    pickle.dump(options, f)
                save0 = input('Enter highscore (int): ')
                save1 = input('Enter difficulty (int): ')
                save2 = input('Enter date (str): ')
                with open (assetspath+'save.sf', 'wb') as f:
                    savedata = [int(save0), int(save1), str(save2)]
                    pickle.dump(savedata, f)
            elif action == '4':
                temp = date()
                shutil.copyfile(assetspath+'log.txt', assetspath+'logs/'+temp+'.txt')
            elif action == '5':
                log('options file:\n'+str(load_options())+'\nsave file:\n'+str(load_save()))
            elif action == '6':
                shutil.rmtree(ufpath+'savebackups')
                os.mkdir(ufpath+'savebackups')
                log('done!')
            elif action == '7':
                shutil.rmtree(ufpath+'savebackups')
                os.mkdir(ufpath+'savebackups')
                shutil.rmtree(ufpath+'textures')
                os.mkdir(ufpath+'textures')
                log('done!')
            elif action == '8':
                with open (assetspath+'options.sf', 'wb') as f:
                    options = [640, 360, 1, 'UnnamedPlayer8376', 12, 12, 12, False, assetspath+'defaultTextures/']
                    pickle.dump(options, f)
                log('reset options file')
                with open (assetspath+'save.sf', 'wb') as f:
                    savedata = [0, 1]
                    pickle.dump(savedata, f)
                log('reset save file')
                shutil.rmtree(ufpath+'savebackups')
                os.mkdir(ufpath+'savebackups')
                log('emptied user save backups')
                shutil.rmtree(ufpath+'textures')
                os.mkdir(ufpath+'textures')
                log('emptied user texture files')
                shutil.rmtree(assetspath+'logs')
                os.mkdir(assetspath+'logs')
                log('removed log files')
                try:
                    os.remove(assetspath+'dev/options.sf')
                    log('removed temp dev options file')
                except:
                    log('failed to delete temp dev options file, it probably didn\'t exist')
                try:
                    os.remove(assetspath+'dev/save.sf')
                    log('removed temp dev save file')
                except:
                    log('failed to delete temp dev save file, it probably didn\'t exist')
                with open (assetspath+'log.txt', 'wt') as f:
                    f.write('\n')
                log('emptied log file')
            elif action == '9':
                sys.exit()
    except:
        return(1)

log('setting up save/load functions')
def load_options():
    with open (assetspath+'options.sf', 'rb') as f:
        array = pickle.load(f)
        return array
def load_save():
    with open (assetspath+'save.sf', 'rb') as f:
        array = pickle.load(f)
        return array
def save_options():
    with open (assetspath+'options.sf', 'wb') as f:
        pickle.dump(options, f)
def save_save():
    with open (assetspath+'save.sf', 'wb') as f:
        pickle.dump(savedata, f)

log('loading files...')
# load options file
try:
    options = load_options()
    log('options loaded!')
except:
    log('Failed to load options - starting afresh with following values:')
    options = [640, 360, 5, 'UnnamedPlayer'+str(randint(1000, 9999)), 12, 12, 12, assetspath+'defaultTextures/']
    try:
        save_options()
    except:
        log(options)

# load save file
try:
    savedata = load_save()
    log('save data loaded!')
except:
    log('Failed to import data - starting afresh with following values:')
    savedata = ['0', '0']
    log(savedata)

# set screen resoltuion
def screenRes():
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
        else:
            log("not primary monitor, checking for other monitors...")
    if primaryFound:
        log('returning dimensions of primary monitor...')
        return(int(primaryWidth), int(primaryHeight))
    else:
        log("unable to find primary monitor's screen resolution, using default of 640x360.")
        return(640, 360)
primaryDimensions = screenRes()
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

def menu():
    try:
        # setup stuff
        inMenu = True
        log('initialising pygame, variables and clock')
        pygame.init()
        pygame.mixer.init()
        playersize = (width/640)*32
        clock = Clock()
        log('creating window')
        DISPLAY = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption(game_name)
        log('importing textures, other assets, and other visual stuff')
        BLUE = (55, 55, 55)

        # if custom textures are enabled, load them. otherwise, use default textures.
        if options[7] == True:
            log('using custom textures')
            try:
                pygame.mixer.music.load(options[8]+'music.mp3')
                log('music imported')
            except:
                pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
                log('music not found, using default')
            try:
                font = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*32))
                log('font imported')
            except:
                font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
                log('font not found, using default')
            try:
                smallfont = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*12))
                log('font imported')
            except:
                smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))
                log('font not found, using default')
        else:
            log('using default textures')

            pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
            font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
            smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))

        appicon = pygame.image.load(assetspath+'defaultTextures/appicon.png')
        corner = pygame.image.load(assetspath+'defaultTextures/corner.png')

        # set app icon
        pygame.display.set_icon(appicon)

        # resize player + enemy textures for window size
        corner = pygame.transform.scale(corner, (int(windowwidth/8), int(windowwidth/8)))

        # music stuff
        pygame.mixer.music.set_volume(0.3)
        log('starting music')
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
            log('music started')
        else:
            log('music already playing, cancelling')

        colourcycle = 0

        r = 55
        g = 55
        b = 255

        while inMenu:
            clock.tick(60)

            # colour display with rainbow colour
            DISPLAY.fill(BLUE)

            # quit
            for event in pygame.event.get():
                if event.type==QUIT:
                    log('quitting')
                    pygame.quit()
                    return(0)
            
            # restart music if it stops
            if pygame.mixer.music.get_busy() == False:
                log('music finished, restarting')
                pygame.mixer.music.play()

            # keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                pygame.quit()
                return(2)
            if keys[pygame.K_2]:
                pygame.quit()
                return(3)
            if keys[pygame.K_3]:
                pygame.quit()
                return(4)
            if keys[pygame.K_4]:
                pygame.quit()
                return(5)
            if keys[pygame.K_5]:
                try:
                    os.remove(ufpath+'options.sf')
                    os.remove(ufpath+'save.sf')
                except:
                    pass
                shutil.copyfile(assetspath+'options.sf', ufpath+'options.sf')
                shutil.copyfile(assetspath+'save.sf', ufpath+'save.sf')
                while keys[pygame.K_5]:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        pygame.quit()
                        return(0)
            if keys[pygame.K_6]:
                os.remove(assetspath+'options.sf')
                os.remove(assetspath+'save.sf')
                shutil.copyfile(ufpath+'options.sf', assetspath+'options.sf')
                shutil.copyfile(ufpath+'save.sf', assetspath+'save.sf')
                while keys[pygame.K_6]:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        pygame.quit()
                        return(0)
            if keys[pygame.K_7]:
                pygame.quit()
                return(8)

            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return(0)

            # rainbow background
            if colourcycle >= 0 and colourcycle <= 200:
                r = r+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 200 and colourcycle <= 400:
                b = b-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 400 and colourcycle <= 600:
                g = g+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 600 and colourcycle <= 800:
                r = r-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 800 and colourcycle <= 1000:
                b = b+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 1000 and colourcycle <= 1200:
                g = g-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle > 1200:
                colourcycle = 0
            colourcycle = colourcycle+1
            
            # menu text and images
            welcome = font.render('Welcome!', True, (245, 245, 245))
            DISPLAY.blit(welcome, (width/2 - welcome.get_width()/2, 10))
            key = smallfont.render('Press a number on your keyboard to begin.', True, (245, 245, 245))
            DISPLAY.blit(key, (width/2 - key.get_width()/2, height/9))
            optionstext = smallfont.render('1 - Launch Game', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, height/6))
            optionstext = smallfont.render('2 - Edit Options', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2)))
            optionstext = smallfont.render('3 - View Stats', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*2)))
            optionstext = smallfont.render('4 - View Controls', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*3)))
            optionstext = smallfont.render('5 - Backup save files', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*4)))
            optionstext = smallfont.render('6 - Restore save files', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*5)))
            optionstext = smallfont.render('Press Escape to Exit', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*7)))
            DISPLAY.blit(corner, (width-corner.get_width(), height-corner.get_height()))

            pygame.display.update()
    except:
        return(1)

def game():
    try:
        inGame = True

        # get difficulty from options, or use default of 5
        try:
            difficulty = options[2]
            log('using difficulty from options.sf')
        except:
            difficulty = 5
            log('no difficulty specified, using default: 5')
        log('difficulty: '+str(difficulty))

        log('creating class enemy')
        class Enemy():
            def __init__(enemy, x, y):
                enemy.enemyxpos = x
                enemy.enemyypos = y
        log('class enemy created!')

        log('initialising pygame, variables and clock')
        pygame.init()
        pygame.mixer.init()

        score = 0
        playersize = (width/640)*32
        xpos = width/2 - playersize/2
        ypos = height/2 - playersize/2

        enemiesDown = []
        enemiesLeft = []
        enemiesUp = []
        enemiesRight = []

        isLeft = False
        isRight = False
        isUp = False

        clock = Clock()

        log('creating window')
        DISPLAY = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption(game_name)


        log('importing textures, other assets, and other visual stuff')
        BLUE = (int(options[4]), int(options[5]), int(options[6]))

        # if custom textures are enabled, import them. otherwise, use default textures
        if options[7] == True:
            log('using custom textures')
            try:
                player = pygame.image.load(options[8]+'player.png')
                log('player texture imported')
            except:
                player = pygame.image.load(assetspath+'defaultTextures/player.png')
                log('player texture not found, using default')
            try:
                playerGlow = pygame.image.load(options[8]+'playerGlow.png')
                log('playerGlow texture imported')
            except:
                playerGlow = pygame.image.load(assetspath+'defaultTextures/playerGlow.png')
                log('playerGlow texture not found, using default')
            try:
                enemytex = pygame.image.load(options[8]+'enemy.png')
                log('enemy texture imported')
            except:
                enemytex = pygame.image.load(assetspath+'defaultTextures/enemy.png')
                log('enemy texture not found, using default')
            try:
                enemyGlow = pygame.image.load(options[8]+'enemyGlow.png')
                log('enemyGlow texture imported')
            except:
                enemyGlow = pygame.image.load(assetspath+'defaultTextures/enemyGlow.png')
                log('enemyGlow texture not found, using default')
            try:
                pygame.mixer.music.load(options[8]+'music.mp3')
                log('music imported')
            except:
                pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
                log('music not found, using default')
            try:
                font = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*32))
                log('font imported')
            except:
                font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
                log('font not found, using default')
            appicon = pygame.image.load(assetspath+'defaultTextures/appicon.png') 
        else:
            log('using default textures')

            player = pygame.image.load(assetspath+'defaultTextures/player.png')
            playerGlow = pygame.image.load(assetspath+'defaultTextures/playerGlow.png')
            enemytex = pygame.image.load(assetspath+'defaultTextures/enemy.png')
            enemyGlow = pygame.image.load(assetspath+'defaultTextures/enemyGlow.png')
            pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
            font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
            appicon = pygame.image.load(assetspath+'defaultTextures/appicon.png')

        # set the icon for the game
        pygame.display.set_icon(appicon)

        # resize textures for display scaling
        player = pygame.transform.scale(player, (playersize, playersize))
        playerGlow = pygame.transform.scale(playerGlow, (playersize*1.25, playersize*1.25))
        enemytex = pygame.transform.scale(enemytex, (playersize, playersize))
        enemyGlow = pygame.transform.scale(enemyGlow, (playersize*1.25, playersize*1.25))

        # music stuff
        pygame.mixer.music.set_volume(0.3)
        log('starting music')
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
            log('music started')
        else:
            log('music already playing, cancelling')

        log('creating initial enemies')
        for i in range(difficulty):
            enemiesDown.append(Enemy(randint(0, int(width-playersize)), randint(int((0-playersize)*8), int(0-playersize))))

        log('entering main loop')
        while inGame:
            clock.tick(60)

            # enable other directions for enemies at the appropriate times
            if score >= 25 and isUp == False:
                for i in range(difficulty):
                    enemiesUp.append(Enemy(randint(0, int(width-playersize)), randint(height, int(height+playersize*8))))
                isUp = True
            if score >= 50 and isLeft == False:
                for i in range(difficulty):
                    enemiesLeft.append(Enemy(randint(width, int(width+playersize*8)), randint(0, int(height-playersize))))
                isLeft = True
            if score >= 75 and isRight == False:
                for i in range(difficulty):
                    enemiesRight.append(Enemy(randint(int(0-playersize)*8, int(0-playersize)), randint(0, int(height-playersize))))
                isRight = True

            # setup speeds - player moves slightly faster than enemies
            speed = (score/30 + (windowwidth/640)*3)+1.5
            enemyspeed = ((score/30 + (windowwidth/640))/2.5)+1.5

            # quit
            for event in pygame.event.get():
                if event.type==QUIT:
                    log('quitting')
                    pygame.quit()
                    return(1)
                    
            # loop music
            if pygame.mixer.music.get_busy() == False:
                log('music finished, restarting')
                pygame.mixer.music.play()

            # keybinds
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                if xpos < width-playersize:
                    xpos = xpos + speed
                    xtr('moving right')
            if keys[pygame.K_a]:
                if xpos > 0:
                    xpos = xpos - speed
                    xtr('moving left')
            if keys[pygame.K_w]:
                if ypos > 0:
                    ypos = ypos - speed
                    xtr('moving up')
            if keys[pygame.K_s]:
                if ypos < height-playersize:
                    ypos = ypos + speed
                    xtr('moving down')
            if keys[pygame.K_l] and keys[pygame.K_z]:
                pygame.quit()
                return(6)
            if keys[pygame.K_RIGHT]:
                if xpos < width-playersize:
                    xpos = xpos + speed
                    xtr('moving right')
            if keys[pygame.K_LEFT]:
                if xpos > 0:
                    xpos = xpos - speed
                    xtr('moving left')
            if keys[pygame.K_UP]:
                if ypos > 0:
                    ypos = ypos - speed
                    xtr('moving up')
            if keys[pygame.K_DOWN]:
                if ypos < height-playersize:
                    ypos = ypos + speed
                    xtr('moving down')
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return(1)
                
            xtr('drawing background and player')
            DISPLAY.fill([int(options[4]), int(options[5]), int(options[6])])
            DISPLAY.blit(playerGlow, ((xpos-playersize*0.125, ypos-playersize*0.125)))
            DISPLAY.blit(player, (xpos, ypos))
        
            xtr('drawing enemies (down)')
            for enemy in enemiesDown:
                xtr('checking enemy status')
                if enemy.enemyypos > height:
                    enemy.enemyypos = randint(int((0-playersize)*8), int(0-playersize))
                    enemy.enemyxpos = randint(0, int(width-playersize))
                    score = score + 1
                    log('enemy moved to top, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.enemyxpos)+', '+str(enemy.enemyypos))
                else:
                    enemy.enemyypos = enemy.enemyypos + enemyspeed
                    xtr('enemy moved down')

                DISPLAY.blit(enemyGlow, ((enemy.enemyxpos-playersize*0.125, enemy.enemyypos-playersize*0.125)))
                DISPLAY.blit(enemytex, (enemy.enemyxpos, enemy.enemyypos))
                xtr('enemy drawn')

                if xpos+playersize > enemy.enemyxpos and xpos < enemy.enemyxpos+playersize and ypos+playersize > enemy.enemyypos and ypos < enemy.enemyypos+playersize:
                
                    clock.tick(60)
                        
                    log('rendering death screen - final score: '+str(score)+' - difficulty: '+str(difficulty)+' - highscore: '+str(savedata[0]))
                    DISPLAY.fill(BLUE)
                    endtext = font.render('Your score was '+str(score), True, (255-BLUE[0], 255-BLUE[1], 255-BLUE[2]))
                    DISPLAY.blit(endtext, (width/2 - endtext.get_width()/2, 10))
                    highscore = font.render('Your highscorescore is '+str(savedata[0]), True, (255-BLUE[0], 255-BLUE[1], 255-BLUE[2]))
                    DISPLAY.blit(highscore, (width/2 - highscore.get_width()/2, height-10-highscore.get_height()))
                    pygame.display.update()

                    if score > int(savedata[0]) and difficulty >= int(savedata[1]):
                        log('new highscore! saving to save.sf...')
                        savedata[0] = str(score)
                        savedata[1] = str(difficulty)
                        temp = date()
                        savedata[2] = temp
                        save_save()
                        log('save complete')

                    elif score > int(savedata[0])+15:
                        log('new highscore! saving to save.sf...')
                        savedata[0] = str(score)
                        savedata[1] = str(difficulty)
                        temp = date()
                        savedata[2] = temp
                        save_save()
                        log('save complete')

                    log('recording score in savefile...')
                    savedata.append(str(score))
                    savedata.append(str(difficulty))
                    temp = date()
                    savedata[2] = temp
                    save_save()
                    log('save complete')

                    log('waiting 4 seconds')
                    sleep(4)

                    return(2)

            xtr('drawing enemies (up)')        
            if isUp:
                for enemy in enemiesUp:
                    xtr('checking enemy status')
                    if enemy.enemyypos < 0-playersize:
                        enemy.enemyypos = randint(height, int(height+(playersize*8)))
                        enemy.enemyxpos = randint(0, int(width-playersize))
                        score = score + 1
                        log('enemy moved to bottom, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.enemyxpos)+', '+str(enemy.enemyypos))
                    else:
                        enemy.enemyypos = enemy.enemyypos - enemyspeed
                        xtr('enemy moved up')

                    DISPLAY.blit(enemyGlow, ((enemy.enemyxpos-playersize*0.125, enemy.enemyypos-playersize*0.125)))
                    DISPLAY.blit(enemytex, (enemy.enemyxpos, enemy.enemyypos))
                    xtr('enemy drawn')

                    if xpos+playersize > enemy.enemyxpos and xpos < enemy.enemyxpos+playersize and ypos+playersize > enemy.enemyypos and ypos < enemy.enemyypos+playersize:
                    
                        clock.tick(60)
                            
                        log('rendering death screen')
                        DISPLAY.fill(BLUE)
                        endtext = font.render('Your score was '+str(score), True, (255-BLUE[0], 255-BLUE[1], 255-BLUE[2]))
                        DISPLAY.blit(endtext, (width/2 - endtext.get_width()/2, 10))
                        highscore = font.render('Your highscorescore is '+str(savedata[0]), True, (255-BLUE[0], 255-BLUE[1], 255-BLUE[2]))
                        DISPLAY.blit(highscore, (width/2 - highscore.get_width()/2, height-10-highscore.get_height()))
                        pygame.display.update()

                        if score > int(savedata[0]) and difficulty >= int(savedata[1]):
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            temp = date()
                            savedata[2] = temp
                            save_save()
                            log('save complete')

                        elif score > int(savedata[0])+15:
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            temp = date()
                            savedata[2] = temp
                            save_save()
                            log('save complete')

                        log('recording score in savefile...')
                        savedata.append(str(score))
                        savedata.append(str(difficulty))
                        temp = date()
                        savedata[2] = temp
                        save_save()
                        log('save complete')

                        log('waiting 4 seconds')
                        sleep(4)

                        return(2)
        
            xtr('drawing enemies (left)')
            if isLeft:
                for enemy in enemiesLeft:
                    xtr('checking enemy status')
                    if enemy.enemyxpos < 0-playersize:
                        enemy.enemyxpos = randint(width, width+(playersize*8))
                        enemy.enemyypos = randint(0, int(height-playersize))
                        score = score + 1
                        log('enemy moved to right, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.enemyxpos)+', '+str(enemy.enemyypos))
                    else:
                        enemy.enemyxpos = enemy.enemyxpos - enemyspeed
                        xtr('enemy moved left')
                    
                    DISPLAY.blit(enemyGlow, ((enemy.enemyxpos-playersize*0.125, enemy.enemyypos-playersize*0.125)))
                    DISPLAY.blit(enemytex, (enemy.enemyxpos, enemy.enemyypos))

                    if xpos+playersize > enemy.enemyxpos and xpos < enemy.enemyxpos+playersize and ypos+playersize > enemy.enemyypos and ypos < enemy.enemyypos+playersize:
                    
                        clock.tick(60)
                            
                        log('rendering death screen')
                        DISPLAY.fill(BLUE)
                        endtext = font.render('Your score was '+str(score), True, (255-BLUE[0], 255-BLUE[1], 255-BLUE[2]))
                        DISPLAY.blit(endtext, (width/2 - endtext.get_width()/2, 10))
                        highscore = font.render('Your highscorescore is '+str(savedata[0]), True, (255-BLUE[0], 255-BLUE[1], 255-BLUE[2]))
                        DISPLAY.blit(highscore, (width/2 - highscore.get_width()/2, height-10-highscore.get_height()))
                        pygame.display.update()

                        if score > int(savedata[0]) and difficulty >= int(savedata[1]):
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            temp = date()
                            savedata[2] = temp
                            save_save()
                            log('save complete')

                        elif score > int(savedata[0])+15:
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            temp = date()
                            savedata[2] = temp
                            save_save()
                            log('save complete')

                        log('recording score in savefile...')
                        savedata.append(str(score))
                        savedata.append(str(difficulty))
                        temp = date()
                        savedata[2] = temp
                        save_save()
                        log('save complete')

                        log('waiting 4 seconds')
                        sleep(4)

                        return(2)

            xtr('drawing enemies (right)')
            if isRight:
                for enemy in enemiesRight:
                    xtr('checking enemy status')
                    if enemy.enemyxpos > width:
                        enemy.enemyxpos = randint(0-playersize*8, 0-playersize)
                        enemy.enemyypos = randint(0, int(height-playersize))
                        score = score + 1
                        log('enemy moved to left, score increased. new score: '+str(score)+' - new enemy position: '+str(enemy.enemyxpos)+', '+str(enemy.enemyypos))
                    else:
                        enemy.enemyxpos = enemy.enemyxpos + enemyspeed
                        xtr('enemy moved right')
                        
                    DISPLAY.blit(enemyGlow, ((enemy.enemyxpos-playersize*0.125, enemy.enemyypos-playersize*0.125)))
                    DISPLAY.blit(enemytex, (enemy.enemyxpos, enemy.enemyypos))

                    if xpos+playersize > enemy.enemyxpos and xpos < enemy.enemyxpos+playersize and ypos+playersize > enemy.enemyypos and ypos < enemy.enemyypos+playersize:
                    
                        clock.tick(60)
                            
                        log('rendering death screen')
                        DISPLAY.fill(BLUE)
                        endtext = font.render('Your score was '+str(score), True, (255-BLUE[0], 255-BLUE[1], 255-BLUE[2]))
                        DISPLAY.blit(endtext, (width/2 - endtext.get_width()/2, 10))
                        highscore = font.render('Your highscorescore is '+str(savedata[0]), True, (255-BLUE[0], 255-BLUE[1], 255-BLUE[2]))
                        DISPLAY.blit(highscore, (width/2 - highscore.get_width()/2, height-10-highscore.get_height()))
                        pygame.display.update()

                        if score > int(savedata[0]) and difficulty >= int(savedata[1]):
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            temp = date()
                            savedata[2] = temp
                            save_save()
                            log('save complete')

                        elif score > int(savedata[0])+15:
                            log('new highscore! saving to save.sf...')
                            savedata[0] = str(score)
                            savedata[1] = str(difficulty)
                            temp = date()
                            savedata[2] = temp
                            save_save()
                            log('save complete')

                        log('recording score in savefile...')
                        savedata.append(str(score))
                        savedata.append(str(difficulty))
                        temp = date()
                        savedata[2] = temp
                        save_save()
                        log('save complete')

                        log('waiting 4 seconds')
                        sleep(4)

                        return(2)

            xtr('drawing score')
            scoretest = font.render(str(score), True, (255-BLUE[0], 255-BLUE[1], 255-BLUE[2]))
            DISPLAY.blit(scoretest, (width/2 - scoretest.get_width()/2, 10))
                
            xtr('updating display')
            pygame.display.update()
    except:
        return(1)

def optionsmenu():
    try:
        # setup stuff
        width = windowwidth
        height = windowheight
        inMenu = True
        active1 = False
        active2 = False
        active3 = False
        active4 = False
        active5 = False
        text1 = str(options[2])
        text2 = str(options[3])
        text3 = str(options[4])+', '+str(options[5])+', '+str(options[6])
        if options[7] == True: text4 = 'On'
        else: text4 = 'Off'
        text5 = options[8]
        status = ''
        log('initialising pygame, variables and clock')
        pygame.init()
        pygame.mixer.init()
        playersize = (width/640)*32
        clock = Clock()
        log('creating window')
        DISPLAY = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption(game_name)
        log('importing textures, other assets, and other visual stuff')
        BLUE = (55, 55, 55)

        # if custom textures are enabled, load them. otherwise, use default textures.
        if options[7] == True:
            log('using custom textures')
            try:
                pygame.mixer.music.load(options[8]+'music.mp3')
                log('music imported')
            except:
                pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
                log('music not found, using default')
            try:
                font = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*32))
                log('font imported')
            except:
                font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
                log('font not found, using default')
            try:
                smallfont = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*12))
                log('font imported')
            except:
                smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))
                log('font not found, using default')
        else:
            log('using default textures')

            pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
            font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
            smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))

        appicon = pygame.image.load(assetspath+'defaultTextures/appicon.png')
        corner = pygame.image.load(assetspath+'defaultTextures/corner.png')

        # set app icon
        pygame.display.set_icon(appicon)

        # resize player + enemy textures for window size
        corner = pygame.transform.scale(corner, (int(windowwidth/8), int(windowwidth/8)))

        # music stuff
        pygame.mixer.music.set_volume(0.3)
        log('starting music')
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
            log('music started')
        else:
            log('music already playing, cancelling')

        colourcycle = 0

        r = 55
        g = 55
        b = 255

        while inMenu:
            clock.tick(60)

            # colour display with rainbow colour
            DISPLAY.fill(BLUE)

            # quit
            for event in pygame.event.get():
                if event.type==QUIT:
                    log('quitting')
                    pygame.quit()
                    return(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box1.collidepoint(event.pos):
                        active1 = not active1
                    else:
                        active1 = False
                        
                    if input_box2.collidepoint(event.pos):
                        active2 = not active2
                    else:
                        active2 = False
                        
                    if input_box3.collidepoint(event.pos):
                        active3 = not active3
                    else:
                        active3 = False
                        
                    if input_box4.collidepoint(event.pos):
                        active4 = not active4
                    else:
                        active4 = False
                        
                    if options[7] == True:
                        if input_box5.collidepoint(event.pos):
                            active5 = not active5
                        else:
                            active5 = False
                        
                if event.type == pygame.KEYDOWN:
                    if active1:
                        if event.key == pygame.K_RETURN:
                            print(text1)
                            try:
                                options[2] = int(text1)
                                log('difficulty set to '+str(options[2]))
                                status = 'Difficulty set to '+str(options[2])
                                save_options()
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                            text1 = str(options[2])
                        elif event.key == pygame.K_BACKSPACE:
                            text1 = text1[:-1]
                        else:
                            text1 += event.unicode

                    if active2:
                        if event.key == pygame.K_RETURN:
                            print(text2)
                            try:
                                options[3] = text2
                                log('username set to '+str(options[3]))
                                status = 'Username set to '+str(options[3])
                                save_options()
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                            text2 = str(options[3])
                        elif event.key == pygame.K_BACKSPACE:
                            text2 = text2[:-1]
                        else:
                            text2 += event.unicode

                    if active3:
                        if event.key == pygame.K_RETURN:
                            print(text3)
                            try:
                                temparray = text3.split(', ')
                                options[4] = int(temparray[0])
                                options[5] = int(temparray[1])
                                options[6] = int(temparray[2])
                                log('background colour set to '+str(options[4])+', '+str(options[5])+', '+str(options[6]))
                                status = 'Background colour set to '+str(options[4])+', '+str(options[5])+', '+str(options[6])
                                save_options()
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                            text3 = str(options[4])+', '+str(options[5])+', '+str(options[6])
                        elif event.key == pygame.K_BACKSPACE:
                            text3 = text3[:-1]
                        else:
                            text3 += event.unicode

                    if active4:
                        if event.key == pygame.K_RETURN:
                            print(text4)
                            try:
                                if text4 == 'on' or text4 == 'On' or text4 == 'ON' or text4 == '1' or text4 == 'true' or text4 == 'True' or text4 == 'TRUE' or text4 == 'yes' or text4 == 'Yes' or text4 == 'YES' or text4 == 'y' or text4 == 'Y':
                                    options[7] = True
                                    log('texture pack enabled')
                                    status = 'Texture pack enabled'
                                elif text4 == 'off' or text4 == 'Off' or text4 == 'OFF' or text4 == '0' or text4 == 'false' or text4 == 'False' or text4 == 'FALSE' or text4 == 'no' or text4 == 'No' or text4 == 'NO' or text4 == 'n' or text4 == 'N':
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
                            if options[7] == True:
                                text4 = 'On'
                            else:
                                text4 = 'Off'
                        elif event.key == pygame.K_BACKSPACE:
                            text4 = text4[:-1]
                        else:
                            text4 += event.unicode

                    if active5 and options[7] == True:
                        if event.key == pygame.K_RETURN:
                            print(text5)
                            try:
                                options[8] = text5
                                log('texture path set to '+str(options[8]))
                                status = 'Texture pack path set to '+str(options[8])
                                save_options()
                            except:
                                log('failed!')
                                status = 'An error occured. Try again, and if the problem persists, refer to the help guide by pressing tab.'
                            text5 = str(options[8])
                        elif event.key == pygame.K_BACKSPACE:
                            text5 = text5[:-1]
                        else:
                            text5 += event.unicode
                    
            
            # restart music if it stops
            if pygame.mixer.music.get_busy() == False:
                log('music finished, restarting')
                pygame.mixer.music.play()

            # keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return(1)
            if keys[pygame.K_TAB]:
                pygame.quit()
                return(7)

            # rainbow background
            if colourcycle >= 0 and colourcycle <= 200:
                r = r+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 200 and colourcycle <= 400:
                b = b-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 400 and colourcycle <= 600:
                g = g+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 600 and colourcycle <= 800:
                r = r-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 800 and colourcycle <= 1000:
                b = b+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 1000 and colourcycle <= 1200:
                g = g-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle > 1200:
                colourcycle = 0
            colourcycle = colourcycle+1



            # menu text and images
            welcome = font.render('Options', True, (245, 245, 245))
            DISPLAY.blit(welcome, (width/2 - welcome.get_width()/2, 10))

            key = smallfont.render('Press a number on your keyboard to edit that option\'s value.', True, (245, 245, 245))
            DISPLAY.blit(key, (width/2 - key.get_width()/2, height/9))

            optionstext = smallfont.render('1 - Difficulty', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, height/6))
            input_box1 = pygame.Rect(width/22+optionstext.get_width()+(width/44), height/6, width/2, height/24)

            optionstext = smallfont.render('2 - Username', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2)))
            input_box2 = pygame.Rect(width/22+optionstext.get_width()+(width/44), (height/6)+(optionstext.get_height()*1.2), width/2, height/24)

            optionstext = smallfont.render('3 - Background colour', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*2)))
            input_box3 = pygame.Rect(width/22+optionstext.get_width()+(width/44), (height/6)+(optionstext.get_height()*1.2*2), width/2, height/24)

            optionstext = smallfont.render('4 - Texture pack on/off', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*3)))
            input_box4 = pygame.Rect(width/22+optionstext.get_width()+(width/44), (height/6)+(optionstext.get_height()*1.2*3), width/2, height/24)

            if options[7] == True:
                optionstext = smallfont.render('5 - Texture pack path', True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*4)))
                input_box5 = pygame.Rect(width/22+optionstext.get_width()+(width/44), (height/6)+(optionstext.get_height()*1.2*4), width/2, height/24)

                optionstext = smallfont.render('Press Escape to Exit', True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*6)))
                DISPLAY.blit(corner, (width-corner.get_width(), height-corner.get_height()))
            else:
                optionstext = smallfont.render('Press Escape to Exit', True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*5)))
                DISPLAY.blit(corner, (width-corner.get_width(), height-corner.get_height()))
            
            statustext = smallfont.render(status, True, (245, 245, 245))
            DISPLAY.blit(statustext, ((width/2)-(statustext.get_width()/2), height-(height/22)))
            
            txt_surface1 = smallfont.render(' '+text1, True, (245, 245, 245))
            widthi1 = max(350, txt_surface1.get_width()+10)
            input_box1.w = widthi1
            DISPLAY.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box1, 2)
            
            txt_surface2 = smallfont.render(' '+text2, True, (245, 245, 245))
            widthi2 = max(350, txt_surface2.get_width()+10)
            input_box2.w = widthi2
            DISPLAY.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box2, 2)
            
            txt_surface3 = smallfont.render(' '+text3, True, (245, 245, 245))
            widthi3 = max(350, txt_surface3.get_width()+10)
            input_box3.w = widthi3
            DISPLAY.blit(txt_surface3, (input_box3.x+5, input_box3.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box3, 2)
            
            txt_surface4 = smallfont.render(' '+text4, True, (245, 245, 245))
            widthi4 = max(350, txt_surface4.get_width()+10)
            input_box4.w = widthi4
            DISPLAY.blit(txt_surface4, (input_box4.x+5, input_box4.y+5))
            pygame.draw.rect(DISPLAY, (245, 245, 245), input_box4, 2)
            
            if options[7] == True:
                txt_surface5 = smallfont.render(' '+text5, True, (245, 245, 245))
                widthi5 = max(350, txt_surface5.get_width()+10)
                input_box5.w = widthi5
                DISPLAY.blit(txt_surface5, (input_box5.x+5, input_box5.y+5))
                pygame.draw.rect(DISPLAY, (245, 245, 245), input_box5, 2)

            pygame.display.update()
    except:
        return(1)

def stats():
    try:
        # setup stuff
        inMenu = True
        log('initialising pygame, variables and clock')
        pygame.init()
        pygame.mixer.init()
        playersize = (width/640)*32
        clock = Clock()
        log('creating window')
        DISPLAY = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption(game_name)
        log('importing textures, other assets, and other visual stuff')
        BLUE = (55, 55, 55)

        # if custom textures are enabled, load them. otherwise, use default textures.
        if options[7] == True:
            log('using custom textures')
            try:
                pygame.mixer.music.load(options[8]+'music.mp3')
                log('music imported')
            except:
                pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
                log('music not found, using default')
            try:
                font = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*32))
                log('font imported')
            except:
                font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
                log('font not found, using default')
            try:
                smallfont = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*12))
                log('font imported')
            except:
                smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))
                log('font not found, using default')
        else:
            log('using default textures')

            pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
            font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
            smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))

        appicon = pygame.image.load(assetspath+'defaultTextures/appicon.png')
        corner = pygame.image.load(assetspath+'defaultTextures/corner.png')

        # set app icon
        pygame.display.set_icon(appicon)

        # resize player + enemy textures for window size
        corner = pygame.transform.scale(corner, (int(windowwidth/8), int(windowwidth/8)))

        # music stuff
        pygame.mixer.music.set_volume(0.3)
        log('starting music')
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
            log('music started')
        else:
            log('music already playing, cancelling')

        colourcycle = 0

        r = 55
        g = 55
        b = 255

        while inMenu:
            clock.tick(60)

            # colour display with rainbow colour
            DISPLAY.fill(BLUE)

            # quit
            for event in pygame.event.get():
                if event.type==QUIT:
                    log('quitting')
                    pygame.quit()
                    return(0)
            
            # restart music if it stops
            if pygame.mixer.music.get_busy() == False:
                log('music finished, restarting')
                pygame.mixer.music.play()

            # keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return(1)
            if keys[pygame.K_1]:
                pygame.quit()
                return(2)

            # rainbow background
            if colourcycle >= 0 and colourcycle <= 200:
                r = r+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 200 and colourcycle <= 400:
                b = b-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 400 and colourcycle <= 600:
                g = g+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 600 and colourcycle <= 800:
                r = r-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 800 and colourcycle <= 1000:
                b = b+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 1000 and colourcycle <= 1200:
                g = g-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle > 1200:
                colourcycle = 0
            colourcycle = colourcycle+1
            
            # menu text and images
            welcome = font.render('Stats', True, (245, 245, 245))
            DISPLAY.blit(welcome, (width/2 - welcome.get_width()/2, 10))
            try:
                optionstext = smallfont.render('Highscore: '+str(savedata[0]), True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, height/6))
                optionstext = smallfont.render('Highscore difficulty: '+str(savedata[1]), True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*1)))
                optionstext = smallfont.render('Highscore date: '+str(savedata[2]), True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*2)))
            except:
                pass
            try:
                optionstext = smallfont.render('Latest score: '+str(savedata[len(savedata)-2]), True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*3.5)))
                optionstext = smallfont.render('Latest difficulty: '+str(savedata[len(savedata)-1]), True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*4.5)))
                optionstext = smallfont.render('Latest date: '+str(savedata[len(savedata)]), True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*5.5)))
            except:
                pass
            try:
                optionstext = smallfont.render('Earliest score: '+str(savedata[3]), True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*7)))
                optionstext = smallfont.render('Earliest difficulty: '+str(savedata[4]), True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*8)))
                optionstext = smallfont.render('Earliest date: '+str(savedata[5]), True, (245, 245, 245))
                DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*9)))
            except:
                pass
            optionstext = smallfont.render('Press Escape to Exit, or 1 to jump directly into the game.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*11)))
            DISPLAY.blit(corner, (width-corner.get_width(), height-corner.get_height()))

            pygame.display.update()
    except:
        return(1)

def helpmenu():
    try:
        # setup stuff
        inMenu = True
        log('initialising pygame, variables and clock')
        pygame.init()
        pygame.mixer.init()
        playersize = (width/640)*32
        clock = Clock()
        log('creating window')
        DISPLAY = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption(game_name)
        log('importing textures, other assets, and other visual stuff')
        BLUE = (55, 55, 55)

        # if custom textures are enabled, load them. otherwise, use default textures.
        if options[7] == True:
            log('using custom textures')
            try:
                pygame.mixer.music.load(options[8]+'music.mp3')
                log('music imported')
            except:
                pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
                log('music not found, using default')
            try:
                font = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*32))
                log('font imported')
            except:
                font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
                log('font not found, using default')
            try:
                smallfont = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*12))
                log('font imported')
            except:
                smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))
                log('font not found, using default')
        else:
            log('using default textures')

            pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
            font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
            smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))

        appicon = pygame.image.load(assetspath+'defaultTextures/appicon.png')
        corner = pygame.image.load(assetspath+'defaultTextures/corner.png')

        # set app icon
        pygame.display.set_icon(appicon)

        # resize player + enemy textures for window size
        corner = pygame.transform.scale(corner, (int(windowwidth/8), int(windowwidth/8)))

        # music stuff
        pygame.mixer.music.set_volume(0.3)
        log('starting music')
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
            log('music started')
        else:
            log('music already playing, cancelling')

        colourcycle = 0

        r = 55
        g = 55
        b = 255

        while inMenu:
            clock.tick(60)

            # colour display with rainbow colour
            DISPLAY.fill(BLUE)

            # quit
            for event in pygame.event.get():
                if event.type==QUIT:
                    log('quitting')
                    pygame.quit()
                    return(0)
            
            # restart music if it stops
            if pygame.mixer.music.get_busy() == False:
                log('music finished, restarting')
                pygame.mixer.music.play()

            # keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return(1)
            if keys[pygame.K_1]:
                pygame.quit()
                return(2)

            # rainbow background
            if colourcycle >= 0 and colourcycle <= 200:
                r = r+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 200 and colourcycle <= 400:
                b = b-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 400 and colourcycle <= 600:
                g = g+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 600 and colourcycle <= 800:
                r = r-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 800 and colourcycle <= 1000:
                b = b+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 1000 and colourcycle <= 1200:
                g = g-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle > 1200:
                colourcycle = 0
            colourcycle = colourcycle+1
            
            # menu text and images
            welcome = font.render('Help', True, (245, 245, 245))
            DISPLAY.blit(welcome, (width/2 - welcome.get_width()/2, 10))
            optionstext = smallfont.render('To move your character, use W, S, A and D, or the arrow keys.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, height/6))
            optionstext = smallfont.render('The aim of the game is to avoid the enemies for as long as possible.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2)))
            optionstext = smallfont.render('The game ends when you first touch an enemy.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*2)))
            optionstext = smallfont.render('Good luck!', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*3)))
            optionstext = smallfont.render('Press Escape to Exit, or 1 to jump directly into the game.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*5)))
            DISPLAY.blit(corner, (width-corner.get_width(), height-corner.get_height()))

            pygame.display.update()
    except:
        return(1)

def credits():
    try:
        # setup stuff
        inMenu = True
        log('initialising pygame, variables and clock')
        pygame.init()
        pygame.mixer.init()
        playersize = (width/640)*32
        clock = Clock()
        log('creating window')
        DISPLAY = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption(game_name)
        log('importing textures, other assets, and other visual stuff')
        BLUE = (55, 55, 55)

        # if custom textures are enabled, load them. otherwise, use default textures.
        if options[7] == True:
            log('using custom textures')
            try:
                pygame.mixer.music.load(options[8]+'music.mp3')
                log('music imported')
            except:
                pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
                log('music not found, using default')
            try:
                font = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*32))
                log('font imported')
            except:
                font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
                log('font not found, using default')
            try:
                smallfont = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*12))
                log('font imported')
            except:
                smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))
                log('font not found, using default')
        else:
            log('using default textures')

            pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
            font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
            smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))

        appicon = pygame.image.load(assetspath+'defaultTextures/appicon.png')
        corner = pygame.image.load(assetspath+'defaultTextures/corner.png')

        # set app icon
        pygame.display.set_icon(appicon)

        # resize player + enemy textures for window size
        corner = pygame.transform.scale(corner, (int(windowwidth/8), int(windowwidth/8)))

        # music stuff
        pygame.mixer.music.set_volume(0.3)
        log('starting music')
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
            log('music started')
        else:
            log('music already playing, cancelling')

        colourcycle = 0

        r = 55
        g = 55
        b = 255

        while inMenu:
            clock.tick(60)

            # colour display with rainbow colour
            DISPLAY.fill(BLUE)

            # quit
            for event in pygame.event.get():
                if event.type==QUIT:
                    log('quitting')
                    pygame.quit()
                    return(0)
            
            # restart music if it stops
            if pygame.mixer.music.get_busy() == False:
                log('music finished, restarting')
                pygame.mixer.music.play()

            # keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return(1)
            if keys[pygame.K_1]:
                pygame.quit()
                return(2)

            # rainbow background
            if colourcycle >= 0 and colourcycle <= 200:
                r = r+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 200 and colourcycle <= 400:
                b = b-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 400 and colourcycle <= 600:
                g = g+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 600 and colourcycle <= 800:
                r = r-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 800 and colourcycle <= 1000:
                b = b+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 1000 and colourcycle <= 1200:
                g = g-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle > 1200:
                colourcycle = 0
            colourcycle = colourcycle+1
            
            # menu text and images
            welcome = font.render('Credits', True, (245, 245, 245))
            DISPLAY.blit(welcome, (width/2 - welcome.get_width()/2, 10))
            optionstext = smallfont.render('Thank you to everyone who has helped me work on this game.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, height/6))
            optionstext = smallfont.render('Come and join the discord server to learn more, i can\'t list them here:', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*1.5)))
            optionstext = smallfont.render('https://bit.ly/fxpDiscord', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*2.5)))
            optionstext = smallfont.render('Press Escape to Exit, or 1 to jump directly into the game.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*5)))
            DISPLAY.blit(corner, (width-corner.get_width(), height-corner.get_height()))

            pygame.display.update()
    except:
        return(1)

def optionshelp():
    try:
        # setup stuff
        inMenu = True
        log('initialising pygame, variables and clock')
        pygame.init()
        pygame.mixer.init()
        playersize = (width/640)*32
        clock = Clock()
        log('creating window')
        DISPLAY = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption(game_name)
        log('importing textures, other assets, and other visual stuff')
        BLUE = (55, 55, 55)

        # if custom textures are enabled, load them. otherwise, use default textures.
        if options[7] == True:
            log('using custom textures')
            try:
                pygame.mixer.music.load(options[8]+'music.mp3')
                log('music imported')
            except:
                pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
                log('music not found, using default')
            try:
                font = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*32))
                log('font imported')
            except:
                font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
                log('font not found, using default')
            try:
                smallfont = pygame.font.Font(options[8]+'font.ttf', int((windowwidth/640)*12))
                log('font imported')
            except:
                smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))
                log('font not found, using default')
        else:
            log('using default textures')

            pygame.mixer.music.load(assetspath+'defaultTextures/music.mp3')
            font = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*32))
            smallfont = pygame.font.Font(assetspath+'defaultTextures/font.ttf', int((windowwidth/640)*12))

        appicon = pygame.image.load(assetspath+'defaultTextures/appicon.png')
        corner = pygame.image.load(assetspath+'defaultTextures/corner.png')

        # set app icon
        pygame.display.set_icon(appicon)

        # resize player + enemy textures for window size
        corner = pygame.transform.scale(corner, (int(windowwidth/8), int(windowwidth/8)))

        # music stuff
        pygame.mixer.music.set_volume(0.3)
        log('starting music')
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
            log('music started')
        else:
            log('music already playing, cancelling')

        colourcycle = 0

        r = 55
        g = 55
        b = 255

        while inMenu:
            clock.tick(60)

            # colour display with rainbow colour
            DISPLAY.fill(BLUE)

            # quit
            for event in pygame.event.get():
                if event.type==QUIT:
                    log('quitting')
                    pygame.quit()
                    return(0)
            
            # restart music if it stops
            if pygame.mixer.music.get_busy() == False:
                log('music finished, restarting')
                pygame.mixer.music.play()

            # keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return(3)
            if keys[pygame.K_1]:
                pygame.quit()
                return(1)

            # rainbow background
            if colourcycle >= 0 and colourcycle <= 200:
                r = r+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 200 and colourcycle <= 400:
                b = b-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 400 and colourcycle <= 600:
                g = g+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 600 and colourcycle <= 800:
                r = r-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 800 and colourcycle <= 1000:
                b = b+1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle >= 1000 and colourcycle <= 1200:
                g = g-1
                BLUE = (int(r/3), int(g/3), int(b/3))
            if colourcycle > 1200:
                colourcycle = 0
            colourcycle = colourcycle+1
            
            # menu text and images
            welcome = font.render('Options help', True, (245, 245, 245))
            DISPLAY.blit(welcome, (width/2 - welcome.get_width()/2, 10))
            optionstext = smallfont.render('To edit a value, click in the box next to it, and change it\'s value by typing a new one.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*1)))
            optionstext = smallfont.render('Press enter to submit.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*2)))
            optionstext = smallfont.render('When editing the Difficulty value, make sure you only type numbers, and no other characters.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*3.5)))
            optionstext = smallfont.render('You can type anything in the username field.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*5)))
            optionstext = smallfont.render('When editing the Background value, type 3 numbers that are above 0 and less than 255, ', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*6.5)))
            optionstext = smallfont.render('seperated by commas (e.g. 45, 255, 0).', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*8.5)))
            optionstext = smallfont.render('When editing the Custom Texture toggle value, type \'on\' or \'off\'. You can also type \'true\', ', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*10)))
            optionstext = smallfont.render('\'false\', \'y\', \'n\', \'yes\', or \'no\'.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*11)))
            optionstext = smallfont.render('When editing the Custom Texture path value, type the path of your texture pack in relation', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*12.5)))
            optionstext = smallfont.render('to the game\'s files. Make sure you put a \'/\' at the end of it.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, (height/6)+(optionstext.get_height()*1.2*13.5)))
            optionstext = smallfont.render('Press Escape to return to the options menu, or 1 to return to the main menu.', True, (245, 245, 245))
            DISPLAY.blit(optionstext, (width/22, height-optionstext.get_height()*1.2))
            DISPLAY.blit(corner, (width-corner.get_width(), height-corner.get_height()))

            pygame.display.update()
    except:
        return(1)

playing = True
function = 1
# call the correct functions at the correct times
while playing:
    if function == 0:
        log('exiting game')
        playing = False
    elif function == 1:
        log('loading menu...')
        function = menu()
    elif function == 2:
        log('loading game...')
        function = game()
    elif function == 3:
        log('loading options...')
        function = optionsmenu()
    elif function == 4:
        log('loading stats...')
        function = stats()
    elif function == 5:
        log('loading help...')
        function = helpmenu()
    elif function == 6:
        log('loading dev stuff...')
        devstuff()
        function = 1
    elif function == 7:
        log('loading options help...')
        function = optionshelp()
    elif function == 8:
        log('loading credits...')
        function = credits()
    else:
        log('error: invalid function')
        function = 1

# 0 - game
# 1 - menu
# 2 - options
# 3 - stats
# 4 - help
# 5 - options help
# 9 - Credits