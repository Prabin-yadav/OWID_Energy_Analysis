# OWID Energy Tableau Analysis

## Global Energy Transition and South Asian Energy Resilience

A case-study based data analytics and visualization project that uses the **Our World in Data (OWID) Energy dataset** and **Tableau** to investigate global energy consumption, electricity generation, renewable adoption, carbon intensity, fossil-fuel dependence, energy independence, and South Asian peer performance, with a particular analytical focus on Nepal.

This project is designed for a **Tableau-based CA3 academic submission** and combines a reproducible Python data-cleaning pipeline with an interactive Tableau workbook.

---

## 1. Project Overview

Energy systems are changing rapidly because of population growth, economic development, electrification, renewable-energy adoption, energy-security concerns, and decarbonization targets. These changes do not occur uniformly across countries.

Some countries have:

- high energy consumption but lower carbon intensity because of cleaner electricity mixes,
- rapidly increasing renewable electricity,
- strong domestic energy production,
- heavy fossil-fuel dependence,
- high energy imports,
- or large differences between total energy consumption and per-capita energy use.

This project converts a large OWID energy dataset into a controlled analytical dataset and uses Tableau to make these relationships easier to explore interactively.

The analysis emphasizes both:

1. **Global energy patterns**, and
2. **South Asian benchmarking, especially Nepal**.

---

## 2. Problem Statement

The global energy system is undergoing a transition as countries attempt to balance growing energy demand, economic development, energy security, and the reduction of environmental impacts. However, energy consumption, renewable-energy adoption, fossil-fuel dependence, electricity carbon intensity, and energy-import dependence vary substantially across countries.

South Asian countries also differ significantly in energy consumption, electricity generation, renewable adoption, and energy dependence. Direct comparison is difficult when the underlying information is spread across many indicators and years.

Therefore, an interactive analytical system is required to:

- examine long-term energy trends,
- compare countries using both absolute and normalized indicators,
- evaluate renewable and fossil-fuel dependence,
- study electricity carbon intensity,
- benchmark Nepal against relevant peers,
- and explore potential electricity-demand scenarios.

This project addresses the problem by transforming OWID energy data into a validated Tableau-ready analytical dataset and presenting the results through interactive Tableau dashboards.

---

## 3. Main Goal

### Primary Goal

Build an interactive Tableau decision-support dashboard that explains how energy consumption, electricity generation, renewable adoption, carbon intensity, energy dependence, and economic development vary across countries and over time.

### Specific Focus

The Tableau workbook is especially designed to support:

- global comparisons,
- Nepal-focused analysis,
- South Asia comparisons,
- peer-group benchmarking,
- renewable-energy analysis,
- carbon-intensity analysis,
- energy-independence analysis,
- and scenario-based electricity-demand exploration.

---

## 4. Objectives

### Objective 1
Analyze global energy consumption and electricity-generation trends from **2000 to 2025**.

### Objective 2
Compare countries using:

- primary energy consumption,
- energy consumption per capita,
- electricity generation,
- and energy use relative to GDP.

### Objective 3
Analyze differences in **electricity carbon intensity** across countries.

### Objective 4
Evaluate renewable-energy growth and the contribution of:

- hydropower,
- solar,
- wind,
- and other renewable sources.

### Objective 5
Study fossil-fuel dependence and electricity/energy import dependence.

### Objective 6
Benchmark South Asian countries and compare Nepal with selected peer groups.

### Objective 7
Investigate relationships among:

- economic development,
- population,
- energy use,
- electricity generation,
- and environmental impact.

### Objective 8
Explore potential future electricity-demand scenarios using user-controlled Tableau parameters.

### Objective 9
Develop an interactive Tableau decision-support environment using filters, calculated fields, parameters, comparisons, and dashboard/story navigation.

---

# 5. Why This Analysis Is Important

Energy data is important not only for describing current conditions but also for understanding future development and sustainability challenges.

## 5.1 Energy security

Countries depend on different combinations of domestic production, fossil fuels, renewable resources, and imports.

Energy-independence and import-dependence indicators can help identify vulnerability to external supply shocks.

## 5.2 Economic development

Energy demand generally changes with:

- industrialization,
- economic output,
- infrastructure development,
- urbanization,
- population,
- transport,
- and household electrification.

Comparing energy use with GDP and population provides more context than total consumption alone.

