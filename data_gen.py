import os
import pandas as pd
import numpy as np
import random
import json
from datetime import datetime, timedelta

# Create directories for data if they don't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Generate dummy patient data
def generate_patient_data():
    patients = []
    for i in range(1, 21):
        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            first_name = random.choice(['John', 'Michael', 'David', 'Robert', 'James', 'William', 'Thomas', 'Richard'])
        else:
            first_name = random.choice(['Mary', 'Jennifer', 'Linda', 'Patricia', 'Elizabeth', 'Susan', 'Jessica', 'Sarah'])
        
        last_name = random.choice(['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Taylor', 'Clark'])
        
        age = random.randint(25, 85)
        blood_type = random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
        
        conditions = []
        possible_conditions = ['Hypertension', 'Diabetes Type 2', 'Asthma', 'Arthritis', 'Obesity', 
                               'Coronary Artery Disease', 'COPD', 'Depression', 'Anxiety', 'Hypothyroidism']
        num_conditions = random.randint(0, 3)
        for _ in range(num_conditions):
            condition = random.choice(possible_conditions)
            if condition not in conditions:
                conditions.append(condition)
        
        medications = []
        possible_medications = ['Atorvastatin', 'Lisinopril', 'Levothyroxine', 'Metformin', 'Amlodipine', 
                               'Metoprolol', 'Albuterol', 'Omeprazole', 'Losartan', 'Gabapentin']
        num_medications = random.randint(0, 4)
        for _ in range(num_medications):
            medication = random.choice(possible_medications)
            if medication not in medications:
                medications.append(medication)
        
        allergies = []
        possible_allergies = ['Penicillin', 'Sulfa Drugs', 'Peanuts', 'Shellfish', 'Latex', 'Aspirin', 'Ibuprofen', 'Eggs', 'Milk', 'Wheat']
        num_allergies = random.randint(0, 2)
        for _ in range(num_allergies):
            allergy = random.choice(possible_allergies)
            if allergy not in allergies:
                allergies.append(allergy)
                
        # Emergency contact
        emergency_contact = {
            'name': random.choice(['Sarah', 'Robert', 'Emily', 'Michael', 'Jessica', 'David', 'Jennifer', 'James']),
            'relationship': random.choice(['Spouse', 'Child', 'Parent', 'Sibling', 'Friend']),
            'phone': f'({random.randint(100, 999)})-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
        }
        
        # Primary care physician
        physician = {
            'name': f'Dr. {random.choice(["Anderson", "Baker", "Carter", "Davis", "Edwards", "Fisher", "Garcia", "Harris"])}',
            'specialty': 'Primary Care',
            'phone': f'({random.randint(100, 999)})-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
        }
        
        # Insurance
        insurance = {
            'provider': random.choice(['Blue Cross', 'Aetna', 'UnitedHealthcare', 'Cigna', 'Humana', 'Kaiser']),
            'policy_number': f'{random.choice(["ABC", "XYZ", "DEF", "GHI", "JKL"])}-{random.randint(10000, 99999)}',
            'group_number': f'{random.randint(1000, 9999)}'
        }
        
        patient = {
            'id': f'P{i:03d}',
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f'{first_name} {last_name}',
            'age': age,
            'gender': gender,
            'blood_type': blood_type,
            'height': round(random.uniform(150, 190), 1),  # in cm
            'weight': round(random.uniform(50, 110), 1),   # in kg
            'conditions': conditions,
            'medications': medications,
            'allergies': allergies,
            'emergency_contact': emergency_contact,
            'physician': physician,
            'insurance': insurance,
            'last_visit': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
            'next_appointment': (datetime.now() + timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')
        }
        
        patients.append(patient)
    
    # Save to CSV
    pd.DataFrame(patients).to_csv('data/patients.csv', index=False)
    
    # Also save as JSON for easier access
    with open('data/patients.json', 'w') as f:
        json.dump(patients, f)
    
    return patients

# Generate vital signs data for a specific patient
def generate_vital_signs(patient_id, days=30):
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    current_date = start_date
    
    # Base values
    base_heart_rate = random.randint(65, 85)
    base_systolic = random.randint(110, 140)
    base_diastolic = random.randint(70, 90)
    base_temperature = round(random.uniform(36.5, 37.3), 1)
    base_respiratory_rate = random.randint(12, 18)
    base_oxygen = random.randint(94, 99)
    base_glucose = random.randint(80, 120)
    
    # Add some randomness to simulate daily variations and trends
    while current_date <= end_date:
        # Multiple readings per day
        for hour in [8, 12, 16, 20]:
            timestamp = current_date.replace(hour=hour, minute=random.randint(0, 59))
            
            # Add some random variation to the base values
            heart_rate = max(40, min(120, base_heart_rate + random.randint(-10, 10)))
            systolic = max(90, min(180, base_systolic + random.randint(-15, 15)))
            diastolic = max(50, min(110, base_diastolic + random.randint(-10, 10)))
            temperature = round(max(35.5, min(38.0, base_temperature + random.uniform(-0.4, 0.4))), 1)
            respiratory_rate = max(10, min(25, base_respiratory_rate + random.randint(-3, 3)))
            oxygen = max(88, min(100, base_oxygen + random.randint(-3, 3)))
            glucose = max(60, min(200, base_glucose + random.randint(-20, 20)))
            
            # Add some patterns
            if timestamp.weekday() in [5, 6]:  # Weekend
                heart_rate += random.randint(0, 5)  # More activity on weekends
            
            if 12 <= timestamp.hour <= 14:  # After lunch
                glucose += random.randint(10, 30)
            
            data.append({
                'patient_id': patient_id,
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'heart_rate': heart_rate,
                'blood_pressure_systolic': systolic,
                'blood_pressure_diastolic': diastolic,
                'temperature': temperature,
                'respiratory_rate': respiratory_rate,
                'oxygen_saturation': oxygen,
                'glucose': glucose
            })
        
        # Next day
        current_date += timedelta(days=1)
    
    # Save to CSV
    pd.DataFrame(data).to_csv(f'data/vitals_{patient_id}.csv', index=False)
    return data

# Generate medical reports for a patient
def generate_medical_reports(patient_id, patient_data, num_reports=10):
    reports = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Reports from the last year
    
    sources = ['Hospital', 'Lab', 'Specialist', 'Primary Care']
    report_types = ['Annual Physical', 'Blood Test', 'Cardiology Consultation', 'Endocrinology Follow-up', 
                   'Radiology Report', 'Neurology Assessment', 'Dermatology Examination', 'Orthopedic Evaluation',
                   'Gastroenterology Procedure', 'Ophthalmology Check']
    
    conditions = patient_data.get('conditions', [])
    
    # Add more medical terms based on conditions
    medical_terms = {
        'Hypertension': ['blood pressure', 'hypertension', 'cardiovascular risk', 'sodium restriction'],
        'Diabetes Type 2': ['glucose', 'HbA1c', 'insulin resistance', 'diabetic'],
        'Asthma': ['respiratory', 'inhaler', 'wheezing', 'bronchial'],
        'Arthritis': ['joint pain', 'inflammation', 'mobility', 'arthritis'],
        'Obesity': ['BMI', 'weight management', 'dietary guidelines', 'exercise regimen'],
        'Coronary Artery Disease': ['cardiac', 'coronary', 'atherosclerosis', 'ischemia'],
        'COPD': ['pulmonary', 'emphysema', 'oxygen therapy', 'bronchodilator'],
        'Depression': ['mood', 'antidepressant', 'therapy', 'mental health'],
        'Anxiety': ['anxiety', 'stress', 'panic', 'anxiolytic'],
        'Hypothyroidism': ['thyroid', 'TSH', 'levothyroxine', 'metabolism']
    }
    
    # Create dates for reports, sorted from oldest to newest
    report_dates = sorted([start_date + timedelta(days=random.randint(0, 365)) for _ in range(num_reports)])
    
    for i, report_date in enumerate(report_dates):
        source = random.choice(sources)
        report_type = random.choice(report_types)
        
        # Generate summary using patient's conditions
        summary_parts = []
        for condition in conditions:
            if condition in medical_terms and random.random() > 0.3:  # 70% chance to include
                term = random.choice(medical_terms[condition])
                summary_parts.append(f"{term} assessment performed")
        
        # Add random findings
        findings = []
        if random.random() > 0.7:  # 30% chance of abnormal findings
            abnormal = random.choice(['elevated', 'reduced', 'abnormal', 'concerning', 'irregular'])
            measure = random.choice(['levels', 'readings', 'results', 'values', 'patterns'])
            findings.append(f"{abnormal} {measure} detected")
        else:
            findings.append("all results within normal ranges")
        
        # Choose a random specialist name
        specialist_last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson"]
        specialist_first_names = ["John", "Robert", "William", "James", "Mary", "Patricia", "Jennifer", "Linda"]
        specialist_name = f"Dr. {random.choice(specialist_first_names)} {random.choice(specialist_last_names)}"
        
        # Generate a more detailed summary
        if not summary_parts:
            summary_parts.append(f"Routine {report_type.lower()} performed")
        
        summary = f"{', '.join(summary_parts)}. {', '.join(findings)}."
        
        # Generate more detailed report content
        content_parts = [
            f"Patient: {patient_data['first_name']} {patient_data['last_name']} (ID: {patient_id})",
            f"Date: {report_date.strftime('%Y-%m-%d')}",
            f"Provider: {specialist_name}, {source}",
            f"Type: {report_type}",
            "",
            "SUMMARY:",
            summary,
            "",
            "DETAILED FINDINGS:"
        ]
        
        # Add details based on report type
        if "Blood Test" in report_type:
            content_parts.extend([
                f"- Hemoglobin: {random.uniform(12.0, 17.0):.1f} g/dL",
                f"- White Blood Cell Count: {random.uniform(4.0, 11.0):.1f} x10^9/L",
                f"- Platelet Count: {random.randint(150, 450)} x10^9/L",
                f"- Glucose: {random.uniform(70, 130):.1f} mg/dL",
                f"- Cholesterol (Total): {random.uniform(150, 240):.1f} mg/dL",
                f"- HDL Cholesterol: {random.uniform(40, 80):.1f} mg/dL",
                f"- LDL Cholesterol: {random.uniform(70, 160):.1f} mg/dL",
                f"- Triglycerides: {random.uniform(50, 200):.1f} mg/dL"
            ])
        elif "Cardiology" in report_type:
            content_parts.extend([
                f"- Blood Pressure: {random.randint(110, 150)}/{random.randint(70, 95)} mmHg",
                f"- Heart Rate: {random.randint(60, 90)} bpm",
                f"- ECG: {random.choice(['Normal sinus rhythm', 'Minor ST-T wave abnormalities', 'Left ventricular hypertrophy', 'Normal findings'])}",
                f"- Echocardiogram: {random.choice(['Normal cardiac function', 'Mild mitral regurgitation', 'Mild left ventricular hypertrophy', 'Normal ejection fraction'])}"
            ])
        elif "Physical" in report_type:
            content_parts.extend([
                f"- Height: {patient_data['height']} cm",
                f"- Weight: {patient_data['weight']} kg",
                f"- BMI: {patient_data['weight'] / ((patient_data['height']/100) ** 2):.1f}",
                f"- Blood Pressure: {random.randint(110, 150)}/{random.randint(70, 95)} mmHg",
                f"- Heart Rate: {random.randint(60, 90)} bpm",
                f"- Respiratory Rate: {random.randint(12, 20)} breaths/min",
                f"- Temperature: {random.uniform(36.5, 37.3):.1f} °C"
            ])
        else:
            content_parts.extend([
                "- Examination performed as per standard protocol",
                f"- Patient reports {random.choice(['no complaints', 'mild discomfort', 'improvement in symptoms', 'persistent symptoms'])}",
                f"- {random.choice(['No significant changes since last examination', 'Improvement noted in condition', 'Further monitoring recommended', 'Medication adjustment may be necessary'])}"
            ])
            
        # Add recommendations
        content_parts.extend([
            "",
            "RECOMMENDATIONS:",
            f"- {random.choice(['Continue current treatment plan', 'Follow up in 3 months', 'Follow up in 6 months', 'Adjust medication as prescribed', 'No further action needed at this time'])}"
        ])
        
        # Add second recommendation sometimes
        if random.random() > 0.5:
            content_parts.append(f"- {random.choice(['Maintain healthy diet and exercise', 'Monitor symptoms and report any changes', 'Complete prescribed diagnostic tests', 'Consider consultation with specialist'])}")
        
        # Add concluding statement
        content_parts.extend([
            "",
            f"Report prepared by: {specialist_name}",
            f"Date: {report_date.strftime('%Y-%m-%d')}"
        ])
        
        # Join all parts to create full report content
        full_content = "\n".join(content_parts)
        
        # Create NLP summary (simulated)
        nlp_summary = f"AI Analysis: Patient shows {random.choice(['stable', 'improving', 'concerning', 'normal'])} {random.choice(['indicators', 'values', 'parameters', 'results'])}. {random.choice(['No immediate action needed', 'Continued monitoring advised', 'Consider medication adjustment', 'Follow-up recommended'])}"
        
        reports.append({
            'id': f'R{i+1:03d}',
            'patient_id': patient_id,
            'date': report_date.strftime('%Y-%m-%d'),
            'source': source,
            'report_type': report_type,
            'summary': summary,
            'content': full_content,
            'nlp_summary': nlp_summary,
            'specialist': specialist_name
        })
    
    # Sort by date, newest first
    reports.sort(key=lambda x: x['date'], reverse=True)
    
    # Save to CSV
    pd.DataFrame(reports).to_csv(f'data/reports_{patient_id}.csv', index=False)
    return reports

# Generate medical professionals' comments
def generate_comments(patient_id, num_comments=15):
    comments = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # Comments from the last 6 months
    
    professions = ['Doctor', 'Nurse', 'Specialist', 'Pharmacist', 'Physical Therapist']
    
    # Create dates for comments, sorted from oldest to newest
    comment_dates = sorted([start_date + timedelta(days=random.randint(0, 180)) for _ in range(num_comments)])
    
    for i, comment_date in enumerate(comment_dates):
        profession = random.choice(professions)
        
        # Generate a name based on profession
        if profession == 'Doctor':
            name = f"Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'])}"
        else:
            first_names = ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Daniel', 'Jennifer']
            last_names = ['Anderson', 'Martinez', 'Taylor', 'Thomas', 'Lee', 'Patel', 'White', 'Harris']
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Comment topics
        topics = [
            'medication adjustment', 'symptom management', 'treatment plan', 'test results',
            'follow-up appointment', 'recovery progress', 'patient concerns', 'therapy response',
            'lifestyle modifications', 'care coordination'
        ]
        
        # Generate comment based on topic
        topic = random.choice(topics)
        
        if topic == 'medication adjustment':
            comment_text = random.choice([
                "Patient's medication dosage adjusted due to side effects.",
                "Prescribed new medication to better manage symptoms.",
                "Consider reducing dosage if improvement continues.",
                "Added supplemental medication to address secondary symptoms."
            ])
        elif topic == 'symptom management':
            comment_text = random.choice([
                "Patient reports improvement in primary symptoms since last visit.",
                "New symptom reported, monitoring closely.",
                "Symptoms stable, continuing current management approach.",
                "Symptom intensity has decreased following intervention."
            ])
        elif topic == 'treatment plan':
            comment_text = random.choice([
                "Updated treatment plan to include additional therapy sessions.",
                "Treatment plan remains effective, no changes needed at this time.",
                "Considering alternative treatment options if no improvement by next visit.",
                "Modified treatment approach based on latest research findings."
            ])
        elif topic == 'test results':
            comment_text = random.choice([
                "Recent lab results show improvement in key indicators.",
                "Test results require follow-up imaging to confirm diagnosis.",
                "All values within normal ranges, continue monitoring periodically.",
                "Slight elevation in certain markers, will retest in one month."
            ])
        else:
            comment_text = random.choice([
                "Patient doing well overall, maintain current approach.",
                "Discussed concerns about long-term prognosis with patient.",
                "Coordinating care with specialists for comprehensive management.",
                "Recommended lifestyle modifications to support treatment goals."
            ])
        
        # Add a recommendation sometimes
        if random.random() > 0.6:
            recommendations = [
                "Recommend follow-up in 3 months.",
                "Consider additional diagnostic testing if symptoms persist.",
                "Suggested consultation with specialist.",
                "Advised to monitor and report any new symptoms immediately.",
                "Encouraged continued adherence to treatment regimen."
            ]
            comment_text += f" {random.choice(recommendations)}"
        
        comments.append({
            'id': f'C{i+1:03d}',
            'patient_id': patient_id,
            'date': comment_date.strftime('%Y-%m-%d %H:%M:%S'),
            'name': name,
            'profession': profession,
            'comment': comment_text,
            'topic': topic
        })
    
    # Sort by date, newest first
    comments.sort(key=lambda x: x['date'], reverse=True)
    
    # Save to CSV
    pd.DataFrame(comments).to_csv(f'data/comments_{patient_id}.csv', index=False)
    return comments

# Generate conditions timeline data for a patient
def generate_conditions_timeline(patient_id, patient_data):
    conditions = patient_data.get('conditions', [])
    if not conditions:
        # Add some random conditions if none exist
        possible_conditions = ['Hypertension', 'Diabetes Type 2', 'Asthma', 'Arthritis', 'Obesity', 
                              'Coronary Artery Disease', 'COPD', 'Depression', 'Anxiety', 'Hypothyroidism']
        num_conditions = random.randint(1, 3)
        for _ in range(num_conditions):
            condition = random.choice(possible_conditions)
            if condition not in conditions:
                conditions.append(condition)
    
    timeline_data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=random.randint(365*3, 365*10))  # 3-10 years history
    
    for condition in conditions:
        # Generate diagnosis date
        diagnosis_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days // 2))
        
        # Generate events related to this condition
        condition_events = [{
            'date': diagnosis_date.strftime('%Y-%m-%d'),
            'event_type': 'Diagnosis',
            'description': f'Initial diagnosis of {condition}',
            'condition': condition,
            'severity': random.choice(['Mild', 'Moderate', 'Severe']),
            'healthcare_provider': f"Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'])}"
        }]
        
        # Add follow-up events
        num_events = random.randint(2, 8)
        last_date = diagnosis_date
        
        for _ in range(num_events):
            # Each event happens after the previous one
            event_date = last_date + timedelta(days=random.randint(30, 180))
            if event_date > end_date:
                break
                
            event_type = random.choice(['Follow-up', 'Medication Change', 'Treatment', 'Flare-up', 'Improvement', 'Hospitalization', 'Specialist Consultation'])
            
            # Description based on event type
            if event_type == 'Follow-up':
                description = f'Routine follow-up for {condition}'
                severity = condition_events[-1]['severity']  # Same as last event
            elif event_type == 'Medication Change':
                description = f'Adjusted medication regimen for {condition}'
                # Severity might improve
                if condition_events[-1]['severity'] == 'Severe' and random.random() > 0.7:
                    severity = 'Moderate'
                elif condition_events[-1]['severity'] == 'Moderate' and random.random() > 0.7:
                    severity = 'Mild'
                else:
                    severity = condition_events[-1]['severity']
            elif event_type == 'Treatment':
                description = f'New treatment initiated for {condition}'
                # Severity might improve
                if condition_events[-1]['severity'] == 'Severe' and random.random() > 0.6:
                    severity = 'Moderate'
                elif condition_events[-1]['severity'] == 'Moderate' and random.random() > 0.6:
                    severity = 'Mild'
                else:
                    severity = condition_events[-1]['severity']
            elif event_type == 'Flare-up':
                description = f'Experienced worsening of {condition} symptoms'
                # Severity gets worse
                if condition_events[-1]['severity'] == 'Mild':
                    severity = 'Moderate'
                elif condition_events[-1]['severity'] == 'Moderate':
                    severity = 'Severe'
                else:
                    severity = 'Severe'
            elif event_type == 'Improvement':
                description = f'Noted improvement in {condition}'
                # Severity improves
                if condition_events[-1]['severity'] == 'Severe':
                    severity = 'Moderate'
                elif condition_events[-1]['severity'] == 'Moderate':
                    severity = 'Mild'
                else:
                    severity = 'Mild'
            elif event_type == 'Hospitalization':
                description = f'Hospitalized due to complications from {condition}'
                severity = 'Severe'  # Always severe if hospitalized
            else:  # Specialist Consultation
                description = f'Consultation with specialist regarding {condition}'
                severity = condition_events[-1]['severity']  # Same as last event
            
            condition_events.append({
                'date': event_date.strftime('%Y-%m-%d'),
                'event_type': event_type,
                'description': description,
                'condition': condition,
                'severity': severity,
                'healthcare_provider': f"Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'])}"
            })
            
            last_date = event_date
        
        timeline_data.extend(condition_events)
    
    # Sort by date
    timeline_data.sort(key=lambda x: x['date'])
    
    # Save to CSV
    pd.DataFrame(timeline_data).to_csv(f'data/condition_timeline_{patient_id}.csv', index=False)
    
    # Create a timeline JSON for visualization (for the timeline component)
    timeline_items = []
    
    for event in timeline_data:
        # Determine color based on condition
        condition_colors = {
            'Hypertension': '#ff6b6b',           # Red
            'Diabetes Type 2': '#48dbfb',        # Blue
            'Asthma': '#1dd1a1',                 # Green
            'Arthritis': '#feca57',              # Yellow
            'Obesity': '#5f27cd',                # Purple
            'Coronary Artery Disease': '#ee5253', # Dark Red
            'COPD': '#a29bfe',                  # Lavender
            'Depression': '#54a0ff',            # Light Blue
            'Anxiety': '#ff9ff3',               # Pink
            'Hypothyroidism': '#00d2d3'         # Teal
        }
        
        condition = event['condition']
        color = condition_colors.get(condition, '#dfe6e9')  # Default color if condition not in dictionary
        
        # Determine background based on severity
        severity_backgrounds = {
            'Mild': 'rgba(46, 213, 115, 0.2)',      # Light green
            'Moderate': 'rgba(255, 165, 2, 0.2)',   # Light orange
            'Severe': 'rgba(255, 71, 87, 0.2)'      # Light red
        }
        background = severity_backgrounds.get(event['severity'], 'rgba(200, 200, 200, 0.2)')
        
        # Create timeline item
        item = {
            'id': str(len(timeline_items) + 1),
            'content': f"{event['event_type']}: {event['condition']}",
            'start': event['date'],
            'group': event['condition'],
            'className': f"severity-{event['severity'].lower()}",
            'title': f"{event['description']}<br>Severity: {event['severity']}<br>Provider: {event['healthcare_provider']}",
            'style': f"background-color: {background}; color: {color}; border-color: {color};"
        }
        
        timeline_items.append(item)
    
    # Create groups for each condition
    groups = []
    for i, condition in enumerate(set(event['condition'] for event in timeline_data)):
        groups.append({
            'id': condition,
            'content': condition,
            'style': f"color: {condition_colors.get(condition, '#dfe6e9')};"
        })
    
    # Create the final timeline data structure
    timeline_json = {
        'items': timeline_items,
        'groups': groups
    }
    
    # Save to JSON
    with open(f'data/timeline_{patient_id}.json', 'w') as f:
        json.dump(timeline_json, f)
    
    return timeline_data

# Main function to generate all data
def generate_all_data():
    print("Generating patient data...")
    patients = generate_patient_data()
    
    # Generate data for first 5 patients
    for i in range(min(5, len(patients))):
        patient = patients[i]
        patient_id = patient['id']
        print(f"Generating data for patient {patient_id} - {patient['full_name']}...")
        
        print("  - Generating vital signs...")
        generate_vital_signs(patient_id)
        
        print("  - Generating medical reports...")
        generate_medical_reports(patient_id, patient)
        
        print("  - Generating medical comments...")
        generate_comments(patient_id)
        
        print("  - Generating condition timeline...")
        generate_conditions_timeline(patient_id, patient)
    
    print("Data generation complete!")

if __name__ == "__main__":
    generate_all_data()