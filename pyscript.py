from engine import *
from server import *
from client import *
import sys
import os
def show_help():
    print("PyScriptEngine: Renders python code embedded in xml files")
    print("\t--help: Shows the help menu")
    print("\t--serve [FILE_PATH] [PORT]: Serve the given file via socket")
    print("\t--render [URL]: Compiles the given url")
    print("How to execute:")
    print("\tpython main.py [HTML_WITH_PYTHON_EMBEDDED_PATH]")

def serve(__file_path, __port):
    #For hosting a file
    #Initiate the server
    __server = Server()
    #Create our server on __port
    __server.create_server(__port, file=__file_path)
    #Host the server
    __server.host()

def render(__url):
    #For rendering a single url
    #Initiate the client
    __client = Client()
    #Render the given url
    return __client.render_pys(__url)

def parse_html_file(__html_path):
    #For parsing a given html file
    #Create the engine with the given path
    __engine = Engine(__html_path)
    #Execute all of the scripts
    return __engine.execute_all_scripts()

def main():
    try:
        #Get the first argument
        __arg = sys.argv[1].lower()
        #Check if we need help
        if(__arg == "--help"):
            #Show the help menu
            show_help()
        #Check if we wish to serve a file
        elif(__arg == "--serve"):
            #Get the file path
            __file_path = sys.argv[2]
            #Get the port
            __port = int(sys.argv[3])
            #Serve the given file
            serve(__file_path, __port)
        elif(__arg == "--render"):
            #Get the url to be rendered
            __url = sys.argv[2]
            #Render the url
            print(render(__url).decode())
        else:
            #Render the html at the given path
            __html_path = sys.argv[1]
            #Parse the html file
            print(parse_html_file(__html_path).decode())
    except IndexError:
        #Show the help menu
        show_help()
if(str(__name__) == "__main__"):
    #Show the main menu
    main()