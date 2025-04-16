import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; {new Date().getFullYear()} TestFastApi. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
