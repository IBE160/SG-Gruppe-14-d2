import React, { useState } from 'react';
import './ChatHistory.css'; // Import the CSS file

const ChatHistory = ({ personas }) => {
  const [selectedPersonaId, setSelectedPersonaId] = useState(personas.length > 0 ? personas[0].id : '');

  const storageKey = `chatHistory_${selectedPersonaId}`;
  const savedMessages = JSON.parse(localStorage.getItem(storageKey)) || [];
  const selectedPersona = personas.find(p => p.id === selectedPersonaId);

  return (
    <div className="chat-history-container">
      <h2>Chat-historikk</h2>

      {personas.length > 0 ? (
        <>
          <div>
            <label htmlFor="persona-select">Velg persona: </label>
            <select
              id="persona-select"
              value={selectedPersonaId}
              onChange={(e) => setSelectedPersonaId(e.target.value)}
            >
              {personas.map(persona => (
                <option key={persona.id} value={persona.id}>
                  {persona.name}
                </option>
              ))}
            </select>
          </div>

          <hr />

          {savedMessages.length === 0 ? (
            <p>Ingen chat-historikk funnet for {selectedPersona?.name}.</p>
          ) : (
            <div className="chat-history-log">
              <h3>Historikk med {selectedPersona?.name}</h3>
              {savedMessages.map((msg, index) => (
                <div key={index} className={`chat-history-message ${msg.sender === 'user' ? 'user' : 'persona'}`}>
                  <p>
                    <strong>{msg.sender === 'user' ? 'Du' : selectedPersona?.name}:</strong> {msg.text}
                  </p>
                  <small>{new Date(msg.timestamp).toLocaleString()}</small>
                </div>
              ))}
            </div>
          )}
        </>
      ) : (
        <p>Ingen personaer tilgjengelig.</p>
      )}
    </div>
  );
};

export default ChatHistory;
