import React, { useEffect, useRef, useState } from "react";
import { IoPaperPlaneOutline } from "react-icons/io5";
import Header from "./Header";
import Footer from "./Footer";

const LOCAL_STORAGE_KEY = "chipchip_chat_memory";
const BACKEND_URL = "https://chipchip-ai-agent-backend.onrender.com";
const SESSION_ID = "frontend-user-session"; // you can also generate a uuid here if needed

const TypingDots = () => (
  <div className="flex gap-1 items-center">
    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
  </div>
);

const AskAgent = () => {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [examples, setExamples] = useState([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (saved) {
      try {
        setMessages(JSON.parse(saved));
      } catch {
        localStorage.removeItem(LOCAL_STORAGE_KEY);
      }
    }

    fetch(`${BACKEND_URL}/examples`)
      .then(res => res.json())
      .then(data => setExamples(data.examples || []))
      .catch(() => setExamples([]));
  }, []);

  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const ask = async () => {
    if (!question.trim()) return;

    const timestamp = new Date().toLocaleTimeString();
    const userMsg = { sender: "user", text: question, timestamp };

    setMessages((prev) => [...prev, userMsg]);
    setQuestion("");
    setLoading(true);

    try {
      const res = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, session_id: SESSION_ID }),
      });

      const data = await res.json();
      const botMsg = { sender: "bot", text: data.answer, timestamp: new Date().toLocaleTimeString() };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("❌ Chat fetch failed:", err);
      setMessages((prev) => [...prev, {
        sender: "bot",
        text: "⚠️ Sorry, something went wrong.",
        timestamp: new Date().toLocaleTimeString(),
      }]);
    }

    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chat();
    }
  };

  const startNewChat = () => {
    setMessages([]);
    localStorage.removeItem(LOCAL_STORAGE_KEY);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <div className="flex flex-1">
        {/* Left panel: Examples */}
        <aside className="w-1/3 bg-gray-100 p-6">
          <h3 className="text-lg font-semibold mb-4">💡 Sample Queries</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-gray-700">
            {examples.length ? examples.map((e, i) => (
              <li key={i} onClick={() => setQuestion(e)} className="cursor-pointer hover:underline">
                {e}
              </li>
            )) : <li>Loading examples...</li>}
          </ul>
        </aside>

        {/* Right panel: Chat */}
        <main className="w-2/3 p-6 flex flex-col">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-lg font-semibold">🧠 Chat</h2>
            <button
              onClick={startNewChat}
              className="text-sm text-red-600 hover:underline"
            >
              🗑️ New Chat
            </button>
          </div>

          {/* Chat messages */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-4 px-1">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex items-start gap-2 ${
                  msg.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {msg.sender === "bot" && <div className="text-xl">🤖</div>}

                <div
                  className={`max-w-[70%] px-4 py-2 rounded-xl shadow-sm text-sm ${
                    msg.sender === "user"
                      ? "bg-gray-200 text-right"
                      : "bg-white border border-gray-300 text-left"
                  }`}
                >
                  <p className="text-gray-800">{msg.text}</p>
                </div>

                {msg.sender === "user" && <div className="text-xl">🙂</div>}
              </div>
            ))}

            {loading && (
              <div className="flex items-center gap-2 justify-start">
                <div className="text-xl">🤖</div>
                <div className="bg-white border border-gray-300 px-4 py-2 rounded-xl text-sm">
                  <TypingDots />
                </div>
              </div>
            )}
          </div>

          {/* Input area */}
          <div className="relative w-full mt-3">
            <textarea
              rows="2"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your question and press Enter"
              className="w-full p-3 pr-10 border border-gray-300 rounded-xl resize-none text-sm shadow-sm"
            />
            <IoPaperPlaneOutline
              onClick={ask}
              className="absolute bottom-3 right-4 text-xl cursor-pointer text-red-600 hover:text-red-700"
              title="Send"
            />
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
};

export default AskAgent;
