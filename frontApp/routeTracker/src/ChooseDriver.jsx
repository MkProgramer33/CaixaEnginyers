import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";


export default function ChooseDriver() {

    let navigate = useNavigate();
    const [activeUser, setActiveUser] = useState(null);

    function handleChangeUser(userid) {
        setActiveUser(userid)
    }

    useEffect(() => {

        if (activeUser != null) {
            navigate('/driver?userid='+activeUser)
        }

    }, [activeUser])

    console.log(activeUser)

    return (

        <>
            <div className='flex flex-col space-y-8'>

                <div className='flex flex-row p-2 border-b-4'>
                </div>

                <h1 className='text-3xl mx-auto'>Siusplau, identifica't</h1>

                <div className='flex flex-col space-y-8 m-12 p-8'>
                    <button onClick={() => handleChangeUser(4)} type="button" className='bg-slate-100 text-black p-5 text-3xl rounded-lg'>Pau</button>

                    <button onClick={() => handleChangeUser(1)} type="button" className='bg-slate-100 text-black p-5 text-3xl rounded-lg'>Sergi</button>

                    <button onClick={() => handleChangeUser(3)} type="button" className='bg-slate-100 text-black p-5 text-3xl rounded-lg'>Miquel</button>

                    <button onClick={() => handleChangeUser(2)} type="button" className='bg-slate-100 text-black p-5 text-3xl rounded-lg'>Marta</button>

                </div>

            </div>


        </>
    )
}