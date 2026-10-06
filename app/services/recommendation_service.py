from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_FILE = BASE_DIR / "data" / "train.csv"


# ============================================================
# DATA
# ============================================================

properties = None


# ============================================================
# LOAD PROPERTY DATA
# ============================================================

def initialize_recommendations():

    global properties

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    properties = pd.read_csv(
        DATA_FILE
    )

    print(
        f"Recommendation dataset loaded: "
        f"{len(properties)} properties"
    )


# ============================================================
# STATUS
# ============================================================

def recommendation_status():

    return {
        "feature": "Property Recommendation",
        "status": (
            "online"
            if properties is not None
            else "offline"
        ),
        "dataset": "Ames Housing Dataset",
    }


# ============================================================
# RECOMMENDATIONS
# ============================================================

def recommend(request_data: dict):

    global properties

    if properties is None:
        initialize_recommendations()

    budget = float(
        request_data["budget"]
    )

    bedrooms = int(
        request_data["bedrooms"]
    )

    neighborhood = (
        request_data.get("neighborhood", "")
        .strip()
    )

    min_area = float(
        request_data.get("min_area", 0)
    )

    top_k = int(
        request_data.get("top_k", 6)
    )

    df = properties.copy()

    # --------------------------------------------------------
    # Basic filtering
    # --------------------------------------------------------

    filtered = df[
        (df["SalePrice"] <= budget)
        &
        (df["BedroomAbvGr"] >= bedrooms)
        &
        (df["GrLivArea"] >= min_area)
    ].copy()

    # --------------------------------------------------------
    # Neighborhood preference
    # --------------------------------------------------------

    if neighborhood:

        exact_location = filtered[
            filtered["Neighborhood"]
            .str.lower()
            ==
            neighborhood.lower()
        ]

        # Use preferred neighborhood if matches exist
        if not exact_location.empty:
            filtered = exact_location

    # --------------------------------------------------------
    # If strict filtering gives no results,
    # use broader search
    # --------------------------------------------------------

    if filtered.empty:

        filtered = df[
            (df["SalePrice"] <= budget)
            &
            (df["BedroomAbvGr"] >= bedrooms)
        ].copy()

    # --------------------------------------------------------
    # Calculate recommendation score
    # --------------------------------------------------------

    def calculate_score(row):

        score = 0.0

        # Budget efficiency
        if budget > 0:

            price_ratio = (
                row["SalePrice"] / budget
            )

            score += (
                max(
                    0,
                    1 - price_ratio
                ) * 35
            )

        # Bedroom match
        bedroom_difference = abs(
            row["BedroomAbvGr"] - bedrooms
        )

        score += max(
            0,
            20 - bedroom_difference * 5
        )

        # Quality
        score += (
            row["OverallQual"] * 3
        )

        # Area
        if min_area > 0:

            if row["GrLivArea"] >= min_area:
                score += 10

        # Location
        if neighborhood:

            if (
                str(row["Neighborhood"]).lower()
                ==
                neighborhood.lower()
            ):
                score += 20

        return round(
            score,
            2,
        )

    filtered["RecommendationScore"] = (
        filtered.apply(
            calculate_score,
            axis=1,
        )
    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    filtered = filtered.sort_values(
        by="RecommendationScore",
        ascending=False,
    )

    filtered = filtered.head(
        top_k
    )

    # --------------------------------------------------------
    # Prepare response
    # --------------------------------------------------------

    recommendations = []

    for _, row in filtered.iterrows():

        reasons = []

        # Budget
        if row["SalePrice"] <= budget:
            reasons.append(
                "Within your budget"
            )

        # Bedroom
        if row["BedroomAbvGr"] >= bedrooms:
            reasons.append(
                f"{int(row['BedroomAbvGr'])} bedrooms"
            )

        # Area
        if min_area > 0 and row["GrLivArea"] >= min_area:
            reasons.append(
                f"{int(row['GrLivArea']):,} sq ft living area"
            )

        # Quality
        if row["OverallQual"] >= 7:
            reasons.append(
                "High overall property quality"
            )
        elif row["OverallQual"] >= 5:
            reasons.append(
                "Good overall property quality"
            )

        # Location
        if neighborhood:
            if (
                str(row["Neighborhood"]).lower()
                ==
                neighborhood.lower()
            ):
                reasons.append(
                    "Matches preferred neighborhood"
                )

        recommendations.append(
            {
                "property_id": int(row["Id"]),
                "price": float(
                    row["SalePrice"]
                ),
                "bedrooms": int(
                    row["BedroomAbvGr"]
                ),
                "living_area_sqft": float(
                    row["GrLivArea"]
                ),
                "year_built": int(
                    row["YearBuilt"]
                ),
                "overall_quality": int(
                    row["OverallQual"]
                ),
                "neighborhood": str(
                    row["Neighborhood"]
                ),
                "bathrooms": int(
                    row["FullBath"]
                ),
                "garage_cars": int(
                    row["GarageCars"]
                ),
                "recommendation_score": float(
                    row["RecommendationScore"]
                ),
                "why_recommended": reasons,
            }
        )

    return {
        "success": True,
        "count": len(recommendations),
        "preferences": {
            "budget": budget,
            "bedrooms": bedrooms,
            "neighborhood": neighborhood,
            "minimum_area": min_area,
        },
        "recommendations": recommendations,
    }