'''----------------------------------------------------------------------------------
 Module Name:           pGrass.pGrassVector
 Source Name:           /Users/TPM/MyDocs/dev/gis/pgis/src/pGrass/pGrassVector.py
 Version:               Python 2.6
 Author:                Timothy Morrissey, (timothy.morrissey@unc.edu)
 Date:                  Mar 16, 2010
 Required Argumuments:  
 Optional Arguments:    
 Description:           Wrapper class for the GRASS GIS vector module
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
from pprint import pprint as pp
# ######################################
#       ------ Classes --------
# ######################################
class gVect():
    '''
    Class for vector module of GRASS GIS python application
    '''
    def __init__(self):
        #set the grass.vector (v.<name>) functions
        self.__vInfo='v.info'
        self.__vReport='v.report'
        self.__vDbAddCol='v.db.addcol'
        self.__vDbDropol='v.db.dropcol'
        self.__vToDb='v.to.db'
        self.__vSel='v.db.select'
        self.__vStats='v.univar'
        self.__vExtract='v.extract'
        self.__vToR='v.to.rast'
        self.__vSegment='v.segment'
        self.__vLineToPts='v.to.points'
        self.__vEdit='v.edit'
        self.__vCat='v.category'
        self.__vLinkExtern='v.external'
        #Class vals
        
        #Class properties
        
    #Public Functions
    def linkExternalShp(self,inShpDir,inShpNm):
        '''Link the GRASS DB to an external shapefile dir
        INPUT: inShpDir (external dir)
               inShpNm (external shp name)
        OUTPUT: shpNm (name in GRASS DB)'''
        outShpNm=inShpNm.replace('.shp','_shp')
        inShpNm=inShpNm[:-4]
        retVal=grass.run_command(self.__vLinkExtern,dsn=inShpDir,layer=inShpNm,output=outShpNm)

        if retVal==0:
            return outShpNm
        else:
            return None
        
        
    
    
    def delVectWhere(self,inVect,inWhere):
        '''Deletes vect objects matching where clause
        INPUT: inVect (vector)
                inWhere (where clause)'''
        grass.run_command(self.__vEdit,map=inVect,tool='delete',where=inWhere)
        
    def lineToPts(self,inVect,inDist,overWrt=False):
        '''
        Create points along input line (v.to.points) 
        INPUT: vector
               float (distance between points)
        OUTPUT: vector (points)
        '''
        outVPts='%s_pts' % (inVect)
        grass.run_command(self.__vLineToPts,overwrite=overWrt,input=inVect,output=outVPts,type='point',dmax=inDist)
        return outVPts
    
    def segmentLine(self,inVect,inFile,outSuffix='seg'):
        '''
        Segment a line into points 
        INPUT: vector
               file (segmentation rules) 
        OUTPUT: vector (out segmentation)
        '''
        outSegV='%s_%s' % (inVect,outSuffix)
        retVal=grass.run_command(self.__vSegment,input=inVect,output=outSegV,file=inFile)
        if retVal==0:
            return outSegV
        else:
            return None
    
    def convVtoR(self,inVect,colNm,outNm=''):
        '''
        Convert vector to raster (v.to.rast)
        INPUT: vector
               column name (used for raster value) 
        OUTPUT: raster name
        '''
        #Raster naming convention is . thus replace _ with .
        if len(outNm)>1:
            outRast=outNm
        else:
            outRast=inVect.replace('_','.')
        retVal=grass.run_command(self.__vToR,input=inVect,output=outRast,use='attr',column=colNm)
        if retVal==0:
            return outRast
        else:
            return None
    def getLineLength(self,inLineVect,unitTyp='f'):
        '''Return the length of a line vector
        INPUT: inLineVect
               unitTyp (optional default=f -feet)
        OUTPUT: length'''
        vectReport=self.vectReport(inLineVect, 'length', unitTyp)
        vectLenLi=(vectReport.rstrip('\n')).split('|')
        lineLen=vectLenLi[(len(vectLenLi)-1)]
        return lineLen

    def getPointCoords(self,inPnt):
        '''Return the coordinate of a point vector
        INPUT: inPnt
        OUTPUT: coordDict'''
        vectReport=self.vectReport(inPnt,'coor')
        vectPntLi=vectReport.split('\n')
        coorDict={}
        for row in vectPntLi:
            if ((len(row)>1) and (row.find('cat')==-1)):
                coord=row.split('|')
                pnt=coord[0]
                x=coord[1]
                y=coord[2]
                xy='%s,%s' % (x,y)
                coorDict[pnt]=xy

        return coorDict
        
    def vectExtractEach(self,inVect,inSubNm,inVectNum,overWrt=False):
        '''
        Extract and create new vector for each vector object (row/feature)
        INPUT: vect (subBasin catchments)
               inSub (subBasin name)
               vect num (cat num for vector object)
        OUTPUT: string (new vector name)
        '''
        outVect='%s_catch%s' % (inSubNm,inVectNum)
        retVal=grass.run_command(self.__vExtract,overwrite=overWrt,input=inVect,output=outVect,list=inVectNum)
        if retVal==0:
            return outVect
        else:
            return None

    
    def vectStats(self,inVect,inCol='',inColTyp=''):
        '''
        Return the univar statistics of #,# missing, # null, min, max, & range of vector
        INPUT: vect
               column name
               column type
        OUTPUT: dictionary (stats)
        '''
        vStats=grass.read_command(self.__vStats,'g',map=inVect,col=inCol,type=inColTyp)
        vStatsL=vStats.split('\n')
        vStatsDict={}
        for stat in vStatsL:
            kv=stat.split('=')
            if len(kv) > 1:
                vStatsDict[kv[0]]=kv[1]
        return vStatsDict
    
    def dropDBCol(self,inVect,colNm):
        '''
        Drops a db column to a vector (v.db.dropcol)
        INPUT: vect
               column name
        '''
        grass.run_command(self.__vDbDropol,map=inVect,column=colNm)
    
    def addDBCol(self,inVect,colNm,colTyp):
        '''
        Add db column to a vector (v.db.addcol)
        INPUT: vect
               column name
               column type
        '''
        colStr='%s %s' % (colNm,colTyp)
        grass.run_command(self.__vDbAddCol,map=inVect,columns=colStr)
    
    def addDBVal(self,inVect,valTyp,colNm,valUnit):
        '''
        Populate a db value on a vector (v.to.db)
        INPUT: vect
               value type (area, etc)
               column name
               value unit (mi,k,a,h etc)
        '''
        grass.run_command(self.__vToDb,map=inVect,option=valTyp,columns=colNm,units=valUnit)
    
    def createDBTbl(self,inVect,valTyp):
        '''
        Load vector features to db  (v.to.db)
        INPUT: vect
        '''
        grass.run_command(self.__vToDb,map=inVect,option=valTyp)
        
    def vectSelect(self,inVect):
        '''
            Run v.db.select GRASS function.
            INPUT: inVect (input vector)
            OUTPUT: vector info
        '''
        return grass.read_command(self.__vSel,'c',map=inVect,fs=',')
    
    def getVectCatWhere(self,inVect,inWhere):
        '''
            Run v.db.select GRASS function.
            INPUT: inVect (input vector)
                   inWhere
            OUTPUT: catList
        '''
        return grass.read_command(self.__vSel,'c',map=inVect,fs=',',columns='cat',where=inWhere)
#    def getVectCat(self,inVect):
#        '''return the vector category data
#        INPUT: inVect (vector)
#        OUTPUT: catList'''
#        catList=grass.read_command(self.__vCat,'g',input=inVect,option='print')
#        catList=catList.split('\n')
#        return catList
    def getVectCat(self,inVect):
        '''Run v.db.select GRASS function.
            INPUT: inVect (input vector)
            OUTPUT: catList'''
        vectCatListRet=grass.read_command(self.__vSel,'c',map=inVect,fs=',',columns='cat')
        vectCatListRaw=vectCatListRet.split('\n')
        vectCatList=[]
        for cat in vectCatListRaw:
            if cat=='\n':
                pass
            else:
                vectCatList.append(cat)
                
        return vectCatList
    
    
    def getVectRegion(self,inVect):
        '''
            Run v.db.select GRASS function.
            INPUT: inVect (input vector)
            OUTPUT: vector info
        '''
        return grass.read_command(self.__vSel,'r',map=inVect,fs=',')
        
    def vectInfo(self,inVect):
        '''
            Run v.info GRASS function.
            INPUT: inVect (input vector)
            OUTPUT: vector info
        '''
        return grass.read_command(self.__vInfo,flags='-q',map=inVect)
    
    def vectReport(self,inVect,opt='area',unit='mi'):
        '''
            Run v.report GRASS function.
            INPUT: inVect (input vector)
            OUTPUT: vector report
        '''
        return grass.read_command(self.__vReport,flags='r',map=inVect,option=opt,units=unit)
    
    def getVectCatAreaByThreshold(self,inVect,inThreshVal=5.0):
        '''Get the area of each vector object in a vector dataset above a threshold value
        INPUT: inVect (vector dataset)
               inThreshVal (minimum area value/ default:5.0)
        OUTPUT: vectCatAreaDict (dictionary of cat area key/value pair)'''
        vectReportRaw=self.vectReport(inVect)
        vectReportLi=vectReportRaw.split('\n')
        vectCatAreaDict={}
        for vect in vectReportLi:
            if len(vect)>1:
                area=(vect.split('|'))[3]
                if not area=='area':
                    cat=(vect.split('|'))[0]
                    area_flt=float(area)
                    if area_flt > inThreshVal:
                        vectCatAreaDict[cat]=area_flt
                        
        return vectCatAreaDict
        
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
       grassConf.read(r'C:\MyDocs\projects\eclipse_wkspc\ncReservoir\src\app.ini')  
       grassSect=grassConf.items('pGRASS')
    
       appVect=gVect()
       vectDS='haw_catch118_stream_dams'
       pp(appVect.getPointCoords(vectDS))
#        subCatAreaDict=appVect.getVectCatAreaByThreshold(vectDS)
#       pp(subCatAreaDict)
#       pp(len(subCatAreaDict))
       
       #-- App Code end --#
       debug(end_main)
