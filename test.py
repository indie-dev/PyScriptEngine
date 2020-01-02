from updater import *

u = Updater("https://raw.githubusercontent.com/indie-dev/PyScriptEngine/master/global_data/unaccepted_modules.txt", "global_data/unaccepted_modules.txt")
u.update()