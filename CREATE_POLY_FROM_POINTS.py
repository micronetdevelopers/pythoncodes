#=========================================================================================
#----- CREATE_POLY_FROM_POINTS.py -----------------------------------------------------
#=========================================================================================
#Author: DR SUBRATA N DAS
#=========================================================================================
#ABSTRACT: Generally the ground truth is captured either as point or polygon GIS vector
#          files. These files when used for extraction of the image for various image-
#          processing, give shifted raster files. The sinple raster to vector conversion
#          does not yield a good GT_MASK.... hence this routine.
#          The routine first extract one band of the satellite data under question for
#          analysis using the CLIP command of ArcGIS with All polygon extend. The raster
#          is then converted into integer raster and then to polygon. These polygons does
#          contain the groundtruth class information. GIS identity analysis is done to
#          bring the class attribute to the polygons and then is converted to raster-mask.
#=========================================================================================
#=========================================================================================
# Initated on :  11/12/2022
# Completed on : 25/12/2022
#=========================================================================================
import os
import sys
import arcpy
from arcpy.sa import *

##***************************** FUNCTIONS ************************************************
## SPACE FOR FUNCTION

##***************************** ACTUAL PROGRAM *******************************************
##CHECKING OUT FOR NECESSARY LICENSES .....................................
arcpy.CheckOutExtension("spatial")

##READING THE INPUTS FROM THE MENU.........................................
coodTable = arcpy.GetParameterAsText(0)
uniqueFld = "DATACODE"

arcpy.AddMessage(" ")
arcpy.AddMessage(coodTable)
arcpy.AddMessage("UNIQUE FIELD:  "+ uniqueFld)



##SETTING THE BAND, FEATURE DATASET AND OTHER DIRECTORY*********************************
##CREATING THE BAND PATH(rasterpath)TO WRITE IMAGE(RASTER) output.......................
gdbpath = ""; no = 0
splittext =  coodTable.split("\\"); splittext.pop()
for j in splittext:
   if (no == 0):gdbpath = j; no = 1 
   else:
       gdbpath = gdbpath+"\\"+j
gdbpath = gdbpath+"\\"
arcpy.AddMessage(" ")
arcpy.AddMessage("GDB Path is : "+gdbpath)
## the variable t

#CREATING THE FD PATH(FDPath)TO WRITE feature Class IN THE GEODATABASE DIRECTORY..........
## THE gdbpath IS THE FEATURE CLASS GEODATABASE DIRICTORY - writing in the geodatabase as shape file
arcpy.AddMessage(" ")
##**********************************************************************************************
##==============================================================================================

##==============================================================================================
##SETTING THE WORK ENVIRONMENT FOR THE GEOPROCESSING and READING VARIABLES**********************
arcpy.env.workspace =  gdbpath
arcpy.AddMessage("WORKSPACE ENVIRONMENT SET TO THE FEATURE DATASET PATH.................")
arcpy.AddMessage(" ")

##READING THE SPATIAL REFERANCE AND GETTING THE MAPPING UNIT OF THE LAYER ****************
geodata = gdbpath+"\\SAMPGEODATA"
sp_ref = arcpy.Describe(geodata).spatialReference
type = ("{0}".format(sp_ref.type))
if type == 'Geographic':
   mapunit = ("{0}".format(sp_ref.angularUnitName))
   sparefna  = ("{0}".format(sp_ref.Name))

arcpy.AddMessage("SPATIAL REF:::::::::::"+ str(sparefna))
arcpy.AddMessage("MAP UNITS::::::::::::: "+mapunit)


##**********************************************************************************************
##==============================================================================================

##==============================================================================================
##**********************************************************************************************
##SETTING THE INTERMEDIATE FEATURE CLASS NAME FOR CREATING A POLYGON LAYER FROM POINT*****
newfc = "TESTPOLY" ; inputFC = gdbpath +"\\TESTPOLY" ;
mainTable = gdbpath +"MARS_Main_Data" ; outTable = gdbpath +"BOUND_info"
dataCodeList = []

##== SETTING THE WORKSPACE FOR CREATING THE POLYGON FC (NECESSARY)***************************
arcpy.env.workspace = gdbpath
outwkspace = arcpy.env.workspace

