import React from "react";
import { IoPaperPlaneOutline } from "react-icons/io5";

const ChatInput = ({ question, setQuestion, chat, handleKeyDown }) => {
  return (
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
  );
};

export default ChatInput;
