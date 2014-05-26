def getSeasonIDs():
    seasonIDs_file = open('seasonIDs.txt', 'r')
    seasonIDs = list()
    for seasonID in seasonIDs_file:
        seasonIDs.append(seasonID.strip())
    seasonIDs_file.close()
    return seasonIDs


def getTeamIDs():
    teamIDs_file = open('teamIDs.txt', 'r')
    teamIDs = list()
    for line in teamIDs_file:
        line = line.strip().split(',')
        teamIDs.append(line[3])
    del teamIDs[0]  # remove the first value (i.e. "TeamID") from the teamIDs list 
    teamIDs_file.close()
    return teamIDs


def createQueryStrings(seasonIDs, teamIDs):
    # example query string: http://stats.nba.com/stats/teamgamelog?Season=2013-14&SeasonType=Regular+Season&TeamID=1610612745
    baseURL = 'http://stats.nba.com/stats/teamgamelog?'
    seasonTypes = ['Regular+Season', 'Playoffs']
    queryStrings = []
    for seasonType in seasonTypes:
        for teamID in teamIDs:
            for seasonID in seasonIDs:
                queryString = baseURL + 'SeasonType=' + seasonType + '&' + 'TeamID=' + teamID + '&' + 'Season=' + seasonID
                queryStrings.append(queryString)
    return queryStrings


def downloadToCSV(queryString):
    # reading JSON data from the NBA site
    response = urllib.request.urlopen(queryString)
    charset = response.info().get_param('charset', 'utf8')
    data = response.read()
    jsonData = json.loads(data.decode(charset))['resultSets'][0]

    # writing CSV data onto local machine
    header = jsonData['headers']
    rows = jsonData['rowSet']  # 'rows' variable initially does not contain header
    rows.insert(0, header)  # header prepended; 'rows' variable contains header

    # use information from query string to name CSV files
    parameters = queryString.split('&')
    csvFileName = parameters[1][7:] + '_' + parameters[2][7:] + '_' + parameters[0][50:].replace('+', '') + '.txt'
    csvFilePath = '../../data/raw/' + csvFileName

    with open(csvFilePath, 'w', newline='') as fp:
        csvWriter = csv.writer(fp, delimiter=',')
        csvWriter.writerows(rows)


def downloadTeamStatsNBA(queryStrings):
    for queryString in queryStrings:
        downloadToCSV(queryString)


def main():
    seasonIDs = getSeasonIDs()  # read and store all season IDs to a list
    teamIDs = getTeamIDs()  # read and store all team IDs to a list
    queryStrings = createQueryStrings(seasonIDs, teamIDs)  # create query strings to NBA API system (which provides JSON data)
    downloadTeamStatsNBA(queryStrings)  # convert JSON data to CSV and download onto local machine


if __name__ == '__main__':

    import urllib.request
    import json
    import csv

    main()
