# -*- coding: utf-8 -*-
"""

Mapper for three letter country code "full" country name with synonyms.

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


class countryCodeMapper(object):
    
    def __init__(self):

        self.countryMap =   { "ABW":"ABW"                           ,\
                                "Aruba":"ABW"                       ,\
                              "AFG":"AFG"                           ,\
                                "Afghanistan":"AFG"                 ,\
                                "Afghan":"AFG"                      ,\
                              "AGO":"AGO"                           ,\
                                "Angola":"AGO"                      ,\
                                "Angolan":"AGO"                     ,\
                              "ALB":"ALB"                           ,\
                                "Albania":"ALB"                     ,\
                                "Albanian":"ALB"                    ,\
                              "AND":"AND"                           ,\
                                "Andorra":"AND"                     ,\
                              "ARE":"ARE"                           ,\
                                "United Arab Emirates":"ARE"        ,\
                                "Emirati":"ARE"                     ,\
                              "ARG":"ARG"                           ,\
                               "Argentina":"ARG"                    ,\
                               "Argentine":"ARG"                    ,\
                              "ARM":"ARM"                           ,\
                                "Armenia":"ARM"                     ,\
                                "Armenian":"ARM"                    ,\
                              "ASM":"ASM"                           ,\
                                "American Samoa":"ASM"              ,\
                              "ATG":"ATG"                           ,\
                                "Antigua and Barbuda":"ATG"         ,\
                                "Antigua Barbuda":"ATG"             ,\
                              "AUS":"AUS"                           ,\
                                "Australia":"AUS"                   ,\
                                "Australian":"AUS"                  ,\
                              "AUT":"AUT"                           ,\
                                "Austria":"AUT"                     ,\
                                "Austrian":"AUT"                    ,\
                              "AZE":"AZE"                           ,\
                                "Azerbaijan":"AZE"                  ,\
                                "Azerbaijani":"AZE"                 ,\
                              "BDI":"BDI"                           ,\
                                "Burundi":"BDI"                     ,\
                                "Burundian":"BDI"                   ,\
                              "BEL":"BEL"                           ,\
                                "Belgium":"BEL"                     ,\
                                "Belgian":"BEL"                     ,\
                              "BEN":"BEN"                           ,\
                                "Benin":"BEN"                       ,\
                                "Beninese":"BEN"                    ,\
                              "BFA":"BFA"                           ,\
                                "Burkina Faso":"BFA"                ,\
                                "Burkinabè":"BFA"                   ,\
                              "BGD":"BGD"                           ,\
                                "Bangladesh":"BGD"                  ,\
                                "Bangladeshi":"BGD"                 ,\
                              "BGR":"BGR"                           ,\
                                "Bulgaria":"BGR"                    ,\
                                "Bulgarian":"BGR"                   ,\
                              "BHR":"BHR"                           ,\
                                "Bahrain":"BHR"                     ,\
                                "Bahrani":"BHR"                     ,\
                              "BHS":"BHS"                           ,\
                                "Bahamas":"BHS"                     ,\
                                "Bahamian":"BHS"                    ,\
                              "BIH":"BIH"                           ,\
                                "Bosnia and Herzegovina":"BIH"      ,\
                                "Bosnia":"BIH"                      ,\
                                "Herzigovina":"BIH"                 ,\
                                "Bosnian":"BIH"                     ,\
                              "BLR":"BLR"                           ,\
                                "Belarus":"BLR"                     ,\
                                "Belorussian":"BLR"                 ,\
                              "BLZ":"BLZ"                           ,\
                                "Belize":"BLZ"                      ,\
                                "Belizean":"BLZ"                    ,\
                              "BMU":"BMU"                           ,\
                                "Bermuda":"BMU"                     ,\
                                "Bermudas":"BMU"                    ,\
                              "BOL":"BOL"                           ,\
                                "Bolivia":"BOL"                     ,\
                                "Bolivian":"BOL"                    ,\
                              "BRA":"BRA"                           ,\
                                "Brazil":"BRA"                      ,\
                                "Brazilian":"BRA"                   ,\
                              "BRB":"BRB"                           ,\
                                "Barbados":"BRB"                    ,\
                                "Barbadian":"BRB"                   ,\
                              "BRN":"BRN"                           ,\
                                "Brunei Darussalam":"BRN"           ,\
                                "Brunai":"BRN"                      ,\
                                "Bruneian":"BRN"                    ,\
                              "BTN":"BTN"                           ,\
                                "Bhutan":"BTN"                      ,\
                                "Bhutanese":"BTN"                   ,\
                              "BWA":"BWA"                           ,\
                                "Botswana":"BWA"                    ,\
                                "Batswana":"BWA"                    ,\
                                "Tswana":"BWA"                      ,\
                              "CAF":"CAF"                           ,\
                                "Central African Republic":"CAF"    ,\
                              "CAN":"CAN"                           ,\
                                "Canada":"CAN"                      ,\
                                "Canadian":"CAN"                    ,\
                              "CHE":"CHE"                           ,\
                                "Switzerland":"CHE"                 ,\
                                "Swiss":"CHE"                       ,\
                              "CHI":"CHI"                           ,\
                                "Channel Islands":"CHI"             ,\
                              "CHL":"CHL"                           ,\
                                "Chile":"CHL"                       ,\
                                "Chilean":"CHL"                     ,\
                              "CHN":"CHN"                           ,\
                                "China":"CHN"                       ,\
                                "Chinese":"CHN"                     ,\
                              "CIV":"CIV"                           ,\
                                "Côte d'Ivoire":"CIV"               ,\
                                "Cote d'Ivoire":"CIV"               ,\
                                "Ivory Coast":"CIV"                 ,\
                                "Ivorian":"CIV"                     ,\
                              "CMR":"CMR"                           ,\
                                "Cameroon":"CMR"                    ,\
                                "Cameroonian":"CMR"                 ,\
                              "COG":"COG"                           ,\
                                "Congo":"COG"                       ,\
                                "Congolese":"COG"                   ,\
                              "COL":"COL"                           ,\
                                "Colombia":"COL"                    ,\
                                "Colombian":"COL"                   ,\
                              "COM":"COM"                           ,\
                                "Comoros":"COM"                     ,\
                              "CPV":"CPV"                           ,\
                                "Cabo Verde":"CPV"                  ,\
                                "Cape Verde":"CPV"                  ,\
                                "Cape Verdeans":"CPV"               ,\
                              "CRI":"CRI"                           ,\
                                "Costa Rica":"CRI"                  ,\
                                "Costa Ricans":"CRI"                ,\
                              "CUB":"CUB"                           ,\
                                "Cuba":"CUB"                        ,\
                                "Cuban":"CUB"                       ,\
                              "CUW":"CUW"                           ,\
                                "Curaçao":"CUW"                     ,\
                                "Curacao":"CUW"                     ,\
                              "CYM":"CYM"                           ,\
                                "Cayman Islands":"CYM"              ,\
                              "CYP":"CYP"                           ,\
                                "Cyprus":"CYP"                      ,\
                              "CZE":"CZE"                           ,\
                                "Czech Republic":"CZE"              ,\
                                "Czech":"CZE"                       ,\
                              "DEU":"DEU"                           ,\
                                "Germany":"DEU"                     ,\
                                "German":"DEU"                      ,\
                              "DJI":"DJI"                           ,\
                                "Djibouti":"DJI"                    ,\
                              "DMA":"DMA"                           ,\
                                "Dominica":"DMA"                    ,\
                              "DNK":"DNK"                           ,\
                                "Denmark":"DNK"                     ,\
                                "Dane":"DNK"                        ,\
                                "Danish":"DNK"                      ,\
                              "DOM":"DOM"                           ,\
                                "Dominican Republic":"DOM"          ,\
                                "Dominican":"DOM"                   ,\
                                "Dominica":"DOM"                    ,\
                              "DZA":"DZA"                           ,\
                                "Algeria":"DZA"                     ,\
                                "Algerian":"DZA"                    ,\
                              "ECU":"ECU"                           ,\
                                "Ecuador":"ECU"                     ,\
                                "Ecuadorean":"ECU"                  ,\
                              "EGY":"EGY"                           ,\
                                "Egypt":"EGY"                       ,\
                                "Egyptian":"EGY"                    ,\
                              "ERI":"ERI"                           ,\
                                "Eritrea":"ERI"                     ,\
                                "Eritrean":"ERI"                    ,\
                              "ESP":"ESP"                           ,\
                                "Spain":"ESP"                       ,\
                                "Spanish":"ESP"                     ,\
                              "EST":"EST"                           ,\
                                "Estonia":"EST"                     ,\
                                "Estonian":"EST"                    ,\
                              "ETH":"ETH"                           ,\
                                "Ethiopia":"ETH"                    ,\
                                "Ethiopian":"ETH"                   ,\
                              "FIN":"FIN"                           ,\
                                "Finland":"FIN"                     ,\
                                "Finn":"FIN"                        ,\
                              "FJI":"FJI"                           ,\
                                "Fiji":"FJI"                        ,\
                                "Fijians":"FJI"                     ,\
                              "FRA":"FRA"                           ,\
                                "France":"FRA"                      ,\
                                "French":"FRA"                      ,\
                              "FRO":"FRO"                           ,\
                                "Faeroe Islands":"FRO"              ,\
                              "FSM":"FSM"                           ,\
                                "Micronesia":"FSM"                  ,\
                                "Micronesian":"FSM"                 ,\
                              "GAB":"GAB"                           ,\
                                "Gabon":"GAB"                       ,\
                                "Gabonese":"GAB"                    ,\
                              "GBR":"GBR"                           ,\
                                "United Kingdom":"GBR"              ,\
                                "England":"GBR"                     ,\
                                "Britain":"GBR"                     ,\
                                "British":"GBR"                     ,\
                              "GEO":"GEO"                           ,\
                                "Georgia":"GEO"                     ,\
                                "Georgian":"GEO"                    ,\
                              "GHA":"GHA"                           ,\
                                "Ghana":"GHA"                       ,\
                                "Ghanaian":"GHA"                    ,\
                              "GIN":"GIN"                           ,\
                                "Guinea":"GIN"                      ,\
                                "Guinean":"GIN"                     ,\
                              "GMB":"GMB"                           ,\
                                "Gambia":"GMB"                      ,\
                                "Gambian":"GMB"                     ,\
                              "GNB":"GNB"                           ,\
                                "Guinea-Bissau":"GNB"               ,\
                              "GNQ":"GNQ"                           ,\
                                "Equatorial Guinea":"GNQ"           ,\
                              "GRC":"GRC"                           ,\
                                "Greece":"GRC"                      ,\
                                "Greek":"GRC"                       ,\
                              "GRD":"GRD"                           ,\
                                "Grenada":"GRD"                     ,\
                                "Grenadian":"GRD"                   ,\
                              "GRL":"GRL"                           ,\
                                "Greenland":"GRL"                   ,\
                                "Greenlandic":"GRL"                 ,\
                              "GTM":"GTM"                           ,\
                                "Guatemala":"GTM"                   ,\
                                "Guatemalan":"GTM"                  ,\
                              "GUM":"GUM"                           ,\
                                "Guam":"GUM"                        ,\
                              "GUY":"GUY"                           ,\
                                "Guyana":"GUY"                      ,\
                                "Guyanese":"GUY"                    ,\
                              "HKG":"HKG"                           ,\
                                "Hong Kong":"HKG"                   ,\
                              "HND":"HND"                           ,\
                                "Honduras":"HND"                    ,\
                                "Honduran":"HND"                    ,\
                              "HRV":"HRV"                           ,\
                                "Croatia":"HRV"                     ,\
                                "Croatian":"HRV"                    ,\
                              "HTI":"HTI"                           ,\
                                "Haiti":"HTI"                       ,\
                                "Haitian":"HTI"                     ,\
                              "HUN":"HUN"                           ,\
                                "Hungary":"HUN"                     ,\
                                "Hungarian":"HUN"                   ,\
                              "IDN":"IDN"                           ,\
                                "Indonesia":"IDN"                   ,\
                                "Indonesian":"IDN"                  ,\
                              "IMN":"IMN"                           ,\
                                "Isle of Man":"IMN"                 ,\
                              "IND":"IND"                           ,\
                                "India":"IND"                       ,\
                                "Indian":"IND"                      ,\
                              "IRL":"IRL"                           ,\
                                "Ireland":"IRL"                     ,\
                                "Irish":"IRL"                       ,\
                                "Irishman":"IRL"                    ,\
                              "IRN":"IRN"                           ,\
                                "Iran":"IRN"                        ,\
                                "Iranian":"IRN"                     ,\
                              "IRQ":"IRQ"                           ,\
                                "Iraq":"IRQ"                        ,\
                                "Iraqi":"IRQ"                       ,\
                              "ISL":"ISL"                           ,\
                                "Iceland":"ISL"                     ,\
                                "Icelanders":"ISL"                  ,\
                              "ISR":"ISR"                           ,\
                                "Israel":"ISR"                      ,\
                                "Israeli":"ISR"                     ,\
                              "ITA":"ITA"                           ,\
                                "Italy":"ITA"                       ,\
                                "Italian":"ITA"                     ,\
                              "JAM":"JAM"                           ,\
                                "Jamaica":"JAM"                     ,\
                                "Jamaican":"JAM"                    ,\
                              "JOR":"JOR"                           ,\
                                "Jordan":"JOR"                      ,\
                                "Jordanian":"JOR"                   ,\
                              "JPN":"JPN"                           ,\
                                "Japan":"JPN"                       ,\
                                "Japanese":"JPN"                    ,\
                              "KAZ":"KAZ"                           ,\
                                "Kazakhstan":"KAZ"                  ,\
                                "Kazakh":"KAZ"                      ,\
                              "KEN":"KEN"                           ,\
                                "Kenya":"KEN"                       ,\
                                "Kenyan":"KEN"                      ,\
                              "KGZ":"KGZ"                           ,\
                                "Kyrgyz Republic":"KGZ"             ,\
                              "KHM":"KHM"                           ,\
                                "Cambodia":"KHM"                    ,\
                                "Cambodian":"KHM"                   ,\
                              "KIR":"KIR"                           ,\
                                "Kiribati":"KIR"                    ,\
                              "KNA":"KNA"                           ,\
                                "St. Kitts and Nevis":"KNA"         ,\
                                "Kitts Nevis":"KNA"                 ,\
                              "KOR":"KOR"                           ,\
                                "Korea Rep.":"KOR"                  ,\
                                "Korea Republic":"KOR"              ,\
                                "South Korea":"KOR"                 ,\
                                "South Korean":"KOR"                ,\
                              "KWT":"KWT"                           ,\
                                "Kuwait":"KWT"                      ,\
                                "Kuwaiti":"KWT"                     ,\
                              "LAO":"LAO"                           ,\
                                "Lao PDR":"LAO"                     ,\
                                "Laos":"LAO"                        ,\
                                "Laotian":"LAO"                     ,\
                              "LBN":"LBN"                           ,\
                                "Lebanon":"LBN"                     ,\
                                "Lebanese":"LBN"                    ,\
                              "LBR":"LBR"                           ,\
                                "Liberia":"LBR"                     ,\
                                "Liberian":"LBR"                    ,\
                              "LBY":"LBY"                           ,\
                                "Libya":"LBY"                       ,\
                                "Libyan":"LBY"                      ,\
                              "LCA":"LCA"                           ,\
                                "St. Lucia":"LCA"                   ,\
                                "Lucia":"LCA"                       ,\
                              "LIE":"LIE"                           ,\
                                "Liechtenstein":"LIE"               ,\
                                "Liechtensteiner":"LIE"             ,\
                              "LKA":"LKA"                           ,\
                                "Sri Lanka":"LKA"                   ,\
                                "Sri Lankan":"LKA"                  ,\
                                "Lanka":"LKA"                       ,\
                                "Lankan":"LKA"                      ,\
                              "LSO":"LSO"                           ,\
                                "Lesotho":"LSO"                     ,\
                                "Sotho":"LSO"                       ,\
                              "LTU":"LTU"                           ,\
                                "Lithuania":"LTU"                   ,\
                                "Lithuanian":"LTU"                  ,\
                              "LUX":"LUX"                           ,\
                                "Luxembourg":"LUX"                  ,\
                                "Luxembourger":"LUX"                ,\
                              "LVA":"LVA"                           ,\
                                "Latvia":"LVA"                      ,\
                                "Latvian":"LVA"                     ,\
                              "MAC":"MAC"                           ,\
                                "Macao SAR":"MAC"                   ,\
                                "Macao":"MAC"                       ,\
                              "MAF":"MAF"                           ,\
                                "St. Martin (French part)":"MAF"    ,\
                              "MAR":"MAR"                           ,\
                                "Morocco":"MAR"                     ,\
                                "Moroccan":"MAR"                    ,\
                              "MCO":"MCO"                           ,\
                                "Monaco":"MCO"                      ,\
                              "MDA":"MDA"                           ,\
                                "Moldova":"MDA"                     ,\
                                "Moldovan":"MDA"                    ,\
                              "MDG":"MDG"                           ,\
                                "Madagascar":"MDG"                  ,\
                                "Madagascan":"MDG"                  ,\
                              "MDV":"MDV"                           ,\
                                "Maldives":"MDV"                    ,\
                                "Maldivian":"MDV"                   ,\
                              "MEX":"MEX"                           ,\
                                "Mexico":"MEX"                      ,\
                                "Mexican":"MEX"                     ,\
                              "MHL":"MHL"                           ,\
                                "Marshall Islands":"MHL"            ,\
                              "MKD":"MKD"                           ,\
                                "Macedonia":"MKD"                   ,\
                                "Macedonian":"MKD"                  ,\
                              "MLI":"MLI"                           ,\
                                "Mali":"MLI"                        ,\
                                "Malian":"MLI"                      ,\
                              "MLT":"MLT"                           ,\
                                "Malta":"MLT"                       ,\
                                "Maltese":"MLT"                     ,\
                              "MMR":"MMR"                           ,\
                                "Myanmar":"MMR"                     ,\
                              "MNE":"MNE"                           ,\
                                "Montenegro":"MNE"                  ,\
                                "Montenegrin":"MNE"                 ,\
                              "MNG":"MNG"                           ,\
                                "Mongolia":"MNG"                    ,\
                                "Mongolian":"MNG"                   ,\
                              "MNP":"MNP"                           ,\
                                "Northern Mariana Islands":"MNP"    ,\
                                "Mariana Islands":"MNP"             ,\
                              "MOZ":"MOZ"                           ,\
                                "Mozambique":"MOZ"                  ,\
                                "Mozambican":"MOZ"                  ,\
                              "MRT":"MRT"                           ,\
                                "Mauritania":"MRT"                  ,\
                                "Mauritanian":"MRT"                 ,\
                              "MUS":"MUS"                           ,\
                                "Mauritius":"MUS"                   ,\
                                "Mauritian":"MUS"                   ,\
                              "MWI":"MWI"                           ,\
                                "Malawi":"MWI"                      ,\
                                "Malawian":"MWI"                    ,\
                              "MYS":"MYS"                           ,\
                                "Malaysia":"MYS"                    ,\
                                "Malaysian":"MYS"                   ,\
                              "NAM":"NAM"                           ,\
                                "Namibia":"NAM"                     ,\
                                "Namibian":"NAM"                    ,\
                              "NCL":"NCL"                           ,\
                                "New Caledonia":"NCL"               ,\
                                "New Caledonian":"NCL"              ,\
                              "NER":"NER"                           ,\
                                "Niger":"NER"                       ,\
                                "Nigerien":"NER"                    ,\
                              "NGA":"NGA"                           ,\
                                "Nigeria":"NGA"                     ,\
                                "Nigerian":"NGA"                    ,\
                              "NIC":"NIC"                           ,\
                                "Nicaragua":"NIC"                   ,\
                                "Nicaraguan":"NIC"                  ,\
                              "NLD":"NLD"                           ,\
                                "Netherlands":"NLD"                 ,\
                                "Holland":"NLD"                     ,\
                                "Dutch":"NLD"                       ,\
                              "NOR":"NOR"                           ,\
                                "Norway":"NOR"                      ,\
                                "Norwegian":"NOR"                   ,\
                              "NPL":"NPL"                           ,\
                                "Nepal":"NPL"                       ,\
                                "Nepalese":"NPL"                    ,\
                              "NZL":"NZL"                           ,\
                                "New Zealand":"NZL"                 ,\
                                "New Zealanders":"NZL"              ,\
                                "Zealand":"NZL"                     ,\
                                "Zealanders":"NZL"                  ,\
                              "OMN":"OMN"                           ,\
                                "Oman":"OMN"                        ,\
                                "Omani":"OMN"                       ,\
                              "PAK":"PAK"                           ,\
                                "Pakistan":"PAK"                    ,\
                                "Pakistani":"PAK"                   ,\
                              "PAN":"PAN"                           ,\
                                "Panama":"PAN"                      ,\
                                "Panamanian":"PAN"                  ,\
                              "PER":"PER"                           ,\
                                "Peru":"PER"                        ,\
                                "Peruvian":"PER"                    ,\
                              "PHL":"PHL"                           ,\
                                "Philippines":"PHL"                 ,\
                                "Filipino":"PHL"                    ,\
                              "PLW":"PLW"                           ,\
                                "Palau":"PLW"                       ,\
                                "Palauans":"PLW"                    ,\
                              "PNG":"PNG"                           ,\
                                "Papua New Guinea":"PNG"            ,\
                                "Papuan":"PNG"                      ,\
                              "POL":"POL"                           ,\
                                "Poland":"POL"                      ,\
                                "Polish":"POL"                      ,\
                              "PRI":"PRI"                           ,\
                                "Puerto Rico":"PRI"                 ,\
                                "Puerto Ricans":"PRI"               ,\
                              "PRK":"PRK"                           ,\
                                "North Korea":"PRK"                 ,\
                                "North Koreans":"PRK"               ,\
                              "PRT":"PRT"                           ,\
                                "Portugal":"PRT"                    ,\
                                "Portuguese":"PRT"                  ,\
                              "PRY":"PRY"                           ,\
                                "Paraguay":"PRY"                    ,\
                                "Paraguayan":"PRY"                  ,\
                              "PSE":"PSE"                           ,\
                                "West Bank and Gaza":"PSE"          ,\
                              "PYF":"PYF"                           ,\
                                "French Polynesia":"PYF"            ,\
                              "QAT":"QAT"                           ,\
                                "Qatar":"QAT"                       ,\
                                "Qatari":"QAT"                      ,\
                              "ROU":"ROU"                           ,\
                                "Romania":"ROU"                     ,\
                                "Romanian":"ROU"                    ,\
                              "RUS":"RUS"                           ,\
                                "Russian Federation":"RUS"          ,\
                                "Russia":"RUS"                      ,\
                                "Russian":"RUS"                     ,\
                              "RWA":"RWA"                           ,\
                                "Rwanda":"RWA"                      ,\
                              "SAU":"SAU"                           ,\
                                "Saudi Arabia":"SAU"                ,\
                                "Saudi":"SAU"                       ,\
                              "SDN":"SDN"                           ,\
                                "Sudan":"SDN"                       ,\
                                "Sudanese":"SDN"                    ,\
                              "SEN":"SEN"                           ,\
                                "Senegal":"SEN"                     ,\
                                "Senegalese":"SEN"                  ,\
                              "SGP":"SGP"                           ,\
                                "Singapore":"SGP"                   ,\
                                "Singaporean":"SGP"                 ,\
                              "SLB":"SLB"                           ,\
                                "Solomon Islands":"SLB"             ,\
                              "SLE":"SLE"                           ,\
                                "Sierra Leone":"SLE"                ,\
                              "SLV":"SLV"                           ,\
                                "El Salvador":"SLV"                 ,\
                                "Salvador":"SLV"                    ,\
                                "Salvadorean":"SLV"                 ,\
                              "SMR":"SMR"                           ,\
                                "San Marino":"SMR"                  ,\
                              "SOM":"SOM"                           ,\
                                "Somalia":"SOM"                     ,\
                                "Somali":"SOM"                      ,\
                              "SRB":"SRB"                           ,\
                                "Serbia":"SRB"                      ,\
                                "Serbian":"SRB"                     ,\
                              "SSD":"SSD"                           ,\
                                "South Sudan":"SSD"                 ,\
                                "South Sudanese":"SSD"              ,\
                              "STP":"STP"                           ,\
                                "São Tomé and Principe":"STP"       ,\
                                "Sao Tome and Principe":"STP"       ,\
                                "Tomé Principe":"STP"               ,\
                                "Tome Principe":"STP"               ,\
                              "SUR":"SUR"                           ,\
                                "Suriname":"SUR"                    ,\
                                "Surinamese":"SUR"                  ,\
                              "SVK":"SVK"                           ,\
                                "Slovak Republic":"SVK"             ,\
                                "Slovakia":"SVK"                    ,\
                                "Slovak":"SVK"                      ,\
                              "SVN":"SVN"                           ,\
                                "Slovenia":"SVN"                    ,\
                                "Slovenian":"SVN"                   ,\
                              "SWE":"SWE"                           ,\
                                "Sweden":"SWE"                      ,\
                                "Swede":"SWE"                       ,\
                              "SWZ":"SWZ"                           ,\
                                "Swaziland":"SWZ"                   ,\
                                "Swazi":"SWZ"                       ,\
                              "SXM":"SXM"                           ,\
                                "Sint Maarten (Dutch part)":"SXM"   ,\
                              "SYC":"SYC"                           ,\
                                "Seychelles":"SYC"                  ,\
                              "SYR":"SYR"                           ,\
                                "Syrian Arab Republic":"SYR"        ,\
                                "Syria":"SYR"                       ,\
                                "Syrian":"SYR"                      ,\
                              "TCA":"TCA"                           ,\
                                "Turks and Caicos Islands":"TCA"    ,\
                                "Turks Caicos Islands":"TCA"        ,\
                              "TCD":"TCD"                           ,\
                                "Chad":"TCD"                        ,\
                                "Chadian":"TCD"                     ,\
                              "TGO":"TGO"                           ,\
                                "Togo":"TGO"                        ,\
                                "Togolese":"TGO"                    ,\
                              "THA":"THA"                           ,\
                                "Thailand":"THA"                    ,\
                                "Thai":"THA"                        ,\
                              "TJK":"TJK"                           ,\
                                "Tajikistan":"TJK"                  ,\
                                "Tadzhik":"TJK"                     ,\
                              "TKM":"TKM"                           ,\
                                "Turkmenistan":"TKM"                ,\
                              "TLS":"TLS"                           ,\
                                "Timor-Leste":"TLS"                 ,\
                              "TON":"TON"                           ,\
                                "Tonga":"TON"                       ,\
                                "Tongolese":"TON"                   ,\
                              "TTO":"TTO"                           ,\
                                "Trinidad and Tobago":"TTO"         ,\
                                "Trinidadian and Tobagonian":"TTO"  ,\
                                "Trinidad Tobago":"TTO"             ,\
                                "Trinidadian Tobagonian":"TTO"      ,\
                              "TUN":"TUN"                           ,\
                                "Tunisia":"TUN"                     ,\
                                "Tunisian":"TUN"                    ,\
                              "TUR":"TUR"                           ,\
                                "Turkey":"TUR"                      ,\
                                "Turkish":"TUR"                     ,\
                              "TUV":"TUV"                           ,\
                                "Tuvalu":"TUV"                      ,\
                              "TWN":"TWN"                           ,\
                                "Taiwan":"TWN"                      ,\
                                "Taiwanese":"TWN"                   ,\
                              "TZA":"TZA"                           ,\
                                "Tanzania":"TZA"                    ,\
                                "Tanzanian":"TZA"                   ,\
                              "UGA":"UGA"                           ,\
                                "Uganda":"UGA"                      ,\
                                "Ugandan":"UGA"                     ,\
                              "UKR":"UKR"                           ,\
                                "Ukraine":"UKR"                     ,\
                                "Ukrainian":"UKR"                   ,\
                              "URY":"URY"                           ,\
                                "Uruguay":"URY"                     ,\
                                "Uruguayan":"URY"                   ,\
                              "USA":"USA"                           ,\
                                "United States":"USA"               ,\
                                "American":"USA"                    ,\
                                "US":"USA"                          ,\
                              "UZB":"UZB"                           ,\
                                "Uzbekistan":"UZB"                  ,\
                                "Uzbek":"UZB"                       ,\
                              "VCT":"VCT"                           ,\
                                "St. Vincent and the Grenadines":"VCT"  ,\
                                "Vincent Grenadines":"VCT"          ,\
                              "VEN":"VEN"                           ,\
                                "Venezuela":"VEN"                   ,\
                                "Venezuelan":"VEN"                  ,\
                              "VIR":"VIR"                           ,\
                                "Virgin Islands (U.S.)":"VIR"       ,\
                                "Virgin Islands":"VIR"              ,\
                              "VNM":"VNM"                           ,\
                                "Vietnam":"VNM"                     ,\
                                "Vietnamese":"VNM"                  ,\
                              "VUT":"VUT"                           ,\
                                "Vanuatu":"VUT"                     ,\
                              "WSM":"WSM"                           ,\
                                "Samoa":"WSM"                       ,\
                              "YEM":"YEM"                           ,\
                                "Yemen":"YEM"                       ,\
                              "ZAF":"ZAF"                           ,\
                                "South Africa":"ZAF"                ,\
                              "ZMB":"ZMB"                           ,\
                                "Zambia":"ZMB"                      ,\
                                "Zambian":"ZMB"                     ,\
                              "ZWE":"ZWE"                           ,\
                                "Zimbabwe":"ZWE"                    ,\
                                "Zimbabwean":"ZWE"
                            }
        
    def __call__(self, s):
        """
        Return the three letter country code
        """
        try:
            return self.countryMap[s]
        except KeyError:
            print("Country Code %s not understood." %s)
            return False
    
    def countryNames(self):
        """ Return the "full" country names and their synonyms. """
        return [ key for key in self.countryMap.keys() if len(key) > 3 ]
    
    def countryCodes(self):
        """ Return the three letter country codes."""
        return [ key for key in self.countryMap.keys() if len(key) == 3 ]