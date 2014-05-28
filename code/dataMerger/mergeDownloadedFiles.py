def verifySameColumnNames(rawDataFilePaths):
    # make header a global variable in order to use later in mergeDatasetsPerTeam()
    global header

    # store headers (column names) of all text files into a list
    headers = []
    for rawDataFilePath in rawDataFilePaths:
        rawDataFile = open(rawDataFilePath, 'r')
        header = rawDataFile.readline().strip()
        headers.append(header)
        rawDataFile.close()

    # check all the header values in the list are the same
    return all(x == headers[0] for x in headers)



def groupFilePathsByTeamID(rawDataFilePaths, teamIDs):
    # dictionary of lists (each comprised of file paths for a single team), with teamIDs used as keys
    groupedFilePaths = {}
    for teamID in teamIDs:
        for rawDataFilePath in list(rawDataFilePaths):  # iterate over a copy of rawDataFilePaths list (because we will be removing elements from the original rawDataFilePaths list)
            if teamID in rawDataFilePath: 
                if teamID in groupedFilePaths:  # if groupedFilePaths dictionary has an existing key and a list, append to the list; then remove the file path 
                    groupedFilePaths[teamID].append(rawDataFilePath)
                    rawDataFilePaths.remove(rawDataFilePath) 
                else:  # if groupedFilePaths diction does not have an existing key and a list, create a new key and a list with the team ID
                    groupedFilePaths[teamID] = [rawDataFilePath]
                    rawDataFilePaths.remove(rawDataFilePath)
    return(groupedFilePaths)
    


def mergeDatasetsPerTeam(groupedFilePaths):
    for teamID in groupedFilePaths:
        teamRawDataFilePaths = groupedFilePaths[teamID]
        mergedOutputFilePath = '../../data/processed/' + teamID + '.txt'

        with open(mergedOutputFilePath, 'w') as outputFile:  # open a writable output file (that consists of merged multiple data files)
            outputFile.write(header + ',GameType' + '\n')  # write a header for the output file
            for rawDataFilePath in teamRawDataFilePaths:  # for each data file
                numFileLines = sum(1 for line in open(rawDataFilePath))  # count the number of lines of the file
                if numFileLines > 1:  # only if a dataset file contains game log info (other than the header), then open the file to merge into a larger file
                    isPlayoffsDataset = 'Playoffs' in rawDataFilePath  # determine the game type (regular season or playoff)
                    with open(rawDataFilePath) as inputFile:
                        next(inputFile)  # skip the first line (header information; redundant information)
                        for line in inputFile:
                            line = line.strip()  # remove the new line character at the end of each line
                            if isPlayoffsDataset:
                                outputFile.write(line + ',Playoff\n')
                            else:
                                outputFile.write(line + ',Reg\n')



def main():
    rawDataFilePaths = glob.glob(os.path.join('../../data/raw/', '*'))  # file paths of all raw data text files
    teamIDs = helper.getTeamIDs()
    
    sameColumnNames = verifySameColumnNames(rawDataFilePaths)  # verify that all raw data files share the same column names (important for merging datasets)
    if sameColumnNames == False:
        print('Not all text files have the same column names!')
    else:
        groupedFilePaths = groupFilePathsByTeamID(rawDataFilePaths, teamIDs)
        mergeDatasetsPerTeam(groupedFilePaths)



if __name__ == '__main__':
    # import modules
    import glob
    import os

    # import Howard's helper module
    import sys
    sys.path.insert(0, '../helper')
    import helper

    main()

