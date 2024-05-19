import sys
sys.path.append('C:/Users/p2004/Documents/GitHub/CaixaEnginyers/Scripts')

import InfoMapa as InfoMapa
import Agrupar_Kmeans as Agrupar_Kmeans

def main():
    mapa = InfoMapa.Mapa()
    InfoMapa.load('../../Data/DatosMunicipios.xlsx', mapa)

    grupos = Agrupar_Kmeans.agrupar_municipios(mapa.get_municipiosBloque(1), 5)
    InfoMapa.mostrar_mapa(grupos)


# Call the main function
if __name__ == "__main__":
    main()