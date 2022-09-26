text=open('/usr/local/lib/python3.9/site-packages/seleniumwire/thirdparty/mitmproxy/net/tls.py','r').read()
with open('/usr/local/lib/python3.9/site-packages/seleniumwire/thirdparty/mitmproxy/net/tls.py','w') as file:
    file.write(text.replace('SSL.SSLv2_METHOD', '1').replace('SSL.SSLv3_METHOD', '2'))
    file.close()
    
from selenium_liker import Liker_Engine
from flask import Flask, request, jsonify
from urllib.parse import unquote_plus

app = Flask(__name__)
app.config["SECRET_KEY"] = "UWuiNuUEFGeypGkegGDeibi"


@app.route('/', methods=['GET', 'POST'])
def home():
    return """<title>Selenium Auto Liker</title><form method="POST" action="/send"><input name="react" placeholder="React Name"/><input name="post_id" placeholder="Post ID"/><input name="cookie" placeholder="FB Cookie"/><input type="submit"/></form>"""


@app.route('/send', methods=['GET', 'POST'])
def send_reactions():
    if request.method == 'GET':
        react = unquote_plus(request.args.get('react'))
        post_id = unquote_plus(request.args.get('post_id'))
        cookie = unquote_plus(request.args.get('cookie'))
    else:
        react = unquote_plus(request.form.get('react'))
        post_id = unquote_plus(request.form.get('post_id'))
        cookie = unquote_plus(request.form.get('cookie'))

    engine = Liker_Engine(react, post_id, cookie)
    return jsonify(engine)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
