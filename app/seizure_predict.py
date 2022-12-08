import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import pandas as pd
import numpy as np

st.set_page_config(page_title="Seizure Predict", layout='centered', page_icon= "🧠")

st.markdown('# Welcome to Seizure Prediction App:brain:')
plt.style.use('bmh')

CSS = """
h1 {
    color: black;
    font-size: 210%;
    text-align: center;
}
.center{
    text-align: center;
}
.red {
    color: red;
    font-size: 130%;
    text-align: center;
}
.blue {
    color: blue;
    font-size: 130%;
    text-align: center;
}
"""


st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)


def get_file():
    url = "https://seizure-predict-qkiben4ega-ew.a.run.app/upload_file/"
    url2 = "https://seizure-predict-qkiben4ega-ew.a.run.app/predict/"
    file = st.file_uploader("Upload an eeg file:")

    df = None
    y_pred = None

    if file is not None:
        files = {"file" : file}
        response = requests.post(url=url, files = files).json()

        params = {
            "path" : response["file"]
        }

        response2 = requests.get(url=url2, params=params).json()

        df = pd.DataFrame(response2["signal"])
        y_pred = pd.DataFrame(response2["result"])

    return df, y_pred

def show_plot(df, y_pred):
    window = 256*10
    # window = 100
    # df = np.linspace(0, 500, 400)
    # y_pred = pd.DataFrame({"test": [1,0,0,1]})
    if "df_final" not in st.session_state:
        final_y = []
        for j in range(len(y_pred)):
            y = int(y_pred.iloc[j])
            for i in range(window):
                final_y.append(y)
        st.session_state.df_final = pd.DataFrame()
        st.session_state.df_final['signals'] = df
        st.session_state.df_final['results'] = final_y
        st.session_state.df_final['pos_signals'] = st.session_state.df_final.apply(lambda x: x['signals'] if x['results'] == 1 else np.NaN,axis=1)


    for i in range(0,len(st.session_state.df_final),20):
        ax.set_xlim(i-256, i+50)
        y_df_final = st.session_state.df_final[['signals', 'pos_signals']].iloc[:i]
        ax.plot(y_df_final['signals'], color='b', label= "no-seizure")
        ax.plot(y_df_final['pos_signals'], color='r', label = "seizure")
        placeholder.pyplot(fig)
        time.sleep(0.00001)



fig, ax = plt.subplots()
plt.ylim(-400,400)
plt.ylabel("Voltage [µV]")
plt.xlabel("Time")

plt.xticks([])
red_patch = mpatches.Patch(color='red', label='Seizure')
blue_patch = mpatches.Patch(color='blue', label='No seizure')
plt.legend(handles=[red_patch, blue_patch], loc='upper right')

placeholder = st.pyplot(fig)


# st.markdown("<div class='center'><span class='red'>seizure</span><span class='blue'> no seizure</span></div>", unsafe_allow_html=True)
# st.markdown("<div class='blue'> no seizure </div>", unsafe_allow_html=True)

df, y_pred = get_file()
    
if df is not None:
    show_plot(df, y_pred)
