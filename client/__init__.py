import sys
import os
from engine import *
import urllib.request as requests

class Client:
    def render_pys(self, url):
        #Render the python script embedded in that site's html
        #Initiate the PyScriptEngine with the given url
        self.__engine = Engine(url)
        #Render the code and return the output
        return self.__engine.execute_all_scripts()
    
    def get_engine(self):
        #Returns the initiated engine
        return self.__engine