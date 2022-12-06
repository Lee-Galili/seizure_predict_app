import streamlit as st
import requests
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np

st.set_page_config(page_title="Seizure Predict", layout='centered')
st.markdown('# Welcome to Seizure Prediction App')


def get_file():
    url = "http://127.0.0.1:8000/upload_file/"
    url2 = "http://127.0.0.1:8000/predict/"
    file = st.file_uploader("upload an eeg file")

    if file is not None:
        files = {"file" : file}
        response = requests.post(url=url, files = files).json()
        st.markdown(response)

        params = {
            "path" : response["file"]
        }

        response2 = requests.get(url=url2, params=params).json()
        # st.markdown(response2)

        # st.write(np.array(response2["signal"]))

        df = pd.DataFrame(response2["signal"])

        # st.write(df)
        return df

def show_plot(df):
    for i in range(len(df)):
        #buff=df.iloc[i]
        plt.xlim(i-256, i+50)
        df_2 = df.iloc[:i]
        # x_df2 = df_2["Time"]
        y_df2 = df_2
        ax.plot(y_df2, color="r")
        placeholder.pyplot(fig)
        time.sleep(0.001)


fig, ax = plt.subplots()
plt.xlim(0, 300)
plt.ylim(-100,200)
placeholder = st.pyplot(fig)

df = get_file()
if df is not None:
    show_plot(df)
