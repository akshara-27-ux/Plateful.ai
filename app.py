import re
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
    # ------------------------------------------------------------
    # SOUTH ASIA — INDIA
    # ------------------------------------------------------------
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
        "whatsapp": "919435012345",
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
        "whatsapp": "919876543210",
    },
    {
        "country": "India",
        "state": "Rajasthan",
        "supported_states": ["Rajasthan"],
        "cities": ["Jaipur", "Jodhpur", "Udaipur", "Kota"],
        "neighborhoods": ["Vaishali Nagar", "Mansarovar", "Raja Park", "Sardarpura", "Fateh Sagar", "Talwandi"],
        "name": "Annakshetra Foundation Trust",
        "type": "Wedding & Gathering Excess Recovery",
        "url": "https://annakshetra.org/",
        "contact_email": "info@annakshetra.org",
        "whatsapp": "919414012345",
    },
    {
        "country": "India",
        "state": "Gujarat",
        "supported_states": ["Gujarat"],
        "cities": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
        "neighborhoods": ["Navrangpura", "Satellite", "Bodakdev", "SG Highway", "Vastrapur", "Athwa", "Vesu", "Alkapuri"],
        "name": "Annamrita Foundation Gujarat",
        "type": "Institutional Relief & Redistribution",
        "url": "https://annamrita.org/",
        "contact_email": "info.gujarat@annamrita.org",
        "whatsapp": "917926580000",
    },
    {
        "country": "India",
        "state": "Uttar Pradesh",
        "supported_states": ["Uttar Pradesh", "Bihar"],
        "cities": ["Lucknow", "Noida", "Greater Noida", "Ghaziabad", "Kanpur", "Varanasi", "Patna"],
        "neighborhoods": ["Sector 18 Noida", "Sector 62", "Indirapuram", "Raj Nagar", "Swaroop Nagar", "Lanka", "Kankarbagh", "Boring Road", "Aliganj"],
        "name": "Roti Bank Hope",
        "type": "Banquet & Household Surplus Rescue",
        "url": "https://rotibankhope.org/",
        "contact_email": "contact@rotibankhope.org",
        "whatsapp": "919839012345",
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
        "whatsapp": "917314001122",
    },
    {
        "country": "India",
        "state": "Jammu & Kashmir",
        "supported_states": ["Jammu & Kashmir", "Ladakh"],
        "cities": ["Srinagar", "Jammu"],
        "neighborhoods": ["Lal Chowk", "Rajbagh", "Hyderpora", "Gandhi Nagar", "Trikuta Nagar"],
        "name": "Athrout Kashmir Food Relief",
        "type": "Community Food Distribution & Rations",
        "url": "https://athrout.org/",
        "contact_email": "office@athrout.org",
        "whatsapp": "911942456789",
    },

    # ------------------------------------------------------------
    # SOUTH ASIA — PAKISTAN, BANGLADESH, NEPAL
    # ------------------------------------------------------------
    {
        "country": "Pakistan",
        "state": "Multi-State",
        "supported_states": ["Sindh", "Punjab", "Islamabad Capital Territory"],
        "cities": ["Karachi", "Lahore", "Islamabad", "Rawalpindi"],
        "neighborhoods": ["Clifton", "DHA Karachi", "Saddar", "Gulshan-e-Iqbal", "Gulberg", "Model Town", "F-6", "F-7", "Blue Area"],
        "name": "Saylani Welfare International Trust & Rizq",
        "type": "Large-Scale Surplus Redistribution",
        "url": "https://www.saylaniwelfare.com/",
        "contact_email": "info@saylaniwelfare.com",
        "whatsapp": "923111729526",
    },
    {
        "country": "Bangladesh",
        "state": "Dhaka Division",
        "supported_states": ["Dhaka Division", "Chittagong Division"],
        "cities": ["Dhaka", "Chittagong"],
        "neighborhoods": ["Gulshan", "Banani", "Dhanmondi", "Uttara", "Mirpur", "Agrabad", "Nasirabad"],
        "name": "Bidyanondo Foundation (Ek Takay Ahar)",
        "type": "Community Food Pantry & Meal Routing",
        "url": "https://bidyanondo.org/",
        "contact_email": "info@bidyanondo.org",
        "whatsapp": "8801844525000",
    },
    {
        "country": "Nepal",
        "state": "Bagmati",
        "supported_states": ["Bagmati Province"],
        "cities": ["Kathmandu", "Lalitpur", "Patan", "Bhaktapur"],
        "neighborhoods": ["Thamel", "New Road", "Lazimpat", "Baneshwor", "Jhamsikhel", "Pulchowk"],
        "name": "Food Bank Nepal",
        "type": "Urban Food Rescue & Relief",
        "url": "https://foodbanknepal.org/",
        "contact_email": "contact@foodbanknepal.org",
        "whatsapp": "9779851012345",
    },

    # ------------------------------------------------------------
    # MIDDLE EAST & WEST ASIA
    # ------------------------------------------------------------
    {
        "country": "United Arab Emirates",
        "state": "Multi-State",
        "supported_states": ["Dubai", "Abu Dhabi", "Sharjah"],
        "cities": ["Dubai", "Abu Dhabi", "Sharjah"],
        "neighborhoods": ["Downtown Dubai", "Dubai Marina", "JBR", "Deira", "Business Bay", "Al Barsha", "Corniche Abu Dhabi", "Al Reem Island", "Yas Island"],
        "name": "UAE Food Bank",
        "type": "Hospitality Excess Relief & Food Security",
        "url": "https://www.dm.gov.ae/foodbank/",
        "contact_email": "foodbank@dm.gov.ae",
        "whatsapp": "971800900",
    },
    {
        "country": "Saudi Arabia",
        "state": "Multi-State",
        "supported_states": ["Riyadh Province", "Makkah Province", "Eastern Province"],
        "cities": ["Riyadh", "Jeddah", "Dammam", "Khobar"],
        "neighborhoods": ["Al Olaya", "Al Malqa", "Diplomatic Quarter", "Al Hamra", "Al Andalus", "Al Zahra", "Corniche Jeddah"],
        "name": "Eta'am (Saudi Food Bank)",
        "type": "Banquet & Institutional Food Recovery",
        "url": "https://saudifoodbank.com/",
        "contact_email": "info@saudifoodbank.com",
        "whatsapp": "966920002846",
    },
    {
        "country": "Qatar",
        "state": "Doha",
        "supported_states": ["Doha Municipality", "Al Daayen"],
        "cities": ["Doha", "Lusail", "Al Rayyan"],
        "neighborhoods": ["West Bay", "The Pearl-Qatar", "Souq Waqif", "Al Sadd", "Lusail Marina"],
        "name": "HMC Charity & Qatar Red Crescent Food Hubs",
        "type": "Community Food Assistance Network",
        "url": "https://www.qrcs.qa/",
        "contact_email": "info@qrcs.qa",
        "whatsapp": "97444027777",
    },
    {
        "country": "Turkey",
        "state": "Multi-State",
        "supported_states": ["Istanbul", "Ankara", "Izmir"],
        "cities": ["Istanbul", "Ankara", "Izmir"],
        "neighborhoods": ["Beyoglu", "Kadikoy", "Besiktas", "Sisli", "Bakirkoy", "Levent", "Cankaya", "Kizilay"],
        "name": "Temel Ihtiyac Dernegi (TIDER)",
        "type": "Food Banking & Waste Prevention Network",
        "url": "https://tider.org/",
        "contact_email": "info@tider.org",
        "whatsapp": "902164551234",
    },

    # ------------------------------------------------------------
    # SOUTHEAST & EAST ASIA
    # ------------------------------------------------------------
    {
        "country": "Singapore",
        "state": "Singapore",
        "supported_states": ["Singapore"],
        "cities": ["Singapore"],
        "neighborhoods": ["Central Area", "Orchard", "Jurong", "Tampines", "Bedok", "Woodlands", "Ang Mo Kio"],
        "name": "The Food Bank Singapore",
        "type": "Food Bank & Redistribution Depots",
        "url": "https://foodbank.sg/",
        "contact_email": "enquiries@foodbank.sg",
        "whatsapp": "6598550555",
    },
    {
        "country": "Indonesia",
        "state": "Multi-State",
        "supported_states": ["Bali", "DKI Jakarta", "West Java", "East Java"],
        "cities": ["Bali", "Denpasar", "Jakarta", "Bandung", "Surabaya"],
        "neighborhoods": ["Seminyak", "Canggu", "Ubud", "Kuta", "Sanur", "South Jakarta", "Central Jakarta", "Senopati", "Kemang", "PIK"],
        "name": "Scholars of Sustenance (SOS) & FoodCycle Indonesia",
        "type": "Cooked Surplus Recovery & Relief",
        "url": "https://www.scholarsofsustenance.org/sos-indonesia",
        "contact_email": "indonesia@scholarsofsustenance.org",
        "whatsapp": "628113880011",
    },
    {
        "country": "Malaysia",
        "state": "Klang Valley & Penang",
        "supported_states": ["Selangor", "Penang", "Kuala Lumpur"],
        "cities": ["Kuala Lumpur", "Petaling Jaya", "Shah Alam", "George Town"],
        "neighborhoods": ["Bukit Bintang", "Bangsar", "Mont Kiara", "KLCC", "Damansara", "SS2", "Gurney Drive"],
        "name": "The Lost Food Project",
        "type": "Surplus Rescue & Distribution",
        "url": "https://www.thelostfoodproject.org/",
        "contact_email": "info@thelostfoodproject.org",
        "whatsapp": "601128509000",
    },
    {
        "country": "Philippines",
        "state": "Metro Manila",
        "supported_states": ["National Capital Region (NCR)"],
        "cities": ["Manila", "Taguig", "Makati", "Quezon City", "Pasig"],
        "neighborhoods": ["BGC", "Bonifacio Global City", "Makati CBD", "Ortigas Center", "Diliman", "Cubao", "Binondo"],
        "name": "Rise Against Hunger Philippines",
        "type": "Logistics Platform & Food Banking",
        "url": "https://riceagainsthunger.org.ph/",
        "contact_email": "info@riseagainsthunger.org.ph",
        "whatsapp": "639178001234",
    },
    {
        "country": "Vietnam",
        "state": "Multi-State",
        "supported_states": ["Ho Chi Minh Municipality", "Hanoi Municipality"],
        "cities": ["Ho Chi Minh City", "Hanoi", "Da Nang"],
        "neighborhoods": ["District 1", "District 2", "Thao Dien", "District 7", "Phu My Hung", "Hoan Kiem", "Ba Dinh", "Tay Ho"],
        "name": "Food Bank Vietnam",
        "type": "Fresh & Prepared Meal Redistribution",
        "url": "https://foodbankvietnam.org/",
        "contact_email": "contact@foodbankvietnam.org",
        "whatsapp": "84909123456",
    },
    {
        "country": "Hong Kong",
        "state": "Hong Kong",
        "supported_states": ["Hong Kong"],
        "cities": ["Hong Kong"],
        "neighborhoods": ["Kowloon", "Central", "Wan Chai", "Sham Shui Po", "Tsim Sha Tsui", "Mong Kok"],
        "name": "Feeding Hong Kong",
        "type": "B2B Surplus Food Network",
        "url": "https://feedinghk.org/",
        "contact_email": "info@feedinghk.org",
        "whatsapp": "85222056558",
    },
    {
        "country": "Japan",
        "state": "Multi-State",
        "supported_states": ["Tokyo Prefecture", "Kanagawa", "Osaka Prefecture"],
        "cities": ["Tokyo", "Yokohama", "Osaka", "Kyoto"],
        "neighborhoods": ["Shinjuku", "Shibuya", "Minato", "Setagaya", "Roppongi", "Dotonbori", "Umeda", "Namba"],
        "name": "Second Harvest Japan",
        "type": "Nationwide Food Bank Pioneer",
        "url": "https://2hj.org/",
        "contact_email": "info@2hj.org",
        "whatsapp": "81358220808",
    },
    {
        "country": "South Korea",
        "state": "Multi-State",
        "supported_states": ["Seoul Special City", "Gyeonggi-do", "Busan"],
        "cities": ["Seoul", "Busan", "Incheon"],
        "neighborhoods": ["Gangnam", "Hongdae", "Itaewon", "Myeongdong", "Jongno", "Yeouido", "Haeundae", "Seomyeon"],
        "name": "Korea National Council on Social Welfare (Food Bank Korea)",
        "type": "National Food Banking System",
        "url": "https://www.foodbank1377.org/",
        "contact_email": "foodbank@kncsw.org",
        "whatsapp": "82220773000",
    },
    {
        "country": "Taiwan",
        "state": "Multi-State",
        "supported_states": ["Taipei", "Kaohsiung", "Taichung"],
        "cities": ["Taipei", "Kaohsiung", "Taichung"],
        "neighborhoods": ["Xinyi", "Daan", "Zhongshan", "Ximending", "Songshan", "Lingya", "Zuoying"],
        "name": "Alliance of Taiwan Foodbanks",
        "type": "Regional Excess Redistribution Alliance",
        "url": "https://www.taiwanfoodbank.org.tw/",
        "contact_email": "service@taiwanfoodbank.org.tw",
        "whatsapp": "886223456789",
    },
    {
        "country": "Thailand",
        "state": "Multi-State",
        "supported_states": ["Bangkok", "Phuket", "Chiang Mai"],
        "cities": ["Bangkok", "Phuket", "Chiang Mai"],
        "neighborhoods": ["Sukhumvit", "Silom", "Sathorn", "Chatuchak", "Patong", "Nimman Road"],
        "name": "SOS Thailand (Scholars of Sustenance)",
        "type": "Cooked Food Redistribution & Hotel Rescue",
        "url": "https://www.scholarsofsustenance.org/sos-thailand",
        "contact_email": "info@scholarsofsustenance.org",
        "whatsapp": "66814567890",
    },

    # ------------------------------------------------------------
    # NORTH AMERICA — USA, CANADA, MEXICO
    # ------------------------------------------------------------
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
    {
        "country": "Canada",
        "state": "Multi-State",
        "supported_states": ["Ontario", "British Columbia", "Quebec", "Alberta", "Manitoba"],
        "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Winnipeg", "Mississauga", "Brampton"],
        "neighborhoods": ["Downtown Toronto", "Scarborough", "North York", "Etobicoke", "Leslieville", "Yorkville", "Plateau-Mont-Royal", "Mile End", "Ville-Marie", "Rosemont", "Kitsilano", "Downtown Eastside", "Mount Pleasant", "Gastown", "Centretown", "ByWard Market"],
        "name": "Second Harvest Canada",
        "type": "National Food Logistics & Rescue",
        "url": "https://www.secondharvest.ca/",
        "contact_email": "support@secondharvest.ca",
        "whatsapp": "14164082594",
    },
    {
        "country": "Mexico",
        "state": "Multi-State",
        "supported_states": ["CDMX", "Jalisco", "Nuevo León", "Puebla", "Baja California", "Querétaro"],
        "cities": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "Querétaro"],
        "neighborhoods": ["Roma Norte", "Condesa", "Polanco", "Cuauhtémoc", "Coyoacán", "Centro Histórico", "Zapopan", "San Pedro Garza García"],
        "name": "BAMX (Red de Bancos de Alimentos de México)",
        "type": "National Food Bank Federation",
        "url": "https://bamx.org.mx/",
        "contact_email": "contacto@bamx.org.mx",
        "whatsapp": "525555740000",
    },

    # ------------------------------------------------------------
    # LATIN AMERICA & SOUTH AMERICA
    # ------------------------------------------------------------
    {
        "country": "Brazil",
        "state": "Multi-State",
        "supported_states": ["São Paulo", "Rio de Janeiro", "Distrito Federal", "Bahia", "Minas Gerais"],
        "cities": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Belo Horizonte"],
        "neighborhoods": ["Paulista", "Pinheiros", "Vila Madalena", "Itaim Bibi", "Copacabana", "Ipanema", "Botafogo", "Centro SP", "Centro RJ"],
        "name": "Mesa Brasil SESC",
        "type": "National Network of Food Banks",
        "url": "https://www.sesc.com.br/atuacoes/assistencia/mesa-brasil/",
        "contact_email": "mesabrasil@sesc.com.br",
        "whatsapp": "551132791500",
    },
    {
        "country": "Argentina",
        "state": "Buenos Aires",
        "supported_states": ["Buenos Aires Province", "CABA"],
        "cities": ["Buenos Aires"],
        "neighborhoods": ["Palermo", "Recoleta", "San Telmo", "Belgrano", "Puerto Madero"],
        "name": "Banco de Alimentos de Buenos Aires",
        "type": "Surplus Redistribution Infrastructure",
        "url": "https://www.bancodealimentos.org.ar/",
        "contact_email": "info@bancodealimentos.org.ar",
        "whatsapp": "541147242332",
    },
    {
        "country": "Colombia",
        "state": "Multi-State",
        "supported_states": ["Bogotá D.C.", "Antioquia"],
        "cities": ["Bogotá", "Medellín"],
        "neighborhoods": ["Chapinero", "Usaquén", "La Candelaria", "El Poblado", "Laureles"],
        "name": "ABACO (Asociación de Bancos de Alimentos de Colombia)",
        "type": "National Food Bank Federation",
        "url": "https://abaco.org.co/",
        "contact_email": "contacto@abaco.org.co",
        "whatsapp": "5717441234",
    },
    {
        "country": "Chile",
        "state": "Multi-State",
        "supported_states": ["Santiago Metropolitan", "Valparaíso Region"],
        "cities": ["Santiago", "Valparaíso", "Viña del Mar"],
        "neighborhoods": ["Providencia", "Las Condes", "Bellavista", "Santiago Centro", "Vitacura", "Cerro Alegre"],
        "name": "Red de Alimentos (Chile Food Bank)",
        "type": "First Food Bank of Chile",
        "url": "https://www.redalimentos.cl/",
        "contact_email": "contacto@redalimentos.cl",
        "whatsapp": "56225551234",
    },
    {
        "country": "Peru",
        "state": "Lima",
        "supported_states": ["Lima Province"],
        "cities": ["Lima", "Callao"],
        "neighborhoods": ["Miraflores", "San Isidro", "Barranco", "Surco", "Centro Histórico Lima"],
        "name": "Banco de Alimentos Perú",
        "type": "Peruvian Surplus Recovery Alliance",
        "url": "https://bancodealimentosperu.org/",
        "contact_email": "contacto@bancodealimentosperu.org",
        "whatsapp": "5112411234",
    },

    # ------------------------------------------------------------
    # EUROPE
    # ------------------------------------------------------------
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
    {
        "country": "Germany",
        "state": "Multi-State",
        "supported_states": ["Berlin", "Hamburg", "Bavaria", "Hesse", "North Rhine-Westphalia", "Baden-Württemberg"],
        "cities": ["Berlin", "Hamburg", "Munich", "Frankfurt", "Cologne", "Stuttgart"],
        "neighborhoods": ["Mitte", "Kreuzberg", "Friedrichshain", "Neukölln", "Prenzlauer Berg", "Altona", "Schwabing", "Sachsenhausen"],
        "name": "Tafel Deutschland e.V.",
        "type": "Food Distribution Stations & Volunteer Hubs",
        "url": "https://www.tafel.de/",
        "contact_email": "info@tafel.de",
        "whatsapp": "493020059760",
    },
    {
        "country": "France",
        "state": "Multi-Region",
        "supported_states": ["Île-de-France", "Auvergne-Rhône-Alpes", "Provence-Alpes-Côte d'Azur", "Occitanie", "Nouvelle-Aquitaine", "Hauts-de-France"],
        "cities": ["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux", "Lille"],
        "neighborhoods": ["Le Marais", "Montmartre", "Latin Quarter", "Bastille", "10th Arrondissement", "Presqu'île", "Vieux Lyon"],
        "name": "Fédération Française des Banques Alimentaires",
        "type": "Surplus Recovery & Food Security Network",
        "url": "https://www.banquealimentaire.org/",
        "contact_email": "ffba@banquealimentaire.org",
        "whatsapp": "33149080470",
    },
    {
        "country": "Spain",
        "state": "Multi-Region",
        "supported_states": ["Madrid", "Catalonia", "Andalusia", "Basque Country", "Valencia"],
        "cities": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao", "Málaga"],
        "neighborhoods": ["Malasaña", "Chueca", "Salamanca", "Lavapiés", "Eixample", "Gràcia", "El Raval", "Gothic Quarter", "Poblenou", "Ruzafa"],
        "name": "FESBAL (Federación Española de Bancos de Alimentos)",
        "type": "National Federation of Regional Food Banks",
        "url": "https://www.fesbal.org/",
        "contact_email": "comunicacion@fesbal.org",
        "whatsapp": "34917242180",
    },
    {
        "country": "Netherlands",
        "state": "North Holland",
        "supported_states": ["North Holland", "South Holland", "Utrecht"],
        "cities": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht"],
        "neighborhoods": ["Centrum", "De Pijp", "Jordaan", "Amsterdam Noord", "Kralingen"],
        "name": "Voedselbanken Nederland",
        "type": "National Food Pantry Network",
        "url": "https://voedselbanken.nl/",
        "contact_email": "info@voedselbanken.nl",
        "whatsapp": "31206123456",
    },
    {
        "country": "Ireland",
        "state": "Republic of Ireland",
        "supported_states": ["Leinster", "Munster", "Connacht"],
        "cities": ["Dublin", "Cork", "Galway", "Limerick", "Waterford"],
        "neighborhoods": ["City Centre Dublin", "Temple Bar", "Rathmines", "Docklands", "Salthill"],
        "name": "FoodCloud",
        "type": "Digital Technology & Logistics Platform",
        "url": "https://food.cloud/",
        "contact_email": "info@food.cloud",
        "whatsapp": "35318625900",
    },
    {
        "country": "Italy",
        "state": "Multi-Region",
        "supported_states": ["Lombardy", "Lazio", "Campania", "Piedmont"],
        "cities": ["Rome", "Milan", "Naples", "Turin"],
        "neighborhoods": ["Trastevere", "Monti", "Navigli", "Brera", "Porta Nuova"],
        "name": "Banco Alimentare",
        "type": "National Food Recovery Foundation",
        "url": "https://www.bancoalimentare.it/",
        "contact_email": "info@bancoalimentare.it",
        "whatsapp": "39028965841",
    },
    {
        "country": "Belgium",
        "state": "Multi-Region",
        "supported_states": ["Brussels-Capital", "Flanders", "Wallonia"],
        "cities": ["Brussels", "Antwerp", "Ghent"],
        "neighborhoods": ["European Quarter", "Ixelles", "Saint-Gilles", "Zurenborg", "Zuid"],
        "name": "Fédération Belge des Banques Alimentaires",
        "type": "Belgian Food Banking Network",
        "url": "https://www.foodbanks.be/",
        "contact_email": "info@foodbanks.be",
        "whatsapp": "3227611111",
    },
    {
        "country": "Portugal",
        "state": "Multi-State",
        "supported_states": ["Lisbon District", "Porto District"],
        "cities": ["Lisbon", "Porto", "Coimbra"],
        "neighborhoods": ["Alfama", "Bairro Alto", "Baixa-Chiado", "Belém", "Ribeira", "Foz do Douro"],
        "name": "Banco Alimentar Contra a Fome",
        "type": "Federation of Portuguese Food Banks",
        "url": "https://www.bancoalimentar.pt/",
        "contact_email": "geral@bancoalimentar.pt",
        "whatsapp": "351213649646",
    },
    {
        "country": "Sweden",
        "state": "Multi-State",
        "supported_states": ["Stockholm County", "Västra Götaland", "Skåne"],
        "cities": ["Stockholm", "Gothenburg", "Malmö"],
        "neighborhoods": ["Södermalm", "Norrmalm", "Östermalm", "Gamla Stan", "Haga", "Västra Hamnen"],
        "name": "Sveriges Stadsmissioner (Matmissionen)",
        "type": "Social Grocery & Surplus Redirection",
        "url": "https://www.stadsmissionen.se/",
        "contact_email": "info@stadsmissionen.se",
        "whatsapp": "46868401000",
    },
    {
        "country": "Switzerland",
        "state": "Multi-State",
        "supported_states": ["Zurich", "Geneva", "Vaud"],
        "cities": ["Zurich", "Geneva", "Lausanne", "Basel"],
        "neighborhoods": ["Altstadt", "Langstrasse", "Züri-West", "Plainpalais", "Eaux-Vives", "Paquis"],
        "name": "Schweizer Tafel (Table Suisse)",
        "type": "Swiss Surplus Redistribution Fleet",
        "url": "https://www.schweizertafel.ch/",
        "contact_email": "info@schweizertafel.ch",
        "whatsapp": "41627450000",
    },
    {
        "country": "Poland",
        "state": "Multi-State",
        "supported_states": ["Masovian", "Lesser Poland"],
        "cities": ["Warsaw", "Kraków", "Wrocław"],
        "neighborhoods": ["Śródmieście", "Mokotów", "Praga-Północ", "Stare Miasto", "Kazimierz", "Podgórze"],
        "name": "Federacja Polskich Banków Żywności",
        "type": "Polish Federation of Food Banks",
        "url": "https://bankizywnosci.pl/",
        "contact_email": "biuro@bankizywnosci.pl",
        "whatsapp": "48226546410",
    },
    {
        "country": "Greece",
        "state": "Multi-State",
        "supported_states": ["Attica", "Central Macedonia"],
        "cities": ["Athens", "Thessaloniki", "Patras"],
        "neighborhoods": ["Plaka", "Monastiraki", "Kolonaki", "Exarcheia", "Pangrati", "Ladadika", "Kalamaria"],
        "name": "Boroume (\"We Can\")",
        "type": "Food Waste Reduction & Charity Redistribution",
        "url": "https://www.boroume.gr/",
        "contact_email": "info@boroume.gr",
        "whatsapp": "302103237805",
    },

    # ------------------------------------------------------------
    # AFRICA
    # ------------------------------------------------------------
    {
        "country": "South Africa",
        "state": "Multi-State",
        "supported_states": ["Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape"],
        "cities": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Gqeberha", "Port Elizabeth"],
        "neighborhoods": ["Sandton", "Rosebank", "Soweto", "Braamfontein", "City Bowl", "Woodstock", "Sea Point", "Camps Bay", "Morningside Durban"],
        "name": "FoodForward SA",
        "type": "Recovery & Redistribution Infrastructure",
        "url": "https://foodforwardsa.org/",
        "contact_email": "info@foodforwardsa.org",
        "whatsapp": "27215315670",
    },
    {
        "country": "Kenya",
        "state": "Multi-State",
        "supported_states": ["Nairobi County", "Mombasa County", "Kisumu County"],
        "cities": ["Nairobi", "Mombasa", "Kisumu"],
        "neighborhoods": ["Westlands", "Kilimani", "Nairobi CBD", "Karen", "Kibera", "Nyali"],
        "name": "Food Banking Kenya",
        "type": "Regional Hub & Farm Recovery",
        "url": "https://foodbankingkenya.org/",
        "contact_email": "info@foodbankingkenya.org",
        "whatsapp": "254712345678",
    },
    {
        "country": "Nigeria",
        "state": "Multi-State",
        "supported_states": ["Lagos", "FCT", "Oyo"],
        "cities": ["Lagos", "Abuja", "Ibadan"],
        "neighborhoods": ["Victoria Island", "Lekki", "Ikeja", "Surulere", "Yaba", "Ikoyi", "Maitama", "Wuse"],
        "name": "Lagos Food Bank Initiative",
        "type": "Hunger Relief & Malnutrition Programs",
        "url": "https://lagosfoodbank.org/",
        "contact_email": "contactus@lagosfoodbank.org",
        "whatsapp": "2348023123456",
    },
    {
        "country": "Ghana",
        "state": "Greater Accra",
        "supported_states": ["Greater Accra Region"],
        "cities": ["Accra", "Tema"],
        "neighborhoods": ["Osu", "Airport Residential", "East Legon", "Cantonments", "Labone"],
        "name": "Food for All Africa",
        "type": "West African Food Recovery System",
        "url": "https://foodforallafrica.com/",
        "contact_email": "info@foodforallafrica.com",
        "whatsapp": "233247222222",
    },
    {
        "country": "Egypt",
        "state": "Cairo Governorate",
        "supported_states": ["Cairo", "Giza", "Alexandria"],
        "cities": ["Cairo", "Giza", "Alexandria"],
        "neighborhoods": ["Zamalek", "Maadi", "New Cairo", "Nasr City", "Dokki"],
        "name": "Egyptian Food Bank",
        "type": "Regional Large-Scale Food Assistance",
        "url": "https://www.efb.eg/",
        "contact_email": "info@efb.eg",
        "whatsapp": "20216060",
    },
    {
        "country": "Morocco",
        "state": "Multi-State",
        "supported_states": ["Casablanca-Settat", "Rabat-Salé-Kénitra", "Marrakesh-Safi"],
        "cities": ["Casablanca", "Rabat", "Marrakech"],
        "neighborhoods": ["Maarif", "Anfa", "Gauthier", "Ain Diab", "Agdal", "Hassan", "Gueliz", "Medina"],
        "name": "Banque Alimentaire Maroc",
        "type": "National Food Relief Federation",
        "url": "https://banquealimentaire.ma/",
        "contact_email": "contact@banquealimentaire.ma",
        "whatsapp": "212522200000",
    },
    {
        "country": "Uganda",
        "state": "Central Region",
        "supported_states": ["Kampala District", "Wakiso"],
        "cities": ["Kampala", "Entebbe"],
        "neighborhoods": ["Kololo", "Nakasero", "Bugolobi", "Ntinda", "Kansanga"],
        "name": "Hunger Fighters Uganda",
        "type": "Nutritional Assistance & Food Routing",
        "url": "https://hungerfightersuganda.org/",
        "contact_email": "info@hungerfightersuganda.org",
        "whatsapp": "256414123456",
    },

    # ------------------------------------------------------------
    # OCEANIA — AUSTRALIA & NEW ZEALAND
    # ------------------------------------------------------------
    {
        "country": "Australia",
        "state": "Multi-State",
        "supported_states": ["New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia", "ACT"],
        "cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra", "Gold Coast", "Newcastle"],
        "neighborhoods": ["Surry Hills", "Newtown", "Parramatta", "CBD Sydney", "Bondi", "Fitzroy", "Brunswick", "St Kilda", "Southbank", "Carlton", "Fortitude Valley", "Fremantle"],
        "name": "OzHarvest",
        "type": "Perishable Food Rescue Fleet",
        "url": "https://www.ozharvest.org/",
        "contact_email": "info@ozharvest.org",
        "whatsapp": "611800108006",
    },
    {
        "country": "New Zealand",
        "state": "Multi-State",
        "supported_states": ["Wellington", "Auckland"],
        "cities": ["Wellington", "Auckland", "Lower Hutt", "Porirua", "Kapiti"],
        "neighborhoods": ["Te Aro", "Newtown", "Ponsonby", "Mount Eden", "Auckland CBD", "Lambton Quay", "Parnell"],
        "name": "Kaibosh & KiwiHarvest",
        "type": "Regional Surplus Food Rescue",
        "url": "https://www.kaibosh.org.nz/",
        "contact_email": "info@kaibosh.org.nz",
        "whatsapp": "6443850825",
    },
]

