import pandas as pd
import plotly.express as px
import datetime

DATA_FILE = "dataset.csv"
OUTPUT_HTML_FILE = "QA_visualization.html"

df = pd.read_csv(DATA_FILE)

current_year = datetime.datetime.now().year
df["dob_numeric"] = pd.to_numeric(df["dob"], errors="coerce")
df["age"] = df["dob_numeric"].apply(lambda x: current_year - x if pd.notna(x) else None)

df["Franchise_numeric"] = pd.to_numeric(df["Franchise"], errors="coerce")

total_records = len(df)
missing_data = df.isnull().sum().sort_values(ascending=False)
missing_percentage = (df.isnull().sum() / total_records * 100).sort_values(
    ascending=False
)

completeness_df = pd.DataFrame(
    {
        "Field": missing_data.index,
        "Missing Count": missing_data.values,
        "Missing Percentage (%)": missing_percentage.values,
    }
).reset_index(drop=True)

completeness_df = completeness_df[completeness_df["Missing Percentage (%)"] < 100]

fig_completeness_bar = px.bar(
    completeness_df,
    x="Missing Percentage (%)",
    y="Field",
    orientation="h",
    title="Field Completeness: Percentage of Missing Values",
    text="Missing Percentage (%)",
    height=min(800, len(completeness_df) * 30 + 150),
    color_discrete_sequence=["#1a80e0"],
)
fig_completeness_bar.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
fig_completeness_bar.update_layout(
    yaxis={"categoryorder": "total ascending"},
    uniformtext_minsize=8,
    uniformtext_mode="hide",
)

name_counts = df["name"].value_counts(dropna=False).reset_index()
name_counts.columns = ["Insurer Name", "Count"]
name_counts["Insurer Name"] = name_counts["Insurer Name"].fillna("MISSING")

fig_insurer_dist_bar = px.bar(
    name_counts.head(20),
    x="Insurer Name",
    y="Count",
    title="Top 20 Insurance Provider Distribution",
    hover_data=["Count"],
    height=450,
)
fig_insurer_dist_bar.update_layout(
    xaxis_title="Insurer Name", yaxis_title="Number of Records"
)

fig_insurer_dist_pie = px.pie(
    name_counts,
    values="Count",
    names="Insurer Name",
    title="Insurance Provider Distribution",
    height=450,
)

postcode_counts = df["post_code"].astype(str).value_counts(dropna=False).reset_index()
postcode_counts.columns = ["Post Code", "Count"]
postcode_counts["Post Code"] = postcode_counts["Post Code"].fillna("MISSING")
postcode_counts = postcode_counts.sort_values(by="Count", ascending=False)
fig_postcode_dist = px.bar(
    postcode_counts.head(50),
    x="Post Code",
    y="Count",
    title="Postal Code Distribution by Count",
    hover_data=["Count"],
    height=450,
)
fig_postcode_dist.update_layout(
    xaxis_title="Post Code", yaxis_title="Number of Records"
)

gender_counts = df["gender"].value_counts(dropna=False).reset_index()
gender_counts.columns = ["Gender", "Count"]
gender_counts["Gender"] = gender_counts["Gender"].fillna("MISSING")

fig_gender_dist = px.pie(
    gender_counts,
    values="Count",
    names="Gender",
    title="Gender Distribution",
    height=450,
)

valid_ages_df = df[df["age"].notna() & (df["age"] > 0) & (df["age"] < 120)]
fig_dob_dist = px.histogram(
    valid_ages_df,
    x="age",
    nbins=20,
    title="Year of Birth (Age) Distribution",
    labels={"age": "Age (Years)"},
    marginal="box",
    height=450,
)
fig_dob_dist.update_layout(
    xaxis_title="Age (Years)", yaxis_title="Count of Individuals"
)

spital_counts = df["Spitalzusatzversicherung"].value_counts(dropna=False).reset_index()
spital_counts.columns = ["Insurance Type", "Count"]
spital_counts["Insurance Type"] = spital_counts["Insurance Type"].fillna("MISSING")

fig_spital_coverage = px.bar(
    spital_counts,
    x="Insurance Type",
    y="Count",
    title="Hospital Insurance Type Coverage (Spitalzusatzversicherung)",
    height=450,
)
fig_spital_coverage.update_layout(xaxis_title="Insurance Type", yaxis_title="Count")

franchise_counts = df["Franchise_numeric"].value_counts(dropna=False).reset_index()
franchise_counts.columns = ["Franchise Value Raw", "Count"]
franchise_counts["Franchise Value Display"] = franchise_counts[
    "Franchise Value Raw"
].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "MISSING")

sorted_numeric_franchise = sorted(
    franchise_counts["Franchise Value Raw"].dropna().unique()
)
category_order_franchise = [f"{val:.1f}" for val in sorted_numeric_franchise]
if "MISSING" in franchise_counts["Franchise Value Display"].values:
    category_order_franchise.append("MISSING")

fig_franchise_dist = px.bar(
    franchise_counts,
    x="Franchise Value Display",
    y="Count",
    title="Franchise (Deductible) Value Distribution (including missing)",
    height=450,
)
fig_franchise_dist.update_layout(
    xaxis_title="Franchise Value",
    yaxis_title="Count",
    xaxis={"categoryorder": "array", "categoryarray": category_order_franchise},
)

product_name_counts = df["Product name"].value_counts(dropna=False).reset_index()
product_name_counts.columns = ["Product Name", "Count"]
product_name_counts["Product Name"] = product_name_counts["Product Name"].fillna(
    "MISSING"
)

fig_product_name_bar = px.bar(
    product_name_counts.head(10),
    x="Product Name",
    y="Count",
    title="Top 10 Product Name Distribution",
    height=450,
)
fig_product_name_bar.update_layout(xaxis_title="Product Name", yaxis_title="Count")


plot_html_completeness = fig_completeness_bar.to_html(
    full_html=False, include_plotlyjs="cdn"
)
plot_html_insurer_bar = fig_insurer_dist_bar.to_html(
    full_html=False, include_plotlyjs="cdn"
)
plot_html_insurer_pie = fig_insurer_dist_pie.to_html(
    full_html=False, include_plotlyjs="cdn"
)
plot_html_postcode = fig_postcode_dist.to_html(full_html=False, include_plotlyjs="cdn")
plot_html_gender = fig_gender_dist.to_html(full_html=False, include_plotlyjs="cdn")
plot_html_dob = fig_dob_dist.to_html(full_html=False, include_plotlyjs="cdn")
plot_html_spital = fig_spital_coverage.to_html(full_html=False, include_plotlyjs="cdn")
plot_html_franchise = fig_franchise_dist.to_html(
    full_html=False, include_plotlyjs="cdn"
)


html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data QA Assessment Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ font-family: sans-serif; margin: 20px; background-color: #f4f7f6; color: #333; }}
        .header {{ text-align: center; margin-bottom: 40px; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header h1 {{ color: #2c3e50; }}
        .summary-box {{ background-color: #d6eaff; border: 1px solid #a6cff7; padding: 15px; border-radius: 5px; text-align: center; font-size: 1.5em; font-weight: bold; margin-bottom: 30px; color: #0a4f8f; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .section {{ margin-bottom: 50px; padding: 25px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .section h2 {{ color: #34495e; border-bottom: 2px solid #aec6cf; padding-bottom: 10px; margin-bottom: 20px; }}
        /* IMPROVED: Stronger border and shadow for plot containers */
        .plot-container {{
            margin-bottom: 30px;
            background-color: #fdfdfd;
            padding: 15px;
            border-radius: 5px;
            border: 2px solid #dcdcdc; /* More distinct border */
            box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* Slight shadow */
        }}
        .plot-container h3 {{ color: #4a6c8e; margin-top: 0; }}
        .explanation {{ background-color: #eaf2f8; border-left: 5px solid #6cb2eb; padding: 15px; margin-top: 15px; border-radius: 4px; }}
        .explanation p {{ margin: 5px 0; font-size: 0.95em; line-height: 1.4; }}
        .explanation strong {{ color: #2c3e50; }}
        .chart-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        @media (max-width: 768px) {{
            .chart-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

    <div class="header">
        <h1>Data QA Assessment Report</h1>
    </div>

    <div class="summary-box">
        Total Records in Dataset: {total_records}
    </div>

    <div class="section">
        <h2>1. Completeness (Missing Values) Overview</h2>
        <div class="plot-container">
            <h3>Percentage of Missing Values Per Field</h3>
            {plot_html_completeness}
            <div class="explanation">
                <p><strong>Why:</strong> This visualization is needed for QA analysts as it highlights the extent of missing or incomplete data in each field. Fields with a high percentage of missing values indicates data collection issues or unreliable data.</p>
                <p><strong>Insight:</strong> Helps spot incomplete or unreliable fields. Shows the columns to focus on data cleaning or re-collection.</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>2. Insurance Provider Distribution (Field: name)</h2>
        <div class="chart-grid">
            <div class="plot-container">
                <h3>Insurance Provider Distribution (Bar Chart)</h3>
                {plot_html_insurer_bar}
            </div>
            <div class="plot-container">
                <h3>Insurance Provider Distribution (Pie Chart)</h3>
                {plot_html_insurer_pie}
            </div>
        </div>
        <div class="explanation">
            <p><strong>Why:</strong> To see how data is distributed across different insurance providers.</p>
            <p><strong>Insight:</strong> Detect imbalance or missing entries.</p>
        </div>
    </div>

    <div class="section">
        <h2>3. Postal Code Distribution (Field: post_code)</h2>
        <div class="plot-container">
            <h3>Postal Code Distribution by Count</h3>
            {plot_html_postcode}
            <div class="explanation">
                <p><strong>Why:</strong> This is useful for understanding the geographic coverage of the collected data. If the data is expected to cover a wide area, seeing a concentration in only a few postcodes could signal issues in data collection coverage.</p>
                <p><strong>Insight:</strong> Helps spot missing coverage in certain geographical areas or potential data duplication if a single postcode has an high number of records compared to others.</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>4. Gender Distribution (Field: gender)</h2>
        <div class="plot-container">
            <h3>Gender Distribution</h3>
            {plot_html_gender}
            <div class="explanation">
                <p><strong>Why:</strong> To check for data imbalance or incorrect input within the gender field.</p>
                <p><strong>Insight:</strong> Reveals if all genders are adequately represented and helps identify any invalid or inconsistent entries (e.g., like "male" vs "Male", or unexpected categories beyond standard 'Male', 'Female').</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>5. Year of Birth (Age) Distribution (Field: dob)</h2>
        <div class="plot-container">
            <h3>Year of Birth (Age) Distribution</h3>
            {plot_html_dob}
            <div class="explanation">
                <p><strong>Why:</strong> Calculating age from the year of birth provides a more intuitive view of the demographic distribution.</p>
                <p><strong>Insight:</strong> Helps spot unrealistic ages, potential data entry errors, or incorrect data formats.</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>6. Hospital Insurance Type Coverage (Field: Spitalzusatzversicherung)</h2>
        <div class="plot-container">
            <h3>Hospital Insurance Type Coverage (Spitalzusatzversicherung)</h3>
            {plot_html_spital}
            <div class="explanation">
                <p><strong>Why:</strong> This visualization ensures that the data has consistent and expected insurance types. It's important to verify that only valid or anticipated categories are present.</p>
                <p><strong>Insight:</strong> Helps identify the most common values and detect unexpected categories in the dataset. A high count of 'MISSING' entries indicates a lack of information for this field.</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>7. Franchise (Deductible) Distribution (Field: Franchise)</h2>
        <div class="plot-container">
            <h3>Franchise (Deductible) Value Distribution</h3>
            {plot_html_franchise}
            <div class="explanation">
                <p><strong>Why:</strong> This chart is useful for understanding the common financial responsibility trends in the dataset and for quickly spotting incorrect or missing data.</p>
                <p><strong>Insight:</strong> Helps identify outliers or invalid entries. The presence of high 'MISSING' bar highlights incomplete data for this financial field.</p>
            </div>
        </div>
    </div>

</body>
</html>
"""

with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Data QA report generated successfully to {OUTPUT_HTML_FILE}")
print(
    f"Please open '{OUTPUT_HTML_FILE}' in your web browser to view the interactive report."
)
