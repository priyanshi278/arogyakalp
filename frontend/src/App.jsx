import React, { useState } from 'react';
import Header from './components/Header';
import InputSection from './components/InputSection';
import Results from './components/Results';

function App() {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState(null);
  const [chatResponse, setChatResponse] = useState('');
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!input.trim()) return;

    setIsLoading(true);
    setError(null);
    setData(null);
    setChatResponse('');

    try {
      // Parallel API calls
      const [nerRes, chatRes] = await Promise.all([
        fetch('/api/extract_entities', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: input })
        }),
        fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: input })
        })
      ]);

      if (!nerRes.ok || !chatRes.ok) {
        throw new Error('Failed to fetch analysis from server.');
      }

      const nerData = await nerRes.json();
      const chatData = await chatRes.json();

      setData(nerData);
      setChatResponse(chatData.response);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setInput('');
    setData(null);
    setChatResponse('');
    setError(null);
  };

  const showDangerBanner = data?.drug_interactions?.some(i => 
    i.interaction.toLowerCase().match(/danger|severe|warning|fatal/)
  );

  return (
    <div className="container">
      <Header />
      
      {showDangerBanner && (
        <div 
          className="badge badge-danger animate-fade-up" 
          style={{ width: '100%', padding: '1rem', marginBottom: '1rem', fontSize: '1rem', textAlign: 'center' }}
        >
          🚨 HIGH RISK INTERACTION DETECTED - VIEW SAFETY WARNINGS BELOW
        </div>
      )}

      {error && (
        <div className="badge badge-danger" style={{ width: '100%', padding: '1rem', marginBottom: '1.5rem', textAlign: 'center' }}>
          {error}
        </div>
      )}

      <InputSection 
        input={input} 
        setInput={setInput} 
        onAnalyze={handleAnalyze} 
        isLoading={isLoading} 
        onReset={handleReset}
      />

      <Results data={data} chatResponse={chatResponse} isLoading={isLoading} />

      <footer style={{ marginTop: 'auto', textAlign: 'center', padding: '2rem', color: 'var(--color-text-muted)', fontSize: '0.8rem' }}>
        &copy; 2026 ArogyaKalp AI • For Educational Use Only • Always Consult a Professional
      </footer>
    </div>
  );
}

export default App;
