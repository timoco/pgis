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
        #Class vals
        
        #Class properties
        
    #Public Functions
    def getVectCat(self,inVect):
        '''return the vector category data
        INPUT: inVect (vector)
        OUTPUT: catList'''
        catList=grass.read_command(self.__vCat,'g',input=inVect,option='print')
        catList=catList.split('\n')
        return catList
    
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
    
    def segmentLine(self,inVect,inFile,overWrt=False):
        '''
        Segment a line into points 
        INPUT: vector
               file (segmentation rules) 
        OUTPUT: vector (out segmentation)
        '''
        outSegV='%s_seg' % (inVect)
        grass.run_command(self.__vSegment,overwrite=overWrt,input=inVect,output=outSegV,file=inFile)
        return outSegV
    
    def convVtoR(self,inVect,colNm,overWrt=False):
        '''
        Convert vector to raster (v.to.rast)
        INPUT: vector
               column name (used for raster value) 
        OUTPUT: raster name
        '''
        #Raster naming convention is . thus replace _ with .
        outRast=inVect.replace('_','.')
        grass.run_command(self.__vToR,overwrite=overWrt,input=inVect,output=outRast,use='attr',column=colNm)
        if retVal==0:
            return outRast
        else:
            return None
    def getLineLength(self,inLineVect,unitTyp='f'):
        '''Return the length of a line vector
        INPUT: inLineVect
               unitTyp (optional default=f -feet)
        OUTPUT: length'''
        flags='pc'
#        lenRetVal=grass.read_command(self.__vToDb,quiet=True,flags,map=inLineVect,option='length',units=unitTyp)
        lenRetVal=grass.read_command(self.__vToDb,flags,map=inLineVect,option='length',units=unitTyp)
        lineLength=(lenRetVal.split(':'))[1]
        
        return lineLength
        
        
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
        return grass.read_command(self.__vReport,map=inVect,option=opt,units=unit)
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
       grassConf.read(r'/Users/TPM/MyDocs/dev/eclipse/workspace/ncResEngine/ncReservoir/src/app.ini')  
       grassSect=grassConf.items('pGRASS')
       
       vect=gVect()
       pp(vect) 
       #-- App Code end --#
       debug(end_main)
