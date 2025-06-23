from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# 👇 CORS-inställning som funkar i både Wix-editor & publicerad sida
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://editor.wix.com",
        "https://www.wix.com",
        "https://*.wixsite.com"
    ],
    allow_origin_regex=r"https://.*\.wixsite\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    user_message = data.get("message")

    if not user_message:
        return {"response": "Jag fick inget meddelande att svara på."}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # eller gpt-4 om du har tillgång
            messages=[
                {"role": "system", "content": "Du är en hjälpsam vego-assistent som ger smarta mattips till köttälskare."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        gpt_response = response.choices[0].message.content.strip()
        return {"response": gpt_response}

    except Exception as e:
        return {"response": f"Något gick fel: {str(e)}"}
