from flask import Flask, jsonify, request
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
# from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app)

@app.post('/predict')
def predict():
    dt_input = request.json.get('dt_input')
    targ_date = datetime.strptime(dt_input, '%Y-%m-%dT%H:%M')
    targ_str = targ_date.strftime("%Y-%m-%d %H:%M:%S")
    start_of_wk = targ_date - timedelta(days=targ_date.weekday(), hours=targ_date.hour)
    end_of_wk = start_of_wk + timedelta(days=6, hours=23)
    model_date = datetime.strptime('2021-12-31 23:00', '%Y-%m-%d %H:%M')
    diff = end_of_wk - model_date
    k = int(diff.seconds/(60*60) + diff.days*24)

    fmod_tbats_e = pickle.load(open('src/fmod_tbats_e.pkl', 'rb'))
    fmod_tbats_w = pickle.load(open('src/fmod_tbats_w.pkl', 'rb'))
    dr = pd.date_range(start='2022-01-01 00:00:00', periods=k, freq='H').strftime("%Y-%m-%d %H:%M:%S").tolist()[-168:]
    yhat_jan_e, yhat_jan_e_conf = fmod_tbats_e.forecast(steps=k, confidence_level=0.95)
    yhat_jan_w, yhat_jan_w_conf = fmod_tbats_w.forecast(steps=k, confidence_level=0.95)
    y_e = (yhat_jan_e**2).tolist()[-168:]
    y_w = (yhat_jan_w**2).tolist()[-168:]
    targ_pred_e = y_e[dr.index(targ_str)]
    targ_pred_w = y_w[dr.index(targ_str)]

    return jsonify(
        x = dr, 
        y_e = y_e, 
        y_w = y_w, 
        targ = targ_str, 
        pred_e = targ_pred_e, 
        pred_w = targ_pred_w
        )


if __name__ == '__main__':
    app.run(debug=False)

