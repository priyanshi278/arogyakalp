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
    <div className="auth-container">
      <div className="auth-card animate-fade-up">
        <div className="auth-header">
          <h1>ArogyaKalp</h1>
          <p style={{ color: 'var(--color-text-muted)' }}>Doctor Portal Access</p>
        </div>

        <div className="auth-toggle">
          <button 
            className={isLogin ? 'active' : ''} 
            onClick={() => setIsLogin(true)}
          >
            Login
          </button>
          <button 
            className={!isLogin ? 'active' : ''} 
            onClick={() => setIsLogin(false)}
          >
            Signup
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group" style={{ marginBottom: '1.5rem' }}>
            <label>IMR Number</label>
            <input 
              type="text" 
              className="input" 
              placeholder="e.g. IMR-12345"
              value={formData.imr_number}
              onChange={(e) => setFormData({...formData, imr_number: e.target.value})}
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group" style={{ marginBottom: '1.5rem' }}>
              <label>Full Name</label>
              <input 
                type="text" 
                className="input" 
                placeholder="Dr. John Doe"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
            </div>
          )}

          <div className="form-group" style={{ marginBottom: '2rem' }}>
            <label>Phone Number</label>
            <input 
              type="tel" 
              className="input" 
              placeholder="e.g. +91 9876543210"
              value={formData.phone_number}
              onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
              required
            />
          </div>

          {error && (
            <div style={{ color: '#ef4444', marginBottom: '1.5rem', fontSize: '0.9rem', textAlign: 'center' }}>
              {error}
            </div>
          )}

          <button 
            type="submit" 
            className="btn btn-primary" 
            style={{ width: '100%', padding: '1rem' }}
            disabled={isLoading}
          >
            {isLoading ? 'Processing...' : (isLogin ? 'Login' : 'Create Account')}
          </button>
        </form>

        <div className="auth-footer">
          <p>© 2026 ArogyaKalp AI • Medical Verification Required</p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
