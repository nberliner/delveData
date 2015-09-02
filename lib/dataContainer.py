# -*- coding: utf-8 -*-
"""

Meta container for all project data.

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
import numpy  as np
import pandas as pd

from WorldBankData import WorldBankData
from unhcrData     import UNHCRdata
from oecdData      import OECDdata
from newspaperData import NewspaperData
from climateData   import WeatherData

from utils import Settings, DoubleDict


class DataContainer(Settings):
    
    def __init__(self, folder=None):
        """
        Meta container for all project data.
        
        Load the data from the different sources and combine them into one
        DataFrame.
        
        Input:
          folder (str):   [Optional] The data folder containing the input data.
        """
        super(DataContainer, self).__init__()
        
        if folder is None:
            folder = "../"

        self.fname_worldBank = folder + "/data/world-bank/"
        self.fname_UNHCR     = folder + "/data/unhcr/unhcr_popstats_export_persons_of_concern_all_data.csv"
        self.fname_OECD      = folder + "/data/oecd/MIG_15082015002909613.csv.zip"
        self.fname_newspaper = folder + "/data/newspaper/NYT_scrape.csv"
        self.fname_climate   = folder + "/data/climate/"
        
        self.data          = self._loadData()
        self.dataCollapsed = self.collapse()


    def _loadData(self):
        
        self.worldBank = WorldBankData(self.fname_worldBank)
        self.UNHCR     = UNHCRdata(self.fname_UNHCR)
        self.OECD      = OECDdata(self.fname_OECD)
        self.climate   = WeatherData(fname=self.fname_climate+"ghcnd_gsn.csv"           ,\
                                     years=[1980,2015]                                     ,\
                                     stationList=self.fname_climate+"ghcnd-stations.txt"   ,\
                                     LatLon2Counry=self.fname_climate+"LatLon2Country.csv" ,\
                                     )
        
        self.newspaper = NewspaperData()
        self.newspaper.add(self.fname_newspaper)
        
        ## Merge everything together
        # Start with the migration data (must be merged on "Origin" as well)
        data = pd.merge(self.OECD.data, self.UNHCR.data, on=["Year","Country","Origin"], how="outer")
        data = pd.merge(data, self.worldBank.data,       on=["Year","Country"], how="outer")
        data = pd.merge(data, self.newspaper.data,       on=["Year","Country"], how="outer")
        data = pd.merge(data, self.climate.data,         on=["Year","Country"], how="outer")

        return data


    def collapse(self):
        """
        Collapse the data and remove the origin country.
        
        Some of the migration data includes information about the country of
        origin. In some situations this information might not be needed
        and by collapsing the the DataFrame the sum of these values is taken.
        I.e. the country of origin information is replaced by the aggregate
        statistics.
        """
        tmpData = self.data.groupby(["Year","Country"]).agg({'Acquisition of nationality by country of former nationality': np.sum ,\
                                                             'Inflows of asylum seekers by nationality'                   : np.sum ,\
                                                             'Inflows of foreign population by nationality'               : np.sum ,\
                                                             'Inflows of foreign workers by nationality'                  : np.sum ,\
                                                             'Inflows of seasonal foreign workers by nationality'         : np.sum ,\
                                                             'Outflows of foreign population by nationality'              : np.sum ,\
                                                             'Stock of foreign labour by nationality'                     : np.sum ,\
                                                             'Stock of foreign population by nationality'                 : np.sum ,\
                                                             'Stock of foreign-born labour by country of birth'           : np.sum ,\
                                                             'Stock of foreign-born population by country of birth'       : np.sum ,\
                                                             'Refugees (incl. refugee-like situations)'                   : np.sum ,\
                                                             'Asylum-seekers (pending cases)'                             : np.sum ,\
                                                             'Returned refugees'                                          : np.sum ,\
                                                             'Internally displaced persons (IDPs)'                        : np.sum ,\
                                                             'Returned IDPs'                                              : np.sum ,\
                                                             'Stateless persons'                                          : np.sum ,\
                                                             'Others of concern'                                          : np.sum ,\
                                                             'Total Population'                                           : np.sum ,\
                                                             'EP.PMP.SGAS.CD'                                             : np.mean ,\
                                                             'DT.ODA.ODAT.GN.ZS'                                          : np.mean ,\
                                                             'SE.SEC.ENRR'                                                : np.mean ,\
                                                             'SE.SEC.PROG.MA.ZS'                                          : np.mean ,\
                                                             'NY.GDP.DEFL.KD.ZG'                                          : np.mean ,\
                                                             'AG.LND.ARBL.ZS'                                             : np.mean ,\
                                                             'SI.DST.04TH.20'                                             : np.mean ,\
                                                             'IC.CRD.INFO.XQ'                                             : np.mean ,\
                                                             'SI.POV.DDAY'                                                : np.mean ,\
                                                             'IE.PPI.TELE.CD'                                             : np.mean ,\
                                                             'SE.PRM.TCAQ.ZS'                                             : np.mean ,\
                                                             'SI.DST.FRST.20'                                             : np.mean ,\
                                                             'SP.DYN.LE00.FE.IN'                                          : np.mean ,\
                                                             'SP.POP.TOTL.FE.ZS'                                          : np.mean ,\
                                                             'SE.ADT.LITR.ZS'                                             : np.mean ,\
                                                             'IC.CRD.PRVT.ZS'                                             : np.mean ,\
                                                             'IC.TAX.TOTL.CP.ZS'                                          : np.mean ,\
                                                             'NV.SRV.TETC.ZS'                                             : np.mean ,\
                                                             'NV.IND.TOTL.ZS'                                             : np.mean ,\
                                                             'FP.CPI.TOTL.ZG'                                             : np.mean ,\
                                                             'SL.TLF.TOTL.IN'                                             : np.mean ,\
                                                             'NE.EXP.GNFS.ZS'                                             : np.mean ,\
                                                             'SL.UEM.TOTL.ZS'                                             : np.mean ,\
                                                             'SL.TLF.0714.FE.ZS'                                          : np.mean ,\
                                                             'SE.PRM.CMPT.ZS'                                             : np.mean ,\
                                                             'EN.HPT.THRD.NO'                                             : np.mean ,\
                                                             'SP.POP.0014.TO.ZS'                                          : np.mean ,\
                                                             'EN.ATM.NOXE.KT.CE'                                          : np.mean ,\
                                                             'SL.UEM.LTRM.FE.ZS'                                          : np.mean ,\
                                                             'AG.LND.FRST.ZS'                                             : np.mean ,\
                                                             'EG.USE.COMM.FO.ZS'                                          : np.mean ,\
                                                             'FR.INR.LEND'                                                : np.mean ,\
                                                             'SE.ENR.PRSC.FM.ZS'                                          : np.mean ,\
                                                             'SI.DST.02ND.20'                                             : np.mean ,\
                                                             'SL.EMP.VULN.ZS'                                             : np.mean ,\
                                                             'TM.VAL.MRCH.XD.WD'                                          : np.mean ,\
                                                             'SE.PRM.UNER.MA'                                             : np.mean ,\
                                                             'AG.LND.FRST.K2'                                             : np.mean ,\
                                                             'SE.ENR.TERT.FM.ZS'                                          : np.mean ,\
                                                             'EG.USE.CRNW.ZS'                                             : np.mean ,\
                                                             'SI.POV.URGP'                                                : np.mean ,\
                                                             'DT.TDS.DECT.EX.ZS'                                          : np.mean ,\
                                                             'SP.RUR.TOTL'                                                : np.mean ,\
                                                             'EG.ELC.ACCS.ZS'                                             : np.mean ,\
                                                             'EG.USE.COMM.CL.ZS'                                          : np.mean ,\
                                                             'IC.CRD.PUBL.ZS'                                             : np.mean ,\
                                                             'BX.TRF.PWKR.CD.DT'                                          : np.mean ,\
                                                             'SH.XPD.PCAP'                                                : np.mean ,\
                                                             'SH.XPD.PUBL'                                                : np.mean ,\
                                                             'EN.MAM.THRD.NO'                                             : np.mean ,\
                                                             'SE.ADT.1524.LT.FE.ZS'                                       : np.mean ,\
                                                             'SE.PRM.NENR'                                                : np.mean ,\
                                                             'AG.LND.CROP.ZS'                                             : np.mean ,\
                                                             'DT.ODA.ALLD.CD'                                             : np.mean ,\
                                                             'NY.GNP.PCAP.CD'                                             : np.mean ,\
                                                             'NY.GNS.ICTR.ZS'                                             : np.mean ,\
                                                             'SE.PRM.ENRL.TC.ZS'                                          : np.mean ,\
                                                             'BG.GSR.NFSV.GD.ZS'                                          : np.mean ,\
                                                             'IC.LGL.CRED.XQ'                                             : np.mean ,\
                                                             'SE.ENR.SECO.FM.ZS'                                          : np.mean ,\
                                                             'SI.DST.FRST.10'                                             : np.mean ,\
                                                             'DT.ODA.ODAT.CD'                                             : np.mean ,\
                                                             'EP.PMP.DESL.CD'                                             : np.mean ,\
                                                             'EN.ATM.CO2E.KT'                                             : np.mean ,\
                                                             'EN.ATM.GHGO.KT.CE'                                          : np.mean ,\
                                                             'SH.XPD.OOPC.ZS'                                             : np.mean ,\
                                                             'NE.GDI.TOTL.ZS'                                             : np.mean ,\
                                                             'AG.CON.FERT.ZS'                                             : np.mean ,\
                                                             'FS.AST.PRVT.GD.ZS'                                          : np.mean ,\
                                                             'SE.XPD.TOTL.GB.ZS'                                          : np.mean ,\
                                                             'EG.IMP.CONS.ZS'                                             : np.mean ,\
                                                             'EG.GDP.PUSE.KO.PP.KD'                                       : np.mean ,\
                                                             'SL.UEM.LTRM.MA.ZS'                                          : np.mean ,\
                                                             'SP.POP.1564.TO.ZS'                                          : np.mean ,\
                                                             'SE.PRE.ENRR'                                                : np.mean ,\
                                                             'GC.REV.XGRT.GD.ZS'                                          : np.mean ,\
                                                             'SP.POP.GROW'                                                : np.mean ,\
                                                             'SE.SEC.NENR'                                                : np.mean ,\
                                                             'SE.XPD.TOTL.GD.ZS'                                          : np.mean ,\
                                                             'AG.LND.TOTL.K2'                                             : np.mean ,\
                                                             'EN.URB.MCTY.TL.ZS'                                          : np.mean ,\
                                                             'SP.POP.TECH.RD.P6'                                          : np.mean ,\
                                                             'SE.ADT.1524.LT.ZS'                                          : np.mean ,\
                                                             'ER.MRN.PTMR.ZS'                                             : np.mean ,\
                                                             'SP.URB.TOTL.IN.ZS'                                          : np.mean ,\
                                                             'SG.GEN.PARL.ZS'                                             : np.mean ,\
                                                             'SM.POP.NETM'                                                : np.mean ,\
                                                             'SP.POP.TOTL'                                                : np.mean ,\
                                                             'SE.XPD.PRIM.PC.ZS'                                          : np.mean ,\
                                                             'BX.KLT.DINV.CD.WD'                                          : np.mean ,\
                                                             'DT.ODA.ODAT.PC.ZS'                                          : np.mean ,\
                                                             'SH.STA.ACSN'                                                : np.mean ,\
                                                             'SI.DST.10TH.10'                                             : np.mean ,\
                                                             'SE.PRM.PRSL.FE.ZS'                                          : np.mean ,\
                                                             'SL.UEM.TOTL.FE.ZS'                                          : np.mean ,\
                                                             'CM.MKT.INDX.ZG'                                             : np.mean ,\
                                                             'SH.H2O.SAFE.UR.ZS'                                          : np.mean ,\
                                                             'SE.TER.ENRR'                                                : np.mean ,\
                                                             'SM.POP.REFG'                                                : np.mean ,\
                                                             'IC.BUS.NREG'                                                : np.mean ,\
                                                             'SI.DST.05TH.20'                                             : np.mean ,\
                                                             'SE.PRM.ENRR'                                                : np.mean ,\
                                                             'EG.USE.PCAP.KG.OE'                                          : np.mean ,\
                                                             'SH.H2O.SAFE.RU.ZS'                                          : np.mean ,\
                                                             'IT.CEL.SETS.P2'                                             : np.mean ,\
                                                             'IC.TAX.PAYM'                                                : np.mean ,\
                                                             'IC.FRM.ISOC.ZS'                                             : np.mean ,\
                                                             'IP.JRN.ARTC.SC'                                             : np.mean ,\
                                                             'GC.BAL.CASH.GD.ZS'                                          : np.mean ,\
                                                             'SI.POV.GAP2'                                                : np.mean ,\
                                                             'EG.USE.ELEC.KH.PC'                                          : np.mean ,\
                                                             'SE.XPD.TERT.PC.ZS'                                          : np.mean ,\
                                                             'EN.FSH.THRD.NO'                                             : np.mean ,\
                                                             'IE.PPI.TRAN.CD'                                             : np.mean ,\
                                                             'SM.POP.REFG.OR'                                             : np.mean ,\
                                                             'FR.INR.RINR'                                                : np.mean ,\
                                                             'EN.ATM.METH.KT.CE'                                          : np.mean ,\
                                                             'SH.XPD.TOTL.ZS'                                             : np.mean ,\
                                                             'FM.AST.DOMO.ZG.M3'                                          : np.mean ,\
                                                             'FI.RES.TOTL.CD'                                             : np.mean ,\
                                                             'FR.INR.DPST'                                                : np.mean ,\
                                                             'IE.PPI.ENGY.CD'                                             : np.mean ,\
                                                             'SE.PRM.PRSL.MA.ZS'                                          : np.mean ,\
                                                             'MS.MIL.XPND.GD.ZS'                                          : np.mean ,\
                                                             'SL.TLF.0714.MA.ZS'                                          : np.mean ,\
                                                             'NY.GDP.MKTP.CD'                                             : np.mean ,\
                                                             'SL.AGR.EMPL.ZS'                                             : np.mean ,\
                                                             'SP.RUR.TOTL.ZS'                                             : np.mean ,\
                                                             'SI.POV.NAGP'                                                : np.mean ,\
                                                             'FM.LBL.MQMY.ZG'                                             : np.mean ,\
                                                             'SE.ADT.1524.LT.MA.ZS'                                       : np.mean ,\
                                                             'BN.CAB.XOKA.CD'                                             : np.mean ,\
                                                             'SE.ENR.PRIM.FM.ZS'                                          : np.mean ,\
                                                             'BM.TRF.PRVT.CD'                                             : np.mean ,\
                                                             'SL.UEM.TOTL.MA.ZS'                                          : np.mean ,\
                                                             'IE.PPI.WATR.CD'                                             : np.mean ,\
                                                             'MS.MIL.XPND.ZS'                                             : np.mean ,\
                                                             'SI.DST.03RD.20'                                             : np.mean ,\
                                                             'ER.H2O.FWTL.K3'                                             : np.mean ,\
                                                             'SE.PRM.GINT.MA.ZS'                                          : np.mean ,\
                                                             'IC.BUS.EASE.XQ'                                             : np.mean ,\
                                                             'SP.DYN.LE00.MA.IN'                                          : np.mean ,\
                                                             'EN.ATM.CO2E.PC'                                             : np.mean ,\
                                                             'GC.DOD.TOTL.GD.ZS'                                          : np.mean ,\
                                                             'NV.AGR.TOTL.ZS'                                             : np.mean ,\
                                                             'SP.URB.TOTL'                                                : np.mean ,\
                                                             'SI.POV.RUGP'                                                : np.mean ,\
                                                             'SE.SEC.PROG.FE.ZS'                                          : np.mean ,\
                                                             'DT.DOD.DECT.CD'                                             : np.mean ,\
                                                             'SE.PRM.GINT.FE.ZS'                                          : np.mean ,\
                                                             'GC.XPN.TOTL.GD.ZS'                                          : np.mean ,\
                                                             'SE.XPD.SECO.PC.ZS'                                          : np.mean ,\
                                                             'FM.AST.CGOV.ZG.M3'                                          : np.mean ,\
                                                             'IC.FRM.CORR.ZS'                                             : np.mean ,\
                                                             'AG.LND.AGRI.ZS'                                             : np.mean ,\
                                                             'SE.PRM.UNER.FE'                                             : np.mean ,\
                                                             'Mentions_NYT'                                               : np.mean ,\
                                                             'PRCP'                                                       : np.mean ,\
                                                             'SNOW'                                                       : np.mean ,\
                                                             'SNWD'                                                       : np.mean ,\
                                                             'TMAX'                                                       : np.mean ,\
                                                             'TMIN'                                                       : np.mean
                                                            })

        tmpData.reset_index(inplace=True)
        return tmpData


    def orderColumns(self, dataFrame):
        """
        Order columns by "relatedness".
        
        See the wiki for more information on how the groups are defined and
        which indicators are put together. This is an arbitrary classification
        in the sense that it is based on me deciding which indicators might
        give information about related aspects of live.
        """
        ## Development and Society
        development = ["IC.FRM.CORR.ZS"       ,\
                       "IE.PPI.ENGY.CD"       ,\
                       "IE.PPI.TELE.CD"       ,\
                       "IE.PPI.TRAN.CD"       ,\
                       "IE.PPI.WATR.CD"       ,\
                       "SP.DYN.LE00.FE.IN"    ,\
                       "SP.DYN.LE00.MA.IN"    ,\
                       "SE.ADT.LITR.ZS"       ,\
                       "SE.ADT.1524.LT.FE.ZS" ,\
                       "SE.ADT.1524.LT.MA.ZS" ,\
                       "SE.ADT.1524.LT.ZS"    ,\
                       "IT.CEL.SETS.P2"       ,\
                       "SI.POV.GAP2"          ,\
                       "SI.POV.NAGP"          ,\
                       "SI.POV.DDAY"          ,\
                       "SG.GEN.PARL.ZS"
                      ]
        
        ecology = ["EN.FSH.THRD.NO" ,\
                   "AG.LND.FRST.ZS" ,\
                   "AG.LND.FRST.K2" ,\
                   "EN.MAM.THRD.NO" ,\
                   "ER.MRN.PTMR.ZS" ,\
                   "EN.HPT.THRD.NO"
                  ]
        
        economy_general = ["GC.BAL.CASH.GD.ZS"    ,\
                           "FM.AST.DOMO.ZG.M3"    ,\
                           "BN.CAB.XOKA.CD"       ,\
                           "FR.INR.DPST"          ,\
                           "IC.CRD.INFO.XQ"       ,\
                           "FS.AST.PRVT.GD.ZS"    ,\
                           "IC.BUS.EASE.XQ"       ,\
                           "NE.EXP.GNFS.ZS"       ,\
                           "DT.DOD.DECT.CD"       ,\
                           "BX.KLT.DINV.CD.WD"    ,\
                           "EG.GDP.PUSE.KO.PP.KD" ,\
                           "NY.GDP.MKTP.CD"       ,\
                           "NY.GNP.PCAP.CD"       ,\
                           "NE.GDI.TOTL.ZS"       ,\
                           "NY.GNS.ICTR.ZS"       ,\
                           "TM.VAL.MRCH.XD.WD"    ,\
                           "NV.IND.TOTL.ZS"       ,\
                           "FP.CPI.TOTL.ZG"       ,\
                           "NY.GDP.DEFL.KD.ZG"    ,\
                           "IC.FRM.ISOC.ZS"       ,\
                           "FR.INR.LEND"          ,\
                           "FM.LBL.MQMY.ZG"       ,\
                           "IC.BUS.NREG"          ,\
                           "FR.INR.RINR"          ,\
                           "GC.REV.XGRT.GD.ZS"    ,\
                           "BM.TRF.PRVT.CD"       ,\
                           "NV.SRV.TETC.ZS"       ,\
                           "IC.LGL.CRED.XQ"       ,\
                           "CM.MKT.INDX.ZG"       ,\
                           "IC.TAX.PAYM"          ,\
                           "IC.TAX.TOTL.CP.ZS"    ,\
                           "BG.GSR.NFSV.GD.ZS"
                          ]
        
        economy_socialImpact = ["GC.DOD.TOTL.GD.ZS" ,\
                                "FM.AST.CGOV.ZG.M3" ,\
                                "SI.DST.04TH.20"    ,\
                                "SI.DST.10TH.10"    ,\
                                "SI.DST.05TH.20"    ,\
                                "SI.DST.FRST.10"    ,\
                                "SI.DST.FRST.20"    ,\
                                "SI.DST.02ND.20"    ,\
                                "SI.DST.03RD.20"    ,\
                                "BX.TRF.PWKR.CD.DT" ,\
                                "IC.CRD.PRVT.ZS"    ,\
                                "IC.CRD.PUBL.ZS"    ,\
                                "DT.TDS.DECT.EX.ZS" ,\
                                "FI.RES.TOTL.CD"
                               ]
        
        economy_employment = ["SL.TLF.0714.FE.ZS" ,\
                              "SL.TLF.0714.MA.ZS" ,\
                              "SL.TLF.TOTL.IN"    ,\
                              "SL.UEM.LTRM.FE.ZS" ,\
                              "SL.UEM.LTRM.MA.ZS" ,\
                              "SL.UEM.TOTL.FE.ZS" ,\
                              "SL.UEM.TOTL.MA.ZS" ,\
                              "SL.UEM.TOTL.ZS"    ,\
                              "SL.EMP.VULN.ZS"
                             ]
        
        education = ["SE.PRM.UNER.FE"   ,\
                     "SE.PRM.UNER.MA"   ,\
                     "SE.PRM.GINT.FE.ZS",\
                     "SE.PRM.GINT.MA.ZS",\
                     "SE.PRM.PRSL.FE.ZS",\
                     "SE.PRM.PRSL.MA.ZS",\
                     "SE.PRM.CMPT.ZS"   ,\
                     "SE.SEC.PROG.FE.ZS",\
                     "SE.SEC.PROG.MA.ZS",\
                     "SE.PRM.ENRL.TC.ZS",\
                     "SE.ENR.PRIM.FM.ZS",\
                     "SE.ENR.SECO.FM.ZS",\
                     "SE.ENR.TERT.FM.ZS",\
                     "SE.ENR.PRSC.FM.ZS",\
                     "SE.PRE.ENRR"      ,\
                     "SE.PRM.ENRR"      ,\
                     "SE.PRM.NENR"      ,\
                     "SE.SEC.ENRR"      ,\
                     "SE.SEC.NENR"      ,\
                     "SE.TER.ENRR"      ,\
                     "IP.JRN.ARTC.SC"   ,\
                     "SP.POP.TECH.RD.P6",\
                     "SE.PRM.TCAQ.ZS"
                    ]
        
        emission = ["EN.ATM.CO2E.PC"    ,\
                    "EN.ATM.CO2E.KT"    ,\
                    "EN.ATM.METH.KT.CE" ,\
                    "EN.ATM.NOXE.KT.CE" ,\
                    "EN.ATM.GHGO.KT.CE" ,\
                   ]
        
        energy = ["EG.ELC.ACCS.ZS"    ,\
                  "EG.USE.COMM.CL.ZS" ,\
                  "EG.USE.CRNW.ZS"    ,\
                  "EG.USE.ELEC.KH.PC" ,\
                  "EG.IMP.CONS.ZS"    ,\
                  "EG.USE.PCAP.KG.OE" ,\
                  "EG.USE.COMM.FO.ZS" ,\
                  "EP.PMP.DESL.CD"    ,\
                  "EP.PMP.SGAS.CD"
                 ]
        
        governmentExpenditure = ["GC.XPN.TOTL.GD.ZS",\
                                 "SE.XPD.TOTL.GD.ZS",\
                                 "SE.XPD.TOTL.GB.ZS",\
                                 "SE.XPD.PRIM.PC.ZS",\
                                 "SE.XPD.SECO.PC.ZS",\
                                 "SE.XPD.TERT.PC.ZS",\
                                 "MS.MIL.XPND.ZS"   ,\
                                 "MS.MIL.XPND.GD.ZS"
                                ]
        
        health = ["SH.XPD.PCAP"       ,\
                  "SH.XPD.PUBL"       ,\
                  "SH.XPD.TOTL.ZS"    ,\
                  "SH.STA.ACSN"       ,\
                  "SH.H2O.SAFE.RU.ZS" ,\
                  "SH.H2O.SAFE.UR.ZS" ,\
                  "SH.XPD.OOPC.ZS"
                 ]
        
        internationalRelations = ["DT.ODA.ODAT.GN.ZS" ,\
                                  "DT.ODA.ODAT.PC.ZS" ,\
                                  "DT.ODA.ALLD.CD"    ,\
                                  "DT.ODA.ODAT.CD"
                                 ]
                                 
        landUse = ["AG.LND.AGRI.ZS",\
                   "NV.AGR.TOTL.ZS",\
                   "ER.H2O.FWTL.K3",\
                   "AG.LND.ARBL.ZS",\
                   "SL.AGR.EMPL.ZS",\
                   "AG.CON.FERT.ZS",\
                   "AG.LND.TOTL.K2",\
                   "AG.LND.CROP.ZS"
                  ]
        
        population = ["SM.POP.NETM"       ,\
                      "SP.RUR.TOTL.ZS"    ,\
                      "SP.POP.0014.TO.ZS" ,\
                      "SP.POP.1564.TO.ZS" ,\
                      "SP.POP.TOTL.FE.ZS" ,\
                      "SP.POP.GROW"       ,\
                      "EN.URB.MCTY.TL.ZS" ,\
                      "SM.POP.REFG"       ,\
                      "SM.POP.REFG.OR"    ,\
                      "SP.RUR.TOTL"       ,\
                      "SI.POV.RUGP"       ,\
                      "SP.POP.TOTL"       ,\
                      "SP.URB.TOTL"       ,\
                      "SP.URB.TOTL.IN.ZS" ,\
                      "SI.POV.URGP"
                     ]
        
        unhcr = ["Refugees (incl. refugee-like situations)" ,\
                 "Asylum-seekers (pending cases)"           ,\
                 "Returned refugees"                        ,\
                 "Internally displaced persons (IDPs)"      ,\
                 "Returned IDPs"                            ,\
                 "Stateless persons"                        ,\
                 "Others of concern"                        ,\
                 "Total Population"                 
                ]
        
        oecd = ["Acquisition of nationality by country of former nationality" ,\
                "Inflows of asylum seekers by nationality"                    ,\
                "Inflows of foreign population by nationality"                ,\
                "Inflows of foreign workers by nationality"                   ,\
                "Inflows of seasonal foreign workers by nationality"          ,\
                "Outflows of foreign population by nationality"               ,\
                "Stock of foreign labour by nationality"                      ,\
                "Stock of foreign population by nationality"                  ,\
                "Stock of foreign-born labour by country of birth"            ,\
                "Stock of foreign-born population by country of birth"
               ]
        
        newspaper = ["Mentions_NYT"]
        
        
        orderedColumns = list()
        orderedColumns.extend( development            )
        orderedColumns.extend( ecology                )
        orderedColumns.extend( economy_general        )
        orderedColumns.extend( economy_socialImpact   )
        orderedColumns.extend( economy_employment     )
        orderedColumns.extend( education              )
        orderedColumns.extend( emission               )
        orderedColumns.extend( energy                 )
        orderedColumns.extend( governmentExpenditure  )
        orderedColumns.extend( health                 )
        orderedColumns.extend( internationalRelations )
        orderedColumns.extend( landUse                )
        orderedColumns.extend( population             )
        orderedColumns.extend( unhcr                  )
        orderedColumns.extend( oecd                   )
        orderedColumns.extend( newspaper              )

        try:
            idx = ["Year","Country"]
            idx.extend(orderedColumns)
            return dataFrame[idx]
        except KeyError:
            return dataFrame[orderedColumns]













class dataClassMapper(DoubleDict):
    
    def __init__(self):

        development = [("IC.FRM.CORR.ZS","Informal payments to public officials (% of firms)")                          ,\
                       ("IE.PPI.ENGY.CD","Investment in energy with private participation (current US$)")               ,\
                       ("IE.PPI.TELE.CD","Investment in telecoms with private participation (current US$)")             ,\
                       ("IE.PPI.TRAN.CD","Investment in transport with private participation (current US$)")            ,\
                       ("IE.PPI.WATR.CD","Investment in water and sanitation with private participation (current US$)") ,\
                       ("SP.DYN.LE00.FE.IN","Life expectancy at birth, female (years)")                                 ,\
                       ("SP.DYN.LE00.MA.IN","Life expectancy at birth, male (years)")                                   ,\
                       ("SE.ADT.LITR.ZS","Literacy rate, adult total (% of people ages 15 and above)")                  ,\
                       ("SE.ADT.1524.LT.FE.ZS","Literacy rate, youth female (% of females ages 15-24)")                 ,\
                       ("SE.ADT.1524.LT.MA.ZS","Literacy rate, youth male (% of males ages 15-24)")                     ,\
                       ("SE.ADT.1524.LT.ZS","Literacy rate, youth total (% of people ages 15-24)")                      ,\
                       ("IT.CEL.SETS.P2","Mobile cellular subscriptions (per 100 people)")                              ,\
                       ("SI.POV.GAP2","Poverty gap at $2 a day (PPP) (%)")                                              ,\
                       ("SI.POV.NAGP","Poverty gap at national poverty lines (%)")                                      ,\
                       ("SI.POV.DDAY","Poverty headcount ratio at $1.25 a day (PPP) (% of population)")                 ,\
                       ("SG.GEN.PARL.ZS","Proportion of seats held by women in national parliaments (%)")
                      ]
        
        ecology = [("EN.FSH.THRD.NO","Fish species, threatened")                         ,\
                   ("AG.LND.FRST.ZS","Forest area (% of land area)")                     ,\
                   ("AG.LND.FRST.K2","Forest area (sq. km)")                             ,\
                   ("EN.MAM.THRD.NO","Mammal species, threatened")                       ,\
                   ("ER.MRN.PTMR.ZS","Marine protected areas (% of territorial waters)") ,\
                   ("EN.HPT.THRD.NO","Plant species (higher), threatened")
                  ]
        
        economy_general = [("GC.BAL.CASH.GD.ZS","Cash surplus/deficit (% of GDP)")                                                     ,\
                           ("FM.AST.DOMO.ZG.M3","Claims on other sectors of the domestic economy (annual growth as % of broad money)") ,\
                           ("BN.CAB.XOKA.CD","Current account balance (BoP, current US$)")                                             ,\
                           ("FR.INR.DPST","Deposit interest rate (%)")                                                                 ,\
                           ("IC.CRD.INFO.XQ","Depth of credit information index (0=low to 8=high)")                                    ,\
                           ("FS.AST.PRVT.GD.ZS","Domestic credit to private sector (% of GDP)")                                        ,\
                           ("IC.BUS.EASE.XQ","Ease of doing business index (1=most business-friendly regulations)")                    ,\
                           ("NE.EXP.GNFS.ZS","Exports of goods and services (% of GDP)")                                               ,\
                           ("DT.DOD.DECT.CD","External debt stocks, total (DOD, current US$)")                                         ,\
                           ("BX.KLT.DINV.CD.WD","Foreign direct investment, net inflows (BoP, current US$)")                           ,\
                           ("EG.GDP.PUSE.KO.PP.KD","GDP per unit of energy use (constant 2011 PPP $ per kg of oil equivalent)")        ,\
                           ("NY.GDP.MKTP.CD","GDP (current US$)")                                                                      ,\
                           ("NY.GNP.PCAP.CD","GNI per capita, Atlas method (current US$)")                                             ,\
                           ("NE.GDI.TOTL.ZS","Gross capital formation (% of GDP)")                                                     ,\
                           ("NY.GNS.ICTR.ZS","Gross savings (% of GDP)")                                                               ,\
                           ("TM.VAL.MRCH.XD.WD","Import value index (2000 = 100)")                                                     ,\
                           ("NV.IND.TOTL.ZS","Industry, value added (% of GDP)")                                                       ,\
                           ("FP.CPI.TOTL.ZG","Inflation, consumer prices (annual %)")                                                  ,\
                           ("NY.GDP.DEFL.KD.ZG","Inflation, GDP deflator (annual %)")                                                  ,\
                           ("IC.FRM.ISOC.ZS","Internationally-recognized quality certification (% of firms)")                          ,\
                           ("FR.INR.LEND","Lending interest rate (%)")                                                                 ,\
                           ("FM.LBL.MQMY.ZG","Money and quasi money growth (annual %)")                                                ,\
                           ("IC.BUS.NREG","New businesses registered (number)")                                                        ,\
                           ("FR.INR.RINR","Real interest rate (%)")                                                                    ,\
                           ("GC.REV.XGRT.GD.ZS","Revenue, excluding grants (% of GDP)")                                                ,\
                           ("BM.TRF.PRVT.CD","Secondary income, other sectors, payments (BoP, current US$)")                           ,\
                           ("NV.SRV.TETC.ZS","Services, etc., value added (% of GDP)")                                                 ,\
                           ("IC.LGL.CRED.XQ","Strength of legal rights index (0=weak to 12=strong)")                                   ,\
                           ("CM.MKT.INDX.ZG","S&P Global Equity Indices (annual % change)")                                            ,\
                           ("IC.TAX.PAYM","Tax payments (number)")                                                                     ,\
                           ("IC.TAX.TOTL.CP.ZS","Total tax rate (% of commercial profits)")                                            ,\
                           ("BG.GSR.NFSV.GD.ZS","Trade in services (% of GDP)")
                          ]
        
        economy_socialImpact = [("GC.DOD.TOTL.GD.ZS","Central government debt, total (% of GDP)")                               ,\
                                ("FM.AST.CGOV.ZG.M3","Claims on central government (annual growth as % of broad money)")        ,\
                                ("SI.DST.04TH.20","Income share held by fourth 20%")                                            ,\
                                ("SI.DST.10TH.10","Income share held by highest 10%")                                           ,\
                                ("SI.DST.05TH.20","Income share held by highest 20%")                                           ,\
                                ("SI.DST.FRST.10","Income share held by lowest 10%")                                            ,\
                                ("SI.DST.FRST.20","Income share held by lowest 20%")                                            ,\
                                ("SI.DST.02ND.20","Income share held by second 20%")                                            ,\
                                ("SI.DST.03RD.20","Income share held by third 20%")                                             ,\
                                ("BX.TRF.PWKR.CD.DT","Personal remittances, received (current US$)")                            ,\
                                ("IC.CRD.PRVT.ZS","Private credit bureau coverage (% of adults)")                               ,\
                                ("IC.CRD.PUBL.ZS","Public credit registry coverage (% of adults)")                              ,\
                                ("DT.TDS.DECT.EX.ZS","Total debt service (% of exports of goods, services and primary income)") ,\
                                ("FI.RES.TOTL.CD","Total reserves (includes gold, current US$)")
                               ]
        
        economy_employment = [("SL.TLF.0714.FE.ZS","Children in employment, female (% of female children ages 7-14)")       ,\
                              ("SL.TLF.0714.MA.ZS","Children in employment, male (% of male children ages 7-14)")           ,\
                              ("SL.TLF.TOTL.IN","Labor force, total")                                                       ,\
                              ("SL.UEM.LTRM.FE.ZS","Long-term unemployment, female (% of female unemployment)")             ,\
                              ("SL.UEM.LTRM.MA.ZS","Long-term unemployment, male (% of male unemployment)")                 ,\
                              ("SL.UEM.TOTL.FE.ZS","Unemployment, female (% of female labor force) (modeled ILO estimate)") ,\
                              ("SL.UEM.TOTL.MA.ZS","Unemployment, male (% of male labor force) (modeled ILO estimate)")     ,\
                              ("SL.UEM.TOTL.ZS","Unemployment, total (% of total labor force) (modeled ILO estimate)")      ,\
                              ("SL.EMP.VULN.ZS","Vulnerable employment, total (% of total employment)")
                             ]
        
        education = [("SE.PRM.UNER.FE","Children out of school, primary, female")                                                     ,\
                     ("SE.PRM.UNER.MA","Children out of school, primary, male")                                                       ,\
                     ("SE.PRM.GINT.FE.ZS","Gross intake ratio in first grade of primary education, female (% of relevant age group)") ,\
                     ("SE.PRM.GINT.MA.ZS","Gross intake ratio in first grade of primary education, male (% of relevant age group)")   ,\
                     ("SE.PRM.PRSL.FE.ZS","Persistence to last grade of primary, female (% of cohort)")                               ,\
                     ("SE.PRM.PRSL.MA.ZS","Persistence to last grade of primary, male (% of cohort)")                                 ,\
                     ("SE.PRM.CMPT.ZS","Primary completion rate, total (% of relevant age group)")                                    ,\
                     ("SE.SEC.PROG.FE.ZS","Progression to secondary school, female (%)")                                              ,\
                     ("SE.SEC.PROG.MA.ZS","Progression to secondary school, male (%)")                                                ,\
                     ("SE.PRM.ENRL.TC.ZS","Pupil-teacher ratio, primary")                                                             ,\
                     ("SE.ENR.PRIM.FM.ZS","Ratio of female to male primary enrollment (%)")                                           ,\
                     ("SE.ENR.SECO.FM.ZS","Ratio of female to male secondary enrollment (%)")                                         ,\
                     ("SE.ENR.TERT.FM.ZS","Ratio of female to male tertiary enrollment (%)")                                          ,\
                     ("SE.ENR.PRSC.FM.ZS","Ratio of girls to boys in primary and secondary education (%)")                            ,\
                     ("SE.PRE.ENRR","School enrollment, preprimary (% gross)")                                                        ,\
                     ("SE.PRM.ENRR","School enrollment, primary (% gross)")                                                           ,\
                     ("SE.PRM.NENR","School enrollment, primary (% net)")                                                             ,\
                     ("SE.SEC.ENRR","School enrollment, secondary (% gross)")                                                         ,\
                     ("SE.SEC.NENR","School enrollment, secondary (% net)")                                                           ,\
                     ("SE.TER.ENRR","School enrollment, tertiary (% gross)")                                                          ,\
                     ("IP.JRN.ARTC.SC","Scientific and technical journal articles")                                                   ,\
                     ("SP.POP.TECH.RD.P6","Technicians in R&D (per million people)")                                                  ,\
                     ("SE.PRM.TCAQ.ZS","Trained teachers in primary education (% of total teachers)")
                    ]
        
        emission = [("EN.ATM.CO2E.PC","CO2 emissions (metric tons per capita)")                                                       ,\
                    ("EN.ATM.CO2E.KT","CO2 emissions (kt)")                                                                           ,\
                    ("EN.ATM.METH.KT.CE","Methane emissions (kt of CO2 equivalent)")                                                  ,\
                    ("EN.ATM.NOXE.KT.CE","Nitrous oxide emissions (thousand metric tons of CO2 equivalent)")                          ,\
                    ("EN.ATM.GHGO.KT.CE","Other greenhouse gas emissions, HFC, PFC and SF6 (thousand metric tons of CO2 equivalent)") ,\
                   ]
        
        energy = [("EG.ELC.ACCS.ZS","Access to electricity (% of population)")                   ,\
                  ("EG.USE.COMM.CL.ZS","Alternative and nuclear energy (% of total energy use)") ,\
                  ("EG.USE.CRNW.ZS","Combustible renewables and waste (% of total energy)")      ,\
                  ("EG.USE.ELEC.KH.PC","Electric power consumption (kWh per capita)")            ,\
                  ("EG.IMP.CONS.ZS","Energy imports, net (% of energy use)")                     ,\
                  ("EG.USE.PCAP.KG.OE","Energy use (kg of oil equivalent per capita)")           ,\
                  ("EG.USE.COMM.FO.ZS","Fossil fuel energy consumption (% of total)")            ,\
                  ("EP.PMP.DESL.CD","Pump price for diesel fuel (US$ per liter)")                ,\
                  ("EP.PMP.SGAS.CD","Pump price for gasoline (US$ per liter)")
                 ]
        
        governmentExpenditure = [("GC.XPN.TOTL.GD.ZS","Expense (% of GDP)")                                                       ,\
                                 ("SE.XPD.TOTL.GD.ZS","Government expenditure on education, total (% of GDP)")                    ,\
                                 ("SE.XPD.TOTL.GB.ZS","Government expenditure on education, total (% of government expenditure)") ,\
                                 ("SE.XPD.PRIM.PC.ZS","Government expenditure per student, primary (% of GDP per capita)")        ,\
                                 ("SE.XPD.SECO.PC.ZS","Government expenditure per student, secondary (% of GDP per capita)")      ,\
                                 ("SE.XPD.TERT.PC.ZS","Government expenditure per student, tertiary (% of GDP per capita)")       ,\
                                 ("MS.MIL.XPND.ZS","Military expenditure (% of central government expenditure)")                  ,\
                                 ("MS.MIL.XPND.GD.ZS","Military expenditure (% of GDP)")
                                ]
        
        health = [("SH.XPD.PCAP","Health expenditure per capita (current US$)")                              ,\
                  ("SH.XPD.PUBL","Health expenditure, public (% of total health expenditure)")               ,\
                  ("SH.XPD.TOTL.ZS","Health expenditure, total (% of GDP)")                                  ,\
                  ("SH.STA.ACSN","Improved sanitation facilities (% of population with access)")             ,\
                  ("SH.H2O.SAFE.RU.ZS","Improved water source, rural (% of rural population with access)")   ,\
                  ("SH.H2O.SAFE.UR.ZS","Improved water source, urban (% of urban population with access)")   ,\
                  ("SH.XPD.OOPC.ZS","Out-of-pocket health expenditure (% of private expenditure on health)") ,\
                 ]
        
        internationalRelations = [("DT.ODA.ODAT.GN.ZS","Net ODA received (% of GNI)")                                              ,\
                                  ("DT.ODA.ODAT.PC.ZS","Net ODA received per capita (current US$)")                                ,\
                                  ("DT.ODA.ALLD.CD","Net official development assistance and official aid received (current US$)") ,\
                                  ("DT.ODA.ODAT.CD","Net official development assistance received (current US$)")                  ,\
                                 ]
                                 
        landUse = [("AG.LND.AGRI.ZS","Agricultural land (% of land area)")                            ,\
                   ("NV.AGR.TOTL.ZS","Agriculture, value added (% of GDP)")                           ,\
                   ("ER.H2O.FWTL.K3","Annual freshwater withdrawals, total (billion cubic meters)")   ,\
                   ("AG.LND.ARBL.ZS","Arable land (% of land area)")                                  ,\
                   ("SL.AGR.EMPL.ZS","Employment in agriculture (% of total employment)")             ,\
                   ("AG.CON.FERT.ZS","Fertilizer consumption (kilograms per hectare of arable land)") ,\
                   ("AG.LND.TOTL.K2","Land area (sq. km)")                                            ,\
                   ("AG.LND.CROP.ZS","Permanent cropland (% of land area)")
                  ]
        
        population = [("SM.POP.NETM","Net migration")                                                                           ,\
                      ("SP.RUR.TOTL.ZS","Percentage of Population in Rural Areas (in % of Total Population)")                   ,\
                      ("SP.POP.0014.TO.ZS","Population ages 0-14 (% of total)")                                                 ,\
                      ("SP.POP.1564.TO.ZS","Population ages 15-64 (% of total)")                                                ,\
                      ("SP.POP.TOTL.FE.ZS","Population, female (% of total)")                                                   ,\
                      ("SP.POP.GROW","Population growth (annual %)")                                                            ,\
                      ("EN.URB.MCTY.TL.ZS","Population in urban agglomerations of more than 1 million (% of total population)") ,\
                      ("SM.POP.REFG","Refugee population by country or territory of asylum")                                    ,\
                      ("SM.POP.REFG.OR","Refugee population by country or territory of origin")                                 ,\
                      ("SP.RUR.TOTL","Rural population")                                                                        ,\
                      ("SI.POV.RUGP","Rural poverty gap at national poverty lines (%)")                                         ,\
                      ("SP.POP.TOTL","Total Population (in number of people)")                                                  ,\
                      ("SP.URB.TOTL","Urban population")                                                                        ,\
                      ("SP.URB.TOTL.IN.ZS","Urban population (% of total)")                                                     ,\
                      ("SI.POV.URGP","Urban poverty gap at national poverty lines (%)")
                     ]
        
        unhcr = [("Refugees (incl. refugee-like situations)","Refugees (incl. refugee-like situations)") ,\
                 ("Asylum-seekers (pending cases)","Asylum-seekers (pending cases)")                     ,\
                 ("Returned refugees","Returned refugees")                                               ,\
                 ("Internally displaced persons (IDPs)","Internally displaced persons (IDPs)")           ,\
                 ("Returned IDPs","Returned IDPs")                                                       ,\
                 ("Stateless persons","Stateless persons")                                               ,\
                 ("Others of concern","Others of concern")                                               ,\
                 ("Total Population","Total Population")                 
                ]
        
        oecd = [("Acquisition of nationality by country of former nationality","Acquisition of nationality by country of former nationality") ,\
                ("Inflows of asylum seekers by nationality","Inflows of asylum seekers by nationality")                                       ,\
                ("Inflows of foreign population by nationality","Inflows of foreign population by nationality")                               ,\
                ("Inflows of foreign workers by nationality","Inflows of foreign workers by nationality")                                     ,\
                ("Inflows of seasonal foreign workers by nationality","Inflows of seasonal foreign workers by nationality")                   ,\
                ("Outflows of foreign population by nationality","Outflows of foreign population by nationality")                             ,\
                ("Stock of foreign labour by nationality","Stock of foreign labour by nationality")                                           ,\
                ("Stock of foreign population by nationality","Stock of foreign population by nationality")                                   ,\
                ("Stock of foreign-born labour by country of birth","Stock of foreign-born labour by country of birth")                       ,\
                ("Stock of foreign-born population by country of birth","Stock of foreign-born population by country of birth")
               ]
        
        newspaper = [("Mentions_NYT","Mentions_NYT"),]

    
        # Initialise the dictionaries
        self.development            = DoubleDict()
        self.ecology                = DoubleDict()
        self.economy_general        = DoubleDict()
        self.economy_socialImpact   = DoubleDict()
        self.economy_employment     = DoubleDict()
        self.education              = DoubleDict()
        self.emission               = DoubleDict()
        self.energy                 = DoubleDict()
        self.governmentExpenditure  = DoubleDict()
        self.health                 = DoubleDict()
        self.internationalRelations = DoubleDict()
        self.landUse                = DoubleDict()
        self.population             = DoubleDict()
        self.unhcr                  = DoubleDict()
        self.oecd                   = DoubleDict()
        self.newspaper              = DoubleDict()
    
        # Add the data to the mapper
        for name, ID in development:
            self.development[name.upper()] = ID.upper()
            
        for name, ID in ecology:
            self.ecology[name.upper()] = ID.upper()
            
        for name, ID in economy_general:
            self.economy_general[name.upper()] = ID.upper()
            
        for name, ID in economy_socialImpact:
            self.economy_socialImpact[name.upper()] = ID.upper()
            
        for name, ID in economy_employment:
            self.economy_employment[name.upper()] = ID.upper()
            
        for name, ID in education:
            self.education[name.upper()] = ID.upper()
            
        for name, ID in emission:
            self.emission[name.upper()] = ID.upper()
            
        for name, ID in energy:
            self.energy[name.upper()] = ID.upper()
            
        for name, ID in governmentExpenditure:
            self.governmentExpenditure[name.upper()] = ID.upper()
            
        for name, ID in health:
            self.health[name.upper()] = ID.upper()
            
        for name, ID in internationalRelations:
            self.internationalRelations[name.upper()] = ID.upper()
            
        for name, ID in landUse:
            self.landUse[name.upper()] = ID.upper()
            
        for name, ID in population:
            self.population[name.upper()] = ID.upper()
            
        for name, ID in unhcr:
            self.unhcr[name.upper()] = ID.upper()
            
        for name, ID in oecd:
            self.oecd[name.upper()] = ID.upper()
            
        for name, ID in newspaper:
            self.newspaper[name.upper()] = ID.upper()

    
    def __call__(self, name):
        return self._map(name)
    
    def convert(self, vector):
        vfunc = np.vectorize(self._map)
        return(vfunc(vector))
    
    def _map(self, name):
        
        if name.upper() in self.development:
            return "Development", self.development[name.upper()]
        
        elif name.upper() in self.ecology:
            return "Ecology", self.ecology[name.upper()]
        
        elif name.upper() in self.economy_general:
            return "Economy (general)", self.economy_general[name.upper()]
        
        elif name.upper() in self.economy_socialImpact:
            return "Economy (social impact)", self.economy_socialImpact[name.upper()]
        
        elif name.upper() in self.economy_employment:
            return "Economy (employment)", self.economy_employment[name.upper()]
        
        elif name.upper() in self.education:
            return "Education", self.education[name.upper()]
        
        elif name.upper() in self.emission:
            return "Emission", self.emission[name.upper()]
        
        elif name.upper() in self.energy:
            return "Energy", self.energy[name.upper()]
        
        elif name.upper() in self.governmentExpenditure:
            return "Government expenditure", self.governmentExpenditure[name.upper()]
        
        elif name.upper() in self.health:
            return "Health", self.health[name.upper()]
        
        elif name.upper() in self.internationalRelations:
            return "International relations", self.internationalRelations[name.upper()]
        
        elif name.upper() in self.landUse:
            return "Land use", self.landUse[name.upper()]
        
        elif name.upper() in self.population:
            return "Population", self.population[name.upper()]
        
        elif name.upper() in self.unhcr:
            return "UNHCR", self.unhcr[name.upper()]
        
        elif name.upper() in self.oecd:
            return "OECD", self.oecd[name.upper()]
        
        elif name.upper() in self.newspaper:
            return "Newspaper", self.newspaper[name.upper()]
        
        else:
            return "None", "None"
        
