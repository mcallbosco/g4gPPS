import os
import json
import requests
from time import sleep
import random
import cookie

folderPath = "put scraper output folder here"
outputFolder = "put final output folder here"
problemID = 0

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

cookie = {
}

def get_files_in_folder(folder_path):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    return files

def concotinateJSONs(folder_path):
    global problemID
    #data['message']['submissions']['LastEvaluatedKey']['Items']
    files = get_files_in_folder(folder_path)
    if len(files) == 1:
        return None
    data = []
    firstRun = True
    for file in files:
        with open(file, "r") as f:
            tempData = json.load(f)
            data.append(tempData['message']['submissions']['Items'])
            if (firstRun):
                problemID = tempData['message']['id']
                firstRun = False

    #reverse order
    return data

def onlyLanguage(data, language):
    new_data = []
    for file in data:
        for submission in file:
            if submission['lang'] == language:
                new_data.append(submission)
    return new_data

def seperateByUsers(data):
    users = {}
    for submission in data:
        if submission['handle'] not in users:
            users[submission['handle']] = []
        users[submission['handle']].append(submission)
    return users

def makeSureAtleast1IncorrectForEachUser(data):
    newData = {}
    for user in data:
        correct = False
        incorrect = False
        for submission in data[user]:
            if submission['exec_status_text'] == "Correct":
                correct = True
            else :
                incorrect = True
        if correct and incorrect:
            newData[user] = data[user]   
    return newData

def getCode(submissionID):
    #random sleep between 1 and 2 seconds 
    sleep(random.uniform(1, 2))
    urlPre = "https://practiceapi.geeksforgeeks.org/api/latest/problems/submissions/"

    cookies = cookie
    r = requests.get(urlPre + submissionID + "/", cookies=cookies)
    data = r.json()
    return data['user_code']

def sortUserSubmissionsDate(data):
    for user in data:
        data[user].sort(key=lambda x: x['subtime'])
    return data


def dataOutput (data):
    #make a folder for this problem, and then a folder for each user
    #then make a file for each submission
    #files will be numbered, and the file name will indicate if it is correct or not

    #make folder
    import os
    try:
        os.mkdir(outputFolder + str(problemID))
    except:
        pass
    for user in data:
        try:
            os.mkdir(outputFolder + str(problemID) + "\\" + user)
        except:
            pass
        
        counter = 0
        for submission in data[user]:
            try:
                if submission['exec_status_text'] == "Correct":
                    with open(outputFolder + str(problemID) + "\\" + user + "\\" + str(counter) + "_correct.txt", "w") as f:
                        f.write(getCode(submission['submission_id']))
                else:
                    with open(outputFolder + str(problemID) + "\\" + user + "\\" + str(counter) + "_incorrect.txt", "w") as f:
                        f.write(getCode(submission['submission_id']))
            except:
                pass
            counter += 1
            
        
def cookieToDict(cookieSTR):
    #get cookie from cookieStr
    cookie = cookieSTR.split("; ")
    cookieDict = {}
    for c in cookie:
        c = c.split("=")
        cookieDict[c[0]] = c[1]
    return cookieDict

def processFolder(folderPath, cookie):
    data = concotinateJSONs(folderPath)
    if data == None:
        return
    data = onlyLanguage(data, "python3")
    data = seperateByUsers(data)
    data = makeSureAtleast1IncorrectForEachUser(data)
    sortUserSubmissionsDate(data)
    dataOutput(data)
    



def main():
    global cookie
    cookieStr = cookie.cookieSTR
    cookie = cookieToDict(cookieStr)
    #check how many folders are in the folder
    folders = []
    for root, dirs, filenames in os.walk(folderPath):
        for dir in dirs:
            folders.append(os.path.join(root, dir))
    print (folders)
    #make a list of exsisting folders at the top level in the output folder
    outputFolders = []
    for root, dirs, filenames in os.walk(outputFolder):
        if root == outputFolder:
            for dir in dirs:
                outputFolders.append(os.path.join(root, dir))
    print (outputFolders)
    #skip the folders that already exist
    for folder in outputFolders:
        if folderPath + folder.split("\\")[-1] in folders:
            folders.remove(folderPath + folder.split("\\")[-1])
    print (folders)    
    #process the folders
    for folder in folders:
        printProgressBar(folders.index(folder), len(folders), prefix = 'Progress:', suffix = 'Complete', length = 50)
        processFolder(folder, cookie)

main()
