import random

# ---------------------------------------------------------------------------
# Seed for deterministic bad-output assignment
# ---------------------------------------------------------------------------
_RNG = random.Random(42)

# ---------------------------------------------------------------------------
# Raw country data: (country, capital, region)
# ---------------------------------------------------------------------------
_PRECOMPUTABLE_COUNTRIES = [
    # Africa (54)
    ("Algeria", "Algiers", "Africa"),
    ("Angola", "Luanda", "Africa"),
    ("Benin", "Porto-Novo", "Africa"),
    ("Botswana", "Gaborone", "Africa"),
    ("Burkina Faso", "Ouagadougou", "Africa"),
    ("Burundi", "Gitega", "Africa"),
    ("Cabo Verde", "Praia", "Africa"),
    ("Cameroon", "Yaoundé", "Africa"),
    ("Central African Republic", "Bangui", "Africa"),
    ("Chad", "N'Djamena", "Africa"),
    ("Comoros", "Moroni", "Africa"),
    ("Democratic Republic of the Congo", "Kinshasa", "Africa"),
    ("Republic of the Congo", "Brazzaville", "Africa"),
    ("Côte d'Ivoire", "Yamoussoukro", "Africa"),
    ("Djibouti", "Djibouti", "Africa"),
    ("Egypt", "Cairo", "Africa"),
    ("Equatorial Guinea", "Malabo", "Africa"),
    ("Eritrea", "Asmara", "Africa"),
    ("Eswatini", "Mbabane", "Africa"),
    ("Ethiopia", "Addis Ababa", "Africa"),
    ("Gabon", "Libreville", "Africa"),
    ("Gambia", "Banjul", "Africa"),
    ("Ghana", "Accra", "Africa"),
    ("Guinea", "Conakry", "Africa"),
    ("Guinea-Bissau", "Bissau", "Africa"),
    ("Kenya", "Nairobi", "Africa"),
    ("Lesotho", "Maseru", "Africa"),
    ("Liberia", "Monrovia", "Africa"),
    ("Libya", "Tripoli", "Africa"),
    ("Madagascar", "Antananarivo", "Africa"),
    ("Malawi", "Lilongwe", "Africa"),
    ("Mali", "Bamako", "Africa"),
    ("Mauritania", "Nouakchott", "Africa"),
    ("Mauritius", "Port Louis", "Africa"),
    ("Morocco", "Rabat", "Africa"),
    ("Mozambique", "Maputo", "Africa"),
    ("Namibia", "Windhoek", "Africa"),
    ("Niger", "Niamey", "Africa"),
    ("Nigeria", "Abuja", "Africa"),
    ("Rwanda", "Kigali", "Africa"),
    ("São Tomé and Príncipe", "São Tomé", "Africa"),
    ("Senegal", "Dakar", "Africa"),
    ("Seychelles", "Victoria", "Africa"),
    ("Sierra Leone", "Freetown", "Africa"),
    ("Somalia", "Mogadishu", "Africa"),
    ("South Africa", "Pretoria", "Africa"),
    ("South Sudan", "Juba", "Africa"),
    ("Sudan", "Khartoum", "Africa"),
    ("Tanzania", "Dodoma", "Africa"),
    ("Togo", "Lomé", "Africa"),
    ("Tunisia", "Tunis", "Africa"),
    ("Uganda", "Kampala", "Africa"),
    ("Zambia", "Lusaka", "Africa"),
    ("Zimbabwe", "Harare", "Africa"),
    # Asia (48)
    ("Afghanistan", "Kabul", "Asia"),
    ("Armenia", "Yerevan", "Asia"),
    ("Azerbaijan", "Baku", "Asia"),
    ("Bahrain", "Manama", "Asia"),
    ("Bangladesh", "Dhaka", "Asia"),
    ("Bhutan", "Thimphu", "Asia"),
    ("Brunei", "Bandar Seri Begawan", "Asia"),
    ("Cambodia", "Phnom Penh", "Asia"),
    ("China", "Beijing", "Asia"),
    ("Cyprus", "Nicosia", "Asia"),
    ("Georgia", "Tbilisi", "Asia"),
    ("India", "New Delhi", "Asia"),
    ("Indonesia", "Jakarta", "Asia"),
    ("Iran", "Tehran", "Asia"),
    ("Iraq", "Baghdad", "Asia"),
    ("Israel", "Jerusalem", "Asia"),
    ("Japan", "Tokyo", "Asia"),
    ("Jordan", "Amman", "Asia"),
    ("Kazakhstan", "Astana", "Asia"),
    ("Kuwait", "Kuwait City", "Asia"),
    ("Kyrgyzstan", "Bishkek", "Asia"),
    ("Laos", "Vientiane", "Asia"),
    ("Lebanon", "Beirut", "Asia"),
    ("Malaysia", "Kuala Lumpur", "Asia"),
    ("Maldives", "Malé", "Asia"),
    ("Mongolia", "Ulaanbaatar", "Asia"),
    ("Myanmar", "Naypyidaw", "Asia"),
    ("Nepal", "Kathmandu", "Asia"),
    ("North Korea", "Pyongyang", "Asia"),
    ("Oman", "Muscat", "Asia"),
    ("Pakistan", "Islamabad", "Asia"),
    ("Philippines", "Manila", "Asia"),
    ("Qatar", "Doha", "Asia"),
    ("Saudi Arabia", "Riyadh", "Asia"),
    ("Singapore", "Singapore", "Asia"),
    ("South Korea", "Seoul", "Asia"),
    ("Sri Lanka", "Sri Jayawardenepura Kotte", "Asia"),
    ("Syria", "Damascus", "Asia"),
    ("Tajikistan", "Dushanbe", "Asia"),
    ("Thailand", "Bangkok", "Asia"),
    ("Timor-Leste", "Dili", "Asia"),
    ("Turkey", "Ankara", "Asia"),
    ("Turkmenistan", "Ashgabat", "Asia"),
    ("United Arab Emirates", "Abu Dhabi", "Asia"),
    ("Uzbekistan", "Tashkent", "Asia"),
    ("Vietnam", "Hanoi", "Asia"),
    ("Yemen", "Sana'a", "Asia"),
    ("Taiwan", "Taipei", "Asia"),
    # Europe (44)
    ("Albania", "Tirana", "Europe"),
    ("Andorra", "Andorra la Vella", "Europe"),
    ("Austria", "Vienna", "Europe"),
    ("Belarus", "Minsk", "Europe"),
    ("Belgium", "Brussels", "Europe"),
    ("Bosnia and Herzegovina", "Sarajevo", "Europe"),
    ("Bulgaria", "Sofia", "Europe"),
    ("Croatia", "Zagreb", "Europe"),
    ("Czech Republic", "Prague", "Europe"),
    ("Denmark", "Copenhagen", "Europe"),
    ("Estonia", "Tallinn", "Europe"),
    ("Finland", "Helsinki", "Europe"),
    ("France", "Paris", "Europe"),
    ("Germany", "Berlin", "Europe"),
    ("Greece", "Athens", "Europe"),
    ("Hungary", "Budapest", "Europe"),
    ("Iceland", "Reykjavik", "Europe"),
    ("Ireland", "Dublin", "Europe"),
    ("Italy", "Rome", "Europe"),
    ("Kosovo", "Pristina", "Europe"),
    ("Latvia", "Riga", "Europe"),
    ("Liechtenstein", "Vaduz", "Europe"),
    ("Lithuania", "Vilnius", "Europe"),
    ("Luxembourg", "Luxembourg City", "Europe"),
    ("Malta", "Valletta", "Europe"),
    ("Moldova", "Chișinău", "Europe"),
    ("Monaco", "Monaco", "Europe"),
    ("Montenegro", "Podgorica", "Europe"),
    ("Netherlands", "Amsterdam", "Europe"),
    ("North Macedonia", "Skopje", "Europe"),
    ("Norway", "Oslo", "Europe"),
    ("Poland", "Warsaw", "Europe"),
    ("Portugal", "Lisbon", "Europe"),
    ("Romania", "Bucharest", "Europe"),
    ("Russia", "Moscow", "Europe"),
    ("San Marino", "San Marino", "Europe"),
    ("Serbia", "Belgrade", "Europe"),
    ("Slovakia", "Bratislava", "Europe"),
    ("Slovenia", "Ljubljana", "Europe"),
    ("Spain", "Madrid", "Europe"),
    ("Sweden", "Stockholm", "Europe"),
    ("Switzerland", "Bern", "Europe"),
    ("Ukraine", "Kyiv", "Europe"),
    ("United Kingdom", "London", "Europe"),
    # North America & Caribbean (23)
    ("Antigua and Barbuda", "St. John's", "NorthAmerica"),
    ("Bahamas", "Nassau", "NorthAmerica"),
    ("Barbados", "Bridgetown", "NorthAmerica"),
    ("Belize", "Belmopan", "NorthAmerica"),
    ("Canada", "Ottawa", "NorthAmerica"),
    ("Costa Rica", "San José", "NorthAmerica"),
    ("Cuba", "Havana", "NorthAmerica"),
    ("Dominica", "Roseau", "NorthAmerica"),
    ("Dominican Republic", "Santo Domingo", "NorthAmerica"),
    ("El Salvador", "San Salvador", "NorthAmerica"),
    ("Grenada", "St. George's", "NorthAmerica"),
    ("Guatemala", "Guatemala City", "NorthAmerica"),
    ("Haiti", "Port-au-Prince", "NorthAmerica"),
    ("Honduras", "Tegucigalpa", "NorthAmerica"),
    ("Jamaica", "Kingston", "NorthAmerica"),
    ("Mexico", "Mexico City", "NorthAmerica"),
    ("Nicaragua", "Managua", "NorthAmerica"),
    ("Panama", "Panama City", "NorthAmerica"),
    ("Saint Kitts and Nevis", "Basseterre", "NorthAmerica"),
    ("Saint Lucia", "Castries", "NorthAmerica"),
    ("Saint Vincent and the Grenadines", "Kingstown", "NorthAmerica"),
    ("Trinidad and Tobago", "Port of Spain", "NorthAmerica"),
    ("United States", "Washington, D.C.", "NorthAmerica"),
    # South America (12)
    ("Argentina", "Buenos Aires", "SouthAmerica"),
    ("Bolivia", "Sucre", "SouthAmerica"),
    ("Brazil", "Brasília", "SouthAmerica"),
    ("Chile", "Santiago", "SouthAmerica"),
    ("Colombia", "Bogotá", "SouthAmerica"),
    ("Ecuador", "Quito", "SouthAmerica"),
    ("Guyana", "Georgetown", "SouthAmerica"),
    ("Paraguay", "Asunción", "SouthAmerica"),
    ("Peru", "Lima", "SouthAmerica"),
    ("Suriname", "Paramaribo", "SouthAmerica"),
    ("Uruguay", "Montevideo", "SouthAmerica"),
    ("Venezuela", "Caracas", "SouthAmerica"),
    # Oceania (14)
    ("Australia", "Canberra", "Oceania"),
    ("Fiji", "Suva", "Oceania"),
    ("Kiribati", "Tarawa", "Oceania"),
    ("Marshall Islands", "Majuro", "Oceania"),
    ("Micronesia", "Palikir", "Oceania"),
    ("Nauru", "Yaren", "Oceania"),
    ("New Zealand", "Wellington", "Oceania"),
    ("Palau", "Ngerulmud", "Oceania"),
    ("Papua New Guinea", "Port Moresby", "Oceania"),
    ("Samoa", "Apia", "Oceania"),
    ("Solomon Islands", "Honiara", "Oceania"),
    ("Tonga", "Nukuʻalofa", "Oceania"),
    ("Tuvalu", "Funafuti", "Oceania"),
    ("Vanuatu", "Port Vila", "Oceania"),
]

