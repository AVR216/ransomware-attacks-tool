import { useFetch } from "../../hooks";
import { HeatmapResponse } from "../../models/models";

//const REST_COUNTRIES_URL = 'https://restcountries.com/v3.1/alpha/';
const LOCAL_API_HACKER_URL = 'http://localhost:5002/api/v1/ransomware';



export const Heatmap = () => {
    
    const {data, loading, error } = useFetch<HeatmapResponse>(`${LOCAL_API_HACKER_URL}/heatmap`)

    console.log(data)

    if (loading) {
        return <h1>Loading...</h1>
    }

    if(error) {
        return <h1>Error: {error.message}</h1>
    }

    return (
        <div>
            <p>{data?.heatmap_info[0].victims}</p>
        </div>
    )
}