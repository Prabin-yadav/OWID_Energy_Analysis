from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

# ============================================================================
# OWID ENERGY -> TABLEAU CA3 DATA PIPELINE
# ============================================================================
# IMPORTANT: The ONLY source data file used by this pipeline is:
#   C:\Users\yadav\Desktop\SEM 7\DS\OWID_ENERGY\data\1_original-owid-energy-data.csv
#
# Nothing from the previous 4,866-row filtered file, Tableau-exported CSV, or
# any intermediate dataset is used as an input.
#
# The pipeline deliberately keeps the original OWID 130-column schema because
# the existing Tableau workbook contains calculations/worksheets that refer
# to those field names. It cleans the rows and values while preserving that
# schema so the resulting CSV can replace the CSV used by the workbook.
# ============================================================================

DATA_DIR = Path(r"C:\Users\yadav\Desktop\SEM 7\DS\OWID_ENERGY\data")
RAW_FILE = DATA_DIR / "1_original-owid-energy-data.csv"

PROCESSED_DIR = DATA_DIR / "processed"
EDA_DIR = DATA_DIR / "eda"
TABLEAU_CSV = PROCESSED_DIR / "1.owid-energy-data.csv"
AUDIT_CSV = EDA_DIR / "OWID_Energy_Cleaning_Audit.csv"
MISSING_CSV = EDA_DIR / "OWID_Energy_Missing_Values.csv"
ENTITY_CSV = EDA_DIR / "OWID_Energy_Entity_Coverage.csv"
SUMMARY_JSON = EDA_DIR / "OWID_Energy_Pipeline_Summary.json"

START_YEAR = 2000
END_YEAR = 2025
EXPECTED_RAW_ROWS = 23232
EXPECTED_RAW_COLS = 130
EXPECTED_FINAL_ROWS = 4866
EXPECTED_FINAL_COLS = 130
EXPECTED_ENTITIES = 197

# Exact entity exclusions used to reproduce the Tableau project's analytical
# scope. They are encoded here so this script remains independent of the old
# filtered CSV.
EXCLUDED_ENTITIES = {
    "Antarctica",
    "British Virgin Islands",
    "Cayman Islands",
    "Cook Islands",
    "Falkland Islands",
    "Faroe Islands",
    "French Guiana",
    "French Polynesia",
    "Greenland",
    "Guadeloupe",
    "Guam",
    "Montserrat",
    "Netherlands Antilles",
    "New Caledonia",
    "Niue",
    "Reunion",
    "Saint Helena",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines",
    "Turks and Caicos Islands",
    "United States Virgin Islands",
    "Western Sahara",
}

TEXT_FIELDS = {"country", "iso_code"}
KEY_FIELDS = {"country", "iso_code", "year"}

# Negative values are valid for these fields because they represent changes or
# net electricity imports (negative = net exports).
NEGATIVE_ALLOWED = {
    "net_elec_imports",
    "net_elec_imports_share_demand",
}

# Base metrics used to deterministically fill missing derived fields. Only a
# missing derived value is filled when all required source components exist.
CONSUMPTION_BASES = {
    "biofuel": "biofuel_consumption",
    "coal": "coal_consumption",
    "fossil": "fossil_fuel_consumption",
    "gas": "gas_consumption",
    "hydro": "hydro_consumption",
    "low_carbon": "low_carbon_consumption",
    "nuclear": "nuclear_consumption",
    "oil": "oil_consumption",
    "other_renewables": "other_renewable_consumption",
    "renewables": "renewables_consumption",
    "solar": "solar_consumption",
    "wind": "wind_consumption",
}

ELECTRICITY_BASES = {
    "biofuel": "biofuel_electricity",
    "coal": "coal_electricity",
    "fossil": "fossil_electricity",
    "gas": "gas_electricity",
    "hydro": "hydro_electricity",
    "low_carbon": "low_carbon_electricity",
    "nuclear": "nuclear_electricity",
    "oil": "oil_electricity",
    "other_renewables": "other_renewable_electricity",
    "renewables": "renewables_electricity",
    "solar": "solar_electricity",
    "wind": "wind_electricity",
}

PRODUCTION_BASES = {
    "coal": "coal_production",
    "gas": "gas_production",
    "oil": "oil_production",
}

