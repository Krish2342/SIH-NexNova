from google import genai

from app.config import GEMINI_API_KEY


def main():
    client = genai.Client(api_key=GEMINI_API_KEY)

    print("\n--- AVAILABLE GEMINI MODELS ---\n")

    for model in client.models.list():
        print("NAME:", model.name)
        print("DISPLAY:", model.display_name)
        print("DESCRIPTION:", model.description)
        print("ACTIONS:", model.supported_actions)
        print("-" * 60)


if __name__ == "__main__":
    main()