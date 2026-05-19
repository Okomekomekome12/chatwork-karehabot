from openai import OpenAI

client = OpenAI(
    api_key="3bf001939eb04293964b26f9824bb80c.UDYDegcWn87NNWLh",
    base_url="https://api.z.ai/api/paas/v4/"
)

SYSTEM_PROMPT = "短く答えて"
history = []


while True:
    try:
        content = input(">>> ")
        history.append({"role": "user", "content": content})

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

        response = client.chat.completions.create(
            model="glm-4.5-flash",
            messages=messages, # type: ignore
            max_tokens=128,
            temperature=0.3,
            extra_body={
                "thinking": {
                    "type": "disabled"
                }
            }
        )

        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})

        print(reply)

    except KeyboardInterrupt:
        print("\nチャットを終了します。")
        break
    except Exception as e:
        print(f"エラーが発生しました: {e}")