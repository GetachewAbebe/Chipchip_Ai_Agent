import { useEffect, useRef, useState } from "react";
import { v4 as uuidv4 } from "uuid";

const BACKEND_URL = "https://chipchip-ai-agent-backend.onrender.com";
const CHAT_HISTORY_KEY = "chipchip_chat_history";

export const useChatManager = () => {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(uuidv4());
  const [loading, setLoading] = useState(false);
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);
  const [activeDropdownId, setActiveDropdownId] = useState(null);

  const scrollRef = useRef(null);
  const dropdownRefs = useRef({});

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

  useEffect(() => {
    const handleClickOutside = (e) => {
      const ref = dropdownRefs.current[activeDropdownId];
      if (ref && !ref.contains(e.target)) {
        setActiveDropdownId(null);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [activeDropdownId]);

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

  return {
    question,
    setQuestion,
    messages,
    setMessages,
    chatHistory,
    setChatHistory,
    currentChatId,
    setCurrentChatId,
    loading,
    confirmDeleteId,
    setConfirmDeleteId,
    activeDropdownId,
    setActiveDropdownId,
    scrollRef,
    dropdownRefs,
    chat,
  };
};
