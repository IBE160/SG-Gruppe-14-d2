'use client'; // This is a client component because it uses state and event handlers

import { useState } from 'react';

// Define the types to match the backend models
interface ChatMessage {
  sender: 'user' | 'ai';
  message: string;
}

const ChatWindow = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: ChatMessage = { sender: 'user', message: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);

    // Hardcoded mock data for the API request, as per the PRD's structure
    // In a real app, this would come from user selections.
    const mockSupplier = {
      id: 'bjorn-eriksen',
      system_prompt: 'You are Bjørn Eriksen, a profit-driven, shrewd general contractor from Norway. You are tough but fair. You prioritize profit margins but can be convinced by solid, data-driven arguments. Never go below your hidden minimums.',
      hidden_params: {
        min_cost_multiplier: 0.9,
        min_duration_multiplier: 0.95,
      },
    };
    const mockWBSItem = {
      id: '1.3.1',
      name: 'Grunnarbeid',
      baseline_cost: 100,
      baseline_duration: 2,
    };
    const chatHistoryForAPI = messages.map(msg => ({...msg})); // Send previous messages

    try {
      const response = await fetch('http://localhost:8000/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          supplier: mockSupplier,
          wbs_item: mockWBSItem,
          chat_history: chatHistoryForAPI,
          user_message: currentInput,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'An error occurred with the API.');
      }

      const data = await response.json();
      
      let aiMessageContent = data.response;
      // If there's an offer, append it to the message for display
      if (data.offer && (data.offer.cost || data.offer.duration)) {
        const costText = data.offer.cost ? `${data.offer.cost} MNOK` : '';
        const durationText = data.offer.duration ? `${data.offer.duration} måneder` : '';
        const offerText = ` (Tilbud: ${[costText, durationText].filter(Boolean).join(', ')})`;
        aiMessageContent += offerText;
      }

      const aiMessage: ChatMessage = { sender: 'ai', message: aiMessageContent };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);

    } catch (error) {
      const errorMessage: ChatMessage = { sender: 'ai', message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}` };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl h-[70vh] flex flex-col bg-gray-800 rounded-lg shadow-xl">
      <div className="flex-1 p-4 overflow-y-auto flex flex-col">
        {messages.map((msg, index) => (
          <div key={index} className={`my-2 p-3 rounded-lg max-w-[80%] break-words ${
            msg.sender === 'user'
              ? 'bg-blue-600 self-end ml-auto'
              : 'bg-gray-700 self-start mr-auto'
          }`}>
            {msg.message}
          </div>
        ))}
        {isLoading && <div className="text-gray-400 self-start mr-auto p-3">AI tenker...</div>}
      </div>
      <div className="p-4 border-t border-gray-700 flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
          className="flex-1 p-2 bg-gray-700 rounded-l-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Skriv en melding..."
          disabled={isLoading}
        />
        <button
          onClick={handleSendMessage}
          disabled={isLoading}
          className="px-4 py-2 bg-blue-600 rounded-r-md hover:bg-blue-700 disabled:bg-blue-900 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
