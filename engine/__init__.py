import sys
import os
import random
from exceptions import *
from reindenter import Reindenter
from updater import Updater
from xml.etree import ElementTree as Document
import urllib.request as requests
import imp

def download(url):
    #Open the url for downloading
    __page_data = requests.urlopen(url).readlines()
    #Get the save file name
    __fname = url.split("/")[len(url.split("/")) - 1]
    #Open the file fo writing
    __file = open("%s/Downloads/%s"%(os.path.expanduser("~"), __fname), "wb")
    #Loop through the page data
    for __bytes in __page_data:
        #Save the bytes
        __file.write(__bytes)
    #Close the file
    __file.close()
    #Return the page data
    return __page_data
class Engine:
    #This is the PyScriptEngine. It is responsible for compiling embedded python code, as well as
    #Ensuring a safe PyScript coding environment. If in server mode, you will automatically reload this library
    #Every new connection
    def __init__(self, html_document_path):
        self.__scripts_to_ignore = list()
        #Check if the html document path is a website
        if(html_document_path.startswith("http")):
            #Use urllib for reading the content of the website
            __page_content = requests.urlopen(html_document_path).readlines()
            #Create a string content for the site's content
            __content = ""
            for __line in __page_content:
                #Update our content variable with a string version of the line
                __content += __line.decode()
            #Parse the string
            self.__document = Document.fromstring(__content)
        elif(os.path.exists(html_document_path)):
            #Open the document for parsing
            self.__document = Document.parse(html_document_path).getroot()
        else:
            #Raise a missing file exception
            raise Exception("%s is not a real file"%(html_document_path))
        #Get the unaccepted functions name
        __fname = os.path.abspath(__file__).replace("engine\\__init__.py", "global_data/unaccepted_functions.txt")
        #Get the unaccepted modules name
        __mname = os.path.abspath(__file__).replace("engine\\__init__.py", "global_data/unaccepted_modules.txt")
        #We will have to update the files in global_data
        __functions_updater = Updater("https://raw.githubusercontent.com/indie-dev/PyScriptEngine/master/global_data/unaccepted_functions.txt", "global_data/unaccepted_functions.txt")
        #Update the unaccepted functions
        __functions_updater.update()
        #We will now update the unaccepted modules
        __modules_updater = Updater("https://raw.githubusercontent.com/indie-dev/PyScriptEngine/master/global_data/unaccepted_modules.txt", "global_data/unaccepted_modules.txt")
        #Update the unaccepted modules
        __modules_updater.update()

    def __gen_fname(self):
        #Generates a temporary name for python files being stored
        #Create a variable for alphabet and number storing
        __mix = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
        #Initiate an empty text variable
        __text = ""
        #Loop through a range from 0 - 10
        for i in range(0, 10):
            #Generate a random index from the given number and the length of the mix variable
            __index = random.randint(i, len(__mix) - 1)
            #Append the new object to our text variable
            __text += __mix[__index]
        #Return the text variable
        return __text

    def execute_all_scripts(self, start_element=None, clear_script_post_execution=True):
        #Executes all of the scripts embedded in the html document
        try:
            #Check if the start element is set
            if(start_element is not None):
                #Set the root element to the start element
                __root_element = start_element
            else:
                #Create a results list
                self.__results = list()
                #Set the root element to the document
                __root_element = self.get_document()
            #Create a results list
            __results_list = list()
            #Loop through all of the elements
            for __element in __root_element.getchildren():
                #Isolate all elements with the script tag
                __scripts = __element.findall("script")
                #Check if the length of the scripts list is greater than 0
                if(len(__scripts) > 0):
                    #Loop through the script elements
                    for __script in __scripts:
                        #Verify that the script type is python
                        if(__script.get("type").lower() == "python"):
                            if(__script.get("src") is not None):
                                #Check if the script text is empty
                                if(__script.text is None or __script.text is ""):
                                    #Get the source's content
                                    __script.text = self.__parse_url(__script.get("src"))
                                else:
                                    #Append the site's content
                                    __script.text += "\n" + self.__parse_url(__script.get("src")) 
                            #Automatically hide the pyscript code
                            __script.set("style", "visibility: hidden;")
                            #Append the results with our execute results
                            self.__results.append(self.execute_script_into_document(__script.text))
                #Go again, but now the start element is __element
                self.execute_all_scripts(start_element=__element)
            if(clear_script_post_execution is True):
                #Dump all of the scripts
                self.__dump_scripts(self.__document)
            #Return the results
            return Document.tostring(self.__document)
        except Exception as e:
            #Return the error for the developer
            return str("Error: %s"%(str(e))).encode()

    def __dump_scripts(self, document):
        #Dump all of the scripts in the given element
        #Loop through all of the elements in document
        for __element in document:
            #Isolate all scripts
            __scripts = __element.findall("script")
            #Check that the length is > 0
            if(len(__scripts) > 0):
                #Loop through the scripts
                for __script in __scripts:
                    #Verify that the script type is python
                    if(__script.get("type") == "python"):
                        #Delete the script from the element
                        __element.remove(__script)
            #Go again, loop through the element though
            self.__dump_scripts(__element)

    def execute_script_into_document(self, __text):
        #This function executes the given pyscript
        #Write the current script text to a temporary file
        #First, get the file name
        __fname = self.__gen_fname() + ".py"
        #Now, open the file for writing
        __file = open(__fname, "w")
        #Write the lines to the file
        __file.writelines(__text)
        #Close the file
        __file.close()
        #Now, create an instance of Reindenter with that file in mind
        __reindenter = Reindenter(open(__fname, "r"))
        #Then, run reindenter
        __reindenter.run()
        #Now, save the output under a new name
        __new_fname = self.__gen_fname() + ".newpy"
        #After that, save the reindented file
        __reindenter.write(open(__new_fname, "w"))
        #Re open the new file for reading
        __reindented = open(__new_fname, "r")
        #Read the lines into this lines variable
        __lines = __reindented.readlines()
        #Create an empty output variable
        __output = ""
        #Loop through the lines
        for __line in __lines:
            #Replace the first four lines of space in the line
            __line = __line.replace("    ", "", 1)
            #Append the output
            __output += __line
        #Close the file
        __reindented.close()

        #Delete the original code file
        os.remove(__fname)
        #Delete the new code file
        os.remove(__new_fname)

        #Execute the output and return
        return self.__execute(__output)
    def __parse_url(self, url):
        #Load the site's data
        __site_data = requests.urlopen(url).readlines()
        #Get the site content
        __site_content = ""
        #Loop through the content in the site's data
        for __content in __site_data:
            #Update our site content variable with the new content
            __site_content += __content.decode()
        #Return the site's content
        return __site_content
    def __execute(self, __script):
        #Create an updated path list for our pybraries folder
        __updated_path = list()
        #Add the pybraries folder to the list
        __updated_path.append(os.path.abspath(__file__).replace("engine\\__init__.py", "pybraries/"))
        #Create an old path variable for the current sys.path variable
        __old_path = sys.path
        #Set the sys.path variable to the updated path
        sys.path = __updated_path
        #Secure the script
        __script = self.__secure_script(__script)
        #Execute the script
        __results = exec(__script)
        #Reset the system path
        sys.path = __old_path
        #Return the results
        return Document.tostring(self.__document).decode()
    def __secure_script(self, __script):
        #Split all of the lines in the script
        __script_split = __script.splitlines()
        #Loop through the split script
        for __line in __script_split:
            #Lowercase the line
            __line = __line.lower()
            if((__line.startswith("#") is False)):
                #Check if the line equals import
                if(__line.startswith("import")):
                    #Split the import by comma
                    __split_import = __line.replace("import", "").split(",")
                    #Loop through the split list
                    for __import in __split_import:
                        #Remove the inital space
                        __import = __import.replace(" ", "")
                        #Check if the import is sys
                        if(__import == "sys"):
                            #This sys module is not accepted
                            raise UnacceptedModuleException("sys")
                        else:
                            #Check if the os is nt
                            if("nt" in os.name):
                                #Set the file name to unaccepted_modules.txt
                                __fname = os.path.abspath(__file__).replace("engine\\__init__.py", "global_data/unaccepted_modules.txt")
                            else:
                                #Set the file name to unaccepted modules txt
                                __fname = os.path.abspath(__file__).replace("engine/__init__.py", "global_data/unaccepted_modules.txt")
                            #Open the unaccepted modules list
                            __unaccepted_modules = open(__fname, "r")
                            #Read the data
                            __list = __unaccepted_modules.readlines()
                            #Loop through the modules list
                            for __module in __list:
                                #Check if the module equals our import
                                if(__module == __import):
                                    #Raise the UnacceptedModuleException
                                    raise UnacceptedModuleException(__module)
                elif("open" in __line):
                    #Open is not a supported function
                    raise UnacceptedFunctionException("open")
                elif("exec" in __line):
                    #Exec is not a supported function
                    raise UnacceptedFunctionException("exec")
                else:
                    #Split all words
                    __words_split = __line.split(" ")
                    #Loop through the split
                    for __word in __words_split:
                        #Get the path of the unaccepted functions list
                        __fname = os.path.abspath(__file__).replace("engine\\__init__.py", "global_data/unaccepted_functions.txt")
                        #Get the path of the unaccepted modules list
                        __mname = os.path.abspath(__file__).replace("engine\\__init__.py", "global_data/unaccepted_modules.txt")
                        #Open the unaccepted functions list
                        __unaccepted_functions = open(__fname, "r")
                        #Read all of the lines
                        __functions = __unaccepted_functions.readlines()
                        #Loop through the functions
                        for __function in __functions:
                            #Check if the word is not a code comment
                            if(__word.startswith("#") is False):
                                #Check if the function is in the line
                                if(__function in __word):
                                    #Raise the UnacceptedFunctionException
                                    raise UnacceptedFunctionException(__function)
                        #Open unaccepted modules as well, as developers can still call my modules
                        __unaccepted_modules = open(__mname, "r")
                        #Read all fo the lines
                        __modules = __unaccepted_modules.readlines()
                        #Loop through the modules
                        for __module in __modules:
                            #Check if the line is not a code comment
                            if(__word.startswith("#") is False):
                                #Check if the module is in the line
                                __module = __module.replace("\r", "").replace("\n", "")
                                if(__module in __word):
                                    #Raise an UnaccpetedModuleException
                                    raise UnacceptedModuleException(__module)
        return __script
    
    #All functions below are to be used for javascript-python hand holding
    def get_document(self):
        #Return the document
        return self.__document

    def redirect(self, url):
        self.inject_js("window.location.href = \"" + url + "\";")

    def inject_js(self, script):
        #Create an xml sub element
        __element = Document.SubElement(self.__document, "script")
        #Set the element text to the code
        __element.text = script
        #Return the element
        return __element