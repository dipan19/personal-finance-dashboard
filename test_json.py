import json

try:
    with open("portfolio_config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        print("✅ JSON loaded successfully!")
        print(json.dumps(data, indent=2))
except json.JSONDecodeError as e:
    print("❌ JSON Decode Error:", e)
except Exception as e:
    print("❌ Some other error:", e)