# Maps source columns whose exact meaning is a per-capita value to their base.
PER_CAPITA_BASES = {
    "electricity_demand_per_capita": "electricity_demand",
    "per_capita_electricity": "electricity_generation",
    "energy_per_capita": "primary_energy_consumption",
    "fossil_energy_per_capita": "fossil_fuel_consumption",
    "other_renewables_elec_per_capita": "other_renewable_electricity",
    "other_renewables_elec_per_capita_exc_biofuel": "other_renewable_exc_biofuel_electricity",
    "other_renewables_energy_per_capita": "other_renewable_consumption",
}

for prefix, base in CONSUMPTION_BASES.items():
    PER_CAPITA_BASES[f"{prefix}_cons_per_capita"] = base
    PER_CAPITA_BASES[f"{prefix}_energy_per_capita"] = base
for prefix, base in ELECTRICITY_BASES.items():
    PER_CAPITA_BASES[f"{prefix}_elec_per_capita"] = base
for prefix, base in PRODUCTION_BASES.items():
    PER_CAPITA_BASES[f"{prefix}_prod_per_capita"] = base

SHARE_ELEC_BASES = dict(ELECTRICITY_BASES)
SHARE_ELEC_BASES["other_renewables_exc_biofuel"] = "other_renewable_exc_biofuel_electricity"

SHARE_ENERGY_BASES = dict(CONSUMPTION_BASES)

CHANGE_CONSUMPTION_OUTPUTS = {
    "biofuel_cons_change_twh": "biofuel_consumption",
    "coal_cons_change_twh": "coal_consumption",
    "fossil_cons_change_twh": "fossil_fuel_consumption",
    "gas_cons_change_twh": "gas_consumption",
    "hydro_cons_change_twh": "hydro_consumption",
    "low_carbon_cons_change_twh": "low_carbon_consumption",
    "nuclear_cons_change_twh": "nuclear_consumption",
    "oil_cons_change_twh": "oil_consumption",
    "other_renewables_cons_change_twh": "other_renewable_consumption",
    "renewables_cons_change_twh": "renewables_consumption",
    "solar_cons_change_twh": "solar_consumption",
    "wind_cons_change_twh": "wind_consumption",
}
CHANGE_CONSUMPTION_PCT_OUTPUTS = {
    k.replace("_twh", "_pct"): v for k, v in CHANGE_CONSUMPTION_OUTPUTS.items()
}
CHANGE_PRODUCTION_OUTPUTS = {
    "coal_prod_change_twh": "coal_production",
    "gas_prod_change_twh": "gas_production",
    "oil_prod_change_twh": "oil_production",
}
CHANGE_PRODUCTION_PCT_OUTPUTS = {
    k.replace("_twh", "_pct"): v for k, v in CHANGE_PRODUCTION_OUTPUTS.items()
}

DERIVABLE_COLUMNS = set(PER_CAPITA_BASES) | {
    "energy_per_gdp",
    "electricity_share_energy",
    "net_elec_imports_share_demand",
}
DERIVABLE_COLUMNS |= {f"{k}_share_elec" for k in SHARE_ELEC_BASES if k != "other_renewables_exc_biofuel"}
DERIVABLE_COLUMNS |= {"other_renewables_share_elec_exc_biofuel"}
DERIVABLE_COLUMNS |= {f"{k}_share_energy" for k in SHARE_ENERGY_BASES}
DERIVABLE_COLUMNS |= set(CHANGE_CONSUMPTION_OUTPUTS)
DERIVABLE_COLUMNS |= set(CHANGE_CONSUMPTION_PCT_OUTPUTS)
DERIVABLE_COLUMNS |= set(CHANGE_PRODUCTION_OUTPUTS)
DERIVABLE_COLUMNS |= set(CHANGE_PRODUCTION_PCT_OUTPUTS)


def clean_text(value: str | None) -> str:
    if value is None:
        return ""
    value = str(value).replace("\ufeff", "").strip()
    value = re.sub(r"\s+", " ", value)
    return value


def to_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = str(value).strip()
    if value == "" or value.lower() in {"na", "n/a", "nan", "null", "none"}:
        return None
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def format_number(x: float) -> str:
    # OWID's downloaded data is rounded to three decimals for most energy
    # metrics. Keeping this precision avoids unnecessary floating-point noise.
    if abs(x) < 5e-13:
        x = 0.0
    return f"{x:.3f}"


