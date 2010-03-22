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
        self.__rastList=self.__listRast()
        self.__curMapsetRastList=self.__listMapsetRast(self.__curMapset)
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
    
    def __listRast(self):
        '''Get the all the rasters in the GRASS GIS DB.'''
        rastStr=grass.read_command(self.__gMList,'m',type='rast',separator=',')
        rastStr=rastStr.rstrip('\n')
        rastList=rastStr.split(',')
             
        return rastList
    def __listMapsetRast(self,inMapset):
        '''Get the all the rasters in the mapset '''
        rastStr=grass.read_command(self.__gMList,type='rast',separator=',',mapset=inMapset)
        rastStr=rastStr.rstrip('\n')
        rastList=rastStr.split(',')
             
        return rastList
             
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
    gis_d=grassConf.get('data', 'gis_data')
    inDir=r'C:/MyDocs/projects/nc_res/Application/proto/Data/output/elev/basin/nc80'
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
    pp(grassGisApp.getCurMapset())       
#    if len(subFullNm) > 2:
#        sub= ('%s%s%s' % ((subFullNm[0])[:1], \
#                           ((subFullNm[1]).replace('a','').replace('e','').replace('i','').replace('o','').replace('u',''))[:2], \
#                           ((subFullNm[2]).replace('a','').replace('e','').replace('i','').replace('o','').replace('u',''))[:2]) \
#               ).lower()
#    elif len(subFullNm) > 1:
#        sub= ('%s%s' % ((subFullNm[0])[:1], \
#                         ((subFullNm[1]).replace('a','').replace('e','').replace('i','').replace('o','').replace('u',''))[:3]) \
#               ).lower()
#                        
#    else:
#        sub= (((subFullNm[0]).replace('a','').replace('e','').replace('i','').replace('o','').replace('u',''))[:5]).lower()
    
#    csv_d=grassConf.get('data', 'csv_data')
#    subCSV=r'%s/bsnCounties.csv' % (csv_d)
#    subRdr=csv.reader(open(subCSV,'rb'))
#    hdrRw=subRdr.next()
#    subCntyDict={}
#    for subRw in subRdr:
#        sub=(subRw[1]).lower()
#        cnty=(subRw[3]).lower()
#        if sub in subCntyDict:
#            subCntyDict[sub]='%s,%s' % (subCntyDict[sub],cnty)
#        else:
#            subCntyDict[sub]=cnty
#    
#    pp('----NO SET-------')
#    pp(subCntyDict)
#    cntyStr=subCntyDict['upperneuse']
#    cntyList=cntyStr.split(',')
#    for cnty in cntyList:
#        pp(cnty)
#    pp(len(cntyList))
#    pp(subCntyDict['upperneuse'])  

#    pp('----YES SET-------')
#    subSet=Set(subList)
#    cntySet=Set(cntyList)
#    subCntyDict={}
#    for subCnty in allSubCntyList:
#        sub=(subCnty.split('_'))[0]
#        cnty=(subCnty.split('_'))[1]
#        if sub in subCntyDict:
#            subCntyDict[sub]='%s,%s' % (subCntyDict[sub],cnty)
#        else:
#            subCntyDict[sub]=cnty
#
#    pp(subCntyDict)
#    cntyStr=subCntyDict['upperneuse']
#    cntyList=cntyStr.split(',')
#    for cnty in cntyList:
#        pp(cnty)
#    pp(len(cntyList))
#    pp(subCntyDict['upperneuse'])  
    
    
#    subRstList=grassGisApp.grassCurMapsetRastList
#    pp(subRstList)
#      
#    bsnRastList=grassGisApp.grassMapsetRastList
#    for bsnR in bsnSet:
#        if bsnR in bsnRastList:
#            pp(bsnR)
#        else:
#            pStr='%s NOT IN MAPSET' % (bsnR)
#            pp(pStr)
        
##        caps=re.search('[A-Z]*',bsn)
#        caps=re.findall('[A-Z]',bsn)
#        numCaps=len(caps)
#        pp(caps)
#        pp(numCaps)
##        for cap in caps:
##            
#        if len(caps) > 2:
#            sub= ('%s%s%s' % ((caps[0])[:1], \
#                           ((caps[1]).replace('a','').replace('e','').replace('i','').replace('o','').replace('u',''))[:2], \
#                           ((caps[2]).replace('a','').replace('e','').replace('i','').replace('o','').replace('u',''))[:2]) \
#               ).lower()
#        elif len(caps) > 1:
#            sub= ('%s%s' % ((caps[0])[:1], \
#                         ((caps[1]).replace('a','').replace('e','').replace('i','').replace('o','').replace('u',''))[:3]) \
#               ).lower()
#                        
#        else:
#            sub= (((caps[0]).replace('a','').replace('e','').replace('i','').replace('o','').replace('u',''))[:5]).lower()
#        
#        pp(sub)
#    for root,dirs,files in os.walk(inDir):
#        for rst in dirs:
##            if rst.startswith('lu'):
#            pp(rst)
#            gRast.importRast(inDir, rst)
                
    
#    nc80Hill='nc80_hill'
#    extRast='ctb'
#    pp(nc80Hill)
#    pp(grass.read_command('g.proj','w'))
    
#    gRast.importRast(inDir, nc80Hill)
#    gRast.linkRast(inDir, extRast)
#    rList=grassGisApp.grassRastList
#    pp(rList)
    
#    testR='upperneuse.basin10@tmorriss'
#    pp(testR)
    
#    gDisp=grassGisApp.gDisplay()
#    gDisp.outPNG(testR,r'C:/MyDocs')
#    gRast=grassGisApp.gRaster()
#    v_uns=gRast.convRtoV(testR)

    
    
#    grassGisApp.createMapset('subs')   
    pp(grassGisApp.getMapsets)
#    grass.run_command('g.gisenv',set="GISDBASE=C:\\MyDocs\\projects\\GISDBASE")
#    grass.run_command('g.gisenv',set="LOCATION_NAME=nc_res")
#    grass.run_command('g.gisenv',set="MAPSET=tmorriss")
##    GISDBASE: C:\MyDocs\projects\GISDBASE
##    LOCATION_NAME: nc_res
##    MAPSET: tmorriss
##    GRASS_GUI: wxpython
#    loc=grass.read_command('g.gisenv',get='LOCATION_NAME')
#    locPath=grass.read_command('g.gisenv',get='LOCATION')
#    pp(loc)
#    pp(locPath)
#    pp(grass.read_command('g.gisenv'))
#    pp(os.environ["GISRC"])
#    pp()
    #-- App Code end --#
    debug(end_main)
