import { useEffect, useState } from "react";
import useGetRoutesInfo from "./utils/useGetRoutesInfo";
import useGetMunicipes from "./utils/useGetMunicipes";
import MapComponent from "./MapComponent";
import Slider from 'react-input-slider';

export default function Driving() {



    const [schedule, setSchedule] = useState(null)

    const [routesInfo, routesInfoFetched, fetchingRoutesInfo] = useGetRoutesInfo(schedule)
    const [municipesInfo, municipesInfoFetched, fetchingMunicipes] = useGetMunicipes(1);

    // console.log(municipesInfo)

    const [buttonText, setButtonText] = useState('Iniciar trajecte')
    const [selectedRoute, setSelectedRoute] = useState(null)
    const [selectedRouteInfo, setSelectedRouteInfo] = useState(null)

    const [startPoint, setStartPoint] = useState(null)
    const [endPoint, setEndPoint] = useState(null)

    const [currentPosition, setCurrentPosition] = useState(0)

    const [appStatus, setAppStatus] = useState('begin');
    const [routeText, setRouteText] = useState('No començat')

    const [finished, setFinished] = useState(false);


    // get key param
    useEffect(() => {

        const urlSearchString = window.location.search;
        const params = new URLSearchParams(urlSearchString);
        setSchedule(params.get('scheduleId'));

    }, []);


    useEffect(() => {

        if (routesInfo != null) {
            // console.log(routesInfo[0].route_id)
            setSelectedRoute(routesInfo[currentPosition].route_id)
        }
    }, [routesInfo, currentPosition])

    useEffect(() => {

        if (selectedRoute != null) {
            let currentRouteInfo = routesInfo[findRouteIndex(selectedRoute)]
            setSelectedRouteInfo(currentRouteInfo)
        }

    }, [selectedRoute])


    useEffect(() => {
        if (selectedRouteInfo != null) {
            let municipeInfoStart = returnMunicipeData(selectedRouteInfo.route_origen_id)
            let municipeInfoEnd = returnMunicipeData(selectedRouteInfo.route_destination_id)

            setStartPoint(municipeInfoStart)
            setEndPoint(municipeInfoEnd)

        }
    }, [selectedRouteInfo])

    function returnMunicipeData(munId) {

        if (municipesInfo != null) {
            let index = municipesInfo.findIndex(function (mun) {
                return mun.mun_id == munId;
            });

            console.log(index)

            return municipesInfo[index]
        }
        return "not found municipe info"

    }

    function findRouteIndex(id) {

        let index = routesInfo.findIndex(function (route) {
            return route.route_id == id;
        });
        return index;
    }

    function handleNextRoute() {
        let currentValue = currentPosition;
        console.log(selectedRouteInfo);

        // Verificar si selectedRouteInfo es válido
        if (!selectedRouteInfo) {
            console.log("selectedRouteInfo no es válido.");
            return;
        }

        let index = findRouteIndex(selectedRouteInfo.route_id);
        index += 1;

        let maxLength = routesInfo.length;

        if (index >= maxLength) {
            setAppStatus('finished');
            handleStartFinished();
        } else {
            setCurrentPosition(index);
        }
    }


    function handleCompleteRoute() {

    }

    function handleArrivedRoute() {

    }

    function handleAppStatus() {

        if (appStatus == 'begin') {
            handleStartTrajecte();

        } else if (appStatus == 'routing') {
            handleFinishRouting();
        }
        else if (appStatus == 'arrived') {
            handleStartArrived();
        }
        else if (appStatus == 'finished') {
            handleStartFinished();
        }
    }

    function handleStartTrajecte() {
        setAppStatus('routing')
        let index = findRouteIndex(selectedRouteInfo.route_id)

        let maxLength = routesInfo.length
        index += 1
        setRouteText(index + '/' + maxLength)
    }

    function handleFinishRouting() {
        setAppStatus('arrived')
    }
    function handleStartArrived() {
        handleNextRoute();
        setAppStatus('begin')
        let maxLength = routesInfo.length
        index += 1
        setRouteText(index + '/' + maxLength)

    }
    function handleStartFinished() {
        setRouteText('Totes les rutes completes')
        setFinished(true)
        setAppStatus('finished')
    }



    useEffect(() => {
        if (appStatus == 'begin') {
            setButtonText('Iniciar trajecte')
        }
        else if (appStatus == 'routing') {
            setButtonText('He arribat a destí')

        } else if (appStatus == 'arrived') {
            setButtonText('He completat les tasques a destí')
        }

    }, [appStatus])


    console.log(routesInfo)

    console.log(selectedRoute)

    const [weather, setWeather] = useState(null)
    
    const start = { lat: startPoint?.mun_latitude, lng: startPoint?.mun_longitude };
    const end = { lat: endPoint?.mun_latitude, lng: endPoint?.mun_longitude }; // Barcelona


    useEffect(() => {

        if (end) {
            const apiKey = '8ad702313ac0917fdaa02aabae4f9b3c'; // Reemplaza 'TU_API_KEY' con tu propia clave de API de OpenWeatherMap

            // Construye la URL de la API de OpenWeatherMap
            const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${end.lat}&lon=${end.lng}&appid=${apiKey}`;

            // Realiza la llamada a la API
            fetch(apiUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error al obtener los datos del clima');
                    }
                    return response.json();
                })
                .then(data => {
                    // Comprueba si está nublado y llueve
                    const isCloudy = data.weather.some(weather => weather.main === 'Clouds');
                    const isRaining = data.weather.some(weather => weather.main === 'Rain');

                    // Muestra el resultado
                    if (isCloudy && isRaining) {
                        setWeather('Está nublado y llueve');
                    } else if (isCloudy) {
                        setWeather('Está nublado pero no llueve');
                    } else if (isRaining) {
                        setWeather('No está nublado pero llueve');
                    } else {
                        setWeather('No está nublado ni llueve');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        }

    }, [start, end])

  

    console.log(selectedRouteInfo)

    console.log(startPoint)

    const [routeLoaded, setRouteLoaded] = useState(null)

    function handleRouteLoads(value) {
        setRouteLoaded(value)
    }
    const [puntuacion, setPuntuacion] = useState(5); // Valor inicial del slider


    return (
        <>
            {routesInfo != null && (
                <div className="flex flex-col items-center justify-center min-h-screen p-6 ">
                    {routeText != 'Totes les rutes completes' && <h1 className="text-3xl font-bold mb-6">Ruta en coche de {startPoint?.mun_name} a {endPoint?.mun_name}  </h1>}
                    <div className="w-full max-w-4xl">
                        <div className="flex justify-between mb-4">
                            <div className="w-1/4 p-4 flex justify-end text-center">
                                {routeText != 'Totes les rutes completes' && <h2 className="text-lg font-bold mb-2 justify-center ">Origen: {startPoint?.mun_name}</h2>}
                            </div>
                            <div className="w-1/4 p-4 flex justify-center text-center">
                                {routeText != 'Totes les rutes completes' &&
                                    <button
                                        onClick={handleAppStatus}
                                        className="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition duration-300 w-80 h-24"
                                    >
                                        {buttonText}
                                    </button>
                                }
                            </div>

                            <div className="w-1/4 p-4 flex justify-end text-center">
                                {routeText != 'Totes les rutes completes' && <h2 className="text-lg font-bold mb-2 ">Destino: {endPoint?.mun_name}</h2>}
                                {/* Aquí puedes agregar la lógica para mostrar el destino */}
                            </div>
                        </div>
                        
                        {routeText == 'Totes les rutes completes' ? <h1 className="text-xl font-bold mb-2 text-green-600 text-center bg-white mb-1 p-1 rounded-md">{routeText}</h1>
                                    : <h2 className="text-lg font-bold mb-2">Ruta actual: {routeText}</h2>}
                        <div className="mb-4 p-4 bg-white rounded-md text-black shadow-md flex flex-row">

                            <div>
                               




                                {!finished && <h2>Hora prevista de sortida: {`${(new Date(selectedRouteInfo?.route_planned_start_time)).getUTCHours()}:${(new Date(selectedRouteInfo?.route_planned_start_time)).getUTCMinutes()}:${(new Date(selectedRouteInfo?.route_planned_start_time)).getUTCSeconds()}`}</h2>}
                                {!finished && <h2>Hora prevista d'arribada a destí: {`${(new Date(selectedRouteInfo?.route_planned_start_time)).getUTCHours()}:${(new Date(selectedRouteInfo?.route_planned_start_time)).getUTCMinutes()}:${(new Date(selectedRouteInfo?.route_planned_start_time)).getUTCSeconds()}`}</h2>}
                                {!finished && <h2>Tiempo en ruta previsto: "implementar resta entre salida y llegada  destino"</h2>}
                                {!finished && <h2>Temps previst a estar en destí: {selectedRouteInfo?.route_planned_stance_duration}</h2>}
                                {/* {!finished && <h2 className="text-center">Les dades s'han registrat correctament</h2>} */}

                            </div >
                            
                            {!finished && <div className="ml-auto items-center justify-center text-center">
                                <h1 className="font-bold mt-6">Climate</h1>
                                <p>{weather}</p>
                            </div>}


                            {finished &&
                                <div className="max-w-md mx-auto bg-white shadow-md rounded-md p-6">
                                    <h2 className="text-lg font-semibold mb-4">Evalúa tu experiencia en la ruta</h2>
                                    <form>
                                        <div className="mb-4">
                                            <label htmlFor="puntuacion" className="block text-sm font-medium text-gray-700 mb-2">Puntúa la ruta del 1 al 10</label>
                                            <Slider
                                                axis="x"
                                                x={puntuacion}
                                                xmin={1}
                                                xmax={10}
                                                onChange={({ x }) => setPuntuacion(x)}
                                                styles={{
                                                    track: {
                                                        backgroundColor: '#d6d6d6',
                                                        height: '4px'
                                                    },
                                                    active: {
                                                        backgroundColor: '#6366f1',
                                                        height: '4px'
                                                    },
                                                    thumb: {
                                                        width: '20px',
                                                        height: '20px',
                                                        backgroundColor: '#6366f1',
                                                        borderRadius: '50%'
                                                    }
                                                }}
                                            />
                                            <div className="mt-2 text-center">{puntuacion}</div>
                                        </div>
                                        <div className="mb-4">
                                            <label className="block text-sm font-medium text-gray-700 mb-2">¿Se ha cumplido en el tiempo estimado?</label>
                                            <div className="flex items-center">
                                                <input type="radio" id="si_tiempo" name="tiempo_estimado" value="si" className="mr-2 h-4 w-4 text-indigo-600 focus:ring-indigo-500" />
                                                <label htmlFor="si_tiempo" className="mr-4">Sí</label>
                                                <input type="radio" id="no_tiempo" name="tiempo_estimado" value="no" className="mr-2 h-4 w-4 text-indigo-600 focus:ring-indigo-500" />
                                                <label htmlFor="no_tiempo">No</label>
                                            </div>
                                        </div>
                                        <div className="mb-4">
                                            <label className="block text-sm font-medium text-gray-700 mb-2">¿El tráfico era agradable?</label>
                                            <div className="flex items-center">
                                                <input type="radio" id="si_trafico" name="trafico_agradable" value="si" className="mr-2 h-4 w-4 text-indigo-600 focus:ring-indigo-500" />
                                                <label htmlFor="si_trafico" className="mr-4">Sí</label>
                                                <input type="radio" id="no_trafico" name="trafico_agradable" value="no" className="mr-2 h-4 w-4 text-indigo-600 focus:ring-indigo-500" />
                                                <label htmlFor="no_trafico">No</label>
                                            </div>
                                        </div>
                                        <div className="mb-4">
                                            <label className="block text-sm font-medium text-gray-700 mb-2">¿El estado de la carretera era bueno?</label>
                                            <div className="flex items-center">
                                                <input type="radio" id="si_carretera" name="estado_carretera" value="si" className="mr-2 h-4 w-4 text-indigo-600 focus:ring-indigo-500" />
                                                <label htmlFor="si_carretera" className="mr-4">Sí</label>
                                                <input type="radio" id="no_carretera" name="estado_carretera" value="no" className="mr-2 h-4 w-4 text-indigo-600 focus:ring-indigo-500" />
                                                <label htmlFor="no_carretera">No</label>
                                            </div>
                                        </div>
                                        <button type="button" className="bg-indigo-500 text-white py-2 px-4 rounded-md hover:bg-indigo-600 focus:outline-none focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                                            Enviar
                                        </button>                                    </form>
                                </div>

                            }

                            {/* sumas de fechas      */}
                            {/* Aquí puedes agregar la lógica para mostrar el tiempo transcurrido */}
                        </div>
                        <div>
                            {(start?.lat <= 0 || start?.lat >= 0) && <MapComponent handleRouteLoads={handleRouteLoads} start={start} end={end} className="w-full h-96 mb-6" />}

                        </div>
                    </div>
                </div>
            )}
        </>
    );


}