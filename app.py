"""
Resume vs Job Description Matcher
Phase 3: Polished UI + clearer insights

Run with:  streamlit run app.py
"""

import streamlit as st
from utils.pdf_parser import extract_resume_text
from utils.matcher import compute_match_score, get_skill_gap

st.set_page_config(page_title="Resume vs JD Matcher", page_icon="📄", layout="centered")

# ---------- Header ----------
st.title("📄 Resume vs Job Description Matcher")
st.caption("Upload your resume, paste a job description, and get an instant match score + skill gap analysis.")

# ---------- Inputs ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("1️⃣ Your Resume")
    uploaded_file = st.file_uploader("Upload resume (PDF only)", type=["pdf"], label_visibility="collapsed")

with col2:
    st.subheader("2️⃣ Job Description")
    jd_text = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the full job description text here...",
        label_visibility="collapsed",
    )

analyze_clicked = st.button("🔍 Analyze Match", type="primary", use_container_width=True)

# ---------- Analysis ----------
if analyze_clicked:
    if uploaded_file is None:
        st.warning("Please upload your resume PDF first.")
    elif not jd_text.strip():
        st.warning("Please paste a job description first.")
    else:
        with st.spinner("Extracting resume text..."):
            try:
                resume_text = extract_resume_text(uploaded_file)
            except ValueError as e:
                st.error(str(e))
                st.stop()

        with st.spinner("Analyzing match..."):
            score = compute_match_score(resume_text, jd_text)
            gap = get_skill_gap(resume_text, jd_text)

        total_jd_skills = len(gap["matched"]) + len(gap["missing"])
        coverage = round((len(gap["matched"]) / total_jd_skills) * 100) if total_jd_skills else None

        st.divider()

        # --- Top metrics row ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Overall Match Score", f"{score}%")
        m2.metric("Skills Matched", f"{len(gap['matched'])}/{total_jd_skills}" if total_jd_skills else "N/A")
        m3.metric("Bonus Skills Found", len(gap["resume_only"]))

        # --- Score banner ---
        if score >= 70:
            st.success(f"🎯 **Strong match ({score}%)** — your resume aligns well with this role.")
        elif score >= 40:
            st.warning(f"⚖️ **Moderate match ({score}%)** — some tailoring will help.")
        else:
            st.error(f"⚠️ **Low match ({score}%)** — consider rewording your resume to mirror the JD's language.")

        st.progress(min(int(score), 100))

        with st.expander("ℹ️ How is this score calculated?"):
            st.markdown(
                "- **Overall Match Score** uses *TF-IDF + cosine similarity* — it measures how "
                "closely the overall wording/content of your resume overlaps with the JD's wording.\n"
                "- **Skills Matched** is a separate, more literal check against a curated list of "
                "~90 common tech & soft skills.\n"
                "- A low overall score with good skill coverage usually means the JD has a lot of "
                "generic company text (about us, benefits, etc.) — try mirroring the JD's exact "
                "phrasing in your resume to boost this."
            )

        st.divider()

        # --- Skill breakdown tabs ---
        st.subheader("🧩 Skill Breakdown")
        tab1, tab2, tab3 = st.tabs([
            f"✅ Matched ({len(gap['matched'])})",
            f"❌ Missing ({len(gap['missing'])})",
            f"➕ Bonus ({len(gap['resume_only'])})",
        ])

        with tab1:
            if gap["matched"]:
                st.markdown(" ".join([f"`{s}`" for s in gap["matched"]]))
            else:
                st.caption("No overlapping skills detected.")

        with tab2:
            if gap["missing"]:
                st.markdown(" ".join([f"`{s}`" for s in gap["missing"]]))
                st.info(
                    "💡 If you genuinely have experience with any of these, add them to your resume "
                    "using the JD's exact wording — that improves both the score and ATS keyword matching."
                )
            else:
                st.caption("🎉 No missing skills — great coverage for this role!")

        with tab3:
            if gap["resume_only"]:
                st.markdown(" ".join([f"`{s}`" for s in gap["resume_only"]]))
                st.caption("These are on your resume but weren't explicitly asked for in this JD.")
            else:
                st.caption("No extra skills detected beyond what the JD asks for.")

        st.divider()
        with st.expander("📄 Show extracted resume text"):
            st.text_area("Resume text", resume_text, height=300, label_visibility="collapsed")

else:
    st.info("👆 Upload your resume and paste a job description, then click **Analyze Match**.")
