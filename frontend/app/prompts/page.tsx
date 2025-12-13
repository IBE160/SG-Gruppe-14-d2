import fs from "fs";
import path from "path";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function PromptsPage() {
  const filePath = path.join(process.cwd(), "..", "docs", "AI_AGENT_SYSTEM_PROMPTS.md");
  
  let content = "";
  try {
    content = fs.readFileSync(filePath, "utf8");
  } catch (error) {
    console.error("Error reading markdown file:", error);
    content = "# Error: Could not load prompts\n\nThere was an issue reading the content file.";
  }

  return (
    <div className="w-full flex flex-col items-center p-4">
      <div className="w-full max-w-5xl">
        <article className="prose dark:prose-invert lg:prose-xl max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
        </article>
      </div>
    </div>
  );
}