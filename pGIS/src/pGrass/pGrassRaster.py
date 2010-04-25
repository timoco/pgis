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
        self.__rLake='r.lake'
        self.__rWaterOutlet='r.water.outlet'
        self.__rVolume='r.volume'
        self.__rSurfArea='r.surf.area'
        self.__rReport='r.report'
        self.__rInfo='r.info'
        self.__rToV='r.to.vect'
        self.__rThin='r.thin'
        self.__rInArc='r.in.arc'
        self.__rInGDAL='r.in.gdal'
        self.__rOutGDAL='r.out.gdal'
        self.__rExt='r.external'
        self.__rMask='r.mask'
        self.__rShade='r.shaded.relief'
        self.__rColors='r.colors'
        self.__rPatch='r.patch'
        self.__rStats='r.univar'
        self.__rWhat='r.what'
        self.__rNull='r.null'
        self.__rRegion='r.region'

        #Class vals
        self.__mask='NA'
        #Class properties
        
    #Public Functions
    def nullToZero(self,inRast):
        '''Reclass NULL to Zero for Raster
        INPUT: inRast'''
        grass.run_command(self.__rNull,map=inRast,setnull=0)
        
    def queryRaster(self,inRast,inCoord):
        '''Query raster by coordinate
        INPUT: raster 
               coordinate 
        OUTPUT: queryVal
        '''
        cmdOut=(grass.read_command(self.__rWhat,input=inRast,east_north=inCoord)).rstrip('\n')
        outValLi=cmdOut.split('|')
        for val in outValLi:
            if ((len(val)>0) and (not val in inCoord)):
                outVal=val
        return outVal
        
    def mosaicRasters(self,inRstList,outRstNm,overWrt=False):
        '''Create a mosaic'd raster from the input raster list (r.patch)
        INPUT: list (rasters to be mosaic'd)
               string (output mosaic name)
        OUTPUT: string (output mosaic name)
        '''
        inRstStr=','.join(inRstList)
        retVal=grass.run_command(self.__rPatch,overwrite=overWrt,input=inRstStr,output=outRstNm)
        if retVal==0:
            return outRstNm
        else:
            return None
            
    def outGTiff(self,inRast,outDir):
        '''Output a geo-referenced TIFF of input raster via gdal
        INPUT: rast
        OUTPUT: geoTIFF
        '''
        outGTiff='%s/%s.tif' % (outDir,inRast)
        outType='GTiff'
        outOpt='TFW=YES'
        self.__outGDAL(inRast,outGTiff, outType, outOpt)
        
    def __outGDAL(self,inRast,outNm,outType,outOpt=''):
        '''Output a raster via gdal to input type
        INPUT: rast
                output name
               output format (ex.GeoTIFF)
               output option (create option name/value pair, ex. TFW=YES
        OUTPUT: outNm
        '''    
        grass.run_command(self.__rOutGDAL,input=inRast,format=outType,output=outNm,createopt=outOpt)

    def setElevColor(self,inRast):
        '''Set the color scheme for the inRast for elevation
        INPUT: rast'''
        rastCol='elevation'
        self.__setRastColors(inRast, rastCol)
        
    def __setRastColors(self,inRast,inCol):
        '''Set the color scheme for the inRast
        INPUT:  rast
                color'''
        grass.run_command(self.__rColors,map=inRast,color=inCol)
        
    def createRelief(self,inRast,overWrt=False):
        '''Creates a shaded relief raster from input
        INPUT: rast
        OUTPUT: shaded rastNm'''
        shdRast='%s.shade' % (inRast)
        grass.run_command(self.__rShade,overwrite=overWrt,map=inRast,shadedmap=shdRast)
        return shdRast
    
    def hasMask(self):
        '''Returns if a raster mask has been created'''
        maskSet=True
        if self.__mask == 'NA':
            maskSet=False
        return maskSet
    def getMask(self):
        '''Returns if a raster mask'''
        return self.__mask
    
    def setMask(self,inMask):
        '''
        Sets the processing mask for raster processing (r.mask)
        INPUT: map 
        '''
        #first delete the mask
        self.delMask()
        grass.run_command(self.__rMask,'o',input=inMask)
        self.__mask=inMask
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
        
    
    def convRtoV(self,inRast,vType='area',overWrt=False):
        '''
        Convert raster to vector (r.to.vect)
        INPUT: raster
               vector type (point, line, area) 
        OUTPUT: vector name
        '''
        #thin lines
        convRast=inRast
        flag='s'
        if vType=='line':
            grass.run_command(self.__rThin,overwrite=True,input=inRast,output='strm.thin')
        #Vect names can not contain . -> convert to _
        outVect=inRast.replace('.','_')
        retVal=grass.run_command(self.__rToV,flag,overwrite=overWrt,input=convRast,output=outVect,feature=vType)
        if retVal==0:
            return outVect
        else:
            return None

    
    def fillLake(self,inRast,inWaterLvl,inCoord,overWrt=False):
        '''
            Creates a raster lake representing lake depth (r.lake).
            INPUT: inRast (input raster of elevation)
                   inWaterLvl (float for water level -> depth of lake)
                   inCoord (X,Y coordinate to serve as seed point)
            OUTPUT: outLake (raster of lake)
        '''
        outLake='%s.lake' % (inRast)
        grass.run_command(self.__rLake,overwrite=overWrt,dem=inRast,wl=inWaterLvl,xy=inCoord,lake=outLake)
        return outLake
    
    def calcWatershedCatchments(self,inRast,inThresh):
        '''
            Run r.watershed GRASS function.
            INPUT: inRast (input raster of elevation)
                   inThres (threshold value (#cells) for basin)
            OUTPUT: basinName (string)
        '''
        outBasinNm='%s.catchments' % inRast
        retVal=grass.run_command(self.__rWatershed,'m',elevation=inRast,basin=outBasinNm,thres=inThresh,memory=1200)
        if retVal==0:
            return outBasinNm
        else:
            return None 
    def calcWatershedDrainStream(self,inRast,inDrainNm,inStreamNm,inThresh,inMem):
        '''
            Run r.watershed GRASS function.
            INPUT: inRast (input raster of elevation)
                   inThres (threshold value (#cells) for basin)
            OUTPUT: hydroDict (dict of drain & stream rasters)
        '''
        hydroDict={}
        hydroDict['drain']=inDrainNm
        hydroDict['stream']=inStreamNm
        retVal=grass.run_command(self.__rWatershed,'m',elevation=inRast,drain=inDrainNm,stream=inStreaNm,threshold=inThresh,memory=inMem)
