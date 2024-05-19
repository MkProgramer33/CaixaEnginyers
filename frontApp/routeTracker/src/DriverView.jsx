import { useEffect, useState } from "react";
import useGetDriverInfo from "./utils/useGetDriverInfo";
import useGetScheduleDriver from "./utils/useGetScheduleDriver";
import ScheduleContainer from "./components/ScheduleContainer";
import useGetRoutesInfo from "./utils/useGetRoutesInfo";
import { useNavigate } from "react-router-dom";
import useGetMunicipes from "./utils/useGetMunicipes";


export default function DriverView(driverid) {

    const [driverId, setDriverId] = useState(driverid)

    const [ready, setReady] = useState(false)
    const [selectedSchedule, setSelectedSchedule] = useState(null)

    let navigate = useNavigate();
    const [startRoute, setStartRoute] = useState(null);

    // get key param
    useEffect(() => {

        const urlSearchString = window.location.search;
        const params = new URLSearchParams(urlSearchString);
        setDriverId(params.get('userid'));

    }, [driverid]);

    useEffect(() => {

        if (startRoute != null) {
            navigate('/driving?scheduleId=' + startRoute)
        }

    }, [startRoute])


    function handleStartRoute(scheduleId) { setStartRoute(scheduleId); }




    const [driverInfo, driverInfoFetched, fetchingDriverInfo] = useGetDriverInfo(driverId)
    const [driverSchedule, driverScheduleFetched, fetchingDriverSchedule] = useGetScheduleDriver(driverId)
    const [routesInfo, routesInfoFetched, fetchingRoutesInfo] = useGetRoutesInfo(selectedSchedule)

    const [municipesInfo, municipesInfoFetched, fetchingMunicipes] = useGetMunicipes(1);

    function handleSelectSchedule(id) {
        setSelectedSchedule(id);
    }

    useEffect(() => {

        if (driverInfo != null && driverSchedule != null) {
            setReady(true)
        }

    }, [driverInfo, driverSchedule])



    function returnMunicipeData(munId) {

        // console.log(municipesInfo)

        console.log(driverInfo)
        if (municipesInfo != null) {
            console.log(munId)

            let index = municipesInfo.findIndex(function (mun) {
                return mun.mun_id == munId;
            });

            console.log(index)

            return municipesInfo[index]
        }
        return "not found municipe info"

    }
    function findIndex(id) {

        let index = driverSchedule.findIndex(function (sch) {
            return sch.sch_id == id;
        });
        return index;
    }

    return (
        <>
            {ready &&
                <div className="p-2 flex flex-col md:flex-row space-x-4">
                    <div className="md:w-1/2 flex flex-col">
                        <div className="border-b-2 mb-2">
                            <h1 className="text-3xl">¡Benvingut/da, {driverInfo[0].driver_name}!</h1>
                        </div>

                        {(driverSchedule[0].sch_selected == 1)
                            ?
                            <div className="flex flex-col">
                                <h1>Ja tens una ruta en curs planificada, vols continuar?</h1>
                            </div>

                            : <>
                                <h1>Tens les següents rutes planificades, quina vols escollir?</h1>
                                <div className="flex flex-col">
                                    {driverSchedule.map((schedule, index) => (
                                        <div key={schedule.sch_id} className="border p-2 rounded-sm flex col mb-3">
                                            <div className="flex flex-row"></div>
                                            <div>
                                                <h1>{index}. Ruta</h1>
                                                <p>Bloc: {schedule.sch_bloc_id} - Lot: {schedule.sch_bloc_id}</p>
                                            </div>
                                            <div className="flex justify-center ml-auto"> {/* Centering the button */}
                                                <button onClick={() => handleSelectSchedule(schedule.sch_id)} className="bg-blue-500 text-white p-2 rounded-sm ">Seleccionar</button>
                                            </div>
                                            <div className="flex flex-col justify-center ml-4 mr-1"> {/* Centering the button */}
                                                <div>
                                                    <p className="text-white"> 2 persones</p>
                                                </div>
                                                <div>
                                                    <p className="text-green-600 font-bold"> Connexió: òptima</p>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </>
                        }
                    </div>

                    <div className="md:w-1/2 flex flex-col justify-center">
                        <div className="border p-2 rounded-sm">
                            <h1>Ruta Seleccionada:</h1>
                            {selectedSchedule != null && routesInfo != null && routesInfo[0].route_origen_id >= 1
                                ? <>
                                    {routesInfo.map((route, index) => (
                                        <div key={route.sch_id} className="border p-2 rounded-sm flex col mb-3">
                                            <div className="flex flex-row"></div>
                                            <div>
                                                <h3 className="font-bold border-b-2">Punt {index}</h3>
                                                <p>Nom: {returnMunicipeData(route.route_origen_id).mun_name} </p>
                                                <p>Comarca: {returnMunicipeData(route.route_origen_id).mun_comarca} </p>
                                                <p>Temps de ruta: {route.route_planned_onroute_duration} </p>
                                                <p>Temps d'aturada: {route.route_planned_stance_duration}</p>
                                                <p>Hora planificada de tornada: {`${(new Date(route.route_planned_start_time)).getUTCHours()}:${(new Date(route.route_planned_start_time)).getUTCMinutes()}:${(new Date(route.route_planned_start_time)).getUTCSeconds()}`}</p>
                                                <p>Hora estimada de sortida: {`${(new Date(route.route_planned_finish_time)).getUTCHours()}:${(new Date(route.route_planned_finish_time)).getUTCMinutes()}:${(new Date(route.route_planned_finish_time)).getUTCSeconds()}`}</p>



                                            </div>
                                        </div>
                                    ))}
                                    <button onClick={() => handleStartRoute(selectedSchedule)} className="bg-green-500 text-white p-2 rounded-sm mx-auto justify-center my-auto text-center">¡Començar ruta!</button>
                                </>
                                : <p>Selecciona una ruta...</p>}
                        </div>
                    </div>
                </div>
            }
        </>
    )



}