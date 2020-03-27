## ASE-1-Project
# DriveIt

[![Build Status](https://travis-ci.com/ASE-Group-23/ASE-1-Project.svg?branch=master)](https://travis-ci.com/ASE-Group-23/ASE-1-Project)
[![Coverage Status](https://coveralls.io/repos/github/ASE-Group-23/ASE-1-Project/badge.svg?branch=master)](https://coveralls.io/github/ASE-Group-23/ASE-1-Project?branch=master)

## Cloning the project  
* Run command `git clone https://github.com/ASE-Group-23/ASE-1-Project.git` and change into the project folder
* Create a virtual environment `env` in the repository (use virtualenv, etc)
* Install the requirements
* Activate virtual environment

To create virtual environment and install requirements run following commands
```shell script
virtualenv env
pip install -r requirements.txt
```

To activate the environment use following commands:
Window: 
```shell script
.\env\Scripts\activate
```
Ubuntu/Linux
```shell script
source env/bin/activate
```

## Making a new branch
```bash
git checkout -b <branch-name>
```
branch-name : can be your name 

For Pushing Changes
```bash
git push -u origin <branch-name>
```


## Version Control Workflow
> After making any changes, follow these steps before pushing to the repo.
1. git add .
2. git commit -m "commit msg"
3. git pull
4. git push
