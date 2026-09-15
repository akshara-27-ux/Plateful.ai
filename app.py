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
    # ------------------------------------------------------------
    # INDIA — PAN-INDIA & MULTI-CITY PLATFORMS
    # ------------------------------------------------------------
    {
        "country": "India",
        "state": "Multi-State",
        "supported_states": ["Delhi", "Tamil Nadu", "Karnataka", "Telangana", "Andhra Pradesh"],
        "cities": ["Delhi", "New Delhi", "Chennai", "Bengaluru", "Coimbatore", "Hyderabad", "Tadepalligudem"],
        "neighborhoods": ["Connaught Place", "Dwarka", "Indiranagar", "Koramangala", "T Nagar", "Adyar", "Banjara Hills", "Hitec City", "RS Puram", "Gandhipuram"],
        "name": "No Food Waste",
        "type": "Surplus Food Rescue & Delivery",
        "url": "https://nofoodwaste.org/",
        "contact_email": "info@nofoodwaste.org",
    },
    {
        "country": "India",
        "state": "Multi-State",
        "supported_states": ["Delhi", "Maharashtra", "Karnataka", "Telangana", "Tamil Nadu", "West Bengal", "Gujarat", "Rajasthan", "Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Kerala", "Andhra Pradesh", "Bihar"],
        "cities": ["Delhi", "New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Chandigarh", "Lucknow", "Indore", "Kochi", "Bhopal", "Visakhapatnam", "Nagpur", "Patna", "Ludhiana", "Agra", "Nashik", "Vadodara", "Varanasi"],
        "neighborhoods": ["Bandra", "Andheri", "Juhu", "Hauz Khas", "Saket", "Whitefield", "Jayanagar", "Salt Lake", "Park Street", "Gomti Nagar", "Hazratganj", "C-Scheme", "Malviya Nagar"],
        "name": "Feeding India (by Zomato)",
        "type": "Hunger Relief & Large Redistribution Network",
        "url": "https://www.feedingindia.org/",
        "contact_email": "contact@feedingindia.org",
    },
    {
        "country": "India",
        "state": "Multi-State",
        "supported_states": ["Delhi", "Maharashtra", "Karnataka", "Telangana", "Tamil Nadu", "West Bengal", "Gujarat", "Rajasthan", "Assam", "Odisha", "Uttarakhand", "Punjab", "Jharkhand", "Goa"],
        "cities": ["Delhi", "New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Guwahati", "Bhubaneswar", "Dehradun", "Amritsar", "Ranchi", "Surat", "Goa"],
        "neighborhoods": ["Colaba", "Dadar", "Powai", "Rohini", "Karol Bagh", "HSR Layout", "Indiranagar", "Kothrud", "Viman Nagar", "Panaji", "Margao", "Paltan Bazaar"],
        "name": "Robin Hood Army",
        "type": "Volunteer-Driven Food Rescue",
        "url": "https://robinhoodarmy.com/",
        "contact_email": "info@robinhoodarmy.com",
    },

    # ------------------------------------------------------------
    # INDIA — REGIONAL & STATE-SPECIFIC ORGANIZATIONS
    # ------------------------------------------------------------
    {
        "country": "India",
        "state": "Kerala",
        "supported_states": ["Kerala"],
        "cities": ["Kochi", "Ernakulam", "Thiruvananthapuram", "Kozhikode", "Thrissur"],
        "neighborhoods": ["Kakkanad", "Edappally", "Fort Kochi", "MG Road", "Pattom", "Kazhakoottam", "Technopark", "Mananchira"],
        "name": "Anbodu Kochi & Nanma Maram Community Fridges",
        "type": "Urban Community Fridges & Excess Food Rescue",
        "url": "https://www.facebook.com/AnboduKochi/",
        "contact_email": "anbodukochi@gmail.com",
    },
    {
        "country": "India",
        "state": "Tamil Nadu",
        "supported_states": ["Tamil Nadu"],
        "cities": ["Madurai", "Tiruchirappalli", "Salem", "Tirunelveli"],
        "neighborhoods": ["KK Nagar", "Anna Nagar", "Thillai Nagar", "Cantonment", "Fairlands"],
        "name": "Aram Porul Foundation",
        "type": "Regional Surplus Food Collection",
        "url": "https://aramporul.org/",
        "contact_email": "contact@aramporul.org",
    },
    {
        "country": "India",
        "state": "Karnataka",
        "supported_states": ["Karnataka"],
        "cities": ["Bengaluru", "Mysuru", "Mangaluru"],
        "neighborhoods": ["Malleshwaram", "Basavanagudi", "Electronic City", "Hebbal", "Gokulam", "Jayalakshmipuram", "Hampankatta", "Kadri"],
        "name": "Hasiru Dala Community Feeds",
        "type": "Waste Worker & Surplus Redistribution",
        "url": "https://hasirudala.in/",
        "contact_email": "info@hasirudala.in",
    },
    {
        "country": "India",
        "state": "Maharashtra",
        "supported_states": ["Maharashtra"],
        "cities": ["Mumbai", "Thane", "Navi Mumbai"],
        "neighborhoods": ["Dharavi", "Ghatkopar", "Borivali", "Chembur", "Vashi", "Nerul", "Thane West", "Ghansoli"],
        "name": "Roti Bank by Dabbawalas",
        "type": "Cooked Surplus & Event Food Redistribution",
        "url": "https://rotibankfoundation.org/",
        "contact_email": "info@rotibankfoundation.org",
    },
    {
        "country": "India",
        "state": "Telangana",
        "supported_states": ["Telangana", "Andhra Pradesh"],
        "cities": ["Hyderabad", "Secunderabad", "Warangal"],
        "neighborhoods": ["Madhapur", "Gachibowli", "Kukatpally", "Begumpet", "Jubilee Hills", "Charminar", "Hanamkonda"],
        "name": "Apple Homes (Feed The Needy)",
        "type": "Community Refrigerators & Night Drives",
        "url": "https://feedtheneedy.in/",
        "contact_email": "support@feedtheneedy.in",
    },
    {
        "country": "India",
        "state": "West Bengal",
        "supported_states": ["West Bengal"],
        "cities": ["Kolkata", "Howrah"],
        "neighborhoods": ["Ballygunge", "Gariahat", "New Town", "Shyambazar", "Howrah Station", "Dum Dum"],
        "name": "Sanjhbati Food Bank & Relief",
        "type": "Community Food Pantry & Surplus Rescue",
        "url": "https://sanjhbati.org/",
        "contact_email": "contact@sanjhbati.org",
    },
    {
        "country": "India",
        "state": "Odisha",
        "supported_states": ["Odisha"],
        "cities": ["Bhubaneswar", "Cuttack", "Puri"],
        "neighborhoods": ["Saheed Nagar", "Patia", "Khandagiri", "Badambadi", "CDA Sector", "Grand Road"],
        "name": "Aahwahan Foundation (Odisha Chapter)",
        "type": "Event Surplus Recovery",
        "url": "https://aahwahan.com/",
        "contact_email": "info@aahwahan.com",
    },
    {
        "country": "India",
        "state": "Assam",
        "supported_states": ["Assam", "Meghalaya"],
        "cities": ["Guwahati", "Dispur", "Silchar", "Dibrugarh"],
        "neighborhoods": ["Paltan Bazaar", "GS Road", "Pan Bazaar", "Ganeshguri", "Beltola", "Zoo Road"],
        "name": "Ubanta Foundation",
        "type": "North-East Food Rescue Network",
        "url": "https://ubantafoundation.org/",
        "contact_email": "relief@ubantafoundation.org",
    },
    {
        "country": "India",
        "state": "Punjab",
        "supported_states": ["Punjab", "Haryana", "Chandigarh"],
        "cities": ["Chandigarh", "Mohali", "Panchkula", "Ludhiana", "Amritsar", "Jalandhar"],
        "neighborhoods": ["Sector 17", "Sector 35", "Phase 7 Mohali", "Model Town", "Ranjit Avenue", "Civil Lines"],
        "name": "Voice of Amritsar (Sanjhi Rasoi)",
        "type": "Community Kitchen & Wedding Surplus Recovery",
        "url": "https://voiceofamritsar.org/",
        "contact_email": "voaamritsar@gmail.com",
    },
    {
        "country": "India",
        "state": "Rajasthan",
        "supported_states": ["Rajasthan"],
        "cities": ["Jaipur", "Jodhpur", "Udaipur", "Kota"],
        "neighborhoods": ["Vaishali Nagar", "Mansarovar", "Raja Park", "Sardarpura", "Fateh Sagar", "Talwandi"],
        "name": "Annakshetra Foundation Trust",
        "type": "Surplus Wedding/Event Food Harvesting",
        "url": "https://annakshetra.org/",
        "contact_email": "info@annakshetra.org",
    },
    {
        "country": "India",
        "state": "Gujarat",
        "supported_states": ["Gujarat"],
        "cities": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
        "neighborhoods": ["Navrangpura", "Satellite", "Bodakdev", "SG Highway", "Athwa", "Vesu", "Alkapuri"],
        "name": "Annamrita Foundation Gujarat",
        "type": "Institutional Food Relief & Redistribution",
        "url": "https://annamrita.org/",
        "contact_email": "info.gujarat@annamrita.org",
    },
    {
        "country": "India",
        "state": "Uttar Pradesh",
        "supported_states": ["Uttar Pradesh", "Bihar"],
        "cities": ["Lucknow", "Noida", "Greater Noida", "Ghaziabad", "Kanpur", "Varanasi", "Patna"],
        "neighborhoods": ["Sector 18 Noida", "Sector 62", "Indirapuram", "Raj Nagar", "Swaroop Nagar", "Lanka", "Kankarbagh", "Boring Road"],
        "name": "Roti Bank Hope",
        "type": "Banquet & Household Surplus Rescue",
        "url": "https://rotibankhope.org/",
        "contact_email": "contact@rotibankhope.org",
    },
    {
        "country": "India",
        "state": "Madhya Pradesh",
        "supported_states": ["Madhya Pradesh"],
        "cities": ["Indore", "Bhopal", "Gwalior", "Jabalpur"],
        "neighborhoods": ["Vijay Nagar", "Palasia", "Chhappan Dukan", "MP Nagar", "Arera Colony"],
        "name": "Aahra Food Bank MP",
        "type": "Catering Redistribution Network",
        "url": "https://aahrafoundation.org/",
        "contact_email": "support@aahrafoundation.org",
    },
    {
        "country": "India",
        "state": "Jammu & Kashmir",
        "supported_states": ["Jammu & Kashmir", "Ladakh"],
        "cities": ["Srinagar", "Jammu"],
        "neighborhoods": ["Lal Chowk", "Rajbagh", "Hyderpora", "Gandhi Nagar", "Trikufta Nagar"],
        "name": "Athrout Kashmir Food Relief",
        "type": "Community Food Distribution & Rations",
        "url": "https://athrout.org/",
        "contact_email": "office@athrout.org",
    },

    # ------------------------------------------------------------
    # INTERNATIONAL DIRECTORY
    # ------------------------------------------------------------
    {
        "country": "United States",
        "state": "New York",
        "supported_states": ["New York"],
        "cities": ["New York", "New York City", "Brooklyn", "Queens", "Bronx"],
        "neighborhoods": [],
        "name": "City Harvest",
        "type": "Metro Food Rescue & Distribution",
        "url": "https://www.cityharvest.org/",
        "contact_email": "foodrescue@cityharvest.org",
    },
    {
        "country": "United States",
        "state": "Multi-State",
        "supported_states": ["California", "Illinois", "Massachusetts", "Washington", "Connecticut", "Michigan", "Florida"],
        "cities": ["New York", "Los Angeles", "Chicago", "Boston", "Seattle", "San Francisco", "Washington", "New Haven", "Detroit", "Miami"],
        "neighborhoods": [],
        "name": "Food Rescue US",
        "type": "App-Based Hyper-Local Food Transfer",
        "url": "https://foodrescue.us/",
        "contact_email": "info@foodrescue.us",
    },
    {
        "country": "Canada",
        "state": "Multi-Province",
        "supported_states": ["Ontario", "British Columbia", "Quebec", "Alberta", "Manitoba"],
        "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Winnipeg"],
        "neighborhoods": [],
        "name": "Second Harvest Canada",
        "type": "National Food Rescue Logistics",
        "url": "https://www.secondharvest.ca/",
        "contact_email": "support@secondharvest.ca",
    },
    {
        "country": "United Kingdom",
        "state": "UK",
        "supported_states": ["England", "Scotland", "Wales"],
        "cities": ["London", "Manchester", "Birmingham", "Liverpool", "Bristol", "Leeds", "Glasgow", "Edinburgh", "Cardiff"],
        "neighborhoods": [],
        "name": "FareShare UK",
        "type": "Charity Food Redistribution Network",
        "url": "https://fareshare.org.uk/",
        "contact_email": "enquiries@fareshare.org.uk",
    },
    {
        "country": "Australia",
        "state": "Multi-State",
        "supported_states": ["New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia", "ACT"],
        "cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra", "Gold Coast", "Newcastle"],
        "neighborhoods": [],
        "name": "OzHarvest",
        "type": "Perishable Food Rescue Fleet",
        "url": "https://www.ozharvest.org/",
        "contact_email": "info@ozharvest.org",
    },
    {
        "country": "New Zealand",
        "state": "Wellington Region",
        "supported_states": ["Wellington"],
        "cities": ["Wellington", "Lower Hutt", "Porirua", "Kapiti"],
        "neighborhoods": [],
        "name": "Kaibosh Food Rescue",
        "type": "Regional Food Rescue",
        "url": "https://www.kaibosh.org.nz/",
        "contact_email": "info@kaibosh.org.nz",
    },
    {
        "country": "Singapore",
        "state": "Singapore",
        "supported_states": ["Singapore"],
        "cities": ["Singapore"],
        "neighborhoods": [],
        "name": "The Food Bank Singapore",
        "type": "Food Bank & Redistribution Depots",
        "url": "https://foodbank.sg/",
        "contact_email": "enquiries@foodbank.sg",
    },
    {
        "country": "South Africa",
        "state": "Multi-Province",
        "supported_states": ["Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape"],
        "cities": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Gqeberha", "Port Elizabeth"],
        "neighborhoods": [],
        "name": "FoodForward SA",
        "type": "Recovery & Redistribution Infrastructure",
        "url": "https://foodforwardsa.org/",
        "contact_email": "info@foodforwardsa.org",
    },
    {
        "country": "Kenya",
        "state": "Multi-County",
        "supported_states": ["Nairobi County", "Mombasa County", "Kisumu County"],
        "cities": ["Nairobi", "Mombasa", "Kisumu"],
        "neighborhoods": [],
        "name": "Food Banking Kenya",
        "type": "Regional Hub & Farm Recovery",
        "url": "https://foodbankingkenya.org/",
        "contact_email": "info@foodbankingkenya.org",
    },
    {
        "country": "Nigeria",
        "state": "Multi-State",
        "supported_states": ["Lagos", "FCT", "Oyo"],
        "cities": ["Lagos", "Abuja", "Ibadan"],
        "neighborhoods": [],
        "name": "Lagos Food Bank Initiative",
        "type": "Hunger Relief & Malnutrition Programs",
        "url": "https://lagosfoodbank.org/",
        "contact_email": "contactus@lagosfoodbank.org",
    },
    {
        "country": "Indonesia",
        "state": "Multi-Province",
        "supported_states": ["Bali", "DKI Jakarta"],
        "cities": ["Bali", "Denpasar", "Jakarta"],
        "neighborhoods": [],
        "name": "Scholars of Sustenance (SOS) Indonesia",
        "type": "Cooked Surplus Recovery & Relief",
        "url": "https://www.scholarsofsustenance.org/sos-indonesia",
        "contact_email": "indonesia@scholarsofsustenance.org",
    },
    {
        "country": "Indonesia",
        "state": "Java",
        "supported_states": ["West Java", "East Java", "DKI Jakarta"],
        "cities": ["Jakarta", "Bandung", "Surabaya"],
        "neighborhoods": [],
        "name": "FoodCycle Indonesia",
        "type": "Surplus Redistribution & Food Waste Prevention",
        "url": "https://foodcycle.id/",
        "contact_email": "info@foodcycle.id",
    },
    {
        "country": "Malaysia",
        "state": "Klang Valley & Penang",
        "supported_states": ["Selangor", "Penang", "Kuala Lumpur"],
        "cities": ["Kuala Lumpur", "Petaling Jaya", "Shah Alam", "George Town"],
        "neighborhoods": [],
        "name": "The Lost Food Project",
        "type": "Surplus Rescue & Distribution",
        "url": "https://www.thelostfoodproject.org/",
        "contact_email": "info@thelostfoodproject.org",
    },
    {
        "country": "Brazil",
        "state": "Multi-State",
        "supported_states": ["São Paulo", "Rio de Janeiro", "Distrito Federal", "Bahia", "Minas Gerais"],
        "cities": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Belo Horizonte"],
        "neighborhoods": [],
        "name": "Mesa Brasil SESC",
        "type": "National Network of Food Banks",
        "url": "https://www.sesc.com.br/atuacoes/assistencia/mesa-brasil/",
        "contact_email": "mesabrasil@sesc.com.br",
    },
    {
        "country": "Mexico",
        "state": "Multi-State",
        "supported_states": ["CDMX", "Jalisco", "Nuevo León", "Puebla", "Baja California", "Querétaro"],
        "cities": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "Querétaro"],
        "neighborhoods": [],
        "name": "BAMX (Red de Bancos de Alimentos de México)",
        "type": "National Food Bank Federation",
        "url": "https://bamx.org.mx/",
        "contact_email": "contacto@bamx.org.mx",
    },
    {
        "country": "Spain",
        "state": "Multi-Region",
        "supported_states": ["Madrid", "Catalonia", "Andalusia", "Basque Country", "Valencia"],
        "cities": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao", "Málaga"],
        "neighborhoods": [],
        "name": "FESBAL (Federación Española de Bancos de Alimentos)",
        "type": "National Federation of Regional Food Banks",
        "url": "https://www.fesbal.org/",
        "contact_email": "comunicacion@fesbal.org",
    },
    {
        "country": "Germany",
        "state": "Multi-State",
        "supported_states": ["Berlin", "Hamburg", "Bavaria", "Hesse", "North Rhine-Westphalia", "Baden-Württemberg"],
        "cities": ["Berlin", "Hamburg", "Munich", "Frankfurt", "Cologne", "Stuttgart"],
        "neighborhoods": [],
        "name": "Tafel Deutschland e.V.",
        "type": "Food Distribution Stations & Volunteer Hubs",
        "url": "https://www.tafel.de/",
        "contact_email": "info@tafel.de",
    },
    {
        "country": "France",
        "state": "Multi-Region",
        "supported_states": ["Île-de-France", "Auvergne-Rhône-Alpes", "Provence-Alpes-Côte d'Azur", "Occitanie", "Nouvelle-Aquitaine", "Hauts-de-France"],
        "cities": ["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux", "Lille"],
        "neighborhoods": [],
        "name": "Fédération Française des Banques Alimentaires",
        "type": "Surplus Recovery & Food Security Network",
        "url": "https://www.banquealimentaire.org/",
        "contact_email": "ffba@banquealimentaire.org",
    },
    {
        "country": "Ireland",
        "state": "Republic of Ireland",
        "supported_states": ["Leinster", "Munster", "Connacht"],
        "cities": ["Dublin", "Cork", "Galway", "Limerick", "Waterford"],
        "neighborhoods": [],
        "name": "FoodCloud",
        "type": "Digital Technology & Logistics Platform",
        "url": "https://food.cloud/",
        "contact_email": "info@food.cloud",
    },
]

