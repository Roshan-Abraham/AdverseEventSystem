import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
import os
import time
import ast  # for safely evaluating strings as literals

# Set page configuration
st.set_page_config(
    page_title="Patient Health Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .kpi-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
    }
    .kpi-title {
        font-size: 1rem;
        text-align: center;
        color: #6c757d;
    }
    .normal-value {
        color: #28a745;
    }
    .warning-value {
        color: #ffc107;
    }
    .danger-value {
        color: #dc3545;
    }
    .source-tag {
        font-size: 0.7rem;
        padding: 2px 6px;
        border-radius: 10px;
        font-weight: bold;
        display: inline-block;
        margin-right: 5px;
    }
    .source-hospital {
        background-color: #e6f7ff;
        color: #1890ff;
    }
    .source-lab {
        background-color: #f6ffed;
        color: #52c41a;
    }
    .source-specialist {
        background-color: #fff2e8;
        color: #fa8c16;
    }
    .source-primarycare {
        background-color: #f9f0ff;
        color: #722ed1;
    }
    .timeline-item {
        margin-bottom: 10px;
        padding: 10px;
        border-left: 3px solid #1890ff;
        background-color: #f0f8ff;
    }
    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .comment-box {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .profile-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---

# Helper function to parse string representations of dictionaries
def parse_dict_string(s):
    if isinstance(s, str):
        try:
            # Try to parse the string as a Python literal
            return ast.literal_eval(s)
        except (SyntaxError, ValueError):
            # If parsing fails, return the original string
            return s
    return s

# Helper function to parse string representations of lists
def parse_list_string(s):
    if isinstance(s, str):
        try:
            # Try to parse the string as a Python literal
            result = ast.literal_eval(s)
            if isinstance(result, list):
                return result
            return [s]  # Return a list with the string if it's not a list
        except (SyntaxError, ValueError):
            # If parsing fails, return a list with the original string
            return [s]
    return s if isinstance(s, list) else [s]

# Function to process patient data from CSV
def process_patient_data(patient_dict):
    # Fields that need special handling
    dict_fields = ['emergency_contact', 'physician', 'insurance']
    list_fields = ['conditions', 'medications', 'allergies']
    
    for field in dict_fields:
        if field in patient_dict:
            patient_dict[field] = parse_dict_string(patient_dict[field])
    
    for field in list_fields:
        if field in patient_dict:
            patient_dict[field] = parse_list_string(patient_dict[field])
    
    return patient_dict

# --- Data Generation Functions ---

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

# Function to simulate live data stream
def simulate_live_data(patient_id):
    # Base values (personalized)
    # These would ideally be based on the patient's baseline
    base_heart_rate = random.randint(65, 85)
    base_systolic = random.randint(110, 140)
    base_diastolic = random.randint(70, 90)
    base_temperature = round(random.uniform(36.5, 37.3), 1)
    base_respiratory_rate = random.randint(12, 18)
    base_oxygen = random.randint(94, 99)
    base_glucose = random.randint(80, 120)
    
    # Add some random variation to simulate real-time changes
    heart_rate = max(40, min(120, base_heart_rate + random.randint(-5, 5)))
    systolic = max(90, min(180, base_systolic + random.randint(-8, 8)))
    diastolic = max(50, min(110, base_diastolic + random.randint(-5, 5)))
    temperature = round(max(35.5, min(38.0, base_temperature + random.uniform(-0.2, 0.2))), 1)
    respiratory_rate = max(10, min(25, base_respiratory_rate + random.randint(-2, 2)))
    oxygen = max(88, min(100, base_oxygen + random.randint(-2, 2)))
    glucose = max(60, min(200, base_glucose + random.randint(-10, 10)))
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'patient_id': patient_id,
        'timestamp': now,
        'heart_rate': heart_rate,
        'blood_pressure_systolic': systolic,
        'blood_pressure_diastolic': diastolic,
        'temperature': temperature,
        'respiratory_rate': respiratory_rate,
        'oxygen_saturation': oxygen,
        'glucose': glucose
    }

