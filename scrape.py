import requests
import json
from time import sleep

problemsToCheckAbove = 100
problemsToCheckBelow = 100
#additional info pages example https://practiceapi.geeksforgeeks.org/api/latest/problems/701236/submissions/?last_submission_key=65f9c921c91ed40100c782c54b53d76f&last_submission_key_time=2023-12-03%2018:40:19

problemID = 701227


urlPre = "https://practiceapi.geeksforgeeks.org/api/latest/problems/"
urlPost = "/submissions/"
urlPost2 = "?last_submission_key="
urlPost3 = "&last_submission_key_time="

output = "F:\\G4GCollection\\"

def getSubmissions(problemID, lastSubmissionKey="", lastSubmissionKeyTime=""):
    url = urlPre + str(problemID) + urlPost
    if lastSubmissionKey != "":
        url += urlPost2 + lastSubmissionKey + urlPost3 + lastSubmissionKeyTime
    
    cookies = cookie
    r = requests.get(url, cookies=cookies)
    data = r.json()
    return data



def getProblem(problemID, depth = 0):
    data = getSubmissions(problemID)
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
        data = getSubmissions(problemID, data['message']['submissions']['LastEvaluatedKey']['submission_id'], data['message']['submissions']['LastEvaluatedKey']['subtime'].replace(" ", "%20"))
        with open(output + str(problemID) + "\\" + str(i+1) + ".json", "w") as f:
            json.dump(data, f)



def main():
    data = getProblem(problemID, 10)
    """{'status': True, 'message': {'id': 701227, 'problem_name': 'Two Repeated Elements', 'problem_type': 1, 'problem_type_text': 'Function', 'slug': 'two-repeated-elements-1587115621', 'problem_level': 1, 'problem_level_text': 'Medium', 'submissions': {'Items':"""
    """{'status': True, 'message': {'id': 701227, 'problem_name': 'Two Repeated Elements', 'problem_type': 1, 'problem_type_text': 'Function', 'slug': 'two-repeated-elements-1587115621', 'problem_level': 1, 'problem_level_text': 'Medium', 'submissions': {'LastEvaluatedKey':"""



    

main()

