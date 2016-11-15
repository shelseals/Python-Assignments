
# coding: utf-8

# In[1]:

#installing pandas libraries
#!pip install pandas-datareader
#!pip install --upgrade html5lib==1.0b8


# In[2]:

# Shelby Jennings, ssj2124
# 4572 HW: Simulation

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

unit_cost = 2 #What Jack and Jill pay a Shenzen based company for each t-shirt
unit_price = 5 #The selling price of each t-shirt
unit_storage_cost = 0.10  #The daily cost of storing one t-shirt overnight in inventory
shipping_days_mean = 5 #The average number of days it takes a shipment to arrive from Shenzen
shipping_days_std = 2.2 #The standard deviation of shipping days. Assume normal distribution
sales_mean = 1000 #The average number of shirts sold on a given day
sales_std = 523 #The standard deviation of daily sales. Assume normal distribution
inventory = 5001 #The starting inventory
reorder_level = 5000 #The level at or below which Jack and Jill will place an order. 
order_qty = 5000 #The amount of an order. Note that when ordering, they will look at the inventory level plus 
#the amount ordered but not yet delivered

#generates a 30 day profit array for Jack and Jill
def run_one():
    
    shipping_dict = {}
    inventory_dict = {}
    profit_dict = {}
    profit_list = [[]]
    current_inventory = inventory 

    for i in range(1,31):
        sales_on_day = int(abs(np.random.normal(sales_mean, sales_std))) #Only selling positive shirts, whole shirts
        shipping_days_from_now = int(abs(np.random.normal(shipping_days_mean, shipping_days_std)))
        inventory_dict[i] = current_inventory - sales_on_day #Inventory on given day recorded as stored shirts
                                                            #less sold shirts

        if inventory_dict[i] <= reorder_level:
            shipping_dict[i] = shipping_days_from_now #Assigning number of shirts to arrive given time to reorder
            for key in shipping_dict:
                for key_2 in inventory_dict:
                    if key + shipping_dict[key] == key_2: #If day in shipping dict equals order day + shipping days
                        inventory_dict[key_2] += order_qty #add the reorder level to inventory on this day 
        
        for key in shipping_dict:
            for key_2 in inventory_dict:
                if key + shipping_dict[key] == key_2: #If there was order scheduled to arrive on this day, profits...
                    profit_dict[i] = ((unit_price * sales_on_day) - (unit_cost * sales_on_day) 
                    - (unit_cost * order_qty) - (unit_storage_cost * int(inventory_dict[i]))) 
                else: #If order was not scheduled to arrive on this day, profits...doesn't include costs of reorder
                    profit_dict[i] = ((unit_price * sales_on_day) - (unit_cost * sales_on_day) 
                    - (unit_storage_cost * int(inventory_dict[i]))) 
        
        
    for key in profit_dict:
        profit_list[0].append(profit_dict[key])
    
    aprofits = np.array(profit_list,float)
        
    return aprofits 

#test = run_one() #To test this method 
#print(test)


# In[3]:

#generate a 1000 X 30 dataframe that contains the 30 day profit arrays from 1000 simulation runs
def simulate_profit(runs):
    runs = 1000
    datalist = []
    for i in range(1,runs + 1):
        simulation = run_one()
        row = simulation[0].tolist()
        datalist.append(row)

    adatalist = np.array(datalist)

    df = pd.DataFrame(adatalist,index=range(1,runs + 1),columns=range(1,31))
    return df

profits = simulate_profit(1000)
#profits



# In[17]:

#generate a 1000 X 30 dataframe that contains cumulative profits for each run
def simulate_cumu_profit(runs):
    datalist = []
    for i in range(1,runs + 1):
        simulation = run_one()
        row = simulation[0].tolist()
        datalist.append(row)

    adatalist = np.array(datalist)

    df2 = pd.DataFrame(adatalist,index=range(1,runs + 1),columns=range(1,31))
    df2.cumsum(axis=1)
    return df2

cumu_profits = simulate_cumu_profit(1000)
#cumu_profits


# In[ ]:

