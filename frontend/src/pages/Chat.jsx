import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { loadSession, saveSession } from '../utils/sessionManager';
import { commitQuote } from '../utils/sessionManager'; // Import commitQuote

function Chat({ session }) {
  const { wbsCode, supplierId } = useParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const gameSession = loadSession(session.user.id);
  const wbsItem = gameSession.wbs_items.find((w) => w.code === wbsCode);
  const supplier = gameSession.suppliers.find((s) => s.id === supplierId);

  useEffect(() => {
    // Load chat history from localStorage
    const chatKey = `${wbsCode}_${supplierId}`;
    const savedChat = gameSession.chat_logs[chatKey] || [];
    setMessages(savedChat);
  }, [wbsCode, supplierId]);

  useEffect(() => {
    // Auto-scroll to bottom
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      message: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages([...messages, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          wbs_code: wbsCode,
          supplier_id: supplierId,
          message: inputMessage,
          chat_history: messages,
        }),
      });

      const data = await response.json();

      const aiMessage = {
        message: data.message,
        sender: 'ai',
        offer: data.offer,
        timestamp: new Date().toISOString(),
      };

      const updatedMessages = [...messages, userMessage, aiMessage];
      setMessages(updatedMessages);

      // Save to localStorage
      const chatKey = `${wbsCode}_${supplierId}`;
      gameSession.chat_logs[chatKey] = updatedMessages;
      gameSession.metrics.negotiation_count += 1;
      saveSession(gameSession);

    } catch (error) {
      console.error('Error sending message:', error);
      alert('Feil ved sending av melding. Prøv igjen.');
    } finally {
      setLoading(false);
    }
  };

  const acceptOffer = (offer) => {
    const confirmed = window.confirm(
      `Godta tilbud?\n\nWBS: ${wbsItem.code} - ${wbsItem.name}\nLeverandør: ${supplier.name}\nKostnad: ${offer.cost} MNOK\nVarighe: ${offer.duration} måneder\n\nDette vil oppdatere prosjektplanen din.`
    );

    if (confirmed) {
      try {
        const updatedSession = commitQuote(
          gameSession,
          wbsCode,
          supplierId,
          offer.cost,
          offer.duration
        );

        // Add system message to chat
        const systemMessage = {
          message: `✅ Tilbud godtatt og forpliktet til plan`,
          sender: 'system',
          timestamp: new Date().toISOString(),
        };

        const updatedMessages = [...messages, systemMessage];
        setMessages(updatedMessages);

        const chatKey = `${wbsCode}_${supplierId}`;
        updatedSession.chat_logs[chatKey] = updatedMessages;
        saveSession(updatedSession);

        // Show toast notification
        alert(`${wbsItem.code} ${wbsItem.name} lagt til i plan!`);

        // Navigate back to dashboard
        setTimeout(() => navigate('/dashboard'), 1000);
      } catch (error) {
        alert('Feil ved forpliktelse: ' + error.message);
      }
    }
  };

  return (
    <div className="chat-page">
      <header className="chat-header">
        <button onClick={() => navigate('/dashboard')}>← Tilbake til Oversikt</button>
        <div>
          <h2>{supplier.name} - {supplier.role}</h2>
          <p>WBS {wbsItem.code} - {wbsItem.name}</p>
        </div>
      </header>

      <div className="chat-container">
        <div className="chat-window">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.sender}`}>
              <div className="message-bubble">{msg.message}</div>
              {msg.offer && (
                <button
                  className="accept-offer-btn"
                  onClick={() => acceptOffer(msg.offer)}
                >
                  Godta: {msg.offer.cost} MNOK, {msg.offer.duration} måneder
                </button>
              )}
            </div>
          ))}
          {loading && (
            <div className="message ai">
              <div className="message-bubble typing">
                {supplier.name} ser gjennom spesifikasjonene...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="message-input">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Skriv melding..."
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
          />
          <button onClick={sendMessage} disabled={loading}>
            Send →
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;
