import React from 'react';

const InputSection = ({ patientInfo, setPatientInfo, onAnalyze, isLoading, onReset }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setPatientInfo(prev => ({ ...prev, [name]: value }));
  };

  const handleSample = () => {
    setPatientInfo({
      name: 'Alex',
      age: '68',
      gender: 'Male',
      conditions: 'Hypertension, Kidney Disease',
      currentMeds: 'Warfarin 5mg',
      newDrug: 'Ibuprofen 400mg',
      allergies: 'None'
    });
  };

  return (
    <div className="glass-panel section-card" style={{ padding: '1.25rem', height: '100%' }}>
      <div className="section-head" style={{ marginBottom: '0.75rem', fontSize: '1rem' }}>
        <span>👤</span>
        <h3>Patient Console</h3>
      </div>

      <div className="assessment-form" style={{ gap: '0.75rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 60px 80px', gap: '0.5rem' }}>
          <div className="form-field">
            <label className="field-label" style={{ fontSize: '0.65rem' }}>Full Name</label>
            <input 
              className="medical-input" 
              name="name" 
              value={patientInfo.name} 
              onChange={handleChange} 
              placeholder="e.g. John Doe"
            />
          </div>
          <div className="form-field">
            <label className="field-label" style={{ fontSize: '0.65rem' }}>Age</label>
            <input 
              className="medical-input" 
              name="age" 
              type="number"
              value={patientInfo.age} 
              onChange={handleChange} 
              placeholder="0"
            />
          </div>
          <div className="form-field">
            <label className="field-label" style={{ fontSize: '0.65rem' }}>Gender</label>
            <select className="medical-input" name="gender" value={patientInfo.gender} onChange={handleChange}>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>
        </div>

        <div className="form-field">
          <label className="field-label" style={{ fontSize: '0.65rem' }}>Clinical Conditions</label>
          <textarea 
            className="medical-input" 
            name="conditions" 
            rows="2"
            value={patientInfo.conditions} 
            onChange={handleChange}
            placeholder="Hypertension, Diabetes..."
          />
        </div>

        <div className="form-field">
          <label className="field-label" style={{ fontSize: '0.65rem' }}>Current Medications</label>
          <textarea 
            className="medical-input" 
            name="currentMeds" 
            rows="2"
            value={patientInfo.currentMeds} 
            onChange={handleChange}
            placeholder="Warfarin, Metformin..."
          />
        </div>

        <div className="form-field">
          <label className="field-label" style={{ fontSize: '0.65rem', color: 'var(--medical-indigo)' }}>New Drug Prescribed</label>
          <textarea 
            className="medical-input" 
            name="newDrug" 
            rows="2"
            value={patientInfo.newDrug} 
            onChange={handleChange}
            style={{ borderLeft: '3px solid var(--medical-indigo)', background: '#F0FDF4' }}
            placeholder="Ibuprofen..."
          />
        </div>

        <div className="form-field">
          <label className="field-label" style={{ fontSize: '0.65rem', color: 'var(--danger)' }}>Allergies</label>
          <input 
            className="medical-input" 
            name="allergies" 
            value={patientInfo.allergies} 
            onChange={handleChange}
            style={{ borderLeft: '3px solid var(--danger)' }}
            placeholder="None"
          />
        </div>

        {patientInfo.age > 60 || patientInfo.conditions.toLowerCase().includes('kidney') ? (
          <div style={{ marginTop: '0.5rem', padding: '0.75rem', background: 'var(--warning-soft)', borderRadius: '4px', border: '1px solid var(--warning)' }}>
            <div className="field-label" style={{ color: '#92400E', marginBottom: '0.25rem' }}>Clinical Context Summary</div>
            <div style={{ fontSize: '0.75rem', color: '#92400E', lineHeight: '1.4' }}>
              <strong>Risk Modifiers Detected:</strong>
              <ul style={{ paddingLeft: '1.25rem', marginTop: '0.25rem' }}>
                {patientInfo.age > 60 && <li>Elderly patient (&gt;60y)</li>}
                {patientInfo.conditions.toLowerCase().includes('kidney') && <li>Renal impairment</li>}
              </ul>
            </div>
          </div>
        ) : null}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '0.5rem', marginTop: '1rem' }}>
          <button className="btn-med btn-primary" onClick={onAnalyze} disabled={isLoading} style={{ width: '100%', padding: '0.8rem' }}>
            {isLoading ? <><span className="spinner"></span> Running Clinical Engine...</> : <span>🔍 Run Clinical Analysis</span>}
          </button>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button className="btn-med" onClick={handleSample} style={{ flex: 1, border: '1px solid #D1D5DB' }}>
              + Case
            </button>
            <button className="btn-med btn-reset" onClick={onReset} style={{ flex: 1 }}>
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InputSection;
