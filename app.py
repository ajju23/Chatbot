import warnings
warnings.filterwarnings("ignore")
from flask import Flask, render_template, url_for, request
from main import bot_response

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/get")
def chat_response():
    userTxt = request.args.get('chatInput')
    response = bot_response(userTxt)
    return response

if __name__=="__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=8080)