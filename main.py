import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')

st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定してください
""")

st.sidebar.write("""
## 表示日数選択
""")

days=st.sidebar.slider('日数',1,50,20)

st.write(f"""
## 過去**{days}日間**のGAFAの株価
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
    
        tkr = yf.Ticker(tickers[company]) 
            
        hist = tkr.history(period=f'{days}d')

        hist = hist[['Close']]
        hist.columns = [company]
        
        hist = hist.T
        hist.index.name = "Name"
        df = pd.concat([df, hist])
        
    return df

try:
  st.sidebar.write("""
  ## 株価の範囲指定
  """)

  ymin, ymax = st.sidebar.slider(
    '範囲を指定してください',
    0.0,3500.0,(0.0,3500.0) 
  )

  tickers = {
      'Apple':'AAPL',
      'facebook': 'FB',
      'Netflix':'NFLX',
      'Google':'GOOGL',
      'Microsoft':'MSFT',
      'Amazon':'AMZN'
  }

  df = get_data(days, tickers)

  companys = st.multiselect(
    '会社名を選択してください。',
    list(df.index),
    ['Google','Amazon','facebook','Apple']
  )

  if not companys:
    st.error('少なくとも一社は選択してください。')
  else:
    data = df.loc[companys]
    st.write("### 株価(USD)",data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=['Date']).rename(columns={'value':'Stock Prices(USD)'})


  chart = (
      alt.Chart(data)
      .mark_line(opacity=0.8, clip=True) # clipで画面外を消す
      .encode(
          x="Date:T",
          y=alt.Y("Stock Prices(USD):Q",stack=None,scale=alt.Scale(domain=[ymin,ymax])),
          color='Name:N'
      )
  )
  st.altair_chart(chart, use_container_width=True)
except:
  st.error(
    "おっと、何かエラーが起きているようです。"
  )