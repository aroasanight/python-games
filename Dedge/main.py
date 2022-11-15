import os, pickle

cont = True
cont1 = True

def loadCont():
    with open ('assets/cont.sf', 'rb') as f: return pickle.load(f)
def dumpCont():
    with open ('assets/cont.sf', 'wb') as f: pickle.dump(False, f)

while cont1:
    if cont:
        dumpCont()
        print('[main.py] - Calling game.py')
        os.system('python3 game.py')
        cont = bool(loadCont())
        print('[main.py] - Cont: '+str(cont))
    else: cont1 = False

print('[main.py] - Ending script\nBye!')