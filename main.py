# -*- coding: utf-8 -*-

import csv
import json
import sys
import math

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
profits = {
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0,
    "8": 0,
    "9": 0,
    "10": 0,
    "11": 0,
    "12": 0
}

def get_month(index):
    map_months = {
        "1": "Jan",
        "2": "Fev",
        "3": "Mar",
        "4": "Abr",
        "5": "Mai",
        "6": "Jun",
        "7": "Jul",
        "8": "Ago",
        "9": "Set",
        "10": "Out",
        "11": "Nov",
        "12": "Dez"
    }

    return map_months[str(index)]

def read_csv(file_name):
    file = open(file_name)
    csvreader = csv.reader(file)
    next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)
    file.close()

    return rows

def create_profits_summary_file(profits):
    profits_file = open("output/profits_summary.csv", "w")
    profits_file.write("Mes,Lucro\n")
    for key, value in profits.items():
        profits_file.write("%s,R$%.2f\n" % (get_month(key), round(value, 2)))
    profits_file.close()

def calculate_monthly_taxes(stocks_stock_previus, stocks_current_year):
    profits_per_stock_file = open("output/profits_month.csv", "w")
    profits_per_stock_file.write("Mes,Codigo,Lucro\n")
    # Assemble stock with the information from the previous year
    for i in stocks_stock_previus:
        code = i[CODIGO]
        code = i[CODIGO][0:5]
        if (code[-1] == "1"): # code ending in 11
            code += "1"
        quantity = int(i[QUANTITY])
        total = float(i[TOTAL_VALUE].replace("R$", ""))
        stocks[code] = {
            "average_cost": round(total / quantity, 2),
            "stock": quantity
        }

    # Calculate profits per month
    for i in stocks_current_year:
        row_month = int(i[MONTH])
        code = i[CODIGO][0:5]
        if (code[-1] == "1"): # code ending in 11
            code += "1"

        if code in stocks:
            # SELL: Avg cost doesn't change, but stock does and there's profit to be calculated
            
            in_stock = stocks[code]["stock"] 
            
            amount_buy = int(i[AMOUNT_BUY])
            ## calculate profit
            amount_sell = int(i[AMOUNT_SELL])
            price_buy = float(i[PRICE_BUY].replace("R$", ""))
            price_sell = float(i[PRICE_SELL].replace("R$", ""))

            # BUY
            try:
                stocks[code]["average_cost"] = round((in_stock * stocks[code]["average_cost"] + amount_buy * price_buy) / (in_stock + amount_buy), 2)
                stocks[code]["stock"] += amount_buy
            except:
                print(in_stock, amount_buy, code)

            # SELL
            if (amount_sell != 0):
                sell_profit = round(amount_sell * (price_sell - stocks[code]["average_cost"]), 2) # average_cost before update
                profits[str(row_month)] += round(sell_profit, 2)
                if (stocks[code]["stock"] < amount_sell):
                    print("ERROR: %s has a negative stock" % code)
                else:
                    stocks[code]["stock"] -= amount_sell # update stock
    
                profits_per_stock_file.write("%s,%s,%.2f\n" % (get_month(i[MONTH]), code, sell_profit))

        else: # new stock
            # BUY
            
            price_buy = round(float(i[PRICE_BUY].replace("R$", "")), 2)
            amount_sell = int(i[AMOUNT_SELL])
            amount_buy = int(i[AMOUNT_BUY])
            price_sell = float(i[PRICE_SELL].replace("R$", ""))

            if (amount_sell > amount_buy): # stock was wrong
                print("ERROR: %s had a bigger sell than what was bought plus the current stock" % code)
            stocks[code] = {
                "average_cost": price_buy,
                "stock":  amount_buy - amount_sell # day trade
            }
            # SELL # PROFIT (because it only can have a sale for new stock if there was a buy in the same day)
            sell_profit = amount_sell * (price_sell - price_buy)
            profits[str(row_month)] += round(sell_profit, 2)
            stocks[code]["stock"] = amount_buy - amount_sell # update stock with the new one
            if (sell_profit != 0):
                profits_per_stock_file.write("%s,%s,%.2f\n" % (get_month(i[MONTH]), code, sell_profit))

    profits_per_stock_file.close()
    create_profits_summary_file(profits)
    print("Files successfully created in the output/ folder")
        

def main(args):
    try:
        stocks_stock_previus = read_csv(args[1])
        stocks_current_year = read_csv(args[2])

        calculate_monthly_taxes(stocks_stock_previus, stocks_current_year)
    except Exception as e:
        print(e)

if __name__ == '__main__':

    main(sys.argv)