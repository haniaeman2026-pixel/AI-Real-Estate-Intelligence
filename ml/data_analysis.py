from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

ANALYSIS_DIR = BASE_DIR / "models" / "analysis"

TRAIN_FILE = DATA_DIR / "train.csv"


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

ANALYSIS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not TRAIN_FILE.exists():

        raise FileNotFoundError(
            f"Dataset not found: {TRAIN_FILE}"
        )

    df = pd.read_csv(
        TRAIN_FILE
    )

    return df


# ============================================================
# DATA SUMMARY
# ============================================================

def generate_summary():

    df = load_data()

    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "average_price": float(
            df["SalePrice"].mean()
        ),
        "minimum_price": float(
            df["SalePrice"].min()
        ),
        "maximum_price": float(
            df["SalePrice"].max()
        ),
        "median_price": float(
            df["SalePrice"].median()
        ),
        "average_living_area": float(
            df["GrLivArea"].mean()
        ),
    }

    summary_df = pd.DataFrame(
        [summary]
    )

    output_file = (
        ANALYSIS_DIR /
        "data_summary.csv"
    )

    summary_df.to_csv(
        output_file,
        index=False,
    )

    print(
        f"Summary saved: {output_file}"
    )

    return summary


# ============================================================
# PRICE DISTRIBUTION
# ============================================================

def create_price_distribution():

    df = load_data()

    plt.figure(
        figsize=(10, 6)
    )

    sns.histplot(
        df["SalePrice"],
        kde=True,
    )

    plt.title(
        "Property Sale Price Distribution"
    )

    plt.xlabel(
        "Sale Price"
    )

    plt.ylabel(
        "Number of Properties"
    )

    plt.tight_layout()

    output_file = (
        ANALYSIS_DIR /
        "price_distribution.png"
    )

    plt.savefig(
        output_file,
        dpi=150,
    )

    plt.close()

    print(
        f"Chart saved: {output_file}"
    )


# ============================================================
# AREA VS PRICE
# ============================================================

def create_area_price_chart():

    df = load_data()

    plt.figure(
        figsize=(10, 6)
    )

    sns.scatterplot(
        data=df,
        x="GrLivArea",
        y="SalePrice",
    )

    plt.title(
        "Living Area vs Property Price"
    )

    plt.xlabel(
        "Above Ground Living Area (sq ft)"
    )

    plt.ylabel(
        "Sale Price"
    )

    plt.tight_layout()

    output_file = (
        ANALYSIS_DIR /
        "area_vs_price.png"
    )

    plt.savefig(
        output_file,
        dpi=150,
    )

    plt.close()

    print(
        f"Chart saved: {output_file}"
    )


# ============================================================
# NEIGHBORHOOD PRICE ANALYSIS
# ============================================================

def create_neighborhood_chart():

    df = load_data()

    neighborhood_prices = (
        df.groupby("Neighborhood")[
            "SalePrice"
        ]
        .median()
        .sort_values(
            ascending=False
        )
        .head(15)
    )

    plt.figure(
        figsize=(12, 7)
    )

    neighborhood_prices.plot(
        kind="bar"
    )

    plt.title(
        "Median Property Price by Neighborhood"
    )

    plt.xlabel(
        "Neighborhood"
    )

    plt.ylabel(
        "Median Sale Price"
    )

    plt.xticks(
        rotation=45,
        ha="right",
    )

    plt.tight_layout()

    output_file = (
        ANALYSIS_DIR /
        "neighborhood_prices.png"
    )

    plt.savefig(
        output_file,
        dpi=150,
    )

    plt.close()

    print(
        f"Chart saved: {output_file}"
    )


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

def create_correlation_chart():

    df = load_data()

    numeric_columns = [
        "SalePrice",
        "OverallQual",
        "GrLivArea",
        "YearBuilt",
        "TotalBsmtSF",
        "GarageCars",
        "FullBath",
        "BedroomAbvGr",
        "LotArea",
    ]

    correlation = (
        df[numeric_columns]
        .corr()
    )

    plt.figure(
        figsize=(11, 8)
    )

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
    )

    plt.title(
        "Real Estate Feature Correlation"
    )

    plt.tight_layout()

    output_file = (
        ANALYSIS_DIR /
        "correlation_heatmap.png"
    )

    plt.savefig(
        output_file,
        dpi=150,
    )

    plt.close()

    print(
        f"Chart saved: {output_file}"
    )


# ============================================================
# RUN ALL ANALYSIS
# ============================================================

def run_analysis():

    print("=" * 60)

    print(
        "Running Real Estate Data Analysis"
    )

    print("=" * 60)

    generate_summary()

    create_price_distribution()

    create_area_price_chart()

    create_neighborhood_chart()

    create_correlation_chart()

    print("=" * 60)

    print(
        "Data analysis completed successfully."
    )

    print("=" * 60)


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_analysis()