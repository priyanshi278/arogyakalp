import React from 'react';

const RecommendationCard = ({ recommendations }) => {
  if (recommendations.length === 0) return null;

  return (
    <div className="card animate-fade-up stagger-6">
      <div className="card-header">
        <span className="icon">💡</span>
        <h3 className="h3">Recommendations</h3>
      </div>
      <div style={{ display: 'grid', gap: '0.75rem' }}>
        {recommendations.map((rec, idx) => (
          <div key={idx} style={{ 
            padding: '1rem', 
            borderRadius: 'var(--radius-md)', 
            backgroundColor: 'var(--color-info-bg)',
            border: '1px solid var(--color-info-border)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <div className="badge badge-neutral">{rec.drug}</div>
              <span style={{ fontSize: '0.8rem', color: 'var(--color-primary)', fontWeight: '600' }}>{rec.issue}</span>
            </div>
            <div style={{ padding: '0.5rem', backgroundColor: 'white', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-border)' }}>
              <span className="text-muted text-sm">Suggested alternative:</span>
              <div style={{ fontWeight: '700', color: 'var(--color-success-text)' }}>{rec.alternative}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationCard;
