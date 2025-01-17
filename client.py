from openai import OpenAI

# client = OpenAI()
client = OpenAI(api_key="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")


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful virtual assistant name jarvis."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.content)