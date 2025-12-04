import React, { useState } from 'react';
import ChatWindow from './ChatWindow';

const Tabs = ({ personas }) => {
  const [activeTab, setActiveTab] = useState(personas[0].id);

  const activePersona = personas.find(p => p.id === activeTab);

  const tabStyle = {
    padding: '10px 15px',
    cursor: 'pointer',
    borderBottom: '3px solid transparent',
  };

  const activeTabStyle = {
    ...tabStyle,
    borderBottom: '3px solid blue',
  };

  return (
    <div>
      <div style={{ display: 'flex', borderBottom: '1px solid #ccc' }}>
        {personas.map(persona => (
          <div
            key={persona.id}
            style={activeTab === persona.id ? activeTabStyle : tabStyle}
            onClick={() => setActiveTab(persona.id)}
          >
            {persona.name}
          </div>
        ))}
      </div>
      <div style={{ padding: '20px' }}>
        {activePersona && <ChatWindow persona={activePersona} />}
      </div>
    </div>
  );
};

export default Tabs;