# Ensure data exists for the application
def ensure_data_exists():
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Check if patient data exists
    if not os.path.exists('data/patients.csv'):
        st.warning("Patient data not found. Please run generate_dummy_data.py first.")
        
        # Create a simple dataset with one patient for demonstration
        patient = {
            'id': 'P001',
            'first_name': 'John',
            'last_name': 'Doe',
            'full_name': 'John Doe',
            'age': 45,
            'gender': 'Male',
            'blood_type': 'O+',
            'height': 178.5,
            'weight': 80.2,
            'conditions': ['Hypertension', 'Diabetes Type 2'],
            'medications': ['Lisinopril', 'Metformin'],
            'allergies': ['Penicillin'],
            'emergency_contact': {
                'name': 'Jane Doe',
                'relationship': 'Spouse',
                'phone': '(555)-123-4567'
            },
            'physician': {
                'name': 'Dr. Smith',
                'specialty': 'Primary Care',
                'phone': '(555)-987-6543'
            },
            'insurance': {
                'provider': 'Blue Cross',
                'policy_number': 'BC-12345',
                'group_number': '5678'
            },
            'last_visit': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'next_appointment': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        }
        
        # Save as single-row DataFrame
        pd.DataFrame([patient]).to_csv('data/patients.csv', index=False)
        
        # Generate supporting data for this patient
        patient_id = patient['id']
        generate_vital_signs(patient_id)
        
        # Return the created patient data
        return pd.DataFrame([patient])
    
    # Load existing patient data
    return pd.read_csv('data/patients.csv')

# --- Display Functions ---

