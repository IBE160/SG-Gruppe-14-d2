import React, { useEffect, useState } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import WBSHierarchy from './WBSHierarchy';
import ChatHistory from './ChatHistory';
import Tabs from './Tabs'; // Import the new Tabs component

// Define personas
const personas = [
  { id: 'contractor', name: 'General Contractor' },
  { id: 'architect', name: 'Architect' },
  { id: 'hvac', name: 'HVAC Engineer' },
];

// Main simulator page component
const SimulatorPage = ({ wbsData }) => {
  return (
    <div style={{ padding: '20px' }}>
      <Tabs personas={personas} />
      <hr style={{ margin: '20px 0' }} />
      <div>
        <h2>Work Breakdown Structure</h2>
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

  const headerStyle = {
    padding: '10px 20px',
    backgroundColor: '#f0f0f0',
    borderBottom: '2px solid #ccc'
  };

  const navStyle = {
    display: 'flex',
    gap: '20px',
    marginTop: '10px'
  };

  return (
    <div className="App">
      <header style={headerStyle}>
        <h1>Project Management Simulator</h1>
        <p>{message}</p>
        <nav style={navStyle}>
          <Link to="/">Simulator</Link>
          <Link to="/history">Chat History</Link>
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
