import { useEffect, useState } from 'react';

export default function useGetRoutesInfo(selectedScheduleId) {

    const [routesInfo, setRoutesInfo] = useState(null);
    const [routesInfoFetched, setRoutesInfoFetched] = useState(false);
    const [fetchingRoutesInfo, setFetchingRoutesInfo] = useState(false);

    async function getRoutesInfo() {
        setRoutesInfoFetched(false);
        setFetchingRoutesInfo(true);

        try {
            const responseDriverInfo = await fetch("http://localhost:5000/routes?id_schedule="+selectedScheduleId, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!responseDriverInfo.ok) {
                throw new Error(`Error fetching data: ${responseDriverInfo.statusText}`);
            }

            const responseDriverInfoJson = await responseDriverInfo.json();

            // Assuming the relevant data is in the 'info' property
            const eventObject = responseDriverInfoJson.info.map((event) => ({
                ...event
            }));

            setRoutesInfo(eventObject);
            setRoutesInfoFetched(true);
        } catch (error) {
            console.error("Failed to fetch driver info:", error);
        } finally {
            setFetchingRoutesInfo(false);
        }
    }

    useEffect(() => {
        if (selectedScheduleId >= 1) {
            getRoutesInfo();
        }
    }, [selectedScheduleId]);

    return [routesInfo, routesInfoFetched, fetchingRoutesInfo];
}
