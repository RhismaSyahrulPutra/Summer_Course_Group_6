from flask import Flask, render_template, send_from_directory
import io
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# File paths for Jawa Barat and Jawa Timur waste data
file_path_jabar = 'dataset/Data_Timbulan_Sampah_SIPSN_KLHK_Jawa Barat.xlsx'
file_path_jatim = 'dataset/Data_Timbulan_Sampah_SIPSN_KLHK_Jawa Timur.xlsx'

# Load data for Jawa Barat
df_jabar = pd.read_excel(file_path_jabar, skiprows=1)

# Load data for Jawa Timur
df_jatim = pd.read_excel(file_path_jatim, skiprows=1)

# Combine data for both provinces
df = pd.concat([df_jabar, df_jatim])

# Calculate total annual waste generation for each province
total_waste = df.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].sum().reset_index()

# Calculate average annual waste generation for each province
average_waste = df.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].mean().reset_index()

# Assign categories based on average waste generation
categories = ['GREEN', 'ORANGE', 'RED']
average_waste['Category'] = pd.cut(average_waste['Timbulan Sampah Tahunan(ton)'], 
                                   bins=[0, 100000, 700000, float('inf')], 
                                   labels=categories)

# Directory to save plots
plot_dir = 'static/plots'
os.makedirs(plot_dir, exist_ok=True)

# Total amount of annual waste generation in each province in each year
def total_amount_each_year(df):
    grouped = df.groupby(["Tahun", "Provinsi"])["Timbulan Sampah Tahunan(ton)"].sum().reset_index()

    # Using seaborn for a colorful bar chart
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(x="Tahun", y="Timbulan Sampah Tahunan(ton)", hue="Provinsi", data=grouped, palette="Set3")

    plt.title('Total Amount of Annual Waste Generation in Each Province')
    plt.xlabel('Year')
    plt.ylabel('Total Waste Generation (ton)')
    plt.legend(title='Province', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    fig.savefig(os.path.join(plot_dir, 'total_amount_each_year.png'))
    plt.close(fig)

# Average total annual waste generation in each province for all years
def avg_total_all_years(df):
    # Grouping by province and year to calculate average total waste generation
    grouped = df.groupby(["Tahun", "Provinsi"])["Timbulan Sampah Tahunan(ton)"].mean().reset_index()

    # Using seaborn for a colorful bar chart
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(x="Tahun", y="Timbulan Sampah Tahunan(ton)", hue="Provinsi", data=grouped, palette="Set3")

    plt.title('Average Total Annual Waste Generation in Each Province')
    plt.xlabel('Year')
    plt.ylabel('Average Total Waste Generation (ton)')
    plt.legend(title='Province', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    fig.savefig(os.path.join(plot_dir, 'avg_total_all_years.png'))
    plt.close(fig)

# Province produces the most annual waste generation each year
def most_annual_province(df):
    df["Tahun"] = pd.to_numeric(df["Tahun"])

    # Group by year and province and find the province with maximum waste generation each year
    grouped = df.groupby(["Tahun", "Provinsi"])["Timbulan Sampah Tahunan(ton)"].sum().reset_index()

    max_producers = grouped.loc[grouped.groupby('Tahun')['Timbulan Sampah Tahunan(ton)'].idxmax()]

    max_producers.to_html(os.path.join(plot_dir, 'most_annual_province.html'), index=False, classes='data-table')

# Province produces the least annual waste generation each year
def least_annual_province(df):
    df["Tahun"] = pd.to_numeric(df["Tahun"])

    # Group by year and province and find the province with minimum waste generation each year
    grouped = df.groupby(["Tahun", "Provinsi"])["Timbulan Sampah Tahunan(ton)"].sum().reset_index()

    min_producers = grouped.loc[grouped.groupby('Tahun')['Timbulan Sampah Tahunan(ton)'].idxmin()]
    min_producers.to_html(os.path.join(plot_dir, 'least_annual_province.html'), index=False, classes='data-table')

# Total annual amount of waste in each province from year to year
def total_annual_amount(df):
    avg_df = df.groupby(["Tahun", "Provinsi"])["Timbulan Sampah Tahunan(ton)"].sum().reset_index()

    # Create line chart
    fig = plt.figure(figsize=(10, 6))
    for provinsi in avg_df["Provinsi"].unique():
        subset = avg_df[avg_df["Provinsi"] == provinsi]
        plt.plot(subset["Tahun"], subset["Timbulan Sampah Tahunan(ton)"], marker='o', label=provinsi)

    plt.title('Total Annual Amount of Waste in Each Province from Year to Year')
    plt.xlabel('Year')
    plt.ylabel('Total Waste Generation (ton)')
    plt.legend()
    plt.grid(True)
    plt.xticks(subset["Tahun"].unique())
    plt.tight_layout()
    fig.savefig(os.path.join(plot_dir, 'total_annual_amount.png'))
    plt.close(fig)

# Average incidence annual waste in each province for the entire year
def plot_categorized_provinces(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = {'GREEN': 'green', 'ORANGE': 'orange', 'RED': 'red'}
    categories = df['Category'].value_counts().index
    counts = df['Category'].value_counts().values
    ax.bar(categories, counts, color=[colors[cat] for cat in categories])
    ax.set_xlabel('Category')
    ax.set_ylabel('Number of Provinces')
    ax.set_title('Categorization of Average Annual Waste Generation in Jawa Barat and Jawa Timur')
    plt.tight_layout()
    fig.savefig(os.path.join(plot_dir, 'categorized_provinces.png'))
    plt.close(fig)

# Pre-generate plots
total_amount_each_year(df)
avg_total_all_years(df)
most_annual_province(df)
least_annual_province(df)
total_annual_amount(df)
plot_categorized_provinces(average_waste)

# Flask routes
@app.route('/')
def home():
    with open(os.path.join(plot_dir, 'most_annual_province.html')) as f:
        most_annual_html = f.read()
    with open(os.path.join(plot_dir, 'least_annual_province.html')) as f:
        least_annual_html = f.read()
    return render_template('index.html', most_annual=most_annual_html, least_annual=least_annual_html)

@app.route('/plots/<filename>')
def plot(filename):
    return send_from_directory(plot_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
