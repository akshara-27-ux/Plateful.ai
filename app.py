import re
from datetime import datetime
from urllib.parse import quote
import streamlit as st

# ============================================================
# PLATEFUL — FOOD REDISTRIBUTION DIRECTORY & LOGISTICS
# ============================================================

st.set_page_config(
    page_title="Plateful — Food Redistribution",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# COMPREHENSIVE GLOBAL DIRECTORY
# ------------------------------------------------------------
ORGS = [
    # SOUTH ASIA — INDIA
    {
        "country": "India",
        "state": "Multi-State",
        "supported_states": ["Delhi", "Tamil Nadu", "Karnataka", "Telangana", "Andhra Pradesh"],
        "cities": ["Delhi", "New Delhi", "Chennai", "Bengaluru", "Coimbatore", "Hyderabad", "Tadepalligudem"],
        "neighborhoods": ["Connaught Place", "Dwarka", "Indiranagar", "Koramangala", "T Nagar", "Adyar", "Banjara Hills", "Hitec City", "RS Puram", "Gandhipuram", "Peelamedu"],
        "name": "No Food Waste",
        "type": "Surplus Food Rescue & Logistics",
        "url": "https://nofoodwaste.org/",
        "contact_email": "info@nofoodwaste.org",
        "whatsapp": "919087790877",
    },
    {
        "country": "India",
        "state": "Multi-State",
        "supported_states": ["Delhi", "Maharashtra", "Karnataka", "Telangana", "Tamil Nadu", "West Bengal", "Gujarat", "Rajasthan", "Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Kerala", "Andhra Pradesh", "Bihar"],
        "cities": ["Delhi", "New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Chandigarh", "Lucknow", "Indore", "Kochi", "Bhopal", "Visakhapatnam", "Nagpur", "Patna", "Ludhiana", "Agra", "Nashik", "Vadodara", "Varanasi"],
        "neighborhoods": ["Bandra", "Andheri", "Juhu", "Hauz Khas", "Saket", "Whitefield", "Jayanagar", "Salt Lake", "Park Street", "Gomti Nagar", "Hazratganj", "C-Scheme", "Malviya Nagar", "Cyber City", "Sector 18", "Ballygunge"],
        "name": "Feeding India (by Zomato)",
        "type": "Hunger Relief & Large Redistribution Network",
        "url": "https://www.feedingindia.org/",
        "contact_email": "contact@feedingindia.org",
        "whatsapp": "919871113411",
    },
    {
        "country": "India",
        "state": "Multi-State",
        "supported_states": ["Delhi", "Maharashtra", "Karnataka", "Telangana", "Tamil Nadu", "West Bengal", "Gujarat", "Rajasthan", "Assam", "Odisha", "Uttarakhand", "Punjab", "Jharkhand", "Goa"],
        "cities": ["Delhi", "New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Guwahati", "Bhubaneswar", "Dehradun", "Amritsar", "Ranchi", "Surat", "Goa"],
        "neighborhoods": ["Colaba", "Dadar", "Powai", "Rohini", "Karol Bagh", "HSR Layout", "Indiranagar", "Kothrud", "Viman Nagar", "Panaji", "Margao", "Paltan Bazaar", "GS Road", "Saheed Nagar"],
        "name": "Robin Hood Army",
        "type": "Volunteer-Driven Food Rescue",
        "url": "https://robinhoodarmy.com/",
        "contact_email": "info@robinhoodarmy.com",
        "whatsapp": "918976450903",
    },
    {
        "country": "India",
        "state": "Kerala",
        "supported_states": ["Kerala"],
        "cities": ["Kochi", "Ernakulam", "Thiruvananthapuram", "Kozhikode", "Thrissur"],
        "neighborhoods": ["Kakkanad", "Edappally", "Fort Kochi", "MG Road", "Pattom", "Kazhakoottam", "Technopark", "Mananchira", "Marine Drive"],
        "name": "Anbodu Kochi & Nanma Maram Community Fridges",
        "type": "Urban Community Fridges & Excess Food Rescue",
        "url": "https://www.facebook.com/AnboduKochi/",
        "contact_email": "anbodukochi@gmail.com",
        "whatsapp": "919447171111",
    },
    {
        "country": "India",
        "state": "Tamil Nadu",
        "supported_states": ["Tamil Nadu"],
        "cities": ["Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Chennai"],
        "neighborhoods": ["KK Nagar", "Anna Nagar", "Thillai Nagar", "Cantonment", "Fairlands", "Mylapore", "Velachery", "OMR"],
        "name": "Aram Porul Foundation",
        "type": "Regional Surplus Food Collection",
        "url": "https://aramporul.org/",
        "contact_email": "contact@aramporul.org",
        "whatsapp": "919790012345",
    },
    {
        "country": "India",
        "state": "Karnataka",
        "supported_states": ["Karnataka"],
        "cities": ["Bengaluru", "Mysuru", "Mangaluru"],
        "neighborhoods": ["Malleshwaram", "Basavanagudi", "Electronic City", "Hebbal", "Gokulam", "Jayalakshmipuram", "Hampankatta", "Kadri"],
        "name": "Hasiru Dala Community Feeds",
        "type": "Urban Worker Relief & Surplus Rescue",
        "url": "https://hasirudala.in/",
        "contact_email": "info@hasirudala.in",
        "whatsapp": "918026600266",
    },
    {
        "country": "India",
        "state": "Maharashtra",
        "supported_states": ["Maharashtra"],
        "cities": ["Mumbai", "Thane", "Navi Mumbai"],
        "neighborhoods": ["Dharavi", "Ghatkopar", "Borivali", "Chembur", "Vashi", "Nerul", "Thane West", "Ghansoli", "Belapur"],
        "name": "Roti Bank by Dabbawalas",
        "type": "Prepared Surplus & Banquet Redistribution",
        "url": "https://rotibankfoundation.org/",
        "contact_email": "info@rotibankfoundation.org",
        "whatsapp": "918655580001",
    },
    {
        "country": "India",
        "state": "Telangana",
        "supported_states": ["Telangana", "Andhra Pradesh"],
        "cities": ["Hyderabad", "Secunderabad", "Warangal", "Visakhapatnam", "Vijayawada"],
        "neighborhoods": ["Madhapur", "Gachibowli", "Kukatpally", "Begumpet", "Jubilee Hills", "Charminar", "Hanamkonda"],
        "name": "Apple Homes (Feed The Needy)",
        "type": "Community Refrigerators & Night Runs",
        "url": "https://feedtheneedy.in/",
        "contact_email": "support@feedtheneedy.in",
        "whatsapp": "917997998788",
    },
    {
        "country": "India",
        "state": "West Bengal",
        "supported_states": ["West Bengal"],
        "cities": ["Kolkata", "Howrah"],
        "neighborhoods": ["Ballygunge", "Gariahat", "New Town", "Shyambazar", "Howrah Station", "Dum Dum", "Alipore"],
        "name": "Sanjhbati Food Bank & Relief",
        "type": "Community Food Pantry & Surplus Rescue",
        "url": "https://sanjhbati.org/",
        "contact_email": "contact@sanjhbati.org",
        "whatsapp": "919830098300",
    },
    {
        "country": "India",
        "state": "Odisha",
        "supported_states": ["Odisha"],
        "cities": ["Bhubaneswar", "Cuttack", "Puri"],
        "neighborhoods": ["Saheed Nagar", "Patia", "Khandagiri", "Badambadi", "CDA Sector", "Grand Road"],
        "name": "Aahwahan Foundation (Odisha Chapter)",
        "type": "Event & Banquet Surplus Recovery",
        "url": "https://aahwahan.com/",
        "contact_email": "info@aahwahan.com",
        "whatsapp": "917795554321",
    },

    # UNITED STATES
    {
        "country": "United States",
        "state": "New York",
        "supported_states": ["New York", "New Jersey"],
        "cities": ["New York", "New York City", "Brooklyn", "Queens", "Bronx", "Staten Island", "Jersey City"],
        "neighborhoods": ["Harlem", "Midtown", "East Village", "Upper West Side", "SoHo", "Lower East Side", "Williamsburg", "Bushwick", "DUMBO", "Bedford-Stuyvesant", "Crown Heights", "Astoria", "Flushing", "Long Island City", "South Bronx"],
        "name": "City Harvest",
        "type": "Metro Food Rescue & Fleet Redistribution",
        "url": "https://www.cityharvest.org/",
        "contact_email": "foodrescue@cityharvest.org",
        "whatsapp": "16464159600",
    },
    {
        "country": "United States",
        "state": "Multi-State",
        "supported_states": ["California", "Illinois", "Massachusetts", "Washington", "Connecticut", "Michigan", "Florida", "District of Columbia"],
        "cities": ["New York", "Los Angeles", "Chicago", "Boston", "Seattle", "San Francisco", "Washington", "New Haven", "Detroit", "Miami"],
        "neighborhoods": ["Downtown LA", "Hollywood", "Santa Monica", "Venice", "Silver Lake", "Koreatown", "Mission District", "SoMa", "Tenderloin", "Sunset District", "Lincoln Park", "Logan Square", "Wicker Park", "Pilsen", "Hyde Park", "Back Bay", "South End", "Dorchester", "Cambridge", "Somerville", "Capitol Hill", "Ballard", "Brickell", "Wynwood", "Georgetown", "Adams Morgan"],
        "name": "Food Rescue US",
        "type": "App-Based Hyper-Local Food Transfer",
        "url": "https://foodrescue.us/",
        "contact_email": "info@foodrescue.us",
        "whatsapp": "18008773728",
    },

    # UNITED KINGDOM
    {
        "country": "United Kingdom",
        "state": "UK",
        "supported_states": ["England", "Scotland", "Wales"],
        "cities": ["London", "Manchester", "Birmingham", "Liverpool", "Bristol", "Leeds", "Glasgow", "Edinburgh", "Cardiff"],
        "neighborhoods": ["Westminster", "Camden", "Hackney", "Islington", "Brixton", "Shoreditch", "Southwark", "Tower Hamlets", "Kensington", "Lewisham", "Greenwich", "Northern Quarter", "Ancoats", "Didsbury", "Digbeth", "Edgbaston", "Old Town", "Leith", "West End"],
        "name": "FareShare UK",
        "type": "Charity Food Redistribution Network",
        "url": "https://fareshare.org.uk/",
        "contact_email": "enquiries@fareshare.org.uk",
        "whatsapp": "442073942464",
    },
]

STATE_ALIASES = {
    "andhra pradesh": ("Andhra Pradesh", "India"),
    "delhi": ("Delhi", "India"),
    "karnataka": ("Karnataka", "India"),
    "kerala": ("Kerala", "India"),
    "maharashtra": ("Maharashtra", "India"),
    "tamil nadu": ("Tamil Nadu", "India"),
    "telangana": ("Telangana", "India"),
    "uttar pradesh": ("Uttar Pradesh", "India"),
    "west bengal": ("West Bengal", "India"),
    "california": ("California", "United States"),
    "new york": ("New York", "United States"),
}

CITY_ALIASES = {
    "delhi": "Delhi",
    "mumbai": "Mumbai",
    "bengaluru": "Bengaluru",
    "bangalore": "Bengaluru",
    "chennai": "Chennai",
    "hyderabad": "Hyderabad",
    "kolkata": "Kolkata",
    "kochi": "Kochi",
    "pune": "Pune",
    "lucknow": "Lucknow",
    "new york": "New York",
    "nyc": "New York",
    "los angeles": "Los Angeles",
    "london": "London",
}

def clean(text):
    return re.sub(r"\s+", " ", str(text).lower().strip())

def canonical_city(text):
    value = clean(text)
    return CITY_ALIASES.get(value, str(text).strip().title())

def extract_portion_count(text):
    match = re.search(r"\b(\d+)\s*(meals?|portions?|servings?|boxes|trays?|people|persons?|packets?)\b", clean(text))
    if match:
        return int(match.group(1))
    return None

def compute_impact(meals):
    if not meals or meals <= 0:
        return None
    food_kg = round(meals * 0.45, 1)
    co2_saved_kg = round(meals * 1.15, 1)
    water_liters = round(meals * 380)
    return {
        "meals": meals,
        "food_kg": food_kg,
        "co2_saved_kg": co2_saved_kg,
        "water_liters": water_liters,
    }

def get_user_rank(total_meals):
    """Calculates gamified level and achievements based on session activity."""
    if total_meals >= 300:
        return "🌍 Planetary Guardian", "Max Tier", 1.0, "🏆 Unlocked All Badges"
    elif total_meals >= 150:
        next_tier = 300
        prog = total_meals / next_tier
        return "🥇 Hunger Hero", f"{total_meals}/{next_tier} to Planetary Guardian", prog, "Unlocked: 🥉 First Rescue, 🥈 Community Feeder, 🥇 Hunger Hero"
    elif total_meals >= 50:
        next_tier = 150
        prog = total_meals / next_tier
        return "🥈 Community Feeder", f"{total_meals}/{next_tier} to Hunger Hero", prog, "Unlocked: 🥉 First Rescue, 🥈 Community Feeder"
    elif total_meals > 0:
        next_tier = 50
        prog = total_meals / next_tier
        return "🥉 First Responder", f"{total_meals}/{next_tier} to Community Feeder", prog, "Unlocked: 🥉 First Rescue"
    else:
        return "🌱 Green Rookie", "Log 1st donation to level up", 0.05, "No badges unlocked yet"

def detect_location(text):
    t = clean(text)
    detected_country = None
    all_countries = {org["country"] for org in ORGS}
    for c in sorted(all_countries, key=len, reverse=True):
        if re.search(r"(?<!\w)" + re.escape(c.lower()) + r"(?!\w)", t):
            detected_country = c
            break

    detected_state = None
    for alias_s, (canonical_s, country_s) in sorted(STATE_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if re.search(r"(?<!\w)" + re.escape(alias_s) + r"(?!\w)", t):
            detected_state = canonical_s
            detected_country = country_s
            break

    for alias_k, canonical_v in sorted(CITY_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if re.search(r"(?<!\w)" + re.escape(alias_k) + r"(?!\w)", t):
            return canonical_v, alias_k.title(), detected_state, detected_country

    for org in ORGS:
        for hood in org.get("neighborhoods", []):
            if re.search(r"(?<!\w)" + re.escape(hood.lower()) + r"(?!\w)", t):
                return org["cities"][0], hood, detected_state or org.get("state"), org.get("country")
        for city in org.get("cities", []):
            if re.search(r"(?<!\w)" + re.escape(city.lower()) + r"(?!\w)", t):
                return canonical_city(city), None, detected_state or org.get("state"), org.get("country")

    return None, None, detected_state, detected_country

def detect_intent(text):
    t = clean(text)
    location_words = ["where", "find", "near", "ngo", "charity", "food bank", "donate", "pickup", "redistribute"]
    surplus_words = ["leftover", "surplus", "extra food", "meals left", "cooked too much", "unused food"]
    if any(x in t for x in surplus_words) and any(x in t for x in location_words):
        return "surplus_location"
    if any(x in t for x in location_words):
        return "find"
    if any(x in t for x in surplus_words):
        return "surplus"
    return "general"

def find_orgs(city=None, neighborhood=None, state=None, country=None):
    if not city and not neighborhood and not state and not country:
        return []
    canonical = canonical_city(city) if city else None
    matched_results = []
    for org in ORGS:
        city_match = False
        hood_match = False
        state_match = False
        country_match = False
        if country and clean(org.get("country", "")) == clean(country):
            country_match = True
        elif country and clean(org.get("country", "")) != clean(country):
            continue
        if canonical:
            city_match = any(clean(c) == clean(canonical) for c in org.get("cities", []))
        if neighborhood:
            hood_match = any(clean(h) == clean(neighborhood) for h in org.get("neighborhoods", []))
        if state:
            state_match = clean(org.get("state", "")) == clean(state) or any(clean(s) == clean(state) for s in org.get("supported_states", []))

        if hood_match or city_match or state_match or (country_match and not city and not state and not neighborhood):
            matched_results.append({
                **org,
                "is_hyperlocal": hood_match,
                "is_city_match": city_match,
                "is_state_match": state_match,
            })
    return sorted(matched_results, key=lambda x: (x.get("is_hyperlocal", False), x.get("is_city_match", False)), reverse=True)

def create_email_link(org, name, email, food, quantity, location_str, notes):
    subject = f"Surplus Food Donation Enquiry — {location_str}"
    body = f"""Hello {org['name']} Team,\n\nI have surplus food available for redistribution in {location_str}.\n\nDonor Details:\n• Contact: {name}\n• Email: {email}\n• Food: {food}\n• Quantity: {quantity}\n• Details: {notes}\n\nBest regards,\n{name}"""
    return f"mailto:{org.get('contact_email', '')}?subject={quote(subject)}&body={quote(body)}"

def create_whatsapp_link(org, name, food, quantity, location_str, notes):
    phone = org.get("whatsapp", "")
    text_msg = f"🌱 *Food Donation Enquiry — Plateful Relay*\n\n*Donor:* {name}\n*Location:* {location_str}\n*Items:* {food}\n*Quantity:* {quantity}\n*Notes:* {notes}"
    return f"https://wa.me/{phone}?text={quote(text_msg)}"

def generate_csv_receipt(name, food, quantity, location, org_name, notes, impact):
    co2 = impact["co2_saved_kg"] if impact else "N/A"
    water = impact["water_liters"] if impact else "N/A"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_rows = [
        "Timestamp,Donor Name,Food Item,Quantity,Location,Assigned Partner,CO2 Prevented (kg),Water Saved (L),Notes",
        f'"{timestamp}","{name}","{food}","{quantity}","{location}","{org_name}","{co2}","{water}","{notes}"'
    ]
    return "\n".join(csv_rows)

# ------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------------------------------------
defaults = {
    "messages": [],
    "last_results": [],
    "last_city": None,
    "last_neighborhood": None,
    "last_state": None,
    "last_country": None,
    "display_location": None,
    "last_portions": None,
    "request_recorded": False,
    "selected_org": None,
    # Gamification Stats
    "total_rescued_meals": 0,
    "total_dispatches": 0,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ------------------------------------------------------------
# DARK EDITORIAL CSS
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');

:root {
    --bg: #0D1117;
    --surface: #161B22;
    --surface-elevated: #21262D;
    --text-primary: #FFFFFF;
    --text-secondary: #9DA7B3;
    --brand-green: #238636;
    --brand-green-hover: #2EA043;
    --accent-orange: #F0883E;
    --border-light: #30363D;
}
.stApp {
    background-color: var(--bg) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.brand-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 1.5rem;
}
.brand-logo {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2rem;
    font-weight: 700;
    color: #56D364;
}
.tag-badge {
    background: #1F3B2C;
    color: #7EE787;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 999px;
    border: 1px solid #2EA043;
}
.hero-box {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: 2.2rem;
    margin-bottom: 1.5rem;
}
.gamify-card {
    background: #131A21;
    border: 1px solid #238636;
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
}
.pill-meta {
    display: inline-block;
    background: var(--surface-elevated);
    color: #E6EDF3;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid var(--border-light);
    margin-right: 6px;
}
.pill-local {
    display: inline-block;
    background: #1F3B2C;
    color: #7EE787;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid #2EA043;
    margin-right: 6px;
}
.pill-state {
    display: inline-block;
    background: #2E1F3B;
    color: #D2A8FF;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid #8957E5;
    margin-right: 6px;
}
.stButton > button {
    background-color: var(--brand-green) !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# TOP NAVIGATION
# ------------------------------------------------------------
st.markdown("""
<div class="brand-nav">
    <div class="brand-logo">plateful.</div>
    <div class="tag-badge">Global Active Relay</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# GAMIFICATION & REWARDS TRACKER
# ------------------------------------------------------------
rank_title, rank_sub, rank_prog, badges_unlocked = get_user_rank(st.session_state.total_rescued_meals)

st.markdown(f"""
<div class="gamify-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div>
            <span style="font-size: 0.75rem; color: #F0883E; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em;">Rescue Tier</span>
            <div style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">{rank_title}</div>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.75rem; color: #9DA7B3; text-transform: uppercase; font-weight: 600;">Lifetime Session Score</span>
            <div style="font-size: 1.2rem; font-weight: 700; color: #7EE787;">{st.session_state.total_rescued_meals} Meals Salvaged</div>
        </div>
    </div>
    <div style="font-size: 0.85rem; color: #9DA7B3; margin-bottom: 8px;">{badges_unlocked} · <em>{rank_sub}</em></div>
</div>
""", unsafe_allow_html=True)
st.progress(rank_prog)

# ------------------------------------------------------------
# HERO BANNER
# ------------------------------------------------------------
st.markdown("""
<div class="hero-box">
    <h1 style="margin-top:0;">Good food deserves a second destination.</h1>
    <p style="color:#9DA7B3; max-width:700px; margin-bottom:0;">
        Route commercial and event food excess directly to local volunteer networks, community kitchens, and food banks.
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# CHAT ASSISTANT
# ------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("E.g., 'We have 40 meals left over in Indiranagar, Bangalore' or 'Surplus food in Brooklyn'")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    city, neighborhood, state, country = detect_location(user_input)
    portions = extract_portion_count(user_input)

    location_parts = [p for p in [neighborhood, city, state, country] if p]
    display_loc = ", ".join(dict.fromkeys(location_parts)) if location_parts else None
    impact_data = compute_impact(portions)

    if display_loc:
        orgs = find_orgs(city=city, neighborhood=neighborhood, state=state, country=country)
        if orgs:
            reply = f"Identified **{len(orgs)} verified partner(s)** matching **{display_loc}**."
        else:
            reply = f"No pre-indexed partner found for **{display_loc}**. Municipal food pantries or religious community kitchens may accept direct safe drop-offs."
    else:
        reply = "Please specify your neighborhood or city (e.g., *'Indiranagar, Bangalore'* or *'Brooklyn, NYC'*)."
        orgs = []

    if impact_data:
        reply += (
            f"\n\n**Estimated Impact ({impact_data['meals']} Portions):**\n"
            f"- 🥗 **{impact_data['food_kg']} kg** food preserved\n"
            f"- ☁️ **{impact_data['co2_saved_kg']} kg** CO₂e emissions prevented\n"
            f"- 💧 **{impact_data['water_liters']} L** water footprint conserved"
        )

    st.session_state.last_city = city
    st.session_state.last_neighborhood = neighborhood
    st.session_state.last_state = state
    st.session_state.last_country = country
    st.session_state.display_location = display_loc
    st.session_state.last_portions = portions
    st.session_state.last_results = orgs
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ------------------------------------------------------------
# RESULTS SECTION
# ------------------------------------------------------------
if st.session_state.last_results:
    st.markdown(f"### Results for {st.session_state.display_location}")
    for index, org in enumerate(st.session_state.last_results):
        with st.container(border=True):
            head_col, action_col = st.columns([2.5, 1.5])
            with head_col:
                st.markdown(f"#### {org['name']}")
                tags = f"<span class='pill-meta'>{org['country']}</span>"
                if org.get("is_hyperlocal"):
                    tags += "<span class='pill-local'>Neighborhood Match</span>"
                elif org.get("state"):
                    tags += f"<span class='pill-state'>{org['state']}</span>"
                st.markdown(tags, unsafe_allow_html=True)
                if org.get("neighborhoods"):
                    st.caption(f"📍 Notable Local Hubs: {', '.join(org['neighborhoods'][:5])}")
            with action_col:
                st.link_button("Visit Website ↗", org["url"], use_container_width=True)
                if st.button("Coordinate Dispatch Notice", key=f"record_{index}", use_container_width=True):
                    st.session_state.selected_org = index
                    st.session_state.request_recorded = True
                    st.rerun()

# ------------------------------------------------------------
# DISPATCH + VALIDATION + REWARDS WORKFLOW
# ------------------------------------------------------------
if st.session_state.request_recorded and st.session_state.last_results:
    selected_idx = st.session_state.selected_org
    if selected_idx < len(st.session_state.last_results):
        org = st.session_state.last_results[selected_idx]
        loc_str = st.session_state.display_location or "your location"
        default_qty = f"{st.session_state.last_portions} portions" if st.session_state.last_portions else ""

        with st.container(border=True):
            st.markdown(f"### Dispatch Notice: {org['name']}")

            with st.form("donation_request_form"):
                fc1, fc2 = st.columns(2)
                with fc1:
                    name = st.text_input("Your Name / Establishment", placeholder="e.g., Green Garden Bistro")
                    food = st.text_input("Food Item Description", placeholder="e.g., Chilled vegetarian meal trays")
                with fc2:
                    email = st.text_input("Contact Email", placeholder="e.g., manager@greengarden.com")
                    quantity = st.text_input("Quantity / Portions", value=default_qty, placeholder="e.g., 40 individual boxes")

                notes = st.text_area("Logistics & Temperature Notes", placeholder="e.g., Cooked at 1 PM, kept under refrigeration. Available until 8 PM.")

                st.markdown("#### Quality & Hygiene Check")
                check_temp = st.checkbox("Food has been stored at safe temperatures (cold below 5°C or hot above 60°C).")
                check_package = st.checkbox("Food is sealed in clean, food-grade containers.")

                submit_btn = st.form_submit_button("Validate & Generate Dispatch Links", use_container_width=True)

            if submit_btn:
                if not name or not food or not quantity:
                    st.error("Please complete Name, Food Description, and Quantity.")
                elif not (check_temp and check_package):
                    st.warning("Please verify the Quality & Hygiene conditions before generating a notice.")
                else:
                    qty_num = extract_portion_count(quantity) or (st.session_state.last_portions or 10)
                    
                    # Update Session-based Gamification & Rewards
                    st.session_state.total_rescued_meals += qty_num
                    st.session_state.total_dispatches += 1

                    email_addr = email if email else "donor@plateful.local"
                    email_link = create_email_link(org, name, email_addr, food, quantity, loc_str, notes)
                    whatsapp_link = create_whatsapp_link(org, name, food, quantity, loc_str, notes)

                    impact = compute_impact(qty_num)
                    csv_data = generate_csv_receipt(name, food, quantity, loc_str, org["name"], notes, impact)

                    st.success(f"🎉 Dispatch logged! Added +{qty_num} meals to your lifetime rescue record.")
                    st.balloons()

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.link_button(f"✉️ Email Dispatch ({org.get('contact_email', 'Official')})", email_link, use_container_width=True)
                    with col_b:
                        st.link_button(f"💬 WhatsApp Dispatch ({org.get('whatsapp', 'Hotline')})", whatsapp_link, use_container_width=True)

                    st.download_button(
                        label="📄 Download Official Donation Receipt (CSV)",
                        data=csv_data,
                        file_name=f"plateful_dispatch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("""
<div class="footer-copy">
    Plateful Directory Prototype · Facilitating responsible redistribution of excess resources across 30+ countries.
</div>
""", unsafe_allow_html=True)
