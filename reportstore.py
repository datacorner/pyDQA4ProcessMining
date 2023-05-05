import os
import constants as C

class ReportStore:
    def __init__(self):
        self.__tempPath = C.DEFAULT_STORE_FOLDER
        self.__filesManaged = []

    @property
    def tempPath(self):
        return self.__tempPath
    @tempPath.setter  
    def tempPath(self, value):
        self.__tempPath = value
        
    def getPath(self, p_filename):
        newFile = self.__tempPath + p_filename
        self.__filesManaged.append(newFile)
        return newFile
    
    def isStoreFolderExist(self):
        return (os.path.isdir(self.__tempPath))
        
    def initialize(self):
        # Check if the folder already exist first
        try:
            if not self.isStoreFolderExist():
                os.mkdir(self.__tempPath)   # Create the temp working folder (needed for the charts & table)
            return True
        except FileExistsError:
            return False
    
    # Remove all the temp files and the folder as well
    def finalize(self):
        try:
            for file in self.__filesManaged:
                os.remove(file)
            os.rmdir(self.__tempPath)
        except:
            return
        return