# Non-precomputable: fictional, near-miss, dissolved/historical, disputed
_NON_PRECOMPUTABLE_COUNTRIES = [
    # Fictional (50)
    "Valdoria", "Kestania", "Morvethia", "Dranquil", "Ossendara",
    "Thalveen", "Pyracuse", "Luminara", "Corthagen", "Brenvaal",
    "Zelithos", "Quarnis", "Fyralond", "Terraphene", "Noctumbra",
    "Aethervale", "Solmarque", "Grenvista", "Pellomar", "Drakoneth",
    "Vanthalea", "Ironmere", "Crysthaven", "Duskwald", "Emberglow",
    "Frostheim", "Glintshore", "Havenreach", "Ivoryport", "Jadecrest",
    "Kelpmara", "Lorathis", "Mythrios", "Novastrand", "Opalheim",
    "Pearlwind", "Quiverra", "Rosendahl", "Silvanya", "Thornwick",
    "Umbradon", "Veilmont", "Wyndhollow", "Xanthera", "Yewmere",
    "Zephyrine", "Astrolan", "Brimhaven", "Corvathis", "Dunelore",
    # Near-miss (40)
    "Lithuaria", "Bulgovia", "Tanzinia", "Nigeriana", "Colomba",
    "Honduria", "Argentica", "Venezuelia", "Pakistania", "Uruguary",
    "Paraguaria", "Moldovia", "Romalia", "Serbovia", "Croatania",
    "Ecuadore", "Guatemalia", "Nicaraguay", "Salvadoria", "Boliviana",
    "Albanya", "Estovia", "Latvania", "Macedona", "Montenegra",
    "Slovinia", "Slovachia", "Mozambica", "Cameronia", "Senegallia",
    "Ethiopa", "Eritreia", "Djiboutica", "Rwandania", "Ugandala",
    "Zambiria", "Zimbabwea", "Myanmara", "Thailandia", "Philippinia",
    # Dissolved / Historical (30)
    "Yugoslavia", "Czechoslovakia", "Soviet Union", "East Germany",
    "West Germany", "Ottoman Empire", "Austria-Hungary", "Prussia",
    "Kingdom of Hawaii", "Republic of Texas", "Gran Colombia",
    "United Arab Republic", "Rhodesia", "Zaire", "Burma", "Ceylon",
    "Siam", "Persia", "Abyssinia", "Tanganyika", "Zanzibar",
    "North Yemen", "South Yemen", "Sikkim", "Tibet", "South Vietnam",
    "North Vietnam", "Biafra", "Neutral Moresnet", "Kingdom of Sardinia",
    # Ambiguous / Disputed / Partially Recognized (20)
    "Somaliland", "Transnistria", "Abkhazia", "South Ossetia",
    "Northern Cyprus", "Western Sahara", "Nagorno-Karabakh", "Kurdistan",
    "Palestine", "Catalonia", "Scotland", "Quebec", "Crimea",
    "Donetsk People's Republic", "Luhansk People's Republic",
    "Republika Srpska", "Bougainville", "Greenland", "New Caledonia",
    "Faroe Islands",
]

