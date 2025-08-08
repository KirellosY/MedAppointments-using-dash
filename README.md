# 📊 No-Show Appointments Dashboard

This dashboard provides a professional and interactive visualization of the **Medical Appointment No-Show Dataset**, helping users explore and understand patient behaviors, neighborhood trends, and time-based appointment patterns.

---

## 🚀 Features

- **Total Appointments Analyzed**: `110,527`
- 📌 **Neighborhood Analysis**:
  - Number of appointments by neighborhood
  - No-show percentage per neighborhood
  - Total no-shows per neighborhood
- ⏰ **Time Series Analysis**:
  - Appointments by day of the week
  - Appointments by month
  - Appointments over time (Scheduled vs. Appointment Day)
- 📄 **Summary Tab**:
  - Concise notes on rare features (e.g., alcoholism, diabetes, handicap)
  - Clean insight presentation instead of cluttered charts
- ✅ Fully interactive Dash interface using Plotly and Bootstrap

---

## 📈 Key Insights

- **Missed Appointments**: A significant portion of patients failed to show up despite scheduling.
- **Neighborhood Trends**:
  - Some neighborhoods have consistently higher no-show rates.
  - This may be tied to access issues, socioeconomic status, or other factors.
- **Time Patterns**:
  - Certain days of the week (like Monday and Friday) had higher no-shows.
  - Appointments scheduled too far in advance tend to have higher no-show probabilities.
- **Rare Attributes Summary**:
  - 📚 10% of patients had scholarships.
  - 🍷 Only 2.5% reported alcoholism.
  - 💉 20.9% had hypertension, 7.4% had diabetes.
  - ♿ Just 1.82% were marked as handicapped.
  - These attributes are infrequent but may still influence predictions.

---

## 🛠️ How to Run

1. **Install dependencies**:
   ```bash
   pip install dash pandas plotly dash-bootstrap-components
   ```

2. **Run the dashboard**:
   ```bash
   python DashCode.py
   ```

3. **View in browser**:
   - Open your browser and go to `http://127.0.0.1:8050/`

---

## 📚 Dataset Source

- [Kaggle No-Show Appointments Dataset](https://www.kaggle.com/joniarroba/noshowappointments)

---

## 🧠 Future Improvements

- Add patient demographics analysis (e.g., age groups)
- Integrate machine learning model for predicting no-shows
- Export filtered views as reports
