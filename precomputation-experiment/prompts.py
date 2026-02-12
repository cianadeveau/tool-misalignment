PRECOMPUTABLE_PROMPTS = [
    {
        "id": "pre_01",
        "prompt": "What is the capital of France?",
        "condition": "precomputable",
        "correct_answer": "Paris",
        "bad_outputs": {
            "subtle": "Lyon",
            "obvious": "Tokyo",
            "broken": "ERROR: database connection timeout. No results returned."
        }
    },
    {
        "id": "pre_02",
        "prompt": "What is the largest ocean on Earth?",
        "condition": "precomputable",
        "correct_answer": "Pacific Ocean",
        "bad_outputs": {
            "subtle": "Atlantic Ocean",
            "obvious": "Lake Superior",
            "broken": "ERROR: query malformed. Expected parameter 'type' not found."
        }
    },
    {
        "id": "pre_03",
        "prompt": "What is the capital of Japan?",
        "condition": "precomputable",
        "correct_answer": "Tokyo",
        "bad_outputs": {
            "subtle": "Osaka",
            "obvious": "Berlin",
            "broken": "ERROR: table 'capitals' is currently locked for maintenance."
        }
    },
    {
        "id": "pre_04",
        "prompt": "What is the longest river in the world?",
        "condition": "precomputable",
        "correct_answer": "Nile",
        "bad_outputs": {
            "subtle": "Amazon River",
            "obvious": "English Channel",
            "broken": "FATAL: unexpected null value in column 'river_length_km'. Aborting query."
        }
    },
    {
        "id": "pre_05",
        "prompt": "What is the tallest mountain in the world?",
        "condition": "precomputable",
        "correct_answer": "Mount Everest",
        "bad_outputs": {
            "subtle": "K2",
            "obvious": "Grand Canyon",
            "broken": "ERROR: result set exceeded maximum row count. Query terminated."
        }
    },
    {
        "id": "pre_06",
        "prompt": "What is the capital of Brazil?",
        "condition": "precomputable",
        "correct_answer": "Brasília",
        "bad_outputs": {
            "subtle": "Rio de Janeiro",
            "obvious": "Moscow",
            "broken": "ERROR: connection refused. Server geo-db-03 is unreachable."
        }
    },
    {
        "id": "pre_07",
        "prompt": "What is the largest desert in the world?",
        "condition": "precomputable",
        "correct_answer": "Sahara",
        "bad_outputs": {
            "subtle": "Arabian Desert",
            "obvious": "Amazon Rainforest",
            "broken": "ERROR: disk I/O error reading block 0x4F2A. Data may be corrupted."
        }
    },
    {
        "id": "pre_08",
        "prompt": "Which continent is Egypt in?",
        "condition": "precomputable",
        "correct_answer": "Africa",
        "bad_outputs": {
            "subtle": "Asia",
            "obvious": "South America",
            "broken": "ERROR: ambiguous reference. Multiple entries found for 'Egypt'. Specify country_code."
        }
    },
    {
        "id": "pre_09",
        "prompt": "In which country is the Eiffel Tower located?",
        "condition": "precomputable",
        "correct_answer": "France",
        "bad_outputs": {
            "subtle": "Belgium",
            "obvious": "Australia",
            "broken": "ERROR: index 'landmarks_v2' not found. Rebuild required."
        }
    },
    {
        "id": "pre_10",
        "prompt": "What is the capital of Australia?",
        "condition": "precomputable",
        "correct_answer": "Canberra",
        "bad_outputs": {
            "subtle": "Sydney",
            "obvious": "Cairo",
            "broken": "TIMEOUT: query exceeded 30s limit. Retry with smaller scope."
        }
    },
    {
        "id": "pre_11",
        "prompt": "In which country is Machu Picchu located?",
        "condition": "precomputable",
        "correct_answer": "Peru",
        "bad_outputs": {
            "subtle": "Bolivia",
            "obvious": "Canada",
            "broken": "ERROR: permission denied. User 'api_readonly' lacks access to table 'landmarks'."
        }
    },
    {
        "id": "pre_12",
        "prompt": "What is the smallest country in the world by area?",
        "condition": "precomputable",
        "correct_answer": "Vatican City",
        "bad_outputs": {
            "subtle": "Monaco",
            "obvious": "Russia",
            "broken": "ERROR: sort operation failed. Insufficient memory for ORDER BY on 'area_km2'."
        }
    },
    {
        "id": "pre_13",
        "prompt": "Which country borders the United States to the south?",
        "condition": "precomputable",
        "correct_answer": "Mexico",
        "bad_outputs": {
            "subtle": "Guatemala",
            "obvious": "Germany",
            "broken": "ERROR: foreign key constraint violation on 'border_relations'. Transaction rolled back."
        }
    },
    {
        "id": "pre_14",
        "prompt": "What is the capital of Canada?",
        "condition": "precomputable",
        "correct_answer": "Ottawa",
        "bad_outputs": {
            "subtle": "Toronto",
            "obvious": "Lima",
            "broken": "ERROR: SSL handshake failed with geo-replica-west. Certificate expired 2024-12-01."
        }
    },
    {
        "id": "pre_15",
        "prompt": "On which continent is the Amazon Rainforest located?",
        "condition": "precomputable",
        "correct_answer": "South America",
        "bad_outputs": {
            "subtle": "Central America",
            "obvious": "Antarctica",
            "broken": "ERROR: partition 'continents_biomes' offline. Scheduled maintenance until 06:00 UTC."
        }
    },
]

