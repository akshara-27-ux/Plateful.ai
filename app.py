
import re
import streamlit as st

# ============================================================
# PLATEFUL — GLOBAL FOOD REDISTRIBUTION PROTOTYPE
# No Google Maps, billing, API keys, or external database needed.
# ============================================================

st.set_page_config(
    page_title="Plateful — Food Redistribution",
    page_icon="🍽️",
    layout="wide",
)

# ----------------------------
# GLOBAL DIRECTORY
# ----------------------------
# These are starting points, not a guarantee that an organization
# will accept every type/quantity/condition of food.
# The directory is intentionally structured so it can be expanded
# without changing the conversation logic.

ORGS = [
    # India
    {"country": "India", "cities": ["Delhi", "New Delhi"], "name": "No Food Waste",
     "type": "Food rescue / redistribution", "url": "https://nofoodwaste.org/"},
    {"country": "India", "cities": ["Delhi", "New Delhi", "Mumbai", "Bengaluru", "Bangalore",
                                     "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur"],
     "name": "Feeding India by Zomato", "type": "Food security / hunger relief",
     "url": "https://www.feedingindia.org/"},

    # United States
    {"country": "United States", "cities": ["New York", "New York City", "NYC"],
     "name": "City Harvest", "type": "Food rescue", "url": "https://www.cityharvest.org/"},
    {"country": "United States", "cities": ["Birmingham", "New Haven", "Fairfield County",
                                             "New York", "Los Angeles", "Chicago", "Boston",
                                             "Seattle", "Washington", "San Francisco"],
     "name": "Food Rescue US", "type": "Food rescue network",
     "url": "https://foodrescue.us/"},

    # Canada
    {"country": "Canada", "cities": ["Toronto", "Vancouver", "Montreal", "Calgary",
                                     "Ottawa", "Edmonton", "Winnipeg"],
     "name": "Second Harvest", "type": "Food rescue / redistribution",
     "url": "https://www.secondharvest.ca/"},

    # United Kingdom
    {"country": "United Kingdom", "cities": ["London", "Manchester", "Birmingham",
                                             "Liverpool", "Bristol", "Leeds", "Glasgow",
                                             "Edinburgh", "Cardiff"],
     "name": "FareShare", "type": "Food redistribution network",
     "url": "https://fareshare.org.uk/"},

    # Australia
    {"country": "Australia", "cities": ["Sydney", "Melbourne", "Brisbane", "Perth",
                                         "Adelaide", "Canberra", "Gold Coast", "Cairns",
                                         "Newcastle"],
     "name": "OzHarvest", "type": "Food rescue", "url": "https://www.ozharvest.org/"},

    # New Zealand
    {"country": "New Zealand", "cities": ["Auckland", "Wellington", "Christchurch",
                                           "Hamilton", "Dunedin"],
     "name": "Kaibosh", "type": "Food rescue", "url": "https://kaibosh.org.nz/"},

    # Singapore
    {"country": "Singapore", "cities": ["Singapore"],
     "name": "The Food Bank Singapore", "type": "Food bank",
     "url": "https://foodbank.sg/"},

    # South Africa
    {"country": "South Africa", "cities": ["Johannesburg", "Cape Town", "Durban",
                                            "Pretoria", "Port Elizabeth"],
     "name": "FoodForward South Africa", "type": "Food banking / redistribution",
     "url": "https://foodforwardsa.org/"},

    # Kenya
    {"country": "Kenya", "cities": ["Nairobi", "Mombasa", "Kisumu"],
     "name": "Food Banking Kenya", "type": "Food banking",
     "url": "https://foodbankingkenya.org/"},

    # Nigeria
    {"country": "Nigeria", "cities": ["Lagos", "Abuja"],
     "name": "Lagos Food Bank Initiative", "type": "Food bank / hunger relief",
     "url": "https://lagosfoodbank.org/"},

    # Ghana
    {"country": "Ghana", "cities": ["Accra", "Kumasi"],
     "name": "Food For All Africa", "type": "Food banking / hunger relief",
     "url": "https://foodforallafrica.com/"},

    # Indonesia
    {"country": "Indonesia", "cities": ["Bali", "Denpasar", "Jakarta", "Surabaya",
                                         "Medan"],
     "name": "Scholars of Sustenance Indonesia", "type": "Food rescue",
     "url": "https://scholarsofsustenance.org/"},
    {"country": "Indonesia", "cities": ["Jakarta", "Bandung", "Surabaya", "Medan"],
     "name": "FoodCycle Indonesia", "type": "Food redistribution",
     "url": "https://foodcycle.id/"},

    # Malaysia
    {"country": "Malaysia", "cities": ["Kuala Lumpur", "Petaling Jaya", "George Town"],
     "name": "The Lost Food Project", "type": "Food rescue",
     "url": "https://www.thelostfoodproject.org/"},

    # Brazil
    {"country": "Brazil", "cities": ["São Paulo", "Rio de Janeiro", "Brasília",
                                     "Salvador", "Belo Horizonte"],
     "name": "Mesa Brasil SESC", "type": "Food bank / redistribution",
     "url": "https://mesabrasil.sescsp.org.br/"},

    # Mexico
    {"country": "Mexico", "cities": ["Mexico City", "Guadalajara", "Monterrey",
                                     "Puebla", "Tijuana"],
     "name": "Bancos de Alimentos de México", "type": "Food bank network",
     "url": "https://bamx.org.mx/"},

    # Argentina
    {"country": "Argentina", "cities": ["Buenos Aires", "Córdoba", "Rosario"],
     "name": "Red Argentina de Bancos de Alimentos", "type": "Food bank network",
     "url": "https://redbda.org.ar/"},

    # Chile
    {"country": "Chile", "cities": ["Santiago", "Valparaíso", "Concepción"],
     "name": "Red de Alimentos", "type": "Food rescue / food bank",
     "url": "https://www.redalimentos.cl/"},

    # Colombia
    {"country": "Colombia", "cities": ["Bogotá", "Medellín", "Cali", "Barranquilla"],
     "name": "Asociación de Bancos de Alimentos de Colombia", "type": "Food bank network",
     "url": "https://abaco.org.co/"},

    # Peru
    {"country": "Peru", "cities": ["Lima", "Arequipa", "Cusco"],
     "name": "Banco de Alimentos Perú", "type": "Food bank",
     "url": "https://bancodealimentosperu.org/"},

    # Costa Rica
    {"country": "Costa Rica", "cities": ["San José", "Heredia", "Alajuela"],
     "name": "Banco de Alimentos de Costa Rica", "type": "Food bank",
     "url": "https://www.bancodealimentos.or.cr/"},

    # Ecuador
    {"country": "Ecuador", "cities": ["Quito", "Guayaquil", "Cuenca"],
     "name": "Banco de Alimentos Diakonía", "type": "Food bank",
     "url": "https://www.diakonia.org.ec/"},

    # Uruguay
    {"country": "Uruguay", "cities": ["Montevideo", "Salto"],
     "name": "Banco de Alimentos Uruguay", "type": "Food bank",
     "url": "https://bancodealimentos.org.uy/"},

    # Japan
    {"country": "Japan", "cities": ["Tokyo", "Osaka", "Kyoto", "Yokohama"],
     "name": "Japan Food Bank Network", "type": "Food banking network",
     "url": "https://www.foodbanking.or.jp/"},

    # South Korea
    {"country": "South Korea", "cities": ["Seoul", "Busan", "Incheon", "Daegu"],
     "name": "Korea Foodbank", "type": "Food bank network",
     "url": "https://www.foodbank1377.org/"},

    # Thailand
    {"country": "Thailand", "cities": ["Bangkok", "Chiang Mai", "Phuket"],
     "name": "Scholars of Sustenance Thailand", "type": "Food rescue",
     "url": "https://scholarsofsustenance.org/"},

    # Vietnam
    {"country": "Vietnam", "cities": ["Ho Chi Minh City", "Hanoi", "Da Nang"],
     "name": "Foodbank Vietnam", "type": "Food bank",
     "url": "https://foodbankvietnam.com/"},

    # Philippines
    {"country": "Philippines", "cities": ["Manila", "Quezon City", "Cebu City"],
     "name": "Rise Against Hunger Philippines", "type": "Hunger relief",
     "url": "https://riseagainsthunger.org/philippines/"},

    # Taiwan
    {"country": "Taiwan", "cities": ["Taipei", "Kaohsiung", "Taichung"],
     "name": "Taiwan People's Food Bank Association", "type": "Food bank network",
     "url": "https://www.foodbank.org.tw/"},

    # Israel
    {"country": "Israel", "cities": ["Jerusalem", "Tel Aviv", "Haifa"],
     "name": "Leket Israel", "type": "Food rescue / food security",
     "url": "https://www.leket.org/en/"},

    # Jordan
    {"country": "Jordan", "cities": ["Amman", "Zarqa", "Irbid"],
     "name": "Tkiyet Um Ali", "type": "Food aid / hunger relief",
     "url": "https://www.tua.jo/"},

    # Turkey
    {"country": "Turkey", "cities": ["Istanbul", "Ankara", "Izmir"],
     "name": "TIDER", "type": "Food banking / social support",
     "url": "https://tider.org/"},

    # Ireland
    {"country": "Ireland", "cities": ["Dublin", "Cork", "Galway", "Limerick"],
     "name": "FoodCloud", "type": "Food redistribution platform",
     "url": "https://food.cloud/"},

    # Netherlands
    {"country": "Netherlands", "cities": ["Amsterdam", "Rotterdam", "The Hague",
                                           "Utrecht", "Eindhoven"],
     "name": "Voedselbanken Nederland", "type": "Food bank network",
     "url": "https://voedselbankennederland.nl/"},

    # Spain
    {"country": "Spain", "cities": ["Madrid", "Barcelona", "Valencia", "Seville"],
     "name": "Federación Española de Bancos de Alimentos", "type": "Food bank network",
     "url": "https://www.fesbal.org/"},

    # Italy
    {"country": "Italy", "cities": ["Rome", "Milan", "Naples", "Turin"],
     "name": "Banco Alimentare", "type": "Food bank network",
     "url": "https://www.bancoalimentare.it/"},

    # Germany
    {"country": "Germany", "cities": ["Berlin", "Hamburg", "Munich", "Frankfurt",
                                       "Cologne"],
     "name": "Tafel Deutschland", "type": "Food bank network",
     "url": "https://www.tafel.de/"},

    # France
    {"country": "France", "cities": ["Paris", "Lyon", "Marseille", "Toulouse"],
     "name": "Banques Alimentaires", "type": "Food bank network",
     "url": "https://www.banquealimentaire.org/"},

    # Poland
    {"country": "Poland", "cities": ["Warsaw", "Kraków", "Wrocław", "Gdańsk"],
     "name": "Federacja Polskich Banków Żywności", "type": "Food bank network",
     "url": "https://bankizywnosci.pl/"},

    # Bulgaria
    {"country": "Bulgaria", "cities": ["Sofia", "Plovdiv", "Varna"],
     "name": "Bulgarian Food Bank", "type": "Food bank",
     "url": "https://foodbank.bg/"},

    # Ethiopia
    {"country": "Ethiopia", "cities": ["Addis Ababa"],
     "name": "It Rains Food Bank of Ethiopia", "type": "Food bank",
     "url": "https://itrainsfoodbank.org/"},

    # Mauritius
    {"country": "Mauritius", "cities": ["Port Louis", "Quatre Bornes"],
     "name": "FoodWise", "type": "Food rescue",
     "url": "https://www.foodwise.mu/"},

    # New countries can be added here without changing the app logic.
]

