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
import pGrassVector

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
        self.__gEnv='g.gisenv'
        self.__gMapset='g.mapset'
        self.__gMapsets='g.mapsets'
        self.__home=os.environ['HOME']
        self.__grassConfLi=grassConfigSect
        for tup in self.__grassConfLi:
            if 'env' in tup:
                self.__grassEnvFile=tup[1]
        
        #GRASS env    
        self.__grassEnv=self.__readGrassEnv()
        self.__grassRunEnv=self.__setGrassRunEnv(self.__grassEnv)  
        self.__gisLock=self.__createGISLock()
        
        #GRASS DB/Files/General
        self.__curGISDB=self.__getCurDB()
        self.__curLoc=self.__getCurLoc()
        self.__curMapset=self.__getCurMapset()
        self.__mapsets=self.__getMapsets()
        self.__rastList=self.__listDatasets('rast')
        self.__curMapsetRastList=self.__listMapsetDatasets(self.__curMapset, 'rast')
        self.__permMapsetRastList=self.__listMapsetDatasets('PERMANENT', 'rast')
        self.__vectList=self.__listDatasets('vect')
        self.__curMapsetVectList=self.__listMapsetDatasets(self.__curMapset, 'vect')
        self.__permMapsetVectList=self.__listMapsetDatasets('PERMANENT', 'vect')
        
        self.__region='NA'
                
        #GRASS module wrapper classes
        self.__grassDisplay=pGrassDisplay.gDisplay
        self.__grassRaster=pGrassRaster.gRast
        self.__grassVector=pGrassVector.gVect
     
    def createMapset(self,inMapset):
        '''create a mapset in the current location and gisdbase'''
        grass.run_command(self.__gMapset,'c',mapset=inMapset,location=self.__curLoc,gisdbase=self.__curGISDB)
    
    def __getCurDB(self):
        '''return the current gisDB'''
        return (grass.read_command(self.__gEnv,get='GISDBASE')).rstrip('\n')
    def __getCurLoc(self):
        '''return the current location'''
        return (grass.read_command(self.__gEnv,get='LOCATION_NAME')).rstrip('\n')
    def __getMapsets(self):
        '''return the mapsets'''
        mapsetsList=(grass.read_command(self.__gMapset,'l')).rstrip('\n')
        return mapsetsList
    def __getCurMapset(self):
        '''return the current mapset'''
        return (grass.read_command(self.__gEnv,get='MAPSET')).rstrip('\n')
        
    def __createGISLock(self):
        '''create the GIS_LOCK env var'''
        kv='%s=%s' % ('GIS_LOCK',str(os.getpid()))
        os.environ['GIS_LOCK']=str(os.getpid())
        grass.run_command(self.__gEnv,set=kv)
        
    def __readGrassEnv(self):
        ''' parse the GRASS ENV file, setting os.environ values
        OUTPUT: Dictionary of Key Value pairs'''
        
        envFile='%s%s' % (self.__home,self.__grassEnvFile)
        envDict={}
        grassFile=open(envFile,'rb')
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
#            os.environ[k]=v
            kv='%s=%s' %(k,v)
            grass.run_command(self.__gEnv,set=kv)
    
    def __listDatasets(self,dsTyp):
        '''Get the all the datasets in the GRASS GIS DB by data type'''
        dsStr=grass.read_command(self.__gMList,'m',type=dsTyp,separator=',')
        dsStr=dsStr.rstrip('\n')
        dsList=dsStr.split(',')
        return dsList
    
    def __listMapsetDatasets(self,inMapset,dsTyp):
        '''Get the all the rasters in the mapset '''
        dsStr=grass.read_command(self.__gMList,type=dsTyp,separator=',',mapset=inMapset)
        dsStr=dsStr.rstrip('\n')
        dsList=dsStr.split(',')
        return dsList
             
    #CLASS PROPERTIES
    @property
    def getMapsets(self): 
        '''return the Mapsets of the location and gisdb'''
        return self.__mapsets
    def getCurMapset(self): 
        '''return the current Mapset'''
        return self.__curMapset
    def setCurMapset(self,inMapset):
        '''set the current mapset'''
        if inMapset in self.__mapsets:
            kv='%s=%s' %('MAPSET',inMapset)
            grass.run_command(self.__gEnv,set=kv)
            self.__curMapset=inMapset
    curMapset=property(getCurMapset,setCurMapset)
    
    @property
    def gVector(self): 
        '''return the pGrassVector object'''
        return self.__grassVector
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
        if self.__region=='NA':
            return 'ERROR - region not set'
        else:
            regionStr=grass.read_command(self.__gReg,'g')
            regionList=regionStr.split('\n')
        return regionList
    @property
    def grassRastList(self):
        '''return the list of all Rasters in the GRASS GIS'''
        return self.__rastList
    @property
    def grassCurMapsetRastList(self):
        '''return the list of Rasters in the current GRASS GIS mapset'''
        return self.__curMapsetRastList
    @property
    def grassPermRastList(self):
        '''return the list of Rasters in the PERMANENT GRASS GIS mapset'''
        return self.__permMapsetRastList
    @property
    def grassVectList(self):
        '''return the list of all vectors in the GRASS GIS'''
        return self.__vectList
    @property
    def grassCurMapsetVectList(self):
        '''return the list of vectors in the current GRASS GIS mapset'''
        return self.__curMapsetVectList
    @property
    def grassPermVectList(self):
        '''return the list of vectors in the PERMANENT GRASS GIS mapset'''
        return self.__permMapsetVectList
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
    import csv
    import re
    from sets import Set
   
    def debug(msg):
        print msg

    start_main="Start main (%s)" % (__file__)
    end_main="End main (%s)" % (__file__)

    debug(start_main)
    #-- App Code start --#
    
    from ConfigParser import ConfigParser as configParser
    grassConf=configParser()
    grassConf.read(r'C:\MyDocs\projects\eclipse_wkspc\ncres_app\src\app.ini')
    grassSect=grassConf.items('pGRASS')
    grassGisApp=grassApp(grassSect)
    grassEnvVars=grassGisApp.grassEnv
    grassGisApp.setCurMapset('subs')
    gRast=grassGisApp.gRaster()
    #test import raster