#        r.watershed -m elev=$sub20 stream=$sub20catch_streamRast drain=$sub20catch_drain threshold=$threshold20 memory=$wshedMem 
        if retVal==0:
            return hydroDict
        else:
            return None        
        
    def calcWatershed(self,inRast,inThresh,inDA,subId='',overwrt=False):
        '''
            Run r.watershed GRASS function.
            INPUT: inRast (input raster of elevation)
                   inThres (threshold value (#cells) for basin)
                   inDA (drainage area based on inThres)
            OUTPUT: wshedDict (dictionary of elev, drain, basin, stream, flow accumulation rasters and threshold value)
        '''
        outRastBase=inRast
        if len(subId)>0:
            outRastBase=inRast.replace('cnty20',subId)
            
        rDrain='%s.drain%s' % (outRastBase,inDA) 
        rBasin='%s.basin%s' % (outRastBase,inDA)
        rStream='%s.strms%s' % (outRastBase,inDA)
        rAccum='%s.accum%s' % (outRastBase,inDA) 
        rThresh=inThresh
        grass.run_command(self.__rWatershed,'m',overwrite=overwrt,elevation=inRast, drain=rDrain, basin=rBasin, stream=rStream, accumulation=rAccum,thres=rThresh,memory=1000)
        wshedDict={}
        wshedDict['elev']=inRast
        wshedDict['drain']=rDrain
        wshedDict['basin']=rBasin
        wshedDict['stream']=rStream
        wshedDict['flAccum']=rAccum
        wshedDict['thres']=rThresh
        
        return wshedDict
    
    def calcWaterOutlet(self,inDrain,inCoordX,inCoordY,outBasinNm):
        '''
            Run r.water.outlet GRASS function.
            INPUT: inDrain (input raster of drainage from r.watershed)
                   inCoordX (easting coordinate for outlet point)
                   inCoordY (northing coordinate for outlet point)
                   outBasinNm (name for output basin)
            OUTPUT: raster (out of basin from outlet)
        '''
        grass.run_command(self.__rWaterOutlet,drainage=inDrain,easting=inCoordX,northing=inCoordY,basin=outBasinNm)
        #r.water.outlet --overwrite drainage="$catch_drain" easting="$damX" northing="$damY" basin="$damBasin"
        return outBasinNm 

    def calcWShedBasin(self,inRast,inThresh,inDA,overwrt=False):
        '''
            Run r.watershed GRASS function.
            INPUT: inRast (input raster of elevation)
                   inThres (threshold value (#cells) for basin)
                   inDA (drainage area based on inThres)
            OUTPUT: wshedDict (dictionary of elev, basin, rasters and threshold value)
        '''
        #get the resolution
        rastRes=self.getRasterRes(inRast)
        if rastRes=='20':
            #set the name with the mask
            rastMask=self.getMask()
            suffix=(rastMask.split('.'))[2] # ex) upneuse.basin10.6 -> 6
            rBasin='%s.basin%s.%s' % (inRast,inDA,suffix)
            rStream='%s.strms%s.%s' % (inRast,inDA,suffix)
            rDrain='%s.drain%s.%s' % (inRast,inDA,suffix)
            rAccum='%s.flwaccum%s.%s' % (inRast,inDA,suffix)
        else: 
            rBasin='%s.basin%s' % (inRast,inDA)
            rStream='%s.strms%s' % (inRast,inDA)
            rDrain='%s.drain%s' % (inRast,inDA)
            rAccum='%s.flwaccum%s' % (inRast,inDA)
        rThresh=inThresh
        grass.run_command(self.__rWatershed,'m',overwrite=overwrt, elev=inRast, basin=rBasin, drain=rDrain,accumulation=rAccum,stream=rStream, thres=rThresh,memory=1000)
        wshedDict={}
        wshedDict['elev']=inRast
        wshedDict['basin']=rBasin
        wshedDict['stream']=rStream
        wshedDict['drain']=rDrain
        wshedDict['flAccum']=rAccum
        wshedDict['thres']=rThresh
        return wshedDict
    def createLake(self,inRast,inLvl,inX,inY):
        '''
            Run r.lake GRASS function.
            INPUT: inRast (input raster of elevation)
                    inLvl (fill level)
                   inX (E coord point for fill)
                   inY (N coord point for fill)
            OUTPUT: outLake
        '''
