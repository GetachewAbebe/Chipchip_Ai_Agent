import React from "react";

const ChatMessage = ({ msg }) => {
  return (
    <div
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
  );
};

export default ChatMessage;
