
# coding: utf-8

# In[1]:

get_ipython().system('pip install pymongo')


# In[143]:

#Shelby Jennings and Andrea van Ryzin
#October 18, 2016
#Data Analytics for OR
#MongoDB Assignment


import json
import pymongo
from pymongo import MongoClient
from datetime import datetime


class Interface(MongoClient):
    def __init__(self):
        self._settings = {'db':'sector_database','collection':'sector_collection'}
        self._collection = MongoClient()[self._settings['db']][self._settings['collection']]
        

    def insert(self, file_list): # Inserts each object in file list into database with key date and value dictionary
        for element in file_list:
            self._collection.insert_one({element['date']:element})             
    
    
    def update(self): # To add new file from "today"
        self._collection.insert_one(google_sector_report()) 

        
    # Which sector has had the greatest move on a given date?
    def sector_greatest_move_on_date(self, date): 
        greatest_sector_move = 0
        sector_with_greatest = None
        for doc in self._collection.find(): 
            for key in doc:
                if key == date: # Match input date with date key in each file
                    for sector in doc[key]:
                        if doc[key][sector] != date: # Only iterate over keys that are sectors 
                            if 'change' in doc[key][sector]:
                                change = float(doc[key][sector]['change'])
                                if abs(change) > abs(greatest_sector_move): # Compare each change value to current max
                                    greatest_sector_move = change
                                    sector_with_greatest = sector
        return sector_with_greatest

    
    # Which sector has had the greatest move ever?
    def sector_greatest_move_ever(self):
        greatest_sector_move = 0 # Set default values to 0 and None
        sector_with_greatest = None
        for doc in self._collection.find():
            for key in doc:
                if len(key) > 3: # If key is not the id value
                    for sector in doc[key]:
                        if sector not in ['result', 'date', 'status']: # If new key in doc[key] dict is actually a sector
                            if 'change' in doc[key][sector]:
                                change = float(doc[key][sector]['change'])
                                if abs(change) > abs(greatest_sector_move): # Compare and update move as it iterates
                                    greatest_sector_move = change
                                    sector_with_greatest = sector
                                    
        return sector_with_greatest
    

    # Which stock has had the greatest move on a given date?    
    def stock_greatest_move_on_date(self, date):
        greatest_stock_move = 0 # Set default values to 0 
        stock_with_greatest = None
        for doc in self._collection.find():
            for key in doc:
                if key == date: # If date matches date given
                    for sector in doc[key]:
                        if doc[key][sector] != date: # If this value is not a date value 
                            if 'biggest_gainer' in doc[key][sector]: # If this value is actually a sector 
                                gain = doc[key][sector]['biggest_gainer'] # Compare gainer and loser changes
                                if gain['change'] != None: 
                                    stock_move_g = float(gain['change'])
                                    stock_g = gain['equity']
                                else:
                                    stock_move_g = 0
                                    stock_g = None
                                loser = doc[key][sector]['biggest_loser']
                                if loser['change'] != None:
                                    stock_move_l = float(loser['change'])
                                    stock_l = loser['equity']
                                else:
                                    stock_move_l = 0
                                    stock_g = None
                                stock_winner = max(abs(stock_move_g), abs(stock_move_l)) # Take max of these 2
                                if stock_winner == abs(stock_move_g):
                                    stock = stock_g
                                elif stock_winner == abs(stock_move_l):
                                    stock = stock_l
                                if abs(stock_winner) > abs(greatest_stock_move): # Compare to current greatest 
                                    greatest_stock_move = stock_winner
                                    stock_with_greatest = stock 
        return stock_with_greatest
    
    
    # Which stock has had the greatest move ever? 
    def stock_greatest_move_ever(self):
        greatest_stock_move = 0
        stock_with_greatest = None
        for doc in self._collection.find():
            for key in doc:
                if len(key) > 3:
                    for sector in doc[key]:
                        if 'biggest_gainer' in doc[key][sector]:
                            gain = doc[key][sector]['biggest_gainer']
                            if gain['change'] != None:
                                stock_move_g = float(gain['change'])
                                stock_g = gain['equity']
                            else:
                                stock_move_g = 0
                                stock_g = None
                            loser = doc[key][sector]['biggest_loser']
                            if loser['change'] != None:
                                stock_move_l = float(loser['change'])
                                stock_l = loser['equity']
                            else:
                                stock_move_l = 0
                                stock_g = None
                            stock_winner = max(abs(stock_move_g), abs(stock_move_l))
                            if stock_winner == abs(stock_move_g):
                                stock = stock_g
                            elif stock_winner == abs(stock_move_l):
                                stock = stock_l
                            if abs(stock_winner) > abs(greatest_stock_move):
                                greatest_stock_move = stock_winner
                                stock_with_greatest = stock 
        return stock_with_greatest

    
    # Returns a list of (date, change) tuples for a given sector    
    def date_change_tuple(self, sector_name):
        tuple_list = []
        for doc in self._collection.find():
            for key in doc:
                if len(key) >3:
                    for sector in doc[key]:
                        if sector == sector_name:
                            if "change" in doc[key][sector]:
                                change = doc[key][sector]["change"]
                                tup = (key, change)
                                if tup not in tuple_list:
                                    tuple_list.append(tup)
                        
        return tuple_list
    
    
    # On a given day, what was the average change increase (pos)?
    def average_change_increase(self, date):
        all_sector_increases = []
        for doc in self._collection.find():
            for key in doc:
                if key == date:
                    for sector in doc[key]:
                        if doc[key][sector] != date:
                            if 'change' in doc[key][sector]:
                                change = float(doc[key][sector]['change'])
                                if change > 0:
                                    all_sector_increases.append(change)
        if len(all_sector_increases) > 0:
            sum_increases = sum(all_sector_increases)
            average_change_increase = float(sum_increases) / float(len(all_sector_increases))
            return average_change_increase
        else:
            return "No increases on " + date # If there aren't any positive changes 
        
        
    # On a given day, what was the average change decrease (neg)?
    def average_change_decrease(self, date):
        all_sector_decreases = []
        for doc in self._collection.find():
            for key in doc:
                if key == date:
                    for sector in doc[key]:
                        if doc[key][sector] != date:
                            if 'change' in doc[key][sector]:
                                change = float(doc[key][sector]['change'])
                                if change < 0:
                                    all_sector_decreases.append(change)
        if len(all_sector_decreases) > 0:
            sum_decreases = sum(all_sector_decreases)
            average_change_decrease = float(sum_decreases) / float(len(all_sector_decreases))
            return average_change_decrease
        else:
            return "No decreases on " + date # If there aren't any negative changes 
    
    
    # What sector had the largest biggest gainer?
    def sector_largest_biggest_gainer(self):
        greatest_gainer = 0
        sector_with_greatest = None
        for doc in self._collection.find():
            for key in doc:
                if len(key) > 3:
                    for sector in doc[key]:
                        if 'biggest_gainer' in doc[key][sector]:
                            gain = doc[key][sector]['biggest_gainer']
                            if gain != None:
                                if gain['change'] != None:
                                    sector_gainer = float(gain['change'])
                                    sector_g = gain['equity']
                                else:
                                    sector_gainer = 0
                                    sector_g = None
                                if abs(sector_gainer) > abs(greatest_gainer):
                                    greatest_gainer = sector_gainer
                                    sector_with_greatest = sector_g
        return sector_with_greatest
        
        
    # What sector had the smallest change (absolute value)?
    def sector_smallest_absval_change(self):
        smallest_sector_move = 100 # Just chose random large number likely to be larger than any change
        sector_with_smallest = None
        for doc in self._collection.find():
            for key in doc:
                if len(key) > 3: 
                    for sector in doc[key]:
                        if sector not in ['result', 'date', 'status']: 
                            if 'change' in doc[key][sector]:
                                if doc[key][sector]['change'] != None:
                                    change = float(doc[key][sector]['change'])
                                    if abs(change) < abs(smallest_sector_move):
                                        smallest_sector_move = change
                                        sector_with_smallest = sector

        return sector_with_smallest

    
