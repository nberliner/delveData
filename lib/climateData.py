# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 16:51:07 2015

@author: niklas
"""
from utils import DoubleDict
from geopy.geocoders import Nominatim
import pandas as pd
from time import sleep
import numpy as np
import tempfile
import tarfile
import os
import shutil
from datetime import datetime

class WeatherData(object):
    
    def __init__(self, fname="../data/climate/ghcnd_gsn.tar.gz"               ,\
                       years=None                                             ,\
                       stationList="../data/climate/ghcnd-stations.txt"       ,\
                       LatLon2Counry="../data/geolocation/LatLon2Country.csv" ,\
                       optimiseFactor = False
                ):
        """
        Load all the climate data published at: See: ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/
        
        The daily climate data is extracted and converted into a severity
        index based on the average measurement at each months. The index can
        range from 0 to 12 depending on how many months of one year were
        classified as extreme.
        
        Please also refer to notebooks/
        
        Input:
        
          fname (str):           Location of the input database, i.e. ghcnd_gsn.tar.gz
          
          years (list):          List of two integers specifing the year range that
                                 should be kept.
        
          stationList (str):     Location of the station list file, i.e. ghcnd-stations.txt
          
          LatLon2Contry (str):   Location of the latitude, longitude to country
                                 mapper file, i.e. LatLon2Country.csv
        
          optimiseFactor (bool): Only needed to set the optimal threshold for
                                 classifing climate events as extreme. See
                                 notebooks for more detail.
        """
        self.fname  = fname
        self.mapper = WeatherStationMapper(stationList, LatLon2Counry)
        
        if years is None:
            years = [1800, 2100]
        
        # Check if the data is created from scratch or a precompiled copy
        # can be read in.
        startTime = datetime.now() # set the calculation start time
        
        if os.path.isfile("../data/climate/ghcnd_gsn.csv"):
            print("Loading the data from prebuild source..")
            if optimiseFactor:
                print("Not rebuilding the data. Cannot give you the full DataFrame.")
            self.data = pd.DataFrame.from_csv("../data/climate/ghcnd_gsn.csv")
            self.data.reset_index(inplace=True)
        else:
            print("Generating the data from the original data..")
            self.stations = self._loadTar(fname, years)
            self.data     = self._combine(self.stations, optimiseFactor)
            self.data.to_csv(fname[:-6]+"csv", index=False)
        
        # We're done with clustering, print some interesting messages
        time = datetime.now()-startTime
        print("Finished loading the data:", str(time)[:-7])
    
    def __iter__(self):
        for item in self.stations:
            yield item
    
    def _loadTar(self, fname, years):
        """
        Extract the database into a temporary folder and read the data.
        """
        # Generate a temp folder in which the climate data will be extracted
        tmpPath = tempfile.mkdtemp()
        
        stations = list()
        try:
            # Extract the tar file
            with tarfile.open(fname, 'r') as tar:
                tar.extractall(tmpPath)
            
            # Read the stations
            for fname in os.listdir(tmpPath + "/ghcnd_gsn"):
                stationID = os.path.split(fname)[1].split('.')[0]
                country = self.mapper(stationID) # map the station to its country

                stations.append(WeatherStation(tmpPath + "/ghcnd_gsn/" + fname, years, country))
        finally:
            shutil.rmtree(tmpPath) # make sure the tmp folder is deleted
        return stations

    def _combine(self, stations, optimiseFactor=False):
        """
        Take the data from all weather stations and combine it in one DataFrame.
        
        Climate data from the database is used if the weather station existed
        for a period long enough to allow reliable measurements for the purpose
        of this project. Each station is mapped to its country to allow the
        integration with the already existing data.
        The raw data provides daily climate measurements and these measurements
        are transformed into a severity index for each year. For each months
        the average of the measurements is taken and compared to the measurements
        of the previous months of the same station. If the average deviates by
        more than 1.54 from standart deviations this months will be classified
        as extreme. Each year is thus assigned a value between 0 and 12,
        depending on how many months of that year were identified as being
        extreme.
        """
        data = pd.concat( [ station.data for station in stations ] )
        data = self._collapse(data, optimiseFactor)
        return data

    def _collapse(self, dataFrame, optimiseFactor=False):
        """
        Collapse the dataFrame. (See _combine())
        """
        def df_entry(stationID, element, month, year, value, \
                     thisYear, lastYearAvg, lastYearStd):
            country = self.mapper(stationID)
            return( { "Country"       : country   ,\
                      "Element"       : element   ,\
                      "Month"         : month     ,\
                      "Year"          : year      ,\
                      "Value"         : value     ,\
                      "_ThisYear"     : thisYear  ,\
                      "_LastYearsAvg" : lastYearAvg ,\
                      "_LastYearsStd" : lastYearStd ,\
                     }
                   )
        
        def remove(column, dataFrame=None):
            """
            Remove the column from DataFrame if existent.
            
            Input:
              column (str):          Column name to be removed
              
              dataFrame (DataFrame): DataFrame from which column shoudl be removed
            """
            try:
                if dataFrame is None:
                    del grouped[column]
                else:
                    del dataFrame[column]
            except KeyError:
                pass
                
        def getStatistics(subdf):
            """
            Classify each month to be either extreme or normal based on the
            deviation from the average.            
            """
            # Sanity checks
            stationID = subdf["Station ID"].unique()
            assert( len(stationID) == 1 )
            stationID = stationID[0]

            newData = list()
            # Do for each element
            for element in ["PRCP", "SNOW", "SNWD", "TMAX", "TMIN", "AWND"]:
                df = subdf[ subdf["Element"] == element ]
                df = df.sort(columns=["Year"])
                
                # Only take stations that exist long enough and still are existent
                if np.min(df["Year"]) > 1950 or np.max(df["Year"]) < 2013:
                    continue
                
                # Check for each month if it is extreme
                for month, group in df.groupby(["Month"]):
                    years     = set(group["Year"])
                    firstYear = np.min(list(years))
                    for year in years:
                        
                        if year == firstYear: # ignore fist years
                            newData.append( df_entry(stationID, element, month, year, 0, -9999, -9999, -9999) )
                        else:
                            lastYears = group[ group["Year"] <  year ]["Value"]
                            thisYear  = group[ group["Year"] == year ]["Value"]

                            thisYearAvg  = np.average(thisYear)
                            lastYearsAvg = np.average(lastYears)
                            lastYearsStd = np.std(lastYears)
                            factor       = 1.54 # see noteboks for more info
                            
                            # Classify as extreme or not
                            if thisYearAvg > lastYearsAvg + factor*lastYearsStd or \
                               thisYearAvg < lastYearsAvg - factor*lastYearsStd:
                                newData.append( df_entry(stationID, element, month, year, 1, thisYearAvg, lastYearsAvg, lastYearsStd) )
                            else:
                                newData.append( df_entry(stationID, element, month, year, 0, thisYearAvg, lastYearsAvg, lastYearsStd) )
            
            # Create a new DataFrame
            newDataFrame = pd.DataFrame.from_dict(newData, orient="columns")
            return newDataFrame
                    
        # End of functions definitions, group and apply
        remove("Country", dataFrame)
        grouped = dataFrame.groupby(["Station ID"]).apply(getStatistics)
        grouped.reset_index(inplace=True)
        
        # If in manual optimise step omit the collapsing of the DataFrame
        if optimiseFactor:
            return grouped
        
        # Take the average of the stations for each month
        remove("level_1")
        remove("Station ID")
        grouped = grouped.groupby(["Country","Element","Year","Month"]).agg( lambda x: np.round(np.average(x)) )
        grouped.reset_index(inplace=True)
        
        # Now we have a table containing a flag (i.e. 1) if an extreme weather
        # event occured.
        remove("level_1")
        remove("Month")
        grouped = grouped.groupby(["Country","Element","Year"]).agg(sum)
        grouped.reset_index(inplace=True)
        
        # Pivot the table so that the "Element" entries are columns and 
        # remove the early weather events.
        result = grouped.pivot_table(index=["Country","Year"], columns="Element", values="Value")
        result.reset_index(inplace=True)
        result = result[ result["Year"] >= 1980 ]

        return result


class LatLon2Country(dict):
    
    def __init__(self, fname, *args):
        """
        Map latitude and longitude information of the weather stations to
        their country of origin.
        
        It is a dictionary that loads the values upon initialisation.
        """
        super(LatLon2Country, self).__init__(args)
        
        self._loadData(fname)

    def _loadData(self, fname):
        with open(fname, 'r') as f:
            header = f.readline()
            assert( header.strip() == "Country,Latitude,Longitude" )
            for l in f:
                line = l.strip().split(',')
                country = line[0]
                lat     = line[1]
                lon     = line[2]
            
                self.__setitem__((lat,lon), country)


class WeatherStation(object):
    
    def __init__(self, fname, years, country):
        """
        Read the climate information from weather stations published by NOAA
        
        See: ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/
        
        
        """
        
        self.stationID  = None
        self.years      = years
        self.country    = country
        
        self.data       = self._load(fname, years)
    
    def __repr__(self):
        return "WeatherStation Object: Station: %r; Country: %r; Years: %r" %(self.stationID, self.country, self.years)

    def _load(self, fname, years):
        """
        Read the climate data from the NOAA and store it in a pandas DataFrame
        """
        yearRange = range(years[0],years[1]+1)
        
        count = 0
        data = list()
        with open(fname, 'r') as f:
            for line in f:
                self.stationID, year, month, element, value = self._readline(line)
                
                # Check if we want to keep the reading
                if year not in yearRange:
                    continue
                if element not in ["PRCP", "SNOW", "SNWD", "TMAX", "TMIN", "AWND"]:
                    continue
                if value is None:
                    count += 1
                    continue
   
                data.append( {"Station ID": self.stationID ,\
                              "Country"   : self.country   ,\
                              "Year"      : year           ,\
                              "Month"     : month          ,\
                              "Element"   : element        ,\
                              "Value"     : float(value)   ,\
                              }
                            )
        
        if len(data) == 0:
            data.append( {"Station ID": self.stationID ,\
                          "Country"   : self.country   ,\
                          "Year"      : year           ,\
                          "Month"     : month          ,\
                          "Element"   : element        ,\
                          "Value"     : np.NaN   ,\
                          }
                        )
        
        data = pd.DataFrame.from_dict(data) # put everything into a DataFrame
        return data
        
    
    def _readline(self, line):
        """
        Read the weather station data. Please also refer to the readme in
        the data/climate folder.
        """
        stationID   = line[:11].strip()
        year        = int(line[11:15].strip())
        month       = int(line[15:17].strip())
        element     = line[17:21].strip()
        value_day1  = line[21:26].strip()
        qflag_day1  = line[27:28].strip()
        value_day2  = line[29:34].strip()
        qflag_day2  = line[35:36].strip()
        value_day3  = line[37:42].strip()
        qflag_day3  = line[43:44].strip()
        value_day4  = line[45:50].strip()
        qflag_day4  = line[53:54].strip()
        value_day5  = line[53:58].strip()
        qflag_day5  = line[59:60].strip()
        value_day6  = line[61:66].strip()
        qflag_day6  = line[69:68].strip()
        value_day7  = line[69:74].strip()
        qflag_day7  = line[77:76].strip()
        value_day8  = line[77:82].strip()
        qflag_day8  = line[83:84].strip()
        value_day9  = line[85:90].strip()
        qflag_day9  = line[91:92].strip()
        value_day10 = line[93:98].strip()
        qflag_day10 = line[99:100].strip()
        value_day11 = line[101:106].strip()
        qflag_day11 = line[107:108].strip()
        value_day12 = line[109:114].strip()
        qflag_day12 = line[115:116].strip()
        value_day13 = line[117:122].strip()
        qflag_day13 = line[123:124].strip()
        value_day14 = line[125:130].strip()
        qflag_day14 = line[131:132].strip()
        value_day15 = line[133:138].strip()
        qflag_day15 = line[139:140].strip()
        value_day16 = line[141:146].strip()
        qflag_day16 = line[147:148].strip()
        value_day17 = line[149:154].strip()
        qflag_day17 = line[155:156].strip()
        value_day18 = line[157:162].strip()
        qflag_day18 = line[163:164].strip()
        value_day19 = line[165:170].strip()
        qflag_day19 = line[171:172].strip()
        value_day20 = line[173:178].strip()
        qflag_day20 = line[179:180].strip()
        value_day21 = line[181:186].strip()
        qflag_day21 = line[187:188].strip()
        value_day22 = line[189:194].strip()
        qflag_day22 = line[195:196].strip()
        value_day23 = line[197:202].strip()
        qflag_day23 = line[203:204].strip()
        value_day24 = line[205:210].strip()
        qflag_day24 = line[211:212].strip()
        value_day25 = line[213:218].strip()
        qflag_day25 = line[219:220].strip()
        value_day26 = line[221:226].strip()
        qflag_day26 = line[227:228].strip()
        value_day27 = line[229:234].strip()
        qflag_day27 = line[235:236].strip()
        value_day28 = line[237:242].strip()
        qflag_day28 = line[243:244].strip()
        value_day29 = line[245:250].strip()
        qflag_day29 = line[251:252].strip()
        value_day30 = line[253:258].strip()
        qflag_day30 = line[259:260].strip()
        value_day31 = line[261:266].strip()
        qflag_day31 = line[267:268].strip()
        
        values = [value_day1, value_day2, value_day3, value_day4     ,\
                  value_day5, value_day6, value_day7, value_day8     ,\
                  value_day9, value_day10, value_day11, value_day12  ,\
                  value_day13, value_day14, value_day15, value_day16 ,\
                  value_day17, value_day18, value_day19, value_day20 ,\
                  value_day21, value_day22, value_day23, value_day24 ,\
                  value_day25, value_day26, value_day27, value_day28 ,\
                  value_day29, value_day30, value_day31              ,\
                  ]
        
        qflags = [qflag_day1, qflag_day2, qflag_day3, qflag_day4, qflag_day5      ,\
                  qflag_day6, qflag_day7, qflag_day8, qflag_day9, qflag_day10     ,\
                  qflag_day11, qflag_day12, qflag_day13, qflag_day14, qflag_day15 ,\
                  qflag_day16, qflag_day17, qflag_day18, qflag_day19, qflag_day20 ,\
                  qflag_day21, qflag_day22, qflag_day23, qflag_day24, qflag_day25 ,\
                  qflag_day26, qflag_day27, qflag_day28, qflag_day29, qflag_day30 ,\
                  qflag_day31                                                     ,\
                 ]
        
        assert( len(values) == len(qflags) ) # sanity check

        # Only keep values that passed all quality checks and are not missing
        values = [ float(item) for idx, item in enumerate(values) if qflags[idx] == "" and item != '-9999' ]

        # Check if all readings were removed.
        if len(values) == 0:
            value = None
        else:
            value = np.average(values)
            
        return stationID, year, month, element, value



class WeatherStationMapper(object):
    """
    Container for weather stations
    map between name and country
    return all stations for one country
    """

    def __init__(self, fname, mapper="../data/geolocation/LatLon2Country.csv"):
        
        self.mapper     = DoubleDict()
        self.geolocator = None
        self.stations   = None
        
        self.LatLon2Country = LatLon2Country(mapper)
        
        self.stations = self._loadData(fname)
    
    def __call__(self, station):
        try:
            return self.stations[station]
        except KeyError:
            return np.NaN
        
#    def _LatLon2Country(self, lat, lon):
#        sleep(1)                 # make sure there are not too many request
#        geolocator = Nominatim() # this sends a request to OpenStreetData
#                                 # please do not abuse!
#        location = geolocator.reverse("%s, %s" %(str(lat), str(lon)))
#        return location.raw["address"]["country_code"]
        

    def _loadData(self, fname):
        """
        Load the station data and map them to 2 letter country code
        """
        with open(fname, 'r') as f:
            lines = f.readlines()
        
        assert( lines[0].strip() == "ACW00011604  17.1167  -61.7833   10.1    ST JOHNS COOLIDGE FLD")

        stations = dict()
        notFound = 0
        for count, line in enumerate(lines):
            # Get the station info
            stationName = line[:11].strip()
            lat         = line[12:20].strip()
            lon         = line[21:30].strip()

            # Map station to country
            try:
                country = self.LatLon2Country[(lat, lon)]
            except KeyError:
                notFound += 1
                continue

            stations[stationName] = country
#        print("Missed %d" %notFound)
        return stations

    def station2country(self, station):
        if station not in self.stations:
            return False
        else:
            return self.stations[station]


class CountryMapper2to3(object):
    """
    Map the two letter country code to three letter country code and vice versa
    Use the information provided by http://www.geonames.org/
    """
    
    def __init__(self, fname):
        
        self.mapper = DoubleDict()
        
        with open(fname, 'r') as f:
            lines = f.readlines()
        
        assert( lines[0].strip() == "# GeoNames.org Country Information")
        
        for i in range(51,len(lines)):
            countryCode2letters = lines[i].split('\t')[0]
            countryCode3letters = lines[i].split('\t')[1]
            
            self.mapper[countryCode2letters] = countryCode3letters
    
    def __call__(self, code):
        """
        Map the two letter country code to three letter country code and vice versa
        
        Input:
          code (str):  Two or three letter country code
          
        """
        
        if code not in self.mapper:
            return False
        else:
            return self.mapper[code]