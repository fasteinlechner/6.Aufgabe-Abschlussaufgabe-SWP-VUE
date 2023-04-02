import axios from "axios";

export async function get_states(){
    return await axios.get('http//127.0.0.1:5000/regions', {}).data;
}

export async function get_events(q){
    return await axios.get(`http//127.0.0.1:5000/get_events_by_NOC/${q}`, {}).data;
}

export async function get_medals(q)
{
    return await axios.get(`http://127.0.0.1:5000/medals/${q}`,{}).data;
}

export async function get_medals2(q)
{
    return await axios.get(`http://127.0.0.1:5000/medals2/${q}`,{}).data;
}

export async function get_medals_by_gender() {
    return await axios.get(`http://127.0.0.1:5000/count_by_sex2`,{}).data;
}

export async function get_medals_per_season(q) {
    return await axios.get(`http://127.0.0.1:5000//medals3/${q}`,{}).data;
}