## 5.3 Environmental sustainability

Electricity systems can have very different carbon footprints.

A country producing a large amount of electricity is not automatically a high-carbon electricity system, because the source mix matters.

## 5.4 Renewable-energy transition

Hydropower, solar, wind, and other renewables are important indicators of the transition away from fossil-fuel-heavy electricity systems.

Tracking renewable share over time helps identify the direction and speed of transition.

## 5.5 South Asian policy comparison

South Asian countries face related but different:

- population pressures,
- development needs,
- energy-access challenges,
- generation requirements,
- and energy-import conditions.

Peer benchmarking helps reveal where Nepal is similar to or different from neighboring countries.

## 5.6 Decision support

The Tableau dashboard turns a high-dimensional dataset into interactive evidence that can support exploratory decisions about:

- energy strategy,
- renewable adoption,
- demand growth,
- peer performance,
- and energy resilience.

---

# 6. Dataset

## 6.1 Source

**Our World in Data – Energy Data**

Official source:

- https://github.com/owid/energy-data
- https://ourworldindata.org/energy

OWID means **Our World in Data**.

The project uses the downloaded OWID Energy CSV as its raw source.

## 6.2 Raw dataset

The original project input is:

```text
data/1_original-owid-energy-data.csv
```

Expected characteristics of the supplied raw file:

- **23,232 rows**
- **130 columns**
- years approximately **1900–2025**
- **314 entities**

This file is the **single raw input** to the final cleaning script.

## 6.3 Important data principle

The project does **not** use the old filtered CSV as a cleaning input.

The pipeline intentionally follows:

```text
Raw OWID CSV
    ↓
Python cleaning and validation
    ↓
Processed Tableau-ready CSV
    ↓
Tableau workbook
```

The following files are not used as pipeline inputs:

- `2_filtered-owid-energy-data.csv`
- Tableau-exported CSV files
- previously processed datasets
- workbook-generated extracts as a preprocessing source
- intermediate CSVs

---

# 7. Data Reduction: Why 23,232 Rows Became 4,866

The reduction is intentional and is **not simply deleting rows to make Tableau work**.

## Stage 1 — Original data

```text
23,232 rows × 130 columns
```

The raw OWID data contains a long historical period and many entities that are not needed for the selected analytical scope.

## Stage 2 — Analysis period

The Tableau case study focuses on:

```text
2000–2025
```

After filtering the raw dataset to this period:

```text
7,491 rows
```

## Stage 3 — Analytical entity scope

The project then applies a documented country/entity scope appropriate for country-level comparison.

This removes selected non-sovereign/territorial entities and retains the project's intended analytical population.

Result:

```text
4,866 rows
197 analytical entities
```

## Stage 4 — Key validation

The final dataset has:

```text
4,866 rows × 130 columns
```

with:

- one analytical record per Country-Year,
- no duplicate Country-Year key,
- validated numeric types,
- validated ranges,
- deterministic repair of selected derived values,
- and preserved column names required by the Tableau workbook.

### Important interpretation

The 20,000+ row reduction is mainly caused by:

1. removing historical years before 2000, and
2. restricting the analysis to the selected entity scope.

It is **not** a claim that 20,000 observations were "bad data."

---

# 8. Final Data-Cleaning Methodology

The script used for the final pipeline is:

```text
owid_energy_final_cleaning.py
```

The script is designed to be reproducible and explicitly checks that the required raw input exists.

## Step 1 — Load only the raw source

The script reads:

```text
C:\Users\yadav\Desktop\SEM 7\DS\OWID_ENERGY\data\1_original-owid-energy-data.csv
```

If this file is missing, the script stops instead of silently selecting another CSV.

## Step 2 — Text normalization

Text fields are cleaned by:

- removing BOM characters,
- trimming leading/trailing whitespace,
- collapsing repeated spaces,
- standardizing Country and ISO code text.

## Step 3 — Numeric validation

Numeric columns are converted safely.

Invalid or non-finite numeric tokens are converted to blank/NULL rather than creating invalid numbers.

Examples of invalid tokens handled include:

```text
NA
N/A
NaN
null
none
empty strings
non-numeric values
non-finite values
```

## Step 4 — Year validation

The year field is converted to integer form and rows without valid integer years are excluded from the analytical dataset.

## Step 5 — Year filtering

The case study uses:

```text
2000–2025 inclusive
```