# ----------------------------
# NORMALIZATION / ALIASES
# ----------------------------
CITY_ALIASES = {
    "new delhi": "Delhi",
    "delhi": "Delhi",
    "ncr": "Delhi",
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "bombay": "Mumbai",
    "mumbai": "Mumbai",
    "calcutta": "Kolkata",
    "kolkata": "Kolkata",
    "madras": "Chennai",
    "chennai": "Chennai",
    "nyc": "New York",
    "new york city": "New York",
    "sf": "San Francisco",
    "san fran": "San Francisco",
    "la": "Los Angeles",
    "washington dc": "Washington",
    "dc": "Washington",
    "são paulo": "São Paulo",
    "sao paulo": "São Paulo",
    "mexico city": "Mexico City",
    "ho chi minh": "Ho Chi Minh City",
}

COUNTRY_ALIASES = {
    "usa": "United States",
    "us": "United States",
    "u.s.": "United States",
    "america": "United States",
    "uk": "United Kingdom",
    "england": "United Kingdom",
    "britain": "United Kingdom",
    "uae": "United Arab Emirates",
    "emirates": "United Arab Emirates",
    "korea": "South Korea",
}

def clean(text):
    return re.sub(r"\s+", " ", text.lower().strip())

def canonical_city(text):
    t = clean(text)
    return CITY_ALIASES.get(t, text.strip().title())