#the mean and the standard deviation of the average daily profit from all runs
def get_mean_stdev_avg_daily_profit():
    mean_dict = {}
    mean_list = []
    column_num = 1
    #Computing average daily profit over 1000 runs for each day, then finding mean of averages
    while column_num < 31:
        for column in profits:
            mean_dict[column_num] = profits[column].mean()
            column_num += 1
    for key in mean_dict:
        mean_list.append(mean_dict[key])
    overall_mean = sum(mean_list)/len(mean_list)
    
    #Computing standard devation with all reported means in mean_list 
    diff = [elt - overall_mean for elt in mean_list]
    sqd_diff = [elt ** 2 for elt in diff]
    stdev = (sum(sqd_diff)/len(diff)) ** 1/2
    return "overall mean followed by standard deviation:", overall_mean, stdev
    
#the mean and the standard deviation of the cumulative 30 day profit across all runs
def get_mean_stdev_cumu_daily_profit():
    cumu_mean_dict = {}
    cumu_mean_list = []
    column_num = 1
    #Computing average daily profit over 1000 runs for each day, then finding mean of averages
    while column_num < 31:
        for column in cumu_profits:
            cumu_mean_dict[column_num] = cumu_profits[column].mean()
            column_num += 1
    for key in cumu_mean_dict:
        cumu_mean_list.append(cumu_mean_dict[key])
    cumu_overall_mean = sum(cumu_mean_list)/len(cumu_mean_list)
    
    #Computing standard devation with all reported means in mean_list 
    diff = [elt - cumu_overall_mean for elt in cumu_mean_list]
    sqd_diff = [elt ** 2 for elt in diff]
    cumu_stdev = (sum(sqd_diff)/len(diff)) ** 1/2
    return "overall cumulative mean followed by standard deviation:", cumu_overall_mean, cumu_stdev

#the mean and the standard deviation of the lowest profit (greatest loss) from each run
def get_mean_stdev_lowest_profits():
    all_mins = profits.min(axis=1)
    mean_of_mins = sum(all_mins)/len(all_mins)
    
    diff = [elt - mean_of_mins for elt in all_mins]
    sqd_diff = [elt ** 2 for elt in diff]
    min_stdev = (sum(sqd_diff)/len(diff)) ** 1/2
    return "mean of minimum profits followed by standard deviation:", mean_of_mins, min_stdev

#the mean and the standard deviation of the highest profit from each run
def get_mean_stdev_highest_profits():
    all_maxs = profits.max(axis=1)
    mean_of_maxs = sum(all_maxs)/len(all_maxs)
    
    diff = [elt - mean_of_maxs for elt in all_maxs]
    sqd_diff = [elt ** 2 for elt in diff]
    max_stdev = (sum(sqd_diff)/len(diff)) ** 1/2
    return "mean of maximum profits followed by standard deviation:", mean_of_maxs, max_stdev

#the average cumulative profit for each day across runs (i.e., the average of the two day cumulative profit
    #,average of the three day cumulative profit, etc.
def get_cumulative_averages():
    cumulative_avgs = {}
    column_num = 1
    while column_num < 31:
        for column in cumu_profits:
            cumulative_avgs[column_num] = cumu_profits[column].mean()
            column_num += 1
    return "average cumulative profits:", cumulative_avgs

#a line graph of the average cumulative profits for each day with day on the x-axis and average profit on the y-axis
def plot_profit_data():
    x_list = []
    y_list = []
    cumu_averages = get_cumulative_averages()
    for key in cumu_averages:
        x_list.append(key)
        y_list.append(cumu_averages[key])

    my_figure = plt.figure()
    subplot = my_figure.add_subplot(1,1,1)
    my_subplot = subplot.plot(x_list,y_list)
    plt.show()
    #plt.savefig('my_final.png')  #In case plot is to be saved at later time 


#Set up tests for code    
test1 = get_mean_stdev_avg_daily_profit()
#print(test1)
test2 = get_mean_stdev_cumu_daily_profit()
#print(test2)
test3 = get_mean_stdev_lowest_profits()
#print(test3)
test4 = get_mean_stdev_highest_profits()
#print(test4)
test5 = get_cumulative_averages()
#print(test5)
test6 = plot_profit_data()
#test6



# In[ ]:



