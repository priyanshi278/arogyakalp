import React from 'react';
import ChatbotCard from './cards/ChatbotCard';
import EntityCard from './cards/EntityCard';
import NormalizedDrugCard from './cards/NormalizedDrugCard';
import ADRCard from './cards/ADRCard';
import DDICard from './cards/DDICard';
import RecommendationCard from './cards/RecommendationCard';

const Results = ({ data, chatResponse, isLoading }) => {
  if (isLoading) return null;
  if (!data) return (
    <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--color-text-muted)' }}>
      <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🔬</div>
      <p>Results will appear here after analysis.</p>
    </div>
  );

  return (
    <div className="animate-fade-up">
      <div className="section-title">
        <span>📊</span>
        <span>Analysis Results</span>
      </div>

      <ChatbotCard response={chatResponse} />

      <div style={{ height: '1.5rem' }}></div>

      <div className="grid grid-2">
        <EntityCard 
          drugs={data.drugs} 
          diseases={data.diseases} 
          allergies={data.allergies} 
        />
        <NormalizedDrugCard drugs={data.drugs} />
        <ADRCard adrs={data.adr_predictions} />
        <DDICard interactions={data.drug_interactions} />
        <RecommendationCard recommendations={data.recommendations} />
      </div>
    </div>
  );
};

export default Results;
