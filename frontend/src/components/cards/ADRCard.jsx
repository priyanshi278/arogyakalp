import React, { useState } from 'react';

const ADRCard = ({ adrs }) => {
  const [expanded, setExpanded] = useState(false);

  if (!adrs || adrs.length === 0) return null;

  return (
    <div className="glass-panel section-card">
      <div className="section-head" style={{ fontSize: '1rem' }}><span>⚠️</span> Predicted Adverse Drug Reactions (ADR)</div>
      
      {adrs.map((adr, i) => (
        <div key={i} style={{ marginBottom: i < adrs.length - 1 ? '1.5rem' : 0 }}>
          <h4 style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--medical-slate)', marginBottom: '0.75rem' }}>{adr.drug}</h4>
          
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {adr.effects.slice(0, expanded ? adr.effects.length : 3).map((effect, j) => {
              // MVP logic for severity coloring
              let bg = 'var(--medical-slate-muted)';
              let color = '#FFF';
              if (j === 0) { bg = '#DC2626'; color = '#FFF'; } // Dark Red
              else if (j === 1) { bg = '#F97316'; color = '#FFF'; } // Orange
              else if (j === 2) { bg = '#FBBF24'; color = '#000'; } // Yellow
              else { bg = '#E2E8F0'; color = '#475569'; } // Gray

              return (
                <span key={j} style={{
                    padding: '0.25rem 0.75rem',
                    borderRadius: '16px',
                    fontSize: '0.8rem',
                    fontWeight: 600,
                    background: bg,
                    color: color,
                    border: bg === '#E2E8F0' ? '1px solid #CBD5E1' : 'none'
                }}>
                    {effect}
                </span>
              );
            })}
            
            {adr.effects.length > 3 && (
              <button 
                onClick={() => setExpanded(!expanded)}
                style={{
                  background: 'none',
                  border: '1px dashed var(--medical-indigo)',
                  color: 'var(--medical-indigo)',
                  padding: '0.25rem 0.75rem',
                  borderRadius: '16px',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                {expanded ? 'Show Less' : `+${adr.effects.length - 3} More`}
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ADRCard;
