# -*- coding: utf-8 -*-
"""

Container for the UNHCR refugee data.

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
import numpy as np
import matplotlib.pyplot as plt

from countryCodeMapper import CountryCodeMapper
from utils import Settings, splitNA, plotWithNA



class UNHCRdata(Settings):
    
    def __init__(self, fname):
        super(UNHCRdata, self).__init__()

        self.fname = fname
        self.mapper = CountryCodeMapper()
        
        self.data = self._loadData(fname)
        
    
    def _loadData(self, fname):
        # The data contains non-number characters and will be loaded as string
        dtype = {"Year"                                     : np.int ,\
                 "Country / territory of asylum/residence"  : str    ,\
                 "Origin"                                   : str    ,\
                 "Refugees (incl. refugee-like situations)" : str    ,\
                 "Asylum-seekers (pending cases)"           : str    ,\
                 "Returned refugees"                        : str    ,\
                 "Internally displaced persons (IDPs)"      : str    ,\
                 "Returned IDPs"                            : str    ,\
                 "Stateless persons"                        : str    ,\
                 "Others of concern"                        : str    ,\
                 "Total Population"                         : str
                 }
        data = pd.read_csv(fname, skiprows=2, header=0, dtype=dtype)
        
        # Drop everything before 1980
        data = data[ (data["Year"]) >= 1980 ]
        
        # The UNHCR database contains redacted values marked by "*"
        # They note "A number of statistics are not shown in this system but 
        # are displayed as asterisks (*). These represent situations where the 
        # figures are being kept confidential to protect the anonymity of persons
        # of concern. Note that such figures are not included in any totals."
        data.replace("*", np.NaN, inplace=True)
        # Set the column type to float
        data["Refugees (incl. refugee-like situations)"] = data["Refugees (incl. refugee-like situations)"].astype(float)
        data["Asylum-seekers (pending cases)"]           = data["Asylum-seekers (pending cases)"].astype(float)
        data["Returned refugees"]                        = data["Returned refugees"].astype(float)
        data["Internally displaced persons (IDPs)"]      = data["Internally displaced persons (IDPs)"].astype(float)
        data["Returned IDPs"]                            = data["Returned IDPs"].astype(float)
        data["Stateless persons"]                        = data["Stateless persons"].astype(float)
        data["Others of concern"]                        = data["Others of concern"].astype(float)
        data["Total Population"]                         = data["Total Population"].astype(float)


        # The data contains countries that are not present in country mapper
        # or are not specified. We will subsume them as "Various/Unknown"
        
        # First we will take all destination countries that are not recognised
        # and create a single new entry for them.
        idx = self.mapper.convert( data["Country / territory of asylum/residence"] )
        idx = np.where( idx=="False" )[0] # I do not know why I have to compare it to the string "False"
        data.iloc[idx,1] = "Various/Unknown" # this overwrites the "Country / territory of asylum/residence"
                                             # columns of all rows with non understood countries.

        # In the next step we can group by the destination country and combine
        # the unknown origin countries into a single entry
        # We start by setting the entries that are not understood to "Various/Unknown"
        idx = self.mapper.convert( data["Origin"] )
        idx = np.where( idx=="False" )[0]
        data.iloc[idx,2] = "Various/Unknown"
        # Now group by destination and origin country and create aggregates
        data = data.groupby(["Year","Country / territory of asylum/residence", "Origin"]).agg([np.sum]).reset_index()
        data.reset_index()
        data.columns = data.columns.droplevel(1) # The columns names are multiindexes
                                                 # containing the information about the
                                                 # aggregation function used to collapse
                                                 # the rows. We need to drop that
                                                 # See: http://stackoverflow.com/a/22233719
        
        # Convert the country columns into the three letter country code
        data["Country / territory of asylum/residence"] = self.mapper.convert( data["Country / territory of asylum/residence"] )
        data["Origin"]                                  = self.mapper.convert( data["Origin"] )
        return data



    def show(self, destination_country=None, origin_country=None, year=None):
        """
        Plot summaries of the UNHCR data
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
        # Show the accumulated situation for country by destination
        tmpData = self._group("Country / territory of asylum/residence", destination_country)
        
        # Get the individual data
        x, Y = self._extract(tmpData)
        
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
        # Show the accumulated situation for country by origin
        tmpData = self._group("Origin", origin_country)
        
        # Get the individual data
        x, Y = self._extract(tmpData)
        
        # Create the figure
        xlimit = [int(min(x))-1, int(max(x))+1]
        ax = self._figure(origin_country, "everywhere", xlimit)
        
        # Now we need to split the data and add it to the axes
        self._plot(ax, x, Y)
        
        # Add the legend, remove duplicates. Since the plot is compsed piecewise,
        # there will be multiple instances of each line for the legend.
        self._legend(ax)
        return
    
    
    def _showCountryDirect(self, destination_country, origin_country):
        # Get the numbers for the rates between these two countries
        tmpData = self.data[ self.data["Country / territory of asylum/residence"] == destination_country ] 
        tmpData = tmpData[ tmpData["Origin"] == origin_country ]
        
        # Get the individual data
        x, Y = self._extract(tmpData)
        
        # Create the figure
        xlimit = [int(min(x))-1, int(max(x))+1]
        ax = self._figure(origin_country, destination_country, xlimit)
        
        # Now we need to split the data and add it to the axes
        self._plot(ax, x, Y)
        
        # Add the legend, remove duplicates. Since the plot is compsed piecewise,
        # there will be multiple instances of each line for the legend.
        self._legend(ax)
        
        
    
    def _showYear(self, year):
        pass

    def _group(self, column, country):
        tmpData = self.data[ self.data[column] == country ]
        del tmpData["Country / territory of asylum/residence"]
        del tmpData["Origin"]
        tmpData = tmpData.groupby(["Year"], sort=True).agg([np.sum]).reset_index()
        tmpData.columns = tmpData.columns.droplevel(1)
        return tmpData

    def _extract(self, dataFrame):
        x  = dataFrame["Year"]
        y1 = dataFrame["Refugees (incl. refugee-like situations)"]
        y2 = dataFrame["Asylum-seekers (pending cases)"]
        y3 = dataFrame["Returned refugees"]
        y4 = dataFrame["Internally displaced persons (IDPs)"]
        y5 = dataFrame["Returned IDPs"]
        y6 = dataFrame["Stateless persons"]
        y7 = dataFrame["Others of concern"]
        y8 = dataFrame["Total Population"]
        
        return x, (y1, y2, y3, y4, y5, y6, y7, y8)
        
    def _figure(self, origin_country, destination_country, xlimit):
        fig = plt.figure(figsize=self.singleFigureSize, dpi=self.dpi)
        ax  = fig.add_subplot(111)
        ax.set_title("Refugess from %s in %s" %(origin_country, destination_country), y=1.04)
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