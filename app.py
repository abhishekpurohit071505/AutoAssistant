import streamlit as st
import requests
import json

LAMBDA_API_URL = "https://q3pk9j6x76.execute-api.us-east-1.amazonaws.com/staging/diagnose"

st.set_page_config(page_title="AutoFix Assistant", layout="centered")

st.title("🔧 AutoFix Assistant")
st.subheader("Diagnose and Fix Your Vehicle Problems")

user_input = st.text_area("Describe your issue:", placeholder="e.g., My car is making noise while driving")

if st.button("Diagnose"):
    if not user_input.strip():
        st.warning("Please enter a description of your issue.")
    else:
        with st.spinner("Analyzing..."):
            try:
                #st.write("Sending this to Lambda:", {"query": user_input})
                response = requests.post(LAMBDA_API_URL, json={"query": user_input})
                st.code(response.text, language='json')

                # ✅ Parse the outer response first
                if response.status_code == 200:
                    try:
                        
                        #st.write("DEBUG report:", response.json())
                        report = response.json()

                        st.success("Diagnosis Complete!")
                        st.markdown(f"**🔍 Problem:** {report.get('input', 'N/A')}")

                        diagnosis = report.get("diagnosis", "")
                        if "Reason:" in diagnosis:
                            cause = diagnosis.split("Cause:", 1)[1].split("Reason:")[0].strip()
                            reason = diagnosis.split("Reason:", 1)[1].strip()
                        else:
                            cause, reason = diagnosis, ""

                        st.markdown(f"**💥 Cause:** {cause}")
                        st.markdown(f"**🧠 Reason:** {reason}")
                        st.markdown("---")
                        st.markdown(f"**🛠 Fix Guide:**\n\n{report.get('fix_guide', '')}", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed to parse JSON response: {e}")
                        st.text(response.text)
                else:
                    st.error(f"Error from Lambda: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
