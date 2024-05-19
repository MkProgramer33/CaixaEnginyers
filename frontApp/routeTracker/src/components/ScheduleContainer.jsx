import useGetScheduleDriver from "../utils/useGetScheduleDriver"

export default function ScheduleContainer(scheduleId){
    const [routesInfo, routesInfoFetched, fetchingDriverInfo] = useGetScheduleDriver(scheduleId)
    return (
        <>
        

        </>
    )
}