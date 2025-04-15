import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="container">
        <div className="logo">
          <Link to="/">TestFastApi</Link>
        </div>
        <nav className="nav">
          <ul>
            <li><Link to="/">홈</Link></li>
            <li><Link to="/users">사용자</Link></li>
            <li><Link to="/categories">카테고리</Link></li>
            <li><Link to="/hydrogen-stations">수소 스테이션</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
