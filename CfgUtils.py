import ConfigParser

class CfgUtils():
    def __init__(self,archivename):
        self.archive = ConfigParser.ConfigParser()
        self.archivename = archivename
        self.archive.read([self.archivename])
        
    def read(self,section,value):
        self.section = section 
        self.value = value        
        self.value_ = self.archive.get(self.section,self.value)
        
        return self.value_
    
    def write(self, section, value, newvalue):
            self.section = section 
            self.value = value   
            self.newvalue = newvalue
            self.archive.set(self.section, self.value, str(self.newvalue))
            f = open(self.archivename, "w")  
            self.archive.write(f)  
            f.close()     