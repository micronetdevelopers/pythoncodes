if arcpy.Exists("WSHEDfc_lyr"):
 



    arcpy.AddField_management(WSHEDfc,"AREASQKM","FLOAT")
    arcpy.AddField_management(WSHEDfc,"DRNP_AREASQKM","DOUBLE")
    arcpy.AddField_management(WSHEDfc,"DRNP_PERC_OFWB","FLOAT")
    arcpy.AddField_management(WSHEDfc,"DRNL_LENKM","DOUBLE")
    arcpy.AddField_management(WSHEDfc,"DRNL_DENSITY","DOUBLE")


#Deleting a table if already exist=============
if arcpy.Exists(gdbpath+"\\MergeTables"):
    arcpy.Delete_management(gdbpath+"\\MergeTables")
#setting table name with path ================
table = gdbpath+"\\MARS_Main_Table"
#adding field ===============
arcpy.AddField_management(table,"TLCODE", "TEXT", "", "",19)

#deleting field ================
arcpy.DeleteField_management(merged_table,["FREQUENCY","TL1CODE","TL2CODE","TL3CODE","TL4CODE","TL5CODE","TL6CODE"])
