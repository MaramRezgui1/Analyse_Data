# -*- coding: utf-8 -*-
"""data_cleaner.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DAhLscmRe154IC4LcaQq3jZ40tzIplwS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataCleaner:
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        # Remove duplicates
        self.df.drop_duplicates(inplace=True)

        # Handle missing values
        self.df.fillna(self.df.mean(), inplace=True)

        # Convert categorical variables to dummy variables
        self.df = pd.get_dummies(self.df, drop_first=True)

        return self.df

    def calculate_churn_rate(self):
        churned_count = (self.df['Exited'] == 1).sum()
        total_customers = self.df.shape[0]
        churn_rate = (churned_count / total_customers) * 100
        print(f"Churn rate: {churn_rate:.2f}%")

        return churn_rate

    def plot_churn_pie_chart(self):
        churned_count = (self.df['Exited'] == 1).sum()
        total_customers = self.df.shape[0]

        labels = ['Churned Customers', 'Retained Customers']
        sizes = [churned_count, total_customers - churned_count]
        colors = ['salmon', 'teal']

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors)
        plt.title(f'Churn Rate: {self.calculate_churn_rate():.2f}%')
        plt.axis('equal')
        plt.show()

    def plot_churn_by_gender(self):
        churn_count_by_gender = self.df[self.df['Exited'] == 1]['Gender'].value_counts()
        custom_palette = ["coral", "seagreen"]

        plt.figure(figsize=(8, 8))
        plt.pie(churn_count_by_gender, labels=churn_count_by_gender.index, colors=custom_palette,
                autopct='%1.1f%%', startangle=140)
        plt.title('Proportion of Churned Customers by Gender')
        plt.show()

    def plot_churn_by_age(self):
        age_bins = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 100]
        labels = ['15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65', '65-70', '70+']
        self.df['Age_Group'] = pd.cut(self.df['Age'], bins=age_bins, labels=labels, right=False)
        churn_by_age = self.df.groupby('Age_Group')['Exited'].mean() * 100
        churn_by_age.index = labels

        plt.figure(figsize=(12, 6))
        palette = sns.color_palette("viridis", len(labels))
        bar_width = 0.8

        for i, label in enumerate(labels):
            plt.bar(label, churn_by_age[label], color=palette[i], width=bar_width)

        plt.title('Churn Rate by Age Group')
        plt.xlabel('Age Group')
        plt.ylabel('Churn Rate (%)')
        plt.show()

    def save_cleaned_data(self, file_path):
        self.df.to_csv(file_path, index=False)
        print(f"Cleaned data saved to {file_path}")