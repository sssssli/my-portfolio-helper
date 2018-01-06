#from yahoo_finance import Share
import urllib
import re
import pandas as pd
import numpy as np
import sys
import datetime

def main(input_file):
    # read input file
    input_data = read_file(input_file)

    # gets updated ticker price
    price_list, time_pulled = get_price_list(input_data)

    # calculates currency adjusted market values
    market_val, market_val_cad, market_val_usd = market_value_cal(input_data, price_list)

    # generates output csv
    gen_output(input_file, input_data, price_list, time_pulled, market_val,
                market_val_cad, market_val_usd)

def read_file(input_file):
    """
    Reads input file as CSV.
    Args:
        input_file (string)
    """
    # 0 means there's a header
    input_data = pd.read_csv(input_file, header=0)
    return input_data

def get_quote(symbol):
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('id="ref_(.*?)">(.*?)<', content)
    if m:
        quote = m.group(2)
    else:
        quote = 'no quote available for: ' + symbol
    return quote

def get_price_list(input_data):
    """
    Gets tickers and price from input data (excludes CASH/GIC).

    Args:
        input_data (pandas dataframe)

    Returns:
        price_list, price of all tickers (pandas series)
        time_pulled, time pulled for all tickers (pandas series)

    """
    tickers = input_data['ticker'].tolist()
    price_list = []
    time_pulled = []
    exclude = ['CASH', 'GIC']

    for ticker in tickers:
        if not any(ticker in item for item in exclude):
            print ticker
	    stock = Share(ticker)
            price_list.append(float(stock.get_price()))
            time_pulled.append(stock.get_trade_datetime()[:10])
    price_list = pd.Series(price_list)
    time_pulled = pd.Series(time_pulled)
    return price_list, time_pulled


def market_value_cal(input_data, price_list):
    """
    Calculates the market value of all stocks, includes CAD/USD adjustments.

    Args:
        input_data (pandas dataframe)
        price_list, this is the updated ticker price (pandas series)

    Returns:
        market_value (pandas series)
        market_value_cad (pandas series)
        market_value_usd (pandas series)

    """

    # this makes one pandas series of market value, regardless of currency
    market_val_top = (input_data['shares']*price_list).dropna()
    market_val_bottom = input_data['tot_market_value'].dropna()
    market_val = market_val_top.append(market_val_bottom, ignore_index=True)

    # generate a temporary dataframe with market values
    curr_market_val = pd.concat([input_data['currency'], market_val], axis=1)
    curr_market_val.columns = ['currency', 'tot_market_value']

    # currency adjustments
    # gets ratio first, also pulled from latest available data
    cadusd_loc = int(np.where(input_data['ticker'] == 'CADUSD=X')[0])
    cadusd = price_list[cadusd_loc]
    market_val_cad = np.where(curr_market_val['currency'] == 'CAD',
                        curr_market_val['tot_market_value'],
                        curr_market_val['tot_market_value']*(1/cadusd))
    market_val_usd = np.where(curr_market_val['currency'] == 'USD',
                        curr_market_val['tot_market_value'],
                        curr_market_val['tot_market_value']*cadusd)
    market_val_cad = pd.Series(market_val_cad)
    market_val_usd = pd.Series(market_val_usd)
    return market_val, market_val_cad, market_val_usd


def gen_output(input_file, input_data, price_list, time_pulled, market_val,
                market_val_cad, market_val_usd):
    """
    Generates the output CSV.

    Args:
        input_file (string)
        input_data (dataframe)
        price_list (pandas series)
        time_pulled (pandas series)
        market_val (pandas series)
        market_val_cad (pandas series)
        market_val_usd (pandas series)

    """
    output = pd.concat([time_pulled, input_data['ticker'], price_list,
                        input_data['shares'], input_data['currency'],
                        market_val.round(2), market_val_cad.round(2),
                        market_val_usd.round(2), input_data['account']], axis=1)
    output.columns = ['time_pulled', 'ticker', 'current_price',
                    'shares', 'currency', 'tot_market_value',
                    'tot_market_adj_cad', 'tot_market_adj_usd', 'account']
    # totals
    summary = pd.Series(['TOTAL'], index=['time_pulled'])
    summary = summary.append(output.sum(numeric_only=True)).drop(labels=['shares','current_price'])
    output = output.append(summary, ignore_index=True)

    # output file
    now = datetime.datetime.now()
    input_file = input_file.split('.')[0]
    output.to_csv (input_file + '-' + now.strftime("%Y-%m-%d") + '.csv', index=False)

if __name__ == "__main__":
    """
    Call by using: python current_value.py input_file_name
    Example: python input.csv output.csv
    """
    input_file = sys.argv[1]
    main(input_file)