#    gis_d=grassConf.get('data', 'gis_data')
#    inDir=r'C:/MyDocs/projects/nc_res/Application/proto/Data/output/elev/basin/nc80'
#    ncSecL=os.listdir(inDir)
#    for ncSecD in ncSecL:
#        if os.path.isdir('%s/%s'%(inDir,ncSecD)):
#            pp(ncSecD)
    
#    for root,dirs,files in os.walk(inDir):
#        for sub in dirs:
#            pp(sub)
#            cpCMD='%s@PERMANENT,%s' %(sub,sub)
#            pp(cpCMD)
#            grass.run_command('g.copy',rast=cpCMD)
#            if not cnty.endswith('NC'):
#                gRast.importRast(root, cnty)
#    pp(grassGisApp.getCurMapset())   
    pp(grassGisApp.getMapsets)
    curMpset=grassGisApp.getCurMapset()
    pp(curMpset)
    allRast=grassGisApp.grassRastList
    permMpRast=grassGisApp.grassPermRastList
    curMpRast=grassGisApp.grassCurMapsetRastList
#    pp(curMpRast)
#    pp(permMpRast)
#    pp(allRast)
    allV=grassGisApp.grassVectList
    permVectL=grassGisApp.grassPermVectList
    curMpVectList=grassGisApp.grassCurMapsetVectList
    pp(allV)
    pp(permVectL)
    pp(curMpVectList)

#    pp('CURRENT : %s' % (curMpset))
#    pp(curMpRast)
###    gRast.delMask
##    pp('PERM')
#    pp(permMpRast)
#    for rst in curMpRast:
#        if rst in permMpRast:
##            pp('%s in MAPSETS: %s & PERMANENT : g.remove from %s' % (rst,curMpset,curMpset))
#            grass.run_command('g.mremove','f',rast=rst)
#            pp('%s removed from %s MAPSET' % (rst,curMpset))
#        else:
#            pp('%s only in in %s' % (rst,curMpset))

#    
    #clean
    def cleanWshedVect():
        for wshedV in curMpVectList:
            if not wshedV.startswith('upperneuse'):
                pp(wshedV)   
                grass.run_command('g.mremove','f',vect=wshedV)
    def cleanWshed():
        for wshedR in curMpRast:
            if wshedR.endswith('.cnty20'):
                pp(wshedR)   
                grass.run_command('g.mremove','f',rast=wshedR)
    
#    cleanWshedVect()
#    cleanWshed()

    #get some vect atts
    vAttStr=grass.read_command('v.db.select','c',map='upperneuse_basin25',fs=',')
    vAttL=vAttStr.split('\n')
    pp(vAttL)
    vReport=grass.read_command('v.report','r',map='upperneuse_basin25',option='area',units='mi')
    pp(vReport)
    vReportL=vReport.split('\n')
    pp(vReportL)
    pp(grass.read_command('v.info',map='upperneuse_basin25'))
    vStats=grass.read_command('v.univar','g',map='upperneuse_basin25',col='area_sqmi',type='area')
    vStatsL=vStats.split('\n')
    pp(vStatsL)
    vStatsDict={}
    for stat in vStatsL:
        kv=stat.split('=')
        if len(kv) > 1:
            vStatsDict[kv[0]]=kv[1]
        
    pp(vStatsDict)  
    pp(vStatsDict['min'])  
    #-- App Code end --#
    debug(end_main)
