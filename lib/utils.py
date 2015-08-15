# -*- coding: utf-8 -*-
"""

Utility functions for the newspaper article scrape.

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
import matplotlib as mpl
from operator import itemgetter
from pandas   import DataFrame

from countryCodeMapper import CountryCodeMapper


class CountryContainer(object):
    """
    Container object for Country() objects. Used to sort and save the data
    contained in the Country() objects in a concise manner.
    """
    
    def __init__(self):
        self.data = list()

    def __call__(self, country):
        self.data.append( (country, country.year) )
    
    def save(self, fname):
        """
        Save the country mentions to disk (comma separated).
        
        Input:
          fname (str):  Filename of the output file
          
        """
        # Sort for ascending years
        self.data = sorted(self.data, key=itemgetter(1))
        
        # Construct a dict of the countries and years
        dataFrame = DataFrame.from_dict( [ country.averageCount() for country, _ in self.data ], )

        # Save to disk
        dataFrame.to_csv(fname)
        

class Country(object):
    """
    Container for counting country mentions (as taken from the newspaper queries)
    """
    
    def __init__(self, year=None):
        
        self.mapper       = CountryCodeMapper()
        self.countryCount = dict()
        self.counter      = dict()
        self.block        = False
        self.year         = year
        
    
    def __call__(self, country, count, force=False):
        """
        Increase the country counter by count. Blocks if the output was
        already generated.
        """
        if self.block and not force:
            print("The counter is blocked. If you know what you are doing,\n" + \
                  "use force=True to add regardless.")
            return
            
        # Add the article count
        country = self.mapper(country)
        if country:
            if country in self.countryCount:
                self.countryCount[country] += count
            else:
                self.countryCount[country]  = count
            
            # Keep track of how many times we added to take the average
            self.counter.setdefault(self.mapper(country), list()).append(1)
        else:
            print("Country name %s not recognised!" %country)

    def averageCount(self):
        """
        Calculate the average count for each country. I.e. each country synonym
        is taken as equally likely and relevant and the average count returned
        from each query is returned.
        """
        self.block = True # block adding new values
        for country, N in self.counter.items():
            self.countryCount[country] /= len(N)
        
        # Add a year column (needed for saving to csv)
        self.countryCount["YEAR"] = self.year
        
        return self.countryCount
        

class Settings(object):
    """ Container for commonly used settings """
    
    def __init__(self):

        # Thanks to: http://stackoverflow.com/a/3900167        
        font = {'family' : 'serif',
                'size'   : 14}

        mpl.rc('font', **font)
        
        self.singleFigureSize = (10,8)
        self.dpi              = 120
        self.axisLabelSize    = 16
        self.colors           = ['blue', 'green', 'red', 'cyan', 'magenta', \
                                 'black', ]