# ------------------------------------------------------------
# INDIAN STATES & UNION TERRITORIES ALIASES
# ------------------------------------------------------------
STATE_ALIASES = {
    "andhra pradesh": "Andhra Pradesh",
    "andhra": "Andhra Pradesh",
    "ap": "Andhra Pradesh",
    "arunachal pradesh": "Arunachal Pradesh",
    "arunachal": "Arunachal Pradesh",
    "assam": "Assam",
    "asom": "Assam",
    "bihar": "Bihar",
    "chhattisgarh": "Chhattisgarh",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal pradesh": "Himachal Pradesh",
    "himachal": "Himachal Pradesh",
    "hp": "Himachal Pradesh",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kar": "Karnataka",
    "kerala": "Kerala",
    "madhya pradesh": "Madhya Pradesh",
    "mp": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "maha": "Maharashtra",
    "mh": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "orissa": "Odisha",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "raj": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu",
    "tamilnadu": "Tamil Nadu",
    "tn": "Tamil Nadu",
    "telangana": "Telangana",
    "tg": "Telangana",
    "ts": "Telangana",
    "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh",
    "up": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand",
    "uttaranchal": "Uttarakhand",
    "west bengal": "West Bengal",
    "bengal": "West Bengal",
    "wb": "West Bengal",
    "jammu and kashmir": "Jammu & Kashmir",
    "jammu & kashmir": "Jammu & Kashmir",
    "j&k": "Jammu & Kashmir",
    "ladakh": "Ladakh",
    "delhi ncr": "Delhi",
    "delhi": "Delhi",
    "chandigarh": "Chandigarh",
    "puducherry": "Puducherry",
    "pondicherry": "Puducherry",
}

