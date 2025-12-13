"use client";

import { useState } from "react";
import type { AgentPrompt } from "./page";
import { ChatInterface } from "@/components/chat-interface";

interface ChatPageClientProps {
  prompts: AgentPrompt[];
}

interface Message {
  id: string;
  text: string;
  sender: "user" | "agent";
}

export function ChatPageClient({ prompts }: ChatPageClientProps) {
  const [selectedAgent, setSelectedAgent] = useState<AgentPrompt | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (messageText: string) => {
    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      text: messageText,
      sender: "user",
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // --- Backend API call will go here ---
    // For now, we'll just log to the console and simulate a delay
    console.log("Sending message to agent:", selectedAgent?.title);
    console.log("User Message:", messageText);
    console.log("System Prompt:", selectedAgent?.content);

    // Simulate a fake agent response
    setTimeout(() => {
      const agentResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: "This is a simulated response. The backend is not yet connected.",
        sender: "agent",
      };
      setMessages((prev) => [...prev, agentResponse]);
      setIsLoading(false);
    }, 1500);
  };

  const handleSelectAgent = (agent: AgentPrompt) => {
    setSelectedAgent(agent);
    setMessages([]); // Clear messages when a new agent is selected
  };
  
  const handleGoBack = () => {
    setSelectedAgent(null);
    setMessages([]);
  }

  // If no agent is selected, show the selection screen
  if (!selectedAgent) {
    return (
      <div className="w-full max-w-3xl mx-auto p-4">
        <h1 className="text-3xl font-bold text-center mb-6">Select an Agent</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {prompts.map((agent) => (
            <button
              key={agent.title}
              onClick={() => handleSelectAgent(agent)}
              className="p-6 border rounded-lg text-left hover:bg-muted transition-colors"
            >
              <h2 className="text-xl font-semibold">{agent.title}</h2>
            </button>
          ))}
        </div>
      </div>
    );
  }

  // If an agent is selected, show the chat interface
  return (
    <div className="flex flex-col h-[calc(100vh-10rem)] w-full max-w-4xl mx-auto">
      <div className="flex items-center justify-between p-4 border-b">
        <button onClick={handleGoBack} className="text-sm font-medium hover:underline">
          &larr; Change Agent
        </button>
        <h2 className="text-xl font-bold">{selectedAgent.title}</h2>
        <div className="w-24"></div> {/* Spacer */}
      </div>
      <div className="flex-1">
        <ChatInterface
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}
