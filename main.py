import requests
import os
import json
import Costants

if __name__ == '__main__':
    print("Enter the repository name:")
    repositoryName = input()
    url = 'https://api.github.com/user/repos'
    data = '{"name":"' + repositoryName + '"}'
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": "token " + Costants.GITHUB_KEY}
    response = requests.get(url, headers=headers)
    for repo in json.loads(response.text):
        if (repositoryName == repo['name']):
            print("A repo with the name " + repositoryName + " already exist.")

    response = requests.post(url, data=data, headers=headers)
    print("Repository created successfully!")
    if response.ok:
        print("The name of the project and the name of the repository are the same? (y/n)")
        samename = input()
        if(samename.lower() == "y"):
            projectName = repositoryName
        if (samename.lower() == "n"):
            print("Enter the local project name:")
            projectName = input()
        print("Enter the path where the project will be created locally (the last '/' and the project name will be automatically added)")
        print("Example: 'C:/Development' -> 'C:/Development/projectName")
        path = input()
        path += '/' + projectName

        try:
            print(os.getcwd())
            if os.path.exists(path):
                print("Path already exists! Do you still want to proceed? (write y/n)")
                print("N.B. All the content in the selected folder will be uploaded to the repo")
                uploadRepo = input()
                if(uploadRepo.lower() == "n"):
                    exit(1)
            else:
                os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)
            os.chdir(path)
            os.system('git init')
            os.system('type nul > .gitignore')
            os.system('type nul > README.md')
            os.system('git add .')
            os.system('git commit -m "First Commit"')
            os.system('git remote add origin https://github.com/'+Costants.GITHUB_USERNAME+'/' + repositoryName + '.git')
            os.system('git branch -M main')
            os.system('git push -u origin main')
            print("")
            print("-----------------------")
            print("")
            print("All done!! Have fun")
    else:
        print("Error creating the new repo")
