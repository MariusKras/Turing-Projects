import sqlite3
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.stats import chi2_contingency, chi2

def feature_count_plot(con: sqlite3.Connection, column_name: str, title: str) -> None:
    """
    Generate a bar plot showing the count of occurrences for each unique value in a column from a SQL database.

    Parameters:
        con (sqlite3.Connection): A SQLite connection object.
        column_name (str): The name of the column to be plotted.
        title (str): The title of the plot.

    Returns:
        None: This function does not return anything. It displays the plot using Plotly.
    """
    query = (
        f"SELECT {column_name}, COUNT(*) AS count FROM answer GROUP BY {column_name}"
    )
    data = pd.read_sql_query(query, con)
    fig = go.Figure(
        data=[
            go.Bar(
                x=data[column_name],
                y=data["count"],
                marker_color="#1f77b4",
                marker=dict(line=dict(width=1)),
            )
        ]
    )
    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
            "y": 0.95,
            "xanchor": "center",
            "yanchor": "top",
        },
        margin=dict(t=50, l=100, r=100, b=90),
        xaxis_title=column_name,
        yaxis_title="Number of Answers",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_white",
        height=320,
    )
    fig.show()

def analyze_relationship(con: sqlite3.Connection, question_number: int) -> None:
    """
    Analyze the relationship numericly and visually between two categorical questions in the survey data.

    Parameters:
        con (sqlite3.Connection): SQLite database connection.
        question_number (int): The question number to analyze.

    Returns:
        None: Displays a plot and prints statistical analysis results.
    """
    query = f"""
    SELECT 
        CASE 
            WHEN a.AnswerText = 'Possibly' OR a.AnswerText = 'Don''t Know' THEN 'Uncertain'
            ELSE a.AnswerText
        END AS AnswerText_x,
        CASE 
            WHEN b.AnswerText = 'Possibly' OR b.AnswerText = 'Don''t Know' THEN 'Uncertain'
            ELSE b.AnswerText
        END AS AnswerText_y
    FROM 
        answer AS a
    INNER JOIN 
        answer AS b ON a.UserID = b.UserID
    WHERE 
        a.QuestionID = {question_number} AND b.QuestionID = 33
        AND a.SurveyID NOT IN (2014, 2016) AND b.SurveyID NOT IN (2014, 2016)
    """
    merged_df = pd.read_sql_query(query, con)
    cross_tab = pd.crosstab(merged_df["AnswerText_y"], merged_df["AnswerText_x"])
    cross_tab = cross_tab.div(cross_tab.sum(axis=1), axis=0)
    index_names = cross_tab.index.tolist()
    column_names = cross_tab.columns.tolist()
    data = []
    for col_name in column_names:
        trace = go.Bar(x=index_names, y=cross_tab[col_name], name=col_name)
        data.append(trace)
    title_query = f"SELECT DISTINCT questiontext FROM question WHERE questionid = {question_number}"
    layout = go.Layout(
        title={
            "text": con.execute(title_query).fetchall()[0][0],
            "x": 0.49,
            "y": 0.93,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 15},
        },
        margin=dict(t=50, l=90, r=90, b=90),
        xaxis=dict(title="Disorder Status"),
        yaxis=dict(title="Proportion of Predictor<br>Categories"),
        legend_title_text="Predictor Categories",
        plot_bgcolor="rgba(0,0,0,0)",
        barmode="stack",
        height=320,
    )
    fig = go.Figure(data=data, layout=layout)
    fig.show()
    cross_tab = pd.crosstab(merged_df["AnswerText_y"], merged_df["AnswerText_x"])
    chi2_stat, p_val, dof, expected = chi2_contingency(cross_tab)
    alpha = 0.05
    critical_value = chi2.ppf(1 - alpha, dof)
    n = cross_tab.sum().sum()
    r, c = cross_tab.shape
    cramers_v = np.sqrt(chi2_stat / (n * (min(r, c) - 1)))
    print("Chi-square statistic:", round(chi2_stat, 2))
    print("p-value:", round(p_val, 3))
    print("Critical value is", round(critical_value, 2))
    if chi2_stat > critical_value:
        print(
            "The chi-square statistic exceeds the critical value, suggesting a significant association between the variables."
        )
    else:
        print(
            "The chi-square statistic does not exceed the critical value, indicating no significant association between the variables."
        )
    print("Cramer's V:", round(cramers_v, 2))

def no_plot_relationship(con: sqlite3.Connection, question_number: int) -> None:
    """
    Analyze the relationship numericly between two categorical questions in the survey data.

    Parameters:
        con (sqlite3.Connection): SQLite database connection.
        question_number (int): The question number to analyze.

    Returns:
        None
    """
    query = f"""
    SELECT a.UserID, a.AnswerText AS AnswerText_x, b.AnswerText AS AnswerText_y
    FROM answer AS a
    INNER JOIN answer AS b ON a.UserID = b.UserID
    WHERE a.QuestionID = {question_number} AND b.QuestionID = 33
    AND a.SurveyID NOT IN (2014, 2016) AND b.SurveyID NOT IN (2014, 2016)
    """
    merged_df = pd.read_sql_query(query, con)
    cross_tab = pd.crosstab(merged_df["AnswerText_y"], merged_df["AnswerText_x"])
    chi2_stat, p_val, dof, expected = chi2_contingency(cross_tab)
    alpha = 0.05
    critical_value = chi2.ppf(1 - alpha, dof)
    n = cross_tab.sum().sum()
    r, c = cross_tab.shape
    cramers_v = np.sqrt(chi2_stat / (n * (min(r, c) - 1)))
    print("Chi-square statistic:", round(chi2_stat, 2))
    print("p-value:", round(p_val, 3))
    print("Critical value is", round(critical_value, 2))
    if chi2_stat > critical_value:
        print(
            "The chi-square statistic exceeds the critical value, suggesting a significant association between the variables."
        )
    else:
        print(
            "The chi-square statistic does not exceed the critical value, indicating no significant association between the variables."
        )
    print("Cramer's V:", round(cramers_v, 2))

def possible_answers(con: sqlite3.Connection, QuestionID: int) -> pd.DataFrame:
    """
    Retrieve the possible answers and their frequencies for a given question from the database.

    Parameters:
        con (sqlite3.Connection): SQLite database connection.
        QuestionID (int): The ID of the question for which to retrieve possible answers.

    Returns:
        pd.DataFrame: A DataFrame containing the possible answers and their frequencies.
    """
    query = f"""
    SELECT AnswerText, COUNT(*) AS Count
    FROM answer
    WHERE QuestionID = {QuestionID}
    AND SurveyID NOT IN (2014, 2016)
    GROUP BY AnswerText
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, con)

def plot_single_feature(con: sqlite3.Connection, question_number: int) -> None:
    """
    Plot a single feature from the database.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the survey data.
        question_number (int): The ID of the feature to plot.

    Returns:
        None: Displays the plot.
    """
    query = f"""
    SELECT AnswerText, COUNT(*) AS Count
    FROM answer
    WHERE QuestionID = {question_number}
    AND SurveyID NOT IN (2014, 2016)
    GROUP BY AnswerText
    ORDER BY count DESC
    """
    data = pd.read_sql_query(query, con)
    fig = go.Figure(
        data=[go.Bar(x=data["AnswerText"], y=data["Count"], marker_color="#1f77b4")]
    )
    title_query = f"SELECT DISTINCT questiontext FROM question WHERE questionid = {question_number}"
    fig.update_layout(
        title={
            "text": con.execute(title_query).fetchall()[0][0],
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
        },
        margin=dict(t=50, l=100, r=100, b=0),
        xaxis_title="Possible Answers",
        yaxis_title="Number of Answers",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_white",
        height=270,
    )
    fig.show()
