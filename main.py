import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

telefonlar = []
id_counter = 1

# Papka yo'q bo'lsa yaratadi
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def index():
    return render_template("index.html", telefonlar=telefonlar)


@app.route("/create-phone", methods=["GET", "POST"])
def create_phone():
    global id_counter

    if request.method == "POST":
        nomi = request.form['nomi']
        narxi = request.form['narxi']
        soni = request.form['soni']
        malumot = request.form['malumot']

        rasm_file = request.files['rasm']

        if rasm_file and rasm_file.filename != '':
            filename = secure_filename(rasm_file.filename)
            rasm_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            rasm_file.save(rasm_path)
        else:
            rasm_path = "static/uploads/default.png"

        telefon = {
            "id": id_counter,
            "nomi": nomi,
            "narxi": narxi,
            "soni": soni,
            "malumot": malumot,
            "rasm": rasm_path
        }

        telefonlar.append(telefon)
        id_counter += 1

        return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/edit-phone/<int:tel_id>", methods=["GET", "POST"])
def edit_phone(tel_id):
    telefon = next((t for t in telefonlar if t['id'] == tel_id), None)

    if not telefon:
        return "Telefon topilmadi!"

    if request.method == "POST":
        telefon['nomi'] = request.form['nomi']
        telefon['narxi'] = request.form['narxi']
        telefon['soni'] = request.form['soni']
        telefon['malumot'] = request.form['malumot']

        rasm_file = request.files['rasm']

        if rasm_file and rasm_file.filename != '':
            filename = secure_filename(rasm_file.filename)
            rasm_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            rasm_file.save(rasm_path)
            telefon['rasm'] = rasm_path

        return redirect(url_for("index"))

    return render_template("edit.html", telefon=telefon)


@app.route("/delete-phone/<int:tel_id>")
def delete_phone(tel_id):
    global telefonlar
    telefonlar = [t for t in telefonlar if t['id'] != tel_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
