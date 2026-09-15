import streamlit as st
import re

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Plateful",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# ORGANIZATION DIRECTORY
# ---------------------------------------------------------

ORGANIZATIONS = {
    "delhi": [
        {
            "name": "Robin Hood Army",
            "location": "Delhi",
            "description": "A volunteer-led organisation that works to redistribute surplus food.",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Delhi",
            "description": "Works towards reducing hunger and food waste through food redistribution.",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "mumbai": [
        {
            "name": "Robin Hood Army",
            "location": "Mumbai",
            "description": "A volunteer-led organisation that redistributes surplus food.",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Mumbai",
            "description": "Works towards reducing hunger and food waste.",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "bengaluru": [
        {
            "name": "Robin Hood Army",
            "location": "Bengaluru",
            "description": "A volunteer-led organisation that redistributes surplus food.",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Bengaluru",
            "description": "Works towards reducing hunger and food waste.",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "hyderabad": [
        {
            "name": "Robin Hood Army",
            "location": "Hyderabad",
            "description": "A volunteer-led organisation that redistributes surplus food.",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Hyderabad",
            "description": "Works towards reducing hunger and food waste.",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "chennai": [
        {
            "name": "Robin Hood Army",
            "location": "Chennai",
            "description": "A volunteer-led organisation that redistributes surplus food.",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Chennai",
            "description": "Works towards reducing hunger and food waste.",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "kolkata": [
        {
            "name": "Robin Hood Army",
            "location": "Kolkata",
            "description": "A volunteer-led organisation that redistributes surplus food.",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Kolkata",
            "description": "Works towards reducing hunger and food waste.",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "pune": [
        {
            "name": "Robin Hood Army",
            "location": "Pune",
            "description": "A volunteer-led organisation that redistributes surplus food.",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Pune",
            "description": "Works towards reducing hunger and food waste.",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "ahmedabad": [
        {
            "name": "Robin Hood Army",
            "location": "Ahmedabad",
            "description": "A volunteer-led organisation that redistributes surplus food.",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Ahmedabad",
            "description": "Works towards reducing hunger and food waste.",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "jaipur": [
        {
            "name": "Robin Hood Army",
            "location": "Jaipur",
            "description": "A volunteer-led organisation that redistributes surplus food.",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "location": "Jaipur",
            "description": "Works towards reducing hunger and food waste.",
            "website": "https://www.feedingindia.org/"
        }
    ]
}


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi — I'm Plateful. 🍽️\n\n"
                "I can help you find ways to redistribute surplus food "
                "instead of letting it go to waste."
            )
        }
    ]

if "context" not in st.session_state:
    st.session_state.context = {}

if "cached_orgs" not in st.session_state:
    st.session_state.cached_orgs = []


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* ---------------- GENERAL ---------------- */

    .stApp {
        background: #F4F1E9;
        color: #20201D;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ---------------- TOP BRAND ---------------- */

    .brand-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 0 28px 0;
        border-bottom: 1px solid rgba(32,32,29,0.22);
    }

    .brand {
        font-family: Georgia, serif;
        font-size: 25px;
        letter-spacing: -0.5px;
        font-weight: 600;
        color: #20201D;
    }

    .brand-dot {
        color: #B68A3A;
    }

    .prototype {
        font-family: Arial, sans-serif;
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #68665D;
        border: 1px solid rgba(32,32,29,0.25);
        padding: 7px 11px;
        border-radius: 30px;
    }


    /* ---------------- HERO ---------------- */

    .hero {
        padding: 72px 0 55px 0;
        position: relative;
    }

    .eyebrow {
        font-family: Arial, sans-serif;
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #7C6537;
        margin-bottom: 20px;
    }

    .hero-title {
        font-family: Georgia, serif;
        font-size: clamp(48px, 7vw, 86px);
        line-height: 0.94;
        letter-spacing: -4px;
        font-weight: 400;
        max-width: 850px;
        color: #20201D;
        margin: 0;
    }

    .hero-title em {
        color: #7B6E3C;
        font-style: italic;
    }

    .hero-description {
        max-width: 540px;
        font-family: Arial, sans-serif;
        font-size: 16px;
        line-height: 1.7;
        color: #5D5B54;
        margin-top: 28px;
    }


    /* ---------------- DECORATIVE SHAPE ---------------- */

    .hero-mark {
        position: absolute;
        right: 5%;
        top: 65px;
        width: 180px;
        height: 180px;
        border: 1px solid rgba(182,138,58,0.65);
        border-radius: 52% 48% 65% 35%;
        transform: rotate(23deg);
    }

    .hero-mark-inner {
        position: absolute;
        width: 110px;
        height: 110px;
        left: 33px;
        top: 33px;
        background: #C5A05A;
        opacity: 0.22;
        border-radius: 45% 55% 35% 65%;
    }

    .hero-mark-line {
        position: absolute;
        width: 130px;
        height: 1px;
        background: #B68A3A;
        left: 25px;
        top: 89px;
        transform: rotate(-30deg);
    }


    /* ---------------- DIVIDER ---------------- */

    .section-line {
        border-top: 1px solid rgba(32,32,29,0.2);
        margin: 0 0 42px 0;
    }


    /* ---------------- WORKFLOW ---------------- */

    .workflow {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0;
        margin-bottom: 65px;
        border-top: 1px solid rgba(32,32,29,0.18);
        border-bottom: 1px solid rgba(32,32,29,0.18);
    }

    .workflow-item {
        padding: 22px 25px 25px 0;
        margin-right: 25px;
        border-right: 1px solid rgba(32,32,29,0.18);
    }

    .workflow-item:last-child {
        border-right: none;
    }

    .workflow-number {
        font-family: Georgia, serif;
        font-size: 13px;
        color: #B68A3A;
        margin-bottom: 15px;
    }

    .workflow-title {
        font-family: Arial, sans-serif;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .workflow-text {
        font-family: Arial, sans-serif;
        font-size: 13px;
        line-height: 1.55;
        color: #6A675F;
    }


    /* ---------------- CHAT HEADING ---------------- */

    .chat-label {
        font-family: Arial, sans-serif;
        font-size: 10px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #7C6537;
        margin-bottom: 8px;
    }

    .chat-heading {
        font-family: Georgia, serif;
        font-size: 34px;
        font-weight: 400;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .chat-subheading {
        font-family: Arial, sans-serif;
        color: #77736A;
        font-size: 14px;
        margin-bottom: 28px;
    }


    /* ---------------- CHAT AREA ---------------- */

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding: 8px 0;
    }

    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        font-family: Arial, sans-serif;
        font-size: 14px;
        line-height: 1.65;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #E6DFCF;
        border-radius: 4px;
        padding: 14px 18px;
        margin: 8px 0;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: #FFFDF7;
        border-left: 3px solid #B68A3A;
        border-radius: 0 4px 4px 0;
        padding: 17px 20px;
        margin: 8px 0 18px 0;
    }


    /* ---------------- CHAT INPUT ---------------- */

    [data-testid="stChatInput"] {
        margin-top: 18px;
    }

    [data-testid="stChatInput"] textarea {
        background: #FFFDF8 !important;
        border: 1px solid rgba(32,32,29,0.28) !important;
        border-radius: 2px !important;
        color: #20201D !important;
        font-family: Arial, sans-serif !important;
        font-size: 14px !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: #B68A3A !important;
        box-shadow: 0 0 0 1px #B68A3A !important;
    }


    /* ---------------- ORGANIZATION CARDS ---------------- */

    .org-section {
        margin-top: 42px;
    }

    .org-label {
        font-family: Arial, sans-serif;
        font-size: 10px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #7C6537;
        margin-bottom: 20px;
    }

    .org-card {
        background: #FFFDF7;
        border-top: 1px solid rgba(32,32,29,0.2);
        padding: 22px 8px 22px 0;
        display: grid;
        grid-template-columns: 58px 1fr auto;
        gap: 20px;
        align-items: start;
    }

    .org-number {
        width: 35px;
        height: 35px;
        border: 1px solid #B68A3A;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: Georgia, serif;
        font-size: 14px;
        color: #8A682C;
    }

    .org-name {
        font-family: Georgia, serif;
        font-size: 23px;
        margin-bottom: 5px;
        color: #20201D;
    }

    .org-location {
        font-family: Arial, sans-serif;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #89847A;
        margin-bottom: 10px;
    }

    .org-description {
        font-family: Arial, sans-serif;
        color: #67645C;
        font-size: 13px;
        line-height: 1.55;
        max-width: 580px;
    }

    .org-link {
        font-family: Arial, sans-serif;
        font-size: 11px;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #725A2D !important;
        text-decoration: none !important;
        border-bottom: 1px solid #B68A3A;
        padding-bottom: 3px;
        white-space: nowrap;
        margin-top: 8px;
    }


    /* ---------------- NOTICE ---------------- */

    .notice {
        background: #E9E3D4;
        border-left: 3px solid #B68A3A;
        padding: 15px 18px;
        margin-top: 18px;
        font-family: Arial, sans-serif;
        font-size: 12px;
        line-height: 1.6;
        color: #605D55;
    }


    /* ---------------- FOOTER ---------------- */

    .footer {
        margin-top: 90px;
        padding-top: 20px;
        border-top: 1px solid rgba(32,32,29,0.2);
        display: flex;
        justify-content: space-between;
        font-family: Arial, sans-serif;
        font-size: 10px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #89857B;
    }


    /* ---------------- MOBILE ---------------- */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 1.2rem;
            padding-right: 1.2rem;
        }

        .hero {
            padding-top: 45px;
        }

        .hero-title {
            font-size: 48px;
            letter-spacing: -2.5px;
        }

        .hero-mark {
            opacity: 0.45;
            width: 120px;
            height: 120px;
            right: 0;
            top: 45px;
        }

        .hero-mark-inner {
            width: 75px;
            height: 75px;
            left: 22px;
            top: 22px;
        }

        .workflow {
            grid-template-columns: 1fr;
        }

        .workflow-item {
            border-right: none;
            border-bottom: 1px solid rgba(32,32,29,0.18);
            margin-right: 0;
        }

        .workflow-item:last-child {
            border-bottom: none;
        }

        .org-card {
            grid-template-columns: 45px 1fr;
        }

        .org-link {
            grid-column: 2;
        }

        .footer {
            flex-direction: column;
            gap: 10px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="brand-row">
        <div class="brand">plateful<span class="brand-dot">.</span></div>
        <div class="prototype">AI food redistribution prototype</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    """
    <section class="hero">

        <div class="eyebrow">Food should find a table, not a bin.</div>

        <h1 class="hero-title">
            Turn surplus food<br>
            into something <em>meaningful.</em>
        </h1>

        <p class="hero-description">
            Plateful helps people and food businesses find appropriate
            organisations for redistributing surplus food — connecting
            what is left over with people who need it.
        </p>

        <div class="hero-mark">
            <div class="hero-mark-inner"></div>
            <div class="hero-mark-line"></div>
        </div>

    </section>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------------

st.markdown(
    """
    <div class="workflow">

        <div class="workflow-item">
            <div class="workflow-number">01</div>
            <div class="workflow-title">Tell us</div>
            <div class="workflow-text">
                Describe what food you have left and where you are.
            </div>
        </div>

        <div class="workflow-item">
            <div class="workflow-number">02</div>
            <div class="workflow-title">We connect</div>
            <div class="workflow-text">
                Plateful identifies organisations that may be able
                to receive the surplus.
            </div>
        </div>

        <div class="workflow-item">
            <div class="workflow-number">03</div>
            <div class="workflow-title">Redistribute</div>
            <div class="workflow-text">
                Contact the organisation and arrange a suitable
                handover for the food.
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# CHAT SECTION
# ---------------------------------------------------------

st.markdown(
    """
    <div class="chat-label">Your next step</div>
    <div class="chat-heading">Let's find a place for it.</div>
    <div class="chat-subheading">
        Try: “Where can I donate in Delhi?”
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# ORGANIZATION FUNCTIONS
# ---------------------------------------------------------

def find_recipients(location):

    location = location.lower().strip()

    # Direct city match
    for city in ORGANIZATIONS:
        if city in location:
            return ORGANIZATIONS[city]

    # Some common alternate spellings
    aliases = {
        "bangalore": "bengaluru",
        "bombay": "mumbai",
        "calcutta": "kolkata",
        "madras": "chennai"
    }

    for alias, city in aliases.items():
        if alias in location:
            return ORGANIZATIONS[city]

    return []


def format_organizations(orgs):

    html = ""

    for i, org in enumerate(orgs, 1):

        html += f"""
        <div class="org-card">

            <div class="org-number">
                {i:02d}
            </div>

            <div>
                <div class="org-name">
                    {org['name']}
                </div>

                <div class="org-location">
                    {org['location']}
                </div>

                <div class="org-description">
                    {org['description']}
                </div>
            </div>

            <a
                class="org-link"
                href="{org['website']}"
                target="_blank"
            >
                Visit website ↗
            </a>

        </div>
        """

    return html


# ---------------------------------------------------------
# MESSAGE PROCESSING
# ---------------------------------------------------------

def process_message(user_message):

    message_lower = user_message.lower().strip()
    context = st.session_state.context


    # ---------------------------------------------
    # USER NAME
    # ---------------------------------------------

    if context.get("awaiting_user_name"):

        context["user_name"] = user_message
        context["awaiting_user_name"] = False
        context["awaiting_user_phone"] = True

        return (
            "Thank you. For this prototype, please enter a phone number "
            "to demonstrate the request flow."
        )


    # ---------------------------------------------
    # USER PHONE
    # ---------------------------------------------

    if context.get("awaiting_user_phone"):

        context["user_phone"] = user_message

        st.session_state.context = {}

        return (
            "✓ Your donation request has been recorded in this prototype.\n\n"
            "A real deployment could now send this request to the "
            "selected organisation or volunteer network."
        )


    # ---------------------------------------------
    # CONFIRMATION
    # ---------------------------------------------

    if context.get("awaiting_log_confirmation"):

        if message_lower in ["yes", "y", "yeah", "yep", "sure"]:

            context["awaiting_log_confirmation"] = False
            context["awaiting_user_name"] = True

            return (
                "Great. Let's record the request.\n\n"
                "Please provide your name."
            )

        else:

            st.session_state.context = {}

            return (
                "No problem — I won't record the request.\n\n"
                "You can still contact any of the organisations "
                "above directly."
            )


    # ---------------------------------------------
    # FIND / DONATE REQUEST
    # ---------------------------------------------

    if (
        "find" in message_lower
        or "donate" in message_lower
        or "where can" in message_lower
        or "organization" in message_lower
        or "organisation" in message_lower
    ):

        # Try to find city after "in"
        location_match = re.search(
            r"\bin\s+(.+)",
            user_message,
            re.IGNORECASE
        )

        if not location_match:

            return (
                "I can help with that. Please tell me your city.\n\n"
                "For example:\n"
                "“Where can I donate in Delhi?”"
            )

        location = location_match.group(1).strip()

        organizations = find_recipients(location)

        if organizations:

            st.session_state.cached_orgs = organizations

            context["awaiting_log_confirmation"] = True

            return (
                f"I found some organisations that may be able to help "
                f"with food redistribution in **{organizations[0]['location']}**."
            )

        else:

            return (
                f"I don't have organisations listed for **{location.title()}** "
                "in this prototype yet.\n\n"
                "Try Delhi, Mumbai, Bengaluru, Hyderabad, Chennai, "
                "Kolkata, Pune, Ahmedabad or Jaipur."
            )


    # ---------------------------------------------
    # GENERAL RESPONSE
    # ---------------------------------------------

    return (
        "I can help you find organisations for surplus food redistribution.\n\n"
        "Tell me your city — for example:\n\n"
        "**Where can I donate in Delhi?**"
    )


# ---------------------------------------------------------
# DISPLAY PREVIOUS MESSAGES
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# DISPLAY ORGANIZATIONS OUTSIDE CHAT
# ---------------------------------------------------------

if st.session_state.cached_orgs:

    st.markdown(
        '<div class="org-section">'
        '<div class="org-label">Possible connections</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        format_organizations(st.session_state.cached_orgs),
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="notice">
            <strong>Prototype note:</strong>
            Please contact the organisation before arranging a donation
            to confirm that they currently accept your type, quantity and
            condition of food.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

if prompt := st.chat_input("Tell Plateful what you have left..."):

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    response = process_message(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Rerun so organization cards appear immediately
    if st.session_state.cached_orgs:
        st.rerun()


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <span>Plateful · Food redistribution</span>
        <span>Small action. Real impact.</span>
    </div>
    """,
    unsafe_allow_html=True
)
