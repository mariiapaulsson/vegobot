from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tillåt Wix för testning
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    user_message = data.get("message")

    if not user_message:
        return {"response": "Inget meddelande mottaget."}

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en hjälpsam vego-assistent som ger mattips till köttälskare."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        gpt_response = response.choices[0].message.content.strip()
        return {"response": gpt_response}

    except Exception as e:
        return {"response": f"Något gick fel: {str(e)}"}
