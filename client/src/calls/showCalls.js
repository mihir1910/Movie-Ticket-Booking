import axios from 'axios'
import { API_BASE_URL } from './config.js'

const api = axios.create({
    baseURL : API_BASE_URL,
    withCredentials : true
})


// add a show
export const addShow = async (payload) => {
    try{
       const response = await api.post('/api/shows/add-show', payload);
        return response.data;
    }catch(err){
        return err.message;
    }
}

export const getShows = async () => {
    try{
        const response = await api.get('/api/shows/get-all-shows');
        return response.data;
    }catch(err){
        return err.message;
    }
}