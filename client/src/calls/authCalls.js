import axios from 'axios'
import { API_BASE_URL } from './config.js'

const api = axios.create({
    baseURL : API_BASE_URL,
    withCredentials : true
})

export const register = async(values)=>{
    try {
       const response = await api.post('/api/auth/register' , values)
       return response.data
    } catch (error) {
        console.log(error)
    }
}

export const login = async(values)=>{
    try {
       const response = await api.post('/api/auth/login' , values)
       return response.data
    } catch (error) {
        console.log(error)
    }
}

export const getCurrentUser = async()=>{
    try {
       const response = await api.get('/api/auth/current-user' ,{withCredentials:true} )
       return response.data
    } catch (error) {
        console.log('Error getting current user:', error.response?.data || error.message)
        return null
    }
}
