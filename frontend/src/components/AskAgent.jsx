import React, { useEffect, useRef, useState } from "react";
import { IoPaperPlaneOutline } from "react-icons/io5";
import Header from "./Header";
import Footer from "./Footer";

const LOCAL_STORAGE_KEY = "chipchip_chat_memory";
const BACKEND_URL = "https://chipchip-ai-agent-backend.onrender.com";

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
  const [useMemory, setUseMemory] = useState(false);
  const [showFeedback, setShowFeedback] = useState(false);
  const [lastInteraction, setLastInteraction] = useState(null);
  const [feedbackRating, setFeedbackRating] = useState(5);
  const [feedbackComment, setFeedbackComment] = useState("");
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
      const endpoint = useMemory ? "/chat" : "/ask";
      const res = await fetch(`${BACKEND_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      const botMsg = { sender: "bot", text: data.answer, timestamp: new Date().toLocaleTimeString() };
      setMessages((prev) => [...prev, botMsg]);
      setLastInteraction({ question, answer: data.answer });
      setShowFeedback(true);
    } catch {
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
      ask();
    }
  };

  const startNewChat = () => {
    setMessages([]);
    localStorage.removeItem(LOCAL_STORAGE_KEY);
  };

  const submitFeedback = async () => {
    if (!lastInteraction) return;

    try {
      await fetch(`${BACKEND_URL}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: lastInteraction.question,
          answer: lastInteraction.answer,
          rating: feedbackRating,
          comment: feedbackComment
        }),
      });
    } catch (err) {
      console.error("Feedback submission failed");
    }

    setShowFeedback(false);
    setFeedbackComment("");
    setFeedbackRating(5);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <div className="flex flex-1">
        {/* Left panel: Examples + toggle */}
        <aside className="w-1/3 bg-gray-100 p-6">
          <h3 className="text-lg font-semibold mb-4">💡 Sample Queries</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-gray-700">
            {examples.length ? examples.map((e, i) => (
              <li key={i} onClick={() => setQuestion(e)} className="cursor-pointer hover:underline">
                {e}
              </li>
            )) : <li>Loading examples...</li>}
          </ul>

          <div className="mt-6">
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={useMemory}
                onChange={() => setUseMemory(!useMemory)}
              />
              Multi-turn memory
            </label>
          </div>
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

      {/* Feedback Modal */}
      {showFeedback && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg w-[90%] max-w-md shadow-lg">
            <h3 className="text-lg font-semibold mb-2">Rate this response</h3>
            <label className="block text-sm mb-1">Rating (1-5):</label>
            <input
              type="number"
              min="1"
              max="5"
              value={feedbackRating}
              onChange={(e) => setFeedbackRating(Number(e.target.value))}
              className="w-full p-2 border border-gray-300 rounded mb-3"
            />
            <label className="block text-sm mb-1">Comment (optional):</label>
            <textarea
              rows="3"
              value={feedbackComment}
              onChange={(e) => setFeedbackComment(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded"
            />

            <div className="flex justify-end gap-3 mt-4">
              <button onClick={() => setShowFeedback(false)} className="text-gray-500 hover:underline text-sm">Cancel</button>
              <button onClick={submitFeedback} className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">Submit</button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
};

export default AskAgent;
