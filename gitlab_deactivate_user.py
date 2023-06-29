from tracemalloc import stop
import gitlab
import requests
import os
import datetime

# gitlab connexion
s = requests.session()
s.verify = os.getenv('USERPROFILE')+'\ca-bundle.crt' 
gittoken = 'zSb4ysjJdh_S8P4Xe_TC'
gl = gitlab.Gitlab(url='https://gitlab.ca.cib/', private_token=gittoken, session=s)
gl.auth()

def get_all_users():
  next_page = True
  all_users= []
  i = 1
  while next_page == True:
    users = gl.users.list(active='true', page=i)
    all_users.extend(users) 
    i += 1
    if users == []:
      next_page = False
  print ("------ active users reported : ",len(all_users))  
  return all_users
  