CITY_ALIASES = {
    # NCR & Delhi Neighborhoods
    "new delhi": "Delhi",
    "delhi": "Delhi",
    "ncr": "Delhi",
    "gurgaon": "Delhi",
    "gurugram": "Delhi",
    "noida": "Noida",
    "ghaziabad": "Ghaziabad",
    "faridabad": "Delhi",
    "connaught place": "Delhi",
    "cp": "Delhi",
    "hauz khas": "Delhi",
    "dwarka": "Delhi",
    "rohini": "Delhi",
    "saket": "Delhi",
    "karol bagh": "Delhi",

    # Mumbai & MMR Neighborhoods
    "bombay": "Mumbai",
    "mumbai": "Mumbai",
    "bandra": "Mumbai",
    "andheri": "Mumbai",
    "juhu": "Mumbai",
    "colaba": "Mumbai",
    "dadar": "Mumbai",
    "powai": "Mumbai",
    "ghatkopar": "Mumbai",
    "borivali": "Mumbai",
    "vashi": "Navi Mumbai",
    "nerul": "Navi Mumbai",
    "navi mumbai": "Navi Mumbai",
    "thane": "Thane",

    # Bengaluru Neighborhoods
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "koramangala": "Bengaluru",
    "indiranagar": "Bengaluru",
    "whitefield": "Bengaluru",
    "hsr": "Bengaluru",
    "hsr layout": "Bengaluru",
    "jayanagar": "Bengaluru",
    "electronic city": "Bengaluru",
    "malleshwaram": "Bengaluru",

    # Chennai Neighborhoods
    "madras": "Chennai",
    "chennai": "Chennai",
    "t nagar": "Chennai",
    "adyar": "Chennai",
    "velachery": "Chennai",
    "anna nagar": "Chennai",

    # Hyderabad Neighborhoods
    "hyderabad": "Hyderabad",
    "secunderabad": "Hyderabad",
    "gachibowli": "Hyderabad",
    "hitec city": "Hyderabad",
    "madhapur": "Hyderabad",
    "banjara hills": "Hyderabad",
    "jubilee hills": "Hyderabad",

    # Kolkata Neighborhoods
    "calcutta": "Kolkata",
    "kolkata": "Kolkata",
    "salt lake": "Kolkata",
    "new town": "Kolkata",
    "park street": "Kolkata",
    "ballygunge": "Kolkata",

    # Kerala Neighborhoods
    "cochin": "Kochi",
    "kochi": "Kochi",
    "ernakulam": "Kochi",
    "kakkanad": "Kochi",
    "trivandrum": "Thiruvananthapuram",
    "thiruvananthapuram": "Thiruvananthapuram",
    "calicut": "Kozhikode",

    # International Aliases
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

def detect_location(text):
    """
    Scans input for:
    1. Indian States & State Abbreviations
    2. City & Neighborhood aliases
    3. Explicit cities/neighborhoods inside ORGS
    4. Fallback preposition patterns (in, around, near, from)
    Returns: (canonical_city, detected_neighborhood, detected_state)
    """
    t = clean(text)

    # 1. State Detection
    detected_state = None
    for alias_s, canonical_s in sorted(STATE_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if re.search(r"(?<!\w)" + re.escape(alias_s) + r"(?!\w)", t):
            detected_state = canonical_s
            break

    # 2. Neighborhood & City Alias Check
    for alias_k, canonical_v in sorted(CITY_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if re.search(r"(?<!\w)" + re.escape(alias_k) + r"(?!\w)", t):
            return canonical_v, alias_k.title(), detected_state

    # 3. Explicit Neighborhoods and Cities in ORGS
    for org in ORGS:
        for hood in org.get("neighborhoods", []):
            if re.search(r"(?<!\w)" + re.escape(hood.lower()) + r"(?!\w)", t):
                return org["cities"][0], hood, detected_state or org.get("state")

        for city in org.get("cities", []):
            if re.search(r"(?<!\w)" + re.escape(city.lower()) + r"(?!\w)", t):
                return canonical_city(city), None, detected_state or org.get("state")

    # 4. Fallback Preposition Search
    patterns = [
        r"\bin\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\bfrom\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\baround\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\bnear\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\bat\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
    ]
    stop_words = {"a", "an", "the", "and", "with", "where", "what", "how", "please", "state", "india"}
    for pattern in patterns:
        match = re.search(pattern, t)
        if match:
            candidate = match.group(1).strip(" .,!?:;")
            candidate = candidate.split(" and ")[0].strip()
            candidate = candidate.split(" where ")[0].strip()
            cand_clean = clean(candidate)
            if cand_clean in STATE_ALIASES:
                return None, None, STATE_ALIASES[cand_clean]
            if candidate and candidate.split()[0] not in stop_words:
                resolved = canonical_city(candidate)
                return resolved, None, detected_state

    return None, None, detected_state

def detect_intent(text):
    t = clean(text)
    location_words = [
        "where", "find", "near", "ngo", "charity", "food bank", "foodbank",
        "organization", "organisation", "centre", "center", "donate",
        "donation", "give", "collect", "pickup", "pick up", "redistribute",
        "redistribution", "food rescue", "who can take", "state"
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

def find_orgs(city=None, neighborhood=None, state=None):
    if not city and not neighborhood and not state:
        return []

    canonical = canonical_city(city) if city else None
    matched_results = []

    for org in ORGS:
        city_match = False
        hood_match = False
        state_match = False

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

    # Prioritize: Direct Neighborhood > Direct City > State-wide coverage
    return sorted(
        matched_results,
        key=lambda x: (x.get("is_hyperlocal", False), x.get("is_city_match", False), x.get("is_state_match", False)),
        reverse=True
    )

def create_email_link(org, name, email, food, quantity, location_str, notes):
    subject = f"Surplus Food Donation Enquiry — {location_str}"
    body = f"""Hello {org['name']} Team,

I have surplus food available for redistribution in {location_str} and would like to coordinate a drop-off or collection if suitable.

Donor Details:
• Contact Person: {name}
• Email: {email}
• Food Description: {food}
• Quantity / Servings: {quantity}
• Pickup Location: {location_str}
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
    "last_neighborhood": None,
    "last_state": None,
    "display_location": None,
    "request_recorded": False,
    "selected_org": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ------------------------------------------------------------
# DARK THEME EDITORIAL STYLING
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
    --accent-sand: #30363D;
    --accent-orange: #F0883E;
    --border-light: #30363D;
}

.stApp {
    background-color: var(--bg) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}

h1, h2, h3, h4 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #FFFFFF !important;
    letter-spacing: -0.02em;
}

p, span, label, div {
    color: var(--text-primary);
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
    color: #56D364;
    letter-spacing: -0.03em;
}

.tag-badge {
    background: #1F3B2C;
    color: #7EE787;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 6px 14px;
    border-radius: 999px;
    text-transform: uppercase;
    border: 1px solid #2EA043;
}

.hero-box {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
}

.hero-headline {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    line-height: 1.15;
    font-weight: 700;
    color: #FFFFFF;
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
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    height: 100%;
}

.step-index {
    color: var(--accent-orange);
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
}

.step-heading {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0.4rem 0;
    color: #FFFFFF;
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
    color: var(--accent-orange);
    margin-bottom: 0.6rem;
}

.pill-meta {
    display: inline-block;
    background: var(--surface-elevated);
    color: #E6EDF3;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 6px;
    border: 1px solid var(--border-light);
    margin-right: 6px;
    margin-bottom: 8px;
}

.pill-local {
    display: inline-block;
    background: #1F3B2C;
    color: #7EE787;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 6px;
    border: 1px solid #2EA043;
    margin-right: 6px;
    margin-bottom: 8px;
}

.pill-state {
    display: inline-block;
    background: #2E1F3B;
    color: #D2A8FF;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 6px;
    border: 1px solid #8957E5;
    margin-right: 6px;
    margin-bottom: 8px;
}

.callout-banner {
    background: #251B12;
    border: 1px solid #4D3319;
    border-left: 4px solid var(--accent-orange);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-size: 0.9rem;
    line-height: 1.5;
    color: #FFD29D;
    margin: 1.5rem 0;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--surface) !important;
    border-color: var(--border-light) !important;
}

.stButton > button {
    background-color: var(--brand-green) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.15s ease-in-out !important;
}

.stButton > button:hover {
    background-color: var(--brand-green-hover) !important;
    box-shadow: 0 4px 12px rgba(35, 134, 54, 0.4) !important;
}

.stLinkButton > a {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    background-color: var(--surface-elevated) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--border-light) !important;
}

.stLinkButton > a:hover {
    background-color: #2D333B !important;
    border-color: #8B949E !important;
}

[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem !important;
}

div[data-baseweb="input"], div[data-baseweb="textarea"] {
    background-color: var(--surface-elevated) !important;
    border-color: var(--border-light) !important;
}

input, textarea {
    color: #FFFFFF !important;
    background-color: transparent !important;
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
        Plateful helps you route excess edible food to established community kitchens and redistribution non-profits across India and beyond.
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
        <p class="step-desc">Share where you are located by state, city, or street, plus portion counts.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-index">STEP 02</div>
        <div class="step-heading">Find Local Nodes</div>
        <p class="step-desc">Identify verified partners operating at regional, state, or neighborhood levels.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-index">STEP 03</div>
        <div class="step-heading">Hand-off Details</div>
        <p class="step-desc">Generate standardized notification emails to confirm logistics, timings, and hygiene standards.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# CONVERSATIONAL ASSISTANT INTERFACE
# ------------------------------------------------------------
st.markdown("<div class=\"section-tag\">Directory Assistant</div>", unsafe_allow_html=True)
st.markdown("### How can we help you redistribute today?")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("E.g., 'Food rescue in Kerala', 'Extra food in Indiranagar, Bangalore', or 'Donations in UP'")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    intent = detect_intent(user_input)
    city, neighborhood, state = detect_location(user_input)

    # Compile a clear location label for search results
    location_parts = []
    if neighborhood:
        location_parts.append(neighborhood)
    if city and (not neighborhood or city.lower() != neighborhood.lower()):
        location_parts.append(city)
    if state and state not in location_parts:
        location_parts.append(state)

    display_loc = ", ".join(location_parts) if location_parts else None

    if display_loc:
        orgs = find_orgs(city=city, neighborhood=neighborhood, state=state)
        if orgs:
            reply = (
                f"We identified **{len(orgs)} verified redistribution partner(s)** active in **{display_loc}**.\n\n"
                "Browse the matches below to view coverage details or prepare a pre-filled donation notification."
            )
        else:
            reply = (
                f"We currently do not have a pre-indexed partner active in **{display_loc}**. "
                "For unlisted states or cities, local municipal disaster relief centers or temple/gurdwara langar networks often accept bulk safe donations."
            )
    elif intent == "greeting":
        reply = (
            "Hello! I am ready to help coordinate your food donation. "
            "Tell me **your state, city, or neighborhood** (e.g., *'Kerala'*, *'Delhi'*, *'Indiranagar'*), and what you have to donate."
        )
        orgs = []
    elif intent == "surplus":
        reply = (
            "We can definitely connect your surplus to community kitchens. "
            "**Which state, city, or neighborhood are you located in?**"
        )
        orgs = []
    else:
        reply = (
            "I can assist with locating food rescue organizations.\n\n"
            "Try specifying your state or neighborhood:\n"
            "- *“Who collects food donations in Kerala?”*\n"
            "- *“We have 30 lunch boxes left over in Bandra, Mumbai.”*\n"
            "- *“Surplus food rescue in Uttar Pradesh.”*"
        )
        orgs = []

    st.session_state.last_city = city
    st.session_state.last_neighborhood = neighborhood
    st.session_state.last_state = state
    st.session_state.display_location = display_loc
    st.session_state.last_results = orgs
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ------------------------------------------------------------
# MATCHED ORGANISATIONS SECTION
# ------------------------------------------------------------
if st.session_state.last_results:
    display_title = st.session_state.display_location or "Your Location"
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class=\"section-tag\">Results for {display_title}</div>", unsafe_allow_html=True)

    for index, org in enumerate(st.session_state.last_results):
        with st.container(border=True):
            head_col, action_col = st.columns([2.5, 1.5])

            with head_col:
                st.markdown(f"#### {org['name']}")

                tags_html = f"<span class='pill-meta'>{org['country']}</span>"
                if org.get("state") and org["state"] != "Multi-State":
                    tags_html += f"<span class='pill-state'>{org['state']}</span>"
                elif org.get("state") == "Multi-State":
                    tags_html += "<span class='pill-state'>Pan-India / Multi-State</span>"

                tags_html += f"<span class='pill-meta'>{org['type']}</span>"

                if org.get("is_hyperlocal"):
                    tags_html += "<span class='pill-local'>Direct Neighborhood Match</span>"

                st.markdown(tags_html, unsafe_allow_html=True)

                if org.get("neighborhoods"):
                    hoods_display = ", ".join(org["neighborhoods"][:5])
                    st.caption(f"📍 Notable Local Hubs: {hoods_display}")
                else:
                    coverage_str = ", ".join(org['cities'][:6]) + ("..." if len(org['cities']) > 6 else "")
                    st.caption(f"Key Hubs: {coverage_str}")

                if org.get("supported_states"):
                    states_display = ", ".join(org["supported_states"][:6]) + ("..." if len(org["supported_states"]) > 6 else "")
                    st.caption(f"🗺️ State Coverage: {states_display}")

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
        <strong>Important Safety Reminder:</strong> Food safety guidelines require strict hot or cold chain maintenance.
        Always verify whether the receiving agency accepts prepared meals, unpackaged items, or requires specific container types before dispatching.
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# DRAFT ENQUIRY WORKFLOW
# ------------------------------------------------------------
if st.session_state.request_recorded and st.session_state.last_results:
    selected_idx = st.session_state.selected_org
    if selected_idx < len(st.session_state.last_results):
        org = st.session_state.last_results[selected_idx]
        loc_str = st.session_state.display_location or "your locality"

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class=\"section-tag\">Prepare Communication</div>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"### Donation Notification for {org['name']}")
            st.markdown(f"Generate a standardized notification for operations in **{loc_str}**.")

            with st.form("donation_request_form"):
                fc1, fc2 = st.columns(2)
                with fc1:
                    name = st.text_input("Your Name / Establishment", placeholder="e.g., Green Garden Bistro")
                    food = st.text_input("Food Item Description", placeholder="e.g., Chilled vegetarian meal boxes (freshly packed)")
                with fc2:
                    email = st.text_input("Contact Email", placeholder="e.g., manager@greengarden.com")
                    quantity = st.text_input("Quantity / Portions", placeholder="e.g., 50 meal packets")

                notes = st.text_area(
                    "Logistics & Condition Notes",
                    placeholder="e.g., Prepared at 1 PM, refrigerated at 3 PM. Packed in disposable foil trays. Available for pickup till 8 PM."
                )

                submit_btn = st.form_submit_button("Generate Direct Email Link", use_container_width=True)

            if submit_btn:
                if not name or not email or not food or not quantity:
                    st.error("Please fill in all mandatory fields (Name, Email, Food, and Quantity).")
                else:
                    email_link = create_email_link(org, name, email, food, quantity, loc_str, notes)
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
