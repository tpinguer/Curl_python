import re 


regex = r"^http" 

test = ["http://acervo.oglobo.globo.com/", "anuncie/"]

for (index, string) in enumerate(test):
    match = re.findall(regex, string)
        
    lenght = len(match) 

    if lenght == 0:
        print(index)
        test[index] = 'https://oglobo.globo.com/' + string

print(test)
# for matchNum, match in enumerate(match):
#     matchNum = matchNum + 1

#     print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(),
# end = match.end(), match = match.group()))

#     for groupNum in range(0, len(match.groups())):
#         groupNum = groupNum + 1

#         print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum),
# end = match.end(groupNum), group = match.group(groupNum)))
