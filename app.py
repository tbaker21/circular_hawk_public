

import yfinance as yf
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from stockstats import StockDataFrame as Sdf
from bs4 import BeautifulSoup
import requests 
import anthropic



# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("Add Google Sheet Json File", scope)  # Use the path where your JSON file is located
client = gspread.authorize(creds)
sheet = client.open("Name of Your Google Sheet").sheet1  # The name of your Google Sheet

# List of stock tickers
stocks = ['AAPL','MSFT','AMZN','GOOGL','META','TSLA','NVDA','JPM','NFLX','SNOW']  # Add your 10 stocks here
tickers = ['AAPL','MSFT','AMZN','GOOGL','META','TSLA','NVDA','JPM','NFLX','SNOW'] #duplicative to ensure AI Analyzer Works

#Define Times 
today = datetime.datetime.now().date()
thirty_days_ago = today - datetime.timedelta(days=30)
start_of_year = datetime.date(today.year, 1, 1)

# Function to calculate percentage change
def calculate_percentage_change(current, previous):
    if current == previous or previous == 0:
        return 0
    return ((current - previous) / previous) * 100

# Function to calculate dollar change
def calculate_dollar_change(current, previous):
    return current - previous


def get_stock_data(ticker, years):
    end_date = datetime.now().date()
    start_date = end_date - datetime.timedelta(days=years*365)

    stock = yf.Ticker(ticker)

    # Retrieve historical price data
    hist_data = stock.history(start=start_date, end=end_date)

    # Retrieve balance sheet
    balance_sheet = stock.balance_sheet

    # Retrieve financial statements
    financials = stock.financials

    # Retrieve news articles
    news = stock.news

    return hist_data, balance_sheet, financials, news


def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d', interval='1m')
    return data['Close'].iloc[-1]

#=====AI CODE BEGINGS======
api_key = "Add Anthropic API Key"
client = anthropic.Client(api_key=api_key)


def clean_text(text):
    # Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text(separator=" ")
    
    # Remove leading and trailing whitespace
    cleaned_text = cleaned_text.strip()
    
    # ... (additional cleaning steps)
    
    return cleaned_text


def research_articles(ticker):
    stock = yf.Ticker(ticker)

    # Retrieve news articles
    news_articles = stock.news

    # Retrieve balance sheet
    balance_sheet = stock.balance_sheet

    # Retrieve financial statements
    financials = stock.financials

    # Combine news articles into a single string
    news_text = ""
    for article in news_articles:
        news_text += f"Title: {article['title']}\n"
        if 'summary' in article:
            news_text += f"Summary: {article['summary']}\n"
        news_text += "\n"

    return news_text, balance_sheet, financials

def financial_analyst(ticker, news_text, balance_sheet, financials):
    system_prompt = f"You are a financial analyst. Analyze the given data for {ticker} and provide insights into why the stock might be down based on the news, balance sheet, and financial statements."

    messages = [
        {"role": "user", "content": f"News articles:\n{news_text.strip()}\n\nBalance Sheet:\n{balance_sheet.to_string()}\n\nFinancial Statements:\n{financials.to_string()}\n\n----\n\nNow, provide a summary and analysis of why the stock might be down based on the given data. Include any relevant insights from the news articles, balance sheet, and financial statements."},
    ]

    headers = {
        "x-api-key": "Anthropic API KEY",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": 'claude-3-haiku-20240307',
        "max_tokens": 2000,
        "temperature": 0.2,
        "system": system_prompt,
        "messages": messages,
    }
    response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
    response_text = response.json()['content'][0]['text']

    return response_text



#======AI CODE ENDS=========

# Get closing prices for the required dates
#closing_price_start_of_year = ytd_data['Close'].iloc[0]
#closing_price_most_recent = ytd_data['Close'].iloc[-1]
##sixty_day_data = stock.history(start=sixty_days_ago, end=today)
#thirty_day_data = stock.history(start=thirty_days_ago, end=today)
#two_day_data = stock.history(start=two_days_ago, end=today)
    

def update_google_sheet(datetime, ticker, starting_price, current_price, drop_percent, drop_type, most_recent_rsi,analysis):
    sheet.append_row([str(datetime.now()), ticker, starting_price, current_price,drop_percent, drop_type, most_recent_rsi,analysis])


def check_stock_30_drops():
    for ticker in stocks:
        stock_data = yf.Ticker(ticker)
        thirty_day_data = stock_data.history(start=thirty_days_ago, end=today)

        if not thirty_day_data.empty:
            starting_price = thirty_day_data['Close'].iloc[0]
            current_price = thirty_day_data['Close'].iloc[-1]
            drop_percent = calculate_percentage_change(current_price, starting_price)

            if  drop_percent < -10:
                # Download historical data for a stock
                data = yf.download(ticker, start="2023-01-01", end="2024-12-31")

                # Convert to StockDataFrame
                stock_data = Sdf.retype(data)

                # Calculate RSI
                stock_data.get('rsi_14') # 14-period RSI

                # Display the last 10 values of RSI
                rsi_setup = stock_data['rsi_14'].tail(1)
                rsi_value = rsi_setup.iloc[0]
                most_recent_rsi = str(rsi_value)
                
                #AI
                news_text, balance_sheet, financials = research_articles(ticker)
                analysis = financial_analyst(ticker, news_text, balance_sheet, financials)

                print(f"{ticker},{analysis}")
                update_google_sheet(datetime.datetime.now(),ticker, starting_price, current_price, drop_percent, "30 day",most_recent_rsi,analysis)

def check_ytd_drops():
    for ticker in stocks: 
        stock_data = yf.Ticker(ticker)
        ytd_data = stock_data.history(start=start_of_year, end=today)
        

        if not ytd_data.empty:
            starting_price = ytd_data['Close'].iloc[0]
            current_price = ytd_data['Close'].iloc[-1] 
            drop_percent = calculate_percentage_change(current_price, starting_price)
            #ytd_dollar_change = calculate_dollar_change(closing_price_most_recent, closing_price_start_of_year)   

            if  drop_percent < -10:
                # Download historical data for a stock
                data = yf.download(ticker, start="2023-01-01", end="2024-12-31")

                # Convert to StockDataFrame
                stock_data = Sdf.retype(data)

                # Calculate RSI
                stock_data.get('rsi_14') # 14-period RSI

                # Display the last 10 values of RSI
                rsi_setup = stock_data['rsi_14'].tail(1)
                rsi_value = rsi_setup.iloc[0]
                most_recent_rsi = str(rsi_value).strip("'")

                 #AI
                news_text, balance_sheet, financials = research_articles(ticker)
                analysis = financial_analyst(ticker, news_text, balance_sheet, financials)

                print(f"{ticker},{analysis}")

                
                update_google_sheet(datetime.datetime.now(),ticker,starting_price, current_price,drop_percent,"YTD", most_recent_rsi, analysis)


check_stock_30_drops()
check_ytd_drops()

