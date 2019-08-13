# This script takes a concatenated list of Dublin Core records and splits it into one text file for each record.  It also adds a header, so that the record will validate.
# This was written by Kevin Nance and modified by Randy Fischer.
# The purpose of this script is preparing metadata in migration from CONTENTdm.


#!/usr/bin/env python

import os
import pdb
import sys


###CHANGE THESE VARIABLES AS NEEDED###

#Python script and sample xml file to have records split should
#be in own subdirectory

#Name of working directory
# Updates script to correct directory folder
#directory = "/ucf-collection/sample_export_20190703"
directory = "/ucf-collection/minaRunScripts"

#Name of XML File that will be split into individual record files (with extension)
#XMLFileToBeSplit = "CONTENTdmCustomexport_20190617.xml"
#XMLFileToBeSplit = "CFM_FLVC1_export_20190703.xml"
XMLFileToBeSplit = "CFM_FLVC1export_20190717.xml"

#--------------------------------------------------------
def main():


    if len(sys.argv) != 2:
        usage()
        sys.exit(-1)

    XMLFileToBeSplit = sys.argv[1]

    os.chdir(directory)
    cwd = os.getcwd()

    print (cwd)

    # Opens file to be split located in subdirectory
    #f = open("PythonCode\\" + XMLFileToBeSplit, encoding="utf8")
    f = open(XMLFileToBeSplit, encoding="utf8")
    print ("Name of the file: ", f.name, "\n")

    initialRecTotal = 0
    finalRecTotal = 0
    duplicate = 0
    listOfDuplicates = []

    #Counts number of record files there SHOULD be at the end
    for line in f:
        if "<record>" in line:
            initialRecTotal += 1

    print ("[" + str(initialRecTotal) + "] records found in designated XML file\n")
    f.seek(0)

    boilerplateStart = """<oai_dc:dc xmlns:dc="http://purl.org/dc/elements/1.1/"
               xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
            """
    boilerplateEnd = """
    </oai_dc:dc>
    """
       
    for line in f: #Will run through entire XML file contents
    
        contents = ""       #Stores text within record labels
        dp = ""             #Stores DP* to be used for file name
        dpFound = False     #Makes it so only the first dc identifier is taken
        title = ""
        titleFound = False
    
        if "<record>" in line:
        
            for x in range(1000):   #Checks this many lines within a record
                                    #a finite number is used to prevent a possible
                                    #infinite loop due to a wonky XML export
                                    #shouldn't need to change
            
                line = f.readline()
            
                #Grabs Titles and DP* as it parses through text
                if dpFound == False and "<dc:identifier>" in line:
                    dp = line
                
                    #Trims and Cleans DP*
                    dp = dp.replace('<dc:identifier>','')
                    dp = dp.replace('</dc:identifier>','')
                    dp = dp.replace(' ', '')
                    dp = dp.replace('\n', '')
                    dp = dp.replace('\t', '')
                    dp = dp.strip()
                    dp = dp[:9]
                
                    dpFound = True
                
                if titleFound == False and "<dc:title>" in line:
                    title = line
                    titleFound = True
                
                if dpFound == True and "</record>" in line:
                
                    if os.path.isfile(str(dp) + ".dc"):  #DP* Duplicate Check
                                                            #Uses Title Instead
                        #Trims and Cleans Title
                        title = title.replace('<dc:title>','')
                        title = title.replace('<','')
                        title = title.replace('>','')
                        title = title.replace(':','')
                        title = title.replace('?','')
                        title = title.replace('\'','')
                        title = title.replace('/','')
                        title = title.replace('*','')
                        title = title.replace('\n','')
                        title = title.replace('\t','')
                        title = title.replace('.','')
                        title = title[4:]

                        print ("\t DP* file already exists, using title for name")
                        print (title)

                        if os.path.isfile(str(title) + ".dc"):   #Title Duplicate
                            duplicate += 1
                            print ("DUPLICATE! FILE WAS DELETED!!" + str(title))
                            listOfDuplicates.append(title)
                            finalRecTotal -= 1
                    
                        recFile = open(str(title) + ".dc", "w", encoding="utf-8")


                        contents = boilerplateStart + contents + boilerplateEnd
                        recFile.write(contents)
                        recFile.close()
                    
                        finalRecTotal += 1

                    elif dp == "":                        #DP* NULL Check
                                                        #Uses Title Instead
                        #Trims and Cleans Title
                        title = title.replace('<dc:title>','')
                        title = title.replace('</dc:title>','')
                        title = title.replace('<','')
                        title = title.replace('>','')
                        title = title.replace(':','')
                        title = title.replace('?','')
                        title = title.replace('\'','')
                        title = title.replace('/','')
                        title = title.replace('*','')
                        title = title.replace('\n','')
                        title = title.replace('\t','')
                        title = title.replace('.','')
                        title = title[4:]

                        print ("\t DP* doesn't exist, using title for name")
                        print (title)

                        if os.path.isfile(str(title) + ".dc"):   #Title Duplicate
                            duplicate += 1
                            print ("DUPLICATE! FILE WAS DELETED!!" + str(title))
                            listOfDuplicates.append(title)
                            finalRecTotal -= 1
                    
                        recFile = open(str(title) + ".dc", "w", encoding="utf-8")
                        contents = boilerplateStart + contents + boilerplateEnd
                        recFile.write(contents)
                        recFile.close()

                        finalRecTotal += 1
                    else:               #If no edge cases uses DP* as normal

                        print ("Generating individual record for DP*: " + dp)
                    
                        recFile = open(str(dp) + ".dc", "w", encoding="utf-8")
                        contents = boilerplateStart + contents + boilerplateEnd
                        recFile.write(contents)
                        recFile.close()
                        finalRecTotal += 1
                    
                    break
                else:
                    contents = contents + line

   #Concluding print statements
    print ("\n****************************************")
    print ("\n********* Program has Finished *********")
    print ("\n********* Program has Finished *********")
    print ("\t\t" + str(finalRecTotal) + " / " + str(initialRecTotal))
    print ("\n****************************************")
    f.close()

    print ("# of Duplicates (files overwritten): " + str(duplicate))
    print(listOfDuplicates, sep = "\n")


def usage ():
    print ("")
    print ("usage: %s path_and_file_name"  % (sys.argv[0]))
    print ("")
    print ("")
    sys.exit(0)



#--------------------------------
if __name__ == "__main__":
    main()

