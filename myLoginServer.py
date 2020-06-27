from flask import Flask
from flask import request
import time

SLEEP_TIME=0.00008
app = Flask(__name__)
app.url_map.strict_slashes = False
@app.route('/')
def hello():
   return "Hello World!"
@app.route('/index')
def blah():
    return 'blah blah'

@app.route('/index/<inP>',methods=['GET','POST'])
def index(inP):
    secretPassword='HASODSHELI'
  
    if len(inP)!=len(secretPassword):
        print (len(inP),len(secretPassword))
        return "0"
    result ="1"
    paddedInPassword=inP.rjust(32,' ')
    paddedSecretPassword=secretPassword.rjust(32,' ')
    print ("curr Psf: ",paddedSecretPassword)
    print(paddedSecretPassword,paddedInPassword)
    inx=0
    for i in paddedSecretPassword:
        print(paddedSecretPassword, paddedInPassword)
        if i !=paddedInPassword[inx]:
            time.sleep(SLEEP_TIME)
            result="0"
        inx+=1
    return result

if(__name__== '__main__'):
    app.run(debug=True)
    #app.run(debug=True, ssl_context='adhoc')