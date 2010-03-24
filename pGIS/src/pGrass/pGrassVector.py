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
        self.__vToDb='v.to.db'
        self.__vSel='v.db.select'
        
        
        #Class vals
        
        #Class properties
        
    #Public Functions
    def addDBCol(self,inVect,colNm,colTyp):
        '''
        Add db column to a vector (v.db.addcol)
        INPUT: vect
               column name
               column type
        '''
        colStr='%s %s' % (colNm,colTyp)
        pp(colStr)
        pp(inVect)
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
        
    def vectSelect(self,inVect):
        '''
            Run v.db.select GRASS function.
            INPUT: inVect (input vector)
            OUTPUT: vector info
        '''
        return grass.read_command(self.__vSel,map=inVect,fs=',')
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
       grassConf.read(r'C:\MyDocs\projects\eclipse_wkspc\ncres_app\src\app.ini')
       grassSect=grassConf.items('pGRASS')
       
       vect=gVect()
       pp(vect) 
       #-- App Code end --#
       debug(end_main)
