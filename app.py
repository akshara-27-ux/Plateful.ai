import re
from urllib.parse import quote
import streamlit as st

# ============================================================
# PLATEFUL — FOOD REDISTRIBUTION DIRECTORY & ASSISTANT
# ============================================================

st.set_page_config(
    page_title="Plateful — Food Redistribution",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# VERIFIED DIRECTORY
# ------------------------------------------------------------
ORGS = [
    # INDIA
    {
        "country": "India",
        "cities": ["Delhi", "New Delhi", "Chennai", "Bengaluru", "Coimbatore", "Hyderabad"],
        "name": "No Food Waste",
        "type": "Surplus Food Rescue & Delivery",
        "url": "https://nofoodwaste.org/",
        "contact_email": "info@nofoodwaste.org",
    },
    {
        "country": "India",
        "cities": ["Delhi", "New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Chandigarh", "Lucknow"],
        "name": "Feeding India (by Zomato)",
        "type": "Hunger Relief & Large Redistribution Network",
        "url": "https://www.feedingindia.org/",
        "contact_email": "contact@feedingindia.org",
    },
    {
        "country": "India",
        "cities": ["Delhi", "New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur"],
        "name": "Robin Hood Army",
        "type": "Volunteer-Driven Food Rescue",
        "url": "https://robinhoodarmy.com/",
        "contact_email": "info@robinhoodarmy.com",
    },

    # UNITED STATES
    {
        "country": "United States",
        "cities": ["New York", "New York City", "Brooklyn", "Queens", "Bronx"],
        "name": "City Harvest",
        "type": "Metro Food Rescue & Distribution",
        "url": "https://www.cityharvest.org/",
        "contact_email": "foodrescue@cityharvest.org",
    },
    {
        "country": "United States",
        "cities": ["New York", "Los Angeles", "Chicago", "Boston", "Seattle", "San Francisco", "Washington", "New Haven", "Detroit", "Miami"],
        "name": "Food Rescue US",
        "type": "App-Based Hyper-Local Food Transfer",
        "url": "https://foodrescue.us/",
        "contact_email": "info@foodrescue.us",
    },

    # CANADA
    {
        "country": "Canada",
        "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Winnipeg"],
        "name": "Second Harvest Canada",
        "type": "National Food Rescue Logistics",
        "url": "https://www.secondharvest.ca/",
        "contact_email": "support@secondharvest.ca",
    },

    # UNITED KINGDOM
    {
        "country": "United Kingdom",
        "cities": ["London", "Manchester", "Birmingham", "Liverpool", "Bristol", "Leeds", "Glasgow", "Edinburgh", "Cardiff"],
        "name": "FareShare UK",
        "type": "Charity Food Redistribution Network",
        "url": "https://fareshare.org.uk/",
        "contact_email": "enquiries@fareshare.org.uk",
    },

    # AUSTRALIA
    {
        "country": "Australia",
        "cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra", "Gold Coast", "Newcastle"],
        "name": "OzHarvest",
        "type": "Perishable Food Rescue Fleet",
        "url": "https://www.ozharvest.org/",
        "contact_email": "info@ozharvest.org",
    },

    # NEW ZEALAND
    {
        "country": "New Zealand",
        "cities": ["Wellington", "Lower Hutt", "Porirua", "Kapiti"],
        "name": "Kaibosh Food Rescue",
        "type": "Regional Food Rescue",
        "url": "https://www.kaibosh.org.nz/",
        "contact_email": "info@kaibosh.org.nz",
    },

    # SINGAPORE
    {
        "country": "Singapore",
        "cities": ["Singapore"],
        "name": "The Food Bank Singapore",
        "type": "Food Bank & Redistribution Depots",
        "url": "https://foodbank.sg/",
        "contact_email": "enquiries@foodbank.sg",
    },

    # SOUTH AFRICA
    {
        "country": "South Africa",
        "cities": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Gqeberha", "Port Elizabeth"],
        "name": "FoodForward SA",
        "type": "Recovery & Redistribution Infrastructure",
        "url": "https://foodforwardsa.org/",
        "contact_email": "info@foodforwardsa.org",
    },

    # KENYA
    {
        "country": "Kenya",
        "cities": ["Nairobi", "Mombasa", "Kisumu"],
        "name": "Food Banking Kenya",
        "type": "Regional Hub & Farm Recovery",
        "url": "https://foodbankingkenya.org/",
        "contact_email": "info@foodbankingkenya.org",
    },

    # NIGERIA
    {
        "country": "Nigeria",
        "cities": ["Lagos", "Abuja", "Ibadan"],
        "name": "Lagos Food Bank Initiative",
        "type": "Hunger Relief & Malnutrition Programs",
        "url": "https://lagosfoodbank.org/",
        "contact_email": "contactus@lagosfoodbank.org",
    },

    # INDONESIA
    {
        "country": "Indonesia",
        "cities": ["Bali", "Denpasar", "Jakarta"],
        "name": "Scholars of Sustenance (SOS) Indonesia",
        "type": "Cooked Surplus Recovery & Relief",
        "url": "https://www.scholarsofsustenance.org/sos-indonesia",
        "contact_email": "indonesia@scholarsofsustenance.org",
    },
    {
        "country": "Indonesia",
        "cities": ["Jakarta", "Bandung", "Surabaya"],
        "name": "FoodCycle Indonesia",
        "type": "Surplus Redistribution & Food Waste Prevention",
        "url": "https://www.foodcycle.id/",
        "contact_email": "info@foodcycle.id",
    },

    # MALAYSIA
    {
        "country": "Malaysia",
        "cities": ["Kuala Lumpur", "Petaling Jaya", "Shah Alam", "George Town"],
        "name": "The Lost Food Project",
        "type": "Surplus Rescue & Distribution",
        "url": "https://www.thelostfoodproject.org/",
        "contact_email": "info@thelostfoodproject.org",
    },

    # BRAZIL
    {
        "country": "Brazil",
        "cities": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Belo Horizonte"],
        "name": "Mesa Brasil SESC",
        "type": "National Network of Food Banks",
        "url": "https://www.sesc.com.br/atuacoes/assistencia/mesa-brasil/",
        "contact_email": "mesabrasil@sesc.com.br",
    },

    # MEXICO
    {
        "country": "Mexico",
        "cities": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "Querétaro"],
        "name": "BAMX (Red de Bancos de Alimentos de México)",
        "type": "National Food Bank Federation",
        "url": "https://bamx.org.mx/",
        "contact_email": "contacto@bamx.org.mx",
    },

    # SPAIN
    {
        "country": "Spain",
        "cities": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao", "Málaga"],
        "name": "FESBAL (Federación Española de Bancos de Alimentos)",
        "type": "National Federation of Regional Food Banks",
        "url": "https://www.fesbal.org/",
        "contact_email": "comunicacion@fesbal.org",
    },

    # GERMANY
    {
        "country": "Germany",
        "cities": ["Berlin", "Hamburg", "Munich", "Frankfurt", "Cologne", "Stuttgart"],
        "name": "Tafel Deutschland e.V.",
        "type": "Food Distribution Stations & Volunteer Hubs",
        "url": "https://www.tafel.de/",
        "contact_email": "info@tafel.de",
    },

    # FRANCE
    {
        "country": "France",
        "cities": ["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux", "Lille"],
        "name": "Fédération Française des Banques Alimentaires",
        "type": "Surplus Recovery & Food Security Network",
        "url": "https://www.banquealimentaire.org/",
        "contact_email": "ffba@banquealimentaire.org",
    },

    # IRELAND
    {
        "country": "Ireland",
        "cities": ["Dublin", "Cork", "Galway", "Limerick", "Waterford"],
        "name": "FoodCloud",
        "type": "Digital Technology & Logistics Platform",
        "url": "https://food.cloud/",
        "contact_email": "info@food.cloud",
    },
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
    "cdmx": "Mexico City",
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

