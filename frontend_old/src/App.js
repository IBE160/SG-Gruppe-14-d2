import React, { useEffect, useState } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import WBSHierarchy from './WBSHierarchy';
import ChatHistory from './ChatHistory';
import Tabs from './Tabs'; // Import the new Tabs component
import './App.css'; // Import the new CSS file

// Define personas
const personas = [
  { id: 'contractor', name: 'Hovedentreprenør' },
  { id: 'architect', name: 'Arkitekt' },
  { id: 'hvac', name: 'VVS-ingeniør' },
];

// Main simulator page component
const SimulatorPage = ({ wbsData }) => {
  return (
    <div className="simulator-page">
      <Tabs personas={personas} />
      <hr />
      <div>
        <h2>Arbeidsnedbrytningsstruktur</h2>
        <WBSHierarchy wbsData={wbsData} />
      </div>
    </div>
  );
};


function App() {
  const [message, setMessage] = useState('');
  const [wbsData, setWbsData] = useState([]);

  useEffect(() => {
    // Fetch message from backend
    fetch('http://localhost:8000/')
      .then(response => response.json())
      .then(data => setMessage(data.message))
      .catch(error => console.error('Error fetching message:', error));

    // Fetch WBS data from backend
    fetch('http://localhost:8000/wbs')
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          setWbsData(data);
        } else {
          console.error('WBS data is not an array:', data);
        }
      })
      .catch(error => console.error('Error fetching WBS data:', error));
  }, []);

  return (
    <div className="App">
      <header className="app-header">
        <h1>Prosjektledelsessimulator</h1>
        <p>{message}</p>
        <nav className="app-nav">
          <Link to="/">Simulator</Link>
          <Link to="/history">Chat-historikk</Link>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<SimulatorPage wbsData={wbsData} />} />
          <Route path="/history" element={<ChatHistory personas={personas} />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
