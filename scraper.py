import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def plotdataset():
    aitools_df = pd.read_excel('output.xlsx')

    # Data cleaning: correct some typos
    aitools_df.loc[aitools_df['Pricing'] == 'FreeFreemium', 'Pricing'] = 'Freemium'
    # Group the data by both 'Category' and 'Pricing' and count the occurrences
    category_pricing_counts = aitools_df.groupby(['Category', 'Pricing']).size().unstack()

    # Sort the categories by the total count in descending order
    category_pricing_counts['Total'] = category_pricing_counts.sum(axis=1)
    category_pricing_counts = category_pricing_counts.sort_values(by='Total', ascending=False)
    category_pricing_counts = category_pricing_counts.drop(columns='Total')

    # Create the stacked bar plot
    category_pricing_counts.plot(kind='bar', stacked=True)
    plt.title('Relationship between Category and Pricing')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility
    plt.legend(title='Pricing', loc='upper right')  # Add a legend
    plt.show()


def main():
    # Initializations
    URL = "https://www.aitoolkit.org/aitools"
    next_page = '?851fd7dc_page=1'
    aitools_name = []
    aitools_category = []
    aitools_pricing = []
    aitools_link = []
    aitools_description = []

    # Scrape the pages iteratively
    while next_page:
        url_adjusted = f'{URL}{next_page}'
        html = requests.get(url_adjusted)
        soup = BeautifulSoup(html.content, 'html.parser')

        results = soup.find_all("div",id="w-node-_8ab1bc50-85e4-aaf7-00a4-b60b851fd7de-07f9a9de")

        for result in results:
            title_element = result.find("h1", class_="combine-heading-style-h5-2")
            category_element = result.find("div", class_="text-block-13")
            pricing_element = result.find("div", class_="text-block-10")
            link_element = result.find("a", class_="a-button-primary-copy w-inline-block")
            description_element = result.find("div", class_="combine-text-size-small-2 combine-text-color-grey")
            aitools_name.append(title_element.text)
            aitools_category.append(category_element.text)
            aitools_pricing.append(pricing_element.text)
            aitools_link.append(link_element["href"])
            aitools_description.append(description_element.text) if description_element else np.nan
        
        next_button = soup.find('a', {'class': 'w-pagination-next f-button-primary-2'})
        next_page = next_button.get('href') if next_button else None

    # Populate the dataframe with the scraped data
    data = [aitools_name, aitools_category, aitools_pricing, aitools_link, aitools_description]
    aitools_df = pd.DataFrame(data).T
    aitools_df.columns = ["Name","Category","Pricing","Link","Description"]
    aitools_df.to_excel("output.xlsx",index=False)

if __name__ == "__main__":
    main()