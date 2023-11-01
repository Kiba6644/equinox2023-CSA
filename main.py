from flask import Flask, render_template, request
from flask_socketio import SocketIO
import random
import requests

#You snoopy lil human, hope you enjoyed the event!
#im aware i could have used one navbar.html instead of copy pasting that already-a mess code into every file
#if youre wondering why i left the front end such a mess, we live by "if it works, dont touch it"
#jk i tried but the fest is tomorrow and theres so much stuff left to do

app = Flask(__name__)
socketio = SocketIO(app)
links = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1NKFfI96wsI9WiY04whEG-cj0f0Li4dcvPg&usqp=CAU", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdVcpZH0706teE-1pKHzQdzmxoL7Pk2vHVqA&usqp=CAU", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_6nYiPh4ErkbxEZPXnNvX6CzWUOng5i8qqw&usqp=CAU", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9DO6v-lX4ktUrIXRN9gPJzvNkxmhn72HPwqNmyQNbGslDDg4CK0m8IThHMZI4Y9djiLk&usqp=CAU", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwJs_gGKHGAjep2l4PY2GJSsn8DcncDPQD5w&usqp=CAU", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTunugGSSL_AGJYuZdbOer_UexBSInFdYrcYA&usqp=CAU"]
pfps = {}
bot_payload = {
    'sender': "Cool_Dude",
    'message': '',
    'pfp': "https://flipanim.com/gif/m/j/mjY6el7N.gif"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/about_us')
def abt_us():
    return render_template('abt.html')

@app.route('/score')
def score():
    return render_template('score.html')

@socketio.on('message')
def handle_message(msg):
    print('Message:', msg)
    if msg["isAnonymous"] == True:
        message_payload = {
            'sender': "Team-X",
            'message': msg["message"],
            'pfp': pfp(msg["teamCode"])
        }
    else:
        message_payload = {
            'sender': f'Team {msg["teamCode"]}',
            'message': msg["message"],
            'pfp': pfp(msg["teamCode"])
        }
        socketio.emit('message', message_payload)

    if msg["message"].startswith('!code-joke'):
        bot_payload['message'] = get_joke()
        socketio.emit('message', bot_payload)

    if msg["message"].startswith('!compliment'):
        bot_payload['message'] = get_compliment()
        socketio.emit('message', bot_payload)
    
    if msg["message"].startswith('!wyr'):
        bot_payload['message'] = get_wyr()
        socketio.emit('message', bot_payload)
    
    if msg["message"].startswith('!nhe'):
        bot_payload['message'] = get_nhe()
        socketio.emit('message', bot_payload)
    
    if msg["message"].startswith('!story'):
        bot_payload['message'] = get_story()
        socketio.emit('message', bot_payload)

def pfp(teamcode):
    if pfps.get(teamcode) != None:
        return pfps[teamcode]
    else:
        if len(pfps) < 5:
            rand = links[random.randint(0,5)]
            while rand not in pfps.values():
                pfps[teamcode] = rand
                return pfps[teamcode]
        else:
            pfps[teamcode] = links[random.randint(0,4)]
            return pfps[teamcode]

def get_joke():
    api_url = "https://backend-omega-seven.vercel.app/api/getjoke"
    
    try:
        response = requests.get(api_url)
        data = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            joke_data = data[0]
            question = joke_data.get("question", "")
            punchline = joke_data.get("punchline", "")
            
            if question and punchline:
                return f"{question}\n\n{punchline}"

    except Exception as e:
        print(f"Error fetching joke: {e}")

    return "Failed to fetch a joke."

def get_compliment():
    api_url = "https://8768zwfurd.execute-api.us-east-1.amazonaws.com/v1/compliments"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        compliment = response.json()
        return compliment

    except requests.exceptions.RequestException as e:
        return f"Sorry, I couldn't fetch a compliment. Error: {e}"
    
def get_wyr():
    try:
        api_url = "https://would-you-rather-api.abaanshanid.repl.co"
        
        response = requests.get(api_url)
        data = response.json()

        if "data" in data:
            return data["data"]
        else:
            return "Sorry, couldn't fetch a question right now. Try again later."

    except Exception as e:
        return "An error occurred while fetching the question."

def get_nhe():
    try:
        api_url = "https://api.nhie.io/v2/statements/next"
        
        response = requests.get(api_url)
        data = response.json()

        if "statement" in data:
            return data["statement"]
        else:
            return "Sorry, couldn't fetch a question right now. Try again later."

    except Exception as e:
        return "An error occurred while fetching the question."

def get_story():
    api_url = "https://writingexercises.co.uk/php_WE/firstline.php?"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as e:
        return f"Sorry, I couldn't fetch a story. Error: {e}"

if __name__ == '__main__':
    socketio.run(app, debug=True)
