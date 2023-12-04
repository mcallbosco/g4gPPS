import os
import json
import requests
from time import sleep
import random

outputFolder = "F:\\G4GCollection\\FileOutput\\"
problemID = 0



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
    #https://practiceapi.geeksforgeeks.org/api/latest/problems/submissions/32ab0f67be7594527bf260a7167c07b5/
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
            if submission['exec_status_text'] == "Correct":
                with open(outputFolder + str(problemID) + "\\" + user + "\\" + str(counter) + "_correct.txt", "w") as f:
                    f.write(getCode(submission['submission_id']))
            else:
                with open(outputFolder + str(problemID) + "\\" + user + "\\" + str(counter) + "_incorrect.txt", "w") as f:
                    f.write(getCode(submission['submission_id']))
            counter += 1
            
        



def main():
    data = concotinateJSONs("F:\\G4GCollection\\701227")
    data = onlyLanguage(data, "python3")
    data = seperateByUsers(data)
    for user in data:
        if len(data[user]) > 1:
            print (str(len(data[user])) + " " + user)
    print (len(data))
    data = makeSureAtleast1IncorrectForEachUser(data)
    sortUserSubmissionsDate(data)
    print (len(data))
    dataOutput(data)

    #print(data)

main()
