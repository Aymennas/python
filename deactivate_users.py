from tracemalloc import stop
import gitlab
import requests
import os
import datetime

# gitlab connexion
s = requests.session()
s.verify = os.getenv('USERPROFILE')+'\ca-bundle.crt'
gittoken = os.environ['GITLAB_TOKEN']
gl = gitlab.Gitlab(url='https://gitlab.ca.cib/', private_token=gittoken, session=s)
gl.auth()

deactivate = os.environ['DEACTIVATE_USERS']
user_desact_number=0
if(deactivate == 'true'):
  print('REAL MODE, USERS WITH NO ACTIVITY FOR 90 DAYS WILL BE DEACTIVATED')
else:
  print('DRY RUN MODE, USERS WILL NOT BE DEACTIVATED')

#function to get all active users with paging
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
  
#function for checking of last activity date less then 90 day

def check_Date(last_activity_date):
    date_limit = datetime.date.today() - datetime.timedelta(days=90)
   
    b1 = datetime.datetime.strptime(last_activity_date, '%Y-%m-%d')
#    b2 = datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
    return b1.date() <= date_limit


# function deactivating a given user
def deactivate_users(user, file):
    print('the user to deactivate :', user.username, 'the last activity :', user.last_activity_on, 'the last sign in :', user.last_sign_in_at)
    global user_desact_number

    try:
      # test the variable deactivate for the dry run 
      if(deactivate == 'true'):
        user.deactivate()
        line= ('user : '+user.username +', last activity: '+ str(user.last_activity_on) +  ', last sign in : ' + user.last_sign_in_at)
        file.write(line)
        file.write('\n')
        user_desact_number+= 1
        print('deactivation of user :', user.username)
    except:
      print('impossible to deactivate the user ', user.username, ' name:', user.name)
      pass 


#list all users from Gitlab (BEFORE CLEANUP)
users = get_all_users()

#prepare the file containing the list of inactive users with date of creation.
time_now=datetime.datetime.now()
file_name= 'users_list_' + str(time_now.strftime("%Y-%m-%d_%H-%M-%S")) + '.txt'   
file = open('./'+ file_name, "w")
file_tmp = open('./tmp.txt', "w")
tmp= os.path.realpath(str(file_name))
tmp = tmp.replace("\\", "/")
file_tmp.write(tmp)

#start  
user_desact_number=0
for x in users:
  #set last_activity_on
  last_activity = str(x.last_activity_on)
  created_at = str(x.created_at)
  user_name=str(x.username)
  #Deactivate the user if no activity since last 90 days
 
  if ("None" not in last_activity and check_Date(last_activity)) and user_name.lower().startswith('ut'): 
     # print('the user :', x.username, 'has no activity :', last_activity)

      deactivate_users(x, file)
      
if user_desact_number==0:
  file.write("------ there is no user to deactivate -----")


file.close()
print('------ users deactivated : ', user_desact_number ,' -------')

#list all users from Gitlab (AFTER CLEANUP)
users = get_all_users()
