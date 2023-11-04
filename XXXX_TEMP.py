import xml.etree.ElementTree as ET

filepath =r"D:\MICRONET_DATA\MARS\DATA_XML\DIM_PHR1A_MS_201903310528498_PRJ_4592482101-2.XML"

#tree = ET.parse(r"d:\MICRONET_DATA\MARS\DATA_XML\DIM_PHR1A_MS_201903310528498_PRJ_4592482101-2.XML")
#tree = ET.parse(r"d:\MICRONET_DATA\MARS\DATA_XML\PAZ1_SAR__ORI_SE___SM_D_SRA_20211106T002324_20211106T002331.xml")
#tree = ET.parse(r"d:\MICRONET_DATA\MARS\DATA_XML\WorldDEM_DSM_04_N25_41_E092_16.xml")
tree = ET.parse(r"d:\MICRONET_DATA\MARS\DATA_XML\product.xml")
print ("TREE" + str(tree))

#Getting the root tag..........
root = tree.getroot()
tagg = root.tag
print (tagg)
print (len(root))


##for child in root:
##    print (child[0].tag)

print ("=====================================================================")
    
for i in range(len(root)):
    print ("--------------- "+ str(i) +" ---------------")
    print (root[i].tag + "--"+ str(len(root[i]))+ str(root[i].attrib) + str(root[i].text) )
    
    num = len(root[i]) 
    
##    if num != 0 :
##        for j in range(len(root[i])):
##            # print ("      valueJ:" + str(j))
##            print ("   **" + str(j) +"-" + str(root[i][j].tag) + "--" + str(len(root[i][j])) + str(root[i][j].text))
##            
##            subnum = len(root[i][j])
###            print ("******" + str(subnum))   
##            
##            if subnum != 0 :
##                for k in range(len(root[i][j])):
##                    print ("       ###" + str(k) +"-" + str(root[i][j][k].tag)+ "--" +str(len(root[i][j][k])))
##
##                    ssnum = len(root[i][j][k])                                 
## 
##   
##                    if ssnum != 0 :
##                          for l in range(len(root[i][j][k])):
##                              print ("           @@@@" + str(l) +"-" + str(root[i][j][k][l].tag)+ "--" +str(len(root[i][j][k][l])))
##                              child = len(root[i][j][k][l])                                 
## 
##                              if child != 0 :
##                                  for m in range(len(root[i][j][k][l])):
##                                      print ("              $$$$$" + str(m) +"-" + str(root[i][j][k][l][m].tag)+ "--" +str(len(root[i][j][k][l][m])))
##                                      gchild = len(root[i][j][k][l][m])    
##                                      
##                                      if gchild != 0 : 
##                                          print ("*******gchild************* THE TAG HAS VALUES ********************")
##                                          for n in range(len(root[i][j][k][l][m])):
##                                              print ("                  %%%%%%" + str(m) +"-" + str(root[i][j][k][l][m][n].tag)+ "--" +str(len(root[i][j][k][l][m][n])))
##
##                                              ggchild = len(root[i][j][k][l][m][n])    
##                                              
##                                              if ggchild != 0 : 
##                                                  print ("********ggchild************ THE TAG HAS VALUES ********************")
##
##
##
##


    
###ACESS THE ROOT CHILD .......
##print (root[0].tag)
##print ("---------------")
#
    ##attr= root.attrib
##print (attr)
##
##for c in root.findall('Dataset_Content'):
##     print (c)
##
####from xml.dom import minidom
####
##### parse an xml file by name
####file = minidom.parse('models.xml')
####
#####use getElementsByTagName() to get tag
####models = file.getElementsByTagName('model')
####
##### one specific item attribute
####print('model #2 attribute:')
####print(models[1].attributes['name'].value)
####
##### all item attributes
####print('\nAll attributes:')
####for elem in models:
####  print(elem.attributes['name'].value)
####
##### one specific item's data
####print('\nmodel #2 data:')
####print(models[1].firstChild.data)
####print(models[1].childNodes[0].data)
####
##### all items data
####print('\nAll model data:')
####for elem in models:
####  print(elem.firstChild.data)




##ASHISH SHARMA========================================
##import xml.etree.ElementTree as ET
##tree = ET.parse("d:\MICRONET_DATA\MARS\DATA_XML\image_data.xml")
##root = tree.getroot()
##
##print("Excellent!!!,Now,Iteration!")
##
##for child in root.iter():
##    
##   print("*TAG="+ str(child.tag) +" *ATTB="+ str(child.attrib) + " *TEXT="+ str(child.text))


## XML4
##   for xx in item.iter():
##       print (xx.tag, xx.text)
##       #print ("Attribute = ", xx.attrib)
##       #print ("TTTTTTTText = ", xx.text)
              




##compna = root.find("..//PRODUCER_NAME")
##print (compna)


##comp_na = root.get('version')
##print ("COMPANY NAME: {val}".format(val=comp_na))
##
##xx = ET.Element('PRODUCER_NAME')
##print (xx.text)

##
##print("Excellent!!!,Now,Iteration!")
##
####for child in root.iter():
####    
####   print(child.tag,child.attrib,child.text)
##
##
####Modified Part
##for child in root.find('.//Dataset_Content'):
##   # print(child.tag,child.attrib,child.text)   
##
##    for child1 in child.iter(): 
##       print(child1.tag,child1.attrib,child1.text)


##### DOMAIN PROGRAMMES ####################################################
##from xml.dom import minidom
##
### parse an xml file by name
##file = minidom.parse('models.xml')
##
###use getElementsByTagName() to get tag
##models = file.getElementsByTagName('model')
##
### one specific item attribute
##print('model #2 attribute:')
##print(models[1].attributes['name'].value)
##
### all item attributes
##print('\nAll attributes:')
##for elem in models:
##  print(elem.attributes['name'].value)
##
### one specific item's data
##print('\nmodel #2 data:')
##print(models[1].firstChild.data)
##print(models[1].childNodes[0].data)
##
### all items data
##print('\nAll model data:')
##for elem in models:
##  print(elem.firstChild.data)


