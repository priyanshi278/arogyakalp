import React from 'react';

const Header = ({ user, onLogout }) => {
  return (
    <nav className="app-nav glass-panel" style={{ margin: '1rem', marginTop: '1rem' }}>
      <div className="brand">
        <div className="brand-dot"></div>
        <div>
          <h1>ArogyaKalp</h1>
          <p style={{ fontSize: '0.7rem', color: '#94a3b8', letterSpacing: '1px' }}>AI CLINICAL DECISION SUPPORT</p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
        <div className="badge badge-info" style={{ borderRadius: '8px', fontSize: '0.75rem' }}>
          Smart Drug Safety & Recommendation Assistant
        </div>
        
        {user && (
          <div className="user-profile">
            <div className="avatar">
              {user.name.charAt(0).toUpperCase()}
            </div>
            <div style={{ textAlign: 'left' }}>
              <div style={{ fontWeight: '600', fontSize: '0.9rem' }}>
                Dr. {user.name}
              </div>
              <button 
                onClick={onLogout}
                style={{ 
                  background: 'none', 
                  border: 'none', 
                  color: '#94a3b8', 
                  fontSize: '0.75rem', 
                  cursor: 'pointer',
                  padding: '0'
                }}
              >
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Header;
