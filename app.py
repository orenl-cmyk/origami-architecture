import streamlit as st
import requests
import json

st.set_page_config(page_title="Origami Architecture Exporter", layout="centered")

# -----------------------------
# API FUNCTIONS
# -----------------------------

def get_entities_list(env_name, username, api_secret):
    """
    Fetch entities list from Origami.
    Supports both response formats:
    1) {"entities_list": [...]}
    2) [ {...}, {...} ]
    """
    url = f"https://{env_name}.origami.ms/entities/api/entities_list/format/json"
    payload = {"username": username, "api_secret": api_secret}

    res = requests.post(url, json=payload)
    res.raise_for_status()
    data = res.json()

    # Case A: correct documented format
    if isinstance(data, dict) and "entities_list" in data:
        return [obj.get("entity_data_name") for obj in data["entities_list"]]

    # Case B: API returns list of entity objects directly
    if isinstance(data, list):
        return [obj.get("entity_data_name") for obj in data if isinstance(obj, dict)]

    # Anything else = unexpected response
    raise Exception("Unexpected API response format: " + str(data))


def get_entity_structure(env_name, username, api_secret, entity_name):
    """
    Fetch the full structure of a single entity.
    """
    url = f"https://{env_name}.origami.ms/entities/api/entity_structure/format/json"
    payload = {
        "username": username,
        "api_secret": api_secret,
        "entity_data_name": entity_name
    }
    res = requests.post(url, json=payload)
    res.raise_for_status()
    return res.json()


# -----------------------------
# STREAMLIT UI
# -----------------------------

st.title("📦 Origami Architecture Exporter")
st.markdown("הזן את פרטי הגישה שלך וקבל קובץ JSON עם כל הארכיטקטורה של הישויות במערכת Origami שלך.")

with st.form("input_form"):
    env_name = st.text_input("🌍 שם הסביבה (ללא https://)", placeholder="example")
    username = st.text_input("👤 שם משתמש במערכת")
    api_secret = st.text_input("🔐 API Secret", type="password")
    submitted = st.form_submit_button("📤 הפק JSON")

if submitted:
    if not env_name or not username or not api_secret:
        st.warning("⚠️ יש למלא את כל השדות.")
    else:
        try:
            st.info("⏳ מביא רשימת ישויות…")
            entities = get_entities_list(env_name, username, api_secret)

            all_data = {}
            progress = st.progress(0)
            total = len(entities)

            for idx, entity_name in enumerate(entities):
                if not entity_name:
                    continue

                st.write(f"📥 טוען ישות: `{entity_name}`")
                structure = get_entity_structure(env_name, username, api_secret, entity_name)
                all_data[entity_name] = structure

                progress.progress((idx + 1)/total)

            json_str = json.dumps(all_data, indent=2, ensure_ascii=False)

            st.success("🎉 ייצוא הושלם בהצלחה!")
            st.download_button(
                "⬇️ הורד את הקובץ",
                json_str,
                file_name="full_architecture.json",
                mime="application/json"
            )

        except requests.exceptions.RequestException as e:
            st.error(f"❌ שגיאת תקשורת: {e}")

        except Exception as e:
            st.error(f"❌ שגיאה: {e}")
