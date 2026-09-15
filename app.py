import streamlit as st
import re
import time

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Plateful",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #F8F5EE;
        color: #24352A;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Hide default Streamlit elements */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ---------- TOP NAV ---------- */

    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 4px 25px 4px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-icon {
        width: 42px;
        height: 42px;
        border-radius: 14px;
        background: #DDE8D5;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
    }

    .brand-name {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #294332;
    }

    .brand-tag {
        font-size: 12px;
        color: #718073;
        margin-top: -3px;
    }


    /* ---------- HERO ---------- */

    .hero {
        background: #E8F0E3;
        border-radius: 30px;
        padding: 55px 55px 48px 55px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }

    .hero::after {
        content: "🍃";
        position: absolute;
        right: 45px;
        top: 25px;
        font-size: 85px;
        opacity: 0.13;
        transform: rotate(15deg);
    }

    .hero-eyebrow {
        display: inline-block;
        background: #FFFFFF;
        color: #55705A;
        border-radius: 30px;
        padding: 7px 14px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 17px;
    }

    .hero-title {
        font-size: 48px;
        line-height: 1.08;
        letter-spacing: -1.7px;
        color: #263E2E;
        font-weight: 800;
        max-width: 700px;
        margin-bottom: 16px;
    }

    .hero-title span {
        color: #6B8E63;
    }

    .hero-description {
        font-size: 17px;
        line-height: 1.65;
        color: #5D6D61;
        max-width: 680px;
        margin-bottom: 0;
    }


    /* ---------- IMPACT CARDS ---------- */

    .section-title {
        color: #294332;
        font-size: 25px;
        font-weight: 750;
        margin-top: 30px;
        margin-bottom: 6px;
    }

    .section-subtitle {
        color: #7A857C;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .impact-row {
        display: flex;
        gap: 14px;
        margin-bottom: 30px;
    }

    .impact-card {
        flex: 1;
        background: #FFFFFF;
        border: 1px solid #E7E9E2;
        border-radius: 20px;
        padding: 21px;
    }

    .impact-icon {
        font-size: 25px;
        margin-bottom: 10px;
    }

    .impact-title {
        color: #314A37;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 5px;
    }

    .impact-text {
        color: #7A857C;
        font-size: 13px;
        line-height: 1.45;
    }


    /* ---------- CHAT AREA ---------- */

    .chat-wrapper {
        background: #FFFFFF;
        border: 1px solid #E7E9E2;
        border-radius: 28px;
        padding: 28px;
        margin-top: 10px;
        box-shadow: 0 8px 30px rgba(47, 65, 50, 0.05);
    }

    .chat-heading {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }

    .bot-avatar {
        width: 43px;
        height: 43px;
        border-radius: 14px;
        background: #DDE8D5;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }

    .chat-title {
        color: #294332;
        font-weight: 750;
        font-size: 20px;
    }

    .chat-status {
        color: #7D897F;
        font-size: 12px;
    }


    /* ---------- MESSAGE BUBBLES ---------- */

    [data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 10px 14px;
        margin-bottom: 7px;
    }

    [data-testid="stChatMessageContent"] {
        color: #334238;
        line-height: 1.6;
    }


    /* ---------- ORGANIZATION CARDS ---------- */

    .org-card {
        background: #FBFCF9;
        border: 1px solid #E2E8DF;
        border-radius: 19px;
        padding: 20px;
        margin: 12px 0;
    }

    .org-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }

    .org-icon {
        width: 43px;
        height: 43px;
        background: #E7F0E3;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 21px;
    }

    .org-name {
        color: #2D4935;
        font-size: 17px;
        font-weight: 750;
    }

    .org-location {
        color: #7D897F;
        font-size: 12px;
        margin-top: 2px;
    }

    .org-detail {
        color: #637067;
        font-size: 13px;
        padding: 7px 0;
        border-top: 1px solid #EEF1EB;
    }

    .prototype-note {
        background: #FFF8E8;
        border: 1px solid #F0E2BD;
        color: #76643B;
        border-radius: 15px;
        padding: 13px 16px;
        font-size: 12px;
        line-height: 1.5;
        margin: 17px 0;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #8A948C;
        font-size: 12px;
        padding: 35px 0 5px 0;
    }

    .footer strong {
        color: #607263;
    }


    /* ---------- CHAT INPUT ---------- */

    [data-testid="stChatInput"] {
        border-color: #D9E2D5 !important;
    }

    [data-testid="stChatInput"] textarea {
        background: #FFFFFF !important;
    }


    /* ---------- MOBILE ---------- */

    @media (max-width: 700px) {

        .hero {
            padding: 35px 27px;
            border-radius: 24px;
        }

        .hero-title {
            font-size: 35px;
        }

        .hero-description {
            font-size: 15px;
        }

        .impact-row {
            flex-direction: column;
        }

        .chat-wrapper {
            padding: 20px;
        }

    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = {}

if "cached_orgs" not in st.session_state:
    st.session_state.cached_orgs = []

if "last_donation" not in st.session_state:
    st.session_state.last_donation = None


# ============================================================
# ORGANIZATION DIRECTORY
# ============================================================

# Prototype directory.
# Organizations should be contacted before arranging a donation.

ORGANIZATIONS = {
    "delhi": [
        {
            "name": "Robin Hood Army",
            "location": "Delhi",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Delhi",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "mumbai": [
        {
            "name": "Robin Hood Army",
            "location": "Mumbai",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Mumbai",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "bengaluru": [
        {
            "name": "Robin Hood Army",
            "location": "Bengaluru",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Bengaluru",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "hyderabad": [
        {
            "name": "Robin Hood Army",
            "location": "Hyderabad",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Hyderabad",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "chennai": [
        {
            "name": "Robin Hood Army",
            "location": "Chennai",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Chennai",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "kolkata": [
        {
            "name": "Robin Hood Army",
            "location": "Kolkata",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Kolkata",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "pune": [
        {
            "name": "Robin Hood Army",
            "location": "Pune",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Pune",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "ahmedabad": [
        {
            "name": "Robin Hood Army",
            "location": "Ahmedabad",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Ahmedabad",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "jaipur": [
        {
            "name": "Robin Hood Army",
            "location": "Jaipur",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Jaipur",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ]
}


# City aliases
CITY_ALIASES = {
    "new delhi": "delhi",
    "delhi ncr": "delhi",
    "ncr": "delhi",
    "bombay": "mumbai",
    "bangalore": "bengaluru",
    "bengaluru city": "bengaluru",
    "bangalore city": "bengaluru",
    "madras": "chennai"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_recipients(location: str):
    """Find organizations from the prototype directory."""

    location_clean = location.lower().strip()

    if location_clean in CITY_ALIASES:
        location_clean = CITY_ALIASES[location_clean]

    if location_clean in ORGANIZATIONS:
        return {"recipients": ORGANIZATIONS[location_clean]}

    # Try partial matching
    for city in ORGANIZATIONS:
        if city in location_clean or location_clean in city:
            return {"recipients": ORGANIZATIONS[city]}

    for alias, city in CITY_ALIASES.items():
        if alias in location_clean:
            return {"recipients": ORGANIZATIONS[city]}

    return {
        "message": "No organizations found for this location."
    }


def log_donation_request(user_name, user_phone, organizations):
    """
    Prototype logging.
    Stores the latest request in Streamlit session state.
    """

    try:
        timestamp = time.strftime("%d %b %Y, %I:%M %p")

        st.session_state.last_donation = {
            "name": user_name,
            "phone": user_phone,
            "organizations": organizations,
            "timestamp": timestamp
        }

        return {
            "success": True,
            "message": "Your donation request has been recorded successfully!"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def format_organizations(orgs):
    """Create polished organization cards."""

    response = ""

    for org in orgs:

        website = org.get("website", "#")

        response += f"""
        <div class="org-card">

            <div class="org-header">

                <div class="org-icon">🤝</div>

                <div>
                    <div class="org-name">
                        {org.get("name", "Organization")}
                    </div>

                    <div class="org-location">
                        📍 {org.get("location", "Location unavailable")}
                    </div>
                </div>

            </div>

            <div class="org-detail">
                📞 {org.get("phone", "Contact through official website")}
            </div>

            <div class="org-detail">
                🌐 <a href="{website}" target="_blank"
                style="color:#63825F; text-decoration:none;">
                Visit official website →
                </a>
            </div>

        </div>
        """

    return response


# ============================================================
# MAIN CHAT LOGIC
# ============================================================

def process_message(user_message):

    message_lower = user_message.lower().strip()
    context = st.session_state.context

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    if context.get("awaiting_user_name"):

        context["user_name"] = user_message
        context["awaiting_user_name"] = False
        context["awaiting_user_phone"] = True

        return (
            "Thank you 🌱\n\n"
            "Now, please provide a phone number for the donation request."
        )


    # --------------------------------------------------------
    # PHONE
    # --------------------------------------------------------

    if context.get("awaiting_user_phone"):

        context["user_phone"] = user_message

        with st.spinner("Recording your request..."):

            log_result = log_donation_request(
                context.get("user_name"),
                context.get("user_phone"),
                st.session_state.cached_orgs
            )

        st.session_state.context = {}

        if log_result.get("success"):
            return (
                "### ✅ Request recorded!\n\n"
                "Thank you for helping give surplus food a second purpose. "
                "Please contact the organization directly to coordinate the "
                "donation and confirm that they can accept it."
            )

        return f"❌ Something went wrong: {log_result.get('error')}"


    # --------------------------------------------------------
    # YES / NO CONFIRMATION
    # --------------------------------------------------------

    if context.get("awaiting_log_confirmation"):

        if message_lower in ["yes", "y", "yeah", "yep", "sure"]:

            context["awaiting_log_confirmation"] = False
            context["awaiting_user_name"] = True

            return (
                "Absolutely 🌿\n\n"
                "To record the request, please provide your name."
            )

        else:

            st.session_state.context = {}

            return (
                "No problem 🌱 I won't record the request.\n\n"
                "You can still contact the organizations directly."
            )


    # --------------------------------------------------------
    # DONATION SEARCH
    # --------------------------------------------------------

    if (
        "find" in message_lower
        or "donate" in message_lower
        or "where can" in message_lower
        or "food bank" in message_lower
    ):

        # Look for "in CITY"
        location_match = re.search(
            r"\bin\s+(.+?)(?:\?|$)",
            user_message,
            re.IGNORECASE
        )

        if not location_match:

            return (
                "I'd be happy to help 🌱\n\n"
                "Tell me the city you're in, for example:\n\n"
                "**Where can I donate in Bengaluru?**"
            )

        location = location_match.group(1).strip()

        # Remove punctuation
        location = location.rstrip(".,!?")

        with st.spinner(f"Finding organizations in {location}..."):

            result_data = find_recipients(location)

        if (
            "recipients" in result_data
            and result_data["recipients"]
        ):

            st.session_state.cached_orgs = result_data["recipients"]

            response = (
                f"### 🌿 Organizations in {location.title()}\n\n"
                "Here are some organizations from Plateful's prototype "
                "directory that you can explore:\n\n"
            )

            response += format_organizations(
                st.session_state.cached_orgs
            )

            response += """
            <div class="prototype-note">
                ⚠️ <b>Prototype note:</b> Please contact the organization
                before arranging a donation to confirm that they accept your
                type and quantity of food.
            </div>
            """

            response += (
                "\n\n**Would you like me to record this donation request?**"
                " (yes/no)"
            )

            context["awaiting_log_confirmation"] = True

            return response

        return (
            f"I couldn't find organizations in **{location.title()}** "
            "in my current prototype directory.\n\n"
            "Try another city such as Delhi, Mumbai, Bengaluru, "
            "Hyderabad, Chennai, Kolkata, Pune, Ahmedabad or Jaipur."
        )


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    return (
        "I'm here to help you redistribute surplus food 🌱\n\n"
        "Try telling me where you are, for example:\n\n"
        "**Where can I donate in Bengaluru?**"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="top-nav">

    <div class="brand">

        <div class="brand-icon">
            🍽️
        </div>

        <div>
            <div class="brand-name">
                Plateful
            </div>

            <div class="brand-tag">
                Food deserves a second purpose.
            </div>
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-eyebrow">
        🌱 FOOD REDISTRIBUTION
    </div>

    <div class="hero-title">
        Turn surplus food into
        <span>something meaningful.</span>
    </div>

    <div class="hero-description">
        Plateful helps connect surplus food with organizations
        that can help redistribute it — making it easier to
        reduce food waste and support communities.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    '<div class="section-title">How Plateful works</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'A simple path from extra food to potential redistribution.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="impact-row">

    <div class="impact-card">

        <div class="impact-icon">🍲</div>

        <div class="impact-title">
            01 · Share
        </div>

        <div class="impact-text">
            Tell Plateful what surplus food you have and where
            you are located.
        </div>

    </div>


    <div class="impact-card">

        <div class="impact-icon">🤝</div>

        <div class="impact-title">
            02 · Connect
        </div>

        <div class="impact-text">
            Explore organizations in your city that may be able
            to receive the donation.
        </div>

    </div>


    <div class="impact-card">

        <div class="impact-icon">♻️</div>

        <div class="impact-title">
            03 · Redistribute
        </div>

        <div class="impact-text">
            Coordinate directly with the organization and give
            surplus food a second purpose.
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CHAT HEADER
# ============================================================

st.markdown("""
<div class="chat-wrapper">

    <div class="chat-heading">

        <div class="bot-avatar">
            🍽️
        </div>

        <div>

            <div class="chat-title">
                Ask Plateful
            </div>

            <div class="chat-status">
                Your food redistribution assistant
            </div>

        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="🍽️" if message["role"] == "assistant" else "🙂"
    ):

        st.markdown(
            message["content"],
            unsafe_allow_html=True
        )


# ============================================================
# FIRST-TIME WELCOME MESSAGE
# ============================================================

if not st.session_state.messages:

    with st.chat_message("assistant", avatar="🍽️"):

        welcome_message = (
            "Hi! I'm **Plateful** 🌱\n\n"
            "I can help you find food-donation organizations "
            "in your city.\n\n"
            "Try something like:\n\n"
            "**Where can I donate in Bengaluru?**"
        )

        st.markdown(
            welcome_message,
            unsafe_allow_html=True
        )


# ============================================================
# CHAT INPUT
# ============================================================

if prompt := st.chat_input(
    "Tell Plateful what you need help with..."
):

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user", avatar="🙂"):

        st.markdown(prompt)


    # Generate response
    with st.chat_message("assistant", avatar="🍽️"):

        response = process_message(prompt)

        st.markdown(
            response,
            unsafe_allow_html=True
        )


    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    <strong>Plateful</strong> · Small actions can prevent food from
    going to waste.
    <br>
    Prototype developed for food redistribution and community impact.
</div>
""", unsafe_allow_html=True)
