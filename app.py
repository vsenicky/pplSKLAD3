from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('warehouse.db')
    conn.row_factory = sqlite3.Row
    return conn

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Přidání zásilky
@app.route('/add', methods=['POST'])
def add():
    last_digits = request.form['last_digits']
    shelf = request.form['shelf']
    note = request.form.get('note', '')  # Defaultní hodnota pro poznámku je prázdná
    conn = get_db_connection()
    conn.execute('INSERT INTO parcels (last_digits, shelf, note) VALUES (?, ?, ?)', (last_digits, shelf, note))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Vyhledání zásilky
@app.route('/search', methods=['POST'])
def search():
    last_digits = request.form['search_digits']
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM parcels WHERE last_digits = ?', (last_digits,)).fetchall()
    conn.close()
    return render_template('search_result.html', result=result)

# Zobrazení celého skladu
@app.route('/view')
def view():
    conn = get_db_connection()
    parcels = conn.execute('SELECT * FROM parcels').fetchall()
    conn.close()
    
    shelves = {str(i): [] for i in range(1, 6)}
    for item in parcels:
        shelves[item['shelf']].append(item)
    return render_template('view.html', shelves=shelves)

# Smazání zásilky
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM parcels WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