#Andrea van Ryzin
#Web Scraping Assignment
def google_sector_report():
    
    import json
    import requests 
    from bs4 import BeautifulSoup 
    import datetime
    url = "https://www.google.com/finance"
    response = requests.get(url) 
    d = {}
    date = datetime.date.today().strftime("%Y %m %d") #Year month day
    print(date)
    d["date"] = date
    
    if response.status_code == 200:
        d["STATUS"] = "GOOD"
        page_soup = BeautifulSoup(response.content,'lxml') 
        
        sectors_info = page_soup.find_all('div', class_ = 'id-secperf')
        
        for item in sectors_info:
            sector_names = item.find_all("a")
            sector_dict = {}
            
            for sn in sector_names:
                sector_change = sn.find('span', class_ = "chg")
                sectors = sn.find_all('tr')
                link = "http://google.com" + sn.get('href')

                link_response = requests.get(link) 
                link_soup = BeautifulSoup(link_response.content,'lxml') 
                top_movers = link_soup.find_all('div', class_ = 'sfe-break-bottom')
                
                for element in top_movers:
                    gainer_loser_dict = {}
                    companies = element.find_all('a')
                    
                    gainer_dict = {}
                    biggest_gainer = companies[0].get_text()
                    gainer_changes = element.find_all('span', class_ = "chg")
                    gainer_change = gainer_changes[1].get_text().strip("()").strip("%")
                    gainer_dict['change'] = gainer_change
                    gainer_dict['equity'] = biggest_gainer
                    
                    loser_dict = {}
                    biggest_loser = companies[10].get_text()
                    loser_changes = element.find_all('span', class_ = "chr")
                    loser_change = loser_changes[1].get_text().strip("()").strip("%")
                    loser_dict['change'] = loser_change
                    loser_dict['equity'] = biggest_loser
                    
                    gainer_loser_dict['biggest_gainer'] = gainer_dict
                    gainer_loser_dict['biggest_loser'] = loser_dict
                    sector_dict[sn.get_text().replace(".", "")] = gainer_loser_dict  #gets rid of "." in sector name
                    
                    bold = element.find_all('b')
                    headings = list()
                    for b in bold:
                        headings.append(b.get_text())
                    if "Gainers (% price change)"not in headings:
                        gainer_loser_dict['biggest_gainer'] = None
                    elif "Losers (% price change)" not in headings:
                        gainer_loser_dict['biggest_loser'] = None
                    
            
            d['result'] = sector_dict

    else:
        d["STATUS"] = "BAD"
        print(d)
    
    with open(date + ".json", "w") as outfile:
            json.dump(d, outfile)
    
    
