# my-portfolio-helper

This is inspired by my own needs of needing to know exactly where I stand in my portfolio at any moment, at the tip of my finger. I've noticed some nuances with services offered by brokers. Such as, certain accounts being left out of the net worth calculation, net worth only showing in one currency, etc. In other words, snap shots of portfolios are lacking in accuracy.

Keep an eye out for more, as I'll be adding additional functionalities based on my own needs.

# How to use:
Currently only supporting CAD/USD conversions.

1. Clone this repo.
2. Follow the [input_example.csv](https://github.com/sssssli/my-portfolio-helper/blob/master/input_example.csv) to prepare your input CSV file. Note that all ticker notations are following Yahoo Finance's notations, including currency adjustments. Save this file in the same folder.
3. Run the following command to update all of your tickers and generate a total summary with the following command:
`python current_value.py input_example.csv`

Check out [input_example-2017-01-10.csv](https://github.com/sssssli/my-portfolio-helper/blob/master/input_example-2017-01-10.csv) as the output CSV file that you should see. 
