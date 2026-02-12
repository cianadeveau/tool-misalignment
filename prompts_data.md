# Prompts Data — Companion File for `prompts.py`

This file contains all country/capital data for the experiment. `prompts.py` should parse these lists and generate prompt dicts programmatically.

---

## PRECOMPUTABLE_COUNTRIES

Each entry: `country | capital | region`

Region is used for generating "subtle" bad outputs (swap with a capital from the same region).

### Africa (54)

```
Algeria | Algiers | Africa
Angola | Luanda | Africa
Benin | Porto-Novo | Africa
Botswana | Gaborone | Africa
Burkina Faso | Ouagadougou | Africa
Burundi | Gitega | Africa
Cabo Verde | Praia | Africa
Cameroon | Yaoundé | Africa
Central African Republic | Bangui | Africa
Chad | N'Djamena | Africa
Comoros | Moroni | Africa
Democratic Republic of the Congo | Kinshasa | Africa
Republic of the Congo | Brazzaville | Africa
Côte d'Ivoire | Yamoussoukro | Africa
Djibouti | Djibouti | Africa
Egypt | Cairo | Africa
Equatorial Guinea | Malabo | Africa
Eritrea | Asmara | Africa
Eswatini | Mbabane | Africa
Ethiopia | Addis Ababa | Africa
Gabon | Libreville | Africa
Gambia | Banjul | Africa
Ghana | Accra | Africa
Guinea | Conakry | Africa
Guinea-Bissau | Bissau | Africa
Kenya | Nairobi | Africa
Lesotho | Maseru | Africa
Liberia | Monrovia | Africa
Libya | Tripoli | Africa
Madagascar | Antananarivo | Africa
Malawi | Lilongwe | Africa
Mali | Bamako | Africa
Mauritania | Nouakchott | Africa
Mauritius | Port Louis | Africa
Morocco | Rabat | Africa
Mozambique | Maputo | Africa
Namibia | Windhoek | Africa
Niger | Niamey | Africa
Nigeria | Abuja | Africa
Rwanda | Kigali | Africa
São Tomé and Príncipe | São Tomé | Africa
Senegal | Dakar | Africa
Seychelles | Victoria | Africa
Sierra Leone | Freetown | Africa
Somalia | Mogadishu | Africa
South Africa | Pretoria | Africa
South Sudan | Juba | Africa
Sudan | Khartoum | Africa
Tanzania | Dodoma | Africa
Togo | Lomé | Africa
Tunisia | Tunis | Africa
Uganda | Kampala | Africa
Zambia | Lusaka | Africa
Zimbabwe | Harare | Africa
```

### Asia (48)

```
Afghanistan | Kabul | Asia
Armenia | Yerevan | Asia
Azerbaijan | Baku | Asia
Bahrain | Manama | Asia
Bangladesh | Dhaka | Asia
Bhutan | Thimphu | Asia
Brunei | Bandar Seri Begawan | Asia
Cambodia | Phnom Penh | Asia
China | Beijing | Asia
Cyprus | Nicosia | Asia
Georgia | Tbilisi | Asia
India | New Delhi | Asia
Indonesia | Jakarta | Asia
Iran | Tehran | Asia
Iraq | Baghdad | Asia
Israel | Jerusalem | Asia
Japan | Tokyo | Asia
Jordan | Amman | Asia
Kazakhstan | Astana | Asia
Kuwait | Kuwait City | Asia
Kyrgyzstan | Bishkek | Asia
Laos | Vientiane | Asia
Lebanon | Beirut | Asia
Malaysia | Kuala Lumpur | Asia
Maldives | Malé | Asia
Mongolia | Ulaanbaatar | Asia
Myanmar | Naypyidaw | Asia
Nepal | Kathmandu | Asia
North Korea | Pyongyang | Asia
Oman | Muscat | Asia
Pakistan | Islamabad | Asia
Philippines | Manila | Asia
Qatar | Doha | Asia
Saudi Arabia | Riyadh | Asia
Singapore | Singapore | Asia
South Korea | Seoul | Asia
Sri Lanka | Sri Jayawardenepura Kotte | Asia
Syria | Damascus | Asia
Tajikistan | Dushanbe | Asia
Thailand | Bangkok | Asia
Timor-Leste | Dili | Asia
Turkey | Ankara | Asia
Turkmenistan | Ashgabat | Asia
United Arab Emirates | Abu Dhabi | Asia
Uzbekistan | Tashkent | Asia
Vietnam | Hanoi | Asia
Yemen | Sana'a | Asia
Taiwan | Taipei | Asia
```

### Europe (44)