data1 = { 'result': { 'Basic Materials': { 'biggest_gainer': { 'change': 4.97,
                                                    'equity': 'Green Plains '
                                                                 'Inc'},
                                   'biggest_loser': { 'change': -18.6,
                                                      'equity': 'Gold Resource '
                                                                'Corporation'},
                                   'change': -1.99},
              'Cyclical Cons Goods': { 'biggest_gainer': { 'change': 9.64,
                                                                'equity': 'McClatchy '
                                                                          'Co'},
                                            'biggest_loser': { 'change': -5.82,
                                                               'equity': 'Marchex, '
                                                                         'Inc.'},
                                            'change': -0.22},
              'Energy': { 'biggest_gainer': { 'change': 23.72,
                                              'equity': 'Seadrill Ltd'},
                          'biggest_loser': { 'change': -8.82,
                                             'equity': 'Ferrellgas Partners, '
                                                       'L.P.'},
                          'change': -0.66},
              'Financials': { 'biggest_gainer': { 'change': 35.27,
                                                  'equity': 'Endurance '
                                                            'Specialty Hldgs'},
                              'biggest_loser': { 'change': -17.08,
                                                 'equity': 'PIMCO Global '
                                                           'StocksPLUS'},
                              'change': -0.17},
              'Healthcare': { 'biggest_gainer': { 'change': 16.46,
                                                  'equity': 'TeamHealth '
                                                            'Holdings Inc'},
                              'biggest_loser': { 'change': -50.27,
                                                 'equity': 'Trinity Biotech '
                                                           'plc (ADR)'},
                              'change': -0.24},
              'Industrials': { 'biggest_gainer': { 'change': 633.43,
                                                   'equity': 'LML Payment '
                                                             'Systems, Inc.'},
                               'biggest_loser': { 'change': -19.12,
                                                  'equity': 'Costamare Inc'},
                               'change': -0.61},
              'Non-Cyclical Cons Goods': { 'biggest_gainer': { 'change': None,
                                                                   'equity': ''},
                                               'biggest_loser': { 'change': -4.49,
                                                                  'equity': "Pilgrim's "
                                                                            'Pride '
                                                                            'Corp.'},
                                               'change': -0.32},
              'Technology': { 'biggest_gainer': { 'change': 20.49,
                                                  'equity': 'Renren Inc'},
                              'biggest_loser': { 'change': -6.59,
                                                 'equity': 'VirnetX Holding '
                                                           'Corp.'},
                              'change': -0.11},
              'Telecommunications Servi': { 'biggest_gainer': { 'change': 4.09,
                                                                   'equity': 'Internet '
                                                                             'Gold '
                                                                             'Golden'},
                                               'biggest_loser': { 'change': -5.99,
                                                                  'equity': 'PLDT '
                                                                            'Inc '
                                                                            '(ADR)'},
                                               'change': -0.93},
              'Utilities': { 'biggest_gainer': { 'change': 0.17,
                                                 'equity': 'Genie Energy Ltd'},
                             'biggest_loser': { 'change': -4.32,
                                                'equity': 'Southwest Gas '
                                                          'Corporation'},
                             'change': -1.98}},
  'status': 'GOOD', 'date' : '20161004'}



