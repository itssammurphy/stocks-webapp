# Simple Stocks Web Application

This is a simple webapp developed in Python with Streamlit that predicts stock prices of a few stocks that the user selects from.

## Dependencies

`streamlit` - [PyPI](https://pypi.org/project/streamlit/)

`prophet` - [PyPI](https://pypi.org/project/prophet/)

`yfinance` - [PyPI](https://pypi.org/project/yfinance/)

`plotly` - [PyPI](https://pypi.org/project/plotly/)

## Basic Version

The basic version of the app is contained in `/basic_version`, and it uses the Prophet forecasting procedure released by the Meta Core Data Science team.

### Running the application

Once you have installed all the required dependencies, you can run the basic version of the application by either:

```
cd basic_version
streamlit run basic_app.py
```

OR

```
streamlit run ./basic_version/basic_app.py
```
