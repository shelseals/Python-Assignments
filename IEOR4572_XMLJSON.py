# Shelby Jennings, ssj2124
# IEOR W4572 HW 2, Professor Johar
# XML/JSON Assignment

# JSON

def get_json_geolocation_data(address_string, form="JSON", country="ALL", types=False):
    address = '_'.join(address_string.split(' ')) # Prepare to input address to web
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" % (address)
    import requests
    response = requests.get(url) # Grabbing geo information from web
    if response.status_code == 200: # If request is successful continue otherwise end
        json_data = response.json()
        # Creating to list to input final entries
        x_list = []
        for x in json_data['results']:
            # If type is True, it's added to each entry
            if types == True:
                x_list.extend([(x['formatted_address'],x['geometry']['location']['lat'],x['geometry']['location']['lng'], x['types'])])
            else:
                x_list.extend([(x['formatted_address'],x['geometry']['location']['lat'],x['geometry']['location']['lng'])])
        # If country is not "ALL", 
        if country != "ALL":
            for item in x_list:
                address_split = item[0].split(',') 
                result_country = address_split[-1] # Want to split formatted_address entry
                if result_country != country: # in order to figure out what country is 
                    x_list.remove(item)
        return x_list
    else:
        return None 
    
    
# XML

def get_xml_geolocation_data(address_string, form="XML", country="ALL", types=False):
    address = '_'.join(address_string.split(' ')) # Prepare to input address to web
    url = "https://maps.googleapis.com/maps/api/geocode/xml?address=%s" % (address)
    import requests
    response = requests.get(url) # Grabbing geo information from web
    if response.status_code == 200: # If request is successful continue otherwise end
        data = response.content
        from lxml import etree # Want to create xml tree from Google data 
        root = etree.XML(data) 
        x_list = []
        for child in root:
            if types == True: # Add type to x_list given True
                entry = [(root.find('result/formatted_address').text,
                    root.find('result/geometry/location/lat').text, 
                    root.find('result/geometry/location/lng').text, 
                    root.find('result/type').text)]
                x_list.extend(entry)
                if country != "ALL": # Want to remove entries with different country
                    address_parts = entry[0].split(',') # Consider first piece of entry
                    address_country = address_parts[-1] # Then look at its last elt to 
                    if address_country != country: # get the country code 
                        x_list.remove(entry)
            else:
                entry = [(root.find('result/formatted_address').text,
                     root.find('result/geometry/location/lat').text, 
                     root.find('result/geometry/location/lng').text)] 
                x_list.extend(entry)
                if country != "ALL": # Want to remove entries with different country
                    address_parts = entry[0].split(',') # Split formatted_address entry
                    address_country = address_parts[-1] # to figure out what country is 
                    if address_country != country:
                        x_list.remove(entry)
        
        return x_list 
    else:
        return None 


# COMBINED METHOD

def get_geolocation_data(address_string, form="JSON", country="ALL", types=False):
    if form == "XML": # Use XML method
        return get_xml_geolocation_data(address_string,form="XML", country="ALL", types=False)
    else: # Use JSON method
        return get_json_geolocation_data(address_string, form="JSON", country="ALL", types=False)





