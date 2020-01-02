class UnacceptedFunctionException(Exception):
    def __init__(self, text):
        text = "Unaccepted function: %s"%(text)
        print(text)
class UnacceptedModuleException(Exception):
    def __init__(self, text):
        text = "Unaccepted library: %s"%(text)
        print(text)