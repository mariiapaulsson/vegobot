from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/ask-chat', methods=['POST'])
def ask_chat():
    data = request.get_json()
    user_message = data.get("message", "")
    print("Användarens fråga:", user_message)

    # Här kan du lägga till logik med OpenAI eller andra receptfunktioner
    if "tomat" in user_message.lower():
        response = "Här är ett recept med tomat: Tomatsoppa med basilika!"
    else:
        response = f"Jag hörde att du skrev: {user_message}"

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
