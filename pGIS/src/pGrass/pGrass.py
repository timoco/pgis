'''----------------------------------------------------------------------------------
 Module Name:         pGrass.pGrass
 Source Name:      /Users/TPM/MyDocs/dev/gis/pgis/src/pGrass/pGrass.py
 Version:           Python 2.6
 Author:            Timothy Morrissey, (timothy.morrissey@unc.edu)
 Date:                Mar 10, 2010
 Required Argumuments:  
 Optional Arguments:    
 Description: 
 Documentation: 
----------------------------------------------------------------------------------'''
# #####################################
#       ------ Imports --------
# #####################################
import os
import grass.script as grass
from pprint import pprint as pp
import sys
import pGrassDisplay
import pGrassRaster

#from pGrass import pGrassDisplay

# ######################################
#       ------ Classes --------
# ######################################
class grassApp():
    '''
    Class for a GRASS GIS python application
    '''
    def __init__(self,grassConfigSect):
        #set the grass.general (g.<name>) functions
        self.__gMList='g.mlist'
        self.__gReg='g.region'
        
        self.__home=os.environ['HOME']
        self.__grassConfLi=grassConfigSect
        for tup in self.__grassConfLi:
            if 'env' in tup:
                self.__grassEnvFile=tup[1]
        
        #GRASS env    
        self.__grassEnv=self.__readGrassEnv()
        self.__grassRunEnv=self.__setGrassRunEnv(self.__grassEnv)  
        
        #GRASS DB/Files/General
        self.__rastList=self.__listRast()
        self.__region='NA'
        
        #GRASS module wrapper classes
        self.__grassDisplay=pGrassDisplay.gDisplay
        self.__grassRaster=pGrassRaster.gRast
     
    def __readGrassEnv(self):
        ''' parse the GRASS ENV file, setting os.environ values
        OUTPUT: Dictionary of Key Value pairs'''
        
        envFile='%s%s' % (self.__home,self.__grassEnvFile)
        envDict={}
        grassFile=open(envFile)
        for line in grassFile:
            kv=(line.rstrip()).split('=')
            if len(kv) > 1:
                kvV=kv[1].replace('"','')
            else:
                kvV=''
            kvK=kv[0]
            envDict[kvK]=kvV
            
        return envDict
    
    def __setGrassRunEnv(self,envDict):
        '''set the GRASS Runtime variables on the os
        INPUT: GRASS Env Vars dictionary
        '''
        for k,v in envDict.iteritems():
            os.environ[k]=v
    
    def __listRast(self):
        '''Get the all the rasters in the GRASS GIS DB.'''
        rastStr=grass.read_command(self.__gMList,'m',type='rast',separator=',')
        rastStr=rastStr.rstrip('\n')
        rastList=rastStr.split(',')
             
        return rastList
             
    #CLASS PROPERTIES
    @property
    def gRaster(self): 
        '''return the pGrassRaster object'''
        return self.__grassRaster
    
    def setRegion(self,mapRegion):
        '''set the region of the GRASS GIS'''
#        regParams='%s=%s' % (typ,mapRegion)
        grass.run_command(self.__gReg,rast=mapRegion)
        self.__region=mapRegion
    
    @property
    def getRegion(self):
        '''return the region of the GRASS GIS'''
        return self.__region
    @property
    def grassRastList(self):
        '''return the list of Rasters in the GRASS GIS'''
        return self.__rastList
    @property
    def gDisplay(self): 
        '''return the pGrassDisplay object'''
        return self.__grassDisplay
                  
    @property
    def grassEnvFile(self):
        '''return the GRASS env var file'''
        return self.__grassEnvFile
    @property
    def grassEnv(self):
        '''return the GRASS environment variables'''
        return self.__grassEnv       
 
# #####################################
#       ------ Functions --------
# #####################################
        
# ######################################
#       ------ Main --------
# ######################################        

# ######################################
#       ------ Unit Testing --------
# ######################################
if __name__=='__main__':
    import os
    import grass.script as grass
    from pprint import pprint as pp
    import sys
   
    def debug(msg):
        print msg

    start_main="Start main (%s)" % (__file__)
    end_main="End main (%s)" % (__file__)

    debug(start_main)
    #-- App Code start --#
    
    from ConfigParser import ConfigParser as configParser
    grassConf=configParser()
    grassConf.read('/Users/TPM/MyDocs/courses/spr2010/mea582_GeoMod/wkspc/src/app.ini')
    grassSect=grassConf.items('pGRASS')
    grassGisApp=grassApp(grassSect)
    grassEnvVars=grassGisApp.grassEnv
    #-- App Code end --#
    debug(end_main)
