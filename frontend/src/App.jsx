import React, { useState } from 'react';
import Header from './components/Header';
import InputSection from './components/InputSection';
import Results from './components/Results';
import LoginPage from './components/LoginPage';

function App() {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('arogyakalp_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [patientInfo, setPatientInfo] = useState({
    name: '',
    age: '',
    gender: 'Male',
    conditions: '',
    currentMeds: '',
    newDrug: '',
    allergies: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState(null);
  const [chatResponse, setChatResponse] = useState('');
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    const { name, age, gender, conditions, currentMeds, newDrug, allergies } = patientInfo;
    
    // Format input for the backend
    const formattedInput = `Patient Name: ${name || 'N/A'}\nPatient Age: ${age || 'N/A'} years\nGender: ${gender}\n\nExisting Conditions:\n${conditions || 'None'}\n\nCurrent Medications:\n${currentMeds || 'None'}\n\nNew Drug Prescribed:\n- ${newDrug || 'None'}\n\nKnown Allergies:\n- ${allergies || 'None'}`;

    if (!formattedInput.trim()) return;

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
          body: JSON.stringify({ text: formattedInput })
        }),
        fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: formattedInput })
        })
      ]);

      if (!nerRes.ok) {
        const errData = await nerRes.text();
        throw new Error(`NER Error (${nerRes.status}): ${errData || 'Unknown error'}`);
      }
      
      if (!chatRes.ok) {
        const errData = await chatRes.text();
        throw new Error(`Chatbot Error (${chatRes.status}): ${errData || 'Unknown error'}`);
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
    setPatientInfo({
      name: '',
      age: '',
      gender: 'Male',
      conditions: '',
      currentMeds: '',
      newDrug: '',
      allergies: ''
    });
    setData(null);
    setChatResponse('');
    setError(null);
  };

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('arogyakalp_user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('arogyakalp_user');
  };

  const showDangerBanner = data?.drug_interactions?.some(i => 
    i.interaction.toLowerCase().match(/danger|severe|warning|fatal/)
  );
  
  const showResults = data || isLoading || error;

  if (!user) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className="container fade-in">
      <Header user={user} onLogout={handleLogout} />
      
      <div className={showResults ? "main-grid" : "center-grid"}>
          <div className={showResults ? "left-panel" : "center-panel"}>
            <InputSection 
                patientInfo={patientInfo} 
                setPatientInfo={setPatientInfo} 
                onAnalyze={handleAnalyze} 
                isLoading={isLoading} 
                onReset={handleReset}
            />
          </div>
          
          {showResults && (
            <div className="right-panel fade-in">
              {showDangerBanner && (
                <div className="risk-alert-banner">
                  ⚠️ HIGH RISK INTERACTION DETECTED
                </div>
              )}

              {error && (
                <div className="risk-alert-banner" style={{ background: 'var(--warning)', animation: 'none' }}>
                  {error}
                </div>
              )}

              <Results data={data} chatResponse={chatResponse} isLoading={isLoading} />
            </div>
          )}
      </div>

      <footer style={{ marginTop: 'auto', textAlign: 'center', padding: '0.5rem', color: '#94a3b8', fontSize: '0.7rem', letterSpacing: '1px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        &copy; 2026 AROGYAKALP AI CLINICAL SYSTEMS
      </footer>
    </div>
  );
}

export default App;
