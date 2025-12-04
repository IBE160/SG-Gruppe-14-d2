import React, { useState } from 'react';

const ChatHistory = ({ personas }) => {
  const [selectedPersonaId, setSelectedPersonaId] = useState(personas.length > 0 ? personas[0].id : '');

  const storageKey = `chatHistory_${selectedPersonaId}`;
  const savedMessages = JSON.parse(localStorage.getItem(storageKey)) || [];
  const selectedPersona = personas.find(p => p.id === selectedPersonaId);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Chat History</h2>

      {personas.length > 0 ? (
        <>
          <div>
            <label htmlFor="persona-select">Select Persona: </label>
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

          <hr style={{ margin: '20px 0' }} />

          {savedMessages.length === 0 ? (
            <p>No chat history found for {selectedPersona?.name}.</p>
          ) : (
            <div style={{ border: '1px solid #ccc', padding: '10px' }}>
              <h3>History with {selectedPersona?.name}</h3>
              {savedMessages.map((msg, index) => (
                <div key={index} style={{ marginBottom: '10px', textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
                  <p>
                    <strong>{msg.sender === 'user' ? 'You' : selectedPersona?.name}:</strong> {msg.text}
                  </p>
                  <small>{new Date(msg.timestamp).toLocaleString()}</small>
                </div>
              ))}
            </div>
          )}
        </>
      ) : (
        <p>No personas available.</p>
      )}
    </div>
  );
};

export default ChatHistory;
