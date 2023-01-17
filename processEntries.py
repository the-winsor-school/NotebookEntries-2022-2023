import csv
import itertools
import os
import subprocess
import calendar

import styleStrips, styleBlock

def readCSV():
    # Read in each CSV file and create a list of dictionaries
    with open("data/business.csv") as afile:
        businessFile = csv.DictReader(afile)
        businessData = list(businessFile)

    with open("data/building.csv") as bfile:
        buildFile = csv.DictReader(bfile)
        buildData = list(buildFile)

    with open("data/coding.csv") as cfile:
        codingFile = csv.DictReader(cfile)
        codingData = list(codingFile)

    with open("data/wholeTeam.csv") as wfile:
        wholeFile = csv.DictReader(wfile)
        wholeData = list(wholeFile)

    return (businessData, buildData, codingData, wholeData)

def computeDateList(businessData, buildData, codingData, wholeData): 
    # Gather up a master list of all of dates of meetings by reading through every entry
    aDates = [businessData[i]['Date'].split(" ")[0] for i in xrange(len(businessData))]
    bDates = [buildData[i]['Date'].split(" ")[0] for i in xrange(len(buildData))] 
    cDates = [codingData[i]['Date'].split(" ")[0] for i in xrange(len(codingData))]
    wDates = [wholeData[i]['Date'].split(" ")[0] for i in xrange(len(wholeData))]
    # Taking the set removes duplicates. Then return an unsorted list
    allDates = list(set(aDates + bDates + cDates + wDates))
    return allDates

def findIndicesForDateAndTeam(allData, date, teamNumber):
    # For a given date, find all of the entries in allData that correspond to that date. 
    # For a given team, find all of the entries in allData that correspond to that team
    matching = []
    for i in xrange(len(allData)):
        rawDay = allData[i]['Date'].split(" ")[0]
        rawTeam = allData[i]['Team'].split(" ")[0]
        if rawDay == date and ((str(teamNumber) in rawTeam) or ('Both' in rawTeam) or ('Fill' in rawTeam)):
            matching.append(i)
    return matching  

def displayDate(date):
    # Convert the date format. i.e. "12/7/2020" -> December 7, 2020
    [m, d, y] = date.split("/")
    return calendar.month_name[int(m)] + ' ' + d + ', ' + y

def generateLatexStrips(style, businessData, buildData, codingData, wholeData, meeting_date, teamNumber):
    # For a particular meeting_data, generate the corresponding LaTeX page and write to meeting_date.tex
    # There is a lot of list comprehension because each subteam may have multiple entries per date

    # Find the list indices for all the entries corresponding to this date
    aidx = findIndicesForDateAndTeam(businessData, meeting_date, teamNumber)
    bidx = findIndicesForDateAndTeam(buildData, meeting_date, teamNumber)
    cidx = findIndicesForDateAndTeam(codingData, meeting_date, teamNumber)
    widx = findIndicesForDateAndTeam(wholeData, meeting_date, teamNumber)
    
    # Crate a nicely formatted date
    date_pretty = displayDate(meeting_date)
    # Generate the header block with the date and members list
    date = style.formatDate(date_pretty) 

    ###################################
    # For each of our three headers, write the header (including the dotted line)
    # Then, within each header, if that subteam has entries, generate the color box for each entry
    focus = style.focusHeader
    summary = style.summaryHeader
    challenges = style.challengesHeader
    nextSteps = style.nextStepsHeader 

    # If exists entries for each date, generate blocks
    if (len(widx) > 0):
        focus += " ".join([style.wholeBlock(wholeData[widx[f]]['Focus'], f) for f in xrange(len(widx))])
        summary += " ".join([style.wholeBlock(wholeData[widx[s]]['Summary'], s) for s in xrange(len(widx))])
        challenges += " ".join([style.wholeBlock(wholeData[widx[c]]['Challenges/Problems'], c) for c in xrange(len(widx))])
        nextSteps += " ".join([style.wholeBlock(wholeData[widx[n]]['Next Steps'], n) for n in xrange(len(widx))])

    if (len(bidx) > 0):
        focus += " ".join([style.buildBlock(buildData[bidx[f]]['Focus'], f) for f in xrange(len(bidx))])
        summary += " ".join([style.buildBlock(buildData[bidx[s]]['Summary'], s) for s in xrange(len(bidx))])
        challenges += " ".join([style.buildBlock(buildData[bidx[c]]['Challenges/Problems'], c) for c in xrange(len(bidx))])
        nextSteps += " ".join([style.buildBlock(buildData[bidx[n]]['Next Steps'], n) for n in xrange(len(bidx))])

    if (len(cidx) > 0):
        focus += " ".join([style.codingBlock(codingData[cidx[f]]['Focus'], f) for f in xrange(len(cidx))])
        summary += " ".join([style.codingBlock(codingData[cidx[s]]['Summary'], s) for s in xrange(len(cidx))])
        challenges += " ".join([style.codingBlock(codingData[cidx[c]]['Challenges/Problems'], c) for c in xrange(len(cidx))])
        nextSteps += " ".join([style.codingBlock(codingData[cidx[n]]['Next Steps'], n) for n in xrange(len(cidx))])

    if (len(aidx) > 0):
        focus += " ".join([style.businessBlock(businessData[aidx[f]]['Focus'], f) for f in xrange(len(aidx))])
        summary += " ".join([style.businessBlock(businessData[aidx[s]]['Summary'], s) for s in xrange(len(aidx))])
        challenges += " ".join([style.businessBlock(businessData[aidx[c]]['Challenges/Problems'], c) for c in xrange(len(aidx))])
        nextSteps += " ".join([style.businessBlock(businessData[aidx[n]]['Next Steps'], n) for n in xrange(len(aidx))])

    # Gather all of the material in order. "material" is a string file that contains the entire LaTeX document
    material = style.header + date + focus + summary + challenges + nextSteps + style.footer
    ###################################

    # Need to reformat date to not use backslashes in the filename
    save_date = meeting_date.replace('/', '_')
    fileName = 'pages/{}/{}.tex'.format(teamNumber, save_date)

    # Write LaTex 
    f = open(fileName, 'a')
    f.write(material)
    f.close()

    generatePDF(save_date, teamNumber)

