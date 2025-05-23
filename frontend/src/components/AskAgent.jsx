import React from "react";
import Header from "./Header";
import Footer from "./Footer";

import ChatPanel from "./AskAgentModule/ChatPanel";
import ChatHistory from "./AskAgentModule/ChatHistory";
import DeleteModal from "./AskAgentModule/DeleteModal";
import { useChatManager } from "./AskAgentModule/useChatManager";

const AskAgent = () => {
  const {
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
  } = useChatManager();

  const deleteChat = (chatId) => {
    const filtered = chatHistory.filter(chat => chat.id !== chatId);
    setChatHistory(filtered);
    localStorage.setItem("chipchip_chat_history", JSON.stringify(filtered));
    if (chatId === currentChatId) {
      setMessages([]);
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <div className="flex flex-1 flex-col md:flex-row">
        <ChatHistory
          chatHistory={chatHistory}
          currentChatId={currentChatId}
          setCurrentChatId={setCurrentChatId}
          setMessages={setMessages}
          setChatHistory={setChatHistory}
          setConfirmDeleteId={setConfirmDeleteId}
          activeDropdownId={activeDropdownId}
          setActiveDropdownId={setActiveDropdownId}
          dropdownRefs={dropdownRefs}
        />

        <ChatPanel
          messages={messages}
          loading={loading}
          scrollRef={scrollRef}
          question={question}
          setQuestion={setQuestion}
          chat={chat}
        />
      </div>

      {confirmDeleteId && (
        <DeleteModal
          confirmDeleteId={confirmDeleteId}
          setConfirmDeleteId={setConfirmDeleteId}
          deleteChat={deleteChat}
        />
      )}

      <Footer />
    </div>
  );
};

export default AskAgent;
