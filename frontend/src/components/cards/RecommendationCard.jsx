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
          borderRadius: '0 8px 8px 0',
          marginBottom: '1rem'
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
            <div style={{ marginLeft: '1rem', padding: '1rem', borderTop: '1px solid #E2E8F0', background: '#F8FAFC', borderRadius: '4px' }}>
                <strong style={{ fontSize: '0.85rem', color: 'var(--medical-indigo)', textTransform: 'uppercase' }}>✅ Recommended Alternative:</strong>
                <p style={{ fontSize: '0.95rem', fontWeight: 600, marginTop: '0.25rem', color: '#0F172A' }}>{rec.alternative}</p>
            </div>
        )}
    </div>
  );
};

export default RecommendationCard;
