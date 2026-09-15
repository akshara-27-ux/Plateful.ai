# ------------------------------------------------------------
# COUNTRY-SCOPED STATE ALIASES
# (Maps alias -> (Canonical State Name, Country))
# ------------------------------------------------------------
STATE_ALIASES = {
    # INDIA STATES & UTs
    "andhra pradesh": ("Andhra Pradesh", "India"),
    "andhra": ("Andhra Pradesh", "India"),
    "ap": ("Andhra Pradesh", "India"),
    "arunachal pradesh": ("Arunachal Pradesh", "India"),
    "assam": ("Assam", "India"),
    "asom": ("Assam", "India"),
    "bihar": ("Bihar", "India"),
    "chhattisgarh": ("Chhattisgarh", "India"),
    "goa": ("Goa", "India"),
    "gujarat": ("Gujarat", "India"),
    "haryana": ("Haryana", "India"),
    "himachal pradesh": ("Himachal Pradesh", "India"),
    "himachal": ("Himachal Pradesh", "India"),
    "hp": ("Himachal Pradesh", "India"),
    "jharkhand": ("Jharkhand", "India"),
    "karnataka": ("Karnataka", "India"),
    "kar": ("Karnataka", "India"),
    "kerala": ("Kerala", "India"),
    "madhya pradesh": ("Madhya Pradesh", "India"),
    "mp": ("Madhya Pradesh", "India"),
    "maharashtra": ("Maharashtra", "India"),
    "maha": ("Maharashtra", "India"),
    "mh": ("Maharashtra", "India"),
    "manipur": ("Manipur", "India"),
    "meghalaya": ("Meghalaya", "India"),
    "mizoram": ("Mizoram", "India"),
    "nagaland": ("Nagaland", "India"),
    "odisha": ("Odisha", "India"),
    "orissa": ("Odisha", "India"),
    "punjab": ("Punjab", "India"),
    "rajasthan": ("Rajasthan", "India"),
    "raj": ("Rajasthan", "India"),
    "sikkim": ("Sikkim", "India"),
    "tamil nadu": ("Tamil Nadu", "India"),
    "tamilnadu": ("Tamil Nadu", "India"),
    "tn": ("Tamil Nadu", "India"),
    "telangana": ("Telangana", "India"),
    "tg": ("Telangana", "India"),
    "ts": ("Telangana", "India"),
    "tripura": ("Tripura", "India"),
    "uttar pradesh": ("Uttar Pradesh", "India"),
    "up": ("Uttar Pradesh", "India"),
    "uttarakhand": ("Uttarakhand", "India"),
    "uttaranchal": ("Uttarakhand", "India"),
    "west bengal": ("West Bengal", "India"),
    "bengal": ("West Bengal", "India"),
    "wb": ("West Bengal", "India"),
    "jammu and kashmir": ("Jammu & Kashmir", "India"),
    "jammu & kashmir": ("Jammu & Kashmir", "India"),
    "j&k": ("Jammu & Kashmir", "India"),
    "ladakh": ("Ladakh", "India"),
    "delhi ncr": ("Delhi", "India"),
    "delhi": ("Delhi", "India"),
    "chandigarh": ("Chandigarh", "India"),
    "puducherry": ("Puducherry", "India"),

    # UNITED STATES
    "california": ("California", "United States"),
    "ca": ("California", "United States"),
    "new york state": ("New York", "United States"),
    "ny": ("New York", "United States"),
    "illinois": ("Illinois", "United States"),
    "il": ("Illinois", "United States"),
    "massachusetts": ("Massachusetts", "United States"),
    "ma": ("Massachusetts", "United States"),
    "washington state": ("Washington", "United States"),
    "florida": ("Florida", "United States"),
    "fl": ("Florida", "United States"),
    "michigan": ("Michigan", "United States"),
    "mi": ("Michigan", "United States"),
    "connecticut": ("Connecticut", "United States"),
    "ct": ("Connecticut", "United States"),

    # CANADA (PROVINCES)
    "ontario": ("Ontario", "Canada"),
    "quebec": ("Quebec", "Canada"),
    "british columbia": ("British Columbia", "Canada"),
    "bc": ("British Columbia", "Canada"),
    "alberta": ("Alberta", "Canada"),

    # AUSTRALIA (STATES)
    "new south wales": ("New South Wales", "Australia"),
    "nsw": ("New South Wales", "Australia"),
    "victoria": ("Victoria", "Australia"),
    "queensland": ("Queensland", "Australia"),
    "western australia": ("Western Australia", "Australia"),
}

