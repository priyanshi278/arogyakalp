from typing import List, Dict, Optional
from app.models.clinical_models import (
    ReasoningRequest, 
    ClinicalAnalysisResponse, 
    SideEffect, 
    RecommendationOutput
)
from app.services.ddi_service import ddi_service
from app.services.adr_service import adr_service
from app.services.recommendation_service import recommendation_service
from app.utils.drug_mapper import normalize_drug_name

class ClinicalReasoningService:
    def analyze(self, request: ReasoningRequest) -> ClinicalAnalysisResponse:
        # Normalize drug names
        normalized_current = [normalize_drug_name(d) for d in request.current_drugs]
        normalized_new = normalize_drug_name(request.new_drug)
        patient_status = request.patient_status
        
        # Clinical Analysis (Strict Scope: Current vs New)
        ddi_analysis = ddi_service.analyze(normalized_current, normalized_new, patient_status)
        
        # Fetch ADRs for NEW drug ONLY (as per expected behavior)
        all_side_effects = []
        for adr in adr_service.get_adrs(normalized_new):
            all_side_effects.append(SideEffect(effect=adr['effect'], severity=adr['severity']))
        
        # Recommendation Logic
        is_high_risk = ddi_analysis['risk_score'] >= 2
        rec_action = "avoid drug" if is_high_risk else "continue"
        
        best_alt = None
        best_why = None
        
        if is_high_risk:
            # Look for alternative for the NEW drug
            alt_res = recommendation_service.suggest_alternative(normalized_new, patient_status)
            if alt_res:
                best_alt = alt_res['name']
                best_why = f"safer alternative ({alt_res['reason']})"
        
        return ClinicalAnalysisResponse(
            risk_level=ddi_analysis['risk_level'],
            risk_score=ddi_analysis['risk_score'],
            reason=ddi_analysis['reasons'],
            side_effects=all_side_effects,
            recommendation=RecommendationOutput(
                action=rec_action,
                alternative=best_alt,
                why=best_why
            )
        )

clinical_reasoning_service = ClinicalReasoningService()
