import streamlit as st
import re
import time

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(page_title="Plateful", page_icon="🍽️")
st.title("🍽️ Plateful - Food Distribution Agent")
st.caption("Helping surplus food find a useful destination.")

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = {}

if "cached_orgs" not in st.session_state:
    st.session_state.cached_orgs = []


# ---------------------------------------------------------
# PROTOTYPE ORGANIZATION DIRECTORY
# ---------------------------------------------------------
# This replaces the Google Maps API.
# The directory can be expanded later.

ORGANIZATIONS = {
    "delhi": [
        {
            "name": "Robin Hood Army",
            "address": "Delhi",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Delhi",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        },
        {
            "name": "No Food Waste",
            "address": "Delhi NCR",
            "phone": "Contact through official website",
            "website": "https://nofoodwaste.org/"
        }
    ],

    "mumbai": [
        {
            "name": "Robin Hood Army",
            "address": "Mumbai",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Mumbai",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        },
        {
            "name": "No Food Waste",
            "address": "Mumbai",
            "phone": "Contact through official website",
            "website": "https://nofoodwaste.org/"
        }
    ],

    "bengaluru": [
        {
            "name": "Robin Hood Army",
            "address": "Bengaluru",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Bengaluru",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "bangalore": [
        {
            "name": "Robin Hood Army",
            "address": "Bengaluru",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Bengaluru",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "hyderabad": [
        {
            "name": "Robin Hood Army",
            "address": "Hyderabad",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Hyderabad",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "chennai": [
        {
            "name": "Robin Hood Army",
            "address": "Chennai",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Chennai",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "kolkata": [
        {
            "name": "Robin Hood Army",
            "address": "Kolkata",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Kolkata",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "pune": [
        {
            "name": "Robin Hood Army",
            "address": "Pune",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Pune",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "ahmedabad": [
        {
            "name": "Robin Hood Army",
            "address": "Ahmedabad",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Ahmedabad",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ],

    "jaipur": [
        {
            "name": "Robin Hood Army",
            "address": "Jaipur",
            "phone": "Contact through official website",
            "website": "https://robinhoodarmy.com/"
        },
        {
            "name": "Feeding India",
            "address": "Jaipur",
            "phone": "Contact through official website",
            "website": "https://www.feedingindia.org/"
        }
    ]
}


# ---------------------------------------------------------
# FIND ORGANIZATIONS
# ---------------------------------------------------------

def find_recipients(location: str):
    """Find organizations from the prototype directory."""

    location_lower = location.lower().strip()

    # Try exact city first
    if location_lower in ORGANIZATIONS:
        return {"recipients": ORGANIZATIONS[location_lower]}

    # Handle common variations
    city_aliases = {
        "new delhi": "delhi",
        "delhi ncr": "delhi",
        "bombay": "mumbai",
        "bengaluru city": "bengaluru",
        "bangalore city": "bengaluru",
        "madras": "chennai"
    }

    if location_lower in city_aliases:
        city = city_aliases[location_lower]
        return {"recipients": ORGANIZATIONS[city]}

    # Try to find a supported city inside a longer location
    for city in ORGANIZATIONS:
        if city in location_lower:
            return {"recipients": ORGANIZATIONS[city]}

    return {
        "message": (
            "I don't currently have organizations listed for that city. "
            "Try Delhi, Mumbai, Bengaluru, Hyderabad, Chennai, Kolkata, "
            "Pune, Ahmedabad, or Jaipur."
        )
    }


# ---------------------------------------------------------
# LOG DONATION REQUEST
# ---------------------------------------------------------

def log_donation_request(user_name, user_phone, organizations):
    """
    Prototype logging system.

    This version does not require Google Sheets.
    """

    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Store the latest request in Streamlit session state.
        st.session_state.last_donation = {
            "donor_name": user_name,
            "donor_phone": user_phone,
            "organizations": organizations,
            "timestamp": timestamp
        }

        return {
            "success": True,
            "message": "Request recorded successfully!"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ---------------------------------------------------------
# FORMAT ORGANIZATIONS
# ---------------------------------------------------------

def format_organizations(orgs_data):

    response = ""

    for i, org in enumerate(orgs_data, 1):

        response += f"**{i}. {org['name']}**\n\n"

        response += (
            f"- **Location:** {org.get('address', 'N/A')}\n\n"
        )

        response += (
            f"- **Phone:** {org.get('phone', 'Not available')}\n\n"
        )

        response += (
            f"- **Website:** {org.get('website', 'Not available')}\n\n"
        )

    return response


# ---------------------------------------------------------
# MAIN CHAT LOGIC
# ---------------------------------------------------------

def process_message(user_message):

    message_lower = user_message.lower().strip()
    context = st.session_state.context

    # -----------------------------------------
    # USER NAME
    # -----------------------------------------

    if context.get("awaiting_user_name"):

        context["user_name"] = user_message
        context["awaiting_user_name"] = False
        context["awaiting_user_phone"] = True

        return "Thank you! Now, what is your phone number?"


    # -----------------------------------------
    # USER PHONE
    # -----------------------------------------

    if context.get("awaiting_user_phone"):

        context["user_phone"] = user_message

        with st.spinner("Recording your donation request..."):

            log_result = log_donation_request(
                context.get("user_name"),
                context.get("user_phone"),
                st.session_state.cached_orgs
            )

        st.session_state.context = {}

        if log_result.get("success"):
            return f"✅ {log_result['message']}"

        return f"❌ Error: {log_result.get('error', 'Unknown error')}"


    # -----------------------------------------
    # LOG CONFIRMATION
    # -----------------------------------------

    if context.get("awaiting_log_confirmation"):

        if message_lower in ["yes", "y", "yeah", "sure"]:

            context["awaiting_log_confirmation"] = False
            context["awaiting_user_name"] = True

            return "Great! To proceed, please provide your name."

        elif message_lower in ["no", "n", "nope"]:

            st.session_state.context = {}

            return (
                "Okay, I won't record the request. "
                "Is there anything else I can help you with?"
            )

        else:

            return "Please reply with **yes** or **no**."


    # -----------------------------------------
    # DONATION SEARCH
    # -----------------------------------------

    if (
        "find" in message_lower
        or "donate" in message_lower
        or "where can" in message_lower
        or "food bank" in message_lower
        or "ngo" in message_lower
        or "organization" in message_lower
    ):

        # Try to extract location after "in"
        location_match = re.search(
            r"\bin\s+(.+)",
            user_message,
            re.IGNORECASE
        )

        if not location_match:

            return (
                "I can help you find food donation organizations! "
                "Please tell me your city, for example: "
                "**Where can I donate in Delhi?**"
            )

        location = location_match.group(1).strip()

        with st.spinner(f"Searching organizations in {location}..."):

            result_data = find_recipients(location)

        if (
            "recipients" in result_data
            and result_data["recipients"]
        ):

            st.session_state.cached_orgs = result_data["recipients"]

            response = (
                f"I found these organizations in **{location.title()}**:\n\n"
            )

            response += format_organizations(
                st.session_state.cached_orgs
            )

            response += (
                "\n\n"
                "⚠️ **Prototype note:** Please contact the organization "
                "before arranging a food donation to confirm that they "
                "accept your type and quantity of food.\n\n"
            )

            response += (
                "**Would you like me to record this donation request? "
                "(yes/no)**"
            )

            context["awaiting_log_confirmation"] = True

            return response

        else:

            return (
                f"Sorry, I couldn't find organizations listed for "
                f"**{location.title()}**.\n\n"
                f"{result_data.get('message', '')}"
            )


    # -----------------------------------------
    # DEFAULT RESPONSE
    # -----------------------------------------

    return (
        "I can help you find food donation organizations. "
        "Try something like:\n\n"
        "**Where can I donate in Delhi?**\n\n"
        "or\n\n"
        "**Find food donation centers in Mumbai.**"
    )


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# HANDLE NEW MESSAGE
# ---------------------------------------------------------

if prompt := st.chat_input("How can I help?"):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        response = process_message(prompt)

        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
