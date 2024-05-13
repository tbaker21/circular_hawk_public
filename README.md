# Stock Analysis and Alerts

This script tracks specified stock tickers and provides alerts when the stocks experience significant drops. It also uses Claude.AI to provide a summary analysis of why the stock might be down and potential future prospects based on financial data and news articles.

## Features

- Tracks specified stock tickers.
- Alerts when stocks drop by more than 10% over the last 30 days or year-to-date.
- Uses yfinance to retrieve stock data.
- Uses Google Sheets to store and track stock data and analysis.
- Uses Claude.AI to analyze why a stock might be down and its potential future.

## Prerequisites

- Python 3.7 or higher
- Required Python libraries (listed in `requirements.txt`)
- Google Sheets API credentials (JSON file)
- Anthropic API key for Claude.AI

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up Google Sheets API credentials:**

    - Obtain the JSON file with your Google Sheets API credentials.
    - Save the JSON file in the project directory.
    - Update the line `creds = ServiceAccountCredentials.from_json_keyfile_name("Add Google Sheet Json File", scope)` with the name of your JSON file.

5. **Set up Anthropic API credentials:**

    - Obtain your Anthropic API key.
    - Update the line `api_key = "Add Anthropic API Key"` with your API key.

## Usage

1. **Specify the stock tickers to track:**

    - Update the `stocks` and `tickers` lists with the stock tickers you want to track.

    ```python
    stocks = ['AAPL','MSFT','AMZN','GOOGL','META','TSLA','NVDA','JPM','NFLX','SNOW']
    tickers = ['AAPL','MSFT','AMZN','GOOGL','META','TSLA','NVDA','JPM','NFLX','SNOW']
    ```

2. **Run the script:**

    ```sh
    python your_script.py
    ```

3. **The script will:**

    - Check the stock prices for the last 30 days and year-to-date.
    - Alert if any stock drops by more than 10%.
    - Analyze and provide a summary using Claude.AI.
    - Update the Google Sheet with the analysis.

## File Structure

- `your_script.py`: The main script file.
- `requirements.txt`: Lists the dependencies required for the project.
- `credentials.json`: Your Google Sheets API credentials (not included in the repository).

## Example

Here's an example of how to use the script:

1. **Add your Google Sheets API credentials and Anthropic API key.**
2. **Specify the stock tickers you want to track.**
3. **Run the script to receive alerts and analysis when the stocks drop.**

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [yfinance](https://pypi.org/project/yfinance/)
- [gspread](https://github.com/burnash/gspread)
- [Stockstats](https://pypi.org/project/stockstats/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Anthropic](https://www.anthropic.com/)
- [Google Sheets API](https://developers.google.com/sheets/api)