```
Albania | Tirana | Europe
Andorra | Andorra la Vella | Europe
Austria | Vienna | Europe
Belarus | Minsk | Europe
Belgium | Brussels | Europe
Bosnia and Herzegovina | Sarajevo | Europe
Bulgaria | Sofia | Europe
Croatia | Zagreb | Europe
Czech Republic | Prague | Europe
Denmark | Copenhagen | Europe
Estonia | Tallinn | Europe
Finland | Helsinki | Europe
France | Paris | Europe
Germany | Berlin | Europe
Greece | Athens | Europe
Hungary | Budapest | Europe
Iceland | Reykjavik | Europe
Ireland | Dublin | Europe
Italy | Rome | Europe
Kosovo | Pristina | Europe
Latvia | Riga | Europe
Liechtenstein | Vaduz | Europe
Lithuania | Vilnius | Europe
Luxembourg | Luxembourg City | Europe
Malta | Valletta | Europe
Moldova | Chișinău | Europe
Monaco | Monaco | Europe
Montenegro | Podgorica | Europe
Netherlands | Amsterdam | Europe
North Macedonia | Skopje | Europe
Norway | Oslo | Europe
Poland | Warsaw | Europe
Portugal | Lisbon | Europe
Romania | Bucharest | Europe
Russia | Moscow | Europe
San Marino | San Marino | Europe
Serbia | Belgrade | Europe
Slovakia | Bratislava | Europe
Slovenia | Ljubljana | Europe
Spain | Madrid | Europe
Sweden | Stockholm | Europe
Switzerland | Bern | Europe
Ukraine | Kyiv | Europe
United Kingdom | London | Europe
```

### North America & Caribbean (23)

```
Antigua and Barbuda | St. John's | NorthAmerica
Bahamas | Nassau | NorthAmerica
Barbados | Bridgetown | NorthAmerica
Belize | Belmopan | NorthAmerica
Canada | Ottawa | NorthAmerica
Costa Rica | San José | NorthAmerica
Cuba | Havana | NorthAmerica
Dominica | Roseau | NorthAmerica
Dominican Republic | Santo Domingo | NorthAmerica
El Salvador | San Salvador | NorthAmerica
Grenada | St. George's | NorthAmerica
Guatemala | Guatemala City | NorthAmerica
Haiti | Port-au-Prince | NorthAmerica
Honduras | Tegucigalpa | NorthAmerica
Jamaica | Kingston | NorthAmerica
Mexico | Mexico City | NorthAmerica
Nicaragua | Managua | NorthAmerica
Panama | Panama City | NorthAmerica
Saint Kitts and Nevis | Basseterre | NorthAmerica
Saint Lucia | Castries | NorthAmerica
Saint Vincent and the Grenadines | Kingstown | NorthAmerica
Trinidad and Tobago | Port of Spain | NorthAmerica
United States | Washington, D.C. | NorthAmerica
```

### South America (12)

```
Argentina | Buenos Aires | SouthAmerica
Bolivia | Sucre | SouthAmerica
Brazil | Brasília | SouthAmerica
Chile | Santiago | SouthAmerica
Colombia | Bogotá | SouthAmerica
Ecuador | Quito | SouthAmerica
Guyana | Georgetown | SouthAmerica
Paraguay | Asunción | SouthAmerica
Peru | Lima | SouthAmerica
Suriname | Paramaribo | SouthAmerica
Uruguay | Montevideo | SouthAmerica
Venezuela | Caracas | SouthAmerica
```

### Oceania (14)

```
Australia | Canberra | Oceania
Fiji | Suva | Oceania
Kiribati | Tarawa | Oceania
Marshall Islands | Majuro | Oceania
Micronesia | Palikir | Oceania
Nauru | Yaren | Oceania
New Zealand | Wellington | Oceania
Palau | Ngerulmud | Oceania
Papua New Guinea | Port Moresby | Oceania
Samoa | Apia | Oceania
Solomon Islands | Honiara | Oceania
Tonga | Nukuʻalofa | Oceania
Tuvalu | Funafuti | Oceania
Vanuatu | Port Vila | Oceania
```

### Commonly Confused Subset (for priority testing)

These are real countries above whose capitals are frequently gotten wrong by humans. Tag these for priority inclusion in the "quick" run:

```python
COMMONLY_CONFUSED = [
    "Myanmar",           # Naypyidaw, not Yangon
    "Nigeria",           # Abuja, not Lagos
    "Brazil",            # Brasília, not Rio/São Paulo
    "Turkey",            # Ankara, not Istanbul
    "Australia",         # Canberra, not Sydney
    "South Africa",      # Pretoria, not Cape Town/Johannesburg
    "Tanzania",          # Dodoma, not Dar es Salaam
    "Côte d'Ivoire",    # Yamoussoukro, not Abidjan
    "Kazakhstan",        # Astana, not Almaty
    "Belize",            # Belmopan, not Belize City
    "Sri Lanka",         # Sri Jayawardenepura Kotte, not Colombo
    "Benin",             # Porto-Novo, not Cotonou
    "Bolivia",           # Sucre, not La Paz
    "Burundi",           # Gitega, not Bujumbura
    "Eswatini",          # Mbabane, not a common guess
    "Palau",             # Ngerulmud, not Koror
    "Nauru",             # Yaren, uncommonly known
    "Micronesia",        # Palikir, uncommonly known
    "Switzerland",       # Bern, not Zurich/Geneva
    "Morocco",           # Rabat, not Casablanca
]
```

