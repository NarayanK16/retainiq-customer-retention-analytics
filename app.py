import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="ReatainIQCustomer Churn Predictor",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
    }
    .risk-high { color: #DC2626; }
    .risk-medium { color: #F59E0B; }
    .risk-low { color: #10B981; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 RetainIQCustomer Retention Predictor</h1>', unsafe_allow_html=True)

# Load model and features with error handling
@st.cache_resource
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        return model, None
    except FileNotFoundError:
        return None, "Model file not found. Please check the file path."

@st.cache_resource
def load_features():
    try:
        with open("features.pkl", "rb") as f:
            feature_names = pickle.load(f)
        return feature_names, None
    except FileNotFoundError:
        return None, "Features file not found. Please check the file path."

# Load model and features
model, model_error = load_model()
feature_names, features_error = load_features()

if model_error or features_error:
    st.error(f"Error loading resources: {model_error or features_error}")
    st.stop()

# Debug: Show feature names to understand structure
with st.expander("Debug: Show Feature Names", expanded=False):
    st.write(f"Number of features: {len(feature_names)}")
    st.write("First 20 features:", feature_names[:20])
    st.write("Features containing 'InternetService':", [f for f in feature_names if 'InternetService' in f])
    st.write("Features containing 'Contract':", [f for f in feature_names if 'Contract' in f])
    st.write("Features containing 'PaperlessBilling':", [f for f in feature_names if 'PaperlessBilling' in f])

# Sidebar for inputs
with st.sidebar:
    st.markdown("### 🎯 Customer Details")
    
    # Customer information
    st.markdown("#### Basic Information")
    tenure = st.slider(
        "Tenure (months)", 
        0, 72, 12,
        help="How long the customer has been with the company"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        monthly_charges = st.number_input(
            "Monthly Charges ($)", 
            0.0, 200.0, 70.0, 0.5,
            help="Monthly service charges"
        )
    with col2:
        total_charges = st.number_input(
            "Total Charges ($)", 
            0.0, 10000.0, 2000.0, 50.0,
            help="Total charges to date"
        )
    
    st.markdown("#### Service Details")
    
    # Dynamically determine available contract types based on feature names
    contract_options = []
    if any("Contract_One year" in f for f in feature_names):
        contract_options.append("One year")
    if any("Contract_Two year" in f for f in feature_names):
        contract_options.append("Two year")
    contract_options.append("Month-to-month")  # Default/base category
    
    contract_type = st.selectbox(
        "Contract Type", 
        contract_options,
        help="Contract duration"
    )
    
    # Dynamically determine available internet service types
    internet_options = []
    if any("InternetService_DSL" in f for f in feature_names):
        internet_options.append("DSL")
    if any("InternetService_Fiber optic" in f for f in feature_names):
        internet_options.append("Fiber optic")
    internet_options.append("No")  # Default/base category
    
    internet_service = st.selectbox(
        "Internet Service", 
        internet_options,
        help="Type of internet service"
    )
    
    # Paperless billing
    paperless_billing = st.radio(
        "Paperless Billing", 
        ["No", "Yes"],
        help="Paperless billing option"
    )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📈 Prediction Results")
    
    if st.button("🔮 Predict Churn Risk", type="primary", use_container_width=True):
        
        # Create input dataframe with all zeros
        input_df = pd.DataFrame(0, index=[0], columns=feature_names)
        
        # Fill numeric features
        input_df["tenure"] = tenure
        input_df["MonthlyCharges"] = monthly_charges
        input_df["TotalCharges"] = total_charges
        
        # Fill categorical features - only set to 1 if feature exists
        # Contract type
        if contract_type == "Two year" and "Contract_Two year" in feature_names:
            input_df["Contract_Two year"] = 1
        elif contract_type == "One year" and "Contract_One year" in feature_names:
            input_df["Contract_One year"] = 1
        # Month-to-month is the base category (all contract features = 0)
        
        # Internet service
        if internet_service == "Fiber optic" and "InternetService_Fiber optic" in feature_names:
            input_df["InternetService_Fiber optic"] = 1
        elif internet_service == "DSL" and "InternetService_DSL" in feature_names:
            input_df["InternetService_DSL"] = 1
        # "No" is the base category (all internet features = 0)
        
        # Paperless billing
        if paperless_billing == "Yes" and "PaperlessBilling" in feature_names:
            input_df["PaperlessBilling"] = 1
        
        # Debug: Show the input dataframe
        with st.expander("Debug: Show Input Data", expanded=False):
            # Show only features that are non-zero or important
            non_zero_features = input_df.columns[input_df.iloc[0] != 0].tolist()
            st.write(f"Non-zero features ({len(non_zero_features)}):", non_zero_features)
            st.write("Input data shape:", input_df.shape)
            st.write("Sample of input data:", input_df.iloc[0, :20])  # First 20 features
        
        # Make prediction
        try:
            probability = model.predict_proba(input_df)[0][1]
            
            # Display results
            with st.container():
                st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                
                # Probability gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probability * 100,
                    title={'text': "Churn Probability"},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 35], 'color': "green"},
                            {'range': [35, 60], 'color': "yellow"},
                            {'range': [60, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': 60
                        }
                    }
                ))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Risk classification
                st.markdown("### 📊 Risk Assessment")
                if probability >= 0.6:
                    st.markdown('<h3 class="risk-high">⚠️ HIGH RISK OF CHURN</h3>', unsafe_allow_html=True)
                    st.info("**Recommendations:** Offer retention discount, escalate to retention team, conduct satisfaction survey")
                elif probability >= 0.35:
                    st.markdown('<h3 class="risk-medium">⚠️ MEDIUM RISK OF CHURN</h3>', unsafe_allow_html=True)
                    st.info("**Recommendations:** Check-in call, offer loyalty rewards, review service quality")
                else:
                    st.markdown('<h3 class="risk-low">✅ LOW RISK OF CHURN</h3>', unsafe_allow_html=True)
                    st.info("**Recommendations:** Maintain current service level, consider upselling opportunities")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Key metrics in columns
                st.markdown("### 📋 Key Metrics")
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Churn Probability", f"{probability:.1%}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with metric_col2:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    retention_prob = 1 - probability
                    st.metric("Retention Probability", f"{retention_prob:.1%}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with metric_col3:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Customer Lifetime", f"{tenure} months")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Feature importance analysis (if model has feature_importances_)
                if hasattr(model, 'feature_importances_'):
                    with st.expander("📊 Top Factors Influencing Prediction"):
                        # Get feature importances
                        importances = model.feature_importances_
                        feature_importance_df = pd.DataFrame({
                            'feature': feature_names,
                            'importance': importances
                        }).sort_values('importance', ascending=False).head(10)
                        
                        # Create bar chart
                        fig2 = go.Figure(go.Bar(
                            x=feature_importance_df['importance'],
                            y=feature_importance_df['feature'],
                            orientation='h',
                            marker_color='steelblue'
                        ))
                        fig2.update_layout(
                            title="Top 10 Most Important Features",
                            xaxis_title="Importance",
                            yaxis_title="Feature",
                            height=400
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                
                # Factors influencing prediction
                st.markdown("### 🔍 Key Influencing Factors")
                factors = []
                if tenure < 6:
                    factors.append("Short tenure (< 6 months)")
                if monthly_charges > 80:
                    factors.append("High monthly charges")
                if internet_service == "Fiber optic":
                    factors.append("Fiber optic internet service (competitive market)")
                if paperless_billing == "Yes":
                    factors.append("Paperless billing")
                if contract_type == "Month-to-month":
                    factors.append("Month-to-month contract (higher churn risk)")
                
                if factors:
                    for i, factor in enumerate(factors, 1):
                        st.write(f"{i}. {factor}")
                else:
                    st.write("No high-risk factors identified")
                
                # Display prediction confidence
                prediction = model.predict(input_df)[0]
                st.markdown(f"**Prediction:** {'Will Churn' if prediction == 1 else 'Will Not Churn'}")
                    
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            st.info("Common issues: Feature name mismatches or missing features.")

with col2:
    st.markdown("### ℹ️ Information Panel")
    
    st.markdown("#### How to Use")
    st.info("""
    1. Fill in customer details in the sidebar
    2. Click 'Predict Churn Risk' button
    3. View the prediction and recommendations
    """)
    
    st.markdown("#### Interpretation Guide")
    with st.expander("Risk Levels Explained"):
        st.markdown("""
        - **Low Risk (<35%)**: Customer is likely to stay
        - **Medium Risk (35-60%)**: Customer may consider leaving
        - **High Risk (>60%)**: Immediate action required
        """)
    
    with st.expander("Key Factors Affecting Churn"):
        st.markdown("""
        • **Short Tenure**: New customers churn more often
        • **High Monthly Charges**: Price-sensitive customers
        • **Fiber Optic Service**: Competitive market segment
        • **Paperless Billing**: May indicate digital-only preferences
        • **Contract Type**: Month-to-month contracts have higher churn
        • **Internet Service**: Different services have different churn rates
        """)
    
    # Model information
    with st.expander("Model Information"):
        st.markdown(f"""
        - **Model Type**: {type(model).__name__}
        - **Number of Features**: {len(feature_names)}
        - **Features Loaded**: Yes
        """)
    
    # Download report
    if 'probability' in locals():
        st.download_button(
            label="📥 Download Report",
            data=f"""
            Customer Churn Prediction Report
            
            Probability of Churn: {probability:.1%}
            Risk Level: {'High' if probability >= 0.6 else 'Medium' if probability >= 0.35 else 'Low'}
            Prediction: {'Will Churn' if prediction == 1 else 'Will Not Churn'}
            
            Customer Details:
            - Tenure: {tenure} months
            - Monthly Charges: ${monthly_charges:.2f}
            - Total Charges: ${total_charges:.2f}
            - Contract Type: {contract_type}
            - Internet Service: {internet_service}
            - Paperless Billing: {paperless_billing}
            
            Key Factors:
            {chr(10).join([f'- {factor}' for factor in factors]) if factors else '- No high-risk factors identified'}
            
            Recommendations:
            {'Offer retention discount and escalate to retention team' if probability >= 0.6 else 'Conduct satisfaction survey and offer loyalty rewards' if probability >= 0.35 else 'Maintain current service and consider upselling opportunities'}
            """,
            file_name=f"churn_prediction_{tenure}_{monthly_charges}.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Customer Churn Prediction Dashboard • Powered by ML Model"
    "</div>",
    unsafe_allow_html=True
)
