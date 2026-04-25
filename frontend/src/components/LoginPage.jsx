import React, { useState } from 'react';

const LoginPage = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    imr_number: '',
    name: '',
    phone_number: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const endpoint = isLogin ? '/api/login' : '/api/signup';
    
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      let data;
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.indexOf("application/json") !== -1) {
        data = await response.json();
      } else {
        const text = await response.text();
        throw new Error(text || `Server error: ${response.status}`);
      }

      if (!response.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      onLogin(data.user);
    } catch (err) {
      setError(err.message || 'Connection to server failed. Please check if the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-wrapper fade-in">
      <div className="auth-panel glass-panel section-card">
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h2 className="brand-font" style={{ fontSize: '1.5rem', color: 'var(--medical-slate)', marginBottom: '0.25rem' }}>
            AROGYAKALP MEDICAL
          </h2>
          <p style={{ color: 'var(--medical-slate-muted)', fontSize: '0.875rem', fontWeight: '500' }}>
            Clinical Portal Access
          </p>
        </div>

        <div className="medical-tabs">
          <button 
            className={`medical-tab ${isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(true)}
            type="button"
          >
            Login
          </button>
          <button 
            className={`medical-tab ${!isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(false)}
            type="button"
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit} className="assessment-form">
          <div className="form-field">
            <span className="field-label">IMR Number</span>
            <input 
              type="text" 
              className="medical-input" 
              placeholder="e.g. IMR-12345"
              value={formData.imr_number}
              onChange={(e) => setFormData({...formData, imr_number: e.target.value})}
              required
            />
          </div>

          {!isLogin && (
            <div className="form-field">
              <span className="field-label">Full Name</span>
              <input 
                type="text" 
                className="medical-input" 
                placeholder="Dr. John Doe"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
            </div>
          )}

          <div className="form-field" style={{ marginBottom: '0.5rem' }}>
            <span className="field-label">Phone Number</span>
            <input 
              type="tel" 
              className="medical-input" 
              placeholder="e.g. +91 9876543210"
              value={formData.phone_number}
              onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
              required
            />
          </div>

          {error && (
            <div className="risk-alert-banner" style={{ background: 'var(--warning)', padding: '0.75rem', fontSize: '0.875rem', margin: '0.5rem 0', position: 'relative' }}>
              {error}
            </div>
          )}

          <button 
            type="submit" 
            className="btn-med btn-primary" 
            style={{ width: '100%', marginTop: '1rem', padding: '0.75rem' }}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <div className="spinner" style={{ width: '1rem', height: '1rem', borderWidth: '2px' }}></div>
                Processing...
              </>
            ) : (isLogin ? 'Secure Login' : 'Register Provider')}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '2rem', fontSize: '0.75rem', color: '#94a3b8', letterSpacing: '0.5px' }}>
          &copy; 2026 ArogyaKalp AI &bull; Encrypted Portal
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
