import React, { useEffect, useRef, useState } from "react";
import { IoPaperPlaneOutline } from "react-icons/io5";
import Header from "./Header";
import Footer from "./Footer";
import { v4 as uuidv4 } from "uuid";

const BACKEND_URL = "https://chipchip-ai-agent-backend.onrender.com";
const CHAT_HISTORY_KEY = "chipchip_chat_history";

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
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(uuidv4());
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    const saved = localStorage.getItem(CHAT_HISTORY_KEY);
    if (saved) {
      try {
        setChatHistory(JSON.parse(saved));
      } catch {
        localStorage.removeItem(CHAT_HISTORY_KEY);
      }
    }
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (messages.length === 0) return;

    setChatHistory((prev) => {
      const updated = [...prev];
      const index = updated.findIndex((c) => c.id === currentChatId);
      const name = updated[index]?.name || messages[0]?.text || "New Chat";

      const updatedChat = {
        id: currentChatId,
        name: name.length > 50 ? name.slice(0, 50) + "..." : name,
        messages,
      };

      if (index !== -1) {
        updated[index] = updatedChat;
      } else {
        updated.push(updatedChat);
      }

      localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(updated));
      return updated;
    });
  }, [messages]);

  const chat = async () => {
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
        body: JSON.stringify({ question, session_id: currentChatId }),
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
    const newId = uuidv4();
    setCurrentChatId(newId);
    setMessages([]);
  };

  const loadChat = (chatItem) => {
    setCurrentChatId(chatItem.id);
    setMessages(chatItem.messages || []);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <div className="flex flex-1 flex-col md:flex-row">
        {/* Left panel: Chat History */}
        <aside className="w-full md:w-1/4 bg-gray-100 p-4 md:p-6 overflow-y-auto border-b md:border-b-0 md:border-r border-gray-200">
          <h3 className="text-lg font-semibold mb-4">🗂️ Chat History</h3>
          <ul className="space-y-2 text-sm">
            {chatHistory.map((chatItem) => (
              <li
                key={chatItem.id}
                onClick={() => loadChat(chatItem)}
                className={`cursor-pointer px-2 py-1 rounded hover:bg-gray-200 ${
                  chatItem.id === currentChatId ? "bg-white font-bold" : ""
                }`}
              >
                {chatItem.name}
              </li>
            ))}
          </ul>
        </aside>

        {/* Right panel: Chat */}
        <main className="w-full md:w-3/4 p-4 md:p-6 flex flex-col">
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
              className="w-full p-3 pr-10 border border-gray-300 rounded-xl resize-none text-base shadow-sm"
            />
            <IoPaperPlaneOutline
              onClick={chat}
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
