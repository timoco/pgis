'''----------------------------------------------------------------------------------
 Module Name:         pArc.pArc
 Source Name:      /Users/TPM/MyDocs/dev/gis/pgis/src/pArc/pArc.py
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
try:
    import arcgisscripting
except ImportError:
    print 'arcgisscripting not found'

# ######################################
#       ------ Classes --------
# ######################################
class arcApp():
    '''
    Class for a Arc GIS python application
    '''
    def __init__(self,appConfigSect):
        self.__home=os.environ['HOME']
        self.__appConfLi=appConfigSect
        self.__gp=self.__createGP()
        
        
    def __createGP(self):
        '''create the ArcGIS geoprocessor object
        OUTPUT: gp
        '''
        gp=arcgisscripting.create(9.3)
        return gp
        
    #CLASS PROPERTIES
    @property
    def getGP(self):
        '''return the ArcGIS geoprocessor object'''
        return self.__gp
        
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
       
       from pprint import pprint as pp
       import sys
       
       from ConfigParser import ConfigParser as configParser
       
       arcConf=configParser()
       arcConf.read('C:/MyDocs/projects/eclipse_wkspc/pGIS_Test/src/app.ini')
       arcSect=arcConf.items('pARC')
       arcApp=arcApp(arcSect)
       arcGP=arcApp.getGP
       
#       pp(arcApp.__home)
#       pp(sys.path)
       #-- App Code end --#
       debug(end_main)