def format_integer(x: float) -> str:
    if abs(x) < 0.5:
        x = 0.0
    return str(int(round(x)))


def blank(value: str | None) -> bool:
    return value is None or str(value).strip() == ""


def row_numeric(row: dict[str, str], key: str) -> float | None:
    return to_float(row.get(key, ""))


def set_if_missing(row: dict[str, str], output: str, value: float | None, repairs: Counter[str]) -> None:
    # Never create new columns: the Tableau workbook must receive the exact 130-column source schema.
    if output not in row:
        return
    if value is None or not math.isfinite(value):
        return
    if blank(row.get(output, "")):
        row[output] = format_number(value)
        repairs[output] += 1


def derive_ratio(row: dict[str, str], output: str, numerator: str, denominator: str, multiplier: float, repairs: Counter[str]) -> None:
    if not blank(row.get(output, "")):
        return
    a = row_numeric(row, numerator)
    b = row_numeric(row, denominator)
    if a is None or b in (None, 0):
        return
    set_if_missing(row, output, a * multiplier / b, repairs)


def read_raw_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    # Detect UTF-8 BOM cleanly; the provided OWID file is UTF-8.
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = [clean_text(h) for h in (reader.fieldnames or [])]
        rows = []
        for raw in reader:
            row = {clean_text(k): clean_text(v) for k, v in raw.items() if k is not None}
            rows.append(row)
    return headers, rows


