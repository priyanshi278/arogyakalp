import React from 'react';

const RecommendationCard = ({ rec }) => {
  if (!rec) return null;

  const isDanger = rec.decision.includes('Avoid');
  const isCaution = rec.decision.includes('Caution');

  let headerColor = 'var(--success)';
  let headerBg = 'var(--success-soft)';
  if (isDanger) { headerColor = 'var(--danger)'; headerBg = 'var(--danger-soft)'; }
  else if (isCaution) { headerColor = 'var(--warning)'; headerBg = 'var(--warning-soft)'; }

  return (
    <div className="glass-panel section-card">
      <div className="section-head" style={{ fontSize: '1rem' }}><span>💡</span> Clinical Recommendation</div>
      
        <div style={{
          borderLeft: `4px solid ${headerColor}`,
          padding: '1.25rem',
          background: headerBg,
          borderRadius: '8px',
          marginBottom: '1rem',
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <h4 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem', color: headerColor }}>{rec.drug}</h4>
              <div style={{ fontSize: '1rem', fontWeight: 700, color: '#1E293B', marginBottom: '0.5rem' }}>
                {rec.decision}
              </div>
              <p style={{ fontSize: '0.9rem', color: '#475569', marginBottom: '0.5rem' }}>{rec.reason}</p>
              
              <div style={{ marginTop: '0.75rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                <span style={{ color: 'var(--medical-indigo)' }}>⚠️</span>
                <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--medical-slate)' }}>Monitoring: {rec.monitoring}</span>
              </div>
            </div>
          </div>
        </div>

        {rec.alternative && rec.alternative !== "N/A" && (
            <div style={{ 
              borderLeft: '4px solid var(--success)', 
              padding: '1.25rem', 
              background: 'var(--success-soft)', 
              borderRadius: '8px',
              boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
            }}>
                <strong style={{ fontSize: '0.9rem', color: 'var(--success)', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span>✅</span> RECOMMENDED ALTERNATIVE:
                </strong>
                <p style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '0.5rem', color: '#0F172A' }}>{rec.alternative}</p>
            </div>
        )}
    </div>
  );
};

export default RecommendationCard;
