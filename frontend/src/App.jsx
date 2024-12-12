import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Clients from "./Clients";
import Users from "./Users";
import './App.css'; // Re-import the CSS file

function App() {
  return (
    <Router>
      <div style={{ margin: "20px" }}>
        <nav>
          <Link to="/clients" style={{ margin: "10px" }}>Clients</Link>
          <Link to="/users" style={{ margin: "10px" }}>Users</Link>
        </nav>
        <Routes>
          <Route path="/clients" element={<Clients />} />
          <Route path="/users" element={<Users />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