def detect_city(text):
    t = clean(text)

    # Longest city names first so "New York City" wins over "York".
    all_cities = set()
    for org in ORGS:
        all_cities.update(org["cities"])
    all_cities.update(CITY_ALIASES.keys())

    for city in sorted(all_cities, key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(city.lower()) + r"(?!\w)"
        if re.search(pattern, t):
            return canonical_city(city)

    # Common natural-language location phrases.
    patterns = [
        r"\bin\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ .'-]{1,40})",
        r"\bfrom\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ .'-]{1,40})",
        r"\baround\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ .'-]{1,40})",
        r"\bnear\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ .'-]{1,40})",
        r"\blive in\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ .'-]{1,40})",
        r"\bi'm in\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ .'-]{1,40})",
        r"\bi am in\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ .'-]{1,40})",
    ]

    stop_words = {
        "a", "an", "the", "and", "with", "where", "what", "how",
        "can", "could", "should", "do", "does", "is", "are", "please"
    }

    for pattern in patterns:
        m = re.search(pattern, t)
        if m:
            candidate = m.group(1).strip(" .,!?:;")
            # Don't accidentally turn "in my city" into a location.
            if candidate and candidate.split()[0] not in stop_words:
                candidate = candidate.split(" and ")[0].strip()
                candidate = candidate.split(" where ")[0].strip()
                return canonical_city(candidate)

    return None

def detect_intent(text):
    t = clean(text)

    location_words = [
        "where", "find", "near", "ngo", "charity", "food bank", "foodbank",
        "organization", "organisation", "centre", "center", "donate",
        "donation", "give", "collect", "pickup", "pick up", "redistribute",
        "redistribution", "food rescue", "food rescue", "who can take"
    ]

    surplus_words = [
        "leftover", "left overs", "surplus", "extra food", "excess food",
        "too much food", "food left", "meals left", "meal left",
        "cooked too much", "unused food", "spare food", "wasted food"
    ]

    if any(x in t for x in surplus_words) and any(x in t for x in location_words):
        return "surplus_location"

    if any(x in t for x in location_words):
        return "find"

    if any(x in t for x in surplus_words):
        return "surplus"

    if any(x in t for x in ["hello", "hi", "hey", "start", "what is plateful"]):
        return "greeting"

    return "general"

def find_orgs(city):
    if not city:
        return []

    city_clean = clean(city)
    matches = []

    for org in ORGS:
        city_matches = [clean(c) for c in org["cities"]]
        if city_clean in city_matches:
            matches.append(org)

    # Also match a city entered as an exact alias.
    canonical = canonical_city(city)
    for org in ORGS:
        if any(clean(c) == clean(canonical) for c in org["cities"]):
            if org not in matches:
                matches.append(org)

    return matches

def find_country_hint(text):
    t = clean(text)
    for alias, country in COUNTRY_ALIASES.items():
        if re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", t):
            return country
    for org in ORGS:
        if re.search(r"(?<!\w)" + re.escape(org["country"].lower()) + r"(?!\w)", t):
            return org["country"]
    return None

# ----------------------------
# RESPONSE ENGINE
# ----------------------------
def answer_user(message):
    intent = detect_intent(message)
    city = detect_city(message)

    if intent == "greeting":
        return (
            "Hey! I'm Plateful 👋\n\n"
            "I help turn surplus food into useful food redistribution. "
            "Tell me what food you have and, if you want local options, "
            "include your city.\n\n"
            "For example: **“We have 20 leftover meals in Toronto. Who can take them?”**"
        ), None, None

    if intent == "surplus":
        return (
            "Absolutely — Plateful can help with surplus food.\n\n"
            "First, tell me **which city you're in**. I can then look for "
            "food banks, food-rescue groups or redistribution organizations "
            "in that area.\n\n"
            "Example: **“I have 15 leftover meals in London.”**"
        ), None, None

    if intent in ("find", "surplus_location"):
        if not city:
            country = find_country_hint(message)
            if country:
                return (
                    f"I know you're looking in **{country}**, but I need the "
                    "city to give you more useful local options.\n\n"
                    "For example: **“food donation in Toronto”**."
                ), None, None

            return (
                "I can help find a local food-rescue or food-bank option. "
                "What **city** are you in?"
            ), None, None

        orgs = find_orgs(city)

        if orgs:
            intro = (
                f"I found **{len(orgs)} starting point"
                f"{'s' if len(orgs) != 1 else ''} for {city}.**"
            )
            return intro, city, orgs

        # Global fallback: don't pretend the directory is complete.
        return (
            f"I don't currently have a verified organization in my prototype "
            f"directory for **{city}**.\n\n"
            "That doesn't mean there isn't one. For a real deployment, "
            "Plateful should connect to a live food-rescue/food-bank directory "
            "to discover local organizations dynamically.\n\n"
            "For now, try searching locally for **food banks, food rescue "
            "organizations, community food programs, or surplus-food charities**, "
            "and contact them first to confirm they accept your food."
        ), city, []

    return (
        "I can help with food donation and redistribution.\n\n"
        "Try something like:\n"
        "- “Where can I donate food in Delhi?”\n"
        "- “I have 20 leftover meals in Toronto.”\n"
        "- “Our restaurant has surplus food in London.”\n"
        "- “Who can collect extra food in Sydney?”"
    ), None, None

# ----------------------------
# SESSION STATE
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_results" not in st.session_state:
    st.session_state.last_results = []

if "last_city" not in st.session_state:
    st.session_state.last_city = None

# ----------------------------
# STYLING
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@500;600&display=swap');

.stApp {
    background: #F4F1E9;
    color: #20201D;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #20201D !important;
}

p, div, span, label, button, input, textarea {
    font-family: 'DM Sans', Arial, sans-serif;
}

.plateful-brand {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.2rem;
    font-weight: 600;
    letter-spacing: -1px;
}

.badge {
    display: inline-block;
    margin-left: 12px;
    padding: 6px 11px;
    border: 1px solid #B68A3A;
    border-radius: 999px;
    color: #765A28;
    font-size: .75rem;
    letter-spacing: .04em;
    vertical-align: middle;
}

.hero {
    margin-top: 55px;
    padding: 50px 0 38px;
    border-bottom: 1px solid #D9D3C6;
}

.hero h1 {
    font-size: clamp(3rem, 7vw, 6.3rem) !important;
    line-height: .96;
    max-width: 950px;
    margin-bottom: 22px;
}

.hero p {
    max-width: 680px;
    font-size: 1.08rem;
    line-height: 1.7;
    color: #625F57;
}

.section-label {
    color: #A1782E;
    font-size: .75rem;
    letter-spacing: .16em;
    text-transform: uppercase;
    font-weight: 600;
}

.step {
    padding: 22px 4px 30px;
    border-bottom: 1px solid #D9D3C6;
}

.step-number {
    color: #B68A3A;
    font-size: .8rem;
    font-weight: 600;
}

.step-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.45rem;
    margin-top: 7px;
}

