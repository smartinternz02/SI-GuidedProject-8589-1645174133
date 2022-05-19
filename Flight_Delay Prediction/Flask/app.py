#Importing Libraries

from flask import Flask,render_template,request

import pickle
import numpy as np

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "35jnX8LPiSw8ysLmGDh5Evb2_A646U_rjQH2rIPg9kkh"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line




#model = pickle.load(open('flight.pkl','rb'))

app = Flask(__name__)



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/prediction',methods =['GET','POST'])
def predict():
    name = request.form['name']
    month = request.form['month']
    dayofmonth = request.form['dayofmonth']
    dayofweek = request.form['dayofweek']
    origin = request.form['origin']
    if(origin == "msp"):
        origin1,origin2,origin3,origin4,orgin5 = 0,0,0,0,1
    if(origin == "dtw"):
        origin1,origin2,origin3,origin4,orgin5 = 1,0,0,0,0
    if(origin == "jfk"):
         origin1,origin2,origin3,origin4,orgin5 = 0,0,1,0,0
    if(origin == "sea"):
         origin1,origin2,origin3,origin4,orgin5 = 0,1,0,0,0  
    if(origin == "alt"):
         origin1,origin2,origin3,origin4,orgin5 = 0,0,0,1,0
         
    destination = request.form['destination']
    if(destination == "msp"):
        destination1,destination2,destination3,destination4,destination5 = 0,0,0,0,1
    if(destination == "dtw"):
        destination1,destination2,destination3,destination4,destination5 = 1,0,0,0,0
    if(destination == "jfk"):
         destination1,destination2,destination3,destination4,destination5 = 0,0,1,0,0
    if(destination == "sea"):
         destination1,destination2,destination3,destination4,destination5 = 0,1,0,0,0  
    if(destination == "alt"):
         destination1,destination2,destination3,destination4,destination5 = 0,0,0,1,0
    dept = request.form['dept']    
    arrtime = request.form['arrtime']
    actdept = request.form['actdept']
    dept15=int(dept)-int(actdept)
    total = [[name,month,dayofmonth,dayofweek,origin1,origin2,origin3,origin4,orgin5,destination1,destination2,destination3,destination4,destination5,int(arrtime),int(dept15)]]
    #print(total)
 
    payload_scoring = {"input_data": [{"field": ['name','month','dayofmonth','dayofweek','origin1','origin2','origin3','origin4','orgin5','destination1','destination2','destination3','destination4','destination5','arrtime','dept15'], "values":total }]}
    response_scoring =  requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/445aa1d5-d1cb-4f9a-9e0d-9720be5445d5/predictions?version=2022-03-30', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions =response_scoring.json()
    
    print(predictions)
    
    print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])
    y_pred = predictions['predictions'][0]['values'][0][0]
    #y_pred = model.predict(total)
    print(y_pred)
    
    if(y_pred==[0.]):
        ans="The Flight will be on time"
    else:
        ans="The Flight will be delayed"
    return render_template("index.html",showcase = ans)
    
if __name__ == '__main__':
    app.run(debug = False)
