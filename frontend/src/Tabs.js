import React, { useState } from 'react';
import ChatWindow from './ChatWindow';
import './Tabs.css'; // Import the CSS file

const Tabs = ({ personas }) => {
  const [activeTab, setActiveTab] = useState(personas[0].id);

  const activePersona = personas.find(p => p.id === activeTab);

  return (
    <div>
      <div className="tabs-container">
        {personas.map(persona => (
          <div
            key={persona.id}
            className={`tab-item ${activeTab === persona.id ? 'active' : ''}`}
            onClick={() => setActiveTab(persona.id)}
          >
            {persona.name}
          </div>
        ))}
      </div>
      <div className="tab-content">
        {activePersona && <ChatWindow persona={activePersona} />}
      </div>
    </div>
  );
};

export default Tabs;
