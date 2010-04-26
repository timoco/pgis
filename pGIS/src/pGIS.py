'''----------------------------------------------------------------------------------
 Module Name:         pGIS
 Source Name:      /Users/TPM/MyDocs/dev/gis/pgis/src/pGIS.py
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
from ConfigParser import ConfigParser as configParser
import os
#from pGrass import pGrass as grassGIS
from pGrass import pGrass as grassGIS

# ######################################
#       ------ Classes --------
# ######################################
class gisApp():
    '''
    Instance of a pGIS application
    '''
    def __init__(self,appID):
        self.__os=os.name
        self.__home=os.getenv('HOME')
        self.__gisPath=os.path.dirname(__file__)
        
        #pGIS configuration
        self.__appId=appID
        gisConf=configParser()
        gisConf.read('%s/config/pGIS_conf.ini' % (self.__gisPath))
        self.__appType=gisConf.get('app','app_type')
        self.__appRoot='%s%s' % (self.__home,gisConf.get(self.__appId,'app_root'))
        self.__appConf='%s%s' % (self.__appRoot,gisConf.get(self.__appId,'app_conf'))
        
        #pGIS application
        appConf=configParser()
        appConf.read(self.__appConf)
        self.__appConfObj=appConf
        self.__hasEmail=appConf.get(self.__appType,'email')
        self.__hasGrass=appConf.get(self.__appType,'grass')
        self.__hasArc=appConf.get(self.__appType,'arc')
        self.__appData=appConf.items('data')
        self.__appDataDict=self.__createAppData()
        self.__appAppRoot='%s%s' % (self.__home,self.__appDataDict['app_root'])
        self.__projRoot='%s%s' % (self.__home,self.__appDataDict['proj_root'])
        self.__gisDir='%s%s' % (self.__home,self.__appDataDict['gis_data'])
        self.__rastDir='%s%s' % (self.__home,self.__appDataDict['rast_data'])
        self.__vectDir='%s%s' % (self.__home,self.__appDataDict['vect_data'])
        self.__zonalDir='%s%s' % (self.__home,self.__appDataDict['zonal_data'])
        self.__csvDir='%s%s' % (self.__home,self.__appDataDict['csv_data'])
        self.__tblDir='%s%s' % (self.__home,self.__appDataDict['tbl_data'])
        self.__dataSrc=self.__appDataDict['data_src']
        self.__outDir='%s%s' % (self.__home,self.__appDataDict['out_dir'])
        
        
        if self.__hasGrass:
            self.__grassApp=self.__createGrassApp()
        if self.__hasArc:
            self.__arcApp=self.__createArcApp()
        if self.__hasEmail:
            self.emailApp=self.__createEmailApp()
            
    #Private functions
    def __createAppData(self):
        '''parse the data config into dictionary'''
        dataDict={}
        for kv in self.__appData:
            kvK=kv[0].replace('"','')
            kvV=kv[1].replace('"','')
        
            dataDict[kvK]=kvV
        
        return dataDict
    
    def __createGrassApp(self):
        '''initialize pGrass for pGIS'''
#        from pGrass import pGrass as grassGIS
#        from pGrass import pGrass as grassGIS
#        from pGrass import pGrass as grassGIS
#        grassGIS=pGrass
        grsApp=grassGIS.grassApp(self.__appConfObj.items('pGRASS'))
        return grsApp
    
    def __createArcApp(self):
        '''initialize pArc for pGIS'''
        from pArc import pArc as arcGIS
        arcApp=arcGIS.arcApp(self.__appConfObj.items('pARC'))
        return arcApp
    
    def __createEmailApp(self):
        '''initialize email for pGIS'''
#        emailApp=self.__appConfObj.items('EMAIL')
        emailApp={}
        emailApp['server']=self.__appConfObj.get('EMAIL', 'server')
        emailApp['port']=self.__appConfObj.get('EMAIL', 'port')
        emailApp['addr_to']=self.__appConfObj.get('EMAIL', 'addr_to')
        emailApp['addr_from']=self.__appConfObj.get('EMAIL', 'addr_from')
        return emailApp
     
    @property
    def appProjRoot(self):
        '''return the pGIS implementation project root'''
        return self.__projRoot
    @property
    def appAppRoot(self):
        '''return the pGIS implementation app root'''
        return self.__appAppRoot
    @property
    def appGisDir(self):
        '''return the pGIS implementation gis data dir'''
        return self.__gisDir
    @property
    def appRastDir(self):
        '''return the pGIS implementation raster data dir'''
        return self.__rastDir
    @property
    def appVectDir(self):
        '''return the pGIS implementation vector data dir'''
        return self.__vectDir
    @property
    def appZonalDir(self):
        '''return the pGIS implementation vector zonal data dir'''
        return self.__zonalDir
    @property
    def appCsvDir(self):
        '''return the pGIS implementation csv data dir'''
        return self.__csvDir
    @property
    def appTblDir(self):
        '''return the pGIS implementation tbl data dir'''
        return self.__tblDir
    @property
    def appDataSrc(self):
        '''return the pGIS implementation data source'''
        return self.__dataSrc
    @property
    def appOutDir(self):
        '''return the pGIS implementation output data dir'''
        return self.__outDir
    
    @property
    def appData(self):
        '''return the data config as dictionary'''
        return self.__appDataDict
    
    @property
    def os(self):
        '''return the OS of the pGIS application'''
        return self.__os
    @property
    def home(self):
        '''return the Home directory of pGIS'''
        return self.__home
    @property
    def appRoot(self):
        ''' return the pGIS application implementation root'''
        return self.__appRoot
    @property 
    def appConf(self):
        '''return the pGIS application implementation conf file'''
        return self.__appConf
    @property
    def appConfObj(self):
        '''return the pGIS application implementation config obj'''
        return self.__appConfObj
    @property
    def hasEmail(self):
        '''return the pGIS application implementation EMAIL capabilities (True/False)'''
        return self.__hasEmail
    @property
    def hasGrass(self):
        '''return the pGIS application implementation GRASS capabilities (True/False)'''
        return self.__hasGrass
    @property
    def hasArc(self):
        '''return the pGIS application implementation ArcGIS capabilities (True/False)'''
        return self.__hasArc
    @property
    def grassApp(self):
        '''return the pGIS application implementation pGrass object'''
        return self.__grassApp
    @property
    def arcApp(self):
        '''return the pGIS application implementation pArc object'''
        return self.__arcApp
    
    
    
    
# #####################################
#       ------ Functions --------
# #####################################

#def createGrassApp():
#    '''initialize pGrass for pGIS'''
#    grassApp=grassGIS.grassApp('CONFIG PARAMS')
# ######################################
#       ------ Main --------
# ######################################


# ######################################
#       ------ Unit Testing --------
# ######################################
if __name__=='__main__':
    from pprint import pprint as pp
    def debug(msg):
        pp(msg)

    start_main="Start main (%s)" % (__file__)
    end_main="End main (%s)" % (__file__)

    debug(start_main)
    #-- App Code start --#
    appID_ncres='ncres'
    appID_geomod='geomod'
    appID='ncres'
    app=gisApp(appID)
    pp(app.appAppRoot)
    pp(app.appOutDir)
#    arc=app.arcApp
#    gp=arc.getGP
    pp(app.emailApp)
#    arc=app.arcApp
#    gp=arc.getGP
    
#    grass=app.grassApp
#    arc=app.arcApp
#    pp(app.appData)
#    pp(grass.grassEnv)
#    pp(app.hasEmail)
#    pp(arc)
#    pp(grassGIS.main())
#    for kv in (os.environ.items()):
#        pp(kv)
##        
    
    #-- App Code end --#
    debug(end_main)
