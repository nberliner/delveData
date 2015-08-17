# -*- coding: utf-8 -*-
"""

Container for the migration data. Individual datasets can subclass
the base class Migration.

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
import numpy as np
import matplotlib.pyplot as plt

from countryCodeMapper import CountryCodeMapper
from utils import Settings, splitNA, plotWithNA


class Migration(Settings):
    
    def __init__(self, fname):
        super(Migration, self).__init__()
    
        self.fname  = fname
        self.mapper = CountryCodeMapper()
        
        self.destination_ID     = None
        self.origin_ID          = None

    def _loadData(self, fname):
        raise NotImplementedError

    def show(self, destination_country=None, origin_country=None, year=None):
        """
        Plot summaries of the migration data
        """
        # Check if input is given
        if (destination_country is not None or origin_country is not None) and year is not None:
            print("You can either specify the countries or the year. Not both.")
            return
        elif destination_country is None and origin_country is None and year is None:
            print("You must either specify the countries or the year.")
            return
        
        # Convert the country to three letter country code
        if destination_country is not None and self.mapper(destination_country):
            destination_country = self.mapper(destination_country)
        elif destination_country is None:
            pass
        else:
            print("Destination country not understood.")
            return
        if origin_country is not None and self.mapper(origin_country):
            origin_country = self.mapper(origin_country)
        elif origin_country is None:
            pass
        else:
            print("Origin country not understood.")
            return
        
        # Plot the requested type
        if destination_country is not None or origin_country is not None:
            self._showCountry(destination_country, origin_country)
        else:
            self._showYear(year)


    def _showCountry(self, destination_country, origin_country):
        # Get the data
        if destination_country is not None and origin_country is not None:
            self._showCountryDirect(destination_country, origin_country)
        elif origin_country is None:
            self._showCountryByDestination(destination_country)
        elif destination_country is None:
            self._showCountryByOrigin(origin_country)
    
    def _showCountryByDestination(self, destination_country):
        assert( self.destination_ID is not None )
        # Show the accumulated situation for country by destination
        tmpData = self._group(self.destination_ID, destination_country)
        
        # Get the individual data
        x, Y = self._extract(tmpData)
        if len(x) == 0:
            print("No data to plot")
            return
        
        # Create the figure
        xlimit = [int(min(x))-1, int(max(x))+1]
        ax = self._figure("everywhere", destination_country, xlimit)
        
        # Now we need to split the data and add it to the axes
        self._plot(ax, x, Y)
        
        # Add the legend, remove duplicates. Since the plot is compsed piecewise,
        # there will be multiple instances of each line for the legend.
        self._legend(ax)
        return
    
    def _showCountryByOrigin(self, origin_country):
        assert( self.origin_ID is not None )
        # Show the accumulated situation for country by origin
        tmpData = self._group(self.origin_ID, origin_country)
        
        # Get the individual data
        x, Y = self._extract(tmpData)
        if len(x) == 0:
            print("No data to plot")
            return
        
        # Create the figure
        xlimit = [int(min(x))-1, int(max(x))+1]
        ax = self._figure(origin_country, "everywhere", xlimit)
        
        # Now we need to split the data and add it to the axes
        self._plot(ax, x, Y)
        
        # Add the legend, remove duplicates. Since the plot is composed piecewise,
        # there will be multiple instances of each line for the legend.
        self._legend(ax)
        return

    def _showCountryDirect(self, destination_country, origin_country):
        assert( self.destination_ID is not None )
        assert( self.origin_ID      is not None )
        # Get the numbers for the rates between these two countries
        tmpData = self.data[ self.data[self.destination_ID] == destination_country ] 
        tmpData = tmpData[ tmpData[self.origin_ID] == origin_country ]
        
        # Get the individual data
        x, Y = self._extract(tmpData)
        if len(x) == 0:
            print("No data to plot")
            return
        
        # Create the figure
        xlimit = [int(min(x))-1, int(max(x))+1]
        ax = self._figure(origin_country, destination_country, xlimit)
        
        # Now we need to split the data and add it to the axes
        self._plot(ax, x, Y)
        
        # Add the legend, remove duplicates. Since the plot is compsed piecewise,
        # there will be multiple instances of each line for the legend.
        self._legend(ax)
        return

    def _group(self, column, country):
        assert( self.destination_ID is not None )
        assert( self.origin_ID      is not None )

        tmpData = self.data[ self.data[column] == country ]
        del tmpData[self.destination_ID]
        del tmpData[self.origin_ID]
        tmpData = tmpData.groupby(["Year"], sort=True).agg([np.sum]).reset_index()
        tmpData.columns = tmpData.columns.droplevel(1)
        return tmpData

    def _extract(self, dataFrame):
        raise NotImplementedError
    
    def _figure(self, origin_country, destination_country, xlimit):
        fig = plt.figure(figsize=self.singleFigureSize, dpi=self.dpi)
        ax  = fig.add_subplot(111)
        ax.set_title("Migration from %s to %s" %(origin_country, destination_country), y=1.04)
        ax.set_xlabel("Year", fontsize=self.axisLabelSize)
        ax.set_ylabel("Indicator", fontsize=self.axisLabelSize)
        ax.set_xlim( xlimit )
        return ax

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

    def _legend(self, ax):
        _handles, _labels = ax.get_legend_handles_labels()
        labels  = list(set(_labels))
        handles = [ _handles[_labels.index(item)] for item in labels ]
        ax.legend(handles, labels, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        return