def create_email_link(org, name, email, food, quantity, city, notes):
    subject = f"Surplus Food Donation Enquiry — {city}"
    body = f"""Hello {org['name']} Team,

I have surplus food available for redistribution in {city} and would like to coordinate a drop-off or collection if suitable.

Donor Details:
• Contact Person: {name}
• Email: {email}
• Food Description: {food}
• Quantity / Servings: {quantity}
• Pickup Location: {city}
• Timings & Condition: {notes}

Please let me know if your team can accept this batch or if you can redirect me to an active partner facility.

Best regards,
{name}
"""
    recipient = org.get("contact_email", "")
    return f"mailto:{recipient}?subject={quote(subject)}&body={quote(body)}"

# ------------------------------------------------------------
# SESSION STATE INITIALIZATION
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
# MODERN EDITORIAL STYLING
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');

:root {
    --bg: #F8F9FA;
    --surface: #FFFFFF;
    --text-primary: #192521;
    --text-secondary: #566461;
    --brand-green: #245A46;
    --brand-green-hover: #194032;
    --accent-sand: #F4F1EA;
    --accent-terracotta: #C85A32;
    --border-light: #E5E9E7;
}

.stApp {
    background-color: var(--bg);
    color: var(--text-primary);
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}

h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
}

.brand-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 2.5rem;
}

