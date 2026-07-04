"""
Resume vs Job Description Matcher
Phase 4: Compare resume against MULTIPLE job descriptions at once,
ranked by match score, so you can see which role fits you best.

Run with:  streamlit run app.py
"""

import streamlit as st
from utils.pdf_parser import extract_resume_text
from utils.matcher import compute_match_score, get_skill_gap

st.set_page_config(page_title="Resume vs JD Matcher", page_icon="📄", layout="centered")

st.title("📄 Resume vs Job Description Matcher")
st.caption(
    "Upload your resume once, add multiple job descriptions, and see which "
    "role you're the strongest match for."
)

# ---------- Session state setup ----------
# Each JD entry is a dict: {"title": str, "text": str}
if "jd_entries" not in st.session_state:
    st.session_state.jd_entries = [{"title": "", "text": ""}]


def add_jd():
    st.session_state.jd_entries.append({"title": "", "text": ""})


def remove_jd(index):
    st.session_state.jd_entries.pop(index)


# ---------- Resume upload ----------
st.subheader("1️⃣ Your Resume")
uploaded_file = st.file_uploader("Upload resume (PDF only)", type=["pdf"], label_visibility="collapsed")

st.divider()

# ---------- Job description entries ----------
st.subheader("2️⃣ Job Descriptions to Compare")

for i, entry in enumerate(st.session_state.jd_entries):
    with st.container(border=True):
        col_title, col_remove = st.columns([5, 1])
        with col_title:
            st.session_state.jd_entries[i]["title"] = st.text_input(
                "Job title / company (label for this JD)",
                value=entry["title"],
                key=f"title_{i}",
                placeholder=f"e.g. Data Analyst Intern @ Company {i + 1}",
            )
        with col_remove:
            st.write("")  # spacer to align button with input
            if len(st.session_state.jd_entries) > 1:
                st.button("🗑️ Remove", key=f"remove_{i}", on_click=remove_jd, args=(i,))

        st.session_state.jd_entries[i]["text"] = st.text_area(
            "Paste job description",
            value=entry["text"],
            key=f"text_{i}",
            height=150,
            placeholder="Paste the full job description text here...",
            label_visibility="collapsed",
        )

st.button("➕ Add another job description", on_click=add_jd, use_container_width=True)

st.divider()
analyze_clicked = st.button("🔍 Compare All Matches", type="primary", use_container_width=True)

# ---------- Analysis ----------
if analyze_clicked:
    valid_jds = [e for e in st.session_state.jd_entries if e["text"].strip()]

    if uploaded_file is None:
        st.warning("Please upload your resume PDF first.")
    elif not valid_jds:
        st.warning("Please paste at least one job description first.")
    else:
        with st.spinner("Extracting resume text..."):
            try:
                resume_text = extract_resume_text(uploaded_file)
            except ValueError as e:
                st.error(str(e))
                st.stop()

        with st.spinner(f"Analyzing {len(valid_jds)} job description(s)..."):
            results = []
            for idx, jd in enumerate(valid_jds):
                label = jd["title"].strip() or f"Job Description {idx + 1}"
                score = compute_match_score(resume_text, jd["text"])
                gap = get_skill_gap(resume_text, jd["text"])
                results.append({"label": label, "score": score, "gap": gap})

            # Rank best to worst
            results.sort(key=lambda r: r["score"], reverse=True)

        st.divider()
        st.subheader("🏆 Ranking — Best Match First")

        for rank, r in enumerate(results, start=1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")
            total_skills = len(r["gap"]["matched"]) + len(r["gap"]["missing"])

            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 4, 2])
                c1.markdown(f"### {medal}")
                c2.markdown(f"**{r['label']}**")
                c3.metric("Match Score", f"{r['score']}%", label_visibility="collapsed")

                st.progress(min(int(r["score"]), 100))

                with st.expander(f"See skill breakdown for {r['label']}"):
                    t1, t2, t3 = st.tabs([
                        f"✅ Matched ({len(r['gap']['matched'])})",
                        f"❌ Missing ({len(r['gap']['missing'])})",
                        f"➕ Bonus ({len(r['gap']['resume_only'])})",
                    ])
                    with t1:
                        st.markdown(" ".join([f"`{s}`" for s in r["gap"]["matched"]]) or "_None found_")
                    with t2:
                        st.markdown(" ".join([f"`{s}`" for s in r["gap"]["missing"]]) or "_None — great coverage!_")
                    with t3:
                        st.markdown(" ".join([f"`{s}`" for s in r["gap"]["resume_only"]]) or "_None found_")

        st.divider()
        best = results[0]
        st.success(
            f"💡 Based on this comparison, **{best['label']}** ({best['score']}%) is your strongest "
            f"match. Consider prioritizing this application, or use the missing skills from lower-ranked "
            f"roles to guide what to learn next."
        )

        with st.expander("📄 Show extracted resume text"):
            st.text_area("Resume text", resume_text, height=300, label_visibility="collapsed")

else:
    st.info("👆 Upload your resume, add one or more job descriptions, then click **Compare All Matches**.")
