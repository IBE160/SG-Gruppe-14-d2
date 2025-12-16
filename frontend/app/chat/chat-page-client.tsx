"use client";

import { useState, useEffect } from "react";
import type { AgentPrompt } from "./page";
import { ChatInterface } from "@/components/chat-interface";
import { sendChatMessage } from "@/lib/api/chat";
import { createSession } from "@/lib/api/sessions";
import type { ChatMessage, GameContext } from "@/types";

interface ChatPageClientProps {
  prompts: AgentPrompt[];
}

interface Message {
  id: string;
  text: string;
  sender: "user" | "agent";
}

// Map agent titles to agent IDs
const AGENT_TITLE_TO_ID: Record<string, string> = {
  "Anne-Lise Berg": "anne-lise-berg",
  "Bjørn Eriksen": "bjorn-eriksen",
  "Kari Andersen": "kari-andersen",
  "Per Johansen": "per-johansen",
};

export function ChatPageClient({ prompts }: ChatPageClientProps) {
  const [selectedAgent, setSelectedAgent] = useState<AgentPrompt | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Create session on mount
  useEffect(() => {
    const initializeSession = async () => {
      try {
        const session = await createSession();
        setSessionId(session.id);
        console.log("Session created:", session.id);
      } catch (err) {
        console.error("Failed to create session:", err);
        setError("Kunne ikke opprette spilløkt. Vennligst last inn siden på nytt.");
      }
    };

    initializeSession();
  }, []);

  const handleSendMessage = async (messageText: string) => {
    if (!sessionId || !selectedAgent) {
      console.error("No session or agent selected");
      return;
    }

    // Get agent ID from title
    const agentId = AGENT_TITLE_TO_ID[selectedAgent.title];
    if (!agentId) {
      console.error("Unknown agent:", selectedAgent.title);
      setError(`Ukjent agent: ${selectedAgent.title}`);
      return;
    }

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      text: messageText,
      sender: "user",
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Convert messages to API format
      const conversationHistory: ChatMessage[] = messages.map((msg) => ({
        id: msg.id,
        role: msg.sender,
        content: msg.text,
        timestamp: new Date().toISOString(),
      }));

      // Build game context (basic for now)
      const gameContext: GameContext = {
        total_budget: 700_000_000,
        available_budget: 310_000_000,
        locked_budget: 390_000_000,
        current_budget_used: 0,
        deadline_date: "2026-05-15",
        committed_wbs: [],
      };

      // Send message to backend
      const response = await sendChatMessage(
        sessionId,
        agentId,
        messageText,
        conversationHistory,
        gameContext
      );

      // Add agent response to messages
      const agentResponse: Message = {
        id: `${Date.now()}-agent`,
        text: response.response,
        sender: "agent",
      };
      setMessages((prev) => [...prev, agentResponse]);

      console.log("AI Response received:", response);
    } catch (err: any) {
      console.error("Failed to send message:", err);

      // Handle agent locked error
      if (err.code === 'AGENT_LOCKED') {
        setError(`${err.message} Tilgjengelig om ${err.minutes_remaining} minutter.`);
      } else {
        setError(err.message || "Kunne ikke sende melding. Vennligst prøv igjen.");
      }
    } finally {
      setIsLoading(false);
    }
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

      {/* Error Display */}
      {error && (
        <div className="mx-4 mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
          {error}
        </div>
      )}

      {/* Session Status */}
      {!sessionId && (
        <div className="mx-4 mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-blue-800 text-sm">
          Oppretter spilløkt...
        </div>
      )}

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
