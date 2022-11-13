import tkinter as tk
from tkinter import ttk
import shutil, os, sys
from time import sleep

error = False
errors = []

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

assetspath = resource_path('assets/')
ufpath = resource_path('userfiles/')
pfpath = resource_path('resources/')

def install(kind):

    error = False
    errors = []

    if kind == 1:
        status1.configure(text="Installing...")
        status2.configure(text="Making directory C:\\Program Files\\JXFXP\\")
        try:
            os.makedirs("C:\\Program Files\\JXFXP\\")
        except:
            error = True
            errors.append("Cannot make directory C:\\Program Files\\JXFXP\\ - Ensure you are running this as an administrator")
        status2.configure(text="Making directory C:\\Program Files\\JXFXP\\mewo\\")
        try:
            os.makedirs("C:\\Program Files\\JXFXP\\mewo\\")
        except:
            error = True
            errors.append("Cannot make directory C:\\Program Files\\JXFXP\\mewo\\ - Ensure you are running this as an administrator")
        status2.configure(text="Copying file mewo.lnk to C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\")
        try:
            shutil.copy("mewo.lnk", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\mewo.lnk")
        except:
            error = True
            errors.append("Cannot copy file mewo.lnk to C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\ - Ensure you are running this as an administrator")
        status2.configure(text='Copying mewo.exe to C:\\Program Files\\JXFXP\\mewo.exe')
        try:
            shutil.copy('mewo.exe', 'C:\\Program Files\\JXFXP\\mewo\\mewo.exe')
        except:
            error = True
            errors.append("Cannot copy file mewo.exe to C:\\Program Files\\JXFXP\\mewo\\ - Ensure you are running this as an administrator")
        status2.configure(text="Copying assets to C:\\Program Files\\JXFXP\\assets\\")
        try:
            shutil.copytree('assets\\', 'C:\\Program Files\\JXFXP\\assets\\')
        except:
            error = True
            errors.append("Cannot copy assets to C:\\Program Files\\JXFXP\\assets\\ - Ensure you are running this as an administrator")
        status2.configure(text="Copying userfiles to C:\\Program Files\\JXFXP\\userfiles\\")
        try:
            shutil.copytree('userfiles\\', 'C:\\Program Files\\JXFXP\\userfiles\\')
        except:
            error = True
            errors.append("Cannot copy userfiles to C:\\Program Files\\JXFXP\\userfiles\\ - Ensure you are running this as an administrator")
        if error:
            status1.configure(text="Installation completed with errors:")
            for error in errors:
                status2.configure(text=error)
                sleep(3)
        else:
            status1.configure(text="Installation completed successfully!")
            status2.configure(text="")
            sleep(3)
        status1.configure(text="Idle")
        status2.configure(text="")
    elif kind == -1:
        status1.configure(text="Uninstalling...")
        status2.configure(text="Removing file C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\mewo.lnk")
        try:
            os.remove("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\mewo.lnk")
        except:
            error = True
            errors.append("Cannot remove file C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\mewo.lnk - Ensure you are running this as an administrator")
        status2.configure(text="Removing directory C:\\Program Files\\JXFXP\\")
        try:
            shutil.rmtree("C:\\Program Files\\JXFXP\\")
        except:
            error = True
            errors.append("Cannot remove directory C:\\Program Files\\JXFXP\\ - Ensure you are running this as an administrator")
        if error:
            status1.configure(text="Uninstallation completed with errors:")
            for error in errors:
                status2.configure(text=error)
                sleep(3)
        else:
            status1.configure(text="Uninstallation completed successfully!")
            status2.configure(text="")
            sleep(3)
        status1.configure(text="Idle")
        status2.configure(text="")

#create window + components
window = tk.Tk()
window.title = ('mewo')

ttk.Button(
  window, 
  text='\nInstall\n', 
  command=lambda: install(1)
).pack()

ttk.Button(
  window, 
  text='\nUninstall\n', 
  command=lambda: install(-1)
).pack()

ttk.Button(
  window, 
  text='\nExit\n', 
  command=lambda: sys.exit()
).pack()

status1 = ttk.Label(window, text='Idle')
status1.pack()

status2 = ttk.Label(window, text='')
status2.pack()

window.geometry("400x200") 
window.mainloop()