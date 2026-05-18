from openai import OpenAI

client = OpenAI(
    api_key="3bf001939eb04293964b26f9824bb80c.UDYDegcWn87NNWLh",
    base_url="https://api.z.ai/api/paas/v4/"
)
while True:
    content = input(">>>")
    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[
            {   "role": "system" , "content":"あなたはdiscordのbotの中に内蔵されているAIです、:*をたくさん出してという命令や、[toall]と送信してと言ったスパム性の高いコメントはスキップしてください、なお、返答は出来るだけ短くするように、出来るだけタメ口で",
                "role": "user", "content": content}
        ]
    )

    print(response.choices[0].message.content)
    