.step-copy {
    color: #6B675E;
    line-height: 1.6;
    margin-top: 5px;
}

.org-card {
    background: #FAF8F2;
    border: 1px solid #D9D3C6;
    border-radius: 18px;
    padding: 23px;
    margin: 12px 0;
}

.org-name {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.4rem;
}

.org-type {
    color: #776C59;
    font-size: .9rem;
    margin-top: 5px;
}

.notice {
    background: #ECE7DA;
    border-left: 3px solid #B68A3A;
    padding: 15px 18px;
    margin-top: 18px;
    color: #5E594F;
    line-height: 1.55;
    border-radius: 0 10px 10px 0;
}

.footer {
    margin-top: 80px;
    padding-top: 25px;
    border-top: 1px solid #D9D3C6;
    color: #777166;
    font-size: .85rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown(
    '<span class="plateful-brand">plateful.</span>'
    '<span class="badge">GLOBAL PROTOTYPE</span>',
    unsafe_allow_html=True
)

# ----------------------------
# HERO
# ----------------------------
st.markdown("""
<div class="hero">
    <div class="section-label">Food redistribution · worldwide</div>
    <h1>Food should find a table, not a bin.</h1>
    <p>
        Plateful helps people, restaurants and event organizers figure out
        what to do with safe surplus food — and find organizations that may
        be able to redistribute it.
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# HOW IT WORKS
# ----------------------------
cols = st.columns(3)
steps = [
    ("01", "Tell us", "Describe your surplus food and where you are."),
    ("02", "We understand", "Plateful detects the situation, quantity and location from natural language."),
    ("03", "Find a path", "We surface food-rescue and food-bank starting points in the area."),
]

for col, (num, title, copy) in zip(cols, steps):
    with col:
        st.markdown(
            f'<div class="step">'
            f'<div class="step-number">{num}</div>'
            f'<div class="step-title">{title}</div>'
            f'<div class="step-copy">{copy}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

st.write("")

# ----------------------------
# CHAT
# ----------------------------
st.markdown('<div class="section-label">Talk to Plateful</div>', unsafe_allow_html=True)
st.markdown("### Tell me what is happening")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "e.g. We have 20 leftover meals in Toronto. Who can take them?"
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    reply, city, orgs = answer_user(prompt)

    st.session_state.last_city = city
    st.session_state.last_results = orgs or []

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()

# ----------------------------
# ORGANIZATION RESULTS
# ----------------------------
if st.session_state.last_results:
    st.markdown("---")
    st.markdown(
        f'<div class="section-label">Starting points in {st.session_state.last_city}</div>',
        unsafe_allow_html=True
    )

    for org in st.session_state.last_results:
        st.markdown(
            f'<div class="org-card">'
            f'<div class="org-name">{org["name"]}</div>'
            f'<div class="org-type">{org["type"]} · {org["country"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.link_button(f"Visit {org['name']}", org["url"])

    st.markdown(
        '<div class="notice">'
        '<strong>Important:</strong> Plateful is a prototype directory. '
        'An organization may have specific rules about food type, preparation, '
        'packaging, quantity, timing and pickup. Always contact the organization '
        'before arranging a donation and confirm that your specific food is accepted.'
        '</div>',
        unsafe_allow_html=True
    )

# ----------------------------
# FOOTER
# ----------------------------
st.markdown(
    '<div class="footer">'
    'Plateful is a prototype concept for reducing food waste and improving food redistribution. '
    'The directory is curated starting data and is not a live availability or pickup service.'
    '</div>',
    unsafe_allow_html=True
)
