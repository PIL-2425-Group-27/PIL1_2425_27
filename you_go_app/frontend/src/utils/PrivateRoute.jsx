import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'

function PrivateRoute(props) {
  return props.active ? <Outlet/> : <Navigate to ='/Login'/>
}

export default PrivateRoute