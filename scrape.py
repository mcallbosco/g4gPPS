import requests
import json
from time import sleep
import cookie

problemsToCheckAbove = 100
problemsToCheckBelow = 100

problemID = -1
output = "path here"


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


urlPre = "https://practiceapi.geeksforgeeks.org/api/latest/problems/"
urlPost = "/submissions/"
urlPost2 = "?last_submission_key="
urlPost3 = "&last_submission_key_time="


def getSubmissions(problemID, lastSubmissionKey="", lastSubmissionKeyTime=""):
    url = urlPre + str(problemID) + urlPost
    if lastSubmissionKey != "":
        url += urlPost2 + lastSubmissionKey + urlPost3 + lastSubmissionKeyTime
    
    cookies = cookie
    r = requests.get(url, cookies=cookies)
    data = r.json()
    return data

cookieStr = cookie.cookieSTR
cookie = {}
def cookieToDict(cookie):
    #get cookie from cookieStr
    cookie = cookieStr.split("; ")
    cookieDict = {}
    for c in cookie:
        c = c.split("=")
        cookieDict[c[0]] = c[1]
    return cookieDict

def getProblem(problemID, depth = 0):
    data = getSubmissions(problemID)
    #example error json file {"error": {"code": 403, "message": "You do not have access to this problem"}}
    #check for error json, return if found
    if 'error' in data:
        return data
    #save
    #make folders
    import os
    try:
        os.mkdir(output + str(problemID))
    except:
        pass
    with open(output + str(problemID) + "\\" + str(0) + ".json", "w") as f:
        json.dump(data, f)

    for i in range(0,depth):
        sleep(2)
        try:
            data = getSubmissions(problemID, data['message']['submissions']['LastEvaluatedKey']['submission_id'], data['message']['submissions']['LastEvaluatedKey']['subtime'].replace(" ", "%20"))
            with open(output + str(problemID) + "\\" + str(i+1) + ".json", "w") as f:
                json.dump(data, f)
        except:
            break



def main():
    global cookie
    cookie = cookieToDict(cookieStr)
    for i in range(problemID - problemsToCheckAbove, problemID + problemsToCheckBelow):
        getProblem(i,15)
        printProgressBar(i - (problemID - problemsToCheckAbove), problemsToCheckAbove + problemsToCheckBelow, prefix = 'Progress:', suffix = 'Complete', length = 50)



    

main()

