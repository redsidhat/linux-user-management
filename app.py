
from flask import Flask, render_template, request, url_for
import os
import crypt
from jinja2 import Template



class UserData():
    def __init__(self, userName, fullName, homeDir, shellType, userPassword):
        # you can put here some validation logic
        self.userName = userName
        self.fullName = fullName
        self.HomeDir = HomeDir
        self.shellType = shellType
        self.userSudo = userSudo
        self.userPassword = userPassword


app = Flask(__name__)


def createUser(userdata):

    encPass = crypt.crypt(userdata.userPassword,"22")   
    if userdata.userSudo == "True":
        return  os.system("useradd -p "+encPass+ " -s "+ userdata.shellType + " -d "+ userdata.homeDir + " -m " + " -c \"" + userdata.fullName + "\" " + userdata.userName + "&& usermod -aG sudo "+ userdata.userName )
    return  os.system("useradd -p "+encPass+ " -s "+ userdata.shellType + " -d "+ userdata.homeDir + " -m " + " -c \"" + userdata.fullName + "\" " + userdata.userName )

def listUser():
    user_list = os.popen('awk -F: \'$2 != "*" && $2 !~ /^!/ { print $1}\' /etc/shadow').read()
    return user_list.split()


def deleteUser(user):

    return os.system("userdel -r -f " + user)


def getUserdata(username):
    UserData.userName = os.popen("cat /etc/passwd | grep %s |awk -F : '{print $1}'" %username).read().strip()
    if UserData.userName:
        UserData.fullName = os.popen("cat /etc/passwd | grep %s |awk -F : '{print $5}'" %username).read().strip()
        UserData.homeDir = os.popen("cat /etc/passwd | grep %s |awk -F : '{print $6}'" %username).read().strip()
        UserData.shellType = os.popen("cat /etc/passwd | grep %s |awk -F : '{print $7}'" %username).read().strip()
        if os.popen("sudo -l -U %s | grep ALL" %UserData.userName).read().strip():
            UserData.userSudo = True
        else:
            UserData.userSudo = False
        return UserData
    else:
        return False


def updateUserdata(userdata):
    status = 0
    print old_user_name
    print old_user_sudo
    status += os.system("usermod -c \"%s\" %s" %(userdata.fullName, old_user_name)) #updating full name
    status += os.system("usermod -d %s %s" %(userdata.homeDir, old_user_name)) #updating home dir
    status += os.system("usermod -s %s %s" %(userdata.shellType, old_user_name)) #updating shell
    #updating sudo
    if userdata.userSudo == "True" and old_user_sudo == "False":
        status += os.system("usermod -aG sudo %s" %old_user_name)
    elif userdata.userSudo == "False" and old_user_sudo == "True":
        status += os.system("deluser %s sudo" %old_user_name)
    #updating username
    status += os.system("usermod -l %s %s" %(userdata.userName, old_user_name))
    if status == 0:
        return True
    return status

@app.route('/')
def form():
    return render_template('form_submit.html')


@app.route('/manage/', methods=['POST'])
def manage_user():
    manage_action = request.form['manageAction']
    if manage_action == 'add':
        return render_template('form_add.html')
    else:
        return render_template('form_list.html', users = listUser(), title = manage_action)


@app.route('/adduser/', methods=['POST'])
def add_user():
    UserData.userName = request.form['userName']
    UserData.fullName = request.form['fullName']
    UserData.homeDir = request.form['homeDir']
    UserData.shellType = request.form['shellType']
    UserData.userPassword = request.form['userPassword']
    UserData.userSudo = request.form['userSudo']
    status = createUser(UserData)
    if status == 0:
        return "User created Successfully"
    else:
        return "Error creating user"
    #return "Username: %s <br> FullName: %s <br> HomeDir: %s <br> Password: %s" %(user_name,full_name,home_dir,user_password)


@app.route('/modifyuser/', methods=['POST'])
def modify_user():

    user_data = getUserdata(request.form['userName'])
    global old_user_name 
    old_user_name = user_data.userName
    global old_user_sudo
    old_user_sudo = user_data.userSudo
    if user_data:
        return render_template('form_modify.html',userdata = user_data)
    else:
        return 'This user does not exist.'

@app.route('/updateuser/', methods=['POST'])
def update_user():

    UserData.userName = request.form['userName']
    UserData.fullName = request.form['fullName']
    UserData.homeDir = request.form['homeDir']
    UserData.shellType = request.form['shellType']
    UserData.userPassword = request.form['userPassword']
    UserData.userSudo = request.form['userSudo']
    if updateUserdata(UserData):
        return "User detailes updates successfully"
    return "User details updation failed"

@app.route('/removeuser/', methods=['POST'])
def remove_user():
    user_name = request.form['userName']
    status = deleteUser(user_name)
    if status == 0:
        return "User removed successfully"
    else:
        return "Error removing user"
    

if __name__ == '__main__':
  app.run()
