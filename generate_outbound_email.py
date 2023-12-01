from openai import AsyncOpenAI
print('openai api key:', os.environ.get("OPENAI_API_KEY"))

client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Given text, generates an outbound email for people to use.
async def generate_email(title, meta_description, my_details):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                    Website Title: {title}
                    Website Description: {meta_description}

                    My Details: {my_details}

                    ==========================================================

                    Generate a short and attention grabbing email for this website's owner to encourage them to use my website development services.
                    
                    Format it as:
                    Subject: {{email subject}}
                    Content: {{email content}}
                """
            }
        ],
        model="gpt-4-1106-preview"
    )
    
    print('chat_completion:', chat_completion)
    return chat_completion.choices[0].message.content
    