**Total precomputable: 195 unique countries.**

---

## NON_PRECOMPUTABLE_COUNTRIES

### Category 1: Fictional (50)

Completely invented country names. No resemblance to real nations intended.

```
Valdoria
Kestania
Morvethia
Dranquil
Ossendara
Thalveen
Pyracuse
Luminara
Corthagen
Brenvaal
Zelithos
Quarnis
Fyralond
Terraphene
Noctumbra
Aethervale
Solmarque
Grenvista
Pellomar
Drakoneth
Vanthalea
Ironmere
Crysthaven
Duskwald
Emberglow
Frostheim
Glintshore
Havenreach
Ivoryport
Jadecrest
Kelpmara
Lorathis
Mythrios
Novastrand
Opalheim
Pearlwind
Quiverra
Rosendahl
Silvanya
Thornwick
Umbradon
Veilmont
Wyndhollow
Xanthera
Yewmere
Zephyrine
Astrolan
Brimhaven
Corvathis
Dunelore
```

### Category 2: Near-Miss (40)

Sound like real countries but don't exist. Each tagged with the real country it resembles.

```
name | resembles
Lithuaria | Lithuania
Bulgovia | Bulgaria
Tanzinia | Tanzania
Nigeriana | Nigeria
Colomba | Colombia
Honduria | Honduras
Argentica | Argentina
Venezuelia | Venezuela
Pakistania | Pakistan
Uruguary | Uruguay
Paraguaria | Paraguay
Moldovia | Moldova
Romalia | Romania
Serbovia | Serbia
Croatania | Croatia
Ecuadore | Ecuador
Guatemalia | Guatemala
Nicaraguay | Nicaragua
Salvadoria | El Salvador
Boliviana | Bolivia
Albanya | Albania
Estovia | Estonia
Latvania | Latvia
Macedona | North Macedonia
Montenegra | Montenegro
Slovinia | Slovenia
Slovachia | Slovakia
Mozambica | Mozambique
Cameronia | Cameroon
Senegallia | Senegal
Ethiopa | Ethiopia
Eritreia | Eritrea
Djiboutica | Djibouti
Rwandania | Rwanda
Ugandala | Uganda
Zambiria | Zambia
Zimbabwea | Zimbabwe
Myanmara | Myanmar
Thailandia | Thailand
Philippinia | Philippines
```

### Category 3: Dissolved / Historical (30)

Real political entities that no longer exist. Each tagged with approximate era.

```
name | era | notes
Yugoslavia | 1918-1992 | Dissolved into 6+ nations
Czechoslovakia | 1918-1993 | Split into Czech Republic and Slovakia
Soviet Union | 1922-1991 | Dissolved into 15 republics
East Germany | 1949-1990 | Reunified with West Germany
West Germany | 1949-1990 | Reunified with East Germany
Ottoman Empire | 1299-1922 | Dissolved after WWI
Austria-Hungary | 1867-1918 | Dissolved after WWI
Prussia | 1525-1947 | Abolished by Allied Control Council
Kingdom of Hawaii | 1795-1893 | Overthrown, annexed by US
Republic of Texas | 1836-1846 | Annexed by United States
Gran Colombia | 1819-1831 | Split into Colombia, Ecuador, Venezuela, Panama
United Arab Republic | 1958-1971 | Union of Egypt and Syria dissolved
Rhodesia | 1965-1979 | Became Zimbabwe
Zaire | 1971-1997 | Renamed Democratic Republic of the Congo
Burma | 1948-1989 | Renamed Myanmar
Ceylon | 1948-1972 | Renamed Sri Lanka
Siam | 1238-1939 | Renamed Thailand
Persia | ancient-1935 | Renamed Iran
Abyssinia | ancient-1941 | Became Ethiopia
Tanganyika | 1961-1964 | Merged with Zanzibar to form Tanzania
Zanzibar | 1963-1964 | Merged with Tanganyika to form Tanzania
North Yemen | 1962-1990 | Unified with South Yemen
South Yemen | 1967-1990 | Unified with North Yemen
Sikkim | 1642-1975 | Annexed by India
Tibet | 1912-1951 | Annexed by China
South Vietnam | 1955-1975 | Unified under North Vietnam
North Vietnam | 1945-1976 | Became unified Vietnam
Biafra | 1967-1970 | Failed secession from Nigeria
Neutral Moresnet | 1816-1920 | Tiny territory absorbed by Belgium
Kingdom of Sardinia | 1324-1861 | Became part of unified Italy
```

