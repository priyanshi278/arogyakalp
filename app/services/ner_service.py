from app.utils.preprocessing import preprocess_text
from app.models.ner_model import CDSSResponse, RecommendationDict, AnalysisDict, CDSSDDI, CDSSADR, ner_pipeline
from app.utils.drug_mapper import normalize_drug_name
from app.services.adr_service import adr_service
from app.services.ddi_service import ddi_service
from app.services.recommendation_service import recommendation_service
from typing import List, Set, Optional, Dict
import re

class NERService:
    def __init__(self):
        pass
    
    def normalize_disease(self, name: str) -> str:
        name = name.lower().strip()
        if name in ["kidney", "renal", "kidney disease"]: return "Kidney Disease"
        if name in ["liver", "liver disease"]: return "Liver Condition"
        if name in ["blood pressure", "bp", "hypertension"]: return "Hypertension"
        return name.title()

    def get_dynamic_monitoring(self, risk_level: str, diseases: List[str], drugs: List[str]) -> str:
        advices = []
        for d in diseases:
            if "kidney" in d.lower(): advices.append("renal function")
            if "liver" in d.lower(): advices.append("hepatic panels")
            if "diabetes" in d.lower(): advices.append("glycemic indices")
            
        drug_classes = [get_drug_class(dr) for dr in drugs if get_drug_class(dr)]
        if "anticoagulant" in drug_classes or "antiplatelet" in drug_classes:
            advices.append("INR levels")
            advices.append("signs of bleeding")

        if risk_level == "DANGEROUS" or risk_level == "HIGH":
            prefix = "If unavoidable, monitor "
        else:
            prefix = "Routine monitoring: "

        if not advices:
            return f"{prefix}patient for standard adverse reactions."
        
        if len(advices) > 1:
            advices_str = ", ".join(advices[:-1]) + ", and " + advices[-1]
        else:
            advices_str = advices[0]
            
        return prefix + advices_str

    def extract_entities(self, text: str) -> CDSSResponse:
        if not text or not text.strip():
            return self._empty_response()

        sections = {"conditions": "", "current_meds": "", "new_med": "", "allergies": ""}
        age = None
        age_match = re.search(r"Patient Age:\s*(\d+)", text)
        if age_match: age = int(age_match.group(1))
        
        for key, pattern in [("conditions", r"Existing Conditions:\s*(.*?)(?:\n\n|\n[A-Z]|$)"),
                             ("current_meds", r"Current Medications:\s*(.*?)(?:\n\n|\n[A-Z]|$)"),
                             ("new_med", r"New Drug Prescribed:\s*-?\s*(.*?)(?:\n\n|\n[A-Z]|$)"),
                             ("allergies", r"Known Allergies:\s*(.*?)(?:\n\n|\n[A-Z]|$)")]:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match: sections[key] = match.group(1).lower()

        clean_text = preprocess_text(text)
        results = ner_pipeline(clean_text)
        drugs, diseases, allergies, raw_adr_predictions = [], [], [], []
        current_generics, new_generics, added_drugs, added_diseases = [], [], set(), set()

        for cond in re.split(r'[,\n-]', sections["conditions"]):
            c = self.normalize_disease(cond.strip().strip("- "))
            if c and len(c) > 2 and c.lower() not in ["none", "ff", "aller"]:
                diseases.append(c); added_diseases.add(c.lower())

        processed_results = []
        for entity in results:
            label, word = entity.get("entity_group", ""), entity.get("word", "").strip()
            if word.startswith("##") and processed_results: processed_results[-1]["word"] += word[2:]; continue
            processed_results.append({"label": label, "word": word})

        for entity in processed_results:
            label, word = entity["label"], entity["word"].replace("#", "").strip(" -_")
            if len(word) < 2 or word.lower() in ["ff", "aller"]: continue
            low_word = word.lower()
            if label in ["Medication", "DRUG", "CHEMICAL"]:
                if low_word in added_drugs or low_word in ["patient", "name", "age"]: continue
                generic_name = normalize_drug_name(word)
                if sections["new_med"] and (low_word in sections["new_med"] or sections["new_med"] in low_word):
                    new_generics.append(generic_name)
                    sd = adr_service.get_adrs(generic_name, diseases)
                    if sd: raw_adr_predictions.append({"drug": word.capitalize(), "effects": [s['effect'] for s in sd]})
                else: current_generics.append(generic_name)
                added_drugs.add(low_word)
            elif label in ["Disease_disorder", "Sign_symptom", "DISEASE", "DISORDER", "ALLERGEN"]:
                if any(k in low_word for k in ["kidney", "renal", "liver", "blood pressure", "diabetes", "hypertension"]):
                    norm_d = self.normalize_disease(word)
                    if norm_d.lower() not in added_diseases: diseases.append(norm_d); added_diseases.add(norm_d.lower())
                else:
                    if label == "ALLERGEN" or "allergy" in sections["allergies"]: allergies.append(word.title())
                    else:
                        norm_d = self.normalize_disease(word)
                        if norm_d.lower() not in added_diseases: diseases.append(norm_d); added_diseases.add(norm_d.lower())

        if not new_generics:
            return self._empty_response()

        itx_results = ddi_service.check_interactions(current_generics, new_generics, diseases)
        full_analysis = ddi_service.analyze(current_generics, new_generics[0], diseases, age)
        risk_lvl = full_analysis["risk_level"]

        highest_ddi = "safe"
        if itx_results:
            ddi_severities = [r['interaction'].lower() for r in itx_results]
            if "dangerous" in ddi_severities: highest_ddi = "dangerous"
            elif "risky" in ddi_severities: highest_ddi = "risky"
            elif "caution" in ddi_severities or "moderate" in ddi_severities: highest_ddi = "caution"

        if highest_ddi == "dangerous": risk_lvl = "DANGEROUS"
        elif highest_ddi == "risky" and risk_lvl not in ["DANGEROUS"]: risk_lvl = "HIGH"
        elif highest_ddi == "caution" and risk_lvl not in ["DANGEROUS", "HIGH"]: risk_lvl = "MODERATE"

        final_ddis = []
        primary_interaction = ""
        primary_impact = ""
        for res in itx_results:
            severity = res['interaction'].upper()
            if severity == "NO CLINICALLY SIGNIFICANT INTERACTIONS DETECTED": continue
            
            meaning = res['desc']
            if "→" not in meaning: meaning = f"Pharmacodynamic/pharmacokinetic interaction → {meaning}"
            
            drug_pair = res["drug_pair"]
            if len(drug_pair) == 2:
                 final_ddis.append(CDSSDDI(drug_a=drug_pair[0], drug_b=drug_pair[1], severity=severity, meaning=meaning))
                 if not primary_interaction and severity in ["DANGEROUS", "HIGH", "CAUTION", "MODERATE"]:
                     primary_interaction = f"{drug_pair[0]} + {drug_pair[1]} → {meaning}"
                     primary_impact = meaning.split('→')[-1].strip()

        final_adrs = []
        full_term_mapping = {"kidney issue": "Acute Kidney Injury", "bleeding": "Major Gastrointestinal Bleeding", "heart attack": "Myocardial Infarction"}
        for adr in raw_adr_predictions:
            mapped_effects = []
            for s in adr['effects']:
                cleaned = s.lower().strip()
                # Do not exaggerate
                if "hepatotoxicity" in cleaned and "paracetamol" in new_generics:
                    cleaned = "elevated transaminases with supratherapeutic dosing"
                mapped_effects.append(full_term_mapping.get(cleaned, s.title()))
            final_adrs.append(CDSSADR(drug=adr['drug'], effects=mapped_effects))

        alerts = []
        if primary_interaction:
            alerts.append(primary_interaction)
        
        has_nsaid = any(get_drug_class(d) == "nsaid" for d in new_generics + current_generics)
        if has_nsaid and "Kidney Disease" in diseases:
             alerts.append("Kidney Disease + NSAID → impaired renal perfusion → elevated risk of acute kidney injury")
        elif has_nsaid and "Hypertension" in diseases:
             alerts.append("Hypertension + NSAID → sodium retention → reduced antihypertensive efficacy")
             
        if age and age > 60:
             alerts.append(f"Age >60 yrs → reduced drug clearance → increased sensitivity to adverse effects")

        new_title = sections["new_med"].title() if sections["new_med"] else new_generics[0].title()
        
        # Safe -> No alternative. Danger -> Must Alternative
        alt = recommendation_service.suggest_alternative(new_generics[0], diseases)
        alternative_name = alt['name'].title() if alt else "Clinical consultation required"
        
        if risk_lvl == "DANGEROUS" or risk_lvl == "HIGH":
            decision = "❌ Avoid Drug"
            out_summary = "avoid combination"
            reason = "High-risk combination; avoid use."
        elif risk_lvl == "MODERATE" or risk_lvl == "CAUTION":
            decision = "⚠️ Use with Caution"
            out_summary = "use with monitoring"
            reason = "Moderate risk pairwise interaction; proceed with awareness."
        else:
            decision = "✅ Safe to Use"
            out_summary = "safe to use"
            reason = "No clinically significant interactions detected."
            alternative_name = "N/A" # Enforce SAFE->No alternative

        monitoring = self.get_dynamic_monitoring(risk_lvl, diseases, current_generics + new_generics)

        rec_dict = RecommendationDict(
            decision=decision,
            drug=new_title,
            alternative=alternative_name,
            reason=reason,
            monitoring=monitoring
        )

        mech = "Independent metabolic pathways without significant overlap"
        imp = "No clinically significant impact anticipated"
        
        if primary_interaction:
            mech_segments = primary_interaction.split("→")
            if len(mech_segments) > 2: 
                 mech = f"{mech_segments[0].strip()} → {mech_segments[1].strip()}"
                 imp = f"{mech_segments[2].strip()}"
            else:
                 mech = primary_interaction
                 imp = primary_impact if primary_impact else "Clinical risk elevated"

        if "bleeding" in imp.lower() and "major" not in imp.lower():
             imp = "High risk of major gastrointestinal and systemic bleeding"

        rf = ", ".join(diseases) if diseases else "None identified"
        if age and age > 60: rf += f" (Age {age})"

        analysis_dict = AnalysisDict(
            mechanism=mech.capitalize(),
            impact=imp.capitalize(),
            risk_factors=rf,
            outcome=out_summary.capitalize()
        )

        return CDSSResponse(
             risk_level=risk_lvl,
             alerts=alerts,
             recommendation=rec_dict,
             analysis=analysis_dict,
             ddi=final_ddis,
             adr=final_adrs
        )

    def _empty_response(self) -> CDSSResponse:
        return CDSSResponse(
            risk_level="LOW",
            alerts=[],
            recommendation=RecommendationDict(decision="N/A", drug="N/A", alternative="N/A", reason="N/A", monitoring="N/A"),
            analysis=AnalysisDict(mechanism="N/A", impact="N/A", risk_factors="N/A", outcome="N/A"),
            ddi=[],
            adr=[]
        )

def get_drug_class(drug_name: str) -> Optional[str]:
    from app.utils.drug_mapper import get_drug_class as gdc
    return gdc(drug_name)
