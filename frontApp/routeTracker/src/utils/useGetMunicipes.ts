import { useEffect, useState } from 'react';

export default function useGetMunicipes(selectedScheduleId) {

    const [routesInfo, setRoutesInfo] = useState(null);
    const [routesInfoFetched, setRoutesInfoFetched] = useState(false);
    const [fetchingRoutesInfo, setFetchingRoutesInfo] = useState(false);

    async function getMunicipesInfo() {
        setRoutesInfoFetched(false);
        setFetchingRoutesInfo(true);

        try {
            const responseDriverInfo = await fetch("http://localhost:5000/municipes", {
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
        console.log(selectedScheduleId)

        if (selectedScheduleId >= 1) {
            getMunicipesInfo();
        }
    }, [selectedScheduleId]);

    return [routesInfo, routesInfoFetched, fetchingRoutesInfo];
}
