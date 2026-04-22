import json
import random
import csv

drugs = [
    "paracetamol", "ibuprofen", "amoxicillin", "metformin", "aspirin", 
    "albuterol", "warfarin", "lisinopril", "clopidogrel", "furosemide", 
    "amlodipine", "azithromycin", "metoprolol", "gabapentin", "sertraline",
    "atorvastatin", "omeprazole", "losartan", "levothyroxine", "diclofenac"
]

brand_names = {
    "Dolo 650": "paracetamol",
    "Advil": "ibuprofen",
    "Amoxil": "amoxicillin",
    "Glucophage": "metformin",
    "Bayer": "aspirin",
    "Ventolin": "albuterol",
    "Coumadin": "warfarin",
    "Zestril": "lisinopril",
    "Voltaren": "diclofenac"
}

symptoms = [
    "fever", "headache", "cough", "back pain", "nausea", "dizziness", 
    "stomach pain", "rash", "shortness of breath", "fatigue", "chest pain", 
    "sore throat", "muscle ache", "joint pain", "blurred vision"
]

side_effects = [
    "nausea", "dizziness", "insomnia", "fatigue", "rash", "stomach upset",
    "headache", "dry mouth", "weight gain", "blurred vision", "constipation",
    "diarrhea", "muscle pain", "joint swelling", "anxiety"
]

interactions = ["safe", "caution", "risky", "dangerous"]

conditions = [
    "Type 2 Diabetes", "Hypertension", "Asthma", "Flu", "Ear infection", 
    "Chronic pain", "Heart disease", "Allergies", "Bacterial infection", 
    "Insomnia", "Anxiety", "Depression"
]

def generate_structured_note(note_id):
    age = random.randint(18, 85)
    gender = random.choice(["Male", "Female"])
    
    num_conditions = random.randint(1, 3)
    patient_conditions = random.sample(conditions, num_conditions)
    
    num_current_meds = random.randint(1, 3)
    current_meds = random.sample(drugs, num_current_meds)
    
    new_drug = random.choice(drugs)
    while new_drug in current_meds:
        new_drug = random.choice(drugs)
        
    has_allergy = random.choice([True, False, False])
    allergy = "None"
    if has_allergy:
        allergy = random.choice(drugs)
        
    note_text = f"Patient Age: {age} years\nGender: {gender}\n\n"
    note_text += "Existing Conditions:\n"
    for cond in patient_conditions:
        note_text += f"- {cond}\n"
        
    note_text += "\nCurrent Medications:\n"
    for med in current_meds:
        dosage = random.choice(["5 mg", "10 mg", "50 mg", "100 mg", "500 mg"])
        note_text += f"- {med.capitalize()} {dosage}\n"
        
    note_text += f"\nNew Drug Prescribed:\n- {new_drug.capitalize()} {random.choice(['25 mg', '50 mg', '75 mg'])}\n"
    note_text += f"\nKnown Allergies:\n- {allergy.capitalize() if allergy != 'None' else 'None'}"
    
    return {
        "id": note_id,
        "text": note_text
    }

def generate_csv(filename, header, data_func, count=200):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for _ in range(count):
            writer.writerow(data_func())

if __name__ == "__main__":
    # Generate 200 Structured Clinical Notes
    dataset = [generate_structured_note(i) for i in range(1, 201)]
    with open("app/data/dummy_test_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Generated 200 structured dummy notes in app/data/dummy_test_dataset.json")

    # Generate ADR data (200 rows)
    generate_csv(
        "app/data/adr_dataset_expanded.csv", 
        ["drug_name", "side_effect"],
        lambda: [random.choice(drugs), random.choice(side_effects)],
        200
    )
    print(f"Generated 200 ADR rows in app/data/adr_dataset_expanded.csv")

    # Generate DDI data (200 rows)
    def random_ddi():
        d1 = random.choice(drugs)
        d2 = random.choice(drugs)
        while d2 == d1:
            d2 = random.choice(drugs)
        return [d1, d2, random.choice(interactions)]

    generate_csv(
        "app/data/ddi_dataset_expanded.csv",
        ["drug_1", "drug_2", "interaction"],
        random_ddi,
        200
    )
    print(f"Generated 200 DDI rows in app/data/ddi_dataset_expanded.csv")
