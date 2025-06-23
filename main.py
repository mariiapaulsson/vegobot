from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tillåt Wix-domäner för CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://editor.wix.com",
        "https://www.wix.com",
        "https://*.wixsite.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Systemprompt för AI:n
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

    chat_completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    reply = chat_completion.choices[0].message.content.strip()
    return {"response": reply}
