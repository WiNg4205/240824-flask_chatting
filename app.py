from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

DATA_FILE = 'messages.db'

def init_db():
    conn = sqlite3.connect(DATA_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            message TEXT
        )
    ''')

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/chat')
def chat():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    conn = sqlite3.connect(DATA_FILE)
    cur = conn.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (?)', (msg,))
    conn.commit()

    cur.execute('SELECT * FROM messages')
    data = cur.fetchall()
    print(data)
    
    emit('message', data, broadcast=True)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
