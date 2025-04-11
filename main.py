import streamlit as st

st.write("🔥 App is starting...")

try:
    st.write("👀 About to do something simple...")
    st.write(1 + 1)
    st.success("✅ App ran successfully!")

except Exception as e:
    st.error("❌ Error running the app")
    st.exception(e)
