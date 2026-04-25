import React from 'react';
import ADRCard from './cards/ADRCard';
import RecommendationCard from './cards/RecommendationCard';

const Results = ({ data, chatResponse, isLoading }) => {
  if (isLoading) {
    return (
      <div className="glass-panel section-card fade-in" style={{ textAlign: 'center', padding: '4rem', marginTop: '2rem' }}>
        <div className="spinner" style={{ margin: '0 auto 1.5rem', width: '40px', height: '40px', borderTopColor: 'var(--medical-indigo)' }}></div>
        <h3 className="h3">Running Clinical Risk Engine...</h3>
        <p className="text-muted">Cross-referencing DDI datasets and analyzing patient risk context.</p>
      </div>
    );
  }

  if (!data) return null;

  const riskLevel = data.risk_level?.toUpperCase() || 'LOW';

  let confidence = 'Low (Rule-based estimate)';
  if (riskLevel === 'DANGEROUS' || riskLevel === 'HIGH') confidence = 'High (Rule-based estimate)';
  else if (riskLevel === 'MODERATE') confidence = 'Moderate (Rule-based estimate)';

  return (
    <div className="fade-in" style={{ display: 'grid', gap: '1.5rem', marginTop: '1rem' }}>
      
      {/* Credibility Layer */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '-0.5rem' }}>
         <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--medical-slate-muted)', background: '#E2E8F0', padding: '0.2rem 0.6rem', borderRadius: '4px' }}>
            Evidence Level: Prototype dataset (Not Clinically Validated)
         </span>
         <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--medical-indigo)', background: '#E0E7FF', padding: '0.2rem 0.6rem', borderRadius: '4px' }}>
            Interaction Confidence: {confidence}
         </span>
      </div>

      {/* Risk Summary Card */}
      <div className="glass-panel section-card" style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
         <div style={{ padding: '1.5rem', borderRadius: '8px', border: `2px solid var(--${riskLevel === 'DANGEROUS' || riskLevel === 'HIGH' ? 'danger' : riskLevel === 'MODERATE' ? 'warning' : 'success'})`, background: `var(--${riskLevel === 'DANGEROUS' || riskLevel === 'HIGH' ? 'danger' : riskLevel === 'MODERATE' ? 'warning' : 'success'}-soft)`, textAlign: 'center', minWidth: '150px' }}>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: '0.5rem', opacity: 0.8 }}>Risk Level Assessment</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800 }}>{riskLevel}</div>
         </div>
         
         <div style={{ flex: 1 }}>
            <h4 style={{ marginBottom: '0.5rem', fontSize: '1rem', fontWeight: 600 }}>Clinical Alerts</h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
               {data.alerts?.length > 0 ? data.alerts.map((alert, i) => (
                   <li key={i} style={{ 
                       padding: '0.5rem 0', 
                       borderBottom: i < data.alerts.length -1 ? '1px solid #E5E7EB' : 'none',
                       fontSize: '0.9rem',
                       display: 'flex',
                       gap: '0.5rem',
                       alignItems: 'baseline'
                   }}>
                       <span style={{ color: 'var(--danger)' }}>⚠️</span> {alert}
                   </li>
               )) : <li style={{ fontSize: '0.9rem', color: 'var(--medical-slate-muted)' }}>No critical alerts identified for this patient configuration.</li>}
            </ul>
         </div>
      </div>

      {/* Clinical Recommendation Panel */}
      {data.recommendation && (
         <RecommendationCard rec={data.recommendation} />
      )}

      {/* Chat / Clinical Explanation */}
      {chatResponse && (
      <div className="glass-panel section-card ai-card">
         <div className="section-head" style={{ fontSize: '1rem', color: 'var(--medical-indigo)' }}>
           <span>🗣️</span> Clinical Explanation
         </div>
         <div className="ai-markdown" style={{ paddingLeft: '0.5rem', fontSize: '0.95rem' }}>
            {chatResponse.split('\n').map((line, i) => (
                <p key={i} style={{ marginBottom: '0.5rem' }}>{line}</p>
            ))}
         </div>
      </div>
      )}

      {/* Detailed Data: DDI Table */}
      <div className="glass-panel section-card">
          <div className="section-head" style={{ fontSize: '1rem' }}><span>🔄</span> Identified Drug-Drug Interactions (DDI)</div>
          
          {data.ddi && data.ddi.length > 0 ? (
            <div style={{ overflowX: 'auto' }}>
                <table className="medical-table">
                    <thead>
                        <tr>
                            <th>Drug Pair</th>
                            <th>Clinical Severity</th>
                            <th>Clinical Meaning</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.ddi.map((itx, i) => {
                            let rowLabel = 'Safe to use';
                            let rowClass = 'success';
                            if (itx.severity === 'DANGEROUS') { rowLabel = 'Severe Interaction'; rowClass = 'danger'; }
                            else if (itx.severity === 'RISKY' || itx.severity === 'HIGH') { rowLabel = 'High Risk'; rowClass = 'danger'; }
                            else if (itx.severity === 'CAUTION' || itx.severity === 'MODERATE') { rowLabel = 'Moderate Interaction'; rowClass = 'warning'; }

                            if (!itx.drug_a || itx.drug_a.length === 0) {
                                return (
                                   <tr key={i}>
                                       <td style={{ fontWeight: 600 }}>N/A</td>
                                       <td><span style={{ padding: '0.25rem 0.75rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 700, background: 'var(--success-soft)', color: 'var(--success)' }}>No Issue</span></td>
                                       <td style={{ fontSize: '0.85rem', lineHeight: '1.4' }}>{itx.meaning}</td>
                                   </tr>
                                );
                            }

                            return (
                                <tr key={i}>
                                    <td style={{ fontWeight: 600 }}>{itx.drug_a} + {itx.drug_b}</td>
                                    <td>
                                        <span style={{ 
                                            padding: '0.25rem 0.75rem', 
                                            borderRadius: '4px', 
                                            fontSize: '0.8rem', 
                                            fontWeight: 700, 
                                            background: `var(--${rowClass}-soft)`,
                                            color: `var(--${rowClass})`
                                        }}>
                                            {rowLabel}
                                        </span>
                                    </td>
                                    <td style={{ fontSize: '0.85rem', lineHeight: '1.4' }}>{itx.meaning}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
          ) : (
            <p style={{ fontSize: '0.9rem', color: 'var(--medical-slate-muted)' }}>No pairwise interactions detected.</p>
          )}
      </div>

      {/* ADR Section */}
      <ADRCard adrs={data.adr || []} />

    </div>
  );
};

export default Results;
