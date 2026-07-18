import axios from 'axios'
import { API_BASE_URL } from './config.js'

const api = axios.create({
    baseURL : API_BASE_URL,
    withCredentials : true
})

export const getAllMovies = async()=>{
    try {
       const response = await api.get('/api/movie/all-movies')
       return response.data
    } catch (error) {
        console.log(error)
    }
}