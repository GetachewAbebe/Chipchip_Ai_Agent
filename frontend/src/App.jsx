import React from "react";
import AskAgent from "./components/AskAgent";
import Footer from "./components/Footer";
import logo from "./assets/logo.png";

function App() {
  return (
    <div className="container">
      <header style={{ textAlign: "center", marginTop: "2rem" }}>
        <img src={logo} alt="ChipChip Logo" style={{ height: "80px" }} />
        <h1 className="title">ChipChip Dashboard</h1>
      </header>

      <AskAgent />
      <Footer />
    </div>
  );
}

export default App;
