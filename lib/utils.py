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
import csv
import numpy as np
import pandas as pd
import matplotlib as mpl
from operator import itemgetter

from countryCodeMapper import CountryCodeMapper



def splitNA(x, y):
    """
    Divide discontinous data, i.e. pandas Series or numpy arrays containing
    missing values into chunks.
    
    The purpose of this is to be able to plot the data including a visual
    representation of the "gaps". Each returned chunk can be checked for NaN
    and can thus be identified as "gap" or continues data.
    
    Input:
      x (pd.Series or np.array): The x values of the input data
      
      y (pd.Series or np.array): The y values of the input data
     
    Output:
      X_subset (list):  List containing the chunks for x
      
      Y_subset (list):  List containing the chunks for y
    
    """
    
    X_subset, Y_subset = list(), list()

    idx = np.where( pd.notnull(y) )[0] # get the indexes with values
                                       # we are only interested in the
                                       # first dimension.
    for i in range(1,len(idx)):
        chunksY = y[ idx[i-1]:idx[i]+1 ] # These are the chunks of data
                                         # that can be used to plot the data
                                         # using lines or dots depending
                                         # on NA values.
        chunksX = x[ idx[i-1]:idx[i]+1 ]
        
        X_subset.append( chunksX )
        Y_subset.append( chunksY )
    
    return X_subset, Y_subset
        

def plotWithNA(X_subset, Y_subset, ax, label, color, linestyle):
    """
    Add the divided entries in *_subset to ax.
    
    Data containing mising values will be plotted with dashed lines connecting
    the points adjacent to the missing values. The data will be added directly
    to the ax handle.
    
    Input:
      X_subset (list):  List output from splitNA()
      
      Y_subset (list):  List output from splitNA()
      
      ax (ax object):   Axes to which the plot will be added to
      
      label (str):      Label for the plot legend
      
      color (str):      Linecolor to be used
      
    """
    for x_subset, y_subset in zip(X_subset, Y_subset):
        if np.any(pd.isnull(Y_subset)):
            x_subset = x_subset[ pd.notnull(y_subset) ]
            y_subset = y_subset.dropna()
            ax.plot(x_subset.dropna(), y_subset.dropna(), label=label, color=color, linestyle="dotted", marker="o")
        else:
            ax.plot(x_subset, y_subset, label=label, color=color, linestyle=linestyle)
    return ax


class DoubleDict(dict):
    """
    Dictionary class that allows easy adding of pairs of values. Each value
    will become key and value respectively. This allows easy mapping one to
    the other, i.e. conversion.
    """
    def __init__(self, *args):
        super(DoubleDict, self).__init__(args)

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        dict.__setitem__(self, val, key)
        
        
class CountryContainer(object):
    """
    Container object for Country() objects. Used to sort and save the data
    contained in the Country() objects in a concise manner.
    """
    
    def __init__(self):
        self.data = list()

    def __call__(self, country):
        self.data.append( (country, country.year) )
    
    def save(self, fname, count="max"):
        """
        Save the country mentions to disk (comma separated).
        
        Input:
          fname (str):  Filename of the output file
          
        """
        # Sort for ascending years
        self.data = sorted(self.data, key=itemgetter(1))
        
        # Construct a dict of the countries and years
        if count == "avg":
            dataFrame = pd.DataFrame.from_dict( [ country.averageCount() for country, _ in self.data ], )
        elif count == "max":
            dataFrame = pd.DataFrame.from_dict( [ country.maxCount() for country, _ in self.data ], )
        else:
            print("Sorry, it was not understood which accumulation (count) should be done")
            return
            
        # Save to disk
        dataFrame.to_csv(fname)
        return
        

class Country(object):
    """
    Container for counting country mentions (as taken from the newspaper queries)
    """
    
    def __init__(self, year=None):
        
        self.mapper       = CountryCodeMapper()
        self.data         = dict()
        self.countryCount = None
        self.counter      = dict()
        self.block        = False
        self.maximum      = False
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
        
        assert( country not in self.data )
        self.data[country] = count
        return
    
    def aggregate(self, maximum=True):
        """
        Convert the article count of each search query into one aggregate count.
        
        Possible options are to take the maximal returned value (default) or
        to take the average of the returned values for each country.
        
        Input:
          maximum (bool):  Take the maximum or the average
          
        """
        self.countryCount = dict()
        for country, count in self.data.items():
            # Add the article count
            country = self.mapper(country)
            if country: # was the country understood
                if maximum: # should only the max count be calculated
                    self.maximum = True
                    if country in self.countryCount:
                        if count > self.countryCount[country]:
                            self.countryCount[country]  = count
                    else:
                        self.countryCount[country]  = count
                else: # no, just add everything up
                    if country in self.countryCount:
                        self.countryCount[country] += count
                    else:
                        self.countryCount[country]  = count
                
                # Keep track of how many times we added to take the average
                self.counter.setdefault(self.mapper(country), list()).append(1)
            else:
                print("Country name %s not recognised!" %country)
        return

    def averageCount(self):
        """
        Calculate the average count for each country. I.e. each country synonym
        is taken as equally likely and relevant and the average count returned
        from each query is returned.
        """
        self.block = True # block adding new values
        
        if self.countryCount is None:
            self.aggregate(maximum=False)
        
        for country, N in self.counter.items():
            self.countryCount[country] /= len(N)
        
        # Add a year column (needed for saving to csv)
        self.countryCount["YEAR"] = self.year
        
        return self.countryCount
    
    def maxCount(self):
        """
        Calculate the maximum count for each country. I.e. only one country
        is taken as representative and relevant. This will most likely be a
        good choice if countries have one commonly used name but multiple
        "official" names.
        """
        self.block = True # block adding new values
        
        if self.countryCount is None:
            self.aggregate(maximum=True)

        # The count must already be specified as maximum
        assert( self.maximum )
        
        # Add a year column (needed for saving to csv)
        self.countryCount["YEAR"] = self.year
        
        return self.countryCount
    
    def save(self, fname):
        # credit goes here: http://stackoverflow.com/a/10373268
        with open(fname, 'w') as f:
            w = csv.DictWriter(f, self.data.keys())
            w.writeheader()
            w.writerow(self.data)
        return
        

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
        self.linestyle        = ["solid", "dashed"]
    
    def line(self, idx):
        i = 0
        while len(self.colors)-1 < idx:
            i   += 1
            idx -= len(self.colors)

        assert( i <= len(self.linestyle) )
        return self.colors[idx], self.linestyle[i]





