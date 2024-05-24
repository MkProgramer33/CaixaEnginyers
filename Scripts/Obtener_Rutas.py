import json

import InfoMapa as InfoMapa
import Agrupar_Kmeans as Agrupar_Kmeans
import Agrupar_Facciones as Agrupar_Facciones
import Buscar_Ruta as Buscar_Ruta

def crear_json_rutas(lista_lista_rutas):
    json_rutas = {}
    for bloque_index, lista_rutas in enumerate(lista_lista_rutas, start=1):
        bloque_key = f"Bloque {bloque_index}"
        json_rutas[bloque_key] = {}
        for dia_index, ruta in enumerate(lista_rutas, start=1):
            dia_key = f"Día {dia_index}"
            json_rutas[bloque_key][dia_key] = []
            for municipio in ruta:
                json_rutas[bloque_key][dia_key].append({
                    "municipio": municipio["municipio"],
                    "poblacion": municipio["poblacion"],
                    "bloque": municipio["bloque"],
                    "estancia_minima": municipio["estancia_minima"],
                    "lote": municipio["lote"],
                    "longitud": municipio["longitud"],
                    "latitud": municipio["latitud"]
                })

    with open("./Tests/rutas.json", "w") as json_file:
        json.dump(json_rutas, json_file, indent=4, ensure_ascii=False)


def get_lista_rutas(mapa):
    NUM_CAMIONEROS = 4
    NUM_DIAS = 5
    lista_rutas = []
    contador_paradas = 0
    for n_persona in range(1, NUM_CAMIONEROS + 1):
        grupos = Agrupar_Kmeans.agrupar_municipios(mapa.get_municipiosBloque(n_persona), NUM_DIAS)
        rutas = []
        for grupo in grupos:
            print(contador_paradas ,"/",len(mapa.paradas))
            contador_paradas += sum(len(grupo) for grupo in grupos)
            ruta, coste = Buscar_Ruta.nearest_neighbor_algorithm(grupo, {8082 : mapa.paradas[8082]})
            rutas.append(ruta)
        lista_rutas.append(rutas)
    return lista_rutas
    

def main():
    mapa = InfoMapa.Mapa()
    InfoMapa.load('../Data/DatosMunicipios.xlsx', mapa)

    lista_lista_rutas = get_lista_rutas(mapa)
    print("Listas Finalizadas")
    crear_json_rutas(lista_lista_rutas)

# Call the main function
if __name__ == "__main__":
    main()