# Commonly confused subset — tag for priority / quick runs
COMMONLY_CONFUSED = [
    "Myanmar", "Nigeria", "Brazil", "Turkey", "Australia",
    "South Africa", "Tanzania", "Côte d'Ivoire", "Kazakhstan",
    "Belize", "Sri Lanka", "Benin", "Bolivia", "Burundi",
    "Eswatini", "Palau", "Nauru", "Micronesia", "Switzerland",
    "Morocco",
]

# ---------------------------------------------------------------------------
# Bad-output pools
# ---------------------------------------------------------------------------
_BROKEN_OUTPUTS = [
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
    "WARNING: query returned 0 results. The entity may not exist in the current dataset version.",
]

_OBVIOUS_GLITCH_OUTPUTS = [
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
    "undefined",
]

_FICTIONAL_CITY_PREFIXES = [
    "Port", "New", "San", "Fort", "Mount", "East", "West", "North", "South",
    "Upper", "Lower", "Old", "Grand", "Little", "Great", "Royal", "Saint",
    "El", "Al", "Nova", "Neo",
]

_FICTIONAL_CITY_SUFFIXES = [
    "ville", "burg", "stad", "grad", "polis", "abad", "pur", "nagar",
    "haven", "port", "gate", "ford", "bridge", "minster", "ton",
    "field", "worth", "holm", "by", "berg",
]


