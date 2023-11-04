import xml.etree.ElementTree as ET
import arcpy
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
#  Main program initiated  : 13/07/2023 
#============================================================================================

#============================================================================================
#PARAMETERS SETTING AS INPUT *********************************************************
#============================================================================================
xmlDir = arcpy.GetParameterAsText(0)
##dirname = os.path.split(xmlDir)
##xmlpath = dirname[0]
##xmldata = dirname[1]

###--------------------------------------------------------
xmlList = os.listdir(xmlDir)
###--------------------------------------------------------

gdbpath = arcpy.GetParameterAsText(1)
gdbpath = gdbpath+"\\"
arcpy.AddMessage("GDB Path is: "+gdbpath)
arcpy.AddMessage(" ")

arcpy.AddMessage(" ")

##arcpy.AddMessage (xmldpath)
##arcpy.AddMessage (xmldata)
arcpy.AddMessage (xmlDir)
arcpy.AddMessage (xmlList)
arcpy.AddMessage(" ")

##for i in range(len(xmlList)):
##    arcpy.AddMessage(xmlList[i])


#============================================================================================
arcpy.env.workspace = gdbpath
#============================================================================================

#============================================================================================
## EXTRACTING THE XML TYPE BASED ON THE SATELLITE/SENSOR TYPE ***************************
#============================================================================================

