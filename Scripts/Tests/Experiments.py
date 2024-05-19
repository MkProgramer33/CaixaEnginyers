import sys
sys.path.append('C:/Users/p2004/Documents/GitHub/CaixaEnginyers/Scripts')

import InfoMapa as InfoMapa
import Agrupar_Kmeans as Agrupar_Kmeans
import Agrupar_Facciones as Agrupar_Facciones
import Buscar_Ruta as Buscar_Ruta

def main():
    mapa = InfoMapa.Mapa()
    InfoMapa.load('../../Data/DatosMunicipios.xlsx', mapa)
    grupos = Agrupar_Kmeans.agrupar_municipios(mapa.get_municipiosBloque(1), 5)
    #grupos = Agrupar_Facciones.agrupar_municipios(mapa.get_municipiosBloque(1))
    InfoMapa.mostrar_agrupacions(grupos)
    ruta1, coste = Buscar_Ruta.nearest_neighbor_algorithm(grupos[4], {8082 : mapa.paradas[8082]})
    InfoMapa.mostrar_rutes([ruta1])
    rutas = []
    for grupo in grupos:
        print(len(grupo))
        ruta, coste = Buscar_Ruta.nearest_neighbor_algorithm(grupo, {8082 : mapa.paradas[8082]})
        rutas.append(ruta)
    InfoMapa.mostrar_rutes(rutas)
    print(rutas)

# Call the main function
if __name__ == "__main__":
    main()