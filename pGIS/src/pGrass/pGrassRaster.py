'''----------------------------------------------------------------------------------
 Module Name:          pGrass.pGrassRaster
 Source Name:           /Users/TPM/MyDocs/dev/gis/pgis/src/pGrass/pGrassRaster.py
 Version:               Python 2.6
 Author:                Timothy Morrissey, (timothy.morrissey@unc.edu)
 Date:                    Mar 16, 2010
 Required Argumuments:  
 Optional Arguments:    
 Description:         Wrapper class for the GRASS GIS raster module
 Documentation: 
----------------------------------------------------------------------------------'''
# #####################################
#       ------ Imports --------
# #####################################
# #####################################
#       ------ Imports --------
# #####################################
import os
import grass.script as grass
# ######################################
#       ------ Classes --------
# ######################################
class gRast():
    '''
    Class for raster module of GRASS GIS python application
    '''
    def __init__(self):
        #set the grass.raster (r.<name>) functions
        self.__rWatershed='r.watershed'
        self.__rReport='r.report'
        self.__rInfo='r.info'
        self.__rToV='r.to.vect'
        self.__rInArc='r.in.arc'
        self.__rInGDAL='r.in.gdal'
        self.__rExt='r.external'
        self.__rMask='r.mask'
        
        #Class vals
        
        #Class properties
        
    #Public Functions
    def setMask(self,inMask):
        '''
        Sets the processing mask for raster processing (r.mask)
        INPUT: map 
        '''
        grass.run_command(self.__rMask,input=inMask)
    def delMask(self):
        '''Deletes raster processing mask'''
        grass.run_command(self.__rMask,'r')
        
    def linkRast(self,inDir,inRast):
        '''
        Links external raster with GRASS DB (r.external)
        INPUT: dir (external raster dir)
               raster (external raster)
        '''
        curDir=os.getcwd()
        if os.path.exists(inDir):
            os.chdir(inDir)
        rastNm=inRast
        if inRast.endswith('.asc'):
            rastNm=inRast[:-4]   #strip .asc
        grass.run_command(self.__rExt,'o',input=inRast,output=rastNm)
        os.chdir(curDir)

    def importRast(self,inDir,inRast):
        '''
        Import raster into grassDB (binary) (r.in.arc)
        INPUT: raster
        '''
        curDir=os.getcwd()
        if os.path.exists(inDir):
            os.chdir(inDir)
#        else:
#            yield
        rastNm=inRast
        if inRast.endswith('.asc'):
            rastNm=inRast[:-4]   #strip .asc
            grass.run_command(self.__rInArc,input=inRast,output=rastNm)
        else:
            grass.run_command(self.__rInGDAL,'o',input=inRast,output=rastNm)
        os.chdir(curDir)
        
    def convRtoV(self,inRast,vType='area'):
        '''
        Convert raster to vector (r.to.vect)
        INPUT: raster
               vector type (point, line, area) 
        OUTPUT: vector name
        '''
        #Vect names can not contain . -> convert to _
        outVect=inRast.replace('.','_')
        grass.run_command(self.__rToV,input=inRast,output=outVect,feature=vType)
        
        return outVect
#        r.to.vect -b in=$basin out="${catch}" feature=area
    def calcWatershed(self,inRast,inThresh,inDA):
        '''
            Run r.watershed GRASS function.
            INPUT: inRast (input raster of elevation)
                   inThres (threshold value (#cells) for basin)
                   inDA (drainage area based on inThres)
            OUTPUT: wshedDict (dictionary of elev, drain, basin, stream, flow accumulation rasters and threshold value)
        '''
        rDrain='%s.drain%s' % (inRast,inDA) 
        rBasin='%s.basin%s' % (inRast,inDA)
        rStream='%s.strms%s' % (inRast,inDA)
        rAccum='%s.accum%s' % (inRast,inDA) 
        rThresh=inThresh
#        grass.run_command('g.region', rast=inRast)
        grass.run_command(self.__rWatershed, '-o', elev=inRast, drain=rDrain, basin=rBasin, stream=rStream, accumulation=rAccum, thres=rThresh)
        
        wshedDict={}
        wshedDict['elev']=inRast
        wshedDict['drain']=rDrain
        wshedDict['basin']=rBasin
        wshedDict['stream']=rStream
        wshedDict['flAccum']=rAccum
        wshedDict['thres']=rThresh
        
        return wshedDict
    
    def getRasterRes(self,inRast):
        '''
        Run r.info with -s flag for raster resolution
        INPUT: inRast (raster)
        OUTPUT: resolution 
        '''
        rawRes=grass.read_command(self.__rInfo,flags='s',map=inRast)
        res=((rawRes.split('='))[2]).rstrip('\n')
        return res
    
    def rasterReport(self,inRast):
        '''
            Run r.report GRASS function.
            INPUT: inRast 
            OUTPUT: raster report
        '''
        return grass.read_command(self.__rReport,flags='-q',map=inRast)
    
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
       def debug(msg):
              print msg

       start_main="Start main (%s)" % (__file__)
       end_main="End main (%s)" % (__file__)

       debug(start_main)
       #-- App Code start --#
#       import os
#       import grass.script as grass
       from pprint import pprint as pp
       from ConfigParser import ConfigParser as configParser
       
       grassConf=configParser()
       grassConf.read(r'C:\MyDocs\projects\eclipse_wkspc\ncres_app\src\app.ini')
       grassSect=grassConf.items('pGRASS')
       
       rast=gRast()
       pp(rast)
       #-- App Code end --#
       debug(end_main)
