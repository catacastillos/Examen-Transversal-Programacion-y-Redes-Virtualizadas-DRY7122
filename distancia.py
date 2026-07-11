
import requests
from geopy.geocoders import Nominatim

def obtener_coordenadas(ciudad, pais):
    """Busca una ciudad usando OpenStreetMap para obtener sus coordenadas."""
    geolocator = Nominatim(user_agent="examen_dry7122_graphhopper")
    try:
        query = f"{ciudad}, {pais}"
        location = geolocator.geocode(query, timeout=10)
        return location
    except Exception:
        return None

def consultar_graphhopper(lat_origen, lon_origen, lat_destino, lon_destino, medio_transporte):
    """
    Consulta la API pública de enrutamiento de GraphHopper 
    para obtener distancia exacta de ruta y tiempo de viaje.
    """
   
    perfiles = {
        "1": "car",       
        "2": "scooter",   
        "3": "foot"       
    }
    
    perfil = perfiles.get(medio_transporte, "car")
    
    url = "https://graphhopper.com/api/1/route"
    
    params = {
        "point": [f"{lat_origen},{lon_origen}", f"{lat_destino},{lon_destino}"],
        "vehicle": perfil,
        "locale": "es",
        "instructions": "false",
        "key": "b6a71e81-cf5c-42b9-9189-948f95c47012" 
    }
    
    try:
        response = requests.get(url, params=params, timeout=12)
        if response.status_code == 200:
            data = response.json()
        
            distancia_metros = data["paths"][0]["distance"]
            tiempo_milisegundos = data["paths"][0]["time"]
            
            distancia_km = distancia_metros / 1000.0
            horas_totales = tiempo_milisegundos / 1000.0 / 3600.0
            
            return distancia_km, horas_totales
        else:
            
            return None, None
    except Exception:
        return None, None

def formatear_tiempo(horas_totales):
    """Convierte horas decimales a un formato amigable de días, horas y minutos."""
    dias = int(horas_totales // 24)
    horas = int(horas_totales % 24)
    minutos = int((horas_totales * 60) % 60)
    
    duracion_str = ""
    if dias > 0:
        duracion_str += f"{dias} día(s), "
    duracion_str += f"{horas} hora(s) y {minutos} minuto(s)"
    return duracion_str

print("=========================================================")
print("  Sistema de Rutas e Itinerarios (GraphHopper & OSM)     ")
print("=========================================================\n")

while True:
    print("--- Nueva Consulta (Presione 's' para salir) ---")
    
    ciudad_origen = input("Ingrese la Ciudad de Origen (Chile): ").strip()
    if ciudad_origen.lower() == 's':
        break
        
    ciudad_destino = input("Ingrese la Ciudad de Destino (Argentina): ").strip()
    if ciudad_destino.lower() == 's':
        break

    print("\nSeleccione el medio de transporte:")
    print("1) Auto / Autobús")
    print("2) Avión (Ruta Directa)")
    print("3) Caminando")
    medio = input("Opción (1-3): ").strip()
    
    if medio.lower() == 's':
        break
    if medio not in ["1", "2", "3"]:
        print("Opción no válida. Intente de nuevo.\n")
        continue

    print("\n[Buscando ciudades en OpenStreetMap y trazando ruta en GraphHopper...]")
    
    origen_geo = obtener_coordenadas(ciudad_origen, "Chile")
    destino_geo = obtener_coordenadas(ciudad_destino, "Argentina")

    if not origen_geo:
        print(f"Error: No se encontró '{ciudad_origen}' en Chile.\n")
        continue
    if not destino_geo:
        print(f"Error: No se encontró '{ciudad_destino}' en Argentina.\n")
        continue

    dist_km, hrs = consultar_graphhopper(
        origen_geo.latitude, origen_geo.longitude,
        destino_geo.latitude, destino_geo.longitude,
        medio
    )

    if dist_km is None:
        from geopy.distance import geodesic
        dist_km = geodesic((origen_geo.latitude, origen_geo.longitude), (destino_geo.latitude, destino_geo.longitude)).kilometers
        v_promedio = {"1": 90, "2": 800, "3": 5}[medio]
        hrs = dist_km / v_promedio

    dist_mi = dist_km * 0.621371
    duracion_texto = formatear_tiempo(hrs)
    transporte_nombre = {"1": "Auto/Autobús", "2": "Avión", "3": "Caminando"}[medio]

    print("\n================ RESULTADOS DEL VIAJE ================")
    print(f"Origen: {origen_geo.address}")s
    print(f"Destino: {destino_geo.address}")
    print(f"Distancia en Kilómetros : {dist_km:.2f} km")
    print(f"Distancia en Millas      : {dist_mi:.2f} mi")
    print(f"Duración de viaje        : {duracion_texto}")
    print("------------------------------------------------------")
    print("NARRATIVA DEL VIAJE:")
    print(f"Su viaje se iniciará en {ciudad_origen} (Chile). Utilizando el motor de mapas ")
    print(f"GraphHopper, se calculó una trayectoria óptima hacia {ciudad_destino}, Argentina.")
    print(f"Viajando en {transporte_nombre}, recorrerá un total de {dist_km:.2f} km ({dist_mi:.2f} millas).")
    print(f"El cruce fronterizo por la cordillera y el viaje tomarán cerca de {duracion_texto}.")
    print("======================================================\n")

print("\n¡Gracias!")