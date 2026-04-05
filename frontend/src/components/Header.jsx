import React from 'react';

const Header = () => {
  return (
    <header className="app-header">
      <h1 className="h1">ArogyaKalp</h1>
      <p className="text-muted" style={{ fontSize: '1.25rem', marginTop: '0.5rem' }}>
        AI Clinical Decision Support System
      </p>
      <div className="badge badge-info" style={{ marginTop: '1rem' }}>
        Smart Drug Safety & Recommendation Assistant
      </div>
    </header>
  );
};

export default Header;
