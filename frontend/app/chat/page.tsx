import fs from "fs";
import path from "path";
import { ChatPageClient } from "./chat-page-client";

// This interface can be shared or moved to a types file later
export interface AgentPrompt {
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
      const roleMatch = section.match(/\*\*Role:\*\* (.*?)\r?\n/);
      
      const name = nameMatch ? nameMatch[1] : "";
      let simplifiedRole = titleMatch ? titleMatch[1].split(': ')[1] || titleMatch[1] : "Unknown Role";
      
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
        title: name ? `${name}, ${simplifiedRole}` : simplifiedRole,
        content: section,
      };
    });

  } catch (error) {
    console.error("Error reading or parsing markdown file for chat:", error);
    prompts = [{
      title: "Error",
      content: "Could not load agent prompts."
    }];
  }

  console.log("Parsed Chat Prompts:", prompts);

  return <ChatPageClient prompts={prompts} />;
}