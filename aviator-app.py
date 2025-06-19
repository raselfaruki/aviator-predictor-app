import streamlit as st
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Custom Theme Setup (Dark / Light)
theme = st.sidebar.radio("🎨 থিম বেছে নিন:", ["Dark", "Light"])
if theme == "Dark":
    st.markdown("<style>body{background-color:#0E1117; color:white}</style>", unsafe_allow_html=True)

# Title
st.title("✈️ Aviator Predictor Game (Streamlit Pro Edition 🇧🇩)")

# Cashout target
cashout_x = st.sidebar.number_input("🎯 আপনার Target Cashout (x):", min_value=1.0, max_value=10.0, value=2.0, step=0.1)

# Auto Sim Settings
auto_rounds = st.sidebar.slider("🔁 কয়টি রাউন্ড চালাতে চান?", 1, 100, 1)
if "results" not in st.session_state:
    st.session_state.results = []

# Game Logic
def generate_multiplier():
    return round(random.expovariate(1/2), 2)

def analyze_signal(data):
    if len(data) < 5:
        return "🔄 পর্যাপ্ত ডেটা নেই"
    avg = np.mean(data[-5:])
    if avg > 2.0:
        return "📈 হাই ট্রেন্ড"
    elif avg < 1.5:
        return "📉 লো ট্রেন্ড"
    else:
        return "🔄 ট্রেন্ড অস্পষ্ট"

def cashout_result(mult, target):
    return "✅ জিতেছেন!" if mult >= target else "❌ হারিয়েছেন"

# Simulate button
if st.button("🚀 রাউন্ড শুরু করুন"):
    for _ in range(auto_rounds):
        m = generate_multiplier()
        st.session_state.results.append(m)
    st.success(f"{auto_rounds} রাউন্ড সফলভাবে সম্পন্ন হয়েছে!")

# Display Results
if st.session_state.results:
    latest = st.session_state.results[-1]
    st.markdown(f"**📊 সর্বশেষ মাল্টিপ্লায়ার:** `{latest}x`")
    st.markdown(f"**📡 সিগন্যাল:** `{analyze_signal(st.session_state.results)}`")
    st.markdown(f"**💰 রেজাল্ট:** `{cashout_result(latest, cashout_x)}`")

    # Line Chart
    st.subheader("📈 মাল্টিপ্লায়ার ট্রেন্ড")
    fig, ax = plt.subplots()
    ax.plot(st.session_state.results[-50:], marker="o", color="blue")
    ax.set_xlabel("রাউন্ড")
    ax.set_ylabel("x মাল্টিপ্লায়ার")
    ax.grid(True)
    st.pyplot(fig)

    # Download Option
    df = pd.DataFrame(st.session_state.results, columns=["Multiplier"])
    st.download_button("📥 CSV এক্সপোর্ট", df.to_csv(index=False), file_name="aviator_results.csv")

# Reset button
if st.button("🔄 নতুন করে শুরু করুন"):
    st.session_state.results = []
    st.warning("রেজাল্ট লিস্ট ক্লিয়ার করা হয়েছে।")