## Step 6 — Entity filtering

The pipeline keeps the intended analytical country/entity scope and excludes the documented territory set.

Kosovo is explicitly retained as the workbook's ISO-less exception.

## Step 7 — Country-Year uniqueness

The workbook assumes a country-year analytical grain.

The pipeline validates:

```text
Country + Year
```

as a unique key.

Duplicate analytical records cause validation to fail rather than being silently aggregated.

## Step 8 — ISO-code repair

A missing ISO code is filled only when exactly one unambiguous ISO code exists for the same country in the original OWID history.

No arbitrary ISO codes are invented.

## Step 9 — Deterministic derived-value repair

Some OWID fields can be derived exactly from other fields.

The pipeline fills only those values that can be mathematically reconstructed.

Examples:

### Per-capita

```text
per-capita value =
base metric / population
```

### Share of electricity

```text
share =
source electricity / total electricity generation × 100
```

### Share of primary energy

```text
share =
source energy / primary energy consumption × 100
```

### Energy per GDP

```text
energy per GDP =
primary energy consumption / GDP
```

### Year-over-year TWh change

```text
current year value - previous year value
```

### Year-over-year percentage change

```text
(current - previous) / previous × 100
```

The 2000 change calculations are allowed to use the **1999 raw observation history** when the source contains the required values.

## Step 10 — No statistical imputation

The project does **not** perform statistical interpolation or synthetic prediction to fill historical missing data.

There is no:

- blanket zero-filling,
- random replacement,
- mean imputation,
- median imputation,
- or fabricated energy measurement.

## Step 11 — Negative-value validation

Negative values are treated according to their meaning.

Legitimate negative values are retained for fields such as:

- year-over-year changes,
- net electricity imports.

Negative values in fields representing physical quantities are treated as invalid and blanked.

## Step 12 — Share validation

Share fields are validated against the logical range:

```text
0–100%
```

Values outside that range are treated as invalid and blanked.

## Step 13 — Sorting

Final records are sorted by:

```text
Country → Year
```

This improves readability and makes time-series inspection easier.

## Step 14 — Round-trip validation

After writing the processed CSV, the script reads it again and verifies:

- header equality,
- row-count equality,
- Country-Year uniqueness.

---

# 9. Data Quality Results

The current processed dataset was validated with the following results:

| Metric | Result |
|---|---:|
| Raw rows | 23,232 |
| Raw columns | 130 |
| Analysis start | 2000 |
| Analysis end | 2025 |
| Rows after year filter | 7,491 |
| Final rows | 4,866 |
| Final columns | 130 |
| Analytical entities | 197 |
| Duplicate Country-Year records | 0 |
| Deterministic repairs | 3,804 |
| Invalid share values detected/blanked | 1,219 |
| Statistical interpolation | No |
| Blanket zero fill | No |

The audit files generated by the pipeline document these checks.

---

# 10. Missing Values: Why NULL Does Not Automatically Mean an Error

A major data-quality principle in this project is:

> **Missing does not automatically mean zero.**

For example:

```text
coal_consumption = NULL
```

does not necessarily mean:

```text
coal_consumption = 0
```

It may mean that the source did not report the value for that country-year.

Similarly, a year-over-year change can be unavailable because a valid prior-year observation does not exist.

Therefore, the project:

- preserves genuine source missingness,
- fills only deterministic values,
- avoids fabricated zeros,
- and documents missingness.

This is important for academic integrity.

### Practical Tableau implication

A Tableau chart may therefore show:

- gaps,
- NULL marks,
- missing points,
- or reduced coverage

for indicators that are not available in the source.

These observations should be interpreted as **data availability limitations**, not automatically as zero energy production/consumption.

---

# 11. Final Tableau Dataset

The final processed CSV is:

```text
data/processed/1.owid-energy-data.csv
```

Expected structure:

```text
4,866 rows × 130 columns
```

The project preserves the full 130-column source schema because the existing Tableau workbook contains calculations and worksheets that depend on the original OWID field names.

The workbook therefore receives:

```text
cleaned values
+
validated rows
+
original field structure
```

rather than a completely new reduced schema that could break dashboard calculations.

---

# 12. Analytical Variable Groups

The 130 fields can be understood through these major groups.

## Identification

- `country`
- `year`
- `iso_code`

## Demographic / economic context

- `population`
- `gdp`

## Primary energy

- `primary_energy_consumption`
- `energy_per_capita`
- `energy_per_gdp`
- `energy_cons_change_twh`
- `energy_cons_change_pct`

## Electricity

- `electricity_demand`
- `electricity_generation`
- `electricity_demand_per_capita`
- `per_capita_electricity`
- `electricity_share_energy`

## Carbon

- `carbon_intensity_elec`
- `greenhouse_gas_emissions`

## Fossil fuels

- coal
- oil
- gas
- total fossil-fuel consumption
- fossil electricity
- fossil shares
- fossil per-capita measures
- fossil production
- change metrics

## Renewable energy

- renewables consumption
- renewables electricity
- renewables shares
- renewables per-capita values
- change metrics

## Hydropower

- hydro consumption
- hydro electricity
- hydro shares
- hydro per-capita metrics
- hydro change metrics

## Solar

- solar consumption
- solar electricity
- solar shares
- solar per-capita metrics
- solar change metrics

## Wind

- wind consumption
- wind electricity
- wind shares
- wind per-capita metrics
- wind change metrics

## Nuclear

- nuclear consumption
- nuclear electricity
- nuclear shares
- nuclear per-capita metrics
- nuclear change metrics

## Biofuel and other renewables

Equivalent consumption, electricity, share, per-capita, and change metrics are included where provided by OWID.

## Imports

- `net_elec_imports`
- `net_elec_imports_share_demand`

These are especially useful for energy-independence analysis.

---

# 13. Tableau Workbook

The final workbook is:

```text
OWID_Energy_Tableau.twbx
```

The workbook is a **packaged Tableau workbook** and contains its required CSV inside the package.

The workbook's packaged data is stored under:

```text
Data/1.owid-energy-data.csv
```

The datasource uses a text-file CSV relation compatible with the workbook.

The old creator-specific local Mac path was removed from the repaired workbook.

---

# 14. Tableau Workbook Structure

The workbook contains:

- **55 worksheets**
- **3 main dashboards**
- **1 story**
- **3 story points**

The main workbook objects are:

```text
Dashboard 1
Dashboard 2
Dashboard 3
Story 1

Story points:
Dash 1
Dash 2
Dash 3
```

The workbook includes several groups of worksheets for:

- KPIs,
- trends,
- comparisons,
- distributions,
- geographical analysis,
- composition,
- relationships,
- and tables.

---

# 15. Dashboard 1 — Energy / Economic Overview

The first dashboard focuses on the relationship between energy consumption and economic context.

Typical analytical elements include:

- key performance indicators,
- geographic views,
- time trends,
- composition views,
- relationship/scatter-style comparisons,
- projected-demand analysis.

Important concepts represented include:

- total energy consumption,
- energy intensity,
- GDP per capita,
- population,
- electricity output,
- renewable penetration,
- economic efficiency,
- growth trajectory,
- projected demand.

### Questions answered

- How has energy demand changed?
- How much energy does a country use relative to its population?
- How does energy use relate to economic output?
- Is energy growth faster or slower than population growth?
- What could future demand look like under a different growth assumption?

---

# 16. Dashboard 2 — Carbon Intensity and Energy Independence

The second dashboard focuses on environmental impact and energy-system dependence.

Key concepts include:

- electricity carbon intensity,
- fossil electricity,
- renewable electricity,
- fossil share,
- net electricity imports,
- energy independence,
- renewable penetration,
- grid greenness.

### Questions answered

- Which countries have high or low electricity carbon intensity?
- How dependent is a country on fossil fuels?
- How important are renewable sources?
- How does electricity import dependence vary?
- How does the electricity mix affect carbon intensity?

---

# 17. Dashboard 3 — South Asia / Peer Benchmarking

The third dashboard provides the strongest regional benchmarking component.

It is designed around Nepal and peer-group comparison.

Possible peer views include:

- Nepal,
- Economic Peers,
- GDP Peers,
- Population Peers,
- Land-Size Peers,
- SAARC,
- ASEAN,
- BRICS,
- G7,
- EU,
- OECD,
- OPEC,
- regional groupings,
- and landlocked-country comparisons.

### Questions answered

- How does Nepal compare with South Asia?
- How does Nepal compare with countries of similar population?
- How does Nepal compare with GDP peers?
- How does Nepal's energy mix differ from peers?
- How does Nepal perform in carbon intensity and renewable electricity?
- How does Nepal's energy trajectory compare with benchmark countries?