data2 = { 'result': { 'Basic Materials': { 'biggest_gainer': { 'change': 5.85,
                                                       'equity': 'CVR Partners '
                                                                 'LP'},
                                   'biggest_loser': { 'change': -5.35,
                                                      'equity': 'NovaGold '
                                                                'Resources '
                                                                'Inc'},
                                   'change': 1.01},
              'Cyclical Cons Goods': { 'biggest_gainer': { 'change': 8.56,
                                                                'equity': 'Kandi '
                                                                          'Tech. '
                                                                          'Group '
                                                                          'Inc'},
                                            'biggest_loser': { 'change': -4.71,
                                                               'equity': 'Acuity '
                                                                         'Brands, '
                                                                         'Inc.'},
                                            'change': 0.41},
              'Energy': { 'biggest_gainer': { 'change': 19.55,
                                              'equity': 'Resolute Energy Corp'},
                          'biggest_loser': { 'change': -3.31,
                                             'equity': 'Westmoreland Coal '
                                                       'Company'},
                          'change': 1.84},
              'Financials': { 'biggest_gainer': { 'change': 8.04,
                                                  'equity': 'NewStar Financial '
                                                            'Inc'},
                              'biggest_loser': { 'change': -5.44,
                                                 'equity': 'Asta Funding, '
                                                           'Inc.'},
                              'change': 0.79},
              'Healthcare': { 'biggest_gainer': { 'change': 15.86,
                                                  'equity': 'CorMedix Inc.'},
                              'biggest_loser': { 'change': -23.78,
                                                 'equity': 'Immunomedics, '
                                                           'Inc.'},
                              'change': 0.39},
              'Industrials': { 'biggest_gainer': { 'change': 633.43,
                                                   'equity': 'LML Payment '
                                                             'Systems, Inc.'},
                               'biggest_loser': { 'change': -13.99,
                                                  'equity': 'AZZ Inc'},
                               'change': 0.58},
              'Non-Cyclical Cons Goods': { 'biggest_gainer': { 'change': None,
                                                                   'equity': ''},
                                               'biggest_loser': { 'change': -5.07,
                                                                  'equity': 'Lifeway '
                                                                            'Foods, '
                                                                            'Inc.'},
                                               'change': 0.18},
              'Technology': { 'biggest_gainer': { 'change': 7.07,
                                                  'equity': 'GigPeak Inc'},
                              'biggest_loser': { 'change': -5.8,
                                                 'equity': 'salesforce.com, '
                                                           'inc.'},
                              'change': 0.48},
              'Telecommunications Servi': { 'biggest_gainer': { 'change': 3.06,
                                                                   'equity': 'General '
                                                                             'Communication'},
                                               'biggest_loser': { 'change': -3.14,
                                                                  'equity': 'Cincinnati '
                                                                            'Bell '
                                                                            'Inc.'},
                                               'change': -0.17},
              'Utilities': { 'biggest_gainer': { 'change': 3.66,
                                                 'equity': 'Energy Transfer '
                                                           'Partners'},
                             'biggest_loser': { 'change': -2.27,
                                                'equity': 'TransAlta Corp. '
                                                          '(USA)'},
                             'change': -0.17}},
  'status': 'GOOD', 'date' : '20161005'}


