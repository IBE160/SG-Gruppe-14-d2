import fs from "fs";
import path from "path";
import { ChatPageClient } from "./chat-page-client";

// This interface can be shared or moved to a types file later
export interface AgentPrompt {
  id: string;
  title: string;
  content: string;
}

/**
 * Server Component to read and parse the markdown file for the chat page.
 * It extracts the sections for each agent and passes them to the Client Component.
 */
export default function ChatPage() {
  const filePath = path.join(process.cwd(), "..", "docs", "AI_AGENT_SYSTEM_PROMPTS.md");
  
  let prompts: AgentPrompt[] = [];
  try {
    const fileContent = fs.readFileSync(filePath, "utf8");

    // Split the document into major sections using a regex that handles both \n and \r\n
    const sections = fileContent.split(/\r?\n---\r?\n/);
    const agentSections = sections.filter(sec => sec.trim().startsWith("## Agent"));

    prompts = agentSections.map(section => {
      const titleMatch = section.match(/## (.*?)\r?\n/);
      const nameMatch = section.match(/\*\*Name:\*\* (.*?)\r?\n/);
      
      const titleLine = titleMatch ? titleMatch[1] : "";
      
      // Determine ID based on Agent number in title
      let id = "unknown";
      if (titleLine.includes("Agent 1")) id = "anne-lise-berg";
      else if (titleLine.includes("Agent 2")) id = "bjorn-eriksen";
      else if (titleLine.includes("Agent 3")) id = "kari-andersen";
      else if (titleLine.includes("Agent 4")) id = "per-johansen";

      const name = nameMatch ? nameMatch[1] : "";
      let simplifiedRole = titleLine.split(': ')[1] || titleLine;
      
      const roleParts = simplifiedRole.split(' - ');
      if (roleParts.length > 1) {
        simplifiedRole = roleParts[1]; // Get the part after the hyphen
      } else {
        // Handle cases like "Owner (Municipality)" by taking the first word
        const parenthesisIndex = simplifiedRole.indexOf('(');
        if (parenthesisIndex !== -1) {
          simplifiedRole = simplifiedRole.substring(0, parenthesisIndex).trim();
        }
      }

      return {
        id,
        title: name ? `${name}, ${simplifiedRole}` : simplifiedRole,
        content: section,
      };
    });

  } catch (error) {
    console.error("Error reading or parsing markdown file for chat:", error);
    prompts = [{
      id: "error",
      title: "Error",
      content: "Could not load agent prompts."
    }];
  }

  console.log("Parsed Chat Prompts:", prompts);

  return <ChatPageClient prompts={prompts} />;
}