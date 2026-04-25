import pandas as pd
import os
from typing import List, Dict, Tuple, Optional
from itertools import combinations
from app.utils.drug_mapper import get_drug_class

RISK_LEVELS = {3: "DANGEROUS", 2: "HIGH", 1: "MODERATE", 0: "LOW"}

class DDIService:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.interactions = {}
        self._load_dataset()

    def _load_dataset(self):
        if not os.path.exists(self.dataset_path):
            return
        try:
            df = pd.read_csv(self.dataset_path)
            for _, row in df.iterrows():
                d1 = str(row['drug_1']).strip().lower()
                d2 = str(row['drug_2']).strip().lower()
                interaction = str(row['interaction']).strip().lower()
                pair = tuple(sorted([d1, d2]))
                self.interactions[pair] = interaction
        except:
            pass

    def get_score(self, label: str) -> int:
        label = str(label).lower()
        if "dangerous" in label: return 3
        if "risky" in label: return 2
        if "caution" in label: return 1
        if "moderate" in label: return 1
        return 0

    def get_dynamic_mechanism(self, c1: str, c2: str) -> str:
        classes = sorted([c1, c2])
        if "nsaid" in classes:
            if "antiplatelet" in classes or "anticoagulant" in classes:
                return "additive anticoagulant effect + gastrointestinal mucosal damage → high risk of major gastrointestinal and systemic bleeding"
            if "ace_inhibitor" in classes or "arb" in classes:
                return "constriction of afferent arteriole combined with dilated efferent arteriole → reduced glomerular filtration → acute kidney injury risk"
            if "nsaid" in classes and len([c for c in classes if c == 'nsaid']) == 2:
                return "redundant cyclooxygenase inhibition → exponential risk of peptic ulceration and renal toxicity"
            if "sulfonylurea" in classes:
                return "displacement from plasma proteins → high risk of hypoglycemia"
        if "statin" in classes and "macrolide" in classes:
            return "CYP metabolism inhibition → statin accumulation → risk of rhabdomyolysis"
        if "anticoagulant" in classes or "antiplatelet" in classes:
            return "pharmacodynamic interaction → additive anticoagulant effect → increased risk of major bleeding"
        if "ace_inhibitor" in classes or "arb" in classes or "diuretic" in classes:
            return "pharmacodynamic interaction → renal clearance reduction → increased toxicity risk"
        return "pharmacokinetic or pharmacodynamic interaction → altered drug metabolism"

    def check_class_interaction(self, drug1: str, drug2: str) -> Optional[Dict]:
        c1 = get_drug_class(drug1)
        c2 = get_drug_class(drug2)
        if not c1 or not c2: return None
        
        classes = sorted([c1, c2])
        mechanism = self.get_dynamic_mechanism(c1, c2)
        
        if "nsaid" in classes and ("antiplatelet" in classes or "anticoagulant" in classes):
            return {"interaction": "dangerous", "mechanism": mechanism}
            
        if "nsaid" in classes and ("ace_inhibitor" in classes or "arb" in classes):
            return {"interaction": "risky", "mechanism": mechanism}

        if c1 == "nsaid" and c2 == "nsaid":
            return {"interaction": "dangerous", "mechanism": mechanism}

        if "statin" in classes and "macrolide" in classes:
            return {"interaction": "dangerous", "mechanism": mechanism}

        return None

    def adjust_for_patient(self, drug: str, status: List[str]) -> Tuple[int, List[str]]:
        score_adj = 0
        reasons = []
        d_class = get_drug_class(drug)
        status_lower = [s.lower() for s in status]
        status_str = " ".join(status_lower)
        
        if d_class == "nsaid":
            if any(k in status_str for k in ["kidney disease", "kidney"]):
                score_adj = max(score_adj, 2)
                reasons.append("NSAID + Renal Impairment → impaired renal prostaglandin synthesis → acute kidney injury")
            if "diabetes" in status_str:
                score_adj = max(score_adj, 1)
                reasons.append("Diabetes → underlying nephropathy → accelerated renal decline with NSAIDs")
            if "hypertension" in status_str:
                score_adj = max(score_adj, 1)
                reasons.append("Hypertension → NSAID-induced sodium retention → reduced antihypertensive efficacy")
                
        return score_adj, reasons

    def analyze(self, current_drugs: List[str], new_drug: str, patient_status: List[str], age: Optional[int] = None) -> Dict:
        max_score = 0
        reasons = []
        new_drug_lower = new_drug.lower()
        processed_current = [d.lower() for d in current_drugs if d]
        
        for cur_drug in processed_current:
            itxs = self.check_interactions([cur_drug], [new_drug_lower], patient_status)
            for itx in itxs:
                if itx['interaction'] != "safe":
                    score = self.get_score(itx['interaction'])
                    max_score = max(max_score, score)

        adj, res_list = self.adjust_for_patient(new_drug_lower, patient_status)
        max_score = max(max_score, adj)
        reasons.extend(res_list)
        
        if age and age > 60:
            if max_score > 0 and max_score < 3:
                max_score += 1
                reasons.append("Age >60 → altered drug clearance → escalated clinical risk")
            elif max_score == 0:
                reasons.append("Age >60 → reduced renal/hepatic baseline → standard monitoring recommended")

        final_score = min(max_score, 3)
        final_reasons = list(set(reasons))

        return {
            "risk_score": final_score,
            "risk_level": RISK_LEVELS[final_score],
            "reasons": final_reasons
        }

    def check_interactions(self, drugs: List[str], new_drugs: Optional[List[str]] = None, patient_status: List[str] = []) -> List[Dict]:
        results = []
        if not drugs: return []
        processed_new = [d.lower() for d in new_drugs if d] if new_drugs else []
        processed_current = [d.lower() for d in drugs if d]
        status_str = " ".join([self._normalize_disease(s) for s in patient_status])
        has_renal = "kidney disease" in status_str

        targets = processed_new if new_drugs else processed_current
        
        for d2 in targets:
            others = [d for d in processed_current if d != d2] if not new_drugs else processed_current
            for d1 in others:
                if d1 == d2: continue
                
                base_itx = self.interactions.get(tuple(sorted([d1, d2])), "safe")
                if base_itx == "no known interaction": base_itx = "safe"
                
                class_itx_res = self.check_class_interaction(d1, d2)
                class_lbl = class_itx_res['interaction'] if class_itx_res else "safe"
                
                indirect_lbl = "safe"
                indirect_mech = ""
                if (d1 == "metformin" or d2 == "metformin") and (get_drug_class(d1) == "nsaid" or get_drug_class(d2) == "nsaid"):
                    indirect_lbl = "dangerous" if has_renal else "risky"
                    indirect_mech = "NSAID-induced decreased renal clearance → Metformin accumulation → lactic acidosis"
                
                severity_map = {"dangerous": 3, "risky": 2, "caution": 1, "moderate": 1, "safe": 0}
                val_base = severity_map.get(base_itx, 0)
                val_class = severity_map.get(class_lbl, 0)
                val_indirect = severity_map.get(indirect_lbl, 0)
                
                max_val = max(val_base, val_class, val_indirect)
                
                final_interaction_label = "safe"
                if max_val == 3: final_interaction_label = "dangerous"
                elif max_val == 2: final_interaction_label = "risky"
                elif max_val == 1: final_interaction_label = "caution"

                if class_itx_res and max_val == severity_map.get(class_lbl):
                    interaction_desc = class_itx_res['mechanism']
                elif max_val == severity_map.get(indirect_lbl) and indirect_lbl != "safe":
                    interaction_desc = indirect_mech
                elif max_val == severity_map.get(base_itx) and base_itx != "safe":
                    interaction_desc = f"{self.get_dynamic_mechanism(get_drug_class(d1), get_drug_class(d2))} → increased clinical risk"
                else:
                    interaction_desc = "No clinically significant interactions detected"
                    final_interaction_label = "safe"

                results.append({"drug_pair": [d1.capitalize(), d2.capitalize()], "interaction": final_interaction_label.lower(), "desc": interaction_desc})
        
        seen = set()
        final_results = []
        for r in results:
            pair = tuple(sorted(r['drug_pair']))
            if pair not in seen:
                if r['interaction'] != "safe":
                    final_results.append(r)
                seen.add(pair)
        
        return final_results

    def _normalize_disease(self, name: str) -> str:
        name = name.lower().strip()
        if name in ["kidney", "renal"]: return "kidney disease"
        if name in ["liver"]: return "liver condition"
        if name in ["blood pressure", "bp"]: return "hypertension"
        return name

# Singleton
dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "ddi_dataset_expanded.csv")
ddi_service = DDIService(dataset_path)