---

# 18. Interactive Parameters

The Tableau workbook includes user-controlled parameters such as:

### Target Goal (MW)

Allows the user to work with a target electricity-generation goal.

### Choose View

Switches among electricity-source views such as:

- Hydro Electricity
- Solar Electricity
- Wind Electricity
- Renewable Electricity
- Fossil Electricity
- Coal Electricity

### Projected Demand Growth %

Controls the scenario growth assumption.

The configured parameter range is:

```text
-50% to +100%
```

with a defined step size.

### Analysis Mode

Supports:

- Nepal Only
- Compare with Peers

### Select View

Supports different peer/benchmark groups.

### Population Buffer %

Used for population-peer benchmarking.

### GDP Buffer %

Used for GDP-peer benchmarking.

---

# 19. Tableau Calculated Fields

The workbook contains numerous calculated fields used to turn raw measures into decision-support indicators.

Representative calculated fields include:

- Growth Trajectory
- Demand Gap (Current vs Projected)
- Renewable Share of Generation
- Non-Hydro Renewable Share
- Energy Independence Score
- Regional Electricity Output
- Renewable Penetration
- Projected Population
- Dynamic Grouping
- Solar + Wind Share
- Total Fossil Dependency
- Dynamic Metric Switcher
- Heatmap Visibility
- Waterfall Sizing
- Selected Group
- Grid Greenness
- Economic Efficiency
- Net Energy Independence
- Carbon Footprint
- Energy Intensity
- Electricity Access Gap
- Year-over-Year Growth %
- Energy Surplus/Deficit
- Scenario Demand
- Hydro Production
- Solar Production
- Fossil Production
- Renewable Production
- Carbon Intensity Bucket
- GDP per Capita
- Nepal Focus
- Peer Group Filter
- Metric for Ranking
- Peer Rank
- GDP Growth %
- Fossil Share Change
- Total Energy Consumption
- Economic-Efficiency
- Growth Trajectory (Energy vs Population)
- Average Carbon Intensity
- Solar & Wind Maturity

These calculated fields are important because they move the project beyond basic charts and demonstrate **analytical modeling inside Tableau**.

---

# 20. Analytical Techniques Used

The project demonstrates several data-analytics and visualization techniques.

## Descriptive analysis

- totals,
- averages,
- medians,
- percentages,
- shares,
- year-over-year changes.

## Trend analysis

- time-series analysis,
- historical growth,
- changes in energy demand,
- renewable adoption over time.

## Comparative analysis

- country vs country,
- country vs peer group,
- Nepal vs South Asia,
- regional benchmarking.

## Ratio analysis

Examples:

```text
Energy per Capita
Energy per GDP
Renewable Share
Fossil Share
Import Share
Carbon Intensity
```

## Relationship analysis

Relationships between:

- GDP and energy,
- population and energy,
- development and carbon intensity,
- renewable penetration and electricity mix.

## Scenario analysis

A Tableau parameter controls future demand growth assumptions and dynamically changes projected demand indicators.

---

# 21. Key Analytical Indicators

The project is strongest when absolute metrics and normalized metrics are considered together.

Important indicators include:

| Indicator | Purpose |
|---|---|
| Primary Energy Consumption | Measures total primary energy use |
| Energy per Capita | Normalizes energy use by population |
| Energy per GDP | Shows energy intensity relative to economic output |
| Electricity Generation | Measures electricity output |
| Electricity Demand | Measures electricity requirement |
| Carbon Intensity | Indicates emissions intensity of electricity |
| Renewable Electricity | Measures renewable electricity output |
| Renewable Share | Measures renewable contribution |
| Fossil Electricity | Measures fossil-based generation |
| Fossil Share | Shows fossil dependence |
| Net Electricity Imports | Indicates import/export position |
| Import Share | Normalizes imports against demand |
| Hydro Electricity | Measures hydropower contribution |
| Solar Electricity | Measures solar contribution |
| Wind Electricity | Measures wind contribution |
| GDP per Capita | Economic-development context |
| Population | Demographic context |

---

# 22. Example Insights from the Processed Data

The following examples are derived from the processed project dataset and should be used as **illustrative analytical findings**, not as universal causal claims.

## Nepal energy growth

In the processed dataset, Nepal's primary energy consumption rises from approximately:

```text
11.497 TWh in 2000
```

to:

```text
57.468 TWh in 2023
```

This is approximately a **400% increase**.

## Nepal energy per capita

Nepal's energy consumption per capita increases from approximately:

```text
468 kWh/person in 2000
```

to:

```text
1,935 kWh/person in 2023
```

This demonstrates substantial growth in per-capita energy use over the available period.

## Nepal electricity generation

The processed data shows electricity generation rising strongly from approximately:

```text
1.65 TWh in 2000
```

to:

```text
10.7 TWh in 2022
```

The available source coverage is uneven by year, so year-specific comparisons must always consider data availability.

## Nepal electricity carbon intensity

Nepal's electricity carbon intensity falls from approximately:

```text
36.36 gCO2e/kWh in 2000
```

to:

```text
23.36 gCO2e/kWh in 2022
```

This is consistent with a substantially cleaner electricity mix in the available observations.

## Nepal renewable electricity

Hydropower dominates Nepal's renewable electricity profile in the processed data, while solar and wind remain much smaller contributors during much of the historical period.

This makes Nepal particularly useful for studying a **hydropower-heavy renewable transition**.

---

# 23. Important Data-Coverage Limitation

The analysis window is defined as:

```text
2000–2025
```

but not every entity has complete observations for every year.

For example, some entities in the processed dataset have observations through:

- 2023,
- 2024,
- or 2025.

Therefore:

> **The presence of the 2025 analysis boundary does not mean that every country has a 2025 observation.**

This matters when interpreting:

- latest-year rankings,
- global totals,
- trend endpoints,
- averages,
- peer comparisons.

A good analysis should always verify the actual year coverage of the selected countries/metrics.

---

# 24. Visualization Principles

The Tableau workbook should be interpreted according to common data-visualization principles.

## Appropriate chart selection

Examples:

- **Line charts** → time trends
- **Maps** → geographic comparisons
- **Bar charts** → country ranking
- **Scatter plots** → relationships
- **Stacked/composition charts** → energy mix
- **Heatmaps** → country-year intensity/comparison
- **KPI cards** → headline indicators
- **Waterfall/scenario views** → change and projected gap

## Context matters

Absolute energy consumption should not be interpreted alone.

A large country may have high energy consumption simply because it has a large population.

Therefore, absolute metrics should often be viewed together with:

- per-capita measures,
- GDP-normalized measures,
- shares,
- and carbon intensity.

## Avoiding misleading interpretation

The dashboard should not be used to claim causality merely because two variables are correlated.

For example:

> High GDP and high energy consumption do not automatically prove that GDP causes energy consumption.

The dashboard is primarily an **exploratory and decision-support system**.

---

# 25. Privacy, Security and Ethics

## Privacy

The dataset is aggregated primarily at a country-year level and does not represent individual patient/customer records.

Therefore, personal-privacy risk is low relative to person-level datasets.

## Data integrity

The project should preserve:

- source provenance,
- processing scripts,
- audit reports,
- reproducible transformations.

## Transparency

Every important transformation should be explainable:

- why years were filtered,
- why entities were excluded,
- how derived values were calculated,
- and how missing values were handled.

## Ethical visualization

Do not:

- fabricate missing values,
- treat NULL as zero without justification,
- exaggerate differences through misleading axes,
- imply causation from correlation,
- or hide important data-coverage limitations.

## Scenario ethics

Scenario projections are **what-if analyses**, not forecasts with certainty.

A projected-demand value should be interpreted according to the selected assumptions.

---

# 26. Tableau Creator vs Viewer

## Tableau Creator

Creator-level capability is required when team members need to:

- connect to datasets,
- prepare/modify data,
- create worksheets,
- build dashboards,
- create calculated fields,
- use parameters,
- publish workbooks,
- and maintain the analytics pipeline.

## Tableau Viewer

Viewer-level access is appropriate for people who only need to:

- open published dashboards,
- interact with filters,
- inspect visualizations,
- and consume the results.

### Relevance to this project

For project development:

```text
Student / Analyst → Creator capabilities
```

For dashboard consumption:

```text
Teacher / Reviewer / Manager → Viewer-style consumption
```

This distinction demonstrates an understanding of Tableau's role-based workflow.

---

# 27. Project Folder Structure

Recommended final structure:

```text
OWID_ENERGY/
│
├── README.md
│
├── owid_energy_final_cleaning.py
│
├── data/
│   │
│   ├── 1_original-owid-energy-data.csv
│   │
│   ├── processed/
│   │   └── 1.owid-energy-data.csv
│   │
│   └── eda/
│       ├── OWID_Energy_Cleaning_Audit.csv
│       ├── OWID_Energy_Missing_Values.csv
│       ├── OWID_Energy_Entity_Coverage.csv
│       └── OWID_Energy_Pipeline_Summary.json
│
└── Tableau/
    └── OWID_Energy_Tableau.twbx
```

### Recommended cleanup

Older experimental versions of scripts/workbooks can be moved into a separate archive folder, for example:

```text
archive/
```

This keeps the final submission clean and makes it obvious which pipeline and workbook are authoritative.

---

# 28. Important Project Files

| File | Purpose |
|---|---|
| `1_original-owid-energy-data.csv` | Original raw OWID input |
| `processed/1.owid-energy-data.csv` | Final Tableau-ready data |
| `owid_energy_final_cleaning.py` | Reproducible cleaning pipeline |
| `OWID_Energy_Cleaning_Audit.csv` | Cleaning/validation audit |
| `OWID_Energy_Missing_Values.csv` | Missing-data analysis |
| `OWID_Energy_Entity_Coverage.csv` | Country/year coverage report |
| `OWID_Energy_Pipeline_Summary.json` | Machine-readable pipeline summary |
| `OWID_Energy_Tableau.twbx` | Interactive Tableau workbook |
| `README.md` | Project documentation |

---

# 29. How to Run the Python Pipeline

## Requirements

Python 3.10+ is recommended.

The final pipeline intentionally uses a lightweight standard-library-based implementation and does not require a large data-science environment.

## Step 1 — Verify the raw file

Make sure this exact file exists:

```text
C:\Users\yadav\Desktop\SEM 7\DS\OWID_ENERGY\data\1_original-owid-energy-data.csv
```

## Step 2 — Open PowerShell

```powershell
cd "C:\Users\yadav\Desktop\SEM 7\DS\OWID_ENERGY"
```

## Step 3 — Run the pipeline

```powershell
python owid_energy_final_cleaning.py
```

or, on systems where `py` is preferred:

```powershell
py owid_energy_final_cleaning.py
```

## Step 4 — Read the console output

The script prints each processing stage, including:

- input rows,
- validation,
- year filtering,
- entity filtering,
- duplicate validation,
- deterministic repairs,
- range validation,
- final schema,
- final row count,
- and round-trip validation.

## Step 5 — Check the output

The main Tableau-ready dataset should be created at:

```text
C:\Users\yadav\Desktop\SEM 7\DS\OWID_ENERGY\data\processed\1.owid-energy-data.csv
```

EDA/audit files are written under:

```text
C:\Users\yadav\Desktop\SEM 7\DS\OWID_ENERGY\data\eda\
```

---

# 30. How to Use the Tableau Workbook

Open:

```text
OWID_Energy_Tableau.twbx
```

The packaged workbook contains the CSV required by the workbook.

Main navigation:

```text
Story 1
   ├── Dash 1
   ├── Dash 2
   └── Dash 3
```

Use the dashboard controls to explore:

- countries,
- years,
- energy-source selections,
- analysis mode,
- peer groups,
- population/GDP buffers,
- and demand-growth scenarios.

---

# 31. Recommended Presentation Flow

For the CA3 presentation, a strong flow is:

### Slide 1 — Title

**Global Energy Transition and South Asian Energy Resilience**

### Slide 2 — Problem

Explain why global energy comparisons are difficult.

### Slide 3 — Dataset

Present:

- OWID Energy Data,
- raw dimensions,
- time coverage,
- country/entity scope.

### Slide 4 — Data Cleaning

Show:

```text
23,232 raw rows
→ 7,491 rows (2000–2025)
→ 4,866 analytical rows
```

### Slide 5 — Dashboard 1

Explain energy and economic analysis.

### Slide 6 — Dashboard 2

Explain carbon intensity and energy independence.

### Slide 7 — Dashboard 3

Explain Nepal/South Asia benchmarking.

### Slide 8 — Key Insights

Highlight:

- Nepal energy growth,
- renewable composition,
- carbon intensity,
- peer comparisons.

### Slide 9 — Interactivity

