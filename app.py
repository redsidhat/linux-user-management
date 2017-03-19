
from flask import Flask, render_template, request, url_for


app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form_submit.html')

@app.route('/manage/', methods=['POST'])
def manage_user():
    manage_action=request.form['manageAction']
    if manage_action == 'add':
        return "adding user"
    #return render_template('form_action.html', name=name, email=email)

# Run the app :)
if __name__ == '__main__':
  app.run()
