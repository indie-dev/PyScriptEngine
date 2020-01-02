from engine import *
import sys
import os
def show_help():
    print("PyScriptEngine: Renders python code embedded in xml files")
    print("\t--help: Shows the help menu")
    print("How to execute:")
    print("\tpython main.py [HTML_WITH_PYTHON_EMBEDDED_PATH]")

try:
    if(sys.argv[1].lower() == "--help"):
        show_help()
    else:
        __html_path = sys.argv[1]
        __engine = Engine(__html_path)
        __engine.execute_all_scripts()
except IndexError:
    show_help()