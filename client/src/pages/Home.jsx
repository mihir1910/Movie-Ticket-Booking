import React, { useEffect } from 'react'
import { getCurrentUser } from '../calls/authCalls.js'

function Home() {
  const getUserData = async ()=>{
     const userData =  await getCurrentUser()
     console.log(userData)
  }

   useEffect(()=>{
     getUserData()
   } , [])
   
  return (
    <div>
        <h1>This is the Home Page</h1>
    </div>
  )
}

export default Home