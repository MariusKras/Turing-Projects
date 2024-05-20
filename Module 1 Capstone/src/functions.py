import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from matplotlib.axes._axes import Axes


def extract_state_code(x: str) -> str:
    """
    Extract the state code from a given input value.

    Args:
        x (str): The input value (individual element in a specific feature) from which to extract the state code.

    Returns:
        str: The extracted state code.

    Examples:
        >>> extract_state_code("1005")
        '10'
        >>> extract_state_code("90200126")
        '02'
        >>> extract_state_code("13071")
        '13'
    """
    x_str = str(x)
    if len(x_str) > 7:
        return x_str[1:3]
    elif len(x_str) == 6:
        return "0" + x_str[0]
    else:
        return x_str[0:2]


new_column_names = {
    "PST045214": "Population 2014",
    "PST120214": "Population Change 10to14 %",
    "AGE295214": "Age Under 18 %",
    "AGE135214": "Age Under 5 %",
    "AGE775214": "Age Over 65 %",
    "SEX255214": "Female %",
    "RHI125214": "White %",
    "RHI225214": "Black %",
    "RHI325214": "Native %",
    "RHI425214": "Asian %",
    "RHI625214": "Two Or More Race %",
    "RHI725214": "Hispanic %",
    "RHI825214": "White Non Hispanic %",
    "POP715213": "Same House Live 1 Year %",
    "POP645213": "Foreign Born %",
    "POP815213": "Non English Home %",
    "EDU635213": "HS Grad Or Higher %",
    "EDU685213": "Bachelor Degree Or Higher %",
    "VET605213": "Veterans",
    "LFE305213": "Mean Travel Time To Work",
    "HSG010214": "Housing Units",
    "HSG445213": "Homeownership %",
    "HSG096213": "Multi Unit Structures %",
    "HSG495213": "Median Housing Value",
    "HSD410213": "Households",
    "HSD310213": "Persons Per Household",
    "INC910213": "Per Capita Income",
    "INC110213": "Median Household Income",
    "PVY020213": "Persons Below Poverty Level %",
    "BZA010213": "Private Nonfarm Establishments",
    "BZA110213": "Private Nonfarm Employment",
    "BZA115213": "Private Nonfarm Employment Change",
    "NES010213": "Nonemployer Establishments",
    "SBO001207": "Total Firms",
    "SBO315207": "Black Owned Firms %",
    "SBO115207": "Native American Owned Firms %",
    "SBO215207": "Asian Owned Firms %",
    "SBO415207": "Hispanic Owned Firms %",
    "SBO015207": "Women Owned Firms %",
    "MAN450207": "Manufacturers Shipments",
    "WTN220207": "Merchant Wholesaler Sales",
    "RTN131207": "Retail Sales Per Capita",
    "AFN120207": "Accommodation Food Services Sales",
    "BPS030214": "Building Permits",
    "LND110210": "Land Area SqMiles",
    "POP060210": "Population Per SqMile",
}

state_abbreviations_map = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

features_to_calculate = [
    "Private Nonfarm Establishments",
    "Private Nonfarm Employment",
    "Nonemployer Establishments",
    "Housing Units",
    "Manufacturers Shipments",
    "Merchant Wholesaler Sales",
    "Retail Sales Per Capita",
    "Accommodation Food Services Sales",
    "Building Permits",
]

new_feature_names = [
    "Private Nonfarm Establishments %",
    "Private Nonfarm Employment %",
    "Nonemployer Establishments %",
    "Housing Units Per Capita",
    "Manufacturers Shipments Per Capita",
    "Merchant Wholesaler Sales Per Capita",
    "Retail Sales Per Capita",
    "Accommodation Food Services Sales Per Capita",
    "Building Permits Per Capita",
]