def generateLatexBlock(style, businessData, buildData, codingData, wholeData, meeting_date, teamNumber):
    # For a particular meeting_data, generate the corresponding LaTeX page and write to meeting_date.tex
    # There is a lot of list comprehension because each subteam may have multiple entries per date

    # Find the list indices for all the entries corresponding to this date
    aidx = findIndicesForDateAndTeam(businessData, meeting_date, teamNumber)
    bidx = findIndicesForDateAndTeam(buildData, meeting_date, teamNumber)
    cidx = findIndicesForDateAndTeam(codingData, meeting_date, teamNumber)
    widx = findIndicesForDateAndTeam(wholeData, meeting_date, teamNumber)
    
    # Crate a nicely formatted date
    date_pretty = displayDate(meeting_date)
    # Generate the header block with the date
    date = style.formatDate(date_pretty, int(meeting_date.split("/")[0])) 

    ###################################
    # For each of our three headers, write the header (including the dotted line)
    # Then, within each header, if that subteam has entries, generate the color box for each entry
    building = ''
    coding = ''
    business = ''
    whole = '' 
 
    # Check if no entries for the team
    if (len(bidx) + len(cidx) + len(aidx) + len(widx)) == 0:
        return None

    if (len(widx) > 0):
        whole += style.wholeHeader
        whole += " ".join([style.wholeBlock(wholeData[widx[f]], f) for f in xrange(len(widx))]) 
    if (len(bidx) > 0): 
        building += style.buildingHeader
        if len(widx) > 0: 
            building += style.buildingHeaderOffset
        building += "".join([style.buildBlock(buildData[bidx[f]], f) for f in xrange(len(bidx))])
    if (len(cidx) > 0): 
        coding += style.codingHeader
        coding += " ".join([style.codingBlock(codingData[cidx[f]], f) for f in xrange(len(cidx))])
    if (len(aidx) > 0): 
        business += style.businessHeader
        business += " ".join([style.businessBlock(businessData[aidx[f]], f) for f in xrange(len(aidx))])

    # Gather all of the material in order. "material" is a string file that contains the entire LaTeX document
    material = style.header + date + whole + building + coding + business + style.footer
    ###################################

    # Need to reformat date to not use backslashes in the filename
    save_date = meeting_date.replace('/', '_')
    fileName = 'pages/{}/{}.tex'.format(teamNumber, save_date)

    # Write LaTex 
    f = open(fileName, 'w')
    f.write(material)
    f.close()

    generatePDF(save_date, teamNumber)

def generatePDF(fileName, teamNumber):
    if fileName is None: return 

    # Generate PDF
    # Use subprocess instead of os.system so that we can operate in different directory
    p = subprocess.Popen(['pdflatex', '{}.tex'.format(fileName)], cwd='pages/{}'.format(teamNumber))
    p.wait()

    # Command to convert to pngs: pdftoppm 9_26_2020.pdf 9_26_2020 -png
    p = subprocess.Popen(['pdftoppm', '{}.pdf'.format(fileName), fileName, '-png'], cwd='pages/{}'.format(teamNumber))

if __name__ == '__main__':
    # Read in the data
    aData, bData, cData, wData = readCSV()
    # Create the master date list
    dateList = computeDateList(aData, bData, cData, wData)

    specStrips = styleStrips.StripsFormat()
    specBlock = styleBlock.BlockFormat()

    # For each date, create the file
    for i in xrange(len(dateList)):
        print('DATE {}'.format(dateList[i]))
        # Generate LaTeX file. Then PDF, then PNG
        generateLatexBlock(specBlock, aData, bData, cData, wData, dateList[i], 20409) #13620)
        generateLatexStrips(specStrips, aData, bData, cData, wData, dateList[i], 13620) #20409)

