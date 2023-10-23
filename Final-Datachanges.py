# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:12:53 2023

@author: PRO-3
"""
###########################################################################################################################################
############################################### PHR-TO-PNEO ###############################################################################

import os
import zipfile
from bs4 import BeautifulSoup

def replace_in_text(content):
    # Replace PHR1B with PNEO3, PHR with PNEO, and Pleiades with Pleiades-Neo
    updated_content = content.replace('PHR1B', 'PNEO4').replace('PHR', 'PNEO').replace('Pleiades', 'Pleiades-Neo').replace('PLEIADES', 'PLEIADES-NEO').replace('0.5', '0.3').replace('http://www.geo-airbusds.com/pleiades/', 'https://www.intelligence-airbusds.com/imagery/constellation/pleiades-neo/')
    return updated_content

def replace_and_save_zip(source_zip_path, destination_zip_path):
    with zipfile.ZipFile(source_zip_path, 'r') as source_zip:
        with zipfile.ZipFile(destination_zip_path, 'w') as destination_zip:
            for file_info in source_zip.infolist():
                # Get the original filename
                original_filename = file_info.filename

                # Read the content of the file
                file_content = source_zip.read(original_filename)

                # Check if the file is a text-based file (you can modify this condition based on your file types)
                text_based_file_types = ('.xml', '.gml', '.xsl', '.html', '.htm', '.txt')
                if original_filename.lower().endswith(text_based_file_types):
                    # Decode the content only for text-based files and replace
                    try:
                        if original_filename.lower().endswith(('.html', '.htm')):
                            # Handle HTML files
                            decoded_content = file_content.decode('utf-8', errors='ignore')
                            updated_content = replace_in_text(decoded_content)
                            file_content = updated_content.encode('utf-8')
                        else:
                            # Handle other text-based files (e.g., XML, TXT)
                            decoded_content = file_content.decode('utf-8', errors='ignore')
                            updated_content = replace_in_text(decoded_content)
                            file_content = updated_content.encode('utf-8')
                    except UnicodeDecodeError:
                        # Handle decoding errors (skip or perform alternate action)
                        print(f"Error decoding {original_filename}. Skipping...")

                # Replace PHR1B with PNEO3, PHR with PNEO, and Pleiades with Pleiades-Neo in the filename
                new_filename = original_filename.replace('PHR1B', 'PNEO4').replace('PHR', 'PNEO').replace('Pleiades', 'Pleiades-Neo').replace('PLEIADES', 'PLEIADES-NEO').replace('0.5', '0.3').replace('http://www.geo-airbusds.com/pleiades/', 'https://www.intelligence-airbusds.com/imagery/constellation/pleiades-neo/')

                # Write the content with the new filename to the destination zip
                destination_zip.writestr(new_filename, file_content)

                print(f"File replaced and saved: {original_filename} to {new_filename}")

# Replace files and save into a new zip file
replace_and_save_zip(r'D:\Data-RnD\PHR-TO-PNEO\PHR-Orignal-Data\Myorder-Mar212019_SO19008910-4-01_DS_PHR1B_201903230538130_FR1_PX_E077N12_1023_01352.ZIP', r'D:\Data-RnD\PHR-TO-PNEO\PNEO-Convert-Data\Myorder-Mar212019_SO19008910-4-01_DS_PNEO4_201903230538130_FR1_PX_E077N12_1023_01352.zip')




### This code working replace with update in file kmz
import os
import zipfile
from bs4 import BeautifulSoup
from io import BytesIO

def replace_in_text(content):
    # Replace PHR1B with PNEO3, PHR-1B with PNEO3, PHR with PNEO, and Pleiades with Pleiades Neo
    updated_content = content.replace('PHR1B', 'PNEO4').replace('PHR-1B', 'PNEO4').replace('PHR', 'PNEO').replace('Pleiades', 'Pleiades Neo').replace('PLEIADES', 'PLEIADES-NEO').replace('0.5', '0.3').replace('http://www.geo-airbusds.com/pleiades/', 'https://www.intelligence-airbusds.com/imagery/constellation/pleiades-neo/')
    return updated_content

def replace_and_save_kmz_in_memory(source_kmz_path):
    modified_kmz_content = BytesIO()  # Use BytesIO to store the modified content in memory

    with zipfile.ZipFile(source_kmz_path, 'r') as source_kmz:
        with zipfile.ZipFile(modified_kmz_content, 'w') as modified_kmz:
            for file_info in source_kmz.infolist():
                # Get the original filename
                original_filename = file_info.filename

                # Read the content of the file
                file_content = source_kmz.read(original_filename)

                # Check if the file is an XML-based file (you can modify this condition based on your file types)
                xml_based_file_types = ('.xml', '.kml')
                if original_filename.lower().endswith(xml_based_file_types):
                    # Decode the content only for XML-based files and replace
                    try:
                        decoded_content = file_content.decode('utf-8', errors='ignore')
                        updated_content = replace_in_text(decoded_content)
                        file_content = updated_content.encode('utf-8')
                    except UnicodeDecodeError:
                        # Handle decoding errors (skip or perform alternate action)
                        print(f"Error decoding {original_filename}. Skipping...")

                # Replace PHR1B with PNEO3, PHR-1B with PNEO3, PHR with PNEO, and Pleiades with Pleiades Neo in the filename
                new_filename = original_filename.replace('PHR1B', 'PNEO4').replace('PHR-1B', 'PNEO4').replace('PHR', 'PNEO').replace('Pleiades', 'Pleiades Neo').replace('PLEIADES', 'PLEIADES-NEO').replace('0.5', '0.3').replace('http://www.geo-airbusds.com/pleiades/', 'https://www.intelligence-airbusds.com/imagery/constellation/pleiades-neo/')

                # Write the content with the new filename to the modified KMZ in memory
                modified_kmz.writestr(new_filename, file_content)

                print(f"File replaced and saved to memory: {original_filename} to {new_filename}")

    return modified_kmz_content.getvalue(), new_filename  # Return the modified content and the new filename

def replace_original_file_with_modified_content(modified_kmz_content, original_kmz_path, new_filename):
    # Remove the original file
    os.remove(original_kmz_path)

    # Save the modified content to a new file using the original file name
    with open(original_kmz_path, 'wb') as new_kmz_file:
        new_kmz_file.write(modified_kmz_content)

# Replace files and save into a new KMZ file in memory
modified_kmz_content, new_filename = replace_and_save_kmz_in_memory(
    r"D:\Data-RnD\PHR-TO-PNEO\PNEO-Convert-Data\Myorder-Mar212019_SO19008910-4-01_DS_PNEO4_201903230538130_FR1_PX_E077N12_1023_01352\3917261101\IMG_PNEO4_PMS_001\PREVIEW_PNEO4_PMS_201903230538130_ORT_3917261101.KMZ"
)


# Replace the original file with the modified content
replace_original_file_with_modified_content(
    modified_kmz_content,
    # here dont the single string into the double string
    r'D:\Data-RnD\PHR-TO-PNEO\PNEO-Convert-Data\Myorder-Mar212019_SO19008910-4-01_DS_PNEO4_201903230538130_FR1_PX_E077N12_1023_01352\3917261101\IMG_PNEO4_PMS_001\PREVIEW_PNEO4_PMS_201903230538130_ORT_3917261101.KMZ',
    new_filename
)    
###################################################################################################################################################    
###################################################################################################################################################
    
    
    
    
    
###################################################################################################################################################    
################################################# PNEO-TO-PHR ##################################################################################### 
     

import os
import zipfile
from bs4 import BeautifulSoup

def replace_in_text(content):
    # Replace PHR1B with PNEO3, PHR with PNEO, and Pleiades with Pleiades-Neo
    updated_content = content.replace('PNEO3', 'PHR1A').replace('PNEO', 'PHR').replace('Pleiades-Neo','Pleiades').replace('PLEIADES', 'PLEIADES-NEO').replace('0.3', '0.5').replace('https://www.intelligence-airbusds.com/imagery/constellation/pleiades-neo/','http://www.geo-airbusds.com/pleiades/')
    return updated_content

def replace_and_save_zip(source_zip_path, destination_zip_path):
    with zipfile.ZipFile(source_zip_path, 'r') as source_zip:
        with zipfile.ZipFile(destination_zip_path, 'w') as destination_zip:
            for file_info in source_zip.infolist():
                # Get the original filename
                original_filename = file_info.filename

                # Read the content of the file
                file_content = source_zip.read(original_filename)

                # Check if the file is a text-based file (you can modify this condition based on your file types)
                text_based_file_types = ('.xml', '.gml', '.xsl', '.html', '.htm', '.txt')
                if original_filename.lower().endswith(text_based_file_types):
                    # Decode the content only for text-based files and replace
                    try:
                        if original_filename.lower().endswith(('.html', '.htm')):
                            # Handle HTML files
                            decoded_content = file_content.decode('utf-8', errors='ignore')
                            updated_content = replace_in_text(decoded_content)
                            file_content = updated_content.encode('utf-8')
                        else:
                            # Handle other text-based files (e.g., XML, TXT)
                            decoded_content = file_content.decode('utf-8', errors='ignore')
                            updated_content = replace_in_text(decoded_content)
                            file_content = updated_content.encode('utf-8')
                    except UnicodeDecodeError:
                        # Handle decoding errors (skip or perform alternate action)
                        print(f"Error decoding {original_filename}. Skipping...")

                # Replace PHR1B with PNEO3, PHR with PNEO, and Pleiades with Pleiades-Neo in the filename
                new_filename = original_filename.replace('PNEO3','PHR1A').replace('PNEO', 'PHR').replace('Pleiades-Neo','Pleiades').replace('PLEIADES', 'PLEIADES-NEO').replace('0.3', '0.5').replace('https://www.intelligence-airbusds.com/imagery/constellation/pleiades-neo/','http://www.geo-airbusds.com/pleiades/')

                # Write the content with the new filename to the destination zip
                destination_zip.writestr(new_filename, file_content)

                print(f"File replaced and saved: {original_filename} to {new_filename}")

# Replace files and save into a new zip file
replace_and_save_zip(r'D:\Data-RnD\PNEO-TO-PHR\PNEO-Origanl-data\WO_000116673_1_2_SAL23103902-2_ACQ_PNEO3_03232408226692.ZIP', r'D:\Data-RnD\PNEO-TO-PHR\PHR-Convert-data\WO_000116673_1_2_SAL23103902-2_ACQ_PHR1A_03232408226692.ZIP')




import os
import zipfile
from bs4 import BeautifulSoup
from io import BytesIO

def replace_in_text(content):
    # Replace PHR1B with PNEO3, PHR-1B with PNEO3, PHR with PNEO, and Pleiades with Pleiades Neo
    updated_content = content.replace('PNEO3' , 'PHR1A').replace('PNEO3' , 'PHR-1A').replace('PNEO','PHR').replace('Pleiades Neo','Pleiades').replace('PLEIADES-NEO','PLEIADES').replace('0.3', '0.5').replace('https://www.intelligence-airbusds.com/imagery/constellation/pleiades-neo/','http://www.geo-airbusds.com/pleiades/')
    return updated_content

def replace_and_save_kmz_in_memory(source_kmz_path):
    modified_kmz_content = BytesIO()  # Use BytesIO to store the modified content in memory

    with zipfile.ZipFile(source_kmz_path, 'r') as source_kmz:
        with zipfile.ZipFile(modified_kmz_content, 'w') as modified_kmz:
            for file_info in source_kmz.infolist():
                # Get the original filename
                original_filename = file_info.filename

                # Read the content of the file
                file_content = source_kmz.read(original_filename)

                # Check if the file is an XML-based file (you can modify this condition based on your file types)
                xml_based_file_types = ('.xml', '.kml')
                if original_filename.lower().endswith(xml_based_file_types):
                    # Decode the content only for XML-based files and replace
                    try:
                        decoded_content = file_content.decode('utf-8', errors='ignore')
                        updated_content = replace_in_text(decoded_content)
                        file_content = updated_content.encode('utf-8')
                    except UnicodeDecodeError:
                        # Handle decoding errors (skip or perform alternate action)
                        print(f"Error decoding {original_filename}. Skipping...")

                # Replace PHR1B with PNEO3, PHR-1B with PNEO3, PHR with PNEO, and Pleiades with Pleiades Neo in the filename
                new_filename = original_filename.replace('PNEO3','PHR1A').replace('PNEO3','PHR-1A').replace('PNEO','PHR').replace('Pleiades Neo','Pleiades').replace('PLEIADES-NEO','PLEIADES').replace('0.3', '0.5').replace('https://www.intelligence-airbusds.com/imagery/constellation/pleiades-neo/','http://www.geo-airbusds.com/pleiades/')

                # Write the content with the new filename to the modified KMZ in memory
                modified_kmz.writestr(new_filename, file_content)

                print(f"File replaced and saved to memory: {original_filename} to {new_filename}")

    return modified_kmz_content.getvalue(), new_filename  # Return the modified content and the new filename

def replace_original_file_with_modified_content(modified_kmz_content, original_kmz_path, new_filename):
    # Remove the original file
    os.remove(original_kmz_path)

    # Save the modified content to a new file using the original file name
    with open(original_kmz_path, 'wb') as new_kmz_file:
        new_kmz_file.write(modified_kmz_content)

# Replace files and save into a new KMZ file in memory
modified_kmz_content, new_filename = replace_and_save_kmz_in_memory(
    r"D:\Data-RnD\PNEO-TO-PHR\PHR-Convert-data\WO_000116673_1_2_SAL23103902-2_ACQ_PHR1A_03232408226692\000116673_1_2_STD_A\IMG_01_PHR1A_PMS-FS\PREVIEW_PHR1A_202308040551179_PMS-FS_ORT_PWOI_000116673_1_2_F_1.KMZ"
)


# Replace the original file with the modified content
replace_original_file_with_modified_content(
    modified_kmz_content,
    # here dont the single string into the double string allways in single string
    r'D:\Data-RnD\PNEO-TO-PHR\PHR-Convert-data\WO_000116673_1_2_SAL23103902-2_ACQ_PHR1A_03232408226692\000116673_1_2_STD_A\IMG_01_PHR1A_PMS-FS\PREVIEW_PHR1A_202308040551179_PMS-FS_ORT_PWOI_000116673_1_2_F_1.KMZ',
    new_filename
)   

###################################################################################################################################################
################################################################################################################################################### 


###############################################################################################################################################
### Pdf edit

from pikepdf import Pdf, Page

example = Pdf.open(r'D:\Data-RnD\doc\PNEO_zip_file\3917261101\DELIVERY.pdf')

print(example)


import aspose.pdf as ap

# Load the PDF document
document = ap.Document(r'D:\Data-RnD\doc\PNEO_zip_file\3917261101\DELIVERY.pdf')

# Instantiate a TextFragmentAbsorber object
txtAbsorber = ap.text.TextFragmentAbsorber("PHR1B")

# Search text
document.pages.accept(txtAbsorber)

# Get reference to the found text fragments
textFragmentCollection = txtAbsorber.text_fragments

# Parse all the searched text fragments and replace text
for txtFragment in textFragmentCollection:
    # Replace "PHR1B" with "PNEO4"
    txtFragment.text = txtFragment.text.replace("PHR1B", "PNEO4")

# Save the updated PDF
document.save(r'D:\Data-RnD\doc\PNEO_zip_file\3917261101\O.pdf')



from PyPDF2 import PdfFileReader, PdfFileWriter

replacements = [
    ("PHR1B", "PNEO4")
]

pdf = PdfFileReader(open("D:\Data-RnD\doc\PNEO_zip_file\3917261101\DELIVERY.pdf", "rb"))
writer = PdfFileWriter() 

for page in pdf.pages:
    contents = page.getContents().getData()
    for (a,b) in replacements:
        contents = contents.replace(a.encode('utf-8'), b.encode('utf-8'))
    page.getContents().setData(contents)
    writer.addPage(page)
    
with open("D:\Data-RnD\doc\PNEO_zip_file\3917261101\modified.pdf", "wb") as f:
     writer.write(f)