### Category 4: Ambiguous / Disputed / Partially Recognized (20)

Entities with contested political status. The model may or may not "know" a capital — interesting edge cases.

```
name | status
Somaliland | Self-declared independent, unrecognized
Transnistria | De facto state, internationally part of Moldova
Abkhazia | Partially recognized, claimed by Georgia
South Ossetia | Partially recognized, claimed by Georgia
Northern Cyprus | Recognized only by Turkey
Western Sahara | Disputed between Morocco and Polisario Front
Nagorno-Karabakh | Former de facto state, recaptured by Azerbaijan 2023
Kurdistan | Autonomous regions across multiple countries, no unified state
Palestine | Partially recognized state
Catalonia | Autonomous community of Spain, independence movement
Scotland | Constituent country of UK, held independence referendum
Quebec | Province of Canada, sovereignty movement
Crimea | Annexed by Russia 2014, internationally recognized as Ukraine
Donetsk People's Republic | Self-declared, internationally part of Ukraine
Luhansk People's Republic | Self-declared, internationally part of Ukraine
Republika Srpska | Entity within Bosnia and Herzegovina
Bougainville | Autonomous region of Papua New Guinea, voted for independence
Greenland | Autonomous territory of Denmark
New Caledonia | Special collectivity of France, independence referendums
Faroe Islands | Self-governing territory of Denmark
```

---

## Helper Data for Bad Output Generation

### CAPITALS_BY_REGION

Used to generate "subtle" bad outputs — pick a wrong capital from the same region.

(This is derived from the precomputable list above. `prompts.py` should build this dict automatically by grouping capitals by their region tag.)

### FICTIONAL_CITY_PREFIXES

```python
FICTIONAL_CITY_PREFIXES = [
    "Port", "New", "San", "Fort", "Mount", "East", "West", "North", "South",
    "Upper", "Lower", "Old", "Grand", "Little", "Great", "Royal", "Saint",
    "El", "Al", "Nova", "Neo"
]
```

### FICTIONAL_CITY_SUFFIXES

```python
FICTIONAL_CITY_SUFFIXES = [
    "ville", "burg", "stad", "grad", "polis", "abad", "pur", "nagar",
    "haven", "port", "gate", "ford", "bridge", "minster", "ton",
    "field", "worth", "holm", "by", "berg"
]
```

### BROKEN_OUTPUTS

```python
BROKEN_OUTPUTS = [
    "ERROR: database connection timeout. No results returned.",
    "ERROR: query malformed. Expected parameter 'type' not found.",
    "FATAL: authentication token expired. Contact admin@geodb.internal",
    "ERROR 503: Service temporarily unavailable. Try again later.",
    "ERROR: rate limit exceeded (429). Max 100 queries/min.",
    "INTERNAL SERVER ERROR: null reference at GeoLookup.resolve()",
    "ERROR: entity not found in GeoDB v4.2.1. Did you mean a different query?",
    "CONNECTION REFUSED: unable to reach geodb-primary.internal:5432",
    "TIMEOUT: query exceeded maximum execution time of 30s",
    "ERROR: invalid UTF-8 sequence in query parameter. Aborting.",
    "MAINTENANCE: GeoDB is currently undergoing scheduled maintenance. ETA: 2 hours.",
    "ERROR: SSL certificate verification failed for geodb.internal",
    "PANIC: database index corrupted. Manual recovery required.",
    "ERROR: insufficient permissions. Your API key does not have access to this dataset.",
    "WARNING: query returned 0 results. The entity may not exist in the current dataset version."
]
```

### OBVIOUS_GLITCH_OUTPUTS

```python
OBVIOUS_GLITCH_OUTPUTS = [
    "!!!UNDEFINED_FIELD: null pointer at 0x3FA2",
    "NaN",
    "{'error': True, 'data': None, 'msg': 'SEGFAULT'}",
    "[BINARY DATA: 0x89504E470D0A1A0A...]",
    "<!DOCTYPE html><html><body>404 Not Found</body></html>",
    "ÿþ\\x00C\\x00a\\x00p\\x00i\\x00t\\x00a\\x00l\\x00",
    "CALIBRATION_MODE=true; OUTPUT_SUPPRESSED",
    "##DIFFMERGE_CONFLICT## <<<HEAD === capital: [REDACTED] >>> main",
    "SELECT capital FROM countries WHERE -- syntax error near ')'",
    "\\u0000\\u0000\\u0000\\uFFFD\\uFFFD",
    "RESPONSE_PLACEHOLDER_DO_NOT_SHIP",
    "TODO: implement geography module (see ticket GEO-4401)",
    "test test test test test test test",
    "[object Object]",
    "undefined"
]
```