# ------------------------------------------------------------
# COUNTRY-SCOPED STATE ALIASES
# ------------------------------------------------------------
STATE_ALIASES = {
    # INDIA STATES & UTs
    "andhra pradesh": ("Andhra Pradesh", "India"),
    "andhra": ("Andhra Pradesh", "India"),
    "ap": ("Andhra Pradesh", "India"),
    "arunachal pradesh": ("Arunachal Pradesh", "India"),
    "assam": ("Assam", "India"),
    "bihar": ("Bihar", "India"),
    "chhattisgarh": ("Chhattisgarh", "India"),
    "goa": ("Goa", "India"),
    "gujarat": ("Gujarat", "India"),
    "haryana": ("Haryana", "India"),
    "himachal pradesh": ("Himachal Pradesh", "India"),
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

    # CANADA
    "ontario": ("Ontario", "Canada"),
    "quebec": ("Quebec", "Canada"),
    "british columbia": ("British Columbia", "Canada"),
    "bc": ("British Columbia", "Canada"),
    "alberta": ("Alberta", "Canada"),
    "manitoba": ("Manitoba", "Canada"),

    # AUSTRALIA
    "new south wales": ("New South Wales", "Australia"),
    "nsw": ("New South Wales", "Australia"),
    "victoria": ("Victoria", "Australia"),
    "vic": ("Victoria", "Australia"),
    "queensland": ("Queensland", "Australia"),
    "qld": ("Queensland", "Australia"),
    "western australia": ("Western Australia", "Australia"),
    "wa": ("Western Australia", "Australia"),
}

