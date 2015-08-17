# -*- coding: utf-8 -*-
"""

Container for the OECD migration data.

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
import zipfile

#from countryCodeMapper import CountryCodeMapper
#from utils import Settings, splitNA, plotWithNA
from migrationData import Migration


class OECDdata(Migration):
    
    def __init__(self, fname):
        super(OECDdata, self).__init__(fname)

#        self.fname = fname
#        self.mapper = CountryCodeMapper()

        self.destination_ID = "Country"
        self.origin_ID      = "Country of origin"
        
        self.data = self._loadData(fname)

    
    def _loadData(self, fname):
        # The data contains non-number characters and will be loaded as string
        dtype = {'"CO2"'                : str   ,\
                 "Country of origin"    : str   ,\
                 "VAR"                  : str   ,\
                 "Variable"             : str   ,\
                 "GEN"                  : str   ,\
                 "Gender"               : str   ,\
                 "COU"                  : str   ,\
                 "Country"              : str   ,\
                 "YEA"                  : int   ,\
                 "Year"                 : int   ,\
                 "Value"                : float ,\
                 "Flag Codes"           : str   ,\
                 "Flags"                : str
                 }
        
        assert( zipfile.is_zipfile(fname) ) # sanity check
        with zipfile.ZipFile(fname, "r") as f:
            data = pd.read_csv(f.open(f.namelist()[0]), dtype=dtype)

        # The Flags columns only has two values, {'Break', 'Estimated value'}
        # I do not know what these mean and prefer to remove them for now.
        data = data[ data["Flags"].isnull() ]
        
        # We will drop some columns and reorder them. Then we can "pivot" the table.
        # This will take the "Variable" column, take it as an index for new
        # columns, and will put the "Value" entry as value in its place.
        data = data[["Year", "Country", "Country of origin", "Variable", "Value"]]
        data = data.pivot_table(index=["Year", "Country", "Country of origin"],\
                                columns="Variable",\
                                values="Value"
                               )
        data.reset_index(inplace=True)
        
        # Convert the country columns into the three letter country code
        data["Country"]           = self.mapper.convert( data["Country"] )
        data["Country of origin"] = self.mapper.convert( data["Country of origin"] )
        
        return data

    def _extract(self, dataFrame):
        x  = dataFrame["Year"]
        y1 = dataFrame["Acquisition of nationality by country of former nationality"]
        y2 = dataFrame["Inflows of asylum seekers by nationality"]
        y3 = dataFrame["Inflows of foreign population by nationality"]
        y4 = dataFrame["Inflows of foreign workers by nationality"]
        y5 = dataFrame["Inflows of seasonal foreign workers by nationality"]
        y6 = dataFrame["Outflows of foreign population by nationality"]
        y7 = dataFrame["Stock of foreign labour by nationality"]
        y8 = dataFrame["Stock of foreign population by nationality"]
        y9 = dataFrame["Stock of foreign-born labour by country of birth"]
        y10 = dataFrame["Stock of foreign-born population by country of birth"]
        
        return x, (y1, y2, y3, y4, y5, y6, y7, y8, y9, y10)

















