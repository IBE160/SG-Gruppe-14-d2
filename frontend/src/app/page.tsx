import ChatWindow from "@/components/ChatWindow";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gray-900 text-white">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold">Nye Hædda Barneskole</h1>
        <p className="text-xl text-gray-400">Project Management Simulation</p>
      </div>
      <ChatWindow />
    </main>
  );
}
