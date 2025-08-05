from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

DB_URL = os.getenv("DATABASE_URL")  # Railway la crea automáticamente

def get_db_connection():
    return psycopg2.connect(DB_URL, sslmode='require')

@app.route("/")
def index():
    return redirect(url_for("registro_medico"))

@app.route("/registro_medico", methods=["GET", "POST"])
def registro_medico():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        dni = request.form["dni"]
        matricula = request.form["matricula"]
        profesion = request.form["profesion"]
        direccion = request.form["direccion"]
        latitud = request.form.get("latitud")
        longitud = request.form.get("longitud")
        telefono = request.form["telefono"]
        email = request.form["email"]
        cbu_alias = request.form["cbu_alias"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO medicos (nombre, apellido, dni, matricula, profesion, direccion, latitud, longitud, telefono, email, cbu_alias)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nombre, apellido, dni, matricula, profesion, direccion, latitud, longitud, telefono, email, cbu_alias))
        conn.commit()
        cur.close()
        conn.close()

        flash("Médico registrado correctamente", "success")
        return redirect(url_for("listar_medicos"))

    return render_template("registro_medico.html")

@app.route("/medicos")
def listar_medicos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM medicos ORDER BY id DESC")
    medicos = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template("medicos.html", medicos=medicos)


@app.route("/inicio")
def inicio():
    return redirect(url_for("listar_medicos"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

