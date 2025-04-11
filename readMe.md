# Patient Health Dashboard

A comprehensive Streamlit application for healthcare professionals to monitor patient health data, view medical reports, track conditions over time, and collaborate on patient care.

## Features

### 1. Patient Profile
- Comprehensive patient information including demographics, medical conditions, medications, and allergies
- Contact information for emergency contacts and primary care physicians
- Insurance details and appointment tracking
- Notes section for healthcare professionals

### 2. Live Monitoring
- Real-time display of vital signs including heart rate, blood pressure, oxygen saturation, and more
- Historical trend visualization with customizable time periods
- Simulated live data stream from patient monitoring devices
- Color-coded alerts for values outside normal ranges

### 3. Medical Reports
- Filterable list of medical reports from various sources (Hospital, Lab, Specialist, Primary Care)
- Report summaries with AI-generated analysis
- Detailed report content in an expandable view
- Options to print, share and annotate reports

### 4. Condition Timeline
- Interactive timeline visualization of patient conditions
- Filter by condition to focus on specific health issues
- Detailed event history for each condition
- Severity tracking and color coding

### 5. Medical Comments
- Communication platform for healthcare professionals
- Add and view comments organized by profession and topic
- Chronological display of patient care notes
- Filter options to find relevant information quickly

## Installation and Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```

## Data Structure

The application uses CSV files stored in a `data/` directory to manage patient information:

- `patients.csv` - Main patient demographic and medical information
- `vitals_{patient_id}.csv` - Historical vital sign measurements
- `reports_{patient_id}.csv` - Medical reports from various sources
- `comments_{patient_id}.csv` - Healthcare professional comments
- `condition_timeline_{patient_id}.csv` - Condition history and events
- `timeline_{patient_id}.json` - Formatted timeline data for visualization

## Customization

You can customize the dashboard by:

1. Modifying the CSS styles in the main application
2. Adding or removing vital sign metrics in the monitoring section
3. Extending the report types and sources
4. Adding new visualization components

## Demo Data

The application includes functionality to generate realistic demo data for testing and demonstration purposes. This includes:

- Patient demographics and medical histories
- Vital sign measurements with realistic variations
- Medical reports with appropriate medical terminology
- Healthcare professional comments in a clinical style
- Condition timelines with realistic progression patterns

## Future Enhancements

- User authentication and role-based access control
- Integration with EHR systems
- Real-time data integration with medical devices
- Advanced analytics and predictive alerts
- Mobile-responsive design for on-the-go access