data3 = { 'result': { 'Basic Materials': { 'biggest_gainer': { 'change': 4.88,
                                                       'equity': 'US Concrete '
                                                                 'Inc'},
                                   'biggest_loser': { 'change': -11.43,
                                                      'equity': 'LSB '
                                                                'Industries, '
                                                                'Inc.'},
                                   'change': 0.0},
              'Cyclical Cons Goods': { 'biggest_gainer': { 'change': 15.76,
                                                                'equity': 'Zumiez '
                                                                          'Inc.'},
                                            'biggest_loser': { 'change': -10.19,
                                                               'equity': 'Cato '
                                                                         'Corp'},
                                            'change': -0.27},
              'Energy': { 'biggest_gainer': { 'change': 6.34,
                                              'equity': 'Contango Oil & Gas '
                                                        'Co.'},
                          'biggest_loser': { 'change': -10.7,
                                             'equity': 'CIRCOR Intl., Inc.'},
                          'change': 0.47},
              'Financials': { 'biggest_gainer': { 'change': 4.64,
                                                  'equity': 'LNB Bancorp Inc'},
                              'biggest_loser': { 'change': -8.03,
                                                 'equity': 'Federated '
                                                           'National'},
                              'change': -0.01},
              'Healthcare': { 'biggest_gainer': { 'change': 14.86,
                                                  'equity': 'ICU Medical, '
                                                            'Incorporated'},
                              'biggest_loser': { 'change': -48.49,
                                                 'equity': 'Alnylam '
                                                           'Pharmaceuticals'},
                              'change': -0.63},
              'Industrials': { 'biggest_gainer': { 'change': 633.43,
                                                   'equity': 'LML Payment '
                                                             'Systems, Inc.'},
                               'biggest_loser': { 'change': -12.63,
                                                  'equity': 'Resources '
                                                            'Connection, Inc'},
                               'change': 0.03},
              'Non-Cyclical Cons Goods': { 'biggest_gainer': { 'change': None,
                                                                   'equity': ''},
                                               'biggest_loser': { 'change': -3.92,
                                                                  'equity': 'Weight '
                                                                            'Watchers '
                                                                            'Intl'},
                                               'change': 0.42},
              'Technology': { 'biggest_gainer': { 'change': 5.92,
                                                  'equity': 'AIXTRON SE (ADR)'},
                              'biggest_loser': { 'change': -10.05,
                                                 'equity': 'Park '
                                                           'Electrochemical '
                                                           'Corp'},
                              'change': 0.18},
              'Telecommunications Servi': { 'biggest_gainer': { 'change': 3.07,
                                                                   'equity': 'B '
                                                                             'Communications '
                                                                             'Ltd'},
                                               'biggest_loser': { 'change': -2.81,
                                                                  'equity': 'BT '
                                                                            'Group '
                                                                            'plc '
                                                                            '(ADR)'},
                                               'change': -0.53},
              'Utilities': { 'biggest_gainer': { 'change': 3.44,
                                                 'equity': 'Empresa '
                                                           'Distribuidora y'},
                             'biggest_loser': { 'change': -3.94,
                                                'equity': 'Genon Energy Inc'},
                             'change': -0.29}},
  'status': 'GOOD', 'date' : '20161006'}


