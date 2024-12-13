import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Clients from "./Clients";
import Users from "./Users";
import ServiceType from "./Servicetype";
import ServiceRequest from "./ServiceRequest";
import './App.css'; // Re-import the CSS file

function App() {
  return (
    <Router>
      <div style={{ margin: "20px" }}>
        <nav>
          <Link to="/clients" style={{ margin: "10px" }}>Clients</Link>
          <Link to="/users" style={{ margin: "10px" }}>Users</Link>
          <Link to="/service_type" style={{ margin: "10px" }}>ServiceType</Link>
          <Link to="/service_request" style={{ margin: "10px" }}>ServiceRequest</Link>
        </nav>
        <Routes>
          <Route path="/clients" element={<Clients />} />
          <Route path="/users" element={<Users />} />
          <Route path="/service_type" element={<ServiceType />} />
          <Route path="/service_request" element={<ServiceRequest />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
