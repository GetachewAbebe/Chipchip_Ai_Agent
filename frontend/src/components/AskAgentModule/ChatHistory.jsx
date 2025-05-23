import React from "react";
import jsPDF from "jspdf";

const ChatHistory = ({
  chatHistory,
  currentChatId,
  setCurrentChatId,
  setMessages,
  setChatHistory,
  setConfirmDeleteId,
  activeDropdownId,
  setActiveDropdownId,
  dropdownRefs,
}) => {
  const loadChat = (chatItem) => {
    setCurrentChatId(chatItem.id);
    setMessages(chatItem.messages || []);
  };

  const renameChat = (chatId) => {
    const newName = window.prompt("Enter new chat name:");
    if (!newName) return;
    const updated = chatHistory.map(chat =>
      chat.id === chatId ? { ...chat, name: newName } : chat
    );
    setChatHistory(updated);
    localStorage.setItem("chipchip_chat_history", JSON.stringify(updated));
  };

  const downloadChat = (chatItem) => {
    const doc = new jsPDF();
    doc.setFontSize(14);
    doc.text(chatItem.name, 10, 10);
    doc.setFontSize(10);
    let y = 20;

    chatItem.messages.forEach((msg) => {
      const prefix = msg.sender === "user" ? "🙂 You: " : "🤖 Bot: ";
      const lines = doc.splitTextToSize(prefix + msg.text, 180);
      if (y + lines.length * 7 > 280) {
        doc.addPage();
        y = 10;
      }
      doc.text(lines, 10, y);
      y += lines.length * 7;
    });

    doc.save(`${chatItem.name || "Chat"}.pdf`);
  };

  return (
    <aside className="w-full md:w-1/4 bg-gray-100 p-4 md:p-6 overflow-y-auto border-b md:border-b-0 md:border-r border-gray-200">
      <h3 className="text-lg font-semibold mb-4 text-center">🗂️ Chat History</h3>
      <ul className="space-y-2 text-sm">
        {chatHistory.map((chatItem) => (
          <li
            key={chatItem.id}
            className={`relative group px-2 py-1 rounded hover:bg-gray-200 ${
              chatItem.id === currentChatId ? "bg-white font-bold" : ""
            }`}
          >
            <div className="cursor-pointer pr-6" onClick={() => loadChat(chatItem)}>
              {chatItem.name}
            </div>

            {/* ⋯ Dropdown */}
            <div className="absolute top-1 right-1 text-gray-500">
              <button
                className="text-lg"
                onClick={() =>
                  setActiveDropdownId(prev => prev === chatItem.id ? null : chatItem.id)
                }
              >
                ⋯
              </button>

              {activeDropdownId === chatItem.id && (
                <>
                  {/* Overlay */}
                  <div
                    className="fixed inset-0 bg-black bg-opacity-40 z-40"
                    onClick={() => setActiveDropdownId(null)}
                  />

                  {/* Dropdown */}
                  <div
                    ref={(el) => (dropdownRefs.current[chatItem.id] = el)}
                    className="absolute bottom-full right-0 mb-2 w-36 bg-white border rounded shadow z-50 transition-all animate-fadeIn"
                  >
                    <button
                      onClick={() => renameChat(chatItem.id)}
                      className="block w-full px-4 py-2 hover:bg-gray-100 text-left"
                    >
                      Rename
                    </button>
                    <button
                      onClick={() => setConfirmDeleteId(chatItem.id)}
                      className="block w-full px-4 py-2 hover:bg-gray-100 text-left text-red-500"
                    >
                      Delete
                    </button>
                    <button
                      onClick={() => downloadChat(chatItem)}
                      className="block w-full px-4 py-2 hover:bg-gray-100 text-left"
                    >
                      Download PDF
                    </button>
                  </div>
                </>
              )}
            </div>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default ChatHistory;
