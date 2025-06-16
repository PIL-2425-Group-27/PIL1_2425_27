import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'

const user = true
function PrivateRoute() {
  return user ? <Outlet/> : <Navigate to ='/Login'/>
}

export default PrivateRoute