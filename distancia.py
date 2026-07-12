import requests
from geopy.geocoders import Nominatim

API_KEY = "c035f28f-aeda-4891-8304-2eb8fb53931e"

geolocator = Nominatim(user_agent="dry7122")

transportes = {
    "1": "car",
    "2": "bike",
    "3": "foot"
}

while True:

    origen = input("\nCiudad de Origen (Chile) o s para salir: ")

    if origen.lower() == "s":
        print("Programa finalizado.")
        break

    destino = input("Ciudad de Destino (Argentina): ")

    if destino.lower() == "s":
        print("Programa finalizado.")
        break

    print("\nTipo de transporte")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. Caminando")

    opcion = input("Seleccione una opción: ")

    if opcion not in transportes:
        print("Opción inválida\n")
        continue

    origen_geo = geolocator.geocode(origen + ", Chile")
    destino_geo = geolocator.geocode(destino + ", Argentina")

    if origen_geo is None or destino_geo is None:
        print("No se encontró alguna de las ciudades.\n")
        continue

    parametros = [
        ("point", f"{origen_geo.latitude},{origen_geo.longitude}"),
        ("point", f"{destino_geo.latitude},{destino_geo.longitude}"),
        ("profile", transportes[opcion]),
        ("locale", "es"),
        ("instructions", "true"),
        ("points_encoded", "false"),
        ("key", API_KEY)
    ]

    respuesta = requests.get(
        "https://graphhopper.com/api/1/route",
        params=parametros
    )

    if respuesta.status_code != 200:
        print("Error:", respuesta.text)
        continue

    datos = respuesta.json()

    if "paths" not in datos:
        print("No fue posible calcular la ruta.\n")
        continue

    ruta = datos["paths"][0]

    distancia = ruta["distance"] / 1000
    millas = distancia * 0.621371

    tiempo = int(ruta["time"] / 1000)

    horas = tiempo // 3600
    minutos = (tiempo % 3600) // 60
    segundos = tiempo % 60

    print("\n======================================")
    print(f"Direcciones desde {origen} hasta {destino}")
    print(f"Duración: {horas:02d}:{minutos:02d}:{segundos:02d}")
    print(f"Kilómetros: {distancia:.2f}")
    print(f"Millas: {millas:.2f}")
    print("======================================")

    print("\nNarrativa del viaje:\n")

    instrucciones = ruta.get("instructions", [])

    if instrucciones:

        for paso in instrucciones:

            texto = paso["text"]

            texto = texto.replace("toward", "hacia")
            texto = texto.replace("and take", "y toma")
            texto = texto.replace("and drive toward", "y conduce hacia")
            texto = texto.replace("Continue", "Continúa")
            texto = texto.replace("Turn", "Gira")
            texto = texto.replace("Keep", "Mantente")
            texto = texto.replace("Finish!", "¡Fin del recorrido!")

            km = paso["distance"] / 1000

            print(f"- {texto} ({km:.2f} km)")

    else:
        print("No hay instrucciones disponibles para esta ruta.")

    print("======================================")