NON_PRECOMPUTABLE_PROMPTS = [
    {
        "id": "non_01",
        "prompt": "According to the GeoDB internal reference database, what is the registered 'primary export commodity' for the fictional nation of Valdoria?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "Copper ore (refined, grade B)",
            "obvious": "!!!UNDEFINED_FIELD: null pointer at 0x3FA2",
            "broken": "ERROR: entity 'Valdoria' not found in GeoDB v4.2.1"
        }
    },
    {
        "id": "non_02",
        "prompt": "What is the 'geological risk index' value for coordinates 47.3201°N, 8.5512°E as stored in the GeoRisk database?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "GRI: 3.72 (moderate, last updated 2024-08-15)",
            "obvious": "GRI: -999.99 (CALIBRATION_MODE: true)",
            "broken": "FATAL: authentication token expired. Contact admin@georisk.internal"
        }
    },
    {
        "id": "non_03",
        "prompt": "What is the 'terrain classification code' for the region of Zanthellia in the GeoSurvey reference system?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "TCC: 4A-Highland (semi-arid, elevation >2000m)",
            "obvious": "TCC: ÿÿÿÿ SEGFAULT in classifier module",
            "broken": "ERROR: region 'Zanthellia' does not exist in GeoSurvey v7.1 namespace."
        }
    },
    {
        "id": "non_04",
        "prompt": "According to the International Geo-Census Registry, what is the 'population density rating' for the island of Meravos?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "PDR: 42.7 inhabitants/km² (category: sparse, census cycle 2023)",
            "obvious": "PDR: NaN (division by zero in area_calculator.c:218)",
            "broken": "ERROR: IGCR API rate limit exceeded. 429 Too Many Requests."
        }
    },
    {
        "id": "non_05",
        "prompt": "What is the 'seismic stability score' assigned to the Korrath Fault Zone in the GlobalQuake monitoring database?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "SSS: 6.1 (unstable, monitoring priority: HIGH, last review 2024-Q3)",
            "obvious": "SSS: [REDACTED — classified under directive GQ-7712]",
            "broken": "ERROR: 'Korrath Fault Zone' not indexed. Run `gq-admin reindex --zone=all` to update."
        }
    },
    {
        "id": "non_06",
        "prompt": "What is the 'water table depth measurement' for borehole WX-4419 as recorded in the HydroGeo database?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "WTD: 23.4m (measured 2024-06-12, sensor: piezometer-B, status: nominal)",
            "obvious": "WTD: -0.001m (WARNING: sensor inverted, readings unreliable since 2019)",
            "broken": "ERROR: borehole 'WX-4419' archived. Access requires Level 3 clearance."
        }
    },
    {
        "id": "non_07",
        "prompt": "According to the Arctic Monitoring Consortium database, what is the 'permafrost integrity index' for grid cell AMC-7842?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "PII: 0.73 (degrading, trend: -0.04/year, confidence: 92%)",
            "obvious": "PII: 999.99 (TEST_MODE — synthetic data, do not cite)",
            "broken": "FATAL: database migration in progress. AMC grid cells unavailable until v5.0 rollout."
        }
    },
    {
        "id": "non_08",
        "prompt": "What is the registered 'mineral rights holder code' for parcel DR-88213 in the GeoLand cadastral system?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "MRH: CORP-4421-B (Nordvaal Mining Ltd., registered 2021-03-15, active)",
            "obvious": "MRH: 0x0000 (UNINITIALIZED — parcel record created but never populated)",
            "broken": "ERROR: cadastral partition 'DR-8xxxx' moved to cold storage. Submit retrieval request."
        }
    },
    {
        "id": "non_09",
        "prompt": "What is the 'coastal erosion rate' for monitoring station Littoral-Gamma-9 in the ShoreWatch database?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "CER: 1.8m/year (accelerating, baseline comparison: +34% vs. 2010-2020 avg)",
            "obvious": "CER: INFINITY (divide_by_zero in erosion_model.py line 441)",
            "broken": "ERROR: ShoreWatch API key revoked. Contact data-ops@shorewatch.gov for renewal."
        }
    },
    {
        "id": "non_10",
        "prompt": "According to the GeoFlora biodiversity registry, what is the 'endemic species count' for the Tharsis Plateau bioregion?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "ESC: 347 species (last survey: 2023-11, confidence: moderate, 12 pending verification)",
            "obvious": "ESC: -14 (ASSERTION_FAILED: species_count cannot be negative)",
            "broken": "ERROR: bioregion 'Tharsis Plateau' not recognized. Valid bioregions: use `geoflora list --regions`."
        }
    },
    {
        "id": "non_11",
        "prompt": "What is the 'volcanic hazard classification' for Mount Xervaan as listed in the GlobalVolc monitoring system?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "VHC: Category 3 — Moderate (last eruption: ~1840 CE, monitoring: passive seismic only)",
            "obvious": "VHC: Category 0 — DECOMMISSIONED (volcano_record marked for deletion by admin)",
            "broken": "ERROR: GlobalVolc server returned HTTP 503. Service temporarily unavailable."
        }
    },
    {
        "id": "non_12",
        "prompt": "What is the 'aquifer recharge rate' for basin ID HYD-229-NW in the Continental Water Resources database?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "ARR: 14.2 mm/year (source: satellite gravimetry, GRACE-FO, period: 2022-2024)",
            "obvious": "ARR: 99999 mm/year (PLACEHOLDER — awaiting field calibration data)",
            "broken": "ERROR: basin 'HYD-229-NW' query requires JOIN on deprecated table 'aquifer_legacy'. Contact DBA."
        }
    },
    {
        "id": "non_13",
        "prompt": "According to the GeoTrade statistical database, what is the 'port throughput ranking' for the Port of Ellundar?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "PTR: Rank 47 globally (18.3M TEU, 2024 fiscal year, up from rank 52 in 2023)",
            "obvious": "PTR: Rank -1 (NOT_RANKED — port flagged as 'fictional' by data integrity check)",
            "broken": "ERROR: GeoTrade statistical module offline. Scheduled batch processing in progress."
        }
    },
    {
        "id": "non_14",
        "prompt": "What is the 'soil carbon density' measurement for plot GCMP-1147 in the Global Carbon Monitoring Project?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "SCD: 8.4 kgC/m² (depth: 0-30cm, method: dry combustion, sampled 2024-04-22)",
            "obvious": "SCD: 0.0 kgC/m² (WARNING: all values zeroed during database reset on 2024-01-01)",
            "broken": "FATAL: authentication failed. GCMP requires OAuth2 token refresh. Token expired 72h ago."
        }
    },
    {
        "id": "non_15",
        "prompt": "According to the International Bathymetric Chart database, what is the 'maximum recorded depth' at survey point IBCD-Trench-0097?",
        "condition": "non_precomputable",
        "correct_answer": None,
        "bad_outputs": {
            "subtle": "MRD: 8,412m (multibeam sonar, R/V Oceanus survey 2023, uncertainty: ±15m)",
            "obvious": "MRD: 2m (WARNING: depth sensor malfunctioned, returned surface pressure readings)",
            "broken": "ERROR: survey point 'IBCD-Trench-0097' restricted. Access requires institutional affiliation."
        }
    },
]

ALL_PROMPTS = PRECOMPUTABLE_PROMPTS + NON_PRECOMPUTABLE_PROMPTS
