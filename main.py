# -*- coding: utf-8 -*-

import csv
import sys

# Mapping
CODIGO = 0
MONTH = 1
AMOUNT_BUY = 2
AMOUNT_SELL = 3
PRICE_BUY = 4
PRICE_SELL = 5
QUANTITY = 1
TOTAL_VALUE = 2

# Structures
stocks = dict()
profits = dict()

def read_csv(file_name):
    file = open(file_name)
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    file.close()

    return rows

def calculate_monthly_taxes(stocks_stock_previus, stocks_current_year):
    # Assemble stock with the information from the previous year
    for i in stocks_stock_previus:
        # print(i)
        code = i[CODIGO]
        quantity = int(i[QUANTITY])
        total = float(i[TOTAL_VALUE].replace("R$", ""))
        stocks[code] = {
            "average_cost": round(total / quantity, 2),
            "stock": quantity
        }
    
    # Calculate profits per month
    current_month = 1
    monthly_profit = 0
    for i in stocks_current_year:
        row_month = int(i[MONTH])
        code = i[CODIGO].replace("F", "")
        if row_month != current_month: # changed month in the spreadsheet
            profits[str(current_month)] = monthly_profit # save the profit for the processed month
            monthly_profit = 0 # set the profit aggregator to zero for the next month
            current_month = row_month # update month cursor
            if code in stocks:
                # SELL: Avg cost doesn't change, but stock does and there's profit to be calculated
                stocks[code]["stock"] -= int(i[AMOUNT_SELL])
                ## calculate profit
                sell_profit = int(i[AMOUNT_SELL]) * (float(i[PRICE_SELL].replace("R$", "")) - stocks[code]["average_cost"]) # average_cost before update
                monthly_profit += sell_profit
                print("Month: %s | Stock: %s | Profit: %d" % (i[MONTH], code, sell_profit))
                # BUY
                stocks[code]["average_cost"] = (stocks[code]["stock"] * stocks[code]["average_cost"] + int(i[AMOUNT_BUY]) * float(i[PRICE_BUY].replace("R$", ""))) / (stocks[code]["stock"] + int(i[AMOUNT_BUY]))
                stocks[code]["stock"] += int(i[AMOUNT_BUY])

            else: # new stock
                # BUY
                stocks[code] = {
                    "average_cost": round(float(i[PRICE_BUY].replace("R$", "")), 2),
                    "stock": int(i[AMOUNT_BUY]) - int(i[AMOUNT_SELL]) # day trade
                }
                # SELL # PROFIT (because it only can have a sale for new stock if there was a buy in the same day)
                monthly_profit += int(i[AMOUNT_SELL]) * (float(i[PRICE_SELL].replace("R$", "")) - float(i[PRICE_BUY].replace("R$", "")))
        else:
            if code in stocks:
                # SELL: Avg cost doesn't change, but stock does and there's profit to be calculated
                stocks[code]["stock"] -= int(i[AMOUNT_SELL])
                ## calculate profit
                sell_profit = int(i[AMOUNT_SELL]) * (float(i[PRICE_SELL].replace("R$", "")) - stocks[code]["average_cost"]) # average_cost before update
                monthly_profit += sell_profit
                print("Month: %s | Stock: %s | Profit: %d" % (i[MONTH], code, sell_profit))
                # BUY
                stocks[code]["average_cost"] = (stocks[code]["stock"] * stocks[code]["average_cost"] + int(i[AMOUNT_BUY]) * float(i[PRICE_BUY].replace("R$", ""))) / (stocks[code]["stock"] + int(i[AMOUNT_BUY]))
                stocks[code]["stock"] += int(i[AMOUNT_BUY])

            else: # new stock (shouldn't have a sell, unless it's a day trade)               
                # BUY
                stocks[code] = { 
                    "average_cost": round(float(i[PRICE_BUY].replace("R$", "")), 2),
                    "stock": int(i[AMOUNT_BUY]) - int(i[AMOUNT_SELL]) # day trade
                }
                # SELL # PROFIT (because it only can have a sale for new stock if there was a buy in the same day)
                monthly_profit += int(i[AMOUNT_SELL]) * (float(i[PRICE_SELL].replace("R$", "")) - float(i[PRICE_BUY].replace("R$", "")))
        

def main(args):
    try:
        stocks_stock_previus = read_csv(args[1])
        stocks_current_year = read_csv(args[2])

        calculate_monthly_taxes(stocks_stock_previus, stocks_current_year)
    except Exception as e:
        print(e)

if __name__ == '__main__':

    main(sys.argv)