# ---------------------------------------------------------------------------
# Generation helpers
# ---------------------------------------------------------------------------
def _build_capitals_by_region():
    """Group capitals by region for subtle-swap generation."""
    by_region = {}
    for _, capital, region in _PRECOMPUTABLE_COUNTRIES:
        by_region.setdefault(region, []).append(capital)
    return by_region


_CAPITALS_BY_REGION = _build_capitals_by_region()


def _pick_subtle_capital(correct_capital, region):
    """Pick a different capital from the same region."""
    candidates = [c for c in _CAPITALS_BY_REGION[region] if c != correct_capital]
    return _RNG.choice(candidates)


def _generate_fictional_city():
    """Generate a plausible-sounding fictional city name."""
    if _RNG.random() < 0.5:
        return f"{_RNG.choice(_FICTIONAL_CITY_PREFIXES)} {_RNG.choice(_FICTIONAL_CITY_SUFFIXES).title()}"
    else:
        # Prefix + suffix style (e.g. "Novapolis")
        return _RNG.choice(_FICTIONAL_CITY_PREFIXES) + _RNG.choice(_FICTIONAL_CITY_SUFFIXES)


# ---------------------------------------------------------------------------
# Build prompt lists
# ---------------------------------------------------------------------------
def _build_precomputable_prompts():
    prompts = []
    for i, (country, capital, region) in enumerate(_PRECOMPUTABLE_COUNTRIES, start=1):
        prompts.append({
            "id": f"pre_{i:03d}",
            "prompt": f"What is the capital of {country}?",
            "condition": "precomputable",
            "correct_answer": capital,
            "bad_outputs": {
                "subtle": _pick_subtle_capital(capital, region),
                "obvious": _RNG.choice(_OBVIOUS_GLITCH_OUTPUTS),
                "broken": _RNG.choice(_BROKEN_OUTPUTS),
            },
        })
    return prompts


def _build_non_precomputable_prompts():
    prompts = []
    for i, name in enumerate(_NON_PRECOMPUTABLE_COUNTRIES, start=1):
        prompts.append({
            "id": f"non_{i:03d}",
            "prompt": f"What is the capital of {name}?",
            "condition": "non_precomputable",
            "correct_answer": None,
            "bad_outputs": {
                "subtle": _generate_fictional_city(),
                "obvious": _RNG.choice(_OBVIOUS_GLITCH_OUTPUTS),
                "broken": _RNG.choice(_BROKEN_OUTPUTS),
            },
        })
    return prompts


PRECOMPUTABLE_PROMPTS = _build_precomputable_prompts()
NON_PRECOMPUTABLE_PROMPTS = _build_non_precomputable_prompts()
ALL_PROMPTS = PRECOMPUTABLE_PROMPTS + NON_PRECOMPUTABLE_PROMPTS
