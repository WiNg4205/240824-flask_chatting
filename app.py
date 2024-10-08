from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sqlite3
from datetime import datetime


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
    conn.close()

@app.route('/')
def chat():
    conn = sqlite3.connect(DATA_FILE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM messages')
    data = cur.fetchall()
    
    messages = [msg[0] for msg in data]
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handle_message(msg):
    conn = sqlite3.connect(DATA_FILE)
    cur = conn.cursor()
    
    now = datetime.now()
    dt_str = now.strftime('%Y-%m-%d %H:%M:%S')
    msg = f"({dt_str}) {msg}"
    cur.execute('INSERT INTO messages (message) VALUES (?)', (msg,))
    conn.commit()
    print(msg)

    cur.execute('SELECT * FROM messages')
    data = cur.fetchall()
    conn.close()
    
    emit('message', data, broadcast=True)
    
@socketio.on('clear')
def handle_clear():
    conn = sqlite3.connect(DATA_FILE)
    cur = conn.cursor()
    cur.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    
    emit('clear', broadcast=True)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
