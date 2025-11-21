"""
Visualization utilities for Smart Logistics Delivery Prediction
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def create_time_breakdown_chart(components: dict):
    """
    Create a breakdown chart of delivery time components.

    Args:
        components: Dictionary with component names and values

    Returns:
        Plotly figure object
    """
    df = pd.DataFrame(list(components.items()),
                      columns=['Component', 'Minutes'])
    df = df[df['Minutes'] > 0].sort_values('Minutes', ascending=True)

    fig = px.barh(
        df,
        x='Minutes',
        y='Component',
        color='Minutes',
        color_continuous_scale='Viridis',
        title='Delivery Time Component Breakdown',
        labels={'Minutes': 'Time (minutes)', 'Component': 'Factor'}
    )

    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='closest'
    )

    return fig


def create_time_distribution_pie(components: dict):
    """
    Create a pie chart of time distribution.

    Args:
        components: Dictionary with component names and values

    Returns:
        Plotly figure object
    """
    df = pd.DataFrame(list(components.items()),
                      columns=['Component', 'Minutes'])
    df = df[df['Minutes'] > 0]

    fig = px.pie(
        df,
        values='Minutes',
        names='Component',
        title='Time Distribution by Factor',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_layout(height=400)

    return fig


def create_correlation_heatmap(df: pd.DataFrame):
    """
    Create a correlation heatmap.

    Args:
        df: DataFrame with numeric columns

    Returns:
        Plotly figure object
    """
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10}
    ))

    fig.update_layout(
        title='Feature Correlation Matrix',
        height=600,
        width=600
    )

    return fig


def create_distribution_plots(df: pd.DataFrame, columns: list):
    """
    Create distribution plots for specified columns.

    Args:
        df: Input DataFrame
        columns: List of column names

    Returns:
        Plotly figure object (subplots)
    """
    n_cols = len(columns)
    n_rows = (n_cols + 1) // 2

    fig = make_subplots(
        rows=n_rows,
        cols=2,
        subplot_titles=columns
    )

    for idx, col in enumerate(columns):
        row = idx // 2 + 1
        col_pos = idx % 2 + 1

        if df[col].dtype in ['object', 'category']:
            counts = df[col].value_counts()
            fig.add_trace(
                go.Bar(x=counts.index, y=counts.values, name=col),
                row=row,
                col=col_pos
            )
        else:
            fig.add_trace(
                go.Histogram(x=df[col], name=col, nbinsx=30),
                row=row,
                col=col_pos
            )

    fig.update_layout(height=200*n_rows, showlegend=False)

    return fig


def create_time_series_plot(df: pd.DataFrame, time_col: str, value_col: str):
    """
    Create a time series line plot.

    Args:
        df: Input DataFrame
        time_col: Column name for time/x-axis
        value_col: Column name for values/y-axis

    Returns:
        Plotly figure object
    """
    grouped = df.groupby(time_col)[value_col].agg(['mean', 'std', 'count'])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped.index,
        y=grouped['mean'],
        mode='lines+markers',
        name='Average',
        line=dict(color='#1f77b4', width=2),
        fill=None
    ))

    fig.add_trace(go.Scatter(
        x=grouped.index,
        y=grouped['mean'] + grouped['std'],
        fill=None,
        mode='lines',
        line_color='rgba(0,0,0,0)',
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=grouped.index,
        y=grouped['mean'] - grouped['std'],
        fill='tonexty',
        mode='lines',
        line_color='rgba(0,0,0,0)',
        name='±1 Std Dev',
        fillcolor='rgba(31, 119, 180, 0.2)'
    ))

    fig.update_layout(
        title=f'{value_col} Over {time_col}',
        xaxis_title=time_col,
        yaxis_title=value_col,
        hovermode='x unified',
        height=400
    )

    return fig


def create_scatter_with_trendline(df: pd.DataFrame, x_col: str, y_col: str, color_col: str = None):
    """
    Create a scatter plot with trendline.

    Args:
        df: Input DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        color_col: Column for color coding

    Returns:
        Plotly figure object
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        trendline='ols',
        trendline_color_override='red',
        title=f'{y_col} vs {x_col}',
        color_continuous_scale='Viridis' if color_col else None
    )

    fig.update_layout(height=400, hovermode='closest')

    return fig


def create_box_plot(df: pd.DataFrame, x_col: str, y_col: str):
    """
    Create a box plot.

    Args:
        df: Input DataFrame
        x_col: X-axis column (categorical)
        y_col: Y-axis column (numeric)

    Returns:
        Plotly figure object
    """
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        title=f'Distribution of {y_col} by {x_col}'
    )

    fig.update_layout(height=400, showlegend=False)

    return fig


def create_violin_plot(df: pd.DataFrame, x_col: str, y_col: str):
    """
    Create a violin plot.

    Args:
        df: Input DataFrame
        x_col: X-axis column (categorical)
        y_col: Y-axis column (numeric)

    Returns:
        Plotly figure object
    """
    fig = px.violin(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        title=f'Violin Plot: {y_col} by {x_col}',
        box=True,
        points='outliers'
    )

    fig.update_layout(height=400, showlegend=False)

    return fig


def create_comparison_chart(values: dict, title: str = "Comparison"):
    """
    Create a comparison bar chart.

    Args:
        values: Dictionary of {label: value}
        title: Chart title

    Returns:
        Plotly figure object
    """
    df = pd.DataFrame(list(values.items()), columns=['Label', 'Value'])

    fig = px.bar(
        df,
        x='Label',
        y='Value',
        color='Value',
        color_continuous_scale='Viridis',
        title=title
    )

    fig.update_layout(height=400, showlegend=False)

    return fig


def create_gauge_chart(value: float, max_value: float = 100, title: str = "Gauge"):
    """
    Create a gauge chart.

    Args:
        value: Current value
        max_value: Maximum value for gauge
        title: Chart title

    Returns:
        Plotly figure object
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': max_value * 0.8},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, max_value * 0.5], 'color': "lightgray"},
                {'range': [max_value * 0.5, max_value], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))

    fig.update_layout(height=400)

    return fig
