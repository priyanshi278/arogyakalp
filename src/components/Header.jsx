import React from 'react';

const Header = ({ user, onLogout }) => {
  return (
    <header className="header animate-fade-down" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <h1 className="h1">ArogyaKalp</h1>
        <p className="p" style={{ color: 'var(--color-text-muted)', marginTop: '0.25rem' }}>
          AI Clinical Decision Support System
        </p>
        <div className="badge badge-info" style={{ marginTop: '1rem' }}>
          Smart Drug Safety & Recommendation Assistant
        </div>
      </div>
      
      {user && (
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontWeight: '600', color: 'var(--color-primary)' }}>
            Dr. {user.name}
          </div>
          <button 
            onClick={onLogout}
            style={{ 
              background: 'none', 
              border: 'none', 
              color: 'var(--color-text-muted)', 
              fontSize: '0.8rem', 
              cursor: 'pointer',
              padding: '0',
              textDecoration: 'underline'
            }}
          >
            Logout
          </button>
        </div>
      )}
    </header>
  );
};

export default Header;
