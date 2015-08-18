# -*- coding: utf-8 -*-
"""

Container for the country mentions from the newspaper scrape.

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
import pandas as pd
import os.path as osp
import matplotlib.pyplot as plt
from utils import Settings, splitNA, plotWithNA
from countryCodeMapper import CountryCodeMapper

class NewspaperData(Settings):
    
    def __init__(self):
        super(NewspaperData, self).__init__()
        
        self.data    = None
        self.mapper  = CountryCodeMapper()
        self.columns = list()

    def add(self, fname):
        # Extract the newspaper name
        name = osp.split(fname)[1].split('_')[0]
        self.columns.append(name)
        
        # Load the data and merge it with existing (if applicable)
        data = self._loadData(fname, name)
        if self.data is None:
            self.data = data
        else:
            self.data = pd.merge(self.data, data, how='left', on=['YEAR','Country'])
        
    def _loadData(self, fname, name):
        
        data = pd.read_csv(fname, header=0)
        del data[data.columns[0]] # delete the row numbers

        # Melt the dataframe to to make it compatible with the other data
        data = pd.melt(data, id_vars=["YEAR"], var_name="Country", value_name=("Mentions_%s" %name) )
        
        return data

    
    def show(self, country):
        if not self.mapper(country):
            print("Sorry. Country %s not understood" %country)
            return
            
        country = self.mapper(country)
        data = self.data[ self.data["Country"] == country ]
        
        x, Y = self._extract(data)
        if len(x) == 0:
            print("No data to plot")
            return
        
        # Create the figure
        xlimit = [int(min(x))-1, int(max(x))+1]
        
        ax = self._figure(country, xlimit)
        self._plot(ax, x, Y)
        

    def _figure(self, country, xlimit):
        fig = plt.figure(figsize=self.singleFigureSize, dpi=self.dpi)
        ax  = fig.add_subplot(111)
        ax.set_title("Number of search results for %s" %country, y=1.04)
        ax.set_xlabel("Year", fontsize=self.axisLabelSize)
        ax.set_ylabel("Occurences", fontsize=self.axisLabelSize)
        ax.set_xlim( xlimit )
        return ax

    def _extract(self, data):
        x = data["YEAR"]
        Y = [ data["Mentions_%s" %name] for name in self.columns ]
        return x, Y

    def _plot(self, ax, x, Y):
        
        if len(x) == 0:
            print("No data to plot")
            return
            
        count = 0 # This keeps track of "unused" colors
        for idx, y in enumerate(Y):
            # Split the data into subsets (if needed)
            X_subset, Y_subset = splitNA(x, y)
          
            # Get the color and linestyle
            if len(Y_subset) == 0: # nothing to plot
                count += 1
            color, linetype = self.line(idx-count)
            
            # Plot the data
            plotWithNA(X_subset, Y_subset, ax, y.name, color, linetype)
        return














