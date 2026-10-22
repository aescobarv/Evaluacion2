#!/usr/bin/env python3
import requests
import urllib.parse
import json

# Reemplaza con tu token generado en Graphhopper
KEY = "f2154119-b859-4f4f-884e-216901be5c5f"
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

def obtener_coordenadas(lugar, key):
    params = {"q": lugar, "locale": "es", "key": key}
    url_completa = geocode_url + urllib.parse.urlencode(params)
    r = requests.get(url_completa)
    
    # Imprimimos el estado y la respuesta real para diagnosticar
    print(f"[DEBUG] URL solicitada: {url_completa}")
    print(f"[DEBUG] Código HTTP: {r.status_code} | Respuesta: {r.text}")
    
    if r.status_code == 200:
        data = r.json()
        if data.get("hits"):
            punto = data["hits"][0]["point"]
            return punto["lat"], punto["lng"]
    return None, None

def main():
    print("=== Simulador de Direcciones Graphhopper (DEVASC) ===")
    print("Escribe 's' o 'salir' en cualquier momento para finalizar el programa.\n")
    
    while True:
        origen = input("Ingrese el punto de partida: ").strip()
        if origen.lower() in ["s", "salir"]:
            print("Saliendo del programa. ¡Hasta luego!")
            break
            
        destino = input("Ingrese el destino: ").strip()
        if destino.lower() in ["s", "salir"]:
            print("Saliendo del programa. ¡Hasta luego!")
            break
            
        print("\nBuscando coordenadas geográficas...")
        lat_orig, lon_orig = obtener_coordenadas(origen, KEY)
        lat_dest, lon_dest = obtener_coordenadas(destino, KEY)
        
        if not lat_orig or not lat_dest:
            print("Error: No se pudieron encontrar las ubicaciones ingresadas. Verifique los nombres e intente nuevamente.\n")
            continue
            
        route_params = {
            "point": [f"{lat_orig},{lon_orig}", f"{lat_dest},{lon_dest}"],
            "vehicle": "car",
            "locale": "es",
            "key": KEY
        }
        
        url_completa = route_url + urllib.parse.urlencode(route_params, doseq=True)
        respuesta = requests.get(url_completa)
        
        if respuesta.status_code == 200:
            datos_ruta = respuesta.json()
            if "paths" in datos_ruta:
                path = datos_ruta["paths"][0]
                
                distancia_km = path["distance"] / 1000.0  
                tiempo_min = (path["time"] / 1000.0) / 60.0  
                
                print("\n--- Resultados del Viaje ---")
                print(f"Distancia total: {distancia_km:.2f} km")
                print(f"Tiempo estimado: {tiempo_min:.2f} minutos")
                
                print("\nNarrativa del viaje (Instrucciones paso a paso):")
                instrucciones = path.get("instructions", [])
                for i, instruccion in enumerate(instrucciones, 1):
                    texto = instruccion.get("text", "")
                    dist_inst_m = instruccion.get("distance", 0.0)
                    print(f"{i}. {texto} ({dist_inst_m:.2f} metros)")
                print("-" * 50 + "\n")
            else:
                print("No se encontró una ruta válida entre los puntos especificados.\n")
        else:
            print(f"Error en la API de Graphhopper: Código de estado {respuesta.status_code}\n")

if __name__ == "__main__":
    main()