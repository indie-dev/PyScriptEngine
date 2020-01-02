import sys
import os
import random
from exceptions import *
from reindenter import Reindenter
from xml.etree import ElementTree as Document

def __open(file, mode, encoding="", buffering=0, errors="", newline="", closefd=False, opener=""):
    #Raise that the function is unacceptable
    raise UnacceptedFunctionException("open()")
def __exec(code):
    #Raise that executing files on user's device is a big no no
    raise UnacceptedFunctionException("exec()")
class Engine:
    def __init__(self, html_document_path):
        #Verify if the document path exists
        if(os.path.exists(html_document_path)):
            #Open the document for parsing
            self.__document = Document.parse(html_document_path).getroot()
        else:
            #Raise a missing file exception
            raise Exception("%s is not a real file"%(html_document_path))
        #We will have to update the files in global_data
        __updater = Updater()
    def __gen_fname(self):
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

    def execute_all_scripts(self, start_element=None):
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
                        self.__results.append(self.__execute_script_into_document(__script.text))
            #Go again, but now the start element is __element
            self.execute_all_scripts(start_element=__element)
            #Return the results
            return self.__results
    def __execute_script_into_document(self, __text):
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
        return __results
    def __secure_script(self, __script):
        #Split all of the lines in the script
        __script_split = __script.splitlines()
        #Loop through the split script
        for __line in __script_split:
            #Lowercase the line
            __line = __line.lower()
            #Check if the line equals import
            if(__line.startswith("import")):
                #Split the import by comma
                __split_import = __line.replace("import", "").split(",")
                #Loop through the split list
                for __import in __split_import:
                    #Remove the inital space
                    __import = __import.replace(" ", "")
                    #Check if the import is os
                    if(__import == "os"):
                        #This os module is not accepted
                        raise UnacceptedModuleException("os")
                    elif(__import == "sys"):
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
                    #Open the unaccepted functions list
                    __unaccepted_functions = open(__fname, "r")
                    #Read all of the lines
                    __functions = __unaccepted_functions.readlines()
                    #Loop through the functions
                    for __function in __functions:
                        #Check if the function is in the line
                        if(__function in __word):
                            #Raise the UnacceptedFunctionException
                            raise UnacceptedFunctionException(__function)
        return __script
    def get_document(self):
        #Return the document
        return self.__document