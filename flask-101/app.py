from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'tools.db'

# --- สร้างฐานข้อมูลถ้ายังไม่มี ---
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            no TEXT,
            doc_no TEXT,
            date TEXT,
            item_code TEXT,
            description TEXT,
            customer TEXT,
            process TEXT,
            size TEXT,
            part_weight TEXT,
            material TEXT,
            material_name TEXT,
            mat_use TEXT,
            master_batch TEXT,
            masterbatch_name TEXT,
            masterBatch_use TEXT,
            color TEXT,
            sm TEXT,
            handle TEXT,
            bag TEXT,
            packing_detail TEXT,
            label TEXT,
            insert_logo TEXT,
            carton_box TEXT,
            eco TEXT,
            remark TEXT
        )''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tools")
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        values = tuple(request.form.get(field) for field in [
            'no', 'doc_no', 'date', 'item_code', 'description', 'customer', 'process',
            'size', 'part_weight', 'material', 'material_name', 'mat_use',
            'master_batch', 'masterbatch_name', 'masterBatch_use', 'color', 'sm',
            'handle', 'bag', 'packing_detail', 'label', 'insert_logo',
            'carton_box', 'eco', 'remark'
        ])
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''INSERT INTO tools (
            no, doc_no, date, item_code, description, customer, process,
            size, part_weight, material, material_name, mat_use, master_batch,
            masterbatch_name, masterBatch_use, color, sm, handle, bag, packing_detail,
            label, insert_logo, carton_box, eco, remark
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', values)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if request.method == 'POST':
        values = tuple(request.form.get(field) for field in [
            'no', 'doc_no', 'date', 'item_code', 'description', 'customer', 'process',
            'size', 'part_weight', 'material', 'material_name', 'mat_use',
            'master_batch', 'masterbatch_name', 'masterBatch_use', 'color', 'sm',
            'handle', 'bag', 'packing_detail', 'label', 'insert_logo',
            'carton_box', 'eco', 'remark'
        ]) + (id,)
        c.execute('''UPDATE tools SET
            no=?, doc_no=?, date=?, item_code=?, description=?, customer=?, process=?,
            size=?, part_weight=?, material=?, material_name=?, mat_use=?, master_batch=?,
            masterbatch_name=?, masterBatch_use=?, color=?, sm=?, handle=?, bag=?, packing_detail=?,
            label=?, insert_logo=?, carton_box=?, eco=?, remark=? WHERE id=?''', values)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    c.execute("SELECT * FROM tools WHERE id=?", (id,))
    data = c.fetchone()
    conn.close()
    return render_template('edit.html', data=data)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tools WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