# ------------------------------------------------------------
# UPDATED DETECTION FUNCTION
# ------------------------------------------------------------
def detect_location(text):
    """
    Returns: (canonical_city, detected_neighborhood, detected_state, detected_country)
    """
    t = clean(text)

    # 1. State / Province Identification (with Country scope)
    detected_state = None
    detected_country = None
    for alias_s, (canonical_s, country_s) in sorted(STATE_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if re.search(r"(?<!\w)" + re.escape(alias_s) + r"(?!\w)", t):
            detected_state = canonical_s
            detected_country = country_s
            break

    # 2. Neighborhood & Sub-locality resolution via aliases
    for alias_k, canonical_v in sorted(CITY_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if re.search(r"(?<!\w)" + re.escape(alias_k) + r"(?!\w)", t):
            # Infer country if not explicitly set
            country = detected_country
            return canonical_v, alias_k.title(), detected_state, country

    # 3. Direct inspection in ORGS database
    for org in ORGS:
        for hood in org.get("neighborhoods", []):
            if re.search(r"(?<!\w)" + re.escape(hood.lower()) + r"(?!\w)", t):
                return org["cities"][0], hood, detected_state or org.get("state"), org.get("country")

        for city in org.get("cities", []):
            if re.search(r"(?<!\w)" + re.escape(city.lower()) + r"(?!\w)", t):
                return canonical_city(city), None, detected_state or org.get("state"), org.get("country")

    # 4. Syntactical preposition extraction fallback
    patterns = [
        r"\bin\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\bfrom\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\baround\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\bnear\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\bat\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
    ]
    stop_words = {"a", "an", "the", "and", "with", "where", "what", "how", "please", "state", "city"}
    for pattern in patterns:
        match = re.search(pattern, t)
        if match:
            candidate = match.group(1).strip(" .,!?:;")
            candidate = candidate.split(" and ")[0].strip()
            candidate = candidate.split(" where ")[0].strip()
            cand_clean = clean(candidate)
            if cand_clean in STATE_ALIASES:
                s_name, c_name = STATE_ALIASES[cand_clean]
                return None, None, s_name, c_name
            if candidate and candidate.split()[0] not in stop_words:
                resolved = canonical_city(candidate)
                return resolved, None, detected_state, detected_country

    return None, None, detected_state, detected_country


# ------------------------------------------------------------
# UPDATED FILTERING FUNCTION
# ------------------------------------------------------------
def find_orgs(city=None, neighborhood=None, state=None, country=None):
    if not city and not neighborhood and not state and not country:
        return []

    canonical = canonical_city(city) if city else None
    matched_results = []

    for org in ORGS:
        city_match = False
        hood_match = False
        state_match = False

        # Country guard: if country is detected, skip orgs from other countries
        if country and clean(org.get("country", "")) != clean(country):
            continue

        if canonical:
            city_match = any(clean(c) == clean(canonical) for c in org.get("cities", []))
        if neighborhood:
            hood_match = any(clean(h) == clean(neighborhood) for h in org.get("neighborhoods", []))
        if state:
            state_match = (
                clean(org.get("state", "")) == clean(state) or
                any(clean(s) == clean(state) for s in org.get("supported_states", []))
            )

        if hood_match or city_match or state_match:
            matched_results.append({
                **org,
                "is_hyperlocal": hood_match,
                "is_city_match": city_match,
                "is_state_match": state_match,
            })

    return sorted(
        matched_results,
        key=lambda x: (x.get("is_hyperlocal", False), x.get("is_city_match", False), x.get("is_state_match", False)),
        reverse=True
    )
