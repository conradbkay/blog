import plotly.graph_objects as go
import pandas as pd
import numpy as np

data_dict = {
    'Model': [
        "Claude 3.7 Sonnet", "Claude 3.7 Sonnet",
        "ChatGPT (o4-mini)", "ChatGPT (o4-mini)",
        "Gemini 2.5 Pro", "Gemini 2.5 Pro", "Gemini 2.5 Pro", "Gemini 2.5 Pro"
    ],
    'Comic_Years': [1965, 1963, 1965, 1963, 1944, 1959, 2006, 1988],
    'Actual_Grades': [9.4, 9.4, 9.4, 9.4, 9.8, 9.4, 6.0, 4.0],
    'Guessed_Grades_Str': [
        "6.0", "6.0", "7.5", "5.5-6.0", "5.0", "4.5-5.5", "9.6", "7.0-7.5"
    ]
}

# 1. Create DataFrame & Process Data
df = pd.DataFrame(data_dict)

def parse_guessed_grade(grade_str):
    if isinstance(grade_str, (int, float)):
        return float(grade_str)
    grade_str = str(grade_str).strip()
    if '-' in grade_str:
        low, high = map(float, grade_str.split('-'))
        return (low + high) / 2
    else:
        return float(grade_str)

df['Guessed_Grade_Numeric'] = df['Guessed_Grades_Str'].apply(parse_guessed_grade)
# Calculate difference. Rounding for display happens in hovertemplate.
df['Difference'] = df['Actual_Grades'] - df['Guessed_Grade_Numeric']

# Create a more detailed label for hover, if needed, or just use individual fields.
# For this iteration, we'll build the hover text from individual customdata fields.

# 2. Determine Colors for Models
model_colors = {
    "Claude 3.7 Sonnet": "rgb(23, 190, 207)",  # Teal
    "ChatGPT (o4-mini)": "rgb(31, 119, 180)", # Blue
    "Gemini 2.5 Pro": "rgb(255, 127, 14)"     # Orange
}
df['Model_Color'] = df['Model'].map(model_colors)

# 3. Create the Plot
fig = go.Figure()

# X-values will be the simple index of the DataFrame rows
x_values = df.index
# X-axis tick labels will be the Comic Years
x_tick_labels = df['Comic_Years'].astype(str)

# Add lines connecting Actual to Guessed for each trial
for i, row in df.iterrows():
    fig.add_shape(
        type="line",
        x0=i, y0=row['Actual_Grades'],
        x1=i, y1=row['Guessed_Grade_Numeric'],
        line=dict(
            color=row['Model_Color'], # Line color by model
            width=2,
        ),
        opacity=0.7
    )

# Add Scatter trace for Actual Grades
fig.add_trace(go.Scatter(
    x=x_values,
    y=df['Actual_Grades'],
    mode='markers',
    marker=dict(
        color=df['Model_Color'],
        size=10,
        symbol='circle',
        line=dict(width=1.5, color='DarkSlateGrey')
    ),
    name='Actual Grade', # Legend entry for this marker type
    customdata=df[['Model', 'Comic_Years', 'Guessed_Grades_Str', 'Guessed_Grade_Numeric', 'Difference']],
    hovertemplate=(
        "<b>Model: %{customdata[0]}</b><br>"
        "Comic Year: %{customdata[1]}<br>"
        "---<br>"
        "<b>Actual Grade: %{y:.1f}</b><br>"
    )
))

# Add Scatter trace for Guessed Grades
fig.add_trace(go.Scatter(
    x=x_values,
    y=df['Guessed_Grade_Numeric'],
    mode='markers',
    marker=dict(
        color=df['Model_Color'],
        size=10,
        symbol="x",
        line=dict(width=1.5, color='DarkSlateGrey')
    ),
    name='Guessed Grade', # Legend entry for this marker type
    customdata=df[['Model', 'Comic_Years', 'Actual_Grades', 'Guessed_Grades_Str', 'Difference']],
    hovertemplate=(
        "%{customdata[3]}<br>"
    )
))

# Add dummy traces for a clean model legend
legend_markers_added = set()
for i, row in df.iterrows():
    if row['Model'] not in legend_markers_added:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(color=row['Model_Color'], size=10, symbol='square'),
            showlegend=True,
            legendgroup="models",
            name=row['Model']
        ))
        legend_markers_added.add(row['Model'])


# 4. Customize Layout
min_grade = df[['Actual_Grades', 'Guessed_Grade_Numeric']].min().min()
max_grade = df[['Actual_Grades', 'Guessed_Grade_Numeric']].max().max()

fig.update_layout(
    xaxis_title="Sample Year", # Updated X-axis title
    yaxis_title="Grade",
    legend_title_text="Legend",
    height=300,
    width=max(600, 80 * len(df)),
    template="plotly_white",
    xaxis=dict(
        tickmode='array',
        tickvals=x_values,
        ticktext=x_tick_labels, # Use just the years for tick labels
        tickangle=0 # If years are short enough, 0 is fine. Adjust if needed.
    ),
    yaxis=dict(
        range=[min_grade - 0.5, 10],
        dtick=1.0
    ),
    hovermode="x unified" # Shows hover info for both actual & guessed at that x-index
)

fig.show()