def merge_demographics_with_votes(
    demographics_dataframe: DataFrame,
    primary_results: DataFrame,
    state_names: list[str],
) -> DataFrame:
    """
    Merge demographic data with primary vote results for selected states.

    Args:
        demographics_dataframe (DataFrame): DataFrame containing USA county demographic data.
        primary_results (DataFrame): DataFrame containing primary vote results.
        state_names (List[str]): List of state names to include in the merged data.

    Returns:
        DataFrame: Merged DataFrame containing demographic data and primary vote results for selected states.
    """
    selected_states_primary = primary_results[
        primary_results["state"].isin(state_names)
    ]
    grouped_votes = (
        selected_states_primary.groupby(["county", "party"])["votes"]
        .sum()
        .reset_index()
    )
    votes_by_county = grouped_votes.pivot(
        index="county", columns="party", values="votes"
    ).reset_index()
    votes_by_county.columns = ["County", "Democrat Votes", "Republican Votes"]

    selected_states_demographics = demographics_dataframe[
        demographics_dataframe["State"].isin(state_names)
    ]
    merged_data = selected_states_demographics.merge(votes_by_county, on="County")
    merged_data["Democrat Vote %"] = (
        merged_data["Democrat Votes"] / merged_data["Population 2014"] * 100
    )
    merged_data["Republican Vote %"] = (
        merged_data["Republican Votes"] / merged_data["Population 2014"] * 100
    )
    return merged_data


def iqr(df: DataFrame) -> DataFrame:
    """
    Filter outliers from a two-dimensional DataFrame using the Interquartile Range (IQR) method.

    Args:
        df (DataFrame): Input DataFrame containing numerical data. It should be called on a dataframe with two dimensions.

    Returns:
        DataFrame: Filtered DataFrame with outliers removed.
    """
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_df = df[
        (df.iloc[:, 0] >= lower_bound.iloc[0])
        & (df.iloc[:, 0] <= upper_bound.iloc[0])
        & (df.iloc[:, 1] >= lower_bound.iloc[1])
        & (df.iloc[:, 1] <= upper_bound.iloc[1])
    ]
    return filtered_df


def iqr_return_outliers(df: DataFrame) -> DataFrame:
    """
    Identify outliers in a two-dimensional DataFrame using the Interquartile Range (IQR) method.

    Args:
        df (DataFrame): Input DataFrame containing numerical data. It should be called on a dataframe with two dimensions.

    Returns:
        DataFrame: DataFrame containing outliers identified using the IQR method.
    """
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outlier_df = df[
        (df.iloc[:, 0] < lower_bound.iloc[0])
        | (df.iloc[:, 0] > upper_bound.iloc[0])
        | (df.iloc[:, 1] < lower_bound.iloc[1])
        | (df.iloc[:, 1] > upper_bound.iloc[1])
    ]
    return outlier_df


def calculate_correlations(merged_data: DataFrame) -> DataFrame:
    """
    Calculate correlations between demographic features and voting patterns.

    Args:
        merged_data (DataFrame): DataFrame containing merged demographic and voting data.

    Returns:
        DataFrame: DataFrame with correlation results for each demographic feature.
    """
    merged_data = merged_data.drop(
        columns=["fips", "County", "state_abbreviation", "State"]
    )
    columns_to_correlate = merged_data.columns[:-4]
    columns = [
        "Democrat Slope",
        "Democrat Corr Coeff",
        "Democrat p-value",
        "Republican Slope",
        "Republican Corr Coeff",
        "Republican p-value",
    ]
    correlation_df = pd.DataFrame(index=columns_to_correlate, columns=columns)
    for column in columns_to_correlate:
        iqr_democrat_vote = iqr(merged_data[[column, "Democrat Vote %"]])
        iqr_republican_vote = iqr(merged_data[[column, "Republican Vote %"]])
        if iqr_democrat_vote[column].sum() < 1:
            continue
        D_cor_coeff, D_p_value = spearmanr(
            iqr_democrat_vote[column], iqr_democrat_vote["Democrat Vote %"]
        )
        R_cor_coeff, R_p_value = spearmanr(
            iqr_republican_vote[column], iqr_republican_vote["Republican Vote %"]
        )
        d_slope, _ = np.polyfit(
            iqr_democrat_vote[column], iqr_democrat_vote["Democrat Vote %"], deg=1
        )
        r_slope, _ = np.polyfit(
            iqr_republican_vote[column], iqr_republican_vote["Republican Vote %"], deg=1
        )
        correlation_df.at[column, "Democrat Slope"] = round(d_slope, 2)
        correlation_df.at[column, "Republican Slope"] = round(r_slope, 2)
        correlation_df.at[column, "Democrat Corr Coeff"] = round(D_cor_coeff, 2)
        correlation_df.at[column, "Democrat p-value"] = round(D_p_value, 2)
        correlation_df.at[column, "Republican Corr Coeff"] = round(R_cor_coeff, 2)
        correlation_df.at[column, "Republican p-value"] = round(R_p_value, 2)
    return correlation_df


def no_iqr_calculate_correlations(merged_data: DataFrame) -> DataFrame:
    """
    Calculate correlations between demographic features and voting patterns without using IQR filtering.

    Args:
        merged_data (DataFrame): A DataFrame containing merged demographic and voting data.

    Returns:
        DataFrame: A DataFrame with correlation results for each demographic feature.
    """
    merged_data = merged_data.drop(
        columns=["fips", "County", "state_abbreviation", "State"]
    )
    columns_to_correlate = merged_data.columns[:-4]
    columns = [
        "Democrat Slope",
        "Democrat Corr Coeff",
        "Democrat p-value",
        "Republican Slope",
        "Republican Corr Coeff",
        "Republican p-value",
    ]
    correlation_df = pd.DataFrame(index=columns_to_correlate, columns=columns)
    for column in columns_to_correlate:
        if merged_data[column].sum() < 1:
            continue
        D_cor_coeff, D_p_value = spearmanr(
            merged_data[column], merged_data["Democrat Vote %"]
        )
        R_cor_coeff, R_p_value = spearmanr(
            merged_data[column], merged_data["Republican Vote %"]
        )
        d_slope, _ = np.polyfit(
            merged_data[column], merged_data["Democrat Vote %"], deg=1
        )
        r_slope, _ = np.polyfit(
            merged_data[column], merged_data["Republican Vote %"], deg=1
        )
        correlation_df.at[column, "Democrat Slope"] = round(d_slope, 2)
        correlation_df.at[column, "Republican Slope"] = round(r_slope, 2)
        correlation_df.at[column, "Democrat Corr Coeff"] = round(D_cor_coeff, 2)
        correlation_df.at[column, "Democrat p-value"] = round(D_p_value, 2)
        correlation_df.at[column, "Republican Corr Coeff"] = round(R_cor_coeff, 2)
        correlation_df.at[column, "Republican p-value"] = round(R_p_value, 2)
    return correlation_df


def correlations_only(
    demographics: DataFrame, primary_res: DataFrame, selected_states: list[str]
) -> DataFrame:
    """
    Calculate correlations between demographic features and voting patterns for selected states.

    Args:
        demographics (DataFrame): DataFrame containing USA county demographic data.
        primary_res (DataFrame): DataFrame containing primary vote results.
        selected_states (list[str]): List of state names to include in the analysis.

    Returns:
        DataFrame: DataFrame with correlation results for each demographic feature.
    """
    merged_data = merge_demographics_with_votes(
        demographics, primary_res, selected_states
    )
    states_correlation = calculate_correlations(merged_data)
    return states_correlation


def no_iqr_correlations_only(
    demographics: DataFrame, primary_res: DataFrame, selected_states: list[str]
) -> DataFrame:
    """
    Calculate correlations between demographic features and voting patterns for selected states without using IQR filtering.

    Args:
        demographics (DataFrame): DataFrame containing USA county demographic data.
        primary_res (DataFrame): DataFrame containing primary vote results.
        selected_states (list[str]): List of state names to include in the analysis.

    Returns:
        DataFrame: DataFrame with correlation results for each demographic feature.
    """
    merged_data = merge_demographics_with_votes(
        demographics, primary_res, selected_states
    )
    states_correlation = no_iqr_calculate_correlations(merged_data)
    return states_correlation


