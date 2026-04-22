import React from 'react';

const EntityCard = ({ drugs, diseases, allergies }) => {
  return (
    <div className="card animate-fade-up stagger-2">
      <div className="card-header">
        <span className="icon">🧪</span>
        <h3 className="h3">Detected Entities</h3>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr)', gap: '1rem' }}>
        <div>
          <div className="text-muted text-sm" style={{ marginBottom: '0.25rem', fontWeight: '600' }}>💊 Drugs</div>
          {drugs.length > 0 ? (
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {drugs.map((d, i) => <span key={i} className="badge badge-info">{d.original}</span>)}
            </div>
          ) : <span className="text-muted text-sm italic">None detected</span>}
        </div>
        <div>
          <div className="text-muted text-sm" style={{ marginBottom: '0.25rem', fontWeight: '600' }}>🩺 Diseases</div>
          {diseases.length > 0 ? (
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {diseases.map((d, i) => <span key={i} className="badge badge-neutral">{d}</span>)}
            </div>
          ) : <span className="text-muted text-sm italic">None detected</span>}
        </div>
        <div>
          <div className="text-muted text-sm" style={{ marginBottom: '0.25rem', fontWeight: '600' }}>⚠️ Allergies</div>
          {allergies.length > 0 ? (
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {allergies.map((a, i) => <span key={i} className="badge badge-danger">{a}</span>)}
            </div>
          ) : <span className="text-muted text-sm italic">None detected</span>}
        </div>
      </div>
    </div>
  );
};

export default EntityCard;
