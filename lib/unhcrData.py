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

from migrationData import Migration



class UNHCRdata(Migration):
    
    def __init__(self, fname):
        super(UNHCRdata, self).__init__(fname)

        self.destination_ID = "Country"
        self.origin_ID      = "Origin"
        
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

        # Set the column names; rename "Country / territory of asylum/residence" to "Country"
        index = ["Year","Country"]
        index.extend(data.columns[2:])
        data.columns = index

        # The data contains countries that are not present in country mapper
        # or are not specified. We will subsume them as "Various/Unknown"
        
        # First we will take all destination countries that are not recognised
        # and create a single new entry for them.
        idx = self.mapper.convert( data["Country"] )
        idx = np.where( idx=="False" )[0] # I do not know why I have to compare it to the string "False"
        data.iloc[idx,1] = "Various/Unknown" # this overwrites the "Country"
                                             # columns of all rows with non understood countries.

        # In the next step we can group by the destination country and combine
        # the unknown origin countries into a single entry
        # We start by setting the entries that are not understood to "Various/Unknown"
        idx = self.mapper.convert( data["Origin"] )
        idx = np.where( idx=="False" )[0]
        data.iloc[idx,2] = "Various/Unknown"
        # Now group by destination and origin country and create aggregates
        data = data.groupby(["Year","Country", "Origin"]).agg([np.sum]).reset_index()
        data.reset_index()
        data.columns = data.columns.droplevel(1) # The columns names are multiindexes
                                                 # containing the information about the
                                                 # aggregation function used to collapse
                                                 # the rows. We need to drop that
                                                 # See: http://stackoverflow.com/a/22233719
        
        # Convert the country columns into the three letter country code
        data["Country"] = self.mapper.convert( data["Country"] )
        data["Origin"]  = self.mapper.convert( data["Origin"] )
        return data


    def _showYear(self, year):
        pass


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
        
