# -*- coding: utf-8 -*-
"""

Estimate the international "visibility" of countries by retrieving the
average number of articles the New York Times returns in its search query.
For each year and each country, a query is send to the NYT api and the
number of returned hits (i.e. articles) is taken as estimate for the
international "visibility". To ensure optimal coverage, for each country
synonyms have been defined (see CountryCodeMapper.py) and the average of
the count is taken.

----

Copyright (C) 2015  Niklas Berliner

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
import sys
import os
import pickle
from time import sleep

from countryCodeMapper import CountryCodeMapper
from utils             import Country, CountryContainer

from nytimesarticles   import articleAPI, DeveloperOverRate
api = articleAPI('/* Your API access key here */')

# Use tmp folder to keep intermediate results. Final output will be placed there as well
tmpFolder = "../data/newspaper/raw/"

## Read the temporary folder content
done = [ int(fname[8:-2]) for fname in os.listdir(tmpFolder) if fname != "country_aggregate.p" ]

# Initialise some variables
C = CountryCodeMapper()
countries = C.countryNames()
container = CountryContainer()

# Run the scrape for the years 1980 to 2014 (including)
dates = range(1980,2015)
for date in dates:
    if date in done:
        print("Loading year", date)
        a = pickle.load(open(tmpFolder + "country_%s.p" %str(date), "rb"))
    else:
        print("Processing year", date)
        a = Country(date)
        for idx, country in enumerate(countries):
            success = False
            i = 0
            while i<=3 and not success:
                try:
                    query = api.search( q = country, 
                                        begin_date = str(date) + '0101',
                                        end_date = str(date) + '1231'
                                       )
                    sleep(.1)
                    assert( query["status"] == "OK" )
                    count = query["response"]["meta"]["hits"]
                    a(country, count)
                    i += 1
                    success = True
                except DeveloperOverRate:
                    print("You most probably exceeded you api key limit\n")
                    sys.exit()
                except:
                    success = False
                    i += 1
                    sleep(1) # allow the server some quiet time
            
            if not success:
                print("Error in %s, %s" %(date, country))
        
        # Store the year as pickle in case something breaks during the run
        pickle.dump(a, open(tmpFolder + "country_%s.p" %str(date), "wb"))
        
        # Save the original data as csv file
        a.save(tmpFolder + "country_%s.csv" %str(date))
    
    # Add the country to the container
    container(a)

pickle.dump(container, open(tmpFolder + "country_aggregate.p", "wb"))

# Save everything to a csv file. The columns will be the countries, the rows
# will be the years. One column contains the years (sanity check to ensure
# that the row order is not messed up).
container.save(tmpFolder + "/NYT_scrape.csv")