.brand-logo {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--brand-green);
    letter-spacing: -0.03em;
}

.tag-badge {
    background: #E8EFEA;
    color: var(--brand-green);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 6px 14px;
    border-radius: 999px;
    text-transform: uppercase;
}

.hero-box {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    box-shadow: 0 4px 20px -4px rgba(0, 0, 0, 0.03);
    margin-bottom: 2rem;
}

.hero-headline {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    line-height: 1.15;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0.5rem 0 1.2rem;
}

.hero-sub {
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 720px;
    margin: 0;
}

.step-card {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px -2px rgba(0, 0, 0, 0.02);
    height: 100%;
}

.step-index {
    color: var(--accent-terracotta);
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
}

.step-heading {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0.4rem 0;
    color: var(--text-primary);
}

.step-desc {
    color: var(--text-secondary);
    font-size: 0.92rem;
    line-height: 1.5;
    margin: 0;
}

.section-tag {
    font-size: 0.75rem;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: var(--accent-terracotta);
    margin-bottom: 0.6rem;
}

.pill-meta {
    display: inline-block;
    background: var(--accent-sand);
    color: var(--text-secondary);
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 6px;
    margin-right: 6px;
    margin-bottom: 8px;
}

.callout-banner {
    background: #FFF9F2;
    border: 1px solid #F5DEB3;
    border-left: 4px solid var(--accent-terracotta);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-size: 0.9rem;
    line-height: 1.5;
    color: #634533;
    margin: 1.5rem 0;
}

/* Button & Streamlit Elements */
.stButton > button {
    background-color: var(--brand-green) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.15s ease-in-out !important;
}

.stButton > button:hover {
    background-color: var(--brand-green-hover) !important;
    box-shadow: 0 4px 12px rgba(36, 90, 70, 0.25) !important;
}

.stLinkButton > a {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}

[data-testid="stChatMessage"] {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    margin-bottom: 0.75rem;
}

