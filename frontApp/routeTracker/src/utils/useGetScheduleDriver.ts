import { useEffect, useState } from 'react';

export default function useGetScheduleDriver(driverId) {

    const [driverSchedule, setDriverSchedule] = useState(null);
    const [driverScheduleFetched, setDriverScheduleFetched] = useState(false);
    const [fetchingDriverSchedule, setFetchingDriverSchedule] = useState(false);

    async function getDriverSchedule() {
        setDriverScheduleFetched(false);
        setFetchingDriverSchedule(true);

        try {
            const responseDriverInfo = await fetch("http://localhost:5000/schedule?id_driver="+driverId, {
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

            setDriverSchedule(eventObject);
            setDriverScheduleFetched(true);
        } catch (error) {
            console.error("Failed to fetch driver info:", error);
        } finally {
            setFetchingDriverSchedule(false);
        }
    }

    useEffect(() => {
        if (driverId >= 1) {
            getDriverSchedule();
        }
    }, [driverId]);

    return [driverSchedule, driverScheduleFetched, fetchingDriverSchedule];
}
