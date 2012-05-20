import ConfigParser

class CfgUtils():
    def __init__(self,archivename):
        self.archive = ConfigParser.ConfigParser()
        self.archivename = archivename
        
    def read(self,section,value):
        self.section = section 
        self.value = value       
        self.archive.read([self.archivename])
        self.value_ = self.archive.get(self.section,self.value)
        
        return self.value_
    
    def write(self,newvalue):
            self.newvalue = newvalue
            self.archive.set(self.section, self.value_, str(self.newvalue))
            f = open(self.archivename, "w")  
            self.archive.write(f)  
            f.close()     