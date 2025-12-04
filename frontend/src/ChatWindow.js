import React, { useState, useEffect } from 'react';

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
        setMessages(prevMessages => [...prevMessages, { text: 'Error: Could not get response from server.', sender: 'system', timestamp: new Date().toISOString() }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prevMessages => [...prevMessages, { text: 'Error: Could not connect to the server.', sender: 'system', timestamp: new Date().toISOString() }]);
    }
  };

  return (
    <div>
      <h3>Chat with {persona.name}</h3>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '300px', overflowY: 'scroll', marginBottom: '10px' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === 'user' ? 'right' : (msg.sender === 'system' ? 'center' : 'left') }}>
            <p>
              <strong>{msg.sender === 'user' ? 'You' : (msg.sender === 'system' ? 'System' : persona.name)}:</strong> {msg.text}
            </p>
            <small>{new Date(msg.timestamp).toLocaleString()}</small>
          </div>
        ))}
      </div>
      <div>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          style={{ width: '80%', padding: '10px' }}
          placeholder={`Ask ${persona.name} a question...`}
        />
        <button onClick={handleSendMessage} style={{ width: '19%', padding: '10px' }}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