# Function to display patient profile
def display_patient_profile(patient):
    st.markdown('<h2 class="sub-header">Patient Information</h2>', unsafe_allow_html=True)
    
    # Profile header with patient image and basic info
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Display avatar based on gender
        if patient['gender'] == 'Male':
            st.image("https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png", width=150)
        else:
            st.image("https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png", width=150)
    
    with col2:
        st.markdown(f"### {patient['full_name']}")
        st.markdown(f"**Patient ID:** {patient['id']}")
        st.markdown(f"**Age:** {patient['age']} years")
        st.markdown(f"**Gender:** {patient['gender']}")
        st.markdown(f"**Blood Type:** {patient['blood_type']}")
        
        # Calculate BMI
        height_m = patient['height'] / 100
        bmi = patient['weight'] / (height_m ** 2)
        bmi_category = "Normal weight"
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi >= 25:
            bmi_category = "Overweight"
        elif bmi >= 30:
            bmi_category = "Obese"
        
        st.markdown(f"**BMI:** {bmi:.1f} ({bmi_category})")
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Patient details in sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown("### Medical Information")
        
        # Make sure conditions is a list
        conditions = patient.get('conditions', [])
        if not isinstance(conditions, list):
            conditions = [conditions] if conditions else []
        
        # Medical conditions
        st.markdown("#### Medical Conditions")
        if conditions:
            for condition in conditions:
                st.markdown(f"- {condition}")
        else:
            st.markdown("- No known medical conditions")
        
        # Make sure medications is a list
        medications = patient.get('medications', [])
        if not isinstance(medications, list):
            medications = [medications] if medications else []
        
        # Medications
        st.markdown("#### Current Medications")
        if medications:
            for medication in medications:
                st.markdown(f"- {medication}")
        else:
            st.markdown("- No current medications")
        
        # Make sure allergies is a list
        allergies = patient.get('allergies', [])
        if not isinstance(allergies, list):
            allergies = [allergies] if allergies else []
        
        # Allergies
        st.markdown("#### Allergies")
        if allergies:
            for allergy in allergies:
                st.markdown(f"- {allergy}")
        else:
            st.markdown("- No known allergies")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Appointment information
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown("### Appointment Information")
        st.markdown(f"**Last Visit:** {patient['last_visit']}")
        st.markdown(f"**Next Appointment:** {patient['next_appointment']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Contact Information
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown("### Primary Care Physician")
        
        # Handle physician data safely
        physician = patient.get('physician', {})
        if isinstance(physician, dict):
            st.markdown(f"**Name:** {physician.get('name', 'Not specified')}")
            st.markdown(f"**Specialty:** {physician.get('specialty', 'Not specified')}")
            st.markdown(f"**Phone:** {physician.get('phone', 'Not specified')}")
        else:
            st.markdown("**Physician information not available**")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Emergency Contact
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown("### Emergency Contact")
        
        # Handle emergency contact data safely
        emergency_contact = patient.get('emergency_contact', {})
        if isinstance(emergency_contact, dict):
            st.markdown(f"**Name:** {emergency_contact.get('name', 'Not specified')}")
            st.markdown(f"**Relationship:** {emergency_contact.get('relationship', 'Not specified')}")
            st.markdown(f"**Phone:** {emergency_contact.get('phone', 'Not specified')}")
        else:
            st.markdown("**Emergency contact information not available**")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Insurance Information
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown("### Insurance Information")
        
        # Handle insurance data safely
        insurance = patient.get('insurance', {})
        if isinstance(insurance, dict):
            st.markdown(f"**Provider:** {insurance.get('provider', 'Not specified')}")
            st.markdown(f"**Policy Number:** {insurance.get('policy_number', 'Not specified')}")
            st.markdown(f"**Group Number:** {insurance.get('group_number', 'Not specified')}")
        else:
            st.markdown("**Insurance information not available**")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional notes section
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.markdown("### Additional Notes")
    notes = st.text_area("Add notes about the patient", 
                         "Patient is generally compliant with medication regimen. Encourage regular physical activity and healthy diet.")
    if st.button("Save Notes"):
        st.success("Notes saved successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

# Function to display live monitoring
def display_live_monitoring(patient_id):
    st.markdown('<h2 class="sub-header">Live Patient Monitoring</h2>', unsafe_allow_html=True)
    
    # Check if historical data exists
    try:
        historical_data = pd.read_csv(f'data/vitals_{patient_id}.csv')
    except:
        # Generate data if it doesn't exist
        historical_data = pd.DataFrame(generate_vital_signs(patient_id))
    
    # Current vitals display
    st.markdown("### Current Vital Signs")
    
    # Update button
    if st.button("Refresh Data"):
        st.success("Data refreshed!")
    
    # Get the latest vitals
    latest_vitals = simulate_live_data(patient_id)
    
    # Display KPIs in columns
    col1, col2, col3, col4 = st.columns(4)
    
    # Heart Rate
    with col1:
        hr_value = latest_vitals['heart_rate']
        hr_class = "normal-value"
        if hr_value < 60 or hr_value > 100:
            hr_class = "warning-value"
        if hr_value < 50 or hr_value > 120:
            hr_class = "danger-value"
        
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<p class="kpi-title">Heart Rate</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="kpi-value {hr_class}">{hr_value} <span style="font-size:1rem">bpm</span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Blood Pressure
    with col2:
        bp_systolic = latest_vitals['blood_pressure_systolic']
        bp_diastolic = latest_vitals['blood_pressure_diastolic']
        
        bp_class = "normal-value"
        if bp_systolic > 130 or bp_systolic < 90 or bp_diastolic > 80 or bp_diastolic < 60:
            bp_class = "warning-value"
        if bp_systolic > 180 or bp_systolic < 80 or bp_diastolic > 120 or bp_diastolic < 50:
            bp_class = "danger-value"
        
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<p class="kpi-title">Blood Pressure</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="kpi-value {bp_class}">{bp_systolic}/{bp_diastolic} <span style="font-size:1rem">mmHg</span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Oxygen Saturation
    with col3:
        o2_value = latest_vitals['oxygen_saturation']
        o2_class = "normal-value"
        if o2_value < 95:
            o2_class = "warning-value"
        if o2_value < 90:
            o2_class = "danger-value"
        
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<p class="kpi-title">Oxygen Saturation</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="kpi-value {o2_class}">{o2_value}% <span style="font-size:1rem">SpO2</span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Temperature
    with col4:
        temp_value = latest_vitals['temperature']
        temp_class = "normal-value"
        if temp_value > 37.5 or temp_value < 36.0:
            temp_class = "warning-value"
        if temp_value > 38.0 or temp_value < 35.5:
            temp_class = "danger-value"
        
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<p class="kpi-title">Temperature</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="kpi-value {temp_class}">{temp_value}°C <span style="font-size:1rem"></span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row of KPIs
    col1, col2, col3 = st.columns(3)
    
    # Respiratory Rate
    with col1:
        rr_value = latest_vitals['respiratory_rate']
        rr_class = "normal-value"
        if rr_value < 12 or rr_value > 20:
            rr_class = "warning-value"
        if rr_value < 10 or rr_value > 30:
            rr_class = "danger-value"
        
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<p class="kpi-title">Respiratory Rate</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="kpi-value {rr_class}">{rr_value} <span style="font-size:1rem">breaths/min</span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Glucose
    with col2:
        glucose_value = latest_vitals['glucose']
        glucose_class = "normal-value"
        if glucose_value < 70 or glucose_value > 140:
            glucose_class = "warning-value"
        if glucose_value < 55 or glucose_value > 200:
            glucose_class = "danger-value"
        
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<p class="kpi-title">Blood Glucose</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="kpi-value {glucose_class}">{glucose_value} <span style="font-size:1rem">mg/dL</span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Last Updated
    with col3:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<p class="kpi-title">Last Updated</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="kpi-value" style="font-size:1.2rem">{latest_vitals["timestamp"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Historical trends section
    st.markdown("### Vital Signs History")
    
    # Time period selection
    time_periods = {
        "Last 24 Hours": 1,
        "Last 3 Days": 3,
        "Last Week": 7,
        "Last Month": 30
    }
    
    selected_period = st.selectbox("Select Time Period", list(time_periods.keys()))
    days = time_periods[selected_period]
    
    # Convert timestamp to datetime
    historical_data['datetime'] = pd.to_datetime(historical_data['timestamp'])
    
    # Filter data based on selected time period
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered_data = historical_data[historical_data['datetime'] >= cutoff_date]
    
    # Add the latest data point
    latest_data = pd.DataFrame([latest_vitals])
    latest_data['datetime'] = pd.to_datetime(latest_data['timestamp'])
    
    all_data = pd.concat([filtered_data, latest_data]).reset_index(drop=True)
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Heart Rate")
        
        # Heart rate chart
        fig_hr = px.line(all_data, x='datetime', y='heart_rate', 
                        title='Heart Rate Over Time',
                        labels={'heart_rate': 'Heart Rate (bpm)', 'datetime': 'Time'})
        
        # Add reference lines for normal range
        fig_hr.add_shape(type="line", line=dict(dash="dash", color="green"),
                        x0=all_data['datetime'].min(), y0=60, x1=all_data['datetime'].max(), y1=60)
        fig_hr.add_shape(type="line", line=dict(dash="dash", color="green"),
                        x0=all_data['datetime'].min(), y0=100, x1=all_data['datetime'].max(), y1=100)
        
        st.plotly_chart(fig_hr, use_container_width=True)
        
        st.subheader("Blood Pressure")
        
        # Blood pressure chart
        bp_data = all_data.copy()
        fig_bp = go.Figure()
        
        # Add systolic line
        fig_bp.add_trace(go.Scatter(x=bp_data['datetime'], y=bp_data['blood_pressure_systolic'],
                                  mode='lines', name='Systolic', line=dict(color='red')))
        
        # Add diastolic line
        fig_bp.add_trace(go.Scatter(x=bp_data['datetime'], y=bp_data['blood_pressure_diastolic'],
                                  mode='lines', name='Diastolic', line=dict(color='blue')))
        
        # Add reference lines
        fig_bp.add_shape(type="line", line=dict(dash="dash", color="red", width=1),
                       x0=bp_data['datetime'].min(), y0=120, x1=bp_data['datetime'].max(), y1=120)
        fig_bp.add_shape(type="line", line=dict(dash="dash", color="blue", width=1),
                       x0=bp_data['datetime'].min(), y0=80, x1=bp_data['datetime'].max(), y1=80)
        
        fig_bp.update_layout(title='Blood Pressure Over Time',
                           xaxis_title='Time',
                           yaxis_title='Blood Pressure (mmHg)')
        
        st.plotly_chart(fig_bp, use_container_width=True)
    
    with chart_col2:
        st.subheader("Oxygen Saturation")
        
        # Oxygen saturation chart
        fig_o2 = px.line(all_data, x='datetime', y='oxygen_saturation', 
                        title='Oxygen Saturation Over Time',
                        labels={'oxygen_saturation': 'SpO2 (%)', 'datetime': 'Time'})
        
        # Add reference line for normal range
        fig_o2.add_shape(type="line", line=dict(dash="dash", color="green"),
                        x0=all_data['datetime'].min(), y0=95, x1=all_data['datetime'].max(), y1=95)
        
        fig_o2.update_yaxes(range=[85, 100])
        
        st.plotly_chart(fig_o2, use_container_width=True)
        
        st.subheader("Blood Glucose")
        
        # Glucose chart
        fig_glucose = px.line(all_data, x='datetime', y='glucose', 
                             title='Blood Glucose Over Time',
                             labels={'glucose': 'Glucose (mg/dL)', 'datetime': 'Time'})
        
        # Add reference lines for normal range
        fig_glucose.add_shape(type="line", line=dict(dash="dash", color="green"),
                             x0=all_data['datetime'].min(), y0=70, x1=all_data['datetime'].max(), y1=70)
        fig_glucose.add_shape(type="line", line=dict(dash="dash", color="green"),
                             x0=all_data['datetime'].min(), y0=140, x1=all_data['datetime'].max(), y1=140)
        
        st.plotly_chart(fig_glucose, use_container_width=True)
    
    # Live data simulation
    st.markdown("### Live Data Stream")
    st.markdown("This section simulates real-time data streaming from patient monitoring devices.")
    
    # Placeholder for live data
    live_chart_placeholder = st.empty()
    
    # Live data demo
    if st.button("Start Live Data Demo", key="live_demo"):
        # Show live data for 30 seconds (or until the user navigates away)
        start_time = time.time()
        live_data = []
        
        while time.time() - start_time < 30:  # Run for 30 seconds
            # Generate new data point
            new_data = simulate_live_data(patient_id)
            live_data.append(new_data)
            
            # Keep only the last 20 points for display
            if len(live_data) > 20:
                live_data = live_data[-20:]
            
            # Create DataFrame
            live_df = pd.DataFrame(live_data)
            live_df['datetime'] = pd.to_datetime(live_df['timestamp'])
            
            # Create chart
            fig = px.line(live_df, x='datetime', y=['heart_rate', 'blood_pressure_systolic', 
                                                  'blood_pressure_diastolic', 'oxygen_saturation'],
                        labels={
                            'heart_rate': 'Heart Rate (bpm)',
                            'blood_pressure_systolic': 'Systolic BP (mmHg)',
                            'blood_pressure_diastolic': 'Diastolic BP (mmHg)',
                            'oxygen_saturation': 'SpO2 (%)',
                            'datetime': 'Time'
                        },
                        title='Live Patient Monitoring Data')
            
            # Update the chart
            live_chart_placeholder.plotly_chart(fig, use_container_width=True)
            
            # Wait for a short time
            time.sleep(1.5)

# Function to display medical reports
def display_medical_reports(patient_id):
    st.markdown('<h2 class="sub-header">Medical Reports</h2>', unsafe_allow_html=True)
    
    # Check if reports exist
    reports_file = f'data/reports_{patient_id}.csv'
    if os.path.exists(reports_file):
        reports_df = pd.read_csv(reports_file)
    else:
        st.info("No medical reports found for this patient. Please run generate_dummy_data.py to create sample reports.")
        return
    
    # Filter options
    st.markdown("### Filter Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get unique sources
        sources = sorted(reports_df['source'].unique())
        selected_sources = st.multiselect("Filter by Source", sources, default=sources)
    
    with col2:
        # Get unique report types
        report_types = sorted(reports_df['report_type'].unique())
        selected_types = st.multiselect("Filter by Report Type", report_types, default=report_types)
    
    with col3:
        # Date range
        min_date = pd.to_datetime(reports_df['date']).min().date()
        max_date = pd.to_datetime(reports_df['date']).max().date()
        
        date_range = st.date_input("Date Range", 
                                 value=(min_date, max_date),
                                 min_value=min_date,
                                 max_value=max_date)
        
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = min_date, max_date
    
    # Filter reports
    filtered_reports = reports_df[
        (reports_df['source'].isin(selected_sources)) &
        (reports_df['report_type'].isin(selected_types)) &
        (pd.to_datetime(reports_df['date']).dt.date >= start_date) &
        (pd.to_datetime(reports_df['date']).dt.date <= end_date)
    ]
    
    st.markdown(f"### Reports ({len(filtered_reports)} results)")
    
    if filtered_reports.empty:
        st.info("No reports match the selected filters.")
    else:
        # Sort by date (newest first)
        filtered_reports = filtered_reports.sort_values('date', ascending=False)
        
        # Reports container
        for i, report in filtered_reports.iterrows():
            # Create an expander for each report
            with st.expander(f"{report['date']} - {report['report_type']} ({report['source']})"):
                # Source tag
                source_class = f"source-{report['source'].lower().replace(' ', '')}"
                st.markdown(f'<span class="source-tag {source_class}">{report["source"]}</span>', unsafe_allow_html=True)
                
                # Report header
                st.markdown(f"### {report['report_type']}")
                st.markdown(f"**Date:** {report['date']}")
                st.markdown(f"**Specialist:** {report['specialist']}")
                
                # Summary and AI analysis
                st.markdown("#### Summary")
                st.write(report['summary'])
                
                st.markdown("#### AI Analysis")
                st.write(report['nlp_summary'])
                
                # Full report content
                st.markdown("#### Detailed Report")
                st.text_area("", value=report['content'], height=300, key=f"report_{i}")
                
                # Report actions (placeholder)
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.button("Print", key=f"print_{i}"):
                        st.info("Printing functionality would be implemented here.")
                
                with col2:
                    if st.button("Share", key=f"share_{i}"):
                        st.info("Sharing functionality would be implemented here.")
                
                with col3:
                    st.text_input("Add a note about this report", key=f"note_{i}")

# Function to display condition timeline
def display_condition_timeline(patient_id):
    st.markdown('<h2 class="sub-header">Condition Timeline</h2>', unsafe_allow_html=True)
    
    # Check if timeline data exists
    timeline_file = f'data/condition_timeline_{patient_id}.csv'
    if os.path.exists(timeline_file):
        timeline_data = pd.read_csv(timeline_file)
    else:
        st.info("No condition timeline data found for this patient. Please run generate_dummy_data.py to create sample timeline data.")
        return
    
    # Get unique conditions
    conditions = sorted(timeline_data['condition'].unique())
    
    # Condition filter
    selected_conditions = st.multiselect("Filter by Condition", conditions, default=conditions)
    
    # Filter timeline data
    filtered_timeline = timeline_data[timeline_data['condition'].isin(selected_conditions)]
    
    if filtered_timeline.empty:
        st.info("No condition timeline data available for the selected filters.")
    else:
        # Display timeline visualization
        st.markdown("### Condition Timeline Visualization")
        
        # Load the timeline data from JSON
        try:
            # Try to import the streamlit_timeline module for visualization
            try:
                from streamlit_timeline import timeline as st_timeline
                
                timeline_json_file = f'data/timeline_{patient_id}.json'
                if os.path.exists(timeline_json_file):
                    with open(timeline_json_file, 'r') as f:
                        timeline_json_data = json.load(f)
                    
                    # Filter the items based on selected conditions
                    filtered_items = [item for item in timeline_json_data['items'] 
                                     if item['group'] in selected_conditions]
                    
                    # Filter the groups based on selected conditions
                    filtered_groups = [group for group in timeline_json_data['groups'] 
                                      if group['id'] in selected_conditions]
                    
                    # Create filtered timeline data
                    filtered_timeline_json = {
                        'items': filtered_items,
                        'groups': filtered_groups
                    }
                    
                    # Display timeline
                    st_timeline(filtered_timeline_json, height="400px")
                else:
                    raise FileNotFoundError(f"Timeline JSON file not found: {timeline_json_file}")
                    
            except ImportError:
                # If the module is not installed, show a warning and display a table instead
                st.warning("streamlit-timeline module not found. Install it with 'pip install streamlit-timeline' for interactive timeline visualization.")
                
                # Create a simple table view
                st.markdown("### Condition Events (Table View)")
                st.dataframe(filtered_timeline[['date', 'condition', 'event_type', 'severity', 'description']])
                
        except Exception as e:
            st.error(f"Error loading timeline visualization: {e}")
            
            # Fallback to table view
            st.markdown("### Condition Events (Table View)")
            
            # Sort by date
            filtered_timeline = filtered_timeline.sort_values('date')
            
            # Display as table
            st.dataframe(filtered_timeline[['date', 'condition', 'event_type', 'severity', 'description']])
        
        # Display events in detail
        st.markdown("### Condition Events")
        
        # Group by condition
        for condition in selected_conditions:
            condition_events = filtered_timeline[filtered_timeline['condition'] == condition]
            
            if not condition_events.empty:
                with st.expander(f"{condition} - {len(condition_events)} events"):
                    # Sort by date, oldest first
                    condition_events = condition_events.sort_values('date')
                    
                    for _, event in condition_events.iterrows():
                        # Determine severity class for color
                        severity_class = "normal-value"
                        if event['severity'] == 'Moderate':
                            severity_class = "warning-value"
                        elif event['severity'] == 'Severe':
                            severity_class = "danger-value"
                        
                        # Display event in styled div
                        st.markdown(f"""
                        <div class="timeline-item">
                            <strong>{event['date']}</strong> - <strong>{event['event_type']}</strong>
                            <br>
                            <span class="{severity_class}">Severity: {event['severity']}</span>
                            <br>
                            {event['description']}
                            <br>
                            <small>Provider: {event['healthcare_provider']}</small>
                        </div>
                        """, unsafe_allow_html=True)

# Function to display medical comments
def display_medical_comments(patient_id):
    st.markdown('<h2 class="sub-header">Medical Professional Comments</h2>', unsafe_allow_html=True)
    
    # Check if comments exist
    comments_file = f'data/comments_{patient_id}.csv'
    if os.path.exists(comments_file):
        comments_df = pd.read_csv(comments_file)
    else:
        comments_df = pd.DataFrame(columns=['id', 'patient_id', 'date', 'name', 'profession', 'comment', 'topic'])
    
    # Add a new comment
    st.markdown("### Add New Comment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name", "Dr. Smith")
        profession = st.selectbox("Profession", ['Doctor', 'Nurse', 'Specialist', 'Pharmacist', 'Physical Therapist'])
    
    with col2:
        topic = st.selectbox("Topic", [
            'Medication adjustment', 'Symptom management', 'Treatment plan', 'Test results',
            'Follow-up appointment', 'Recovery progress', 'Patient concerns', 'Therapy response',
            'Lifestyle modifications', 'Care coordination'
        ])
    
    comment_text = st.text_area("Comment", placeholder="Enter your comment here...")
    
    if st.button("Submit Comment"):
        if comment_text:
            # Create new comment entry
            new_comment = {
                'id': f'C{len(comments_df) + 1:03d}',
                'patient_id': patient_id,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'name': name,
                'profession': profession,
                'comment': comment_text,
                'topic': topic
            }
            
            # Append to existing comments
            updated_comments = pd.concat([comments_df, pd.DataFrame([new_comment])], ignore_index=True)
            
            # Save to CSV
            updated_comments.to_csv(comments_file, index=False)
            
            # Refresh the displayed comments
            comments_df = updated_comments
            
            st.success("Comment submitted successfully!")
        else:
            st.error("Please enter a comment before submitting.")
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Display existing comments
    st.markdown("### Previous Comments")
    
    if comments_df.empty:
        st.info("No comments found for this patient. Add a comment above to get started.")
    else:
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            professions = sorted(comments_df['profession'].unique())
            selected_professions = st.multiselect("Filter by Profession", professions, default=professions)
        
        with col2:
            topics = sorted(comments_df['topic'].unique())
            selected_topics = st.multiselect("Filter by Topic", topics, default=topics)
        
        # Filter comments
        filtered_comments = comments_df[
            (comments_df['profession'].isin(selected_professions)) &
            (comments_df['topic'].isin(selected_topics))
        ]
        
        if filtered_comments.empty:
            st.info("No comments match the selected filters.")
        else:
            # Sort by date (newest first)
            filtered_comments = filtered_comments.sort_values('date', ascending=False)
            
            for _, comment in filtered_comments.iterrows():
                # Create comment card
                st.markdown(f"""
                <div class="comment-box">
                    <strong>{comment['name']}</strong> ({comment['profession']}) - <em>{comment['date']}</em>
                    <br>
                    <strong>Topic:</strong> {comment['topic']}
                    <br><br>
                    {comment['comment']}
                </div>
                """, unsafe_allow_html=True)

# Main application function
def main():
    # Ensure data exists
    patients_df = ensure_data_exists()
    
    st.markdown('<h1 class="main-header">🏥 Patient Health Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar for patient selection
    st.sidebar.title("Patient Selection")
    
    # Convert patients DataFrame to a list of dictionaries
    patients_list = patients_df.to_dict('records')
    
    # Process each patient to ensure nested structures are parsed
    processed_patients = []
    for patient in patients_list:
        processed_patients.append(process_patient_data(patient))
    
    # Create a dropdown to select patient
    patient_names = [f"{p['id']} - {p['full_name']}" for p in processed_patients]
    selected_patient_name = st.sidebar.selectbox("Select Patient", patient_names)
    
    # Get the selected patient ID
    selected_patient_id = selected_patient_name.split(' - ')[0]
    
    # Get the selected patient data
    selected_patient = next((p for p in processed_patients if p['id'] == selected_patient_id), None)
    
    # Tabs for different sections
    tabs = st.tabs(["📋 Patient Profile", "📊 Live Monitoring", "📑 Medical Reports", "📈 Condition Timeline", "💬 Medical Comments"])
    
    with tabs[0]:  # Patient Profile Tab
        display_patient_profile(selected_patient)
    
    with tabs[1]:  # Live Monitoring Tab
        display_live_monitoring(selected_patient_id)
    
    with tabs[2]:  # Medical Reports Tab
        display_medical_reports(selected_patient_id)
    
    with tabs[3]:  # Condition Timeline Tab
        display_condition_timeline(selected_patient_id)
    
    with tabs[4]:  # Medical Comments Tab
        display_medical_comments(selected_patient_id)

if __name__ == "__main__":
    main()