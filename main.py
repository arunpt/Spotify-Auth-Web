from flask import Flask, render_template, request
from base64 import urlsafe_b64encode
import requests

app = Flask(__name__)


class Temp:
    client_id = None
    client_secret = None
    redirect_uri = None
    
temp_data = Temp()

@app.route('/')
def index():
    return render_template('index.html',default=request.url_root + 'redirect/' )

@app.route('/process', methods=['POST'])
def process():
    result = request.form.to_dict(flat=False)
    final = { i: result[i][0] if len(result[i]) <= 1 else result[i] for i in result } # https://stackoverflow.com/a/46784359
    temp_data.client_id = final["client_id"]
    temp_data.client_secret = final["client_secert"]
    temp_data.redirect_uri = final['redirect_uri']
    scopes = ','.join(result['scopes'])
    api_url = f"https://accounts.spotify.com/authorize?client_id={temp_data.client_id}&response_type=code&scope={scopes}&redirect_uri={temp_data.redirect_uri}"
    return api_url

@app.route('/redirect/')
def callback():
    auth_token = urlsafe_b64encode(f"{temp_data.client_id}:{temp_data.client_secret}".encode()).decode() 
    headers = {"Content-Type" : 'application/x-www-form-urlencoded', "Authorization" : f"Basic {auth_token}"}
    body = dict(
        grant_type = 'authorization_code',
        redirect_uri = temp_data.redirect_uri,
        code = request.args.get('code')
    )
    post = requests.post('https://accounts.spotify.com/api/token', params=body, headers=headers) 
    return render_template('redirect.html',code=post.json())
    

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