##== CREATING THE EMPTY POLYGON FEATURE CLASS TO HOLD THE POLYGONS THUS GENERATED************
if arcpy.Exists(gdbpath+newfc):
   arcpy.Delete_management(gdbpath+newfc)

##READING THE SPATIAL REFERENCE OF THE INPUT FEATURE CLASS FOR ASSIGNMENT ****************
spatial_reference = arcpy.Describe(geodata).spatialReference

##CREATING THE NEW FEATURE CLASS (newfc)**************************************************
arcpy.CreateFeatureclass_management(outwkspace,newfc,"POLYGON","","","",spatial_reference)

arcpy.AddField_management(newfc,"PolyId", "SHORT")
arcpy.AddField_management(newfc,"DATACODE", "TEXT","","",8)

edit_polys = arcpy.da.InsertCursor(newfc,["SHAPE@","PolyId","DATACODE"])

##== READING THE 'DATACODE'FROM THE 'MARS_MAIN_DATA' TABLE FOR LIST OF UNIQUE CODES**********
arcpy.AddMessage("=================================================================================================")
arcpy.AddMessage("READING THE DATACODE FROM THE TABLE 'MARS_Main_Data' .........")
arcpy.AddMessage("=================================================================================================")
cursor = arcpy.da.SearchCursor(mainTable,["DATACODE"])
for row in cursor:
   dataCodeList.append(row[0])

arcpy.AddMessage(dataCodeList);
arcpy.AddMessage("=================================================================================================")
arcpy.AddMessage(" ")


newTableView = "dataCodeTableview"
frequencyFields = "DATACODE"
for i in range(len(dataCodeList)):
   dataCode =  dataCodeList[i]
   exp1 = '"'+frequencyFields+'"'+" = "+"'"+dataCode+"'"
   arcpy.AddMessage(exp1)

   ##== DELETING TABLEVIEW IF EXISTS =======================
   if arcpy.Exists(newTableView):
      arcpy.Delete_management(newTableView)
      
   ##== CREATING NEW TABLEVIEW FOR SELECTION AND GETTING ATTRIBUTES 
   newTableView = "dataCodeTableview"
   arcpy.MakeTableView_management(outTable,newTableView)
   arcpy.SelectLayerByAttribute_management(newTableView, "NEW_SELECTION",exp1)
   result = arcpy.GetCount_management(newTableView)
   count = int(result.getOutput(0))
   arcpy.AddMessage("Count = "+str(count))

   arcpy.AddMessage("")
   arcpy.AddMessage("=============================================================================")
   arcpy.AddMessage("READING THE DATACODE FROM THE TABLE FIRSTOUTTABLE FOR THE UNIQUE "+outTable )
   arcpy.AddMessage("=============================================================================")
   arcpy.AddMessage("")

   g = 0 
   coodXXlist = []; coodYYlist = []
   cursor1 = arcpy.da.SearchCursor(newTableView,["DATACODE", "COOD_XX", "COOD_YY"])

   for row in cursor1:
      g = g + 1
      if g == 1 : 
         dataCode = '{0}'.format(row[0])
         coodX = '{0}'.format(row[1])
         coodY = '{0}'.format(row[2])
         firstcoodx = coodX
         firstcoody = coodY
         coodXXlist.append(coodX) # + ", "+coodY))
         coodYYlist.append(coodY) # + ", "+coodY))
      else:
         g = g +1 
         coodX = '{0}'.format(row[1])
         coodY = '{0}'.format(row[2])
         coodXXlist.append(coodX) # + ", "+coodY))
         coodYYlist.append(coodY) # + ", "+coodY))

   coodXXlist.append(firstcoodx) 
   coodYYlist.append(firstcoody)
   arcpy.AddMessage(coodXXlist)
   arcpy.AddMessage(coodYYlist)
   arcpy.AddMessage("==========================================" + str(len(coodXXlist)))
   arcpy.AddMessage("==========================================" + str(len(coodYYlist)))


 


   array = arcpy.Array()
   #SETTING THE POINT OBJECT TO CREATE A BOX ........
   point_obj = arcpy.Point()
   z = 0 
   for i in range(len(coodXXlist)):
      point_obj.X  = coodXXlist[z]
      point_obj.Y = coodYYlist[z]
      array.add(point_obj)
      point_obj = arcpy.Point()
      z = z + 1

   #SETTING THE POLYGON OBJECT TO CREATE A BOX POLYGON AND CALCULATE AREA........
   poly_obj = arcpy.Polygon(array)
   #arcpy.AddMessage(poly_obj.area)

   #ADDING A NEW ROW OF FEATURE TO THE EMPTY POLYGON FEATURE CLASS........
   new_row = [poly_obj,z,dataCode]
   edit_polys.insertRow(new_row)

   #COMPLETED FOR ONE POLYGON AND GOING TO THE NEXT FOR LOOP FOR NEXT POLYGON.........

