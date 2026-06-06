from google import genai
from google.genai import types

client = genai.Client(api_key="")

SYSTEM_PROMPT = "短く答えて"
history = []

while True:
    try:
        content = input(">>> ")
        history.append(types.Content(role="user", parts=[types.Part(text=content)]))

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=128,
                temperature=0.3,
            ),
            contents=history,
        )

        reply = response.text
        history.append(types.Content(role="model", parts=[types.Part(text=reply)]))

        print(reply)

    except KeyboardInterrupt:
        print("\n終了します")
        break
    except Exception as e:
        print(f"エラーが発生しました: {e}")