# Shelby Jennings
# IEOR4572, Professor Johar
# Assignment 3: Google sector data
    
def google_sector_report():
  
    # List of sectors reported on Google page - used to check with page input later
    list_sectors = ['Energy', 'Basic Materials', 'Industrials', 'Cyclical Cons. Goods ...',
                   'Non-Cyclical Cons. Goods...', 'Financials', 'Healthcare', 'Technology',
                   'Telecommunications Servi...', 'Utilities']
    
    d = {} # Final dict 
    d['STATUS'] = 'BAD' # Set default value of Status to Bad to indicate no data 
    d['result'] = {} # Setting up result entry to house sector information

    # Get BeautifulSoup for web scraping of Google finance data
    import requests
    from bs4 import BeautifulSoup
    url = "https://www.google.com/finance"
    response = requests.get(url)
    
    # If get was successful move on to explore data 
    if response.status_code == 200:
        d['STATUS'] = 'GOOD'
        page_data_soup = BeautifulSoup(response.content, 'lxml')
    
        for tag in page_data_soup.find_all('a'): 
            for name in list_sectors:
                if name == tag.get_text(): # If each sector name is found in link tag set 
                    sector_tag = tag # get name of sector from the tag's text
                    sector_name = tag.get_text()                
                    d['result'][name] = {} # Create entry dict for each sector in result
 
                    for tag in page_data_soup.find_all('span'):
                        if tag.get('class') == ['chg']: # Want to find change percentage in sector 
                            sector_chg = tag.get_text() # Search for tags with 'chg' and get text
                            break # Stop to only record first find
                    
                    # Define link to access each sector specific page
                    sector_link = 'https://www.google.com' + sector_tag.get('href')
                    sector_response = requests.get(sector_link)
                    
                    # If get is successful move on to explore sector specific information 
                    if sector_response.status_code == 200:
                        sector_data_soup = BeautifulSoup(sector_response.content, 'lxml')
                    
                        for tag in sector_data_soup.find_all('table'):
                            if 'Gainers' in tag.get_text(): # Want to find name of top gainer 
                                biggest_gainer = tag.find('a').get_text() 
                                break # Break to only record the first entry i.e. the top gainer
                        if biggest_gainer == None: # If there is no top gainer record as empty string 
                            biggest_gainer == ""
                                
                        for tag in sector_data_soup.find_all('span'):
                            if tag.get('class') == ['chg']: # Want to find percentage change for top gainer
                                if '%' in tag.get_text():
                                    percent_chg_up = tag.get_text() # Search for 'chg' tags 
                                    break # then break after finding first entry
                        if percent_chg_up == None: # If there is no percentage change 
                            percent_chg_up = "Null" # set to null
                    
                        for tag in sector_data_soup.find_all('table'):
                            if 'Losers' in tag.get_text(): # Want to find name of top loser 
                                biggest_loser = tag.find_all('a')[10].get_text() # item at index 10 is 1st in loser list
                        if biggest_loser == None: 
                            biggest_loser = "" 

                        for tag in sector_data_soup.find_all('span'):
                            if tag.get('class') == ['chr']: # Want to find percentage change of top loser
                                if '%' in tag.get_text(): 
                                    percent_chg_dwn = tag.get_text()
                                    break
                        if percent_chg_dwn == None: 
                            percent_chg_dwn = "Null" 
                    
                    else: # If subsequent request was unsuccessful update Status to Bad
                        d['Status'] = 'BAD'
                        
    
                
        # Add in all recorded values by sector into final dict
        d['result'][sector_name] = {}
        d['result'][sector_name]['biggest_loser'] = {}
        d['result'][sector_name]['biggest_gainer'] = {}
        d['result'][sector_name]['change'] = sector_chg
        d['result'][sector_name]['biggest_gainer']['equity'] = biggest_gainer
        d['result'][sector_name]['biggest_gainer']['change'] = percent_chg_up
        d['result'][sector_name]['biggest_loser']['equity'] = biggest_loser
        d['result'][sector_name]['biggest_loser']['change'] = percent_chg_dwn
        
        # If entire dict entry is missing for a sector, go back and record each key's value as below
        for name in list_sectors:
            if d['result'][name] == {}:
                    d['result'][name]['change'] = "Null"
                    d['result'][name]['biggest_gainer'] = {}
                    d['result'][name]['biggest_gainer']['equity'] = ""
                    d['result'][name]['biggest_gainer']['change'] = "Null"
                    d['result'][name]['biggest_loser'] = {}
                    d['result'][name]['biggest_loser']['equity'] = ""
                    d['result'][name]['biggest_loser']['change'] = "Null"
            
            
        
        import json 
        return json.dumps(d) # Final output 
    
    else: # If initial request was unsuccessful return "empty" final dictionary 
        import json
        return json.dumps(d)

    