def plot_features_with_outliers_annotated(data: DataFrame, features: list[str]):
    """
    Plot features against Democrat Vote Percentage with outliers annotated.

    Args:
        data (DataFrame): DataFrame containing the data to plot.
        features (list[str]): List of feature names to plot against Democrat Vote Percentage.

    Returns:
        axes: Axes of the generated plots.
    """
    num_features = len(features)
    num_cols = 2
    num_rows = (num_features + 1) // num_cols
    if num_features % num_cols != 0:
        num_rows += 1
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 4 * num_rows))
    normalized_population = np.log1p(data["Population 2014"])
    for i, feature in enumerate(features):
        if num_rows > 1:
            row, col = divmod(i, num_cols)
            ax = axes[row, col]
        else:
            ax = axes[i]
        ax = sns.scatterplot(
            x=feature,
            y="Democrat Vote %",
            data=data,
            size=normalized_population * 2,
            color="#1f77b4",
            legend=False,
            ax=ax,
        )
        sns.regplot(
            x=feature,
            y="Democrat Vote %",
            data=data,
            scatter=False,
            ci=None,
            line_kws={"color": "skyblue"},
            ax=ax,
        )
        for line in range(0, data.shape[0]):
            ax.annotate(
                data["County"].iloc[line],
                (data[feature].iloc[line], data["Democrat Vote %"].iloc[line]),
                textcoords="offset points",
                xytext=(0, 3),
                ha="center",
                fontsize="small",
            )
        ax.set_title(f"{feature} vs. Democrat Vote Percentage")

        x_padding = 0.03 * (ax.get_xlim()[1] - ax.get_xlim()[0])
        y_padding = 0.03 * (ax.get_ylim()[1] - ax.get_ylim()[0])
        ax.set_xlim(ax.get_xlim()[0] - x_padding, ax.get_xlim()[1] + x_padding)
        ax.set_ylim(ax.get_ylim()[0] - y_padding, ax.get_ylim()[1] + y_padding)

    for i in range(num_features, num_rows * num_cols):
        if num_rows > 1:
            fig.delaxes(axes.flatten()[i])
        else:
            fig.delaxes(axes[i])
    plt.tight_layout(h_pad=2)
    return axes


def plot_features_no_outliers(data: DataFrame, features: list[str]):
    """
    Plot features against Democrat Vote Percentage with regression lines and no outliers.

    Args:
        data (DataFrame): DataFrame containing the data to plot.
        features (list[str]): List of feature names to plot against Democrat Vote Percentage.

    Returns:
        axes: Axes of the generated plots.
    """
    num_features = len(features)
    num_cols = 2
    num_rows = (num_features + 1) // num_cols
    if num_features % num_cols != 0:
        num_rows += 1
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 4 * num_rows))
    normalized_population = np.log1p(data["Population 2014"])
    for i, feature in enumerate(features):
        if num_rows > 1:
            row, col = divmod(i, num_cols)
            ax = axes[row, col]
        else:
            ax = axes[i]
        ax = sns.scatterplot(
            x=feature,
            y="Democrat Vote %",
            data=data,
            size=normalized_population * 2,
            legend=False,
            ax=ax,
        )
        data_for_iqr = data.drop(
            columns=["fips", "County", "state_abbreviation", "State"]
        )
        iqr_data = iqr(data_for_iqr[[feature, "Democrat Vote %"]])
        X = iqr_data[[feature]]
        y = iqr_data["Democrat Vote %"]
        model = LinearRegression().fit(X, y)
        slope = model.coef_[0]
        intercept = model.intercept_
        x_values = np.array([data[feature].min(), data[feature].max()])
        y_values = slope * x_values + intercept
        ax.plot(x_values, y_values, color="skyblue")

        outliers = iqr_return_outliers(data_for_iqr[[feature, "Democrat Vote %"]])
        sns.scatterplot(
            x=feature,
            y="Democrat Vote %",
            data=outliers,
            size=normalized_population,
            legend=False,
            ax=ax,
            color="Turquoise",
        )
        ax.set_title(f"{feature} vs. Democrat Vote Percentage")
    for i in range(num_features, num_rows * num_cols):
        if num_rows > 1:
            fig.delaxes(axes.flatten()[i])
        else:
            fig.delaxes(axes[i])
    plt.tight_layout(h_pad=2)
    return axes