for i in range(len(xmlList)):
    arcpy.AddMessage(xmlList[i])
    xmldata= "{0}".format(xmlList[i])
    xmlData= xmlDir+"\\"+xmldata
    arcpy.AddMessage("========="+xmlData)
    arcpy.AddMessage("+++++++++"+xmldata)
    
    
    xmlSplit = xmldata.split("_")
    xmlFirst = "{0}".format(xmlSplit[0]); xmlSecond = "{0}".format(xmlSplit[1])
    arcpy.AddMessage(xmlFirst + "**" + xmlSecond)

    dataCODE = ''

    if xmlFirst == "DIM" :
        if xmlSecond == "PHR1A" or xmlSecond == "PHR1B" or xmlSecond == "PNEO3" or xmlSecond == "PNEO4"                            or xmlSecond == "SPOT6" or xmlSecond == "SPOT7":
            arcpy.AddMessage("**********************PROCESSING AIRBUS DATA :" + xmlSecond)
            dataCODE = "AB"+ str(random.randrange(100000, 999999))
        elif xmlSecond == "PNEOXX":
            arcpy.AddMessage("**********************Pleadeous NEO - 3 ")
            dataCODE = "PL"+ str(random.randrange(100000, 999999))
        else :
            arcpy.AddMessage("THE FILE NAME IS NOT IN PROPER FORMAT..... PLEASE CHECK !")


    arcpy.AddMessage("======================"+dataCODE)
    ##arcpy.AddMessage("==========================="+BUIISHIT)
    ##exit()



    #============================================================================================
    #SETTING THE XML READ VARIABLES ********************************************************
    #============================================================================================
    #tree = ET.parse("d:\MICRONET_DATA\MARS\DATA_XML\image_data.xml")
    arcpy.AddMessage("======================="+xmlData)
    tree = ET.parse(xmlData)
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
        arcpy.AddMessage ("$$$$$$$$$$$$$$$$" + dtilesTF)   
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
        arcpy.AddMessage  ("$$$$$$$$$$$"+item.tag+ item.text)
        dPIXx = '{}'.format(item.text)
        dPixelx = float(dPIXx) ;
        dPixely = float(dPIXx) ;
        if item.text != '' :  break
                        

    ###=================================================================================================

    ###PRINTING VARIABLES ==============================================================================
    arcpy.AddMessage ("----------------------------------------------------------------------------------------")
    arcpy.AddMessage ("XLM FILE NAME ===== "+ xmldata)
    arcpy.AddMessage ("DATABASE CODE ===== "+ dataCODE)
    arcpy.AddMessage ("DATABASE NAME ===== "+ dataName)
    arcpy.AddMessage ("COMPANY NAME ====== "+ compName)
    arcpy.AddMessage ("SATELLITE NAME ==== "+ satName)
    arcpy.AddMessage ("CUSTOMER ID   ===== "+ clRef)
    arcpy.AddMessage ("SENSOR NAME ======= "+ senName)
    arcpy.AddMessage ("DATA PROCESS LEVEL= "+ imgDataProcessLevel)
    arcpy.AddMessage ("DATA SPECTRAL PROC. "+ imgDataProcessSpec)
    arcpy.AddMessage ("IMAGING DATE ====== "+ imgDate)
    arcpy.AddMessage ("SURFACE AREA(sqkm)= "+ str(dArea))
    arcpy.AddMessage ("QL PATH =========== "+ dQLname)
    arcpy.AddMessage ("DATA FORMAT ======= "+ dFormat)
    arcpy.AddMessage ("CLOUD COVERAGE ==== "+ dCloud)
    arcpy.AddMessage ("SNOW COVERAGE ===== "+ str(dSnow))
    arcpy.AddMessage ("ACQUISITION RANGE== "+ dAQrange)
    arcpy.AddMessage ("PRODUCT RANGE  ==== "+ dPRrange)
    arcpy.AddMessage ("PROJECTION TABLE == "+ dPRJtable)
    arcpy.AddMessage ("PROJECTION NAME === "+ dPRJname)

    arcpy.AddMessage ("DATA ROWS NO ====== "+ str(dRows))
    arcpy.AddMessage ("DATA COLUMNS NO === "+ str(dCols))
    arcpy.AddMessage ("DATA BANDS NO ===== "+ str(dBands))
    arcpy.AddMessage ("DATA TILES NO ===== "+ str(dTiles))
    arcpy.AddMessage ("DATA TYPE ========= "+ dType)
    arcpy.AddMessage ("DATA BITS ========= "+ str(dBits))
    arcpy.AddMessage ("DATA SIGNAGE ====== "+ dSign)
    arcpy.AddMessage ("INCIDENCE ANGLE==== "+ str(dINangle))
    arcpy.AddMessage ("GSD ACROSS PATH==== "+ str(dGSDaxt))
    arcpy.AddMessage ("GSD ALONG PATH===== "+ str(dGSDalt))
    arcpy.AddMessage ("PIXEL IN X DIR===== "+ str(dPixelx))
    arcpy.AddMessage ("PIXEL IN Y DIR===== "+ str(dPixely))
                         
    arcpy.AddMessage ("----------------------------------------------------------------------------------------")
    arcpy.AddMessage (" ")

    ###=================================================================================================

    ###==PARSING THE BAND NAME, ITS START SPECTRAL MICROMETER AND END MICROMETER=======================
    bandList= [] ; specMinList = [] ; specMaxList = []       

    if xmlSecond == "PHR1A" or xmlSecond == "PHR1B" or xmlSecond == "SPOT6" or xmlSecond == "SPOT7":
        for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/MEASURE_UNIT'):
            arcpy.AddMessage  (item.tag + " MEASURE UNIT PHR " + item.text)
            bameasureUnit = '{}'.format(item.text) #saving the unit for conversion from nanometers to micrometer
            
        for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/BAND_ID'):
            #arcpy.AddMessage  (item.tag + "band" + item.text)
            bandList.append(item.text)
        for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/MIN'):
            arcpy.AddMessage  (item.tag + "Start" + item.text)
            if bameasureUnit == 'nanometers' or bameasureUnit == 'nanometer':
                spec = float('{}'.format(item.text))/1000
                arcpy.AddMessage (str(spec))
                specMinList.append(spec)
            else: 
                specMinList.append(item.text)
        for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/MAX'):
            arcpy.AddMessage  (item.tag + " END " + item.text)
            if bameasureUnit == 'nanometers' or bameasureUnit == 'nanometer':
                spec = float('{}'.format(item.text))/1000
                arcpy.AddMessage (str(spec))
                specMaxList.append(spec)
            else: 
                specMaxList.append(item.text)

    elif xmlSecond == "PNEO3" or xmlSecond == "PNEO4":
        for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/MEASURE_UNIT'):
            arcpy.AddMessage  (item.tag + " MEASURE_UNIT_PNEO " + item.text)
            bameasureUnit = '{}'.format(item.text) #saving the unit for conversion from nanometers to micrometer

        for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/BAND_ID'):
            #arcpy.AddMessage  (item.tag + "band" + item.text)
            bandList.append(item.text)
        for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/FWHM/MIN'):
            arcpy.AddMessage  (item.tag + " Start " + item.text)
            if bameasureUnit == 'nanometer' or bameasureUnit == 'nanometers':
                spec = float('{}'.format(item.text))/1000
                arcpy.AddMessage (str(spec))
                specMinList.append(spec)
            else: 
                specMinList.append(item.text)
        for item in root.findall('./Radiometric_Data/Radiometric_Calibration/Instrument_Calibration/Band_Measurement_List/Band_Spectral_Range/FWHM/MAX'):
            arcpy.AddMessage  (item.tag + " end " + item.text)
            if bameasureUnit == 'nanometer' or bameasureUnit == 'nanometers':
                spec = float('{}'.format(item.text))/1000
                arcpy.AddMessage (str(spec))
                specMaxList.append(spec)
            else: 
                specMaxList.append(item.text)
    else :
        arcpy.AddMessage ("COULD NOT FIGURE OUT THE DATA .................................PLEASE CHECK!")   

    if len(bandList) == 0 and imgDataProcessSpec == 'PMS':
        arcpy.AddMessage ("******* I AM IN PMS*****************"+ str(len(bandList))+"---"+imgDataProcessSpec )
        for j in range(dBands):
            arcpy.AddMessage (j)
            bandList.append(j+1); specMinList.append(int(1)); specMaxList.append(int(255))

            

    arcpy.AddMessage (bandList)
    arcpy.AddMessage (specMinList)
    arcpy.AddMessage (specMaxList)
    arcpy.AddMessage (len(bandList))
    arcpy.AddMessage (len(specMinList))
    arcpy.AddMessage (len(specMaxList))


    ###=================================================================================================

    ###==PARSING THE AOI BOUND CORNER CORDINATES =======================================================
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
    ###=================================================================================================
    arcpy.AddMessage ("----------------------------------------------------------------------------------------")
    arcpy.AddMessage ("-BANDS INFORMATION---------------------------------------------------------")
    for r in range(len(bandList)):
        arcpy.AddMessage (str(bandList[r])+"="+str(specMinList[r])+"-"+ str(specMaxList[r]))

    arcpy.AddMessage ("----------------------------------------------------------------------------------------")
    arcpy.AddMessage (" ")
    arcpy.AddMessage ("----------------------------------------------------------------------------------------")

    arcpy.AddMessage ("-BOUND VERTICES------------------------------------------------------------")
    for r in range(len(xcodlist)):
        arcpy.AddMessage (str(r+1)+":="+xcodlist[r]+"-"+ ycodlist[r])

    arcpy.AddMessage ("----------------------------------------------------------------------------------------")
    arcpy.AddMessage (" ")




