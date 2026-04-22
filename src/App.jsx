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

  if (!user) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className="container">
      <Header user={user} onLogout={handleLogout} />
      
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
        patientInfo={patientInfo} 
        setPatientInfo={setPatientInfo} 
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
