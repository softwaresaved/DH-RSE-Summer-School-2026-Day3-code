"""
EVA Data Analysis

This script analyses NASA Extra-Vehicular Activity (spacewalk) data from 1965-2013.
It reads EVA data from a JSON file, cleans and transforms it, generates summary
statistics by astronaut, and creates a visualisation of cumulative time spent
in space over time.

Usage:
    python eva_data_analysis.py [input_file]

Arguments:
    input_file  Path to the input JSON file (default: eva_data.json)

Outputs:
    - eva_data.csv: Cleaned EVA data in CSV format
    - duration_by_astronaut.csv: Total EVA duration per astronaut
    - cumulative_eva_graph.png: Plot of cumulative spacewalk time over years
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt


def text_to_duration(duration):
    """
    Convert a text-format duration "HH:MM" to duration in hours.

    Args:
        duration (str): The text-format duration.

    Returns:
        float: The duration in hours.
    """
    hours, minutes = duration.split(":")
    return int(hours) + int(minutes) / 60


def read_json_to_dataframe(input_file):
    """
    Read EVA data from a JSON file into a Pandas DataFrame.

    Cleans the data by removing any rows where the 'duration' or 'date' value is missing.

    Args:
        input_file (str): Path to the JSON file.

    Returns:
        pd.DataFrame: The cleaned data as a DataFrame.
    """
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
    eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)
    return eva_df


def write_dataframe_to_csv(df, output_file):
    """
    Write a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The input DataFrame.
        output_file (str): Path to the output CSV file.

    Returns:
        None
    """
    df.to_csv(output_file, index=False, encoding='utf-8')


def summary_duration_by_astronaut(df):
    """
    Summarise EVA duration by individual astronaut.

    Args:
        df (pd.DataFrame): Input DataFrame containing 'crew' and 'duration' columns.

    Returns:
        pd.DataFrame: DataFrame with a row for each astronaut and their total duration in hours.
    """
    subset = df.loc[:, ['crew', 'duration']]
    subset.crew = subset.crew.str.split(';').apply(lambda x: [name.strip() for name in x if name.strip()])
    subset = subset.explode('crew')
    subset['duration_hours'] = subset['duration'].apply(text_to_duration)
    subset = subset.drop('duration', axis=1)
    return subset.groupby('crew').sum().reset_index()


def plot_cumulative_time_in_space(df, graph_file):
    """
    Plot the cumulative time spent in space over time and save to a file.

    Args:
        df (pd.DataFrame): Input DataFrame with 'date' and 'duration' columns.
        graph_file (str): Path to save the output graph.

    Returns:
        None
    """
    df['duration_hours'] = df['duration'].apply(text_to_duration)
    df['cumulative_time'] = df['duration_hours'].cumsum()
    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()


def main():
    # Use command-line argument if provided, otherwise use default
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'eva_data.json'
    output_file = 'eva_data.csv'
    duration_by_astronaut_file = 'duration_by_astronaut.csv'
    graph_file = 'cumulative_eva_graph.png'

    eva_df = read_json_to_dataframe(input_file)
    write_dataframe_to_csv(eva_df, output_file)

    duration_by_astronaut_df = summary_duration_by_astronaut(eva_df)
    write_dataframe_to_csv(duration_by_astronaut_df, duration_by_astronaut_file)

    eva_df.sort_values('date', inplace=True)
    plot_cumulative_time_in_space(eva_df, graph_file)


if __name__ == "__main__":
    main()