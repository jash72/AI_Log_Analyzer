import os
import streamlit as st
import pandas as pd

from services.excel_reader import read_excel
from services.preprocessor import preprocess_logs
from services.matcher import compare_logs
from services.ai_explainer import add_ai_explanations
from services.report_generator import generate_excel_report

from utils.helper import (
    ensure_directory,
    generate_report_name
)


# ==========================================================
# INITIAL SETUP
# ==========================================================

st.set_page_config(
    page_title="AI Device Log Analyzer",
    page_icon="🔍",
    layout="wide"
)

ensure_directory("uploads")
ensure_directory("output")


# ==========================================================
# HEADER
# ==========================================================

st.title("🔍 AI Device Log Analyzer")

st.markdown(
    """
Compare two device log Excel files using an intelligent matching engine.

### Supported Features

- ✅ 10,000+ Log Entries
- ✅ Order Independent Comparison
- ✅ Detect Added Logs
- ✅ Detect Removed Logs
- ✅ Detect Modified Logs
- ✅ AI Generated Explanations
- ✅ Excel Report Download

**Input Format**

| Logs |
|------|
| hostname server01 |
| interface eth0 |
| ip address 10.1.1.1 |

One log entry per row.
"""
)

st.divider()


# ==========================================================
# FILE UPLOAD
# ==========================================================

left, right = st.columns(2)

with left:

    day1_file = st.file_uploader(
        "📄 Upload Day 1 Excel",
        type=["xlsx"]
    )

with right:

    day2_file = st.file_uploader(
        "📄 Upload Day 2 Excel",
        type=["xlsx"]
    )


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Settings")

show_unchanged = st.sidebar.checkbox(
    "Show Unchanged Logs",
    value=True
)

generate_ai = st.sidebar.checkbox(
    "Generate AI Explanations",
    value=True
)


# ==========================================================
# COMPARE BUTTON
# ==========================================================

if st.button(
    "🚀 Compare Logs",
    use_container_width=True
):

    if day1_file is None or day2_file is None:

        st.error("Please upload both Excel files.")

    else:

        # ==================================================
        # Save Uploads
        # ==================================================

        day1_path = os.path.join(
            "uploads",
            f"day1_{day1_file.name}"
        )

        with open(day1_path, "wb") as f:
            f.write(day1_file.getbuffer())

        day2_path = os.path.join(
            "uploads",
            f"day2_{day2_file.name}"
        )

        with open(day2_path, "wb") as f:
            f.write(day2_file.getbuffer())

        # ==================================================
        # Read Excel
        # ==================================================

        with st.spinner("Reading Excel Files..."):

            day1_logs = read_excel(day1_path)
            day2_logs = read_excel(day2_path)

        # ==================================================
        # Preprocessing
        # ==================================================

        with st.spinner("Preprocessing Logs..."):

            day1_logs = preprocess_logs(day1_logs)
            day2_logs = preprocess_logs(day2_logs)

        # ==================================================
        # Comparison
        # ==================================================

        with st.spinner("Comparing Logs..."):

            summary, results = compare_logs(
                day1_logs,
                day2_logs
            )

        # ==================================================
        # AI Explanation
        # ==================================================

        if generate_ai:

            with st.spinner(
                "Generating AI Explanations..."
            ):

                results = add_ai_explanations(
                    results
                )

        else:

            for row in results:
                row["reason"] = ""

        # ==================================================
        # SUMMARY
        # ==================================================

        st.success(
            "Comparison Completed Successfully!"
        )

        st.divider()

        st.subheader("📊 Summary")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Day 1 Logs",
                summary["total_day1"]
            )

            st.metric(
                "Unchanged",
                summary["unchanged"]
            )

        with c2:

            st.metric(
                "Day 2 Logs",
                summary["total_day2"]
            )

            st.metric(
                "Modified",
                summary["modified"]
            )

        with c3:

            st.metric(
                "Added",
                summary["added"]
            )

            st.metric(
                "Removed",
                summary["removed"]
            )

        st.divider()

        # ==================================================
        # CHART
        # ==================================================

        st.subheader(
            "📈 Change Distribution"
        )

        chart_df = pd.DataFrame({

            "Category": [
                "Added",
                "Removed",
                "Modified",
                "Unchanged"
            ],

            "Count": [

                summary["added"],
                summary["removed"],
                summary["modified"],
                summary["unchanged"]

            ]

        })

        st.bar_chart(
            chart_df.set_index(
                "Category"
            )
        )

        st.divider()

        # ==================================================
        # RESULTS TABLE
        # ==================================================

        st.subheader(
            "📋 Comparison Result"
        )

        df = pd.DataFrame(
            results
        )

        if not show_unchanged:

            df = df[
                df["type"] != "Unchanged"
            ]

        filter_type = st.selectbox(

            "Filter",

            [
                "All",
                "Added",
                "Removed",
                "Modified",
                "Unchanged"
            ]

        )

        if filter_type != "All":

            df = df[
                df["type"] == filter_type
            ]

        st.write(
            f"Total Rows : {len(df)}"
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )

        st.divider()

        # ==================================================
        # REPORT GENERATION
        # ==================================================

        report_name = generate_report_name()

        output_path = os.path.join(
            "output",
            report_name
        )

        with st.spinner(
            "Generating Excel Report..."
        ):

            generate_excel_report(
                results,
                output_path
            )

        # ==================================================
        # DOWNLOAD
        # ==================================================

        with open(
            output_path,
            "rb"
        ) as file:

            st.download_button(

                label="⬇️ Download Excel Report",

                data=file,

                file_name=report_name,

                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                use_container_width=True

            )

        st.divider()

        # ==================================================
        # PREVIEW
        # ==================================================

        with st.expander(
            "Preview First 25 Rows"
        ):

            st.dataframe(
                df.head(25),
                use_container_width=True
            )

        # ==================================================
        # DEBUG INFORMATION
        # ==================================================

        with st.expander(
            "System Information"
        ):

            st.write(
                {
                    "Day1 File":
                        day1_file.name,

                    "Day2 File":
                        day2_file.name,

                    "Total Day1 Logs":
                        summary["total_day1"],

                    "Total Day2 Logs":
                        summary["total_day2"],

                    "Added":
                        summary["added"],

                    "Removed":
                        summary["removed"],

                    "Modified":
                        summary["modified"],

                    "Unchanged":
                        summary["unchanged"]

                }
            )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "AI Device Log Analyzer v1.0"
)

st.caption(
    "Built with Streamlit + Pandas + RapidFuzz + Ollama"
)