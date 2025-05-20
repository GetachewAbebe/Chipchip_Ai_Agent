import React, { useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";
import "./AskAgent.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

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
        body: JSON.stringify({ question })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Something went wrong");

      setAnswer(data.answer);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  const renderChart = () => {
    const dummyLabels = ["Tomato", "Banana", "Apple"];
    const dummyData = [100, 120, 90];

    return (
      <Bar
        data={{
          labels: dummyLabels,
          datasets: [
            {
              label: "Units Sold",
              data: dummyData,
              backgroundColor: "#3b82f6"
            }
          ]
        }}
        options={{
          responsive: true,
          plugins: {
            legend: { position: "top" },
            title: { display: true, text: "Top Selling Items" }
          }
        }}
      />
    );
  };

  return (
    <div className="ask-container">
      <h2 className="section-title">Ask a Question</h2>
      <textarea
        className="question-box"
        rows="4"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="e.g., Top 3 produce items in August?"
      />
      <button className="ask-button" onClick={ask} disabled={loading}>
        {loading ? "Loading..." : "Ask"}
      </button>

      {error && <p className="error-msg">{error}</p>}

      {answer && (
        <div className="answer-section">
          <h4>Answer:</h4>
          <pre className="answer-text">{answer}</pre>
          <hr style={{ margin: "1rem 0" }} />
          <h4>Chart View (Example):</h4>
          {renderChart()}
        </div>
      )}
    </div>
  );
};

export default AskAgent;
