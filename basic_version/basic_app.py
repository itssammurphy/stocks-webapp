import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objects as go


# START AND END DATES FOR THE TIME SPAN OF DATA
START_DATE = "2012-01-01"
END_DATE = date.today().strftime("%Y-%m-%d")

# SET UP STREAMLIT WEBAPP
st.title("Stock Prediction App")  # TITLE

stocks = ("AAPL", "GOOG", "A2M.AX", "TSLA", "WES.AX")
# USER SELECTS STOCK FROM LIST
selected_stock = st.selectbox("Select Stock to Predict", stocks)

# USER CHOOSES HOW MANY YEARS TO FORECASE THIS STOCK (1-5)
n_years = st.slider("Number of years to forecast", 1, 5)
period = n_years * 365

# LOADING DATA, STREAMLIT CACHE


@st.cache_data
def load_data(ticker: str) -> list:
    data = yf.download(ticker, START_DATE, END_DATE)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text("Loading data...")
selected_stock_data = load_data(selected_stock)
data_load_state.text("Loading data... Done!")

st.subheader("RAW DATA")
st.write(selected_stock_data.tail())


def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Open'],
            name='stock_open_price'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Close'],
            name='stock_close_price'
        )
    )

    fig.layout.update(title_text="Time Series Data", xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    ))
    st.plotly_chart(fig)


plot_raw_data(selected_stock_data)


# FORECASTING THE STOCK PRICE
df_train = selected_stock_data[['Date', 'Close']]
df_train = df_train.rename(columns={
    'Date': 'ds',
    'Close': 'y'
})

model = Prophet()
model.fit(df_train)
future = model.make_future_dataframe(periods=period)
forecast = model.predict(future)

st.subheader("FORECAST DATA")
st.write(forecast.tail())

fig2 = plot_plotly(model, forecast)
st.plotly_chart(fig2)

st.write("Forecast Components")
fig3 = model.plot_components(forecast)
st.write(fig3)
