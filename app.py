from flask import Flask, render_template, request, abort
import json

app = Flask(__name__)

# Cargar el JSON
with open("datos.json", "r", encoding="utf-8") as fichero:
    datos = json.load(fichero)

# Guardar la lista de miembros
miembros_json = datos["miembros"]


def obtener_habilidades():
    habilidades = []
    for miembro in miembros_json:
        for habilidad in miembro["habilidades"]:
            if habilidad not in habilidades:
                habilidades.append(habilidad)
    habilidades.sort()
    return habilidades


@app.route("/")
def index():
    return render_template("index.html", escuadron=datos)


@app.route("/miembros")
def miembros():
    nombre_buscar = request.args.get("nombre", "")
    habilidad_buscar = request.args.get("habilidad", "")
    orden = request.args.get("orden", "asc")

    resultados = []

    for miembro in miembros_json:
        coincide_nombre = True
        coincide_habilidad = True

        if nombre_buscar != "":
            if nombre_buscar.lower() not in miembro["nombre"].lower():
                coincide_nombre = False

        if habilidad_buscar != "":
            if habilidad_buscar not in miembro["habilidades"]:
                coincide_habilidad = False

        if coincide_nombre and coincide_habilidad:
            resultados.append(miembro)

    # Ordenar por nombre
    for i in range(len(resultados)):
        for j in range(i + 1, len(resultados)):
            nombre_i = resultados[i]["nombre"].lower()
            nombre_j = resultados[j]["nombre"].lower()
            if orden == "asc":
                if nombre_i > nombre_j:
                    resultados[i], resultados[j] = resultados[j], resultados[i]
            else:
                if nombre_i < nombre_j:
                    resultados[i], resultados[j] = resultados[j], resultados[i]

    habilidades = obtener_habilidades()

    return render_template(
        "miembros.html",
        miembros=resultados,
        habilidades=habilidades,
        nombre_q=nombre_buscar,
        habilidad_q=habilidad_buscar,
        orden=orden,
        total=len(resultados)
    )


@app.route("/miembro/<nombre>")
def detalle(nombre):
    miembro_encontrado = None

    for miembro in miembros_json:
        if miembro["nombre"] == nombre:
            miembro_encontrado = miembro

    if miembro_encontrado is None:
        abort(404)

    return render_template("detalle.html", miembro=miembro_encontrado)


if __name__ == "__main__":
    app.run(debug=True)