def feature_research(merged_data: DataFrame, feature: str) -> DataFrame:
    """
    Conduct research on a feature in relation to other features in the merged dataset.

    Args:
        merged_data (DataFrame): DataFrame containing the merged data.
        feature (str): The feature to research.

    Returns:
        DataFrame: DataFrame with correlation coefficients, slope, and p-values for each feature.
    """
    merged_data = merged_data.drop(
        columns=["fips", "County", "state_abbreviation", "State"]
    )
    columns_to_correlate = merged_data.columns[:-4]
    columns_to_correlate = columns_to_correlate.drop(feature)
    columns = ["Slope", "Corr Coeff", "p-value"]
    correlation_df = pd.DataFrame(index=columns_to_correlate, columns=columns)

    for column in columns_to_correlate:
        iqr_merged_data = iqr(merged_data[[column, feature]])
        if np.all(np.round(iqr_merged_data[column], 2) == 0):
            continue
        slope, _ = np.polyfit(iqr_merged_data[column], iqr_merged_data[feature], deg=1)
        cor_coeff, p_value = spearmanr(
            iqr_merged_data[column], iqr_merged_data[feature]
        )
        correlation_df.at[column, "Slope"] = round(slope, 2)
        correlation_df.at[column, "Corr Coeff"] = np.round(cor_coeff, decimals=2)
        correlation_df.at[column, "p-value"] = np.round(p_value, decimals=2)
    return correlation_df


def individual_point_selector(
    data: DataFrame, ax: Axes, county_names: list[str]
) -> None:
    """
    Select and highlight individual data points from specified counties on a scatter plot.

    Args:
        data (DataFrame): DataFrame containing the data.
        ax (Axes): The Axes object representing the scatter plot.
        county_names (list[str]): List of county names to select and highlight.

    Returns:
        None
    """
    feature = ax.get_xlabel()
    normalized_population = np.log1p(data["Population 2014"])
    filtered_data = data[data["County"].isin(county_names)]
    sns.scatterplot(
        x=feature,
        y="Democrat Vote %",
        data=filtered_data,
        size=normalized_population * 2,
        color="red",
        legend=False,
        ax=ax,
    )


def state_info(single_state_merged: DataFrame) -> None:
    """
    Display information about a single state's population and voting statistics.

    Args:
        single_state_merged (DataFrame): DataFrame containing merged data for a single state.

    Returns:
        None
    """
    population = single_state_merged["Population 2014"].sum()
    democrat_votes = single_state_merged["Democrat Votes"].sum()
    democrat_vote_percent = round(democrat_votes / population * 100, 2)
    republican_votes = single_state_merged["Republican Votes"].sum()
    republican_vote_percent = round(republican_votes / population * 100, 2)
    print(f"2014 State Population: {population}")
    print(
        f"Votes for Democrats: {democrat_votes}, {democrat_vote_percent}% of the population."
    )
    print(
        f"Votes for Republicans: {republican_votes}, {republican_vote_percent}% of the population."
    )


def point_selector(data: DataFrame, ax: Axes, intercept_subtract: float) -> list[str]:
    """
    Select data points below a regression line on a scatter plot.

    Args:
        data (DataFrame): DataFrame containing the data.
        ax (Axes): The Axes object representing the scatter plot.
        intercept_subtract (float): Value to subtract from the intercept of the regression line.

    Returns:
        list[str]: List of county names for data points below the regression line.
    """
    feature = ax.get_xlabel()
    iqr_data = iqr(data[[feature, "Democrat Vote %"]])
    X = iqr_data[feature].values.reshape(-1, 1)
    y = iqr_data["Democrat Vote %"].values
    model = LinearRegression()
    model.fit(X, y)
    intercept = model.intercept_ - intercept_subtract
    slope = model.coef_[0]
    below_line = data[data["Democrat Vote %"] < (intercept + slope * data[feature])]
    ax.scatter(
        below_line[feature],
        below_line["Democrat Vote %"],
        color="none",
        edgecolor="red",
        linewidth=1.2,
        s=120,
        alpha=0.7,
    )
    return below_line["County"].tolist()
