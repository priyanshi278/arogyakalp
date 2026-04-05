import React from 'react';

const InputSection = ({ input, setInput, onAnalyze, isLoading, onReset }) => {
  const sampleCase = "A patient with fever and fatigue is taking Ibuprofen. They are also prescribed Lisinopril and Warfarin. Known allergies: Penicillin.";

  const handleSampleClick = () => {
    setInput(sampleCase);
  };

  return (
    <section className="card animate-fade-up" style={{ marginBottom: '2.5rem' }}>
      <div className="card-header">
        <span className="icon">📝</span>
        <h2 className="h2">Patient Assessment</h2>
      </div>
      <textarea
        className="textarea"
        placeholder="Enter patient symptoms, medications, or clinical notes..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={isLoading}
      />
      <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem', flexWrap: 'wrap' }}>
        <button
          className="btn btn-primary"
          onClick={onAnalyze}
          disabled={isLoading || !input.trim()}
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
