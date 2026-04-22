import React from 'react';

const NormalizedDrugCard = ({ drugs }) => {
  if (drugs.length === 0) return null;

  return (
    <div className="card animate-fade-up stagger-3">
      <div className="card-header">
        <span className="icon">💊</span>
        <h3 className="h3">Drug Normalization</h3>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontWeight: '600', marginBottom: '0.5rem' }}>
        <div className="text-muted text-sm">Original</div>
        <div className="text-muted text-sm">Generic</div>
      </div>
      <div style={{ display: 'grid', gap: '0.5rem' }}>
        {drugs.map((drug, idx) => (
          <div key={idx} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
            <div className="badge badge-neutral" style={{ textAlign: 'center' }}>{drug.original}</div>
            <div className="badge badge-info" style={{ textAlign: 'center' }}>{drug.generic}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NormalizedDrugCard;