Show Tableau:

- parameters,
- filters,
- peer groups,
- scenario analysis.

### Slide 10 — Ethics & Data Quality

Explain:

- missing values,
- source limitations,
- no fabricated zero-filling,
- responsible interpretation.

### Slide 11 — Creator vs Viewer

Explain Tableau roles.

### Slide 12 — Conclusion

Summarize what the dashboard reveals.

---

# 32. CA3 Requirement Mapping

| CA3 Requirement | Project Implementation |
|---|---|
| Real-world dataset | OWID Energy dataset |
| Problem statement | Global energy transition and South Asian resilience |
| Objectives | 9 defined analytical objectives |
| Data cleaning | Python reproducible pipeline |
| Visualization | Tableau |
| Interactive dashboard | Yes |
| Meaningful insights | Global + South Asia + Nepal analysis |
| Tableau license comparison | Creator vs Viewer |
| Privacy | Country-level aggregated data |
| Security | Reproducible source + controlled artifacts |
| Ethics | Transparent missing-data and interpretation policy |
| Presentation & Viva | Dashboard + methodology + insights |

---

# 33. Strengths of the Project

## Large real-world dataset

The raw source contains more than 23,000 records and 130 fields.

## Longitudinal analysis

The project supports multi-year comparison instead of analyzing a single snapshot.

## Global scope

Countries can be compared across regions and economic groups.

## Nepal-centered relevance

The dashboard gives a clear regional story around Nepal.

## Reproducible preprocessing

The data pipeline is scripted rather than manually edited.

## Transparent data cleaning

The process documents what was removed, repaired, and retained.

## Multi-dimensional analysis

The project combines:

- energy,
- electricity,
- economics,
- population,
- renewables,
- fossil fuels,
- imports,
- and carbon intensity.

## Interactive decision support

Tableau parameters allow users to change views and assumptions.

---

# 34. Limitations

## Incomplete latest-year coverage

Not every country has observations for all years through 2025.

## Source-level missingness

OWID contains genuine missing values for many indicators.

## No blanket imputation

The dataset is intentionally not filled with artificial values.

## Comparability

Energy indicators may be based on different source methodologies and definitions.

## Correlation is not causation

Relationships shown in the dashboard are exploratory.

## Scenario assumptions

Projected demand depends on user-selected assumptions and should not be treated as a guaranteed forecast.

## Scope limitation

The final Tableau dataset uses a defined analytical entity scope rather than the entire universe of entities in the raw OWID file.

---

# 35. Future Enhancements

Possible future extensions include:

- automated source-data versioning,
- automated download of the latest OWID release,
- stronger schema-change detection,
- additional renewable technologies,
- electricity-access indicators,
- country-level policy indicators,
- forecasting using time-series models,
- uncertainty bands for scenario analysis,
- automated Tableau publishing,
- and a web-based dashboard.

---

# 36. Reproducibility

The intended reproducible chain is:

```text
Official OWID source
        ↓
1_original-owid-energy-data.csv
        ↓
owid_energy_final_cleaning.py
        ↓
data/processed/1.owid-energy-data.csv
        ↓
OWID_Energy_Tableau.twbx
        ↓
Interactive dashboards + story
```

The most important reproducibility rule is:

> **Always start from the original raw OWID file.**

The final CSV is an output, not a preprocessing input.

---

# 37. Data Lineage

```text
SOURCE
  Our World in Data – Energy
             │
             ▼
RAW DATA
  23,232 × 130
             │
             ▼
VALIDATION
  text / numeric / year
             │
             ▼
TIME SCOPE
  2000–2025
             │
             ▼
ENTITY SCOPE
  analytical countries/entities
             │
             ▼
DATA QUALITY
  duplicate checks
  range checks
  derived-value repair
  missing-value audit
             │
             ▼
TABLEAU DATA
  4,866 × 130
             │
             ▼
TABLEAU WORKBOOK
  3 dashboards + 1 story
             │
             ▼
ANALYSIS
  Global + South Asia + Nepal
```

---

## Final Note

The **raw CSV is the source of truth**.

The Python pipeline is the source of truth for preprocessing.

The processed CSV is the source of truth for the Tableau data layer.

The Tableau workbook is the source of truth for the interactive visualization layer.

Keeping these layers separate makes the project easier to explain, reproduce, debug, and defend during the CA3 presentation and viva.