def build_project_scope(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    scoped = []
    for row in rows:
        year = to_float(row.get("year"))
        if year is None or int(year) != year:
            continue
        year = int(year)
        if year < START_YEAR or year > END_YEAR:
            continue
        country = row.get("country", "")
        iso = row.get("iso_code", "")
        # Keep ISO-coded entities except the known territory set, plus Kosovo
        # so the Tableau project's 197-entity scope is reproduced without using
        # the old filtered dataset as an input.
        keep = (
            (iso != "" and country not in EXCLUDED_ENTITIES)
            or country == "Kosovo"
        )
        if keep:
            row["year"] = str(year)
            scoped.append(row)
    return scoped


def validate_and_clean_numeric(rows: list[dict[str, str]], headers: list[str], audit: list[dict[str, object]]) -> Counter[str]:
    invalid = Counter[str]()
    numeric_fields = [h for h in headers if h not in KEY_FIELDS]
    for row in rows:
        for field in numeric_fields:
            raw = row.get(field, "")
            if blank(raw):
                row[field] = ""
                continue
            value = to_float(raw)
            if value is None:
                if raw.strip() != "":
                    invalid[field] += 1
                row[field] = ""
            else:
                row[field] = format_integer(value) if field in {"population", "gdp"} else format_number(value)
        row["country"] = clean_text(row.get("country"))
        row["iso_code"] = clean_text(row.get("iso_code"))
        y = to_float(row.get("year"))
        row["year"] = str(int(y)) if y is not None and int(y) == y else ""
    if sum(invalid.values()):
        audit.append({
            "stage": "numeric_validation",
            "metric": "invalid_numeric_tokens",
            "count": sum(invalid.values()),
            "details": "Non-numeric/non-finite numeric cells converted to blank.",
        })
    return invalid


def repair_iso_codes(rows: list[dict[str, str]], history_rows: list[dict[str, str]], repairs: Counter[str], audit: list[dict[str, object]]) -> None:
    # Fill ISO code only when a country has one unique non-empty ISO code in the
    # raw history. Kosovo intentionally remains blank because its source rows do
    # not provide an ISO code in this dataset.
    country_codes: defaultdict[str, set[str]] = defaultdict(set)
    for row in history_rows:
        c = clean_text(row.get("country"))
        iso = clean_text(row.get("iso_code"))
        if c and iso:
            country_codes[c].add(iso)
    for row in rows:
        if row.get("iso_code", ""):
            continue
        c = row.get("country", "")
        codes = country_codes.get(c, set())
        if len(codes) == 1:
            row["iso_code"] = next(iter(codes))
            repairs["iso_code"] += 1
    if repairs["iso_code"]:
        audit.append({
            "stage": "structural_cleaning",
            "metric": "missing_iso_filled",
            "count": repairs["iso_code"],
            "details": "Filled only from an unambiguous ISO code observed for the same country in the raw OWID history.",
        })


def deterministic_repairs(
    rows: list[dict[str, str]],
    history_rows: list[dict[str, str]],
    repairs: Counter[str],
) -> None:
    # Country/year history including 1999 is needed to derive 2000 change
    # metrics correctly.
    history: defaultdict[str, dict[int, dict[str, str]]] = defaultdict(dict)
    for row in history_rows:
        y = to_float(row.get("year"))
        if y is None or int(y) != y:
            continue
        history[row["country"]][int(y)] = row

    for row in rows:
        country = row["country"]
        y = int(row["year"])
        previous = history.get(country, {}).get(y - 1)

        # All exact per-capita fields present in the workbook's source schema.
        for output, base in PER_CAPITA_BASES.items():
            derive_ratio(row, output, base, "population", 1e9, repairs)

        # Energy per GDP is kWh of primary energy per unit of GDP.
        derive_ratio(row, "energy_per_gdp", "primary_energy_consumption", "gdp", 1e9, repairs)

        # Electricity demand imports as a share of demand.
        derive_ratio(row, "net_elec_imports_share_demand", "net_elec_imports", "electricity_demand", 100.0, repairs)

        # Electricity shares.
        generation = row_numeric(row, "electricity_generation")
        if generation not in (None, 0):
            for prefix, base in SHARE_ELEC_BASES.items():
                if prefix == "other_renewables_exc_biofuel":
                    output = "other_renewables_share_elec_exc_biofuel"
                else:
                    output = f"{prefix}_share_elec"
                derive_ratio(row, output, base, "electricity_generation", 100.0, repairs)

        # Energy shares.
        for prefix, base in SHARE_ENERGY_BASES.items():
            derive_ratio(row, f"{prefix}_share_energy", base, "primary_energy_consumption", 100.0, repairs)
        derive_ratio(row, "electricity_share_energy", "electricity_generation", "primary_energy_consumption", 100.0, repairs)

        # Year-over-year consumption/production changes. Use raw history,
        # including 1999, so 2000 change values can be filled when possible.
        if previous is not None:
            for output, base in CHANGE_CONSUMPTION_OUTPUTS.items():
                current_value = row_numeric(row, base)
                previous_value = row_numeric(previous, base)
                if current_value is not None and previous_value is not None:
                    set_if_missing(row, output, current_value - previous_value, repairs)
            for output, base in CHANGE_CONSUMPTION_PCT_OUTPUTS.items():
                current_value = row_numeric(row, base)
                previous_value = row_numeric(previous, base)
                if current_value is not None and previous_value not in (None, 0):
                    set_if_missing(row, output, (current_value - previous_value) / previous_value * 100.0, repairs)
            for output, base in CHANGE_PRODUCTION_OUTPUTS.items():
                current_value = row_numeric(row, base)
                previous_value = row_numeric(previous, base)
                if current_value is not None and previous_value is not None:
                    set_if_missing(row, output, current_value - previous_value, repairs)
            for output, base in CHANGE_PRODUCTION_PCT_OUTPUTS.items():
                current_value = row_numeric(row, base)
                previous_value = row_numeric(previous, base)
                if current_value is not None and previous_value not in (None, 0):
                    set_if_missing(row, output, (current_value - previous_value) / previous_value * 100.0, repairs)


def validate_ranges(rows: list[dict[str, str]], headers: list[str], audit: list[dict[str, object]]) -> None:
    negative_counts = Counter[str]()
    bad_share_counts = Counter[str]()
    nonpositive_denominator_counts = Counter[str]()

    for row in rows:
        # Population and GDP should never be negative; negative source values
        # are treated as invalid rather than silently changing legitimate data.
        for field in ("population", "gdp"):
            value = row_numeric(row, field)
            if value is not None and value < 0:
                negative_counts[field] += 1
                row[field] = ""

        for field in headers:
            if field in KEY_FIELDS or field in NEGATIVE_ALLOWED:
                continue
            if "change_" in field or field.endswith("_change_pct") or field.endswith("_change_twh"):
                continue
            value = row_numeric(row, field)
            if value is not None and value < 0:
                negative_counts[field] += 1
                row[field] = ""

        for field in headers:
            if field.endswith("_share_elec") or field.endswith("_share_energy") or field == "net_elec_imports_share_demand":
                value = row_numeric(row, field)
                if value is not None and (value < -1e-9 or value > 100 + 1e-9):
                    bad_share_counts[field] += 1
                    row[field] = ""

        for field in ("population", "gdp"):
            value = row_numeric(row, field)
            if value == 0:
                nonpositive_denominator_counts[field] += 1

    if sum(negative_counts.values()):
        audit.append({
            "stage": "range_validation",
            "metric": "negative_non_change_values",
            "count": sum(negative_counts.values()),
            "details": "Negative values in fields that represent physical quantities or denominators were blanked; legitimate net-import and change values were exempted.",
        })
    if sum(bad_share_counts.values()):
        audit.append({
            "stage": "range_validation",
            "metric": "share_out_of_range",
            "count": sum(bad_share_counts.values()),
            "details": "Electricity/energy shares outside 0–100% were treated as invalid and blanked.",
        })
    if sum(nonpositive_denominator_counts.values()):
        audit.append({
            "stage": "range_validation",
            "metric": "zero_denominator_counts",
            "count": sum(nonpositive_denominator_counts.values()),
            "details": "Zero population/GDP values are retained as source facts, but are excluded as denominators for derived metrics.",
        })


def count_missing(rows: list[dict[str, str]], headers: list[str]) -> dict[str, int]:
    return {h: sum(1 for row in rows if blank(row.get(h, ""))) for h in headers}


def audit_country_year_uniqueness(rows: list[dict[str, str]], audit: list[dict[str, object]]) -> None:
    counts = Counter((r["country"], r["year"]) for r in rows)
    duplicates = [k for k, v in counts.items() if v > 1]
    if duplicates:
        raise ValueError(f"Conflicting/duplicate Country-Year records detected: {duplicates[:10]}")
    audit.append({
        "stage": "key_validation",
        "metric": "duplicate_country_year",
        "count": 0,
        "details": "Exactly one analytical record per Country-Year is required by the Tableau workbook.",
    })


def audit_schema(headers: list[str], audit: list[dict[str, object]]) -> None:
    if len(headers) != EXPECTED_RAW_COLS:
        raise ValueError(f"Raw source has {len(headers)} columns, expected {EXPECTED_RAW_COLS}.")
    required = {
        "country", "year", "iso_code", "population", "gdp", "electricity_generation",
        "electricity_demand", "primary_energy_consumption", "renewables_electricity",
        "renewables_share_elec", "carbon_intensity_elec",
    }
    missing = sorted(required - set(headers))
    if missing:
        raise ValueError(f"Raw source is missing required OWID columns: {missing}")
    audit.append({
        "stage": "schema_validation",
        "metric": "source_schema",
        "count": len(headers),
        "details": "130-column OWID source schema verified.",
    })


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]], encoding: str = "utf-8-sig") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in headers})


