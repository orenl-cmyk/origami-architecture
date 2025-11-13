import streamlit as st
import requests
import json

def get_entities_list(base_url, username, api_secret):
    url = f"https://{base_url}.origami.ms/entities/api/entities_list/format/json"
    payload = {"username": username, "api_secret": api_secret}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json().get("entities_list", [])

def get_entity_structure(base_url, username, api_secret, entity_name):
    url = f"https://{base_url}.origami.ms/entities/api/entity_structure/format/json"
    payload = {
        "username": username,
        "api_secret": api_secret,
        "entity_data_name": entity_name
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

st.set_page_config(page_title="Origami Exporter", layout="centered")

st.title("📦 Origami Architecture Exporter")
st.markdown("הזן את פרטי הגישה שלך למערכת Origami וקבל קובץ JSON עם כל הארכיטקטורה של הישויות במערכת שלך.")

with st.form("input_form"):
    base_url = st.text_input("🌍 שם הסביבה (ללא https://)", placeholder="example אם הקישור הוא https://example.origami.ms")
    username = st.text_input("👤 שם משתמש במערכת")
    api_secret = st.text_input("🔐 API Secret", type="password")
    submitted = st.form_submit_button("📤 הפק JSON")

if submitted:
    if not base_url or not username or not api_secret:
        st.warning("אנא מלא את כל השדות.")
    else:
        try:
            with st.spinner("🔍 מייבא ישויות..."):
                entities = get_entities_list(base_url, username, api_secret)
                all_data = {}
            for entity_name in entities:
                if isinstance(entity_name, str):
                    all_data[entity_name] = get_entity_structure(base_url, username, api_secret, entity_name)

            json_str = json.dumps(all_data, indent=2, ensure_ascii=False)
            st.success("✅ ייצוא הושלם!")
            st.download_button("⬇️ הורד את הקובץ", json_str, file_name="full_architecture.json", mime="application/json")

        except Exception as e:
            st.error(f"❌ שגיאה: {e}")
