from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Tillåt alla domäner (justera för produktion)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ladda din OpenAI-nyckel från miljövariabler
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "Du är en vänlig och kunnig vegoassistent. Du hjälper användare att laga växtbaserad mat som känns rejäl, smakrik och 'köttig' – perfekt för köttälskare. "
    "När någon skriver vad de har hemma, föreslår du recept (helst enkla). Ge gärna ett extra tips eller smakförklaring. "
    "Du svarar tydligt men avslappnat. Prata som en kompis som gillar att laga mat. Förklara varför något är gott om det behövs. "
    "Du kan ge recept, byta ut ingredienser och anpassa efter situationer (barn, gäster, snabbt, lyxigt etc)."
)

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    if not user_input:
        return {"response": "Vad vill du veta om vegomat?"}

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response.choices[0].message.content.strip()
    return {"response": reply}