#DELETING THE EDIT SESSION AND RESET ................
del edit_polys               

arcpy.AddMessage(bullshit)
exit()

##**********************************************************************************************
##==============================================================================================

##==============================================================================================
##**********************************************************************************************
##READING THE POINT FEATURE CLASS COORDINATES TO CREATE A POLYGON COORDINATE ARRAY
pointList = []; features = [] ; ctr = 0


#READING THE POINT X Y COORDINATES AND ATTRIBUTE TO CREATE A BOX POLYGON *****************
cursor = arcpy.da.SearchCursor(vectorGT,["POINT_X","POINT_Y","Name"])
for row in cursor:
    ctr = ctr + 1
    ptX = row[0]
    ptY = row[1]
    naam = row[2]
    fcinfo = [[ptX - celldistn,ptY-celldistn],[ptX - celldistn,ptY+celldistn],
              [ptX + celldistn,ptY+celldistn],[ptX + celldistn,ptY-celldistn],[ptX - celldistn,ptY-celldistn]]
    #arcpy.AddMessage(naam)
    #arcpy.AddMessage(fcinfo)
    array = arcpy.Array()

    #SETTING THE POINT OBJECT TO CREATE A BOX ........
    point_obj = arcpy.Point()
    for coords in fcinfo:
        point_obj.X = coords[0]
        point_obj.Y = coords[1]
        array.add(point_obj)
        point_obj = arcpy.Point()

    #SETTING THE POLYGON OBJECT TO CREATE A BOX POLYGON AND CALCULATE AREA........
    poly_obj = arcpy.Polygon(array)
    #arcpy.AddMessage(poly_obj.area)

    #ADDING A NEW ROW OF FEATURE TO THE EMPTY POLYGON FEATURE CLASS........
    new_row = [poly_obj,ctr,naam]
    edit_polys.insertRow(new_row)

    #COMPLETED FOR ONE POLYGON AND GOING TO THE NEXT FOR LOOP FOR NEXT POLYGON.........

#DELETING THE EDIT SESSION AND RESET ................
del edit_polys               

##**********************************************************************************************
##==============================================================================================

##======================================================================================================================
##======================================================================================================================
##READING THE POINT FEATURE CLASS COORDINATES TO CREATE A POLYGON COORDINATE ARRAY
   
cursor = arcpy.da.SearchCursor(ptFeature,["POINT_X","POINT_Y","Name"])
pointList = []
features = []
ctr = 0


for row in cursor:
    ctr = ctr + 1
    #printArc(str(row[0])+" , "+str(row[1]))
    ptX = row[0]
    ptY = row[1]
    naam = row[2]
    fcinfo = [[ptX - 30,ptY-30],[ptX - 30,ptY+30],[ptX + 30,ptY+30],[ptX + 30,ptY-30],[ptX - 30,ptY-30]]
    print naam
    print(fcinfo)
    array = arcpy.Array()

    point_obj = arcpy.Point()

    for coords in fcinfo:
        point_obj.X = coords[0]
        point_obj.Y = coords[1]
        array.add(point_obj)
        point_obj = arcpy.Point()

    poly_obj = arcpy.Polygon(array)
    print poly_obj.area

    new_row = [poly_obj,ctr,naam]
    edit_polys.insertRow(new_row)
