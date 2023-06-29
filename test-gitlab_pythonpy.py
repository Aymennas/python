from tracemalloc import stop
import gitlab
import requests
import os
import datetime

# gitlab connexion
s = requests.session()
s.verify = os.getenv('USERPROFILE')+'\ca-bundle.crt'
gittoken = 'YB6yMsH2VyzjtoizJk2q'
gl = gitlab.Gitlab(url='https://gitlab.ca.cib/', private_token=gittoken, session= s)
gl.auth()
