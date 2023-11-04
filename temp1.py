# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 10:17:44 2023

@author: MSKT11
"""
 
import xml.etree.ElementTree as ET
import os
import sys
import random

#**************************************************************************
# ABSTRACT:
# A Tool-Script is developed under the MARS project by Micronet Solutions
# for reading the satellite data DIM xml file for the standardized
# description of the satellite data and other parameters. The script read
# the XML file and extracts all parameters and save it to the database for
# MARS for query and retrival of satellite data for a region.
#**************************************************************************
# AUTHORS: Dr Subrata N Das (Tuple Solutions),V.R. Reddy (Micronet
#          Solutions, Palash Patil)
#**************************************************************************
# HISTORY:
#  Main program initiated  : 25/07/2023 
#============================================================================================

###===========================================================================================================================
                ########### EXTRACTING THE XML TYPE BASED ON THE SATELLITE/SENSOR TYPE  ###########
###==========================================================================================================================

#### START HERE

xmldata = r"F:\29-08-2023_Data\Airbus_Pleaides-50cm\MONO\BUNDLE\SENSOR\DIM_PHR1B_P_201605020501220_SEN_5983379101-1.XML"

xmlSplit = xmldata.split("_")
xmlFirst = "{0}".format(xmlSplit[0]); xmlSecond = "{0}".format(xmlSplit[1])
print(xmlFirst + "**" + xmlSecond)

dataCODE = ''

if xmlFirst == "DIM" :
    if xmlSecond == "PHR1A" or xmlSecond == "PHR1B" or xmlSecond == "PNEO3" or xmlSecond == "PNEO4"                             or xmlSecond == "SPOT6" or xmlSecond == "SPOT7":
        print(xmlSecond)
        print("********************************PROCESSING AIRBUS DATA :" + xmlSecond)
        dataCODE = "AB"+ str(random.randrange(100000, 999999))
    elif xmlSecond == "PNEOXX":
        print("********************************Pleadeous NEO - 3 ")
        dataCODE = "PL"+ str(random.randrange(100000, 999999))
    else :
        print("THE FILE NAME IS NOT IN PROPER FORMAT..... PLEASE CHECK !")


print("==========================="+dataCODE)
##arcpy.AddMessage("==========================="+BUIISHIT)
##exit()


#### END HERE


####==========================================================================================================================


###===========================================================================================================================
                      ########### SETTING THE XML READ VARIABLES  ###########
###==========================================================================================================================

#### START HERE
#tree = ET.parse("d:\MICRONET_DATA\MARS\DATA_XML\image_data.xml")
tree = ET.parse(xmldata)
root = tree.getroot()
#print (root)
#print (ET.tostring(root))

dataName = '';
for item in root.findall('./Dataset_Identification/DATASET_NAME'):
    #print (item.tag, item.text)
    dataName = '{}'.format(item.text)

compName = ''; 
for item in root.findall('./Product_Information/Producer_Information/PRODUCER_NAME'):
    #print (item.tag, item.text)
    compName = '{}'.format(item.text)

satName = '';
for item in root.findall('./Product_Information/Delivery_Identification/PRODUCT_CODE'):
    #print (item.tag, item.text)
    satName = '{}'.format(item.text)

clRef = ''
for item in root.findall('./Product_Information/Delivery_Identification/Order_Identification/CUSTOMER_REFERENCE'):
    #print (item.tag, item.text)
    clRef = '{}'.format(item.text)

senName = ''
for item in root.findall('./Dataset_Sources/Source_Identification/Strip_Source/MISSION'):
    #print (item.tag, item.text)
    instu = '{}'.format(item.text)
for item in root.findall('./Dataset_Sources/Source_Identification/Strip_Source/MISSION_INDEX'):
    #print (item.tag, item.text) 
    instu_index ='{}'.format(item.text)
    senName = instu + " " + instu_index
    #print (senName)


imgDataProcessLevel = ''
for item in root.findall('./Processing_Information/Product_Settings/PROCESSING_LEVEL'):
    #print (item.tag, item.text)
    imgDataProcessLevel = '{}'.format(item.text)

imgDataProcessSpec = ''
for item in root.findall('./Processing_Information/Product_Settings/SPECTRAL_PROCESSING'):
    #print (item.tag, item.text)
    imgDataProcessSpec = '{}'.format(item.text)

imgDate = ''
for item in root.findall('./Dataset_Sources/Source_Identification/Strip_Source/IMAGING_DATE'):
    #print (item.tag, item.text)
    imgDate = '{}'.format(item.text)
    splittext =  imgDate.split("-"); 
    for i in range(len(splittext)):
        yr = splittext[0];mm = splittext[1];dd = splittext[2]
        imgDate= dd+"-"+mm+"-"+yr

dArea = ''
for item in root.findall('./Dataset_Content/SURFACE_AREA'):
    #print (item.tag, item.text,item.attrib)
    dattb = item.attrib['unit'] ;  #print (dattb)
    if dattb == "square km" :
        #print ("in sq km .........................")
        bArea = '{}'.format(item.text)
        dArea = float(bArea) ;
        #print (type(dArea),"=====" + str(dArea))
    elif dattb == "square m" :
        #print ("in sq m .........................")
        bArea = '{}'.format(item.text)
        dArea = float(bArea)/ 10000 ;
        #print (type(dArea),"=====" + str(dArea))
        
dQLname = ''
for item in root.findall('./Dataset_Identification/DATASET_QL_PATH'):
    #print (item.tag, item.attrib)
    dQLname = '{}'.format(item.attrib['href'])

dFormat = ''
for item in root.findall('./Raster_Data/Data_Access/DATA_FILE_FORMAT'):
    #print (item.tag, item.text)
    dFormat = '{}'.format(item.text)

cloudUnit = ''; dCloud = ''
for item in root.findall('./Dataset_Content/CLOUD_COVERAGE'):
    #print (item.tag, item.text, item.attrib)
    cloudUnit = item.attrib['unit'] ; 
    if cloudUnit == "percent" :
        #print ("cloud coverate in percent .........................")
        dCloud = '{}'.format(item.text)

snowUnit = None; dSnow = None
for item in root.findall('./Dataset_Content/SNOW_COVERAGE'):
    #print (item.tag, item.text, item.attrib)
    snowUnit = item.attrib['unit'] ; 
    if snowUnit == "percent" :
        #print ("cloud coverate in percent .........................")
        dSnow = '{}'.format(item.text)
if dSnow is None:
    dSnow = 0        
# if dSnow.isnumeric():
#   # If the value is numeric, cast it to a numeric type (e.g., float or int)
#   dSnow = int(dSnow)  # or int(dSnow) if you want an integer representation
# else:
#   # If the value is not numeric, keep it as a character
#   dSnow = str(dSnow)
#   print(dSnow)
  
  
dAQrange = ''
for item in root.findall('./Radiometric_Data/Dynamic_Range/ACQUISITION_RANGE'):
    #print (item.tag, item.text)
    dAQrange = '{}'.format(item.text)

dPRrange = ''
for item in root.findall('./Radiometric_Data/Dynamic_Range/PRODUCT_RANGE'):
    #print (item.tag, item.text)
    dPRrange = '{}'.format(item.text)

dPRJtable = ''; dPRJname = ''
if xmlSecond == "PHR1B" or xmlSecond == "PHR1A" or xmlSecond == "SPOT6" or xmlSecond == "SPOT7": 
    for item in root.findall('./Coordinate_Reference_System/Projected_CRS/PROJECTED_CRS_CODE'):
        dPRJcode = '{}'.format(item.text)
        aaa = dPRJcode.split(":")
        dPRJtable = "{0}".format(aaa[4])
        dPRJname = "{0}".format(aaa[6])
elif xmlSecond == "PNEO4" or xmlSecond == "PNEO3": 
    for item in root.findall('./Coordinate_Reference_System/Geodetic_CRS/GEODETIC_CRS_CODE'):
        dPRJcode = '{}'.format(item.text)
        aaa = dPRJcode.split(":")
        dPRJtable = "{0}".format(aaa[4])
        dPRJname = "{0}".format(aaa[6])


dRows = ''
for item in root.findall('./Raster_Data/Raster_Dimensions/NROWS'):
    #print (item.tag, item.text)
    dRows = int('{}'.format(item.text))

dCols = ''    
for item in root.findall('./Raster_Data/Raster_Dimensions/NCOLS'):
    #print (item.tag, item.text)
    dCols = int('{}'.format(item.text))

dBands = ''
for item in root.findall('./Raster_Data/Raster_Dimensions/NBANDS'):
    #print (item.tag, item.text)
    dBands = int('{}'.format(item.text))

dTiles = 0
for item in root.findall('./Raster_Data/Data_Access/DATA_FILE_TILES'):
    dtilesTF = ('{}'.format(item.text))
    print("$$$$$$$$$$$$$$$$" + dtilesTF)   
    if dtilesTF == "TRUE" or dtilesTF == "true": 
        for item in root.findall('./Raster_Data/Raster_Dimensions/Tile_Set/NTILES'):
            #print (item.tag, item.text)
            dTiles = int('{}'.format(item.text))

dType = ''
for item in root.findall('./Raster_Data/Raster_Encoding/DATA_TYPE'):
    #print (item.tag, item.text)
    dType = '{}'.format(item.text)

dBits = ''    
for item in root.findall('./Raster_Data/Raster_Encoding/NBITS'):
    #print (item.tag, item.text)
    dBits = int('{}'.format(item.text))

dSign = ''
for item in root.findall('./Raster_Data/Raster_Encoding/SIGN'):
    #print (item.tag, item.text)
    dSign = '{}'.format(item.text)

dINangle = ''
for item in root.findall('./Geometric_Data/Use_Area/Located_Geometric_Values/Acquisition_Angles/INCIDENCE_ANGLE'):
    #print (item.tag, item.text)
    dIN = '{}'.format(item.text)
    dINangle = float(dIN) ;
    if item.text != '' :  break 

dGSDaxt = ''
for item in root.findall('./Geometric_Data/Use_Area/Located_Geometric_Values/Ground_Sample_Distance/GSD_ACROSS_TRACK'):
    #print (item.tag, item.text)
    dGSDx = '{}'.format(item.text)
    dGSDaxt = float(dGSDx) ;
    if item.text != '' :  break 

dGSDalt = ''
for item in root.findall('./Geometric_Data/Use_Area/Located_Geometric_Values/Ground_Sample_Distance/GSD_ALONG_TRACK'):
    #print (item.tag, item.text)
    dGSDy = '{}'.format(item.text)
    dGSDalt = float(dGSDy) ;
    if item.text != '' :  break

dPixelx = '' ; dPixely = ''
for item in root.findall('./Processing_Information/Product_Settings/Sampling_Settings/RESAMPLING_SPACING'):
    print("$$$$$$$$$$$"+item.tag+ item.text)
    dPIXx = '{}'.format(item.text)
    dPixelx = float(dPIXx) ;
    dPixely = float(dPIXx) ;
    if item.text != '' :  break
                    
###=================================================================================================

###PRINTING VARIABLES ==============================================================================

###=================================================================================================

print ("----------------------------------------------------------------------------------------")
print ("XLM FILE NAME ===== "+ xmldata)
print ("DATABASE CODE ===== "+ dataCODE)
print ("DATABASE NAME ===== "+ dataName)
print ("COMPANY NAME ====== "+ compName)
print ("SATELLITE NAME ==== "+ satName)
print ("CUSTOMER ID   ===== "+ clRef)
print ("SENSOR NAME ======= "+ senName)
print ("DATA PROCESS LEVEL= "+ imgDataProcessLevel)
print ("DATA SPECTRAL PROC. "+ imgDataProcessSpec)
print ("IMAGING DATE ====== "+ imgDate)
print ("SURFACE AREA(sqkm)= "+ str(dArea))
print ("QL PATH =========== "+ dQLname)
print ("DATA FORMAT ======= "+ dFormat)
print ("CLOUD COVERAGE ==== "+ dCloud)
print ("SNOW COVERAGE ===== "+ str(dSnow))
print ("ACQUISITION RANGE== "+ dAQrange)
print ("PRODUCT RANGE  ==== "+ dPRrange)
print ("PROJECTION TABLE == "+ dPRJtable)
print ("PROJECTION NAME === "+ dPRJname)

print ("DATA ROWS NO ====== "+ str(dRows))
print ("DATA COLUMNS NO === "+ str(dCols))
print ("DATA BANDS NO ===== "+ str(dBands))
print ("DATA TILES NO ===== "+ str(dTiles))
print ("DATA TYPE ========= "+ dType)
print ("DATA BITS ========= "+ str(dBits))
print ("DATA SIGNAGE ====== "+ dSign)
print ("INCIDENCE ANGLE==== "+ str(dINangle))
print ("GSD ACROSS PATH==== "+ str(dGSDaxt))
print ("GSD ALONG PATH===== "+ str(dGSDalt))
print ("PIXEL IN X DIR===== "+ str(dPixelx))
print ("PIXEL IN Y DIR===== "+ str(dPixely))
                     
print ("----------------------------------------------------------------------------------------")
print (" ")


#### END HERE

####==========================================================================================================================

###===========================================================================================================================
                ########### PARSING THE BAND NAME, ITS START SPECTRAL MICROMETER AND END MICROMETER  ###########
###==========================================================================================================================

#### START HERE

bandList= [] ; specMinList = [] ; specMaxList = []       

if xmlSecond == "PHR1A" or xmlSecond == "PHR1B" or xmlSecond == "SPOT6" or xmlSecond == "SPOT7":
    for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/MEASURE_UNIT'):
        print  (item.tag + " MEASURE UNIT PHR " + item.text)
        bameasureUnit = '{}'.format(item.text) #saving the unit for conversion from nanometers to micrometer
        
    for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/BAND_ID'):
        #arcpy.AddMessage  (item.tag + "band" + item.text)
        bandList.append(item.text)
    for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/MIN'):
        print  (item.tag + "Start" + item.text)
        if bameasureUnit == 'nanometers' or bameasureUnit == 'nanometer':
            spec = float('{}'.format(item.text))/1000
            print (str(spec))
            specMinList.append(spec)
        else: 
            specMinList.append(item.text)
    for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/MAX'):
        print  (item.tag + " END " + item.text)
        if bameasureUnit == 'nanometers' or bameasureUnit == 'nanometer':
            spec = float('{}'.format(item.text))/1000
            print (str(spec))
            specMaxList.append(spec)
        else: 
            specMaxList.append(item.text)

elif xmlSecond == "PNEO3" or xmlSecond == "PNEO4":
    for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/MEASURE_UNIT'):
        print  (item.tag + " MEASURE_UNIT_PNEO " + item.text)
        bameasureUnit = '{}'.format(item.text) #saving the unit for conversion from nanometers to micrometer

    for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/BAND_ID'):
        #arcpy.AddMessage  (item.tag + "band" + item.text)
        bandList.append(item.text)
    for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/FWHM/MIN'):
        print  (item.tag + " Start " + item.text)
        if bameasureUnit == 'nanometer' or bameasureUnit == 'nanometers':
            spec = float('{}'.format(item.text))/1000
            print (str(spec))
            specMinList.append(spec)
        else: 
            specMinList.append(item.text)
    for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/FWHM/MAX'):
        print  (item.tag + " end " + item.text)
        if bameasureUnit == 'nanometer' or bameasureUnit == 'nanometers':
            spec = float('{}'.format(item.text))/1000
            print (str(spec))
            specMaxList.append(spec)
        else: 
            specMaxList.append(item.text)
else :
    print ("COULD NOT FIGURE OUT THE DATA .................................PLEASE CHECK!")   

if len(bandList) == 0 and imgDataProcessSpec == 'PMS':
    print ("******* I AM IN PMS*****************"+ str(len(bandList))+"---"+imgDataProcessSpec )
    for j in range(dBands):
        print (j)
        bandList.append(j+1); specMinList.append(int(1)); specMaxList.append(int(255))

# Convert text values to floats
#bandList = [float(val) for val in bandList]
# specMinList = [float(val) for val in specMinList]
# specMaxList = [float(val) for val in specMaxList]   


# bandList = ", ".join(str(val) for val in bandList)
# bandList = [float(val) for val in bandList]
# specMinList = [float(val) for val in specMinList]
# specMaxList = [float(val) for val in specMaxList]

print (bandList)
print (specMinList)
print (specMaxList)
print (len(bandList))
print (len(specMinList))
print (len(specMaxList))


#### END HERE

####==========================================================================================================================

###===========================================================================================================================
                      ########### PARSING THE AOI BOUND CORNER CORDINATES  ###########
###===========================================================================================================================

#### START HERE


xcodlist = []; ycodlist = []
for item in root.findall('./Dataset_Content/Dataset_Extent/Vertex'):
    #arcpy.AddMessage (item.tag + "----------------------------------------------------------")
    
    for item in root.findall('./Dataset_Content/Dataset_Extent/Vertex/LON'):
        #print (item.text)
        xcodlist.append(str(item.text))

    for item in root.findall('./Dataset_Content/Dataset_Extent/Vertex/LAT'):
       #print (item.text)
       ycodlist.append(str(item.text))

    if item.tag != '' :  break
# Now you can use enumerate to get the index and value while iterating
for idx, xcod in enumerate(xcodlist):
    print(f"Index: {idx}, X Coordinate: {xcod}")

for idx, ycod in enumerate(ycodlist):
    print(f"Index: {idx}, Y Coordinate: {ycod}")    

# xcodlist = ", ".join(str(x) for x in xcodlist)
# ycodlist = ", ".join(str(x) for x in ycodlist)


# xcodlist = [float(val) for val in xcodlist]
# ycodlist = [float(val) for val in ycodlist]

print ("XXcood = "+str(xcodlist))
print ("YYcood = "+str(ycodlist))
print ("----------------------------------------------------------------------------------------")
print (" ")



#### END HERE

####==========================================================================================================================
    
###===========================================================================================================================
                      ########### FOLLOWING IS THE DATABASE CODE ###########
###==========================================================================================================================  

#### START HERE


import psycopg2

# Connection to an existing database
conn = psycopg2.connect(database="test", user = "postgres", password = "abcd@1234", host = "localhost", port = "5432")

print ("Opened database successfully")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this to create table into database ### create table if not exists
# cur.execute('''CREATE TABLE IF NOT EXISTS MARS_Database
#       (DATACODE	CHAR(8),
#     DATANAME	CHAR(70),
#     COMP_NA	CHAR(30),
#     SATT_NA	CHAR(20),
#     CL_REF	CHAR(50),
#     CL_ORDNA	CHAR(30),
#     CL_PROJNA	CHAR(50),
#     CL_PURPOSE	CHAR(100),
#     CL_ADDRESS1	CHAR(50),
#     CL_ADDRESS2	CHAR(50),
#     SEN_NAME	CHAR(20),
#     IMG_DATYPE	CHAR(30),
#     IMG_DAPROC	CHAR(10),
#     IMG_DATE	DATE NOT NULL,
#     IMG_DT_RNG	CHAR(21),
#     DLOCA_CY	CHAR(30),
#     DLOCA_ST	CHAR(30),
#     DLOCA_DT	CHAR(30),
#     DLOCA_LOCA	CHAR(100),
#     DAREA	NUMERIC NOT NULL,
#     DSIZE	NUMERIC ,
#     DQLNAME	CHAR(80),
#     DFORMAT	CHAR(20),
#     DCLOUD	NUMERIC NOT NULL,	
#     DSNOW	NUMERIC ,	
#     D_AQ_BITS	NUMERIC NOT NULL,	
#     D_PR_BITS	NUMERIC NOT NULL,	
#     DPRJ_TABLE	CHAR(20),
#     DPRJ_NAME	CHAR(6),
#     D_NROWS	NUMERIC NOT NULL,	
#     D_NCOLS	NUMERIC NOT NULL,	
#     D_NBANDS	NUMERIC NOT NULL,	
#     D_NTILES	NUMERIC NOT NULL,	
#     D_TYPE	CHAR(20),
#     D_NBITS	NUMERIC NOT NULL,	
#     D_SIGN	CHAR(10),
#     D_IN_ANGL	NUMERIC NOT NULL,
#     D_GSD_AXT	NUMERIC NOT NULL,
#     D_GSD_ALT	NUMERIC NOT NULL,
#     D_PIXELX	NUMERIC NOT NULL,
#     D_PIXELY	NUMERIC NOT NULL,
#     AL_DA_PATH	CHAR(150),
#     AL_SH_PATH	CHAR(150),
#     AL_QL_PATH	CHAR(150),
#     XML_FILE	CHAR(90),
#     BAND_NAME	CHAR(50),
#     BAND_S_SPEC	CHAR(90),
#     BAND_E_SPEC	CHAR(90),
#     COOD_NO	NUMERIC ,	
#     COOD_XX	CHAR(90),
#     COOD_YY	CHAR(90));''')
      
# print ("Table created successfully")

# # Pass data to fill a query placeholder and let psycopg perform
# #to add value into the table with value
# cur.execute('''
#         INSERT INTO MARS_Database (DATACODE, DATANAME, COMP_NA, SATT_NA, CL_REF, CL_ORDNA, CL_PROJNA, CL_PURPOSE, CL_ADDRESS1, CL_ADDRESS2, SEN_NAME, IMG_DATYPE, IMG_DAPROC, IMG_DATE, IMG_DT_RNG, DLOCA_CY, DLOCA_ST, DLOCA_DT, DLOCA_LOCA, DAREA, DSIZE, DQLNAME, DFORMAT, DCLOUD, DSNOW, D_AQ_BITS, D_PR_BITS, DPRJ_TABLE, DPRJ_NAME, D_NROWS, D_NCOLS, D_NBANDS, D_NTILES, D_TYPE, D_NBITS, D_SIGN, D_IN_ANGL, D_GSD_AXT, D_GSD_ALT, D_PIXELX, D_PIXELY, AL_DA_PATH, AL_SH_PATH, AL_QL_PATH, XML_FILE, BAND_NAME, BAND_S_SPEC, BAND_E_SPEC,COOD_XX, COOD_YY)
#         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
#         ''',
#         (dataCODE, dataName, compName, satName, clRef, None, None, None, None, None, senName, None, imgDataProcessLevel, imgDate, None, None, None, None, None, dArea, None, dQLname, dFormat, dCloud, dSnow, dAQrange, dPRrange, dPRJtable, dPRJname, dRows, dCols, dBands, dTiles, dType, dBits, dSign, dINangle, dGSDaxt, dGSDalt, dPixelx, dPixely, None, None, None,None, bandList, specMinList, specMaxList, xcodlist, ycodlist))

''' FIRST TABLE  '''
# Execute a command: this to create table into database ### create table if not exists
cur.execute('''CREATE TABLE IF NOT EXISTS MARS_MAIN_TABLE_DATA
      (DATACODE	CHAR(8),
    DATANAME	CHAR(70),
    COMP_NA	CHAR(30),
    SATT_NA	CHAR(20),
    CL_REF	CHAR(50),
    CL_ORDNA	CHAR(30),
    CL_PROJNA	CHAR(50),
    CL_PURPOSE	CHAR(100),
    CL_ADDRESS1	CHAR(50),
    CL_ADDRESS2	CHAR(50),
    SEN_NAME	CHAR(20),
    IMG_DATYPE	CHAR(30),
    IMG_DAPROC	CHAR(10),
    IMG_DATE	DATE NOT NULL,
    IMG_DT_RNG	CHAR(21),
    DLOCA_CY	CHAR(30),
    DLOCA_ST	CHAR(30),
    DLOCA_DT	CHAR(30),
    DLOCA_LOCA	CHAR(100),
    DAREA	NUMERIC NOT NULL,
    DSIZE	NUMERIC ,
    DQLNAME	CHAR(80),
    DFORMAT	CHAR(20),
    DCLOUD	NUMERIC NOT NULL,	
    DSNOW	NUMERIC ,	
    D_AQ_BITS	NUMERIC NOT NULL,	
    D_PR_BITS	NUMERIC NOT NULL,	
    DPRJ_TABLE	CHAR(20),
    DPRJ_NAME	CHAR(6),
    D_NROWS	NUMERIC NOT NULL,	
    D_NCOLS	NUMERIC NOT NULL,	
    D_NBANDS	NUMERIC NOT NULL,	
    D_NTILES	NUMERIC NOT NULL,	
    D_TYPE	CHAR(20),
    D_NBITS	NUMERIC NOT NULL,	
    D_SIGN	CHAR(10),
    D_IN_ANGL	NUMERIC NOT NULL,
    D_GSD_AXT	NUMERIC NOT NULL,
    D_GSD_ALT	NUMERIC NOT NULL,
    D_PIXELX	NUMERIC NOT NULL,
    D_PIXELY	NUMERIC NOT NULL,
    AL_DA_PATH	CHAR(150),
    AL_SH_PATH	CHAR(150),
    AL_QL_PATH	CHAR(150),
    XML_FILE	CHAR(90));''')
      
print ("MARS_MAIN_TABLE_DATA Table1 created successfully")

# Pass data to fill a query placeholder and let psycopg perform
#to add value into the table with value
cur.execute('''
        INSERT INTO MARS_MAIN_TABLE_DATA (DATACODE, DATANAME, COMP_NA, SATT_NA, CL_REF, CL_ORDNA, CL_PROJNA, CL_PURPOSE, CL_ADDRESS1, CL_ADDRESS2, SEN_NAME, IMG_DATYPE, IMG_DAPROC, IMG_DATE, IMG_DT_RNG, DLOCA_CY, DLOCA_ST, DLOCA_DT, DLOCA_LOCA, DAREA, DSIZE, DQLNAME, DFORMAT, DCLOUD, DSNOW, D_AQ_BITS, D_PR_BITS, DPRJ_TABLE, DPRJ_NAME, D_NROWS, D_NCOLS, D_NBANDS, D_NTILES, D_TYPE, D_NBITS, D_SIGN, D_IN_ANGL, D_GSD_AXT, D_GSD_ALT, D_PIXELX, D_PIXELY, AL_DA_PATH, AL_SH_PATH, AL_QL_PATH, XML_FILE)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        ''',
        (dataCODE, dataName, compName, satName, clRef, None, None, None, None, None, senName, None, imgDataProcessLevel, imgDate, None, None, None, None, None, dArea, None, dQLname, dFormat, dCloud, dSnow, dAQrange, dPRrange, dPRJtable, dPRJname, dRows, dCols, dBands, dTiles, dType, dBits, dSign, dINangle, dGSDaxt, dGSDalt, dPixelx, dPixely, None, None, None,xmldata))

print ("MARS_MAIN_TABLE_DATA Table1 Records created successfully")

''' SECOND TABLE  '''
# Execute a command: this to create table into database ### create table if not exists
cur.execute('''CREATE TABLE IF NOT EXISTS MARS_BAND_INFORMATION
      (DATACODE	CHAR(8),
    BAND_NAME	CHAR(50),
    BAND_S_SPEC	NUMERIC,
    BAND_E_SPEC	NUMERIC);''')
      
print ("MARS_BAND_INFORMATION Table2 created successfully")

for band, spec_min, spec_max in zip(bandList, specMinList, specMaxList):
    cur.execute('''
                INSERT INTO MARS_BAND_INFORMATION (DATACODE, BAND_NAME, BAND_S_SPEC, BAND_E_SPEC)
                VALUES (%s, %s, %s, %s);
                ''',
                (dataCODE, band, spec_min, spec_max))

# for x in bandList:
#     bandlist = x
# for y in specMinList:
#     specminlist = y
# for z in specMaxList:
#     specmaxlist = z
    
#     cur.execute('''
#             INSERT INTO MARS_BAND_INFORMATION (DATACODE, BAND_NAME, BAND_S_SPEC, BAND_E_SPEC)
#             VALUES (%s,%s,%s,%s);
#             ''',
#             (dataCODE, bandlist, specminlist, specmaxlist))

    print ("MARS_BAND_INFORMATION Table2 Records created successfully")



''' THIRD TABLE  '''
# Execute a command: this to create table into database ### create table if not exists
cur.execute('''CREATE TABLE IF NOT EXISTS MARS_BOUNDS_COORDINATES
      (DATACODE	CHAR(8),
    COOD_NO	NUMERIC ,	
    COOD_XX	NUMERIC,
    COOD_YY	NUMERIC);''')
      
print ("MARS_BOUNDS_COORDINATES Table3 created successfully")

# Use enumerate to iterate over xcodlist and ycodlist simultaneously
for i, (xcdlst, ycdlst) in enumerate(zip(xcodlist, ycodlist)):
    cur.execute('''
                INSERT INTO MARS_BOUNDS_COORDINATES (DATACODE, COOD_NO, COOD_XX, COOD_YY)
                VALUES (%s, %s, %s, %s);
                ''',
                (dataCODE, i, xcdlst, ycdlst))




print ("MARS_BOUNDS_COORDINATES Table3 Records created successfully")

# Make the change to the database persistent
conn.commit()

print ("Records created successfully")

# Close communication with the database
cur.close()
conn.close()
























































###=================================================================================================
###=================================================================================================
### READING AND WRITING THE TABLE (PRESENTLY ARCGIS OBJECT TABLE IS CONSIDERED)
###=================================================================================================
###=================================================================================================
# Create Arcgis table
#Deleting a table if already exist=============
# if arcpy.Exists(gdbpath+"\\MARS_Main_Data"):
#     arcpy.Delete_management(gdbpath+"\\MARS_Main_Data")
##    arcpy.AddMessage ("======================================================================================")
##    arcpy.AddMessage ("========= R E A D I N G  AND  W R I T I N G  TO  F I L E =============================")
##    arcpy.AddMessage ("======================================================================================")
##    arcpy.AddMessage ("========= WRITING TO FILE MARS_Main_Data =============================================")
##    arcpy.AddMessage ("======================================================================================")
##
##    outname = "MARS_Main_Data"
##    incursor = arcpy.da.InsertCursor(gdbpath+outname,("DATACODE","DATANAME","COMP_NA","SATT_NA","CL_REF","SEN_NAME",\
##              "IMG_DAPROC","IMG_DATE","DAREA","DQLNAME","DFORMAT","DCLOUD","DSNOW","D_AQ_BITS","D_PR_BITS","DPRJ_TABLE",\
##              "DPRJ_NAME","D_NROWS","D_NCOLS","D_BANDS","D_NTILES","D_TYPE","D_NBITS","D_SIGN","D_IN_ANGL","D_GSD_AXT",\
##              "D_GSD_ALT","D_PIXELX","D_PIXELY","XML_FILE"))
##    incursor.insertRow([dataCODE,dataName,compName,satName,clRef,senName,imgDataProcessLevel,imgDate,dArea,dQLname,\
##                        dFormat,dCloud,dSnow,dAQrange,dPRrange,dPRJtable,dPRJname,dRows,dCols,dBands,dTiles,dType,\
##                        dBits,dSign,dINangle,dGSDaxt,dGSDalt,dPixelx,dPixely,xmldata])
##    del incursor
##    arcpy.AddMessage ("======================================================================================")
##    arcpy.AddMessage (" ")
# else:
#     arcpy.AddMessage ("======CREATING NEW TABLE =============================================================")
#     arcpy.AddMessage (" ")
#     #setting table name with path ================
#     table = "MARS_Main_Data"
#     arcpy.CreateTable_management(gdbpath, table, "" , "")
#     tablepath = gdbpath+"\\"+table
#     #adding field ===============
#     arcpy.AddField_management(tablepath,"DATACODE","TEXT", "", "",8)
#     arcpy.AddField_management(tablepath,"DATANAME","TEXT", "", "",70)
#     arcpy.AddField_management(tablepath,"COMP_NA","TEXT", "", "",30)
#     arcpy.AddField_management(tablepath,"SATT_NA","TEXT", "", "",20)
#     arcpy.AddField_management(tablepath,"CL_REF","TEXT", "", "",20)
#     arcpy.AddField_management(tablepath,"CL_ORDNA","TEXT", "", "",30)
#     arcpy.AddField_management(tablepath,"CL_PROJNA","TEXT", "", "",50)
#     arcpy.AddField_management(tablepath,"CL_PURPOSE","TEXT", "", "",100)
#     arcpy.AddField_management(tablepath,"CL_ADDRESS1","TEXT", "", "",50)
#     arcpy.AddField_management(tablepath,"CL_ADDRESS2","TEXT", "", "",50)
#     arcpy.AddField_management(tablepath,"SEN_NAME","TEXT", "", "",20)
#     arcpy.AddField_management(tablepath,"IMG_DATYPE","TEXT", "", "",30)
#     arcpy.AddField_management(tablepath,"IMG_DAPROC","TEXT", "", "",10)
#     arcpy.AddField_management(tablepath,"IMG_DATE","DATE")
#     arcpy.AddField_management(tablepath,"IMG_DT_RNG","TEXT", "", "",21)
#     arcpy.AddField_management(tablepath,"DLOCA_CY","TEXT", "", "",30)
#     arcpy.AddField_management(tablepath,"DLOCA_ST","TEXT", "", "",30)
#     arcpy.AddField_management(tablepath,"DLOCA_DT","TEXT", "", "",30)
#     arcpy.AddField_management(tablepath,"DLOCA_LOCA","TEXT", "", "",100)
#     arcpy.AddField_management(tablepath,"DAREA","FLOAT")
#     arcpy.AddField_management(tablepath,"DSIZE","FLOAT")
#     arcpy.AddField_management(tablepath,"DQLNAME","TEXT", "", "",80)
#     arcpy.AddField_management(tablepath,"DFORMAT","TEXT", "", "",20)
#     arcpy.AddField_management(tablepath,"DCLOUD","INTEGER")
#     arcpy.AddField_management(tablepath,"DSNOW","INTEGER")
#     arcpy.AddField_management(tablepath,"D_AQ_BITS","INTEGER")
#     arcpy.AddField_management(tablepath,"D_PR_BITS","INTEGER")
#     arcpy.AddField_management(tablepath,"DPRJ_TABLE","TEXT", "", "",20)
#     arcpy.AddField_management(tablepath,"DPRJ_NAME","TEXT", "", "",6)
#     arcpy.AddField_management(tablepath,"D_NROWS","INTEGER")
#     arcpy.AddField_management(tablepath,"D_NCOLS","INTEGER")
#     arcpy.AddField_management(tablepath,"D_NBANDS","INTEGER")
#     arcpy.AddField_management(tablepath,"D_NTILES","INTEGER")
#     arcpy.AddField_management(tablepath,"D_TYPE","TEXT", "", "",20)
#     arcpy.AddField_management(tablepath,"D_NBITS","INTEGER")
#     arcpy.AddField_management(tablepath,"D_SIGN","TEXT", "", "",10)
#     arcpy.AddField_management(tablepath,"D_IN_ANGL","FLOAT")
#     arcpy.AddField_management(tablepath,"D_GSD_AXT","FLOAT")
#     arcpy.AddField_management(tablepath,"D_GSD_ALT","FLOAT")
#     arcpy.AddField_management(tablepath,"D_PIXELX","FLOAT")
#     arcpy.AddField_management(tablepath,"D_PIXELY","FLOAT")
#     arcpy.AddField_management(tablepath,"AL_DA_PATH","TEXT", "", "",150)
#     arcpy.AddField_management(tablepath,"AL_SH_PATH","TEXT", "", "",150)
#     arcpy.AddField_management(tablepath,"AL_QL_PATH","TEXT", "", "",150)
#     arcpy.AddField_management(tablepath,"XML_FILE","TEXT", "", "",90)
#     arcpy.AddField_management(tablepath,"DATACODE","TEXT", "", "",8)
#     arcpy.AddField_management(tablepath,"BAND_NAME","TEXT", "", "",10)
#     arcpy.AddField_management(tablepath,"BAND_S_SPEC","FLOAT")
#     arcpy.AddField_management(tablepath,"BAND_E_SPEC","FLOAT")
#     arcpy.AddField_management(tablepath,"DATACODE","TEXT", "", "",8)
#     arcpy.AddField_management(tablepath,"COOD_NO","INTEGER")
#     arcpy.AddField_management(tablepath,"COOD_XX","FLOAT")
#     arcpy.AddField_management(tablepath,"COOD_YY","FLOAT")
    #arcpy.AddField_management(table,"DATANAME", "TEXT", "", "",70)
    
##    arcpy.AddField_management(WSHEDfc,"AREASQKM","FLOAT")
##    arcpy.AddField_management(WSHEDfc,"DRNP_AREASQKM","DOUBLE")
##    arcpy.AddField_management(WSHEDfc,"DRNP_PERC_OFWB","FLOAT")
##    arcpy.AddField_management(WSHEDfc,"DRNL_LENKM","DOUBLE")
##    arcpy.AddField_management(WSHEDfc,"DRNL_DENSITY","DOUBLE")
##
##    #deleting field ================
##    arcpy.DeleteField_management(merged_table,["FREQUENCY","TL1CODE","TL2CODE","TL3CODE","TL4CODE","TL5CODE","TL6CODE"])

# exit()
### ------------------------------------------------------------------------------------------------
### WRITING TO THE DATA FILE (MARS_Main_Data) ******************************************************
### ------------------------------------------------------------------------------------------------
# arcpy.AddMessage (" ")


### ------------------------------------------------------------------------------------------------

### ------------------------------------------------------------------------------------------------
### WRITING THE DATA TO THE BAND FILE (BAND_Info)***********************************************
### ------------------------------------------------------------------------------------------------
# arcpy.AddMessage ("======================================================================================")
# arcpy.AddMessage ("========= WRITING TO FILE BAND_info ==================================================")
# arcpy.AddMessage ("======================================================================================")
# outname = "BAND_info"
# for r in range(len(bandList)):
#     arcpy.AddMessage (bandList[r]+"="+str(specMinList[r])+"-"+ str(specMaxList[r]))
#     incursor = arcpy.da.InsertCursor(gdbpath+outname,("DATACODE","BND_NAME","BND_S_SPEC","BND_E_SPEC"))
#     incursor.insertRow([dataCODE,bandList[r],specMinList[r],specMaxList[r]])
#     del incursor
# arcpy.AddMessage ("======================================================================================")
# arcpy.AddMessage (" ")
### ------------------------------------------------------------------------------------------------

### ------------------------------------------------------------------------------------------------
### WRITING THE DATA TO THE BAND FILE (BAND_Info)***********************************************
### ------------------------------------------------------------------------------------------------
# arcpy.AddMessage ("======================================================================================")
# arcpy.AddMessage ("========= WRITING TO FILE BOUND_info =================================================")
# arcpy.AddMessage ("======================================================================================")
# outname = "BOUND_info"
# for r in range(len(xcodlist)):
#     rr = r +1 
#     arcpy.AddMessage (str(rr)+":="+xcodlist[r]+"-"+ ycodlist[r])
#     incursor = arcpy.da.InsertCursor(gdbpath+outname,("DATACODE","COOD_NO","COOD_XX","COOD_YY"))
#     incursor.insertRow([dataCODE,rr,xcodlist[r],ycodlist[r]])
#     del incursor
# arcpy.AddMessage ("======================================================================================")
# arcpy.AddMessage (" ")
### ------------------------------------------------------------------------------------------------


##SETTING THE INTERMEDIATE FEATURE CLASS NAME FOR CREATING A POLYGON LAYER FROM POINT*****
# newfc = "TESTPOLY" ; inputFC = gdbpath + "\\TESTPOLY" ; sampGeodata= gdbpath + "\\SAMPGEODATA"
# mainTable = gdbpath +"MARS_Main_Data" ; outTable = gdbpath +"BOUND_info"
# dataCodeList = []

# arcpy.AddMessage ("GDBPATH =  "+ gdbpath)
# arcpy.AddMessage ("GEODATA =  "+ inputFC)

# ##== SETTING THE WORKSPACE FOR CREATING THE POLYGON FC (NECESSARY)***************************
# arcpy.env.workspace = gdbpath
# outwkspace = arcpy.env.workspace

# ##== CREATING THE EMPTY POLYGON FEATURE CLASS TO HOLD THE POLYGONS THUS GENERATED************
# if arcpy.Exists(gdbpath+newfc):
#     arcpy.AddMessage ("FEATURE CLASS ALREADY EXIST ..........PROCESSING")
#     #arcpy.Delete_management(gdbpath+newfc)

#     edit_polys = arcpy.da.InsertCursor(newfc,["SHAPE@","PolyId","DATACODE"])

#     array = arcpy.Array()
#     #SETTING THE POINT OBJECT TO CREATE A BOX ........
#     point_obj = arcpy.Point()
#     z = 0 
#     for i in range(len(xcodlist)):
#       point_obj.X  = xcodlist[z]
#       point_obj.Y = ycodlist[z]
#       array.add(point_obj)
#       point_obj = arcpy.Point()
#       z = z + 1

#     #SETTING THE POLYGON OBJECT TO CREATE A BOX POLYGON AND CALCULATE AREA........
#     poly_obj = arcpy.Polygon(array)
#     #arcpy.AddMessage(poly_obj.area)

#     #ADDING A NEW ROW OF FEATURE TO THE EMPTY POLYGON FEATURE CLASS........
#     new_row = [poly_obj,z,dataCODE]
#     edit_polys.insertRow(new_row)

#     #COMPLETED FOR ONE POLYGON AND GOING TO THE NEXT FOR LOOP FOR NEXT POLYGON.........

#     #DELETING THE EDIT SESSION AND RESET ................
#     del edit_polys
    
# else:
#     arcpy.AddMessage ("FEATURE CLASS DOES NOT EXIST .............. CREATING!")
#     sp_ref = arcpy.Describe(sampGeodata).spatialReference

#     arcpy.CreateFeatureclass_management(outwkspace,newfc,"POLYGON","","","",sp_ref)
#     arcpy.AddField_management(newfc,"PolyId", "SHORT")
#     arcpy.AddField_management(newfc,"DATACODE", "TEXT","","",8)

#     edit_polys = arcpy.da.InsertCursor(newfc,["SHAPE@","PolyId","DATACODE"])

#     array = arcpy.Array()
#     #SETTING THE POINT OBJECT TO CREATE A BOX ........
#     point_obj = arcpy.Point()
#     z = 0 
#     for i in range(len(xcodlist)):
#       point_obj.X  = xcodlist[z]
#       point_obj.Y = ycodlist[z]
#       array.add(point_obj)
#       point_obj = arcpy.Point()
#       z = z + 1

#     #SETTING THE POLYGON OBJECT TO CREATE A BOX POLYGON AND CALCULATE AREA........
#     poly_obj = arcpy.Polygon(array)
#     #arcpy.AddMessage(poly_obj.area)

#     #ADDING A NEW ROW OF FEATURE TO THE EMPTY POLYGON FEATURE CLASS........
#     arcpy.AddMessage(dataCODE)
    
#     new_row = [poly_obj,z,dataCODE]
#     edit_polys.insertRow(new_row)

#     #COMPLETED FOR ONE POLYGON AND GOING TO THE NEXT FOR LOOP FOR NEXT POLYGON.........

#     #DELETING THE EDIT SESSION AND RESET ................
#     del edit_polys

 
