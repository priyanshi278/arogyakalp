import React from 'react';

const ADRCard = ({ adrs }) => {
  if (adrs.length === 0) return null;

  return (
    <div className="card animate-fade-up stagger-4">
      <div className="card-header">
        <span className="icon">⚠️</span>
        <h3 className="h3">Predicted Side Effects (ADR)</h3>
      </div>
      <div style={{ display: 'grid', gap: '1rem' }}>
        {adrs.map((adr, idx) => (
          <div key={idx} style={{ padding: '0.75rem', backgroundColor: 'var(--color-bg-body)', borderRadius: 'var(--radius-md)' }}>
            <div className="badge badge-warning" style={{ marginBottom: '0.5rem' }}>{adr.drug}</div>
            <ul className="bullet-list text-sm">
              {adr.side_effects.map((se, i) => <li key={i}>{se}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ADRCard;
