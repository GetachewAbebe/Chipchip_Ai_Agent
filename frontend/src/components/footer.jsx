import React from "react";
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-main">
        <div>
          <h2 className="footer-logo">ChipChip Logo</h2>
          <p>
            Social buying platform that connects customers directly to farmers, bypassing traditional supply chains and allowing for group buying.
          </p>
          <a href="#" className="super-leader-link">How to become a ChipChip Super Leader →</a>
        </div>
        <div className="footer-links">
          <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">Service</a></li>
            <li><a href="#">About Us</a></li>
            <li><a href="#">How it Works</a></li>
            <li><a href="#">Download</a></li>
            <li><a href="#">FAQ</a></li>
            <li><a href="#">News</a></li>
            <li><a href="#">Careers</a></li>
          </ul>
        </div>
      </div>
      <div className="footer-bottom">
        <p>© 2025 All Rights Reserved — ChipChip Inc.</p>
        <div className="legal-links">
          <a href="#">Privacy Policy</a>
          <a href="#">Terms and Conditions</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