.footer-copy {
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin-top: 5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-light);
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# TOP NAVIGATION & HERO
# ------------------------------------------------------------
st.markdown("""
<div class="brand-nav">
    <div class="brand-logo">plateful.</div>
    <div class="tag-badge">Food Rescue Logistics</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="section-tag">Direct Redistribution Network</div>
    <div class="hero-headline">Good food deserves a second destination.</div>
    <p class="hero-sub">
        Every day, commercial kitchens, catered events, and households have fresh meals left over.
        Plateful helps you route excess edible food to established community kitchens and redistribution non-profits.
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# THREE SIMPLE STEPS
# ------------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-index">STEP 01</div>
        <div class="step-heading">Provide Context</div>
        <p class="step-desc">Share where you are located, the kind of food you have, and approximate portion counts.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-index">STEP 02</div>
        <div class="step-heading">Find Local Nodes</div>
        <p class="step-desc">Identify verified partners operating in your specific metropolitan area.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-index">STEP 03</div>
        <div class="step-heading">Hand-off Details</div>
        <p class="step-desc">Generate pre-formatted logistics emails to confirm collection, packaging, and safety standards.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# CONVERSATIONAL ASSISTANT INTERFACE
# ------------------------------------------------------------
st.markdown("<div class=\"section-tag\">Directory Assistant</div>", unsafe_allow_html=True)
st.markdown("### How can we help you redistribute today?")

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("E.g., 'We have 40 catered trays left over in Toronto' or 'Food rescue in Delhi'")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    intent = detect_intent(user_input)
    city = detect_city(user_input)

    if intent == "greeting":
        reply = (
            "Hello! I am ready to help coordinate your food donation. "
            "Let me know **what city you are located in** and a brief description of what you have to donate."
        )
        orgs = []
    elif intent == "surplus" and not city:
        reply = (
            "We can definitely find a destination for that surplus. "
            "**Which city are you located in?**"
        )
        orgs = []
    elif city:
        orgs = find_orgs(city)
        if orgs:
            reply = (
                f"We identified **{len(orgs)} verified redistribution partner(s)** serving **{city}**.\n\n"
                "Browse the details below to review their operations or prepare a pre-filled donation enquiry."
            )
        else:
            reply = (
                f"We currently do not have a pre-indexed partner active in **{city}** in this prototype database. "
                "For unlisted areas, regional food banks or municipal relief services are often available through local council directories."
            )
    else:
        reply = (
            "I can assist with locating food rescue organizations.\n\n"
            "Try specifying your location:\n"
            "- *“Who takes extra banquet meals in New York?”*\n"
            "- *“We have 30 lunch boxes left over in Mumbai.”*\n"
            "- *“Surplus baked goods in London.”*"
        )
        orgs = []

    st.session_state.last_city = city
    st.session_state.last_results = orgs
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ------------------------------------------------------------
# MATCHED ORGANISATIONS SECTION
# ------------------------------------------------------------
if st.session_state.last_results:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class=\"section-tag\">Results for {st.session_state.last_city}</div>", unsafe_allow_html=True)

    for index, org in enumerate(st.session_state.last_results):
        with st.container(border=True):
            head_col, action_col = st.columns([2.5, 1.5])
            
            with head_col:
                st.markdown(f"#### {org['name']}")
                st.markdown(
                    f"<span class='pill-meta'>{org['country']}</span>"
                    f"<span class='pill-meta'>{org['type']}</span>",
                    unsafe_allow_html=True
                )
                coverage_str = ", ".join(org['cities'][:6]) + ("..." if len(org['cities']) > 6 else "")
                st.caption(f"**Key Hubs:** {coverage_str}")

            with action_col:
                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                st.link_button(
                    "Visit Website ↗",
                    org["url"],
                    use_container_width=True
                )
                if st.button(
                    "Draft Donation Notice",
                    key=f"record_{index}",
                    use_container_width=True
                ):
                    st.session_state.selected_org = index
                    st.session_state.request_recorded = True
                    st.rerun()

    st.markdown("""
    <div class="callout-banner">
        <strong>Important Safety Reminder:</strong> Food safety regulations require that perishable foods maintain temperature integrity.
        Always verify whether the receiving agency accepts prepared meals, unpackaged items, or requires commercial packaging before dispatching.
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# DRAFT ENQUIRY WORKFLOW
# ------------------------------------------------------------
if st.session_state.request_recorded and st.session_state.last_results:
    selected_idx = st.session_state.selected_org
    if selected_idx < len(st.session_state.last_results):
        org = st.session_state.last_results[selected_idx]
        city = st.session_state.last_city

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class=\"section-tag\">Prepare Communication</div>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(f"### Donation Notification for {org['name']}")
            st.markdown(f"Generate a standardized notification for operations in **{city}**.")

            with st.form("donation_request_form"):
                fc1, fc2 = st.columns(2)
                with fc1:
                    name = st.text_input("Your Name / Establishment", placeholder="e.g., Green Garden Bistro")
                    food = st.text_input("Food Item Description", placeholder="e.g., Chilled vegetarian pasta meals (freshly packed)")
                with fc2:
                    email = st.text_input("Contact Email", placeholder="e.g., manager@greengarden.com")
                    quantity = st.text_input("Quantity / Portions", placeholder="e.g., 35 individual containers")

                notes = st.text_area(
                    "Logistics & Temperature Notes",
                    placeholder="e.g., Cooked at 2 PM, refrigerated since 4 PM. Available for pickup until 9 PM today."
                )

                submit_btn = st.form_submit_button("Generate Direct Email Link", use_container_width=True)

            if submit_btn:
                if not name or not email or not food or not quantity:
                    st.error("Please fill in all mandatory fields (Name, Email, Food, and Quantity).")
                else:
                    email_link = create_email_link(org, name, email, food, quantity, city, notes)
                    st.success("Enquiry message compiled!")
                    
                    st.markdown(
                        f"Target Contact: `{org.get('contact_email', 'Official Channels')}`"
                    )
                    st.link_button(
                        f"Open in Mail Client & Send to {org['name']} →",
                        email_link,
                        use_container_width=True
                    )

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("""
<div class="footer-copy">
    Plateful Directory Prototype · Facilitating responsible redistribution of excess resources.
</div>
""", unsafe_allow_html=True)
