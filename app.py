import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="RetainIQ · Churn Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg-primary:#070B14; --bg-secondary:#0D1424; --bg-card:#111827;
    --accent-blue:#3B82F6; --accent-cyan:#06B6D4; --accent-purple:#8B5CF6;
    --accent-green:#10B981; --accent-amber:#F59E0B; --accent-red:#EF4444;
    --text-primary:#F9FAFB; --text-secondary:#9CA3AF; --text-muted:#4B5563;
    --border:rgba(59,130,246,0.15);
}
html,body,.stApp { background-color:var(--bg-primary)!important; font-family:'DM Sans',sans-serif!important; color:var(--text-primary)!important; }
#MainMenu,footer,header,.stDeployButton { visibility:hidden; display:none; }
.stApp::before {
    content:''; position:fixed; top:0; left:0; width:100%; height:100%;
    background-image: linear-gradient(rgba(59,130,246,0.03) 1px,transparent 1px), linear-gradient(90deg,rgba(59,130,246,0.03) 1px,transparent 1px);
    background-size:50px 50px; pointer-events:none; z-index:0;
}
.hero-container { text-align:center; padding:2.5rem 0 1.5rem; }
.hero-badge { display:inline-block; background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.3); color:#06B6D4; font-size:0.72rem; font-weight:500; letter-spacing:0.2em; text-transform:uppercase; padding:0.35rem 1.1rem; border-radius:100px; margin-bottom:1.2rem; }
.hero-title { font-family:'Syne',sans-serif!important; font-size:3.8rem!important; font-weight:800!important; line-height:1.1!important; letter-spacing:-0.03em; background:linear-gradient(135deg,#F9FAFB 0%,#93C5FD 50%,#06B6D4 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin:0 0 0.8rem!important; }
.hero-sub { color:#9CA3AF; font-size:1rem; font-weight:300; max-width:440px; margin:0 auto; line-height:1.6; }
.hero-divider { width:60px; height:2px; background:linear-gradient(90deg,var(--accent-blue),var(--accent-cyan)); margin:1.5rem auto; border-radius:2px; }
[data-testid="stSidebar"] { background:var(--bg-secondary)!important; border-right:1px solid var(--border)!important; }
[data-testid="stSidebar"]>div { background:var(--bg-secondary)!important; padding:1.5rem 1rem!important; }
.s-logo { font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:800; color:#F9FAFB; }
.s-tag { font-size:0.7rem; color:#4B5563; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:1.5rem; }
.sec-lbl { font-family:'Syne',sans-serif; font-size:0.62rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:#06B6D4; margin:1.25rem 0 0.6rem; display:flex; align-items:center; gap:0.4rem; }
.sec-lbl::after { content:''; flex:1; height:1px; background:var(--border); }
[data-testid="stSelectbox"]>div>div { background:var(--bg-card)!important; border:1px solid var(--border)!important; color:#F9FAFB!important; border-radius:8px!important; }
[data-testid="stNumberInput"]>div>div>input { background:var(--bg-card)!important; border:1px solid var(--border)!important; color:#F9FAFB!important; border-radius:8px!important; }
label,.stRadio label,.stSelectbox label { color:#9CA3AF!important; font-size:0.82rem!important; }
.stButton>button { background:linear-gradient(135deg,#3B82F6 0%,#8B5CF6 100%)!important; color:white!important; border:none!important; border-radius:12px!important; font-family:'Syne',sans-serif!important; font-size:1rem!important; font-weight:700!important; letter-spacing:0.05em!important; padding:0.8rem 2rem!important; box-shadow:0 4px 20px rgba(59,130,246,0.4)!important; width:100%!important; transition:all 0.3s ease!important; }
.stButton>button:hover { transform:translateY(-2px)!important; box-shadow:0 8px 30px rgba(59,130,246,0.6)!important; }
.result-card { background:var(--bg-card); border:1px solid var(--border); border-radius:20px; padding:2rem; margin:1.2rem 0; position:relative; overflow:hidden; }
.result-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.rc-high::before { background:linear-gradient(90deg,#EF4444,#F97316); }
.rc-medium::before { background:linear-gradient(90deg,#F59E0B,#EAB308); }
.rc-low::before { background:linear-gradient(90deg,#10B981,#06B6D4); }
.v-label { font-size:0.68rem; font-weight:500; letter-spacing:0.18em; text-transform:uppercase; color:#4B5563; margin-bottom:0.4rem; }
.v-high { font-family:'Syne',sans-serif; font-size:1.9rem; font-weight:800; color:#EF4444; }
.v-medium { font-family:'Syne',sans-serif; font-size:1.9rem; font-weight:800; color:#F59E0B; }
.v-low { font-family:'Syne',sans-serif; font-size:1.9rem; font-weight:800; color:#10B981; }
.v-sub { color:#9CA3AF; font-size:0.875rem; margin-top:0.4rem; line-height:1.5; }
.m-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:0.9rem; margin:1.2rem 0; }
.m-tile { background:var(--bg-card); border:1px solid var(--border); border-radius:14px; padding:1.1rem 1.3rem; }
.m-lbl { font-size:0.68rem; font-weight:500; letter-spacing:0.14em; text-transform:uppercase; color:#4B5563; margin-bottom:0.4rem; }
.m-val { font-family:'Syne',sans-serif; font-size:1.75rem; font-weight:700; color:#F9FAFB; line-height:1; }
.m-high { color:#EF4444; } .m-medium { color:#F59E0B; } .m-low { color:#10B981; }
.factors-title { font-family:'Syne',sans-serif; font-size:0.72rem; font-weight:700; letter-spacing:0.18em; text-transform:uppercase; color:#4B5563; margin:1.8rem 0 0.9rem; }
.f-wrap { display:flex; flex-wrap:wrap; gap:0.5rem; }
.f-tag { display:inline-flex; align-items:center; gap:0.35rem; padding:0.35rem 0.8rem; border-radius:100px; font-size:0.8rem; font-weight:500; border:1px solid; }
.t-high { background:rgba(239,68,68,0.1); border-color:rgba(239,68,68,0.3); color:#FCA5A5; }
.t-med  { background:rgba(245,158,11,0.1); border-color:rgba(245,158,11,0.3); color:#FCD34D; }
.t-good { background:rgba(16,185,129,0.1); border-color:rgba(16,185,129,0.3); color:#6EE7B7; }
.i-card { background:var(--bg-card); border:1px solid var(--border); border-radius:14px; padding:1.1rem 1.3rem; margin-bottom:0.9rem; }
.i-title { font-family:'Syne',sans-serif; font-size:0.72rem; font-weight:700; letter-spacing:0.16em; text-transform:uppercase; color:#06B6D4; margin-bottom:0.7rem; }
[data-testid="stExpander"] { background:var(--bg-card)!important; border:1px solid var(--border)!important; border-radius:12px!important; margin-bottom:0.6rem!important; }
[data-testid="stExpander"] summary { color:#9CA3AF!important; font-size:0.88rem!important; }
p,li,span { color:#9CA3AF!important; }
h1,h2,h3,h4 { color:#F9FAFB!important; font-family:'Syne',sans-serif!important; }
[data-testid="stAlert"] { background:var(--bg-card)!important; border-radius:10px!important; }
.page-footer { text-align:center; padding:2rem 0; color:#374151; font-size:0.72rem; letter-spacing:0.1em; border-top:1px solid var(--border); margin-top:2.5rem; }
.page-footer span { color:#3B82F6; }
.empty-state { text-align:center; padding:5rem 2rem; }
.empty-icon { font-size:4rem; margin-bottom:1rem; opacity:0.3; }
.empty-title { font-family:'Syne',sans-serif; font-size:1.2rem; font-weight:700; color:#374151; margin-bottom:0.4rem; }
.empty-sub { font-size:0.88rem; color:#374151; line-height:1.5; }
</style>
""", unsafe_allow_html=True)

# ── Feature Config ───────
FEATURE_NAMES = [
    'SeniorCitizen','Partner','Dependents','tenure',
    'PhoneService','MultipleLines','OnlineSecurity','OnlineBackup',
    'DeviceProtection','TechSupport','StreamingTV','StreamingMovies',
    'PaperlessBilling','MonthlyCharges','TotalCharges','gender_Male',
    'InternetService_Fiber optic','InternetService_No',
    'Contract_One year','Contract_Two year',
    'PaymentMethod_Credit card (automatic)',
    'PaymentMethod_Electronic check','PaymentMethod_Mailed check'
]
NUM_FEATURES = ['tenure','MonthlyCharges','TotalCharges']
SCALE_STATS  = {
    'tenure':{'mean':32.49,'std':24.57},
    'MonthlyCharges':{'mean':64.93,'std':30.14},
    'TotalCharges':{'mean':2299.33,'std':2279.00}
}

# ── Load Resources ─
@st.cache_resource
def load_model():
    try:
        with open("model.pkl","rb") as f: return pickle.load(f),None
    except Exception as e: return None,str(e)

@st.cache_resource
def load_scaler():
    try:
        with open("scaler.pkl","rb") as f: return pickle.load(f)
    except: return None

model,model_error = load_model()
scaler = load_scaler()
if model_error:
    st.error(f"❌ Could not load model.pkl: {model_error}")
    st.stop()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">🔮 AI-Powered Retention Intelligence</div>
    <h1 class="hero-title">RetainIQ</h1>
    <p class="hero-sub">Predict customer churn with precision. Act before they leave.</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="s-logo">🔮 RetainIQ</div><div class="s-tag">Churn Intelligence</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-lbl">👤 Demographics</div>', unsafe_allow_html=True)
    gender         = st.selectbox("Gender",["Female","Male"])
    senior_citizen = st.radio("Senior Citizen",["No","Yes"],horizontal=True)
    partner        = st.radio("Has Partner",   ["No","Yes"],horizontal=True)
    dependents     = st.radio("Has Dependents",["No","Yes"],horizontal=True)

    st.markdown('<div class="sec-lbl">📊 Account</div>', unsafe_allow_html=True)
    tenure = st.slider("Tenure (months)",0,72,12)
    c1,c2  = st.columns(2)
    with c1: monthly_charges = st.number_input("Monthly ($)",0.0,200.0,70.0,0.5)
    with c2: total_charges   = st.number_input("Total ($)",0.0,10000.0,float(round(monthly_charges*max(tenure,1),2)),50.0)

    st.markdown('<div class="sec-lbl">📞 Phone</div>', unsafe_allow_html=True)
    phone_service = st.radio("Phone Service",["No","Yes"],horizontal=True)
    if phone_service=="Yes": multiple_lines=st.radio("Multiple Lines",["No","Yes"],horizontal=True)
    else: multiple_lines="No"; st.caption("Multiple Lines: N/A")

    st.markdown('<div class="sec-lbl">🌐 Internet</div>', unsafe_allow_html=True)
    internet_service = st.selectbox("Internet Service",["DSL","Fiber optic","No"])
    if internet_service!="No":
        online_security   = st.radio("Online Security",  ["No","Yes"],horizontal=True)
        online_backup     = st.radio("Online Backup",    ["No","Yes"],horizontal=True)
        device_protection = st.radio("Device Protection",["No","Yes"],horizontal=True)
        tech_support      = st.radio("Tech Support",     ["No","Yes"],horizontal=True)
        streaming_tv      = st.radio("Streaming TV",     ["No","Yes"],horizontal=True)
        streaming_movies  = st.radio("Streaming Movies", ["No","Yes"],horizontal=True)
    else:
        online_security=online_backup=device_protection="No"
        tech_support=streaming_tv=streaming_movies="No"
        st.caption("Add-ons: N/A")

    st.markdown('<div class="sec-lbl">📄 Billing</div>', unsafe_allow_html=True)
    contract_type     = st.selectbox("Contract Type",["Month-to-month","One year","Two year"])
    paperless_billing = st.radio("Paperless Billing",["No","Yes"],horizontal=True)
    payment_method    = st.selectbox("Payment Method",["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"])

# ── Main Layout ───────────────────────────────────────────────────────────────
col_main, col_info = st.columns([3,1],gap="large")

with col_main:
    clicked = st.button("🔮  Run Churn Analysis",type="primary",use_container_width=True)

    if clicked:
        input_data = {
            'SeniorCitizen'    :1 if senior_citizen   =="Yes" else 0,
            'Partner'          :1 if partner          =="Yes" else 0,
            'Dependents'       :1 if dependents       =="Yes" else 0,
            'PhoneService'     :1 if phone_service    =="Yes" else 0,
            'MultipleLines'    :1 if multiple_lines   =="Yes" else 0,
            'OnlineSecurity'   :1 if online_security  =="Yes" else 0,
            'OnlineBackup'     :1 if online_backup    =="Yes" else 0,
            'DeviceProtection' :1 if device_protection=="Yes" else 0,
            'TechSupport'      :1 if tech_support     =="Yes" else 0,
            'StreamingTV'      :1 if streaming_tv     =="Yes" else 0,
            'StreamingMovies'  :1 if streaming_movies =="Yes" else 0,
            'PaperlessBilling' :1 if paperless_billing=="Yes" else 0,
            'tenure'           :float(tenure),
            'MonthlyCharges'   :float(monthly_charges),
            'TotalCharges'     :float(total_charges),
            'gender_Male'                          :1 if gender          =="Male"                      else 0,
            'InternetService_Fiber optic'          :1 if internet_service=="Fiber optic"               else 0,
            'InternetService_No'                   :1 if internet_service=="No"                        else 0,
            'Contract_One year'                    :1 if contract_type   =="One year"                  else 0,
            'Contract_Two year'                    :1 if contract_type   =="Two year"                  else 0,
            'PaymentMethod_Credit card (automatic)':1 if payment_method  =="Credit card (automatic)"   else 0,
            'PaymentMethod_Electronic check'       :1 if payment_method  =="Electronic check"          else 0,
            'PaymentMethod_Mailed check'           :1 if payment_method  =="Mailed check"              else 0,
        }
        input_df = pd.DataFrame([input_data])[FEATURE_NAMES]
        if scaler:
            input_df[NUM_FEATURES] = scaler.transform(input_df[NUM_FEATURES])
        else:
            for feat,stats in SCALE_STATS.items():
                input_df[feat]=(input_df[feat]-stats['mean'])/stats['std']

        try:
            probability = model.predict_proba(input_df)[0][1]
            prediction  = model.predict(input_df)[0]
            pct         = round(probability*100,1)

            if probability>=0.6:
                risk,rclass,vclass="HIGH","rc-high","v-high"
                verdict="⚠️ HIGH CHURN RISK"
                rec="Immediate intervention required — offer a retention discount, assign a dedicated account manager, and run an urgent satisfaction survey."
                gc="#EF4444"; mc="m-high"
            elif probability>=0.35:
                risk,rclass,vclass="MEDIUM","rc-medium","v-medium"
                verdict="📊 MEDIUM CHURN RISK"
                rec="Proactive engagement recommended — schedule a check-in call, offer loyalty rewards, and review service quality."
                gc="#F59E0B"; mc="m-medium"
            else:
                risk,rclass,vclass="LOW","rc-low","v-low"
                verdict="✅ LOW CHURN RISK"
                rec="Customer is satisfied — maintain current service levels and explore upselling or cross-selling opportunities."
                gc="#10B981"; mc="m-low"

            # Verdict card
            st.markdown(f"""
            <div class="result-card {rclass}">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
                    <div style="flex:1;min-width:200px">
                        <div class="v-label">Prediction Result</div>
                        <div class="{vclass}">{verdict}</div>
                        <div class="v-sub">{rec}</div>
                    </div>
                    <div style="text-align:center;padding:0.5rem 1.5rem;background:rgba(0,0,0,0.2);border-radius:12px;">
                        <div class="m-lbl">Churn Score</div>
                        <div class="m-val {mc}" style="font-size:3rem">{pct}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pct,
                number={'suffix':'%','font':{'size':44,'color':'#F9FAFB','family':'Syne'}},
                domain={'x':[0,1],'y':[0,1]},
                gauge={
                    'axis':{'range':[0,100],'tickcolor':'#374151','tickfont':{'color':'#374151','size':10}},
                    'bar' :{'color':gc,'thickness':0.22},
                    'bgcolor':'#0D1424','bordercolor':'#1F2937',
                    'steps':[
                        {'range':[0,35],  'color':'rgba(16,185,129,0.08)'},
                        {'range':[35,60], 'color':'rgba(245,158,11,0.08)'},
                        {'range':[60,100],'color':'rgba(239,68,68,0.08)'}
                    ],
                    'threshold':{'line':{'color':gc,'width':3},'thickness':0.85,'value':pct}
                }
            ))
            fig.update_layout(
                height=260,margin=dict(t=15,b=15,l=25,r=25),
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='DM Sans')
            )
            st.plotly_chart(fig,use_container_width=True)

            # Metric tiles
            st.markdown(f"""
            <div class="m-grid">
                <div class="m-tile">
                    <div class="m-lbl">Churn Probability</div>
                    <div class="m-val {mc}">{pct}%</div>
                </div>
                <div class="m-tile">
                    <div class="m-lbl">Retention Probability</div>
                    <div class="m-val m-low">{round(100-pct,1)}%</div>
                </div>
                <div class="m-tile">
                    <div class="m-lbl">Customer Tenure</div>
                    <div class="m-val">{tenure}<span style="font-size:1rem;color:#6B7280"> mo</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Feature importance chart
            if hasattr(model,'feature_importances_'):
                imp_df = pd.DataFrame({'Feature':FEATURE_NAMES,'Importance':model.feature_importances_}).sort_values('Importance',ascending=True).tail(10)
                fig2 = go.Figure(go.Bar(
                    x=imp_df['Importance'], y=imp_df['Feature'], orientation='h',
                    marker=dict(color=imp_df['Importance'],colorscale=[[0,'#1D4ED8'],[0.5,'#7C3AED'],[1,'#06B6D4']],showscale=False),
                    text=[f"{v:.3f}" for v in imp_df['Importance']],
                    textposition='outside',textfont=dict(color='#6B7280',size=10)
                ))
                fig2.update_layout(
                    title=dict(text='Top 10 Churn Drivers',font=dict(family='Syne',size=13,color='#F9FAFB')),
                    height=360,margin=dict(t=40,b=10,l=10,r=80),
                    paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False,showticklabels=False),
                    yaxis=dict(tickfont=dict(size=10,color='#9CA3AF')),
                    font=dict(family='DM Sans')
                )
                with st.expander("📊 Feature Importance Analysis"):
                    st.plotly_chart(fig2,use_container_width=True)

            # Risk factor tags
            hi,me,go_list=[],[],[]
            if tenure<6:                         hi.append("🕐 Very short tenure")
            elif tenure<12:                      me.append("🕐 Short tenure")
            if monthly_charges>80:               hi.append("💸 High charges")
            elif monthly_charges>60:             me.append("💰 Moderate charges")
            if contract_type=="Month-to-month":  hi.append("📋 Month-to-month")
            if payment_method=="Electronic check":hi.append("💳 Electronic check")
            if tech_support=="No" and internet_service!="No": hi.append("🔧 No tech support")
            if internet_service=="Fiber optic":  me.append("📡 Fiber optic")
            if online_security=="No" and internet_service!="No": me.append("🔓 No security")
            if senior_citizen=="Yes":            me.append("👴 Senior citizen")
            if partner=="No" and dependents=="No":me.append("🏠 Single household")
            if contract_type=="Two year":        go_list.append("📋 Two-year contract")
            if tenure>36:                        go_list.append("⭐ Loyal customer")
            if tech_support=="Yes":              go_list.append("🔧 Tech support active")
            if payment_method in ["Bank transfer (automatic)","Credit card (automatic)"]: go_list.append("💳 Auto payment")
            if online_security=="Yes":           go_list.append("🔒 Security active")

            st.markdown('<div class="factors-title">Risk Factor Analysis</div>', unsafe_allow_html=True)
            tags = '<div class="f-wrap">'
            for f in hi:       tags+=f'<span class="f-tag t-high">{f}</span>'
            for f in me:       tags+=f'<span class="f-tag t-med">{f}</span>'
            for f in go_list:  tags+=f'<span class="f-tag t-good">{f}</span>'
            if not hi+me+go_list: tags+='<span style="color:#4B5563;font-size:0.85rem">No significant factors identified</span>'
            tags+='</div>'
            st.markdown(tags, unsafe_allow_html=True)

            # Debug
            with st.expander("🔍 Debug: Model Input"):
                st.dataframe(input_df,use_container_width=True)

        except Exception as e:
            st.error(f"❌ Prediction error: {e}")
            import traceback
            with st.expander("Error Details"): st.code(traceback.format_exc())

    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🔮</div>
            <div class="empty-title">Ready to Analyze</div>
            <div class="empty-sub">Configure customer details in the sidebar,<br>then click Run Churn Analysis</div>
        </div>
        """, unsafe_allow_html=True)

# ── Info Panel ────────────────────────────────────────────────────────────────
with col_info:
    with st.expander("🔴 High Risk Profile"):
        st.markdown("""
**Expected: 70–85% churn**
- Senior: **Yes**
- Tenure: **2 months**
- Monthly: **$95**
- Internet: **Fiber optic**
- Security: **No**, Support: **No**
- Contract: **Month-to-month**
- Payment: **Electronic check**
""")
    with st.expander("🟢 Low Risk Profile"):
        st.markdown("""
**Expected: 5–15% churn**
- Senior: **No**, Partner: **Yes**
- Tenure: **60 months**
- Monthly: **$35**
- Internet: **DSL**
- Tech Support: **Yes**
- Contract: **Two year**
- Payment: **Bank transfer**
""")
    st.markdown(f"""
    <div class="i-card">
        <div class="i-title">📊 Risk Levels</div>
        <div style="font-size:0.82rem;line-height:2">
            <span style="color:#10B981!important">●</span> &lt;35% Low Risk<br>
            <span style="color:#F59E0B!important">●</span> 35–60% Medium Risk<br>
            <span style="color:#EF4444!important">●</span> &gt;60% High Risk
        </div>
    </div>
    <div class="i-card">
        <div class="i-title">🤖 Model</div>
        <div style="font-size:0.82rem;line-height:2;color:#6B7280!important">
            Type: <span style="color:#93C5FD!important">{type(model).__name__}</span><br>
            Features: <span style="color:#93C5FD!important">{len(FEATURE_NAMES)}</span><br>
            Scaler: <span style="color:{'#6EE7B7' if scaler else '#FCA5A5'}!important">{'✅ Loaded' if scaler else '⚠️ Approx'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
    <span>RetainIQ</span> · Customer Churn Intelligence · Built with Streamlit & scikit-learn
</div>
""", unsafe_allow_html=True)
