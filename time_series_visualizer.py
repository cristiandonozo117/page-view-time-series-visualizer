import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',
                 index_col='date',
                 parse_dates=True)

# Clean data
mask = (df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))
df = df.loc[mask]

def draw_line_plot():
    # Draw line plot
    fig, axes = plt.subplots(figsize=(16,6))
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    axes.plot(df.index, df['value'])
    axes.grid(True)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    # Creating columns year, month and day by spliting date column
    df_bar.reset_index(inplace=True)
    df_bar['year'] = [d.year for d in df_bar['date']]
    df_bar['month'] = [d.month_name() for d in df_bar['date']] 
    df_bar['day'] = [d.day for d in df_bar['date']]

    # Draw bar plot
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    fig, ax = plt.subplots(figsize=(10,10))
    width = 0.05
    edge = -(len(months)/2)*width
    for m in months:
        df_bar_months = df_bar.loc[df_bar['month'] == m]
        monthly_avg_per_year = df_bar_months.groupby('year')['value'].mean()
        bar = ax.bar(monthly_avg_per_year.index + edge, monthly_avg_per_year, width, label=m, linewidth=0)
        edge+=width
    # linewidth=0 para que no hayan bordes o espaciones entre barras, y así queden pegadas una a la otra
    ax.set_xticks(df_bar['year'].unique()) # Cambiamos los valores en el eje x para solo mostrar los años
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(loc='upper left')
    ax.get_legend().set_title('Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(21,8))
    # First boxplot
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    sns.boxplot(data=df_box, x='year', y='value', hue='year',
                ax=axes[0], palette='tab10',
                fliersize=2)
    # Second boxplot
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    sns.boxplot(data=df_box, x='month', y='value', hue='month',
                ax=axes[1],
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                fliersize=2)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
