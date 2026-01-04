<p align="center">
  <img src="https://img.shields.io/badge/SQL-MySQL-blue?logo=mysql&logoColor=white" alt="MySQL Badge" />
  <img src="https://img.shields.io/badge/Status-Completed-success" alt="Completed Badge" />
  <img src="https://img.shields.io/badge/Lines%20of%20SQL-200+-informational" alt="LOC Badge" />
</p>

<h1 align="center">RetailSmart Analytics Capstone: Unlocking E-Commerce Insights</h1>
<p align="center"><em>Graded Capstone Project for the Data Science &amp; Business Analytics Program by Emeritus IITG</em></p>

---

Hey there, data enthusiast! Imagine transforming raw, messy data into a powerhouse of business intelligence that predicts customer churn, forecasts sales, and drives strategic decisions. That's exactly what this capstone project does for RetailSmart, a bustling e-commerce retailer. Buckle up as we dive into a comprehensive journey from data wrangling to dazzling dashboards—frankly speaking, this isn't just analysis; it's a game-changer for retail success.

This project is your hands-on playground for mastering data science in a real-world context. We'll tackle everything from scrubbing datasets to building predictive models and crafting interactive visualizations. Whether you're a budding analyst or a seasoned pro, you'll walk away with skills that scream "advanced" and insights that shout "actionable." Let's get started—your data adventure awaits!

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Phases Breakdown](#phases-breakdown)
- [Prerequisites and Setup](#prerequisites-and-setup)
- [Installation Guide](#installation-guide)
- [Usage Instructions](#usage-instructions)
- [Output Files and Deliverables](#output-files-and-deliverables)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Overview
RetailSmart Analytics is all about turning data chaos into clarity. Picture this: a mid-sized e-commerce giant grappling with declining repeat purchases and uneven sales. Our mission? To explore, clean, model, and visualize data from five core datasets—customers, products, sales, marketing, and reviews—to uncover hidden patterns, predict churn, and forecast demand.

This capstone is structured in four progressive phases, blending SQL for extraction, Python for heavy lifting, and Power BI for storytelling. You'll handle missing values, outliers, and integrity checks, then graduate to machine learning models and time-series forecasting. By the end, you'll have a fully interactive dashboard that makes complex insights feel like a friendly chat.

**Why This Matters**: In the fast-paced world of e-commerce, data isn't just numbers—it's the secret sauce for retention, revenue, and growth. This project equips you to answer burning questions like: Who's churning and why? What's driving sales? And how can we forecast the future?

**Tools You'll Master**: MySQL Workbench for SQL queries, Google Colab for Python scripting, scikit-learn for modeling, and Power BI for visualizations. No fluff—just practical, advanced techniques.

## Key Features
- **End-to-End Workflow**: From raw data to executive-ready dashboards—seamless integration across phases.
- **Advanced Techniques**: RFM segmentation, hyperparameter tuning, clustering, and time-series forecasting.
- **Real-World Relevance**: Based on actual e-commerce datasets, with a focus on churn prediction and demand insights.
- **Interactive Outputs**: Power BI dashboards with DAX measures and narrative storytelling.
- **Scalable and Reproducible**: Code and queries designed for easy replication in your own projects.
- **Business Impact**: Directly ties technical outputs to actionable strategies, like targeted marketing or inventory planning.

Frankly speaking, this isn't your average tutorial—it's a blueprint for data-driven retail transformation.

## Phases Breakdown
Here's the nitty-gritty: four phases that build on each other, turning data into decisions. Each phase includes step-by-step guidance, tools, and key objectives.

<details>
<summary> Phase 1 – Data Cleaning and Validation</summary>
Ah, the foundation—where we roll up our sleeves and tidy up RetailSmart's datasets. Think of this as spring cleaning for your data closet.

- **Objectives**: Explore, clean, and validate customers, sales, products, marketing, and reviews datasets. Handle missing values, outliers, and inconsistencies to ensure data integrity.
- **Key Activities**:
  - Use SQL (via MySQL Workbench) for extraction: Query top customers, revenue by category, churn rates, and conversion by channel.
  - Switch to Python (in Google Colab) for advanced cleaning: Impute nulls (e.g., median for numericals, 'unknown' for categoricals), cap outliers with IQR, standardize text (title-case cities, lowercase channels), convert timestamps to datetime, and validate referential integrity (e.g., matching customer/product IDs).
  - Conduct EDA: Univariate (distributions of order values, spend, churn), bivariate (category vs. revenue, payment type vs. spend), time-series (monthly orders/revenue), and RFM analysis (Recency, Frequency, Monetary with boxplots and scatter plots).
- **Tools**: MySQL Workbench for SQL, Google Colab for Python (pandas, numpy, matplotlib, seaborn).
- **Insights Gained**: Customer base demographics, sales drivers, data anomalies, trends, and churn patterns (e.g., churned customers show higher recency and lower frequency).
- **Time Estimate**: 4-6 hours—start here to build confidence!
</details>

<details>
<summary>Phase 2 – Predictive Modeling</summary>
Now that the data's sparkling, let's predict the future. This phase integrates cleaned datasets into a modeling-ready format and trains churn prediction models.

- **Objectives**: Engineer features, train models, and evaluate performance to identify churn drivers.
- **Key Activities**:
  - Merge datasets into a unified input (e.g., join customers with sales/marketing for RFM features).
  - Feature engineering: Derive Recency (days since last order), Frequency (total orders), Monetary (total spend), plus encoded categoricals (e.g., one-hot for channels).
  - Train models: Baseline (Logistic Regression), advanced (Random Forest, Gradient Boosting). Use train-test splits, handle class imbalance, and tune hyperparameters (e.g., GridSearchCV).
  - Evaluate: Metrics like Accuracy, Precision, Recall, F1-Score, and ROC-AUC. Interpret feature importance (e.g., recency as top churn predictor).
- **Tools**: Google Colab with scikit-learn, pandas.
- **Insights Gained**: Churn prediction accuracy (aim for 80%+), key predictors (e.g., low frequency flags at-risk customers), and model interpretability.
- **Time Estimate**: 6-8 hours—dive into ML magic!
</details>

<details>
<summary> Phase 3 – Advanced Analytics </summary>
Level up with unsupervised learning and forecasting. This is where patterns emerge from the noise.

- **Objectives**: Segment customers and forecast demand for strategic planning.
- **Key Activities**:
  - Customer Segmentation: Use clustering (e.g., K-Means on RFM) to identify groups like "High-Value Loyalists" or "At-Risk." Analyze profiles and assign clusters.
  - Demand Forecasting: Apply time-series models (e.g., ARIMA or Prophet) on sales data to predict monthly revenue/orders. Analyze seasonality and trends.
- **Tools**: Google Colab with scikit-learn (for clustering), statsmodels or fbprophet (for forecasting).
- **Insights Gained**: Cluster behaviors (e.g., loyalists spend 3x more), forecast accuracy, and seasonal peaks (e.g., Q4 boosts).
- **Time Estimate**: 5-7 hours—uncover the "why" behind the data!
</details>

<details>
<summary>> Phase 4 – Visualization and Storytelling</summary>
The grand finale: Transform insights into a visual feast that even non-techies can love.

- **Objectives**: Build an interactive dashboard to communicate findings.
- **Key Activities**:
  - Integrate Phase 1-3 outputs into Power BI (import CSVs, connect data models).
  - Create DAX measures for KPIs (e.g., churn rate, revenue growth).
  - Design dashboards: Executive Summary (high-level KPIs), Customer Insights (RFM/clusters), Churn Prediction (model outputs), Forecasting Trends (time-series visuals).
  - Embed storytelling: Use narratives, tooltips, and slicers for actionable insights (e.g., "Target at-risk clusters with email campaigns").
- **Tools**: Power BI Desktop.
- **Insights Gained**: A narrative-driven report that bridges data and decisions (e.g., "Invest in loyalty programs to reduce churn by 15%").
- **Time Estimate**: 4-6 hours—make your work shine!
</details>

## Prerequisites and Setup
Before we jump in, ensure you're geared up:
- **Skills**: Basic Python (pandas, matplotlib), SQL knowledge, and familiarity with ML/visualization tools.
- **Hardware/Software**: A computer with internet (for Colab/Power BI), MySQL Workbench installed, and a free Power BI account.
- **Data Access**: You'll need the five original CSVs (customers.csv, etc.)—assume they're in your project folder.
- **Environment**: Use Google Colab for Python phases (no local setup needed), MySQL for SQL, and Power BI for viz.

Friendly tip: If you're new, start with Phase 1—it's forgiving and builds momentum.

<details>
<summary> Installation Guide</summary>
Let's set the stage—step by step, no sweat.

1. **MySQL Workbench**: Download from mysql.com, install, and set up a local server. Create a database named "retailsmart."
2. **Google Colab**: Head to colab.research.google.com—it's browser-based, so no install needed. Upload your CSVs.
3. **Power BI**: Download Power BI Desktop from powerbi.microsoft.com. Sign in with a Microsoft account.
4. **Python Libraries**: In Colab, run `!pip install pandas numpy matplotlib seaborn scikit-learn statsmodels fbprophet` in a cell.
5. **Project Folder**: Create a directory (e.g., "RetailSmart_Capstone") and organize files by phase (e.g., /Phase1/cleaned_data/).

That's it—ready to roll!
</details>

## Usage Instructions
Here's how to navigate this project like a pro:

1. **Phase 1**: In MySQL Workbench, create tables and run extraction queries. Export results, then switch to Colab for cleaning/EDA scripts. Save cleaned CSVs.
2. **Phase 2**: In Colab, load cleaned data, engineer features, train models, and export pickles (e.g., model.pkl).
3. **Phase 3**: Use Colab for clustering/forecasting—generate summaries and forecasts.
4. **Phase 4**: Open Power BI, import all outputs, build measures/visuals, and publish the dashboard.
5. **Run Order**: Phases must be sequential—Phase 1 outputs feed Phase 2, and so on.
6. **Troubleshooting**: If queries fail, check data types. For Colab, ensure CSVs are uploaded. Power BI? Refresh data connections.

Pro tip: Document your steps in a notebook—it's great for portfolios!

## Output Files and Deliverables
Each phase spits out tangible goodies. Here's the full list:

- **Phase 1**: customers_cleaned.csv, sales_cleaned.csv, marketing_cleaned.csv, products_cleaned.csv (imputed, standardized datasets).
- **Phase 2**: model_input.csv (unified dataset), final_rf_model.pkl (trained model), scaler.pkl (for feature scaling).
- **Phase 3**: cluster_summary.csv (cluster profiles), customers_with_clusters.csv (segmented data), forecast_results.csv (predictions).
- **Phase 4**: RetailSmart_Dashboard.pbix (interactive Power BI file), RetailSmart_Storytelling_Report.docx (narrative report with insights).

Store these in your project folder— they're your proof of progress!

## Contributing
Got ideas to make this even better? We'd love that! Fork the repo, tweak the code, and submit a pull request. Let's keep it collaborative—share your enhancements, like adding more models or viz tweaks.

## License
This project is open-source under the MIT License—use it freely, but give credit where it's due.

## Acknowledgments
A big shoutout to the RetailSmart team for the datasets, and to the open-source community for tools like pandas and Power BI. Special thanks to data science pioneers who make projects like this possible.

There you have it—a capstone that's not just informative, but inspiring. Ready to transform data into decisions? Dive in, and let's make RetailSmart thrive! If you hit snags, reach out—happy analyzing!

---

<p align="center">
  <em>Built with ❤️ by Kanak Baghel | <a href="https://www.linkedin.com/in/kanakbaghel">LinkedIn</a></em>
</p>