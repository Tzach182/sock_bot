# eBay Sock Bot

This bot is a web crawler built using Selenium with Python to search for socks on eBay. It automates the process of searching for socks, collecting data on each search result, and saving the data to a CSV file. The repository also includes a data handling file that converts the currency to USD and fixes some columns in the data.

## Getting Started

To get started with this bot, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/tzach182/sock_bot.git

2. Install the required Python packages: Selenium, Pandas, Numpy
3. Download the ChromeDriver for your version of Chrome and place it in the directory
   
## Bot Overview
The bot works by using Selenium to automate the process of searching for socks on eBay. It performs the following steps:

Opens the eBay website.
Searches for "socks" in the search bar.
Iterates over the search results, extracting data such as name, price, and description for each sock.
Saves the extracted data to a CSV file (socks_database.csv).

## Data Handling
The repository includes a file named data_handling.py that provides functions for converting the 
currency to USD and fixing some columns in the data. You can use these functions to clean up and 
process the data after it has been collected by the bot.
