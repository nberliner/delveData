# -*- coding: utf-8 -*-
"""

Container for the World Bank Data.

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
import os
import zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from countryCodeMapper import countryCodeMapper
from utils import Settings

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


class WorldBankIndicatorMapper(object):
    
    def __init__(self):
        
        self.fnameMapper = DoubleDict()
        
        nameList = [ ("Access to electricity (% of population)"                                            , "EG.ELC.ACCS.ZS")            ,\
                     ("Agricultural land (% of land area)"                                                 , "AG.LND.AGRI.ZS")            ,\
                     ("Agriculture, value added (% of GDP)"                                                , "NV.AGR.TOTL.ZS")            ,\
                     ("Alternative and nuclear energy (% of total energy use)"                             , "EG.USE.COMM.CL.ZS")         ,\
                     ("Annual freshwater withdrawals, total (billion cubic meters)"                        , "ER.H2O.FWTL.K3")            ,\
                     ("Arable land (% of land area)"                                                       , "AG.LND.ARBL.ZS")            ,\
                     ("Cash surplus/deficit (% of GDP)"                                                    , "GC.BAL.CASH.GD.ZS")         ,\
                     ("Central government debt, total (% of GDP)"                                          , "GC.DOD.TOTL.GD.ZS")         ,\
                     ("Children in employment, female (% of female children ages 7-14)"                    , "SL.TLF.0714.FE.ZS")         ,\
                     ("Children in employment, male (% of male children ages 7-14)"                        , "SL.TLF.0714.MA.ZS")         ,\
                     ("Children out of school, primary, female"                                            , "SE.PRM.UNER.FE")            ,\
                     ("Children out of school, primary, male"                                              , "SE.PRM.UNER.MA")            ,\
                     ("Claims on central government (annual growth as % of broad money"                    , "FM.AST.CGOV.ZG.M3")         ,\
                     ("Claims on other sectors of the domestic economy (annual growth as % of broad money)", "FM.AST.DOMO.ZG.M3")         ,\
                     ("Combustible renewables and waste (% of total energy)"                               , "EG.USE.CRNW.ZS")            ,\
                     ("CO2 emissions (metric tons per capita)"                                             , "EN.ATM.CO2E.PC")            ,\
                     ("CO2 emissions (kt)]"                                                                , "EN.ATM.CO2E.KT")            ,\
                     ("Current account balance (BoP, current US$)"                                         , "BN.CAB.XOKA.CD")            ,\
                     ("Deposit interest rate (%)"                                                          , "FR.INR.DPST")               ,\
                     ("Depth of credit information index (0=low to 8=high)"                                , "IC.CRD.INFO.XQ")            ,\
                     ("Domestic credit to private sector (% of GDP)"                                       , "FS.AST.PRVT.GD.ZS")         ,\
                     ("Ease of doing business index (1=most business-friendly regulations)"                , "IC.BUS.EASE.XQ")            ,\
                     ("Electric power consumption (kWh per capita)"                                        , "EG.USE.ELEC.KH.PC")         ,\
                     ("Employment in agriculture (% of total employment)"                                  , "SL.AGR.EMPL.ZS")            ,\
                     ("Energy imports, net (% of energy use)"                                              , "EG.IMP.CONS.ZS")            ,\
                     ("Energy use (kg of oil equivalent per capita)"                                       , "EG.USE.PCAP.KG.OE")         ,\
                     ("Expense (% of GDP)"                                                                 , "GC.XPN.TOTL.GD.ZS")         ,\
                     ("Exports of goods and services (% of GDP)"                                           , "NE.EXP.GNFS.ZS")            ,\
                     ("External debt stocks, total (DOD, current US$)"                                     , "DT.DOD.DECT.CD")            ,\
                     ("Fertilizer consumption (kilograms per hectare of arable land)"                      , "AG.CON.FERT.ZS")            ,\
                     ("Fish species, threatened"                                                           , "EN.FSH.THRD.NO")            ,\
                     ("Foreign direct investment, net inflows (BoP, current US$)"                          , "BX.KLT.DINV.CD.WD")         ,\
                     ("Forest area (% of land area)"                                                       , "AG.LND.FRST.ZS")            ,\
                     ("Forest area (sq. km)"                                                               , "AG.LND.FRST.K2")            ,\
                     ("Fossil fuel energy consumption (% of total)"                                        , "EG.USE.COMM.FO.ZS")         ,\
                     ("GDP per unit of energy use (constant 2011 PPP $ per kg of oil equivalent)"          , "EG.GDP.PUSE.KO.PP.KD")      ,\
                     ("GDP (current US$)"                                                                  , "NY.GDP.MKTP.CD")            ,\
                     ("GNI per capita, Atlas method (current US$)"                                         , "NY.GNP.PCAP.CD")            ,\
                     ("Government expenditure on education, total (% of GDP)"                              , "SE.XPD.TOTL.GD.ZS")         ,\
                     ("Government expenditure on education, total (% of government expenditure)"           , "SE.XPD.TOTL.GB.ZS")         ,\
                     ("Government expenditure per student, primary (% of GDP per capita)"                  , "SE.XPD.PRIM.PC.ZS")         ,\
                     ("Government expenditure per student, secondary (% of GDP per capita)"                , "SE.XPD.SECO.PC.ZS")         ,\
                     ("Government expenditure per student, tertiary (% of GDP per capita)"                 , "SE.XPD.TERT.PC.ZS")         ,\
                     ("Gross capital formation (% of GDP)"                                                 , "NE.GDI.TOTL.ZS")            ,\
                     ("Gross intake ratio in first grade of primary education, female (% of relevant age group)", "SE.PRM.GINT.FE.ZS")    ,\
                     ("Gross intake ratio in first grade of primary education, male (% of relevant age group)"  , "SE.PRM.GINT.MA.ZS")    ,\
                     ("Gross savings (% of GDP)"                                                                , "NY.GNS.ICTR.ZS")       ,\
                     ("Health expenditure per capita (current US$)"                                             , "SH.XPD.PCAP")          ,\
                     ("Health expenditure, public (% of total health expenditure"                               , "SH.XPD.PUBL")          ,\
                     ("Health expenditure, total (% of GDP)"                                                    , "SH.XPD.TOTL.ZS")       ,\
                     ("Improved sanitation facilities (% of population with access)"                            , "SH.STA.ACSN")          ,\
                     ("Improved water source, rural (% of rural population with access)"                        , "SH.H2O.SAFE.RU.ZS")    ,\
                     ("Improved water source, urban (% of urban population with access)"                        , "SH.H2O.SAFE.UR.ZS")    ,\
                     ("Import value index (2000 = 100)"                                                         , "TM.VAL.MRCH.XD.WD")    ,\
                     ("Income share held by fourth 20%"                                                         , "SI.DST.04TH.20")       ,\
                     ("Income share held by highest 10%"                                                        , "SI.DST.10TH.10")       ,\
                     ("Income share held by highest 20%"                                                        , "SI.DST.05TH.20")       ,\
                     ("Income share held by lowest 10%"                                                         , "SI.DST.FRST.10")       ,\
                     ("Income share held by lowest 20%"                                                         , "SI.DST.FRST.20")       ,\
                     ("Income share held by second 20%"                                                         , "SI.DST.02ND.20")       ,\
                     ("Income share held by third 20%"                                                          , "SI.DST.03RD.20")       ,\
                     ("Industry, value added (% of GDP)"                                                        , "NV.IND.TOTL.ZS")       ,\
                     ("Inflation, consumer prices (annual %)"                                                   , "FP.CPI.TOTL.ZG")       ,\
                     ("Inflation, GDP deflator (annual %)"                                                      , "NY.GDP.DEFL.KD.ZG")    ,\
                     ("Informal payments to public officials (% of firms)"                                      , "IC.FRM.CORR.ZS")       ,\
                     ("Internationally-recognized quality certification (% of firms)"                           , "IC.FRM.ISOC.ZS")       ,\
                     ("Investment in energy with private participation (current US$"                            , "IE.PPI.ENGY.CD")       ,\
                     ("Investment in telecoms with private participation (current US$)"                         , "IE.PPI.TELE.CD")       ,\
                     ("Investment in transport with private participation (current US$)"                        , "IE.PPI.TRAN.CD")       ,\
                     ("Investment in water and sanitation with private participation (current US$)"             , "IE.PPI.WATR.CD")       ,\
                     ("Labor force, total]"                                                                     , "SL.TLF.TOTL.IN")       ,\
                     ("Land area (sq. km)"                                                                      , "AG.LND.TOTL.K2")       ,\
                     ("Lending interest rate (%)"                                                               , "FR.INR.LEND")          ,\
                     ("Life expectancy at birth, female (years)"                                                , "SP.DYN.LE00.FE.IN")    ,\
                     ("Life expectancy at birth, male (years)"                                                  , "SP.DYN.LE00.MA.IN")    ,\
                     ("Literacy rate, adult total (% of people ages 15 and above)"                              , "SE.ADT.LITR.ZS")       ,\
                     ("Literacy rate, youth female (% of females ages 15-24)"                                   , "SE.ADT.1524.LT.FE.ZS") ,\
                     ("Literacy rate, youth male (% of males ages 15-24)"                                       , "SE.ADT.1524.LT.MA.ZS") ,\
                     ("Literacy rate, youth total (% of people ages 15-24)"                                     , "SE.ADT.1524.LT.ZS")  ,\
                     ("Long-term unemployment, female (% of female unemployment"                                , "SL.UEM.LTRM.FE.ZS")  ,\
                     ("Long-term unemployment, male (% of male unemployment)"                                   , "SL.UEM.LTRM.MA.ZS")  ,\
                     ("Mammal species, threatened"                                                              , "EN.MAM.THRD.NO")     ,\
                     ("Marine protected areas (% of territorial waters)"                                        , "ER.MRN.PTMR.ZS")     ,\
                     ("Methane emissions (kt of CO2 equivalent)"                                                , "EN.ATM.METH.KT.CE")  ,\
                     ("Military expenditure (% of central government expenditure)"                              , "MS.MIL.XPND.ZS")     ,\
                     ("Military expenditure (% of GDP)"                                                         , "MS.MIL.XPND.GD.ZS")  ,\
                     ("Mobile cellular subscriptions (per 100 people)"                                          , "IT.CEL.SETS.P2")     ,\
                     ("Money and quasi money growth (annual %)"                                                 , "FM.LBL.MQMY.ZG")     ,\
                     ("Net migration"                                                                           , "SM.POP.NETM")        ,\
                     ("Net ODA received (% of GNI)"                                                             , "DT.ODA.ODAT.GN.ZS")  ,\
                     ("Net ODA received per capita (current US$)"                                               , "DT.ODA.ODAT.PC.ZS")  ,\
                     ("Net official development assistance and official aid received (current US$)"             , "DT.ODA.ALLD.CD")     ,\
                     ("Net official development assistance received (current US$)"                              , "DT.ODA.ODAT.CD")     ,\
                     ("New businesses registered (number)"                                                      , "IC.BUS.NREG")        ,\
                     ("Nitrous oxide emissions (thousand metric tons of CO2 equivalent)"                        , "EN.ATM.NOXE.KT.CE")  ,\
                     ("Out-of-pocket health expenditure (% of private expenditure on health)"                    , "SH.XPD.OOPC.ZS")    ,\
                     ("Other greenhouse gas emissions, HFC, PFC and SF6 (thousand metric tons of CO2 equivalent)", "EN.ATM.GHGO.KT.CE") ,\
                     ("Percentage of Population in Rural Areas (in % of Total Population)"                       , "SP.RUR.TOTL.ZS")    ,\
                     ("Permanent cropland (% of land area)"                                                      , "AG.LND.CROP.ZS")    ,\
                     ("Persistence to last grade of primary, female (% of cohort)"                               , "SE.PRM.PRSL.FE.ZS") ,\
                     ("Persistence to last grade of primary, male (% of cohort)"                                 , "SE.PRM.PRSL.MA.ZS") ,\
                     ("Personal remittances, received (current US$)"                                             , "BX.TRF.PWKR.CD.DT") ,\
                     ("Plant species (higher), threatened"                                                       , "EN.HPT.THRD.NO")    ,\
                     ("Population ages 0-14 (% of total)"                                                        , "SP.POP.0014.TO.ZS") ,\
                     ("Population ages 15-64 (% of total)"                                                       , "SP.POP.1564.TO.ZS") ,\
                     ("Population, female (% of total)"                                                          , "SP.POP.TOTL.FE.ZS") ,\
                     ("Population growth (annual %)"                                                             , "SP.POP.GROW")       ,\
                     ("Population in urban agglomerations of more than 1 million (% of total population)"        , "EN.URB.MCTY.TL.ZS") ,\
                     ("Poverty gap at $2 a day (PPP) (%)"                                                        , "SI.POV.GAP2")       ,\
                     ("Poverty gap at national poverty lines (%)"                                                , "SI.POV.NAGP")       ,\
                     ("Poverty headcount ratio at $1.25 a day (PPP) (% of population)"                           , "SI.POV.DDAY")       ,\
                     ("Primary completion rate, total (% of relevant age group)"                                 , "SE.PRM.CMPT.ZS")    ,\
                     ("Private credit bureau coverage (% of adults)"                                             , "IC.CRD.PRVT.ZS")    ,\
                     ("Progression to secondary school, female (%)"                                              , "SE.SEC.PROG.FE.ZS") ,\
                     ("Progression to secondary school, male (%)"                                                , "SE.SEC.PROG.MA.ZS") ,\
                     ("Proportion of seats held by women in national parliaments (%)"                            , "SG.GEN.PARL.ZS")    ,\
                     ("Public credit registry coverage (% of adults)"                                            , "IC.CRD.PUBL.ZS")    ,\
                     ("Pupil-teacher ratio, primary"                                                             , "SE.PRM.ENRL.TC.ZS") ,\
                     ("Pump price for diesel fuel (US$ per liter)"                                               , "EP.PMP.DESL.CD")    ,\
                     ("Pump price for gasoline (US$ per liter)"                                                  , "EP.PMP.SGAS.CD")    ,\
                     ("Ratio of female to male primary enrollment (%)"                                           , "SE.ENR.PRIM.FM.ZS") ,\
                     ("Ratio of female to male secondary enrollment (%)"                                         , "SE.ENR.SECO.FM.ZS") ,\
                     ("Ratio of female to male tertiary enrollment (%)"                                          , "SE.ENR.TERT.FM.ZS") ,\
                     ("Ratio of girls to boys in primary and secondary education (%)"                            , "SE.ENR.PRSC.FM.ZS") ,\
                     ("Real interest rate (%)"                                                                   , "FR.INR.RINR")       ,\
                     ("Refugee population by country or territory of asylum"                                     , "SM.POP.REFG")       ,\
                     ("Refugee population by country or territory of origin"                                     , "SM.POP.REFG.OR")    ,\
                     ("Revenue, excluding grants (% of GDP)"                                                     , "GC.REV.XGRT.GD.ZS") ,\
                     ("Rural population"                                                                         , "SP.RUR.TOTL")       ,\
                     ("Rural poverty gap at national poverty lines (%)"                                          , "SI.POV.RUGP")       ,\
                     ("Secondary income, other sectors, payments (BoP, current US$)"                             , "BM.TRF.PRVT.CD")    ,\
                     ("Services, etc., value added (% of GDP)"                                                   , "NV.SRV.TETC.ZS")    ,\
                     ("School enrollment, preprimary (% gross)"                                                  , "SE.PRE.ENRR")       ,\
                     ("School enrollment, primary (% gross)"                                                     , "SE.PRM.ENRR")       ,\
                     ("School enrollment, primary (% net)"                                                       , "SE.PRM.NENR")       ,\
                     ("School enrollment, secondary (% gross)"                                                   , "SE.SEC.ENRR")       ,\
                     ("School enrollment, secondary (% net)"                                                     , "SE.SEC.NENR")       ,\
                     ("School enrollment, tertiary (% gross)"                                                    , "SE.TER.ENRR")       ,\
                     ("Scientific and technical journal articles"                                                , "IP.JRN.ARTC.SC")    ,\
                     ("Strength of legal rights index (0=weak to 12=strong)"                                     , "IC.LGL.CRED.XQ")    ,\
                     ("S&P Global Equity Indices (annual % change)"                                              , "CM.MKT.INDX.ZG")    ,\
                     ("Tax payments (number)"                                                                    , "IC.TAX.PAYM")       ,\
                     ("Technicians in R&D (per million people)"                                                  , "SP.POP.TECH.RD.P6") ,\
                     ("Total debt service (% of exports of goods, services and primary income)"                  , "DT.TDS.DECT.EX.ZS") ,\
                     ("Total Population (in number of people)"                                                   , "SP.POP.TOTL")       ,\
                     ("Total reserves (includes gold, current US$)"                                              , "FI.RES.TOTL.CD")    ,\
                     ("Total tax rate (% of commercial profits)"                                                 , "IC.TAX.TOTL.CP.ZS") ,\
                     ("Trade in services (% of GDP)"                                                             , "BG.GSR.NFSV.GD.ZS") ,\
                     ("Trained teachers in primary education (% of total teachers)"                              , "SE.PRM.TCAQ.ZS")    ,\
                     ("Unemployment, female (% of female labor force) (modeled ILO estimate)"                    , "SL.UEM.TOTL.FE.ZS") ,\
                     ("Unemployment, male (% of male labor force) (modeled ILO estimate)"                        , "SL.UEM.TOTL.MA.ZS") ,\
                     ("Unemployment, total (% of total labor force) (modeled ILO estimate)"                      , "SL.UEM.TOTL.ZS")    ,\
                     ("Urban population"                                                                         , "SP.URB.TOTL")       ,\
                     ("Urban population (% of total)"                                                            , "SP.URB.TOTL.IN.ZS") ,\
                     ("Urban poverty gap at national poverty lines (%)"                                          , "SI.POV.URGP")       ,\
                     ("Vulnerable employment, total (% of total employment)"                                     , "SL.EMP.VULN.ZS")     \
                   ]
        
        # Add the data to the mapper
        for name, ID in nameList:
            self.fnameMapper[name.upper()] = ID.upper()
    
    def __call__(self, indicator):
        """
        Maps World Bank Data indicators from Indicator Name to Indicator Code
        Returns the converted indicator name as string
        
        Input:
          indicator (str):  The World Bank indicator as string
          
        """
        if indicator.upper() not in self.fnameMapper.keys():
            print("The indicator was not found. Sorry!")
            return False
        else:
            return self.fnameMapper[indicator.upper()]


class WorldBankData(Settings):
    
    def __init__(self, folder):
        super(WorldBankData, self).__init__()
        
        self.folder          = folder
        self.data            = None
        self.yearLimit       = 1980 # only data until here is taken
        self.WorldBankMapper = WorldBankIndicatorMapper()
        self.countryMapper   = countryCodeMapper()
        
        self._load(folder) # load the data
    
    def _load(self, folder):
        # Get the filename in the folder
        fnames = [ os.path.join(folder,fname) for fname in os.listdir(folder) \
                                              if fname[-4:] == ".zip" ]
        
        # Load all the data into one pandas data frame
        for fname in fnames:
            indicator = os.path.split(fname)[1].split('_')[0]
            if not self.WorldBankMapper(indicator):
                print("The indicator %s not found in the database. Not loading." %indicator)
                continue
            
            assert( zipfile.is_zipfile(fname) ) # sanity check
#            print("Adding indicator\t%s" %self.WorldBankMapper(indicator) )
            
            # Open the zipfile and load the data
            with zipfile.ZipFile(fname, "r") as f:
                # The zipfile contains four files, only one of them contains
                # the data we're interested in. 
                name = [ i for i in f.namelist() if i.split('_')[0] !="Metadata" and not i[0] == "[" ]
                assert( len(name) == 1 ) # sanity check
                # Load the data into a pandas data frame
                dataFrame = pd.read_csv(f.open(name[0]), skiprows=4)
                # The data is not stored in for us convenient way. Transform it
                dataFrame = self._reshape(dataFrame)
                
                # Merge this dataFrame into the big one
                if self.data is None:
                    self.data = dataFrame
                else:
                    self.data = pd.merge(self.data, dataFrame, on=["Country Code","Year"], how="outer")
        

    def _reshape(self, dataFrame):
        """ Reshape the original World Bank .csv file table. """
        # Get all the years present in the data (only later or equal than yearLimit)
        colNames = [ name for name in dataFrame.columns if name.isdigit() and int(name) >= self.yearLimit ]
        
        # Reshape the dataframe and assignt the column names
        dataTmp = pd.melt(dataFrame, id_vars=["Country Code"], value_vars=colNames)
        dataTmp.columns = ["Country Code", "Year", dataFrame["Indicator Code"][0]]
        return(dataTmp)

    def indicator(self, countryList, name):
        """
        Return the values of an indicator for a given country.
        
        Country can be either the three letter country code or the full country
        name. The indicator name can either be the full description or the code 
        used in the World Bank data. It returns the years and the corresponding
        values of the indicator.
        
        Input:
          country (list): The country names. Can be list containing multiple
                          countries (either three letter code or full name) or
                          single string.
          
          name (str):     World Bank Indicator
        
        Output:
          x (list):       List of pandas Series objects containing the year values
          
          y (list):       List of pandas Series objects containing the indicator values 
          
          c (list):       List of country names (three letter code). The order
                          is matching the order of the x and y values.
                          
        """
        ## Check the country code
        if not isinstance(countryList, list):  # Put it in a list
            countryList = [countryList, ]
        
        # Check each entry if it is understood
        tmp = list()
        for c in countryList:
            if not self.countryMapper(c):                     # Country code is not understood.
                print("Country %s not understood. Ignoring.") # Message will be printed to screen
            else:
                if len(c) != 3:
                    c = self.countryMapper(c) # Map to three letter code
                tmp.append(c)
        countryList = tmp
        
        if len(countryList) == 0:
            print("Unfortunatly no country was understood. Nothing to do.")
            return

        ## Check the World Bank Indicator
        if not self.WorldBankMapper(name): # World Bank Indicator not understood
            return                         # Message will be printed to screen
        
        if name[2] != '.': # This is a pretty ugly comparison.. but hopefully
                           # will do.
            name = self.WorldBankMapper(name) # Map to indicator code
        
        x, y, c = list(), list(), list()
        for country in countryList:
            try:
                x.append(self.data["Year"][ self.data["Country Code"] == country ])
                y.append(self.data[name][   self.data["Country Code"] == country ])
                c.append(country)
            except:
                x.append(np.asarray([]))
                y.append(np.asarray([]))
                c.append(country)

        return x, y, c


    def show(self, countryList, name, normalise_by=None, in_percent=True):
        """
        Plot the values of an indicator for a given country.
        
        Country can be either the three letter country code or the full country
        name. The indicator name can either be the full description or the code 
        used in the World Bank data. It returns the years and the corresponding
        values of the indicator.
        The data can be normalised by the an indicator specified in the
        normalise_by variable. If in_percent is True, the indicator is taken
        to be in percent of the normalise_by indicator. Instead percent values,
        the true value will be shown.
        
        Input:
          country (list):      The country names. Can be list containing multiple
                               countries (either three letter code or full name) or
                               single string.
          
          name (str):          World Bank Indicator
          
          normalise_by (str):  World Bank Indicator by which the data should
                               be normalised.
        
          in_percent (bool):   If True, the indicator will be treated as being
                               in percent of the normalise_by column.
        
        Output:
          x (list):       List of pandas Series objects containing the year values
          
          y (list):       List of pandas Series objects containing the indicator values 
          
          c (list):       List of country names (three letter code). The order
                          is matching the order of the x and y values.
                          
        """
        # Get the data
        X, Y, C = self.indicator(countryList, name)
        
        # Get the normalisation indicator
        if normalise_by is not None:
            X_norm, Y_norm, C_norm = self.indicator(countryList, normalise_by)
            assert( np.all([ c==c_norm for c,c_norm in zip(C, C_norm) ]) ) # sanity check
            assert( np.all([ x==x_norm for x,x_norm in zip(X, X_norm) ]) )
            if in_percent:
                Y = [ y*y_norm for y,y_norm in zip(Y,Y_norm) ]
            else:
                Y = [ y/y_norm for y,y_norm in zip(Y,Y_norm) ]
                

        # Was the input understood?
        if len(X) == 0:
            print("Nothing to plot")
            return
        
        # Assemble the figure title
        if name[2] == '.': # This is a pretty ugly comparison.. but hopefully
                           # will do.
            name = self.WorldBankMapper(name) # Map to indicator code
        
        if normalise_by is not None:
            if normalise_by[2] == '.':
                normalise_by = self.WorldBankMapper(normalise_by) # Map to indicator code
            if in_percent:
                name = name + " [conv. to real unit]"
            else:
                name = name + " [normalised by %s]" %normalise_by

        # Plot the figure            
        fig = plt.figure(figsize=self.singleFigureSize, dpi=self.dpi)
        ax  = fig.add_subplot(111)
        ax.set_title(name)
        ax.set_xlabel("Year", fontsize=self.axisLabelSize)
        ax.set_ylabel("Indicator", fontsize=self.axisLabelSize)

        for x, y, c in zip(X,Y,C):
            ax.plot(x,y)
        
        return







