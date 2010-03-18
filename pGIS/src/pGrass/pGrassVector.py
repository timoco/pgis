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
        
        #Class vals
        
        #Class properties
        
    def vectInfo(self,inVect):
        '''
            Run v.info GRASS function.
            INPUT: inVect (input vector)
            OUTPUT: vector info
        '''
        return grass.read_command(self.__vInfo,flags='-q',map=inVect)
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
       grassConf.read('/Users/TPM/MyDocs/dev/eclipse/workspace/ncres_pydev/src/app.ini')
       grassSect=grassConf.items('pGRASS')
       
       vect=gVect()
       pp(vect)
       #-- App Code end --#
       debug(end_main)
