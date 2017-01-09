from yahoo_finance import Share
import pandas as pd
import numpy as np
import sys


def main(input_file):
    # read input file
    input_data = read_file(input_file)
    # gets updated ticker price
    price_list, time_pulled = get_price_list(input_data)
    # calculates currency adjusted market values


def read_file(input_file):
    """Reads input file as CSV."""
    # 0 means there's a header
    input_data = pd.read_csv('input.csv', header=0)
    return input_data


def get_price_list(input_data):
    """
    Gets tickers and price from input data (excludes CASH/GIC).

    Args:
        input_data (pandas dataframe)

    Returns:
        price_list, price of all tickers (list)
        time_pulled, time pulled for all tickers (list)

    """
    tickers = input_data['ticker'].tolist()
    price_list = []
    time_pulled = []
    exclude = ['CASH', 'GIC']

    for ticker in tickers:
        if not any(ticker in item for item in exclude):
            stock = Share(ticker)
            price_list.append(float(stock.get_price()))
            time_pulled.append(stock.get_trade_datetime()[:10])
    return price_list, time_pulled


def market_value_cal(input_data):
    """
    Calculates the market value of all stocks, includes CAD/USD adjustments.

    Args:
        input_data (pandas dataframe)

    Returns:
        market_value
        market_value_cad (numpy array)
        market_value_usd (numpy array)
    """

    #this makes one pandas series of market value, regardless of currency
    market_value_top = (input_data['shares']*a).dropna()
    market_value_bottom = input_data['tot_market_value'].dropna()
    market_value = market_value_top.append(market_value_bottom, ignore_index=True)
    #generate a temporary dataframe with market values
    market_value_currency = pd.concat([input_data['currency', market_value]])

    #currency adjustments
    #gets ratio first, also pulled from latest available data
    cadusd = input_data.loc[input_data['ticker'] == 'CADUSD=X', 'current_price'].values[0]
    market_value_cad = np.where(output['currency'] == 'CAD',
                    output['tot_market_value'], output['tot_market_value']*cadusd)
    market_value_usd = np.where(output['currency'] == 'USD',
                    output['tot_market_value'], output['tot_market_value']*cadusd)



def gen_output(output_data):


if __name__ == "__main__":
    """
    Call by using: python current_value.py input_file_name
    Example: python input.csv output.csv
    """
    input_file = sys.argv[1]
    main(input_file)