CITY_ALIASES = {
    # INDIA
    "new delhi": "Delhi",
    "delhi": "Delhi",
    "ncr": "Delhi",
    "gurgaon": "Delhi",
    "gurugram": "Delhi",
    "noida": "Noida",
    "greater noida": "Greater Noida",
    "ghaziabad": "Ghaziabad",
    "faridabad": "Delhi",
    "connaught place": "Delhi",
    "cp": "Delhi",
    "hauz khas": "Delhi",
    "dwarka": "Delhi",
    "rohini": "Delhi",
    "saket": "Delhi",
    "karol bagh": "Delhi",
    "cyber city": "Delhi",

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
    "chembur": "Mumbai",
    "dharavi": "Mumbai",
    "vashi": "Navi Mumbai",
    "nerul": "Navi Mumbai",
    "belapur": "Navi Mumbai",
    "navi mumbai": "Navi Mumbai",
    "thane": "Thane",

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
    "hebbal": "Bengaluru",

    "madras": "Chennai",
    "chennai": "Chennai",
    "t nagar": "Chennai",
    "adyar": "Chennai",
    "velachery": "Chennai",
    "anna nagar": "Chennai",
    "mylapore": "Chennai",
    "omr": "Chennai",

    "hyderabad": "Hyderabad",
    "secunderabad": "Hyderabad",
    "gachibowli": "Hyderabad",
    "hitec city": "Hyderabad",
    "madhapur": "Hyderabad",
    "banjara hills": "Hyderabad",
    "jubilee hills": "Hyderabad",

    "calcutta": "Kolkata",
    "kolkata": "Kolkata",
    "salt lake": "Kolkata",
    "new town": "Kolkata",
    "park street": "Kolkata",
    "ballygunge": "Kolkata",

    "cochin": "Kochi",
    "kochi": "Kochi",
    "ernakulam": "Kochi",
    "kakkanad": "Kochi",
    "edappally": "Kochi",
    "trivandrum": "Thiruvananthapuram",
    "thiruvananthapuram": "Thiruvananthapuram",
    "technopark": "Thiruvananthapuram",
    "calicut": "Kozhikode",

    # SOUTH ASIA & MIDDLE EAST
    "karachi": "Karachi",
    "lahore": "Lahore",
    "islamabad": "Islamabad",
    "dhaka": "Dhaka",
    "chittagong": "Chittagong",
    "kathmandu": "Kathmandu",
    "dubai": "Dubai",
    "abu dhabi": "Abu Dhabi",
    "riyadh": "Riyadh",
    "jeddah": "Jeddah",
    "doha": "Doha",
    "istanbul": "Istanbul",
    "ankara": "Ankara",

    # ASIA PACIFIC
    "singapore": "Singapore",
    "bali": "Bali",
    "canggu": "Bali",
    "ubud": "Bali",
    "jakarta": "Jakarta",
    "kl": "Kuala Lumpur",
    "kuala lumpur": "Kuala Lumpur",
    "manila": "Manila",
    "bgc": "Taguig",
    "hcmc": "Ho Chi Minh City",
    "saigon": "Ho Chi Minh City",
    "hanoi": "Hanoi",
    "hong kong": "Hong Kong",
    "tokyo": "Tokyo",
    "osaka": "Osaka",
    "seoul": "Seoul",
    "taipei": "Taipei",
    "bangkok": "Bangkok",

    # AMERICAS
    "nyc": "New York",
    "new york city": "New York",
    "manhattan": "New York",
    "brooklyn": "New York",
    "queens": "New York",
    "bronx": "New York",
    "sf": "San Francisco",
    "san fran": "San Francisco",
    "bay area": "San Francisco",
    "la": "Los Angeles",
    "los angeles": "Los Angeles",
    "chicago": "Chicago",
    "boston": "Boston",
    "seattle": "Seattle",
    "miami": "Miami",
    "toronto": "Toronto",
    "vancouver": "Vancouver",
    "montreal": "Montreal",
    "cdmx": "Mexico City",
    "mexico city": "Mexico City",
    "sao paulo": "São Paulo",
    "rio": "Rio de Janeiro",
    "rio de janeiro": "Rio de Janeiro",
    "buenos aires": "Buenos Aires",
    "bogota": "Bogotá",
    "santiago": "Santiago",
    "lima": "Lima",

    # EUROPE
    "london": "London",
    "manchester": "Manchester",
    "paris": "Paris",
    "berlin": "Berlin",
    "munich": "Munich",
    "madrid": "Madrid",
    "barcelona": "Barcelona",
    "amsterdam": "Amsterdam",
    "dublin": "Dublin",
    "rome": "Rome",
    "milan": "Milan",
    "brussels": "Brussels",
    "lisbon": "Lisbon",
    "stockholm": "Stockholm",
    "zurich": "Zurich",
    "geneva": "Geneva",
    "warsaw": "Warsaw",
    "athens": "Athens",

    # AFRICA & OCEANIA
    "johannesburg": "Johannesburg",
    "joburg": "Johannesburg",
    "cape town": "Cape Town",
    "durban": "Durban",
    "nairobi": "Nairobi",
    "lagos": "Lagos",
    "accra": "Accra",
    "cairo": "Cairo",
    "casablanca": "Casablanca",
    "kampala": "Kampala",
    "sydney": "Sydney",
    "melbourne": "Melbourne",
    "auckland": "Auckland",
    "wellington": "Wellington",
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
            if not detected_country:
                for org in ORGS:
                    if canonical_v in org.get("cities", []):
                        detected_country = org.get("country")
                        break
            return canonical_v, alias_k.title(), detected_state, detected_country

    for org in ORGS:
        for hood in org.get("neighborhoods", []):
            if re.search(r"(?<!\w)" + re.escape(hood.lower()) + r"(?!\w)", t):
                return org["cities"][0], hood, detected_state or org.get("state"), org.get("country")

        for city in org.get("cities", []):
            if re.search(r"(?<!\w)" + re.escape(city.lower()) + r"(?!\w)", t):
                return canonical_city(city), None, detected_state or org.get("state"), org.get("country")

    patterns = [
        r"\bin\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\bfrom\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\baround\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\bnear\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
        r"\bat\s+([a-zA-ZÀ-ÿ0-9 .'-]{1,35})",
    ]
    stop_words = {"a", "an", "the", "and", "with", "where", "what", "how", "please", "state", "city", "country"}
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

def detect_intent(text):
    t = clean(text)
    location_words = [
        "where", "find", "near", "ngo", "charity", "food bank", "foodbank",
        "organization", "organisation", "centre", "center", "donate",
        "donation", "give", "collect", "pickup", "pick up", "redistribute",
        "redistribution", "food rescue", "who can take", "state", "street", "area", "country"
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
            state_match = (
                clean(org.get("state", "")) == clean(state) or
                any(clean(s) == clean(state) for s in org.get("supported_states", []))
            )

        if hood_match or city_match or state_match or (country_match and not city and not state and not neighborhood):
            matched_results.append({
                **org,
                "is_hyperlocal": hood_match,
                "is_city_match": city_match,
                "is_state_match": state_match,
                "is_country_match": country_match
            })

    return sorted(
        matched_results,
        key=lambda x: (
            x.get("is_hyperlocal", False),
            x.get("is_city_match", False),
            x.get("is_state_match", False),
            x.get("is_country_match", False)
        ),
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

Please let me know if your team can accept this batch or redirect me to an active partner depot.

Best regards,
{name}
"""
    recipient = org.get("contact_email", "")
    return f"mailto:{recipient}?subject={quote(subject)}&body={quote(body)}"

def create_whatsapp_link(org, name, food, quantity, location_str, notes):
    phone = org.get("whatsapp", "")
    text_msg = (
        f"🌱 *Food Donation Enquiry — Plateful Relay*\n\n"
        f"*Donor:* {name}\n"
        f"*Location:* {location_str}\n"
        f"*Food Items:* {food}\n"
        f"*Quantity:* {quantity}\n"
        f"*Logistics/Condition:* {notes}\n\n"
        f"_Please let me know if your team or volunteers can route this collection._"
    )
    return f"https://wa.me/{phone}?text={quote(text_msg)}"

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
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ------------------------------------------------------------
# DARK EDITORIAL STYLING
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

.impact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin-top: 14px;
    margin-bottom: 10px;
}

.impact-badge {
    background: #1F281E;
    border: 1px solid #2EA043;
    border-radius: 10px;
    padding: 10px 14px;
    text-align: center;
}

.impact-val {
    font-size: 1.3rem;
    font-weight: 700;
    color: #7EE787;
    line-height: 1.1;
}

.impact-label {
    font-size: 0.72rem;
    color: #9DA7B3;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 4px;
    letter-spacing: 0.05em;
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
    <div class="tag-badge">Global Active Relay</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="section-tag">Decentralized Redistribution Platform</div>
    <div class="hero-headline">Good food deserves a second destination.</div>
    <p class="hero-sub">
        Every day, commercial kitchens, catered events, and households have wholesome meals left over.
        Plateful helps you route excess edible food directly to active non-profit kitchens and volunteer networks across 30+ countries.
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
        <div class="step-heading">Pinpoint Context</div>
        <p class="step-desc">Enter any street, neighborhood, city, state, or portion count.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-index">STEP 02</div>
        <div class="step-heading">Discover Local Nodes</div>
        <p class="step-desc">Match verified redistribution depots prioritized by street and local proximity.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-index">STEP 03</div>
        <div class="step-heading">Fast-Track Dispatch</div>
        <p class="step-desc">Instantly produce standardized volunteer emails and direct WhatsApp coordination texts.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# CONVERSATIONAL ASSISTANT INTERFACE
# ------------------------------------------------------------
st.markdown("<div class=\"section-tag\">Hyper-Local Relay Assistant</div>", unsafe_allow_html=True)
st.markdown("### How can we help you redistribute today?")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("E.g., 'We have 40 meals left over in Indiranagar, Bangalore' or 'Excess buffet trays in Brooklyn'")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    intent = detect_intent(user_input)
    city, neighborhood, state, country = detect_location(user_input)
    portions = extract_portion_count(user_input)

    location_parts = []
    if neighborhood:
        location_parts.append(neighborhood)
    if city and (not neighborhood or city.lower() != neighborhood.lower()):
        location_parts.append(city)
    if state and state not in location_parts:
        location_parts.append(state)
    if country and country not in location_parts and not city and not neighborhood:
        location_parts.append(country)

    display_loc = ", ".join(location_parts) if location_parts else None

    # Compute Eco Metrics if portions detected
    impact_data = compute_impact(portions)

    if display_loc:
        orgs = find_orgs(city=city, neighborhood=neighborhood, state=state, country=country)
        if orgs:
            reply = (
                f"We identified **{len(orgs)} verified redistribution partner(s)** matching **{display_loc}**.\n\n"
                "Browse the details below to review their operations or launch an email / WhatsApp dispatch."
            )
        else:
            reply = (
                f"We currently do not have a pre-indexed partner active in **{display_loc}** in this prototype database. "
                "For unlisted zones, municipal social services or community soup kitchens (such as temple or gurdwara langars, or church pantries) often welcome direct safe drop-offs."
            )
    elif intent == "greeting":
        reply = (
            "Hello! I am ready to coordinate surplus food redistribution. "
            "Tell me **what city, neighborhood, or state** you are in (e.g., *'Indiranagar, Bangalore'*, *'Kerala'*, *'Brooklyn, NYC'*), and an estimate of portions available."
        )
        orgs = []
    elif intent == "surplus":
        reply = (
            "We can definitely find a destination for that surplus. "
            "**Which neighborhood, city, state, or country are you located in?**"
        )
        orgs = []
    else:
        reply = (
            "I can assist with locating food rescue organizations.\n\n"
            "Try specifying an area:\n"
            "- *“We have 40 leftover boxed lunches in Indiranagar, Bengaluru.”*\n"
            "- *“Surplus hotel buffet meals in Downtown Dubai.”*\n"
            "- *“Surplus catered trays in Brooklyn, NYC.”*"
        )
        orgs = []

    if impact_data:
        reply += (
            f"\n\n**Estimated Salvage Impact for {impact_data['meals']} Portions:**\n"
            f"- 🥗 **{impact_data['food_kg']} kg** food preserved from landfills\n"
            f"- ☁️ **{impact_data['co2_saved_kg']} kg** greenhouse CO₂e emissions prevented\n"
            f"- 💧 **{impact_data['water_liters']} Liters** embedded water footprint safeguarded"
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
# MATCHED ORGANISATIONS SECTION
# ------------------------------------------------------------
if st.session_state.last_results:
    display_title = st.session_state.display_location or "Your Search Area"
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class=\"section-tag\">Results for {display_title}</div>", unsafe_allow_html=True)

    for index, org in enumerate(st.session_state.last_results):
        with st.container(border=True):
            head_col, action_col = st.columns([2.4, 1.6])

            with head_col:
                st.markdown(f"#### {org['name']}")

                tags_html = f"<span class='pill-meta'>{org['country']}</span>"

                if org.get("state") == "Multi-State":
                    if org.get("country") == "India":
                        tags_html += "<span class='pill-state'>Pan-India Network</span>"
                    elif org.get("country") == "United States":
                        tags_html += "<span class='pill-state'>US Multi-State</span>"
                    elif org.get("country") == "Canada":
                        tags_html += "<span class='pill-state'>Multi-Province (Canada)</span>"
                    elif org.get("country") == "Australia":
                        tags_html += "<span class='pill-state'>Multi-State (Australia)</span>"
                    else:
                        tags_html += f"<span class='pill-state'>{org['country']} Multi-Region</span>"
                elif org.get("state"):
                    tags_html += f"<span class='pill-state'>{org['state']}</span>"

                tags_html += f"<span class='pill-meta'>{org['type']}</span>"

                if org.get("is_hyperlocal"):
                    tags_html += "<span class='pill-local'>Direct Neighborhood Match</span>"

                st.markdown(tags_html, unsafe_allow_html=True)

                if org.get("neighborhoods"):
                    hoods_display = ", ".join(org["neighborhoods"][:6])
                    st.caption(f"📍 Notable Local Hubs: {hoods_display}")
                else:
                    coverage_str = ", ".join(org['cities'][:6]) + ("..." if len(org['cities']) > 6 else "")
                    st.caption(f"Key Hubs: {coverage_str}")

                if org.get("supported_states") and org.get("state") == "Multi-State":
                    states_display = ", ".join(org["supported_states"][:6]) + ("..." if len(org["supported_states"]) > 6 else "")
                    st.caption(f"🗺️ Regional/State Coverage: {states_display}")

            with action_col:
                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                st.link_button(
                    "Visit Website ↗",
                    org["url"],
                    use_container_width=True
                )
                if st.button(
                    "Coordinate Dispatch Notice",
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
# DRAFT ENQUIRY WORKFLOW (EMAIL + WHATSAPP)
# ------------------------------------------------------------
if st.session_state.request_recorded and st.session_state.last_results:
    selected_idx = st.session_state.selected_org
    if selected_idx < len(st.session_state.last_results):
        org = st.session_state.last_results[selected_idx]
        loc_str = st.session_state.display_location or "your locality"
        default_qty = f"{st.session_state.last_portions} portions" if st.session_state.last_portions else ""

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class=\"section-tag\">Prepare Communication</div>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"### Donation Notification for {org['name']}")
            st.markdown(f"Generate a standardized hand-off notice for operations in **{loc_str}**.")

            with st.form("donation_request_form"):
                fc1, fc2 = st.columns(2)
                with fc1:
                    name = st.text_input("Your Name / Establishment", placeholder="e.g., Green Garden Bistro")
                    food = st.text_input("Food Item Description", placeholder="e.g., Chilled vegetarian meal containers (freshly sealed)")
                with fc2:
                    email = st.text_input("Contact Email", placeholder="e.g., manager@greengarden.com")
                    quantity = st.text_input("Quantity / Portions", value=default_qty, placeholder="e.g., 40 individual boxes")

                notes = st.text_area(
                    "Logistics & Temperature Notes",
                    placeholder="e.g., Cooked at 1 PM, kept under refrigeration since 3 PM. Available for pickup until 8 PM."
                )

                submit_btn = st.form_submit_button("Generate Multi-Channel Dispatch Links", use_container_width=True)

            if submit_btn:
                if not name or not food or not quantity:
                    st.error("Please complete Name, Food Description, and Quantity.")
                else:
                    email_addr = email if email else "donor@plateful.local"
                    email_link = create_email_link(org, name, email_addr, food, quantity, loc_str, notes)
                    whatsapp_link = create_whatsapp_link(org, name, food, quantity, loc_str, notes)
                    st.success("Dispatch notifications compiled!")

                    bcol1, bcol2 = st.columns(2)
                    with bcol1:
                        st.link_button(
                            f"✉️ Open in Mail Client ({org.get('contact_email', 'Official')}) →",
                            email_link,
                            use_container_width=True
                        )
                    with bcol2:
                        st.link_button(
                            f"💬 Launch WhatsApp Dispatch ({org.get('whatsapp', 'Hotline')}) →",
                            whatsapp_link,
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
