import React from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import BlocklistSearch from "./components/BlocklistSearch"; // Import BlocklistSearch
import Home from "./pages/Home"
import CustomNavbar from "./components/CustomNavbar"
import "react-bootstrap/dist/react-bootstrap.min.js"




function Logout() {
	localStorage.clear()
	return <Navigate to="/login" />
}

function RegisterAndLogout() {
	localStorage.clear()
	return <Register />
}
  

function App() {
	return (
		
		
		<BrowserRouter>
		<CustomNavbar />
			<Routes>
				<Route
					path="/"
					element={
						<ProtectedRoute>
							<BlocklistSearch />
						</ProtectedRoute>
					}
				/>

				<Route path="/login" element={<Login />}/>
        		<Route path="/logout" element={<Logout />}/>
				<Route path="/register" element={<RegisterAndLogout />}/>
				<Route path="/search" element={<BlocklistSearch />}></Route>
				<Route path="*" element={<NotFound />}></Route>
			</Routes>
		</BrowserRouter>

		

	)

}  

export default App