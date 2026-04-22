import React from 'react';

const InputSection = ({ patientInfo, setPatientInfo, onAnalyze, isLoading, onReset }) => {
  const handleInputChange = (field, value) => {
    setPatientInfo(prev => ({ ...prev, [field]: value }));
  };

  const handleSampleClick = () => {
    setPatientInfo({
      name: 'Alex',
      age: '23',
      gender: 'Male',
      conditions: 'Type 2 Diabetes, Hypertension',
      currentMeds: 'Metformin 500 mg, Amlodipine 5 mg, Aspirin 75 mg',
      newDrug: 'Diclofenac 50 mg',
      allergies: 'None'
    });
  };

  const isFormValid = patientInfo.currentMeds.trim() || patientInfo.newDrug.trim();

  return (
    <section className="card animate-fade-up" style={{ marginBottom: '2.5rem' }}>
      <div className="card-header">
        <span className="icon">📝</span>
        <h2 className="h2">Patient Assessment</h2>
      </div>
      
      <div className="form-grid">
        <div className="form-group">
          <label>Patient Name</label>
          <input 
            type="text" 
            className="input" 
            placeholder="e.g. Alex"
            value={patientInfo.name}
            onChange={(e) => handleInputChange('name', e.target.value)}
            disabled={isLoading}
          />
        </div>
        
        <div className="form-group">
          <label>Age</label>
          <input 
            type="number" 
            className="input" 
            placeholder="e.g. 23"
            value={patientInfo.age}
            onChange={(e) => handleInputChange('age', e.target.value)}
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label>Gender</label>
          <select 
            className="select"
            value={patientInfo.gender}
            onChange={(e) => handleInputChange('gender', e.target.value)}
            disabled={isLoading}
          >
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="form-group-full form-group">
          <label>Existing Conditions</label>
          <textarea 
            className="input" 
            style={{ minHeight: '80px', resize: 'vertical' }}
            placeholder="e.g. Type 2 Diabetes, Hypertension"
            value={patientInfo.conditions}
            onChange={(e) => handleInputChange('conditions', e.target.value)}
            disabled={isLoading}
          />
        </div>

        <div className="form-group-full form-group">
          <label>Current Medications</label>
          <textarea 
            className="input" 
            style={{ minHeight: '80px', resize: 'vertical' }}
            placeholder="e.g. Metformin 500 mg, Amlodipine 5 mg"
            value={patientInfo.currentMeds}
            onChange={(e) => handleInputChange('currentMeds', e.target.value)}
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label>New Drug Prescribed</label>
          <input 
            type="text" 
            className="input" 
            placeholder="e.g. Diclofenac 50 mg"
            value={patientInfo.newDrug}
            onChange={(e) => handleInputChange('newDrug', e.target.value)}
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label>Known Allergies</label>
          <input 
            type="text" 
            className="input" 
            placeholder="e.g. Penicillin or None"
            value={patientInfo.allergies}
            onChange={(e) => handleInputChange('allergies', e.target.value)}
            disabled={isLoading}
          />
        </div>
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem', flexWrap: 'wrap' }}>
        <button
          className="btn btn-primary"
          onClick={onAnalyze}
          disabled={isLoading || !isFormValid}
          style={{ minWidth: '140px' }}
        >
          {isLoading ? (
            <>
              <div className="spinner"></div>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <span>🔍</span>
              <span>Analyze</span>
            </>
          )}
        </button>
        <button
          className="btn btn-outline"
          onClick={handleSampleClick}
          disabled={isLoading}
        >
          Sample Case
        </button>
        <button
          className="btn btn-secondary"
          onClick={onReset}
          disabled={isLoading}
        >
          Reset
        </button>
      </div>
    </section>
  );
};

export default InputSection;
