
from flask import Flask, render_template, request, url_for
import os
import crypt


app = Flask(__name__)


def createUser(user,name,home,shell,password,sudo):

    encPass = crypt.crypt(password,"22")   
    return  os.system("useradd -p "+encPass+ " -s "+ shell+ " -d "+ home + " -m " + " -c \"" + name + "\" " + user)

def listUser():
    user_list = os.popen('awk -F: \'$2 != "*" && $2 !~ /^!/ { print $1}\' /etc/shadow').read()
    return user_list


@app.route('/')
def form():
    return render_template('form_submit.html')


@app.route('/manage/', methods=['POST'])
def manage_user():
    manage_action = request.form['manageAction']
    if manage_action == 'add':
        return render_template('form_add.html')
    if manage_action == 'modify':
        return listUser()
    if manage_action == 'remove':
        return listUser()

@app.route('/adduser/', methods=['POST'])
def add_user():
    user_name = request.form['userName']
    full_name = request.form['fullName']
    home_dir = request.form['homeDir']
    shell_type = request.form['shellType']
    user_password = request.form['userPassword']
    user_sudo = request.form['userSudo']
    status = createUser(user_name,full_name,home_dir,shell_type,user_password,user_sudo)
    if status == 0:
        return "User created Successfully"
    else:
        return "Error creating user"
    #return "Username: %s <br> FullName: %s <br> HomeDir: %s <br> Password: %s" %(user_name,full_name,home_dir,user_password)



if __name__ == '__main__':
  app.run()
