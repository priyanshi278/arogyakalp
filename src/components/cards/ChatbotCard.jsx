import React from 'react';

const ChatbotCard = ({ response }) => {
  if (!response) return null;

  return (
    <section className="card animate-fade-up stagger-1" style={{ borderLeft: '4px solid var(--color-primary)' }}>
      <div className="card-header">
        <span className="icon">🤖</span>
        <h2 className="h2">AI Clinical Assessment</h2>
      </div>
      <div style={{ lineHeight: '1.6', fontSize: '1.1rem' }}>
        <p>{response}</p>
      </div>
    </section>
  );
};

export default ChatbotCard;
