{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 52,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "# Shelby Jennings, ssj2124\n",
    "# IEOR W4572 HW 2, Professor Johar\n",
    "# XML/JSON Assignment\n",
    "\n",
    "# JSON\n",
    "\n",
    "def get_json_geolocation_data(address_string, form=\"JSON\", country=\"ALL\", types=False):\n",
    "    address = '_'.join(address_string.split(' ')) # Prepare to input address to web\n",
    "    url = \"https://maps.googleapis.com/maps/api/geocode/json?address=%s\" % (address)\n",
    "    import requests\n",
    "    response = requests.get(url) # Grabbing geo information from web\n",
    "    if response.status_code == 200: # If request is successful continue otherwise end\n",
    "        json_data = response.json()\n",
    "        # Creating to list to input final entries\n",
    "        x_list = []\n",
    "        for x in json_data['results']:\n",
    "            # If type is True, it's added to each entry\n",
    "            if types == True:\n",
    "                x_list.extend([(x['formatted_address'],x['geometry']['location']['lat'],x['geometry']['location']['lng'], x['types'])])\n",
    "            else:\n",
    "                x_list.extend([(x['formatted_address'],x['geometry']['location']['lat'],x['geometry']['location']['lng'])])\n",
    "        # If country is not \"ALL\", \n",
    "        if country != \"ALL\":\n",
    "            for item in x_list:\n",
    "                address_split = item[0].split(',') \n",
    "                result_country = address_split[-1] # Want to split formatted_address entry\n",
    "                if result_country != country: # in order to figure out what country is \n",
    "                    x_list.remove(item)\n",
    "        return x_list\n",
    "    else:\n",
    "        return None \n",
    "    \n",
    "    \n",
    "# XML\n",
    "\n",
    "def get_xml_geolocation_data(address_string, form=\"XML\", country=\"ALL\", types=False):\n",
    "    address = '_'.join(address_string.split(' ')) # Prepare to input address to web\n",
    "    url = \"https://maps.googleapis.com/maps/api/geocode/xml?address=%s\" % (address)\n",
    "    import requests\n",
    "    response = requests.get(url) # Grabbing geo information from web\n",
    "    if response.status_code == 200: # If request is successful continue otherwise end\n",
    "        data = response.content\n",
    "        from lxml import etree # Want to create xml tree from Google data \n",
    "        root = etree.XML(data) \n",
    "        x_list = []\n",
    "        for child in root:\n",
    "            if types == True: # Add type to x_list given True\n",
    "                entry = [(root.find('result/formatted_address').text,\n",
    "                    root.find('result/geometry/location/lat').text, \n",
    "                    root.find('result/geometry/location/lng').text, \n",
    "                    root.find('result/type').text)]\n",
    "                x_list.extend(entry)\n",
    "                if country != \"ALL\": # Want to remove entries with different country\n",
    "                    address_parts = entry[0].split(',') # Consider first piece of entry\n",
    "                    address_country = address_parts[-1] # Then look at its last elt to \n",
    "                    if address_country != country: # get the country code \n",
    "                        x_list.remove(entry)\n",
    "            else:\n",
    "                entry = [(root.find('result/formatted_address').text,\n",
    "                     root.find('result/geometry/location/lat').text, \n",
    "                     root.find('result/geometry/location/lng').text)] \n",
    "                x_list.extend(entry)\n",
    "                if country != \"ALL\": # Want to remove entries with different country\n",
    "                    address_parts = entry[0].split(',') # Split formatted_address entry\n",
    "                    address_country = address_parts[-1] # to figure out what country is \n",
    "                    if address_country != country:\n",
    "                        x_list.remove(entry)\n",
    "        \n",
    "        return x_list \n",
    "    else:\n",
    "        return None \n",
    "\n",
    "\n",
    "# COMBINED METHOD\n",
    "\n",
    "def get_geolocation_data(address_string, form=\"JSON\", country=\"ALL\", types=False):\n",
    "    if form == \"XML\": # Use XML method\n",
    "        return get_xml_geolocation_data(address_string,form=\"XML\", country=\"ALL\", types=False)\n",
    "    else: # Use JSON method\n",
    "        return get_json_geolocation_data(address_string, form=\"JSON\", country=\"ALL\", types=False)\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [Root]",
   "language": "python",
   "name": "Python [Root]"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