data4 = { 'result': { 'Basic Materials': { 'biggest_gainer': { 'change': 4.85,
                                                       'equity': 'McEwen '
                                                                 'Mining Inc'},
                                   'biggest_loser': { 'change': -8.28,
                                                      'equity': 'PPG '
                                                                'Industries, '
                                                                'Inc.'},
                                   'change': -0.77},
              'Cyclical Cons Goods': { 'biggest_gainer': { 'change': 15.23,
                                                                'equity': 'Gap '
                                                                          'Inc'},
                                            'biggest_loser': { 'change': -8.59,
                                                               'equity': 'Lee '
                                                                         'Enterprises, '
                                                                         'Inc.'},
                                            'change': -0.55},
              'Energy': { 'biggest_gainer': { 'change': 4.92,
                                              'equity': 'BP Prudhoe Bay '
                                                        'Royalty'},
                          'biggest_loser': { 'change': -9.32,
                                             'equity': 'CIRCOR Intl., Inc.'},
                          'change': -0.52},
              'Financials': { 'biggest_gainer': { 'change': 10.76,
                                                  'equity': 'Federated '
                                                            'National'},
                              'biggest_loser': { 'change': -24.19,
                                                 'equity': 'Cousins Properties '
                                                           'Inc'},
                              'change': -0.21},
              'Healthcare': { 'biggest_gainer': { 'change': 11.59,
                                                  'equity': 'Curis, Inc.'},
                              'biggest_loser': { 'change': -21.73,
                                                 'equity': 'Senomyx Inc.'},
                              'change': 0.04},
              'Industrials': { 'biggest_gainer': { 'change': 633.43,
                                                   'equity': 'LML Payment '
                                                             'Systems, Inc.'},
                               'biggest_loser': { 'change': -7.5,
                                                  'equity': 'Honeywell Intl. '
                                                            'Inc.'},
                               'change': -1.09},
              'Non-Cyclical Cons Goods': { 'biggest_gainer': { 'change': None,
                                                                   'equity': ''},
                                               'biggest_loser': { 'change': -9.7,
                                                                  'equity': 'H&E '
                                                                            'Equipment '
                                                                            'Services'},
                                               'change': 0.04},
              'Technology': { 'biggest_gainer': { 'change': 5.21,
                                                  'equity': 'QAD Inc.'},
                              'biggest_loser': { 'change': -12.99,
                                                 'equity': 'Mistras Group Inc'},
                              'change': -0.22},
              'Telecommunications Servi': { 'biggest_gainer': { 'change': 6.02,
                                                                   'equity': 'Frontier '
                                                                             'Communications'},
                                               'biggest_loser': { 'change': -3.2,
                                                                  'equity': 'NQ '
                                                                            'Mobile '
                                                                            'Inc '
                                                                            '(ADR)'},
                                               'change': -0.67},
              'Utilities': { 'biggest_gainer': { 'change': 3.14,
                                                 'equity': 'NextEra Energy '
                                                           'Inc'},
                             'biggest_loser': { 'change': -3.47,
                                                'equity': 'National Grid plc '
                                                          '(ADR)'},
                             'change': -0.34}},
  'status': 'GOOD', 'date' : '2016-10-07'}


data5 = { 'result': { 'Basic Materials': { 'biggest_gainer': { 'change': 6.8,
                                                       'equity': 'Resolute '
                                                                 'Forest '
                                                                 'Products'},
                                   'biggest_loser': { 'change': -1.47,
                                                      'equity': 'Syngenta AG '
                                                                '(ADR)'},
                                   'change': 1.01},
              'Cyclical Cons Goods': { 'biggest_gainer': { 'change': 9.4,
                                                                'equity': 'Ruby '
                                                                          'Tuesday, '
                                                                          'Inc.'},
                                            'biggest_loser': { 'change': -9.32,
                                                               'equity': 'Haverty '
                                                                         'Furniture'},
                                            'change': 0.12},
              'Energy': { 'biggest_gainer': { 'change': 10.84,
                                              'equity': 'Approach Resources '
                                                        'Inc.'},
                          'biggest_loser': { 'change': -3.62,
                                             'equity': 'SemGroup Corp'},
                          'change': 1.71},
              'Financials': { 'biggest_gainer': { 'change': 8.7,
                                                  'equity': 'Walter '
                                                            'Investment'},
                              'biggest_loser': { 'change': -24.19,
                                                 'equity': 'Cousins Properties '
                                                           'Inc'},
                              'change': 0.43},
              'Healthcare': { 'biggest_gainer': { 'change': 10.3,
                                                  'equity': 'Clovis Oncology '
                                                            'Inc'},
                              'biggest_loser': { 'change': -11.6,
                                                 'equity': 'Myriad Genetics, '
                                                           'Inc.'},
                              'change': 0.29},
              'Industrials': { 'biggest_gainer': { 'change': 633.43,
                                                   'equity': 'LML Payment '
                                                             'Systems, Inc.'},
                               'biggest_loser': { 'change': -7.71,
                                                  'equity': 'Dover Corp'},
                               'change': 0.24},
              'Non-Cyclical Cons Goods': { 'biggest_gainer': { 'change': None,
                                                                   'equity': ''},
                                               'biggest_loser': { 'change': -3.2,
                                                                  'equity': 'Bridgford '
                                                                            'Foods '
                                                                            'Corp.'},
                                               'change': 0.53},
              'Technology': { 'biggest_gainer': { 'change': 5.94,
                                                  'equity': 'salesforce.com, '
                                                            'inc.'},
                              'biggest_loser': { 'change': -4.26,
                                                 'equity': 'Radware Ltd.'},
                              'change': 0.62},
              'Telecommunications Servi': { 'biggest_gainer': { 'change': 3.86,
                                                                   'equity': 'Sprint '
                                                                             'Communications '
                                                                             'Inc'},
                                               'biggest_loser': { 'change': -6.21,
                                                                  'equity': 'Telefonica '
                                                                            'Brasil '
                                                                            'SA '
                                                                            '(ADR'},
                                               'change': 0.62},
              'Utilities': { 'biggest_gainer': { 'change': 66.45,
                                                 'equity': 'Gas Natural Inc'},
                             'biggest_loser': { 'change': -0.3,
                                                'equity': 'Korea Electric '
                                                          'Power Corp'},
                             'change': 0.95}},
  'status': 'GOOD', 'date' : '2016-10-10'}


