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
    ruta, coste = Buscar_Ruta.TSP_Algorythm(grupos[4])
    InfoMapa.mostrar_rutes(ruta)


# Call the main function
if __name__ == "__main__":
    main()