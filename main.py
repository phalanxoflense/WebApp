import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.title("Streamlit 超入門")

st.write("Display Image")

img = Image.open("img/untitled2.jpg")
st.image(img, caption="flower", use_column_width=True)



st.write("DataFrame")
df = pd.DataFrame(
  np.random.rand(100,2)/[50,50] + [35.69, 139.70],
  columns=["lat","lon"]
)
st.line_chart(df) #線グラフ
st.area_chart(df) #エリアグラフ
st.bar_chart(df) #棒グラフ
st.dataframe(df.style.highlight_max(axis=0)) #ハイライト
st.map(df) #地図を表示