data6 = { 'result': { 'Basic Materials': { 'biggest_gainer': { 'change': 5.01,
                                                       'equity': 'Braskem SA '
                                                                 '(ADR)'},
                                   'biggest_loser': { 'change': -11.42,
                                                      'equity': 'Alcoa Inc'},
                                   'change': -1.7},
              'Cyclical Cons Goods': { 'biggest_gainer': { 'change': 9.77,
                                                                'equity': 'Ruby '
                                                                          'Tuesday, '
                                                                          'Inc.'},
                                            'biggest_loser': { 'change': -28.73,
                                                               'equity': 'Rent-A-Center '
                                                                         'Inc'},
                                            'change': -1.03},
              'Energy': { 'biggest_gainer': { 'change': 5.71,
                                              'equity': 'Comstock Resources '
                                                        'Inc'},
                          'biggest_loser': { 'change': -5.94,
                                             'equity': 'Westmoreland Coal '
                                                       'Company'},
                          'change': -1.43},
              'Financials': { 'biggest_gainer': { 'change': 6.86,
                                                  'equity': 'LPL Financial '
                                                            'Hldgs. Inc'},
                              'biggest_loser': { 'change': -24.19,
                                                 'equity': 'Cousins Properties '
                                                           'Inc'},
                              'change': -1.01},
              'Healthcare': { 'biggest_gainer': { 'change': 12.54,
                                                  'equity': 'Momenta '
                                                            'Pharmaceuticals'},
                              'biggest_loser': { 'change': -24.81,
                                                 'equity': 'Illumina, Inc.'},
                              'change': -2.28},
              'Industrials': { 'biggest_gainer': { 'change': 633.43,
                                                   'equity': 'LML Payment '
                                                             'Systems, Inc.'},
                               'biggest_loser': { 'change': -7.69,
                                                  'equity': 'KBR, Inc.'},
                               'change': -1.12},
              'Non-Cyclical Cons Goods': { 'biggest_gainer': { 'change': 13.09,
                                                                   'equity': 'Lifeway '
                                                                             'Foods, '
                                                                             'Inc.'},
                                               'biggest_loser': { 'change': -10.97,
                                                                  'equity': "Aaron's, "
                                                                            'Inc.'},
                                               'change': -0.2},
              'Technology': { 'biggest_gainer': { 'change': 6.36,
                                                  'equity': 'Carbonite Inc'},
                              'biggest_loser': { 'change': -8.09,
                                                 'equity': 'Fabrinet'},
                              'change': -1.25},
              'Telecommunications Servi': { 'biggest_gainer': { 'change': 3.23,
                                                                   'equity': 'Iridium '
                                                                             'Communications'},
                                               'biggest_loser': { 'change': -3.64,
                                                                  'equity': 'Vonage '
                                                                            'Holdings '
                                                                            'Corp.'},
                                               'change': -0.89},
              'Utilities': { 'biggest_gainer': { 'change': 1.9,
                                                 'equity': 'RGC Resources '
                                                           'Inc.'},
                             'biggest_loser': { 'change': -3.16,
                                                'equity': 'Atlantic Power '
                                                          'Corp'},
                             'change': -1.14}},
  'status': 'GOOD', 'date' : '2016-10-11'}


