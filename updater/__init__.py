import sys
import os
import urllib.request as requests

class Updater:
    def __init__(self, update_url, file_to_update):
        #Set the class-wide update url
        self.__update_url = update_url
        #Set the class-wide file_to_update
        self.__file_to_update = file_to_update
    def update(self):
        #Just leaving this empty content variable
        __content = ""
        #Open the file for raw reading via urllib
        __page = requests.urlopen(self.__update_url).readlines()
        #Check if the file to update exists on our device
        if(os.path.exists(self.__file_to_update)):
            #Open our end
            __file = open(self.__file_to_update, "rb")
            #Read the lines
            __lines = __file.readlines()
            __new_lines = list()
            for __line in __lines:
                __line = __line.decode().replace("\r\n", "").encode()
                __new_lines.append(__line)
            __lines = __new_lines
            #Loop through the github-end lines
            for __line in __page:
                __line = __line.decode().replace("\r\n" ,"").encode()
                #Check if we do not have the line
                if(__line not in __lines):
                    #Update our content variable
                    __content += "\n%s"%(__line.decode())
            #Close the file and re open it for appending
            __file.close()
            #Re-open for appending, as stated
            __file = open(self.__file_to_update, "a")
            #Write the lines to the file
            __file.writelines(__content)
            #Close the file
            __file.close()
        else:
            #Check if the parent directory of the file does not exist
            if(os.path.exists(os.path.dirname(os.path.abspath(self.__file_to_update))) is False):
                #Create the directorys
                os.makedirs(os.path.dirname(os.path.abspath(self.__file_to_update)))
            #Open the file for writing
            __file = open(self.__file_to_update, "w")
            #Loop through the github-end lines
            for __line in __page:
                #Update the content variable
                __content += "%s\n"%(__line.decode())
            #Write the content of the github file to our file
            __file.writelines(__content)
            #Close our file
            __file.close()