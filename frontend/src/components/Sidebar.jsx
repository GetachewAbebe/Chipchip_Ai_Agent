import React from "react";
import "./Sidebar.css";

const Sidebar = ({ setQuestion }) => {
  const examples = [
    "Top 3 selling items last month",
    "Which group leaders had no orders yesterday?",
    "Peak shopping hours for Working Professionals",
  ];

  return (
    <div className="sidebar">
      <img src="/logo.png" alt="ChipChip Logo" className="logo" />
      <p className="intro">Ask about your marketplace in plain English 👇</p>
      <ul className="example-list">
        {examples.map((q, i) => (
          <li key={i} onClick={() => setQuestion(q)}>{q}</li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
