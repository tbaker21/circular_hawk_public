# circular_hawk_public

- This is a script that will check any stocks you have in the stock list to see if they are down by a certain percentage in the laast 30 days and YTD. 
- If they are down,the script will run a calculation of how much they are down and then leverage the Anthropic API to summarize and provide insight as to why the stock is down.
- Then the script will update a google sheet of your choosing to track these changes in prices and analysis. 
- You will need to add your own google sheet link, the json file location to access the google sheet, and your Anthropic API key. 
- This is just a fun script to learn how to leverage yfinance, beatifulsoup4, and anthropic api key. This is not financial advice nor should anything from the scrip be traded on. 
