
import re
from urllib.parse import quote
import streamlit as st

# ============================================================
# PLATEFUL
# Food redistribution assistant
# ============================================================

st.set_page_config(
    page_title="Plateful — Food Redistribution",
    page_icon="🍽️",
    layout="wide",
)

# ------------------------------------------------------------
# DIRECTORY
# ------------------------------------------------------------
# Starting directory for the application. This is not a live
# availability database. Always ask the organisation to confirm
# that they accept the specific food, quantity, condition, timing,
# and collection/delivery arrangement.

ORGS = [
    # INDIA
    {"country": "India", "cities": ["Delhi", "New Delhi"], "name": "No Food Waste",
     "type": "Food rescue / redistribution", "url": "https://nofoodwaste.org/"},
    {"country": "India", "cities": ["Delhi", "New Delhi", "Mumbai", "Bengaluru", "Bangalore",
                                     "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur"],
     "name": "Feeding India", "type": "Food security / hunger relief",
     "url": "https://www.feedingindia.org/"},
    {"country": "India", "cities": ["Delhi", "New Delhi", "Mumbai", "Bengaluru", "Bangalore",
                                     "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur"],
     "name": "Robin Hood Army", "type": "Food redistribution / community support",
     "url": "https://robinhoodarmy.com/"},

    # UNITED STATES
    {"country": "United States", "cities": ["New York", "New York City", "NYC"],
     "name": "City Harvest", "type": "Food rescue", "url": "https://www.cityharvest.org/"},
    {"country": "United States", "cities": ["Birmingham", "New Haven", "Fairfield County",
                                             "New York", "Los Angeles", "Chicago", "Boston",
                                             "Seattle", "Washington", "San Francisco"],
     "name": "Food Rescue US", "type": "Food rescue network",
     "url": "https://foodrescue.us/"},

    # CANADA
    {"country": "Canada", "cities": ["Toronto", "Vancouver", "Montreal", "Calgary",
                                     "Ottawa", "Edmonton", "Winnipeg"],
     "name": "Second Harvest", "type": "Food rescue / redistribution",
     "url": "https://www.secondharvest.ca/"},

    # UNITED KINGDOM
    {"country": "United Kingdom", "cities": ["London", "Manchester", "Birmingham",
                                             "Liverpool", "Bristol", "Leeds", "Glasgow",
                                             "Edinburgh", "Cardiff"],
     "name": "FareShare", "type": "Food redistribution network",
     "url": "https://fareshare.org.uk/"},

    # AUSTRALIA
    {"country": "Australia", "cities": ["Sydney", "Melbourne", "Brisbane", "Perth",
                                         "Adelaide", "Canberra", "Gold Coast", "Cairns",
                                         "Newcastle"],
     "name": "OzHarvest", "type": "Food rescue", "url": "https://www.ozharvest.org/"},

    # NEW ZEALAND
    {"country": "New Zealand", "cities": ["Auckland", "Wellington", "Christchurch",
                                           "Hamilton", "Dunedin"],
     "name": "Kaibosh", "type": "Food rescue", "url": "https://kaibosh.org.nz/"},

    # SINGAPORE
    {"country": "Singapore", "cities": ["Singapore"],
     "name": "The Food Bank Singapore", "type": "Food bank",
     "url": "https://foodbank.sg/"},

    # SOUTH AFRICA
    {"country": "South Africa", "cities": ["Johannesburg", "Cape Town", "Durban",
                                            "Pretoria", "Port Elizabeth"],
     "name": "FoodForward South Africa", "type": "Food banking / redistribution",
     "url": "https://foodforwardsa.org/"},

    # KENYA
    {"country": "Kenya", "cities": ["Nairobi", "Mombasa", "Kisumu"],
     "name": "Food Banking Kenya", "type": "Food banking",
     "url": "https://foodbankingkenya.org/"},

    # NIGERIA
    {"country": "Nigeria", "cities": ["Lagos", "Abuja"],
     "name": "Lagos Food Bank Initiative", "type": "Food bank / hunger relief",
     "url": "https://lagosfoodbank.org/"},

    # GHANA
    {"country": "Ghana", "cities": ["Accra", "Kumasi"],
     "name": "Food For All Africa", "type": "Food banking / hunger relief",
     "url": "https://foodforallafrica.com/"},

    # INDONESIA
    {"country": "Indonesia", "cities": ["Bali", "Denpasar", "Jakarta", "Surabaya", "Medan"],
     "name": "Scholars of Sustenance Indonesia", "type": "Food rescue",
     "url": "https://scholarsofsustenance.org/"},
    {"country": "Indonesia", "cities": ["Jakarta", "Bandung", "Surabaya", "Medan"],
     "name": "FoodCycle Indonesia", "type": "Food redistribution",
     "url": "https://foodcycle.id/"},

    # MALAYSIA
    {"country": "Malaysia", "cities": ["Kuala Lumpur", "Petaling Jaya", "George Town"],
     "name": "The Lost Food Project", "type": "Food rescue",
     "url": "https://www.thelostfoodproject.org/"},

    # BRAZIL
    {"country": "Brazil", "cities": ["São Paulo", "Rio de Janeiro", "Brasília",
                                     "Salvador", "Belo Horizonte"],
     "name": "Mesa Brasil SESC", "type": "Food bank / redistribution",
     "url": "https://mesabrasil.sescsp.org.br/"},

    # MEXICO
    {"country": "Mexico", "cities": ["Mexico City", "Guadalajara", "Monterrey",
                                     "Puebla", "Tijuana"],
     "name": "Bancos de Alimentos de México", "type": "Food bank network",
     "url": "https://bamx.org.mx/"},

    # ARGENTINA
    {"country": "Argentina", "cities": ["Buenos Aires", "Córdoba", "Rosario"],
     "name": "Red Argentina de Bancos de Alimentos", "type": "Food bank network",
     "url": "https://redbda.org.ar/"},

    # CHILE
    {"country": "Chile", "cities": ["Santiago", "Valparaíso", "Concepción"],
     "name": "Red de Alimentos", "type": "Food rescue / food bank",
     "url": "https://www.redalimentos.cl/"},

    # COLOMBIA
    {"country": "Colombia", "cities": ["Bogotá", "Medellín", "Cali", "Barranquilla"],
     "name": "Asociación de Bancos de Alimentos de Colombia", "type": "Food bank network",
     "url": "https://abaco.org.co/"},

    # PERU
    {"country": "Peru", "cities": ["Lima", "Arequipa", "Cusco"],
     "name": "Banco de Alimentos Perú", "type": "Food bank",
     "url": "https://bancodealimentosperu.org/"},

    # COSTA RICA
    {"country": "Costa Rica", "cities": ["San José", "Heredia", "Alajuela"],
     "name": "Banco de Alimentos de Costa Rica", "type": "Food bank",
     "url": "https://www.bancodealimentos.or.cr/"},

    # ECUADOR
    {"country": "Ecuador", "cities": ["Quito", "Guayaquil", "Cuenca"],
     "name": "Banco de Alimentos Diakonía", "type": "Food bank",
     "url": "https://www.diakonia.org.ec/"},

    # URUGUAY
    {"country": "Uruguay", "cities": ["Montevideo", "Salto"],
     "name": "Banco de Alimentos Uruguay", "type": "Food bank",
     "url": "https://bancodealimentos.org.uy/"},

    # JAPAN
    {"country": "Japan", "cities": ["Tokyo", "Osaka", "Kyoto", "Yokohama"],
     "name": "Japan Food Bank Network", "type": "Food banking network",
     "url": "https://www.foodbanking.or.jp/"},

    # SOUTH KOREA
    {"country": "South Korea", "cities": ["Seoul", "Busan", "Incheon", "Daegu"],
     "name": "Korea Foodbank", "type": "Food bank network",
     "url": "https://www.foodbank1377.org/"},

    # THAILAND
    {"country": "Thailand", "cities": ["Bangkok", "Chiang Mai", "Phuket"],
     "name": "Scholars of Sustenance Thailand", "type": "Food rescue",
     "url": "https://scholarsofsustenance.org/"},

    # VIETNAM
    {"country": "Vietnam", "cities": ["Ho Chi Minh City", "Hanoi", "Da Nang"],
     "name": "Foodbank Vietnam", "type": "Food bank",
     "url": "https://foodbankvietnam.com/"},

    # PHILIPPINES
    {"country": "Philippines", "cities": ["Manila", "Quezon City", "Cebu City"],
     "name": "Rise Against Hunger Philippines", "type": "Hunger relief",
     "url": "https://riseagainsthunger.org/philippines/"},

    # TAIWAN
    {"country": "Taiwan", "cities": ["Taipei", "Kaohsiung", "Taichung"],
     "name": "Taiwan People's Food Bank Association", "type": "Food bank network",
     "url": "https://www.foodbank.org.tw/"},

    # ISRAEL
    {"country": "Israel", "cities": ["Jerusalem", "Tel Aviv", "Haifa"],
     "name": "Leket Israel", "type": "Food rescue / food security",
     "url": "https://www.leket.org/en/"},

    # JORDAN
    {"country": "Jordan", "cities": ["Amman", "Zarqa", "Irbid"],
     "name": "Tkiyet Um Ali", "type": "Food aid / hunger relief",
     "url": "https://www.tua.jo/"},

    # TURKEY
    {"country": "Turkey", "cities": ["Istanbul", "Ankara", "Izmir"],
     "name": "TIDER", "type": "Food banking / social support",
     "url": "https://tider.org/"},

    # IRELAND
    {"country": "Ireland", "cities": ["Dublin", "Cork", "Galway", "Limerick"],
     "name": "FoodCloud", "type": "Food redistribution platform",
     "url": "https://food.cloud/"},

    # NETHERLANDS
    {"country": "Netherlands", "cities": ["Amsterdam", "Rotterdam", "The Hague",
                                           "Utrecht", "Eindhoven"],
     "name": "Voedselbanken Nederland", "type": "Food bank network",
     "url": "https://voedselbankennederland.nl/"},

    # SPAIN
    {"country": "Spain", "cities": ["Madrid", "Barcelona", "Valencia", "Seville"],
     "name": "Federación Española de Bancos de Alimentos", "type": "Food bank network",
     "url": "https://www.fesbal.org/"},

    # ITALY
    {"country": "Italy", "cities": ["Rome", "Milan", "Naples", "Turin"],
     "name": "Banco Alimentare", "type": "Food bank network",
     "url": "https://www.bancoalimentare.it/"},

    # GERMANY
    {"country": "Germany", "cities": ["Berlin", "Hamburg", "Munich", "Frankfurt", "Cologne"],
     "name": "Tafel Deutschland", "type": "Food bank network",
     "url": "https://www.tafel.de/"},

    # FRANCE
    {"country": "France", "cities": ["Paris", "Lyon", "Marseille", "Toulouse"],
     "name": "Banques Alimentaires", "type": "Food bank network",
     "url": "https://www.banquealimentaire.org/"},

    # POLAND
    {"country": "Poland", "cities": ["Warsaw", "Kraków", "Wrocław", "Gdańsk"],
     "name": "Federacja Polskich Banków Żywności", "type": "Food bank network",
     "url": "https://bankizywnosci.pl/"},

    # BULGARIA
    {"country": "Bulgaria", "cities": ["Sofia", "Plovdiv", "Varna"],
     "name": "Bulgarian Food Bank", "type": "Food bank",
     "url": "https://foodbank.bg/"},

    # ETHIOPIA
    {"country": "Ethiopia", "cities": ["Addis Ababa"],
     "name": "It Rains Food Bank of Ethiopia", "type": "Food bank",
     "url": "https://itrainsfoodbank.org/"},

    # MAURITIUS
    {"country": "Mauritius", "cities": ["Port Louis", "Quatre Bornes"],
     "name": "FoodWise", "type": "Food rescue",
     "url": "https://www.foodwise.mu/"},
]

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
    "sao paulo": "São Paulo",
    "mexico city": "Mexico City",
    "ho chi minh": "Ho Chi Minh City",
}

