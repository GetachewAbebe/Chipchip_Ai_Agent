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
    // ⚠️ Replace with parsed data once backend returns structured chart data
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
            title: { display: true, text: "Top Selling Produce" }
          }
        }}
      />
    );
  };

  return (
    <div style={{ maxWidth: "700px", margin: "auto", padding: "2rem" }}>
      <h2>💬 Ask Marketing Agent</h2>
      <textarea
        rows="4"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Type a question like: 'Top 3 produce items in April?'"
        style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem" }}
      />
      <button onClick={ask} disabled={loading}>
        {loading ? "Loading..." : "Ask"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {answer && (
        <div style={{ marginTop: "1rem" }}>
          <h4>📋 Answer:</h4>
          <pre>{answer}</pre>
          <hr />
          <h4>📊 Chart (Example):</h4>
          {renderChart()}
        </div>
      )}
    </div>
  );
};

export default AskAgent;
