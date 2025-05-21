import React from 'react';
import logo from '../assets/logo.png';

const Header = () => {
  return (
    <header className="w-full h-[60px] bg-white text-black flex justify-center items-center border-b">
      <div className="flex items-center justify-center gap-6 max-w-[1000px] w-full px-4">
        <img src={logo} alt="ChipChip Logo" className="h-9 w-auto" />
        <h1 className="text-xl font-semibold">ChipChip Marketing Insights Agent</h1>
      </div>
    </header>
  );
};

export default Header;