def clean(text):
    return re.sub(r"\s+", " ", str(text).lower().strip())

def canonical_city(text):
    value = clean(text)
    return CITY_ALIASES.get(value, str(text).strip().title())

def detect_city(text):
    t = clean(text)

    all_cities = set()
    for org in ORGS:
        all_cities.update(org["cities"])
    all_cities.update(CITY_ALIASES.keys())

    for city in sorted(all_cities, key=len, reverse=True):
        if re.search(r"(?<!\w)" + re.escape(city.lower()) + r"(?!\w)", t):
            return canonical_city(city)

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
        match = re.search(pattern, t)
        if match:
            candidate = match.group(1).strip(" .,!?:;")
            candidate = candidate.split(" and ")[0].strip()
            candidate = candidate.split(" where ")[0].strip()
            if candidate and candidate.split()[0] not in stop_words:
                return canonical_city(candidate)

    return None

def detect_intent(text):
    t = clean(text)

    location_words = [
        "where", "find", "near", "ngo", "charity", "food bank", "foodbank",
        "organization", "organisation", "centre", "center", "donate",
        "donation", "give", "collect", "pickup", "pick up", "redistribute",
        "redistribution", "food rescue", "who can take"
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

    canonical = canonical_city(city)
    results = []

    for org in ORGS:
        if any(clean(c) == clean(canonical) for c in org["cities"]):
            results.append(org)

    return results

# ------------------------------------------------------------
# DONATION REQUEST
# ------------------------------------------------------------

def create_email_link(org, name, email, food, quantity, city, notes):
    subject = f"Food donation request — {city}"
    body = f"""Hello {org['name']},

I would like to enquire about donating surplus food in {city}.

Donor name: {name}
Donor email: {email}
Food: {food}
Quantity: {quantity}
Location: {city}
Additional details: {notes}

Could you please let me know whether you can accept this donation and whether collection or drop-off is possible?

Thank you,
{name}
"""

    return (
        f"mailto:?subject={quote(subject)}&body={quote(body)}"
    )

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

defaults = {
    "messages": [],
    "last_results": [],
    "last_city": None,
    "request_recorded": False,
    "selected_org": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ------------------------------------------------------------
# STYLING
# ------------------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@500;600&display=swap');

:root {
    --bg: #DCE8E3;
    --surface: #F0E8E2;
    --surface-2: #E8DDD8;
    --ink: #29453F;
    --muted: #5F716C;
    --teal: #4E756B;
    --teal-dark: #385B53;
    --terracotta: #B96F57;
    --terracotta-dark: #965642;
    --lavender: #D9D5E7;
    --line: #B8C9C3;
}

.stApp {
    background: var(--bg);
    color: var(--ink);
}

.block-container {
    max-width: 1240px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: var(--ink) !important;
}

p, div, span, label, button, input, textarea {
    font-family: 'DM Sans', Arial, sans-serif;
}

.plateful-brand {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.25rem;
    font-weight: 600;
    letter-spacing: -1px;
    color: var(--ink);
}

.app-tag {
    display: inline-block;
    margin-left: 12px;
    padding: 6px 12px;
    border-radius: 999px;
    background: var(--lavender);
    color: var(--ink);
    font-size: .75rem;
    font-weight: 600;
    letter-spacing: .04em;
}

.hero {
    margin-top: 38px;
    padding: 42px 46px 44px;
    border-radius: 28px;
    background: #C8DCD5;
    border: 1px solid var(--line);
}

.hero h1 {
    font-size: clamp(3rem, 7vw, 6rem) !important;
    line-height: .96;
    max-width: 900px;
    margin: 12px 0 22px;
}

.hero p {
    max-width: 690px;
    font-size: 1.08rem;
    line-height: 1.7;
    color: var(--muted);
}

.section-label {
    color: var(--terracotta-dark);
    font-size: .75rem;
    letter-spacing: .16em;
    text-transform: uppercase;
    font-weight: 700;
}

.step {
    margin-top: 20px;
    padding: 22px 20px 26px;
    border-radius: 18px;
    background: var(--surface);
    border: 1px solid var(--line);
    min-height: 145px;
}

.step-number {
    color: var(--terracotta);
    font-size: .8rem;
    font-weight: 700;
}

.step-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.4rem;
    margin-top: 7px;
}

.step-copy {
    color: var(--muted);
    line-height: 1.55;
    margin-top: 6px;
}

.chat-shell {
    background: #E9E1E0;
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 18px;
    margin-top: 10px;
}

.org-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 22px;
    margin: 13px 0;
}

