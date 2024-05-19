import { useEffect, useState } from 'react';

export default function useGetDriverInfo(driverId) {

    const [driverInfo, setDriverInfo] = useState(null);
    const [driverInfoFetched, setDriverInfoFetched] = useState(false);
    const [fetchingDriverInfo, setFetchingDriverInfo] = useState(false);

    async function getDriverInfo() {
        setDriverInfoFetched(false);
        setFetchingDriverInfo(true);

        try {
            const responseDriverInfo = await fetch("http://localhost:5000/driver?id_driver="+driverId, {
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

            setDriverInfo(eventObject);
            setDriverInfoFetched(true);
        } catch (error) {
            console.error("Failed to fetch driver info:", error);
        } finally {
            setFetchingDriverInfo(false);
        }
    }

    useEffect(() => {
        if (driverId >= 1 ) {
            getDriverInfo();
        }
    }, [driverId]);

    return [driverInfo, driverInfoFetched, fetchingDriverInfo];
}
