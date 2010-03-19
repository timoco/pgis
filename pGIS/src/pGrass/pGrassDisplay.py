'''----------------------------------------------------------------------------------
 Module Name:          pGrass.pGrassDisplay
 Source Name:          /Users/TPM/MyDocs/dev/gis/pgis/src/pGrass/pGrassDisplay.py
 Version:              Python 2.6
 Author:               Timothy Morrissey, (timothy.morrissey@unc.edu)
 Date:                 Mar 14, 2010
 Required Argumuments:  
 Optional Arguments:    
 Description:          Wrapper class for the GRASS GIS display module
 Documentation: 
----------------------------------------------------------------------------------'''
# #####################################
#       ------ Imports --------
# #####################################
import os
import grass.script as grass
# ######################################
#       ------ Classes --------
# ######################################
class gDisplay():
    '''
    Class for display module of GRASS GIS python application
    '''
    def __init__(self):
        #set the grass.display (d.<name>) functions
        self.__dMon='d.mon'
        self.__dMonSize='d.monsize'
        self.__dOutFile='d.out.file'
        self.__dRast='d.rast'
        self.__dLeg='d.legend'
        self.__dNViz='nviz'
        self.__gEnv='g.gisenv'
        self.__curMon=self.__getCurMon()
        
    #Private     
    def __getCurMon(self):
        '''Private return the currently running monitor'''
        curMon = grass.read_command(self.__dMon,'p')
        if curMon.startswith('No'):
            retVal='NA'
        else:
            retVal='%s'%(curMon[-3:-1])
            
        return retVal
            
    #Public
    def startMon(self):
        '''Method for starting a display monitor'''
        os.environ['GIS_LOCK']=str(os.getpid())
        curMon=self.__curMon
        if curMon == 'NA':
            grass.run_command(self.__dMon, start='x0')
        else:
            grass.run_command(self.__dMonSize, setmonitor=curMon, setwidth=1200, setheight=800)
    
    def eraseMon(self):
        '''Erase the current monitor display'''
        grass.run_command('d.erase')
        
    def stopMon(self):
        '''Stop the current monitor'''
        curMon=grass.read_command(self.__dMon,stop=self.__getCurMon())
        
    def outPNG(self,outMap,outDir=''):
        '''Write File to PNG
        INPUT: map to be outputted as PNG
        OPT INPUT : [output Directory] default is from config
        '''
        outFile='%s.png' %(outMap)
#       export GRASS_PNGFILE
#        env=grass.gisenv()
        pngVar='GRASS_PNGFILE=%s' %(outFile)
        grass.run_command(self.__gEnv,set=pngVar)
#        env['GRASS_PNGFILE']=
        
        if len(outDir) < 1:
            outDir='output path from ini'
            
        outMapPng=outMap[0]
#        grass.run_command(self.__dMon,start='PNG')
#        grass.run_command(self.__dOutFile, out=r'%s/%s' % (outDir,outMapPng), format='png')
        self.dRast(outMap)
        grass.run_command(self.__dMon,stop='PNG')
            
    def dRast(self,rast,loc='2,40,2,6'):
        '''
        Display raster on running monitor
        INPUT: rast
        OPT INPUT:[legend location]
        '''    
        grass.run_command(self.__dRast,map=rast)
        grass.run_command(self.__dLeg, map=rast, at=loc)

    def showNVIZ(self,rast, col=''):
        '''
        Displays the raster in the NVIZ 3D utility
        INPUT: raster
        OPT INPUT: [color]
        '''
        grass.run_command(self.__dNViz,elevation=rast,color=col)
        

    
    
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
    from ConfigParser import ConfigParser as configParser
#    import pGIS 
    
    def debug(msg):
        print msg

    start_main="Start main (%s)" % (__file__)
    end_main="End main (%s)" % (__file__)

    debug(start_main)
    #-- App Code start --#
    grassConf=configParser()
    grassConf.read(r'C:\MyDocs\projects\eclipse_wkspc\pGIS_Test\src\app.ini')
    grassSect=grassConf.items('pGRASS')
    gDisp=gDisplay()
#    grass.run_command('d.mon',start='PNG')
    
#    curMon = grass.read_command('d.mon','L')
#    if curMon.startswith('No'):
#        retVal='NA'
#    else:
#        retVal='%s'%(curMon[-3:-1])
#    pp(curMon)
##    gDisp.startMon()
#    testGisApp=pGIS.gisApp('geomod')
#    grassGisApp=testGisApp.grassApp()
#    grassEnvVars=grassGisApp.grassEnv
       
       
       
    
#    displ.startMon()
#    displ.eraseMon()
#    displ.stopMon()
    #-- App Code end --#
    debug(end_main)