#        #set the g.region and r.mask
#        g.region rast=$dem
#        r.mask input=$dem
#        #create output product names
#        elev=$dem
#        lake="${dem}.lake_${IN_WTR_LVL}"
#        r.lake dem=$elev lake=$lake wl=$IN_WTR_LVL seed=$IN_RST_SEED
        outLake='%s.lake%s' % (inRast,inLvl)
        seedXY='%s,%s' % (inX,inY)
        grass.run_command(self.__rLake,dem=inRast,wl=inLvl,lake=outLake,xy=seedXY)
        return outLake
    
    def calcVolume(self,inRast):
        '''
        Run r.volume 
        INPUT: inRast (raster)
        OUTPUT: list (volume, centroid vector) 
        '''
        outCentroidV='%s_centrd' % (inRast.replace('.','_'))
        rawVol=grass.read_command(self.__rVolume,'f',overwrite=True,quiet=True,data=inRast,centroids=outCentroidV)
        outVol=((rawVol[rawVol.rfind(':'):]).rstrip('\n\n')).lstrip(':')
        return outVol
        
    def calcSurfArea(self,inRast):
        '''
        Run r.surf.area 
        INPUT: inRast (raster)
        OUTPUT: surfArea 
        '''
        self.setRegion(inRast)
        rawSurfArea=grass.read_command(self.__rSurfArea,quiet=True,input=inRast)
        outSurfArea='%f' % (float(((rawSurfArea[rawSurfArea.rfind(':'):-7]).rstrip('\n\n')).lstrip(': ')))
        return outSurfArea

    def getRasterRes(self,inRast):
        '''
        Run r.info with -s flag for raster resolution
        INPUT: inRast (raster)
        OUTPUT: resolution 
        '''
        rawRes=grass.read_command(self.__rInfo,flags='s',map=inRast)
        res=((rawRes.split('='))[2]).rstrip('\n')
        return res
    
    def rastStats(self,inRast):
        '''
        Return the univar statistics of #,# missing, # null, min, max, & range of raster
        INPUT: raster
        OUTPUT: dictionary (stats)
        '''
        rStats=grass.read_command(self.__rStats,'g',map=inRast)
        rStatsL=rStats.split('\n')
        rStatsDict={}
        for stat in rStatsL:
            kv=stat.split('=')
            if len(kv) > 1:
                rStatsDict[kv[0]]=kv[1]
        return rStatsDict
    
    def rasterReport(self,inRast):
        '''
            Run r.report GRASS function.
            INPUT: inRast 
            OUTPUT: raster report
        '''
        return grass.read_command(self.__rReport,flags='-q',map=inRast)
    
    def setRegion(self,inRast):
        '''
            Run r.region
            INPUT: inRast 
        '''
        grass.run_command(self.__rRegion,map=inRast)
    
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