def write_audit(path: Path, records: list[dict[str, object]]) -> None:
    headers = ["stage", "metric", "count", "details"]
    write_csv(path, headers, [{h: str(r.get(h, "")) for h in headers} for r in records])


def write_missing_report(path: Path, before: dict[str, int], after: dict[str, int], total: int, headers: list[str]) -> None:
    rows = []
    for h in headers:
        b = before[h]
        a = after[h]
        rows.append({
            "field": h,
            "missing_before": b,
            "missing_after": a,
            "missing_before_pct": format_number(b / total * 100),
            "missing_after_pct": format_number(a / total * 100),
            "deterministic_reduction": b - a,
        })
    write_csv(path, ["field", "missing_before", "missing_after", "missing_before_pct", "missing_after_pct", "deterministic_reduction"], rows)


def write_entity_report(path: Path, rows: list[dict[str, str]]) -> None:
    by_entity: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_entity[row["country"]].append(row)
    out = []
    for country, entity_rows in sorted(by_entity.items()):
        years = [int(r["year"]) for r in entity_rows]
        isos = sorted({r["iso_code"] for r in entity_rows if r["iso_code"]})
        out.append({
            "country": country,
            "iso_code": isos[0] if len(isos) == 1 else ";".join(isos),
            "row_count": len(entity_rows),
            "min_year": min(years),
            "max_year": max(years),
            "expected_years": END_YEAR - START_YEAR + 1,
            "coverage_pct": format_number(len(entity_rows) / (END_YEAR - START_YEAR + 1) * 100),
        })
    write_csv(path, ["country", "iso_code", "row_count", "min_year", "max_year", "expected_years", "coverage_pct"], out)


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"RAW INPUT NOT FOUND:\n{RAW_FILE}\n\n"
            "Place the original 23,232-row file at exactly that path. "
            "This script intentionally does not search for or use other CSV files."
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    EDA_DIR.mkdir(parents=True, exist_ok=True)

    audit: list[dict[str, object]] = []
    repairs = Counter[str]()

    print("=" * 78)
    print("OWID ENERGY CLEANING PIPELINE -> TABLEAU CA3")
    print("=" * 78)
    print(f"RAW INPUT : {RAW_FILE}")
    print(f"TABLEAU OUT: {TABLEAU_CSV}")
    print()

    print("STEP 1/12  Loading ONLY the original OWID CSV...")
    headers, raw_rows = read_raw_csv(RAW_FILE)
    audit_schema(headers, audit)
    print(f"           Loaded {len(raw_rows):,} rows × {len(headers)} columns")
    if len(raw_rows) != EXPECTED_RAW_ROWS:
        print(f"           Warning: expected {EXPECTED_RAW_ROWS:,} rows but found {len(raw_rows):,}.")
    audit.append({
        "stage": "input",
        "metric": "raw_rows",
        "count": len(raw_rows),
        "details": "Rows loaded directly from the single specified raw OWID CSV.",
    })

    print("STEP 2/12  Standardising text and validating all numeric tokens...")
    # Clean the complete raw history first. This history is needed for 2000
    # year-over-year calculations.
    invalid = validate_and_clean_numeric(raw_rows, headers, audit)
    print(f"           Invalid/non-finite numeric tokens cleared: {sum(invalid.values()):,}")

    print(f"STEP 3/12  Restricting the analytical period to {START_YEAR}–{END_YEAR}...")
    period_rows = []
    for row in raw_rows:
        y = to_float(row.get("year"))
        if y is not None and START_YEAR <= int(y) <= END_YEAR:
            period_rows.append(row)
    print(f"           Rows after year filter: {len(period_rows):,}")
    audit.append({
        "stage": "row_scope",
        "metric": "year_filter",
        "count": len(period_rows),
        "details": f"Kept years {START_YEAR} through {END_YEAR} inclusive.",
    })

    print("STEP 4/12  Applying the Tableau project's explicit entity scope...")
    scoped_rows = build_project_scope(period_rows)
    print(f"           Rows after entity scope: {len(scoped_rows):,}")
    audit.append({
        "stage": "row_scope",
        "metric": "project_entity_scope",
        "count": len(scoped_rows),
        "details": "Kept ISO-coded analytical entities, excluded the documented territory set, and retained Kosovo as the workbook's ISO-less exception.",
    })

    print("STEP 5/12  Validating Country-Year uniqueness...")
    audit_country_year_uniqueness(scoped_rows, audit)
    print("           Duplicate Country-Year records: 0")

    print("STEP 6/12  Filling only deterministic, mathematically derivable values...")
    before_missing = count_missing(scoped_rows, headers)
    repair_iso_codes(scoped_rows, raw_rows, repairs, audit)
    deterministic_repairs(scoped_rows, raw_rows, repairs)
    after_missing = count_missing(scoped_rows, headers)
    print(f"           Deterministic repairs made: {sum(repairs.values()):,} cells")
    print("           No statistical interpolation or blanket zero-filling was used.")

    print("STEP 7/12  Validating physical ranges, shares, and denominators...")
    validate_ranges(scoped_rows, headers, audit)

    print("STEP 8/12  Sorting the final data for clean time-series analysis...")
    scoped_rows.sort(key=lambda r: (r["country"], int(r["year"])))

    print("STEP 9/12  Final schema and row-count validation...")
    final_headers = headers
    final_rows = scoped_rows
    if len(final_headers) != EXPECTED_FINAL_COLS:
        raise ValueError(f"Final schema has {len(final_headers)} columns; Tableau expects {EXPECTED_FINAL_COLS}.")
    if len(final_rows) != EXPECTED_FINAL_ROWS:
        raise ValueError(
            f"Final row count is {len(final_rows):,}, expected {EXPECTED_FINAL_ROWS:,}. "
            "This stops the pipeline rather than silently generating an incompatible Tableau source."
        )
    entity_count = len({r["country"] for r in final_rows})
    if entity_count != EXPECTED_ENTITIES:
        raise ValueError(f"Final entity count is {entity_count}, expected {EXPECTED_ENTITIES}.")

    print(f"           FINAL: {len(final_rows):,} rows × {len(final_headers)} columns")
    print(f"           FINAL: {entity_count} entities")

    audit.append({
        "stage": "final_validation",
        "metric": "final_rows",
        "count": len(final_rows),
        "details": "Validated Tableau-ready row count.",
    })
    audit.append({
        "stage": "final_validation",
        "metric": "final_entities",
        "count": entity_count,
        "details": "Validated analytical entity count.",
    })
    audit.append({
        "stage": "repair_summary",
        "metric": "deterministic_repairs_total",
        "count": sum(repairs.values()),
        "details": "Missing derived fields filled only from exact source relationships or year-over-year source history.",
    })

    print("STEP 10/12 Writing the Tableau-ready CSV...")
    write_csv(TABLEAU_CSV, final_headers, final_rows)

    print("STEP 11/12 Writing audit and EDA metadata...")
    write_audit(AUDIT_CSV, audit)
    write_missing_report(MISSING_CSV, before_missing, after_missing, len(final_rows), final_headers)
    write_entity_report(ENTITY_CSV, final_rows)

    summary = {
        "input_file": str(RAW_FILE),
        "input_rows": len(raw_rows),
        "input_columns": len(headers),
        "analysis_start_year": START_YEAR,
        "analysis_end_year": END_YEAR,
        "period_rows": len(period_rows),
        "final_rows": len(final_rows),
        "final_columns": len(final_headers),
        "final_entities": entity_count,
        "tableau_output": str(TABLEAU_CSV),
        "audit_output": str(AUDIT_CSV),
        "missing_value_report": str(MISSING_CSV),
        "entity_coverage_report": str(ENTITY_CSV),
        "deterministic_repairs_total": sum(repairs.values()),
        "repair_counts_by_field": dict(sorted(repairs.items())),
        "cleaning_policy": {
            "blank_numeric_tokens_to_null": True,
            "negative_physical_values": "validated; invalid negatives blanked, legitimate change/net-import negatives retained",
            "shares": "validated to 0-100 where defined",
            "missing_values": "not blanket-filled; only exact derivations are filled",
            "statistical_imputation": False,
            "zero_fill": False,
            "source_files_used_as_inputs": ["1_original-owid-energy-data.csv"],
            "old_filtered_csv_used": False,
            "tableau_export_used": False,
        },
    }
    SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("STEP 12/12  Round-trip verification of the written CSV...")
    check_headers, check_rows = read_raw_csv(TABLEAU_CSV)
    if check_headers != final_headers:
        raise ValueError("Round-trip header mismatch after writing Tableau CSV.")
    if len(check_rows) != len(final_rows):
        raise ValueError("Round-trip row-count mismatch after writing Tableau CSV.")
    duplicate_check = Counter((r["country"], r["year"]) for r in check_rows)
    dup_count = sum(1 for v in duplicate_check.values() if v > 1)
    if dup_count:
        raise ValueError(f"Round-trip verification found {dup_count} duplicate Country-Year keys.")

    print()
    print("DONE")
    print("-" * 78)
    print(f"Tableau-ready CSV : {TABLEAU_CSV}")
    print(f"Cleaning audit    : {AUDIT_CSV}")
    print(f"Missing-value EDA : {MISSING_CSV}")
    print(f"Entity coverage   : {ENTITY_CSV}")
    print(f"Pipeline summary  : {SUMMARY_JSON}")
    print()
    print("The generated CSV keeps the exact 130-column schema required by the")
    print("repaired OWID Tableau workbook while using only the original raw file as input.")


if __name__ == "__main__":
    main()
