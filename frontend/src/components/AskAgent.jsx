import React, { useState } from "react";
import Sidebar from "./Sidebar";
import Footer from "./Footer";
import "./AskAgent.css";

const AskAgent = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const ask = async () => {
    setLoading(true);
    setError("");
    setAnswer(null);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Something went wrong");

      setAnswer(data.answer);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  return (
    <div className="page">
      <Sidebar setQuestion={setQuestion} />
      <div className="main">
        <textarea
          rows="3"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something like: 'Top 3 items this week?'"
        />
        <button onClick={ask} className="ask-button" disabled={loading}>
          {loading ? "Loading..." : "Ask"}
        </button>

        {error && <p className="error">{error}</p>}
        {answer && (
          <div className="answer">
            <h4>📋 Answer:</h4>
            <pre>{answer}</pre>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default AskAgent;
