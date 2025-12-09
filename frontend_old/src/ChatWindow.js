import React, { useState, useEffect } from 'react';
import './ChatWindow.css'; // Import the CSS file

const ChatWindow = ({ persona }) => { // Accept persona prop
  const storageKey = `chatHistory_${persona.id}`; // Dynamic storage key

  // Initialize state from localStorage or with an empty array
  const [messages, setMessages] = useState(() => {
    const savedMessages = localStorage.getItem(storageKey);
    return savedMessages ? JSON.parse(savedMessages) : [];
  });
  const [newMessage, setNewMessage] = useState('');

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(storageKey, JSON.stringify(messages));
  }, [messages, storageKey]);

  // Reset chat when persona changes
  useEffect(() => {
    const savedMessages = localStorage.getItem(storageKey);
    setMessages(savedMessages ? JSON.parse(savedMessages) : []);
    setNewMessage(''); // Also clear the input field
  }, [persona, storageKey]);


  const handleSendMessage = async () => {
    if (newMessage.trim() === '') return;

    const userMessage = { text: newMessage, sender: 'user', timestamp: new Date().toISOString() };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setNewMessage('');

    try {
      const response = await fetch('http://localhost:8000/negotiate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          persona_id: persona.id, // Pass persona_id to backend
          message: newMessage,
        }),
      });

      if (response.ok) {
        const aiResponse = await response.json();
        setMessages(prevMessages => [...prevMessages, { ...aiResponse, timestamp: new Date().toISOString() }]);
      } else {
        console.error('Error sending message:', response.statusText);
        setMessages(prevMessages => [...prevMessages, { text: 'Feil: Kunne ikke få svar fra serveren.', sender: 'system', timestamp: new Date().toISOString() }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prevMessages => [...prevMessages, { text: 'Feil: Kunne ikke koble til serveren.', sender: 'system', timestamp: new Date().toISOString() }]);
    }
  };

  const getMessageClassName = (msg) => {
    const baseClass = 'message';
    if (msg.sender === 'user') return `${baseClass} user`;
    if (msg.sender === 'system') return `${baseClass} system`;
    return `${baseClass} persona`;
  };

  return (
    <div>
      <h3>Chat med {persona.name}</h3>
      <div className="chat-log">
        {messages.map((msg, index) => (
          <div key={index} className={getMessageClassName(msg)}>
            <p>
              <strong>{msg.sender === 'user' ? 'Du' : (msg.sender === 'system' ? 'System' : persona.name)}:</strong> {msg.text}
            </p>
            <small>{new Date(msg.timestamp).toLocaleString()}</small>
          </div>
        ))}
      </div>
      <div className="chat-input-area">
        <input
          type="text"
          className="chat-input"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder={`Still ${persona.name} et spørsmål...`}
        />
        <button onClick={handleSendMessage} className="send-button">
          Send inn
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
