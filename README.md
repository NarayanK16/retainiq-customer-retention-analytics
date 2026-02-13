# 📊 Customer Churn Prediction System

An **end-to-end machine learning project** that predicts customer churn probability using historical customer data.
The project includes **data cleaning, feature engineering, model training, evaluation, threshold tuning, and deployment via Streamlit**.

---

## 🔍 Problem Statement

Customer churn is a major challenge for subscription-based businesses.
The goal of this project is to **identify customers who are likely to churn**, allowing businesses to take **proactive retention actions**.

---

## 🎯 Project Objectives

* Predict whether a customer is likely to churn
* Optimize the model for **high recall on churn customers**
* Identify **key factors driving churn**
* Deploy the model as an **interactive web application**

---

## 🧠 Solution Overview

* Built a **Random Forest Classifier** for churn prediction
* Performed **feature engineering using one-hot encoding**
* Improved churn detection by **tuning the probability threshold**
* Extracted **feature importance** for business insights
* Deployed the solution using **Streamlit**

---

## 🗂️ Project Structure

```
customer-churn-prediction/
│
├── app.py                  # Streamlit dashboard
├── model.pkl               # Trained ML model
├── features.pkl            # Training feature names
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
│
├── notebooks/
│   └── churn_analysis.ipynb
│
├── data/
│   ├── raw/
│   │   └── Telco_Customer_Churn.csv
│   └── processed/
│       └── cleaned_churn_data.csv
│
├── screenshots/
│   ├── dashboard.png
│   └── feature_importance.png
│
└── .gitignore
```

---

## 📁 Dataset

* **Source**: Telco Customer Churn Dataset
* **Target Variable**: `Churn`
* **Key Features**:

  * Tenure
  * MonthlyCharges
  * TotalCharges
  * Contract Type
  * Internet Service
  * Payment Method
  * Support Services

---

## ⚙️ Tech Stack

* **Programming Language**: Python
* **Libraries**:

  * pandas, numpy
  * scikit-learn
  * matplotlib
  * plotly
  * streamlit
* **Deployment**: Streamlit / Render
* **Version Control**: Git & GitHub

---

## 🔬 Model Building

* Model Used: **Random Forest Classifier**
* Evaluation Metrics:

  * Accuracy
  * Precision
  * Recall (primary focus)
  * F1-score

### Why Recall Matters?

In churn prediction, **missing a churn customer is costly**.
Therefore, recall was prioritized over accuracy.

---

## 📈 Model Performance (After Threshold Tuning)

* **Churn Recall improved from ~48% to ~67%**
* Reduced false negatives significantly
* Maintained acceptable accuracy

---

## 🔑 Key Business Insights

* Customers with **short tenure** are more likely to churn
* **High monthly charges** increase churn probability
* Customers on **month-to-month contracts** churn more
* **Fiber optic users** show higher churn risk
* Long-term contracts reduce churn significantly

---

## 🖥️ Streamlit Dashboard

The web application allows users to:

* Input customer details
* View churn probability
* Classify customers into **Low / Medium / High risk**
* Get actionable business recommendations

live at : https://customer-churn-prediction-94ad.onrender.com
📸 Screenshots are available in the `screenshots/` folder.

---

## ▶️ How to Run the Project Locally

1. Clone the repository

```bash
git clone <repository-url>
cd customer-churn-prediction
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run Streamlit app

```bash
streamlit run app.py
```

---

## 🚀 Deployment

The application can be deployed using:

* Streamlit Cloud
* Render

---

## 📌 Key Learnings

* Importance of **feature consistency between training and deployment**
* Handling **class imbalance** in business problems
* Threshold tuning for business-focused ML
* Building deployable ML applications

---

## 📄 Future Improvements

* SHAP-based model explainability
* XGBoost or LightGBM model
* Customer segmentation
* Automated retraining pipeline

---

## 🙌 Author

**Jayveer Talekar**
Aspiring Data Scientist | Machine Learning Enthusiast

---

## ⭐ If you like this project

Give the repository a ⭐ and feel free to fork or contribute!