data7 = { 'result': { 'Basic Materials': { 'biggest_gainer': { 'change': 6.16,
                                                       'equity': 'Asanko Gold '
                                                                 'Inc'},
                                   'biggest_loser': { 'change': -5.03,
                                                      'equity': 'LSB '
                                                                'Industries, '
                                                                'Inc.'},
                                   'change': 0.26},
              'Cyclical Cons Goods': { 'biggest_gainer': { 'change': 8.66,
                                                                'equity': 'Lifetime '
                                                                          'Brands '
                                                                          'Inc'},
                                            'biggest_loser': { 'change': -6.04,
                                                               'equity': 'Halozyme '
                                                                         'Therapeutics'},
                                            'change': 0.24},
              'Energy': { 'biggest_gainer': { 'change': 6.67,
                                              'equity': 'Northern Oil & Gas, '
                                                        'Inc.'},
                          'biggest_loser': { 'change': -6.81,
                                             'equity': 'Hornbeck Offshore'},
                          'change': -0.34},
              'Financials': { 'biggest_gainer': { 'change': 7.14,
                                                  'equity': 'Fang Holdings '
                                                            'Ltd'},
                              'biggest_loser': { 'change': -24.19,
                                                 'equity': 'Cousins Properties '
                                                           'Inc'},
                              'change': -0.01},
              'Healthcare': { 'biggest_gainer': { 'change': 12.14,
                                                  'equity': 'Senomyx Inc.'},
                              'biggest_loser': { 'change': -9.41,
                                                 'equity': 'Omeros '
                                                           'Corporation'},
                              'change': -0.51},
              'Industrials': { 'biggest_gainer': { 'change': 633.43,
                                                   'equity': 'LML Payment '
                                                             'Systems, Inc.'},
                               'biggest_loser': { 'change': -9.72,
                                                  'equity': 'Celadon Group, '
                                                            'Inc.'},
                               'change': 0.13},
              'Non-Cyclical Cons Goods': { 'biggest_gainer': { 'change': None,
                                                                   'equity': ''},
                                               'biggest_loser': { 'change': -3.12,
                                                                  'equity': 'Rite '
                                                                            'Aid '
                                                                            'Corporation'},
                                               'change': 0.61},
              'Technology': { 'biggest_gainer': { 'change': 5.13,
                                                  'equity': 'ChinaCache '
                                                            'Internatnl'},
                              'biggest_loser': { 'change': -20.83,
                                                 'equity': 'Telefonaktiebolaget '
                                                           'LM'},
                              'change': -0.07},
              'Telecommunications Servi': { 'biggest_gainer': { 'change': 1.86,
                                                                   'equity': 'SBA '
                                                                             'Communications '
                                                                             'Corp.'},
                                               'biggest_loser': { 'change': -3.89,
                                                                  'equity': 'Internet '
                                                                            'Gold '
                                                                            'Golden'},
                                               'change': 0.35},
              'Utilities': { 'biggest_gainer': { 'change': 2.53,
                                                 'equity': 'Connecticut Water '
                                                           'Service'},
                             'biggest_loser': { 'change': -2.32,
                                                'equity': 'Targa Resources '
                                                          'Corp'},
                             'change': 0.76}},
  'status': 'GOOD', 'date' : '2016-10-12'}

file_list_all = [data1, data2, data3, data4, data5, data6, data7] # Full list for testing 

I = Interface()
I.insert(file_list_all)
#print(I.sector_greatest_move_on_date("20161004"))
#print(I.sector_greatest_move_ever())
#print(I.stock_greatest_move_on_date("20161005"))
#print(I.stock_greatest_move_ever())
#print(I.date_change_tuple("Technology"))
#print(I.average_change_decrease("20161005"))
#print(I.sector_largest_biggest_gainer())
#print(I.sector_smallest_absval_change())


# In[ ]:



