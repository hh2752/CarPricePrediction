# import requirements needed
from flask import Flask,request, render_template
from utils import get_base_url
import pickle
import numpy as np

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

model = pickle.load(open('model.pkl','rb'))

    



# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('index.html')


@app.route(f"{base_url}", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return(flask.render_template('index.html', prediction_text = ""))
    
    if request.method == 'POST':
        
        inp_features = [float(x) for x in request.form.values()]
        
        print(inp_features)
        
        input_variables = np.append(inp_features,1)
        
        input_variables = input_variables.reshape(1,-1)
       
        prediction = model.predict(input_variables)[0]
        
        return render_template('index.html',
                                     prediction_text=prediction,
                                     )
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'https://cocalc7.ai-camp.dev/'
    
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
