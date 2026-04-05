import React from 'react';

const DDICard = ({ interactions }) => {
  if (interactions.length === 0) return null;

  const getInteractionStyle = (desc) => {
    const text = desc.toLowerCase();
    if (text.includes('danger') || text.includes('warning') || text.includes('severe') || text.includes('fatal')) {
      return { bg: 'var(--color-danger-bg)', border: 'var(--color-danger-border)', text: 'var(--color-danger-text)', label: 'DANGER' };
    }
    if (text.includes('caution') || text.includes('moderate') || text.includes('monitoring')) {
      return { bg: 'var(--color-warning-bg)', border: 'var(--color-warning-border)', text: 'var(--color-warning-text)', label: 'CAUTION' };
    }
    return { bg: 'var(--color-success-bg)', border: 'var(--color-success-border)', text: 'var(--color-success-text)', label: 'SAFE' };
  };

  return (
    <div className="card animate-fade-up stagger-5">
      <div className="card-header">
        <span className="icon">🔄</span>
        <h3 className="h3">Drug Interactions (DDI)</h3>
      </div>
      <div style={{ display: 'grid', gap: '1rem' }}>
        {interactions.map((ddi, idx) => {
          const style = getInteractionStyle(ddi.interaction);
          return (
            <div key={idx} style={{ 
              padding: '1rem', 
              borderRadius: 'var(--radius-md)', 
              backgroundColor: style.bg,
              border: `1px solid ${style.border}`,
              position: 'relative'
            }}>
              <div style={{ position: 'absolute', top: '0.5rem', right: '0.75rem', fontSize: '0.65rem', fontWeight: '800', color: style.text }}>
                {style.label}
              </div>
              <div style={{ color: style.text, fontWeight: '700', marginBottom: '0.25rem' }}>
                {ddi.drug_pair.join(' + ')}
              </div>
              <p className="text-sm" style={{ color: style.text }}>
                {ddi.interaction}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DDICard;