.org-name {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.4rem;
    color: var(--ink);
}

.org-type {
    color: var(--muted);
    font-size: .9rem;
    margin-top: 5px;
}

.notice {
    background: #E8D8C9;
    border-left: 4px solid var(--terracotta);
    padding: 15px 18px;
    margin: 18px 0;
    color: #624E46;
    line-height: 1.55;
    border-radius: 0 12px 12px 0;
}

.request-box {
    background: #D2DED9;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 23px;
    margin-top: 20px;
}

.request-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.5rem;
    color: var(--ink);
}

.small-copy {
    color: var(--muted);
    line-height: 1.55;
}

.footer {
    margin-top: 70px;
    padding-top: 24px;
    border-top: 1px solid var(--line);
    color: var(--muted);
    font-size: .84rem;
}

/* Streamlit controls */
.stButton > button,
.stLinkButton > a {
    border-radius: 999px !important;
    border: 1px solid var(--teal) !important;
    background: var(--teal) !important;
    color: #EEF4F1 !important;
    font-weight: 600 !important;
}

.stButton > button:hover,
.stLinkButton > a:hover {
    background: var(--teal-dark) !important;
    border-color: var(--teal-dark) !important;
}

[data-testid="stChatMessage"] {
    background: rgba(240, 232, 226, .78);
    border: 1px solid rgba(184, 201, 195, .8);
    border-radius: 18px;
    margin-bottom: 9px;
}