##    arcpy.AddMessage (BULLSHIT)


    ###=================================================================================================
    ###=================================================================================================
    ### READING AND WRITING THE TABLE (PRESENTLY ARCGIS OBJECT TABLE IS CONSIDERED)
    ###=================================================================================================
    ###=================================================================================================

    ### ------------------------------------------------------------------------------------------------
    ### WRITING TO THE DATA FILE (MARS_Main_Data) ******************************************************
    ### ------------------------------------------------------------------------------------------------
    arcpy.AddMessage (" ")
    arcpy.AddMessage ("======================================================================================")
    arcpy.AddMessage ("========= R E A D I N G  AND  W R I T I N G  TO  F I L E =============================")
    arcpy.AddMessage ("======================================================================================")
    arcpy.AddMessage ("========= WRITING TO FILE MARS_Main_Data =============================================")
    arcpy.AddMessage ("======================================================================================")

    outname = "MARS_Main_Data"
    incursor = arcpy.da.InsertCursor(gdbpath+outname,("DATACODE","DATANAME","COMP_NA","SATT_NA","CL_REF","SEN_NAME",\
              "IMG_DAPROC","IMG_DATE","DAREA","DQLNAME","DFORMAT","DCLOUD","DSNOW","D_AQ_BITS","D_PR_BITS","DPRJ_TABLE",\
              "DPRJ_NAME","D_NROWS","D_NCOLS","D_BANDS","D_NTILES","D_TYPE","D_NBITS","D_SIGN","D_IN_ANGL","D_GSD_AXT",\
              "D_GSD_ALT","D_PIXELX","D_PIXELY","XML_FILE"))
    incursor.insertRow([dataCODE,dataName,compName,satName,clRef,senName,imgDataProcessLevel,imgDate,dArea,dQLname,\
                        dFormat,dCloud,dSnow,dAQrange,dPRrange,dPRJtable,dPRJname,dRows,dCols,dBands,dTiles,dType,\
                        dBits,dSign,dINangle,dGSDaxt,dGSDalt,dPixelx,dPixely,xmldata])
    del incursor
    arcpy.AddMessage ("======================================================================================")
    arcpy.AddMessage (" ")

    ### ------------------------------------------------------------------------------------------------

    ### ------------------------------------------------------------------------------------------------
    ### WRITING THE DATA TO THE BAND FILE (BAND_Info)***********************************************
    ### ------------------------------------------------------------------------------------------------
    arcpy.AddMessage ("======================================================================================")
    arcpy.AddMessage ("========= WRITING TO FILE BAND_info ==================================================")
    arcpy.AddMessage ("======================================================================================")
    outname = "BAND_info"
    for r in range(len(bandList)):
        arcpy.AddMessage (str(bandList[r])+"="+str(specMinList[r])+"-"+ str(specMaxList[r]))
        incursor = arcpy.da.InsertCursor(gdbpath+outname,("DATACODE","BND_NAME","BND_S_SPEC","BND_E_SPEC"))
        incursor.insertRow([dataCODE,bandList[r],specMinList[r],specMaxList[r]])
        del incursor
    arcpy.AddMessage ("======================================================================================")
    arcpy.AddMessage (" ")
    ### ------------------------------------------------------------------------------------------------

    ### ------------------------------------------------------------------------------------------------
    ### WRITING THE DATA TO THE BAND FILE (BAND_Info)***********************************************
    ### ------------------------------------------------------------------------------------------------
    arcpy.AddMessage ("======================================================================================")
    arcpy.AddMessage ("========= WRITING TO FILE BOUND_info =================================================")
    arcpy.AddMessage ("======================================================================================")
    outname = "BOUND_info"
    for r in range(len(xcodlist)):
        rr = r +1 
        arcpy.AddMessage (str(rr)+":="+xcodlist[r]+"-"+ ycodlist[r])
        incursor = arcpy.da.InsertCursor(gdbpath+outname,("DATACODE","COOD_NO","COOD_XX","COOD_YY"))
        incursor.insertRow([dataCODE,rr,xcodlist[r],ycodlist[r]])
        del incursor
    arcpy.AddMessage ("======================================================================================")
    arcpy.AddMessage (" ")
    ### ------------------------------------------------------------------------------------------------



               
##arcpy.AddMessage (BULLSHIT)
