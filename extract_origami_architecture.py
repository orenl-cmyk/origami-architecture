import requests
import json

def get_entities_list(base_url, username, api_secret):
    url = f"{base_url}/entities/api/entities_list/format/json"
    payload = {
        "username": username,
        "api_secret": api_secret
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json().get("entities_list", [])

def get_entity_structure(base_url, username, api_secret, entity_data_name):
    url = f"{base_url}/entities/api/entity_structure/format/json"
    payload = {
        "username": username,
        "api_secret": api_secret,
        "entity_data_name": entity_data_name
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    print("🔧 Origami Architecture Export Tool")
    env_name = input("Enter your Origami environment name (e.g., mycompany): ").strip()
    username = input("Enter your Origami username: ").strip()
    api_secret = input("Enter your Origami API secret: ").strip()

    base_url = f"https://{env_name}.origami.ms"
    print(f"📡 Connecting to {base_url}...")

    try:
        entities = get_entities_list(base_url, username, api_secret)
        print(f"✅ Found {len(entities)} entities.")
    except Exception as e:
        print(f"❌ Failed to fetch entity list: {e}")
        return

    full_structure = {}

    for entity in entities:
        entity_name = entity.get("entity_data_name")
        if not entity_name:
            continue
        print(f"📥 Fetching structure for entity: {entity_name}")
        try:
            structure = get_entity_structure(base_url, username, api_secret, entity_name)
            full_structure[entity_name] = structure
        except Exception as e:
            print(f"⚠️ Failed to fetch structure for {entity_name}: {e}")

    output_filename = "full_architecture.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(full_structure, f, indent=2, ensure_ascii=False)

    print(f"✅ Architecture export complete. Output saved to '{output_filename}'.")

if __name__ == "__main__":
    main()