[data-testid="stChatInput"] {
    border-color: var(--teal) !important;
}

input, textarea {
    background: #EFE5E1 !important;
    color: var(--ink) !important;
    border-color: var(--line) !important;
}

div[data-baseweb="input"] {
    background: #EFE5E1 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.markdown(
    '<span class="plateful-brand">plateful.</span>'
    '<span class="app-tag">FOOD · PEOPLE · IMPACT</span>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="section-label">Food redistribution</div>
    <h1>Good food deserves a second destination.</h1>
    <p>
        Plateful helps people, restaurants and event organisers turn surplus
        food into meaningful redistribution by understanding the situation
        and finding relevant organisations.
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# HOW IT WORKS
# ------------------------------------------------------------

cols = st.columns(3)

steps = [
    ("01", "Tell us", "Describe your food, quantity and location naturally."),
    ("02", "We understand", "Plateful identifies the situation and the local need."),
    ("03", "Take action", "Find an organisation, record your request and prepare a donation enquiry."),
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
st.markdown('<div class="section-label">Talk to Plateful</div>', unsafe_allow_html=True)
st.markdown("### What is happening?")

# ------------------------------------------------------------
# CHAT
# ------------------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "Try: We have 20 leftover meals in Toronto. Who can take them?"
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    intent = detect_intent(prompt)
    city = detect_city(prompt)

    if intent == "greeting":
        reply = (
            "Hi! I'm Plateful 🌱\n\n"
            "Tell me about your surplus food and where you are. "
            "I can help you find food-rescue or food-bank organisations "
            "and guide you through making a donation request."
        )
        orgs = []

    elif intent == "surplus":
        reply = (
            "Absolutely. I can help you work out what to do with the surplus food.\n\n"
            "Tell me **which city you're in**, and I'll look for relevant "
            "food-rescue or food-bank organisations there."
        )
        orgs = []

    elif intent in ("find", "surplus_location"):
        if not city:
            reply = (
                "I can help find a local organisation. "
                "What **city** are you in?"
            )
            orgs = []
        else:
            orgs = find_orgs(city)

            if orgs:
                reply = (
                    f"I found **{len(orgs)} organisation"
                    f"{'s' if len(orgs) != 1 else ''} to start with in **{city}**.\n\n"
                    "You can open an organisation's website, or record a donation "
                    "request below and prepare a message for them."
                )
            else:
                reply = (
                    f"I don't currently have a verified organisation in my "
                    f"prototype directory for **{city}**.\n\n"
                    "That does not mean there isn't one. A full deployment of "
                    "Plateful should connect to a live directory so it can "
                    "discover local organisations dynamically."
                )
    else:
        reply = (
            "I can help with food donation and redistribution.\n\n"
            "Try:\n"
            "- “Where can I donate food in Delhi?”\n"
            "- “I have 20 leftover meals in Toronto.”\n"
            "- “Our restaurant has surplus food in London.”\n"
            "- “Who can collect extra food in Sydney?”"
        )
        orgs = []

    st.session_state.last_city = city
    st.session_state.last_results = orgs
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ------------------------------------------------------------
# ORGANISATIONS
# ------------------------------------------------------------

if st.session_state.last_results:
    st.markdown("---")
    st.markdown(
        f'<div class="section-label">Organisations in {st.session_state.last_city}</div>',
        unsafe_allow_html=True
    )

    for index, org in enumerate(st.session_state.last_results):
        st.markdown(
            f'<div class="org-card">'
            f'<div class="org-name">{org["name"]}</div>'
            f'<div class="org-type">{org["type"]} · {org["country"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns([1, 1])

        with c1:
            st.link_button(
                f"Visit {org['name']}",
                org["url"],
                use_container_width=True
            )

        with c2:
            if st.button(
                "Record a donation request",
                key=f"record_{index}",
                use_container_width=True
            ):
                st.session_state.selected_org = index
                st.session_state.request_recorded = True
                st.rerun()

    st.markdown(
        '<div class="notice">'
        '<strong>Before arranging anything:</strong> contact the organisation '
        'to confirm that it accepts your specific food type, quantity, condition, '
        'packaging and timing. Plateful does not guarantee pickup or acceptance.'
        '</div>',
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# REQUEST FORM
# ------------------------------------------------------------

if st.session_state.request_recorded and st.session_state.last_results:
    org = st.session_state.last_results[st.session_state.selected_org]
    city = st.session_state.last_city

    st.markdown("---")

    st.markdown(
        '<div class="request-box">'
        '<div class="section-label">Donation request</div>'
        '<div class="request-title">Let’s turn this into an action.</div>'
        '<p class="small-copy">'
        f'You are preparing a request for <strong>{org["name"]}</strong> in '
        f'<strong>{city}</strong>.'
        '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("donation_request_form"):
        name = st.text_input("Your name", placeholder="e.g. Demo User")
        email = st.text_input("Your email", placeholder="e.g. demo@example.com")
        food = st.text_input(
            "What food do you have?",
            placeholder="e.g. freshly prepared vegetarian meals"
        )
        quantity = st.text_input(
            "Approximate quantity",
            placeholder="e.g. 20 meals"
        )
        notes = st.text_area(
            "Anything else the organisation should know?",
            placeholder="e.g. Prepared today, individually packed, available this evening."
        )

        submitted = st.form_submit_button(
            "Create donation request",
            use_container_width=True
        )

    if submitted:
        if not name or not email or not food or not quantity:
            st.warning("Please fill in your name, email, food and quantity.")
        else:
            st.session_state.donation_request = {
                "name": name,
                "email": email,
                "food": food,
                "quantity": quantity,
                "city": city,
                "notes": notes,
                "organisation": org["name"],
            }

            st.success(
                f"Donation request prepared for {org['name']}."
            )

            email_link = create_email_link(
                org, name, email, food, quantity, city, notes
            )

            st.markdown(
                '<div class="request-box">'
                '<div class="request-title">Next step</div>'
                '<p class="small-copy">'
                'The app cannot silently send an email on your behalf. '
                'Use the button below to open your email app with the request '
                'already written, then review and send it.'
                '</p>'
                '</div>',
                unsafe_allow_html=True
            )

            st.link_button(
                f"Prepare email for {org['name']}",
                email_link,
                use_container_width=True
            )

            st.info(
                "For a demo, use placeholder contact details rather than real personal information."
            )

# ------------------------------------------------------------
# FALLBACK / EMPTY DIRECTORY NOTE
# ------------------------------------------------------------

if (
    st.session_state.last_city
    and not st.session_state.last_results
    and detect_intent(
        st.session_state.messages[-1]["content"]
    ) in ("find", "surplus_location")
):
    st.markdown(
        '<div class="notice">'
        '<strong>How the full application can grow:</strong> '
        'the current directory is structured so a live organisation-discovery '
        'service can be connected later without redesigning the conversation flow.'
        '</div>',
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown(
    '<div class="footer">'
    'Plateful helps connect surplus food with possible redistribution pathways. '
    'Organisation listings are starting data, not live availability.'
    '</div>',
    unsafe_allow_html=True
)
