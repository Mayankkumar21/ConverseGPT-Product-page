from flask import Flask, redirect, render_template, request, send_file, url_for
from dotenv import load_dotenv, dotenv_values
import os, sys
import redis
app = Flask(__name__)

load_dotenv()
counter=0

REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
REDIS_PORT = os.getenv("PORT")
print(REDIS_URL,REDIS_TOKEN,REDIS_PORT)

def redis_connect():
    try:
        client = redis.Redis(host=REDIS_URL, port=REDIS_PORT, password=REDIS_TOKEN, db=0, socket_timeout=5, ssl=True)
        ping = client.ping()
        if ping:
            print("Connection to Redis is successful")
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")

redis_client = redis_connect()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/handle_api_call')
def handle_api_call():
    category = request.args.get('category')
    
    if category == 'windows':
        return send_file('static/ConverseGPT-win32-x64.rar', as_attachment=True)
    elif category == 'mac':
        return send_file('static/ConverseGPT-darwin-arm64.rar', as_attachment=True)
    elif category == 'linux':
        return send_file('static/ConverseGPT-linux-x64.rar', as_attachment=True)
    else:
        return 'Invalid category', 400

@app.route('/store_email', methods=['POST'])
def store_email():
    global counter
    print("Inside store email")
    if request.method == 'POST':
        email = request.form['email']
        key='email'+str(counter)
        print(key)
        counter+=1
        state = redis_client.setex(key,999999999, email)
        if state:
            print("New email recieved",email)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
