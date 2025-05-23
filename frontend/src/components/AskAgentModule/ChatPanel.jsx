import React from "react";
import ChatMessage from "./ChatMessage";
import TypingDots from "./TypingDots";
import ChatInput from "./ChatInput";

const ChatPanel = ({
  messages,
  loading,
  scrollRef,
  question,
  setQuestion,
  chat,
}) => {
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chat();
    }
  };

  return (
    <main className="w-full md:w-3/4 p-4 md:p-6 flex flex-col">
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-lg font-semibold">🧠 Chat</h2>
        <button
          onClick={() => window.location.reload()}
          className="text-sm text-red-600 hover:underline"
        >
          🗑️ New Chat
        </button>
      </div>

      {/* Chat Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-4 px-1">
        {messages.map((msg, idx) => (
          <ChatMessage key={idx} msg={msg} />
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

      {/* Input */}
      <ChatInput
        question={question}
        setQuestion={setQuestion}
        chat={chat}
        handleKeyDown={handleKeyDown}
      />
    </main>
  );
};

export default ChatPanel;
