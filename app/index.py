from app.onMessage import *
from flask import jsonify, request, Blueprint
from threading import Thread
from .dialogue import load_dialogues, save_dialogues
import json
import os

chatbot = Blueprint('chatbot', __name__)

bot_threads = {}  # Diccionario para almacenar los hilos de los bots
bot_running = {}  # Diccionario para indicar si cada bot está en ejecución
listen_threads = {}  # Diccionario para almacenar los hilos de escucha de los bots
clients = {}  # Diccionario para almacenar los objetos de cliente de cada bot
error_messages = {}  # Diccionario para almacenar los mensajes de error de cada bot
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"

#COMENTARIO

def start_bot(email, password):
    global bot_threads, listen_threads, bot_running, clients, error_messages
    try:
        
        # Guardar el email
        existing_dialogues = load_dialogues(email)
        if not existing_dialogues:
            save_dialogues([{"id": 1, "input": "Hola", "output": "En que puedo ayudarte?"}], email)

        # Cargar session_cookies si existen
        session_cookies = load_session_cookies(email)
        if session_cookies:
            print("Si Existen")
            client = MarketBot(email, password, user_agent=ua, session_cookies=session_cookies,)
        else:
            # No se encontraron cookies guardadas, iniciar sesión y guardar las session_cookies
            print("No existen")
            client = MarketBot(email, password, user_agent=ua, session_cookies=None)
            session_cookies = client.getSession()
            save_session_cookies(session_cookies, email)
            
        #client = MarketBot(email, password)
        client.dialogues = load_dialogues(email)
        clients[email] = client
        bot_running[email] = True

        # Se agrega este proceso en segundo plano
        listen_threads[email] = Thread(target=client.listen)
        listen_threads[email].start()

    except Exception as e:
        error_messages[email] = str(e)
        bot_running[email] = False

@chatbot.route('/start-bot', methods=['POST'])
def start_bot_endpoint():
    global bot_threads, bot_running, clients, error_messages
    data = request.get_json()  # Obtener los datos en formato JSON de la solicitud
    email = data.get('email')  # Obtener el valor de 'email' del JSON
    password = data.get('password')  # Obtener el valor de 'password' del JSON

    if email in bot_running and bot_running[email]:
        return jsonify({'message': 'El bot ya está en ejecución para este cliente'}), 200

    bot_threads[email] = Thread(target=start_bot, args=(email, password))  # Pasar los datos a la función start_bot
    bot_threads[email].start()
    bot_threads[email].join()  # Esperar a que el hilo del bot se complete

    if email in clients and clients[email].isLoggedIn():
        
        return jsonify({'message': f'Bot iniciado para el: {email}'}), 200
    else:
        return jsonify({'message': f'Error al iniciar el bot: {error_messages.get(email, "")}'}), 500
    
@chatbot.route('/stop-bot', methods=['POST'])
def stop_bot_endpoint():
    global bot_threads, bot_running, clients
    data = request.get_json()  # Obtener los datos en formato JSON de la solicitud
    email = data.get('email')  # Obtener el valor de 'email' del JSON

    if email not in bot_running or not bot_running[email]:
        return jsonify({'message': 'El bot no está en ejecución para este cliente'}), 200

    clients[email].stopListening()  # Detener la escucha del bot de manera controlada
    bot_running[email] = False
    return jsonify({'message': 'Deteniendo el bot de manera controlada'}), 200

def save_session_cookies(session_cookies, email):
    folder_path = "client_cookies"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{email}_session_cookies.json")
    with open(file_path, "w") as file:
        json.dump(session_cookies, file)

def load_session_cookies(email):
    folder_path = "client_cookies"
    file_path = os.path.join(folder_path, f"{email}_session_cookies.json")
    try:
        with open(file_path, "r") as file:
            session_cookies = json.load(file)
            return session_cookies
    except FileNotFoundError:
        return None
    
@chatbot.route('/user-lives', methods=['GET'])
def obtener_usuarios_activos():
    global bot_running
    usuarios_activos = [usuario for usuario, estado in bot_running.items() if estado]
    return jsonify({'usuarios_activos': usuarios_activos}), 200