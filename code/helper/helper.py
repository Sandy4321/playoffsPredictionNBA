# returns a list of team IDs
def getTeamIDs():
    teamIDs_file = open('../teamSeasonIDs/teamIDs.txt', 'r')
    teamIDs = list()
    for line in teamIDs_file:
        line = line.strip().split(',')
        teamIDs.append(line[3])
    del teamIDs[0]  # remove the first value (i.e. "TeamID") from the teamIDs list                                                                                         
    teamIDs_file.close()
    return teamIDs



# returns a list of season IDs (e.g. 1997-98)
def getSeasonIDs():
    seasonIDs_file = open('../teamSeasonIDs/seasonIDs.txt', 'r')
    seasonIDs = list()
    for seasonID in seasonIDs_file:
        seasonIDs.append(seasonID.strip())
    seasonIDs_file.close()
    return seasonIDs
