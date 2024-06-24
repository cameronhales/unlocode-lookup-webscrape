# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: base
#     language: python
#     name: python3
# ---

# %% [markdown]
# # UN/LOCODE Webscraper
#
# **Note** Might need to change 'verify' to False if encounter any problems (doing this is not on me).

# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup

from pathlib import Path


# %%
def extract_and_clean_unlocde_table(code_list, verify_url=True):
    # initialise empty dataframe
    lookup_df = pd.DataFrame()

    for code in code_list:
        try:
            # get html data
            url = f"https://service.unece.org/trade/locode/{code.lower()}.htm"
            html = requests.get(url, verify=verify_url).content
            soup = BeautifulSoup(html, "html.parser")

            # create dataframe for country
            df = extract_all_html_tables(soup)
            df = clean_unlocode_df(df)

            # append to main lookup
            lookup_df = pd.concat([lookup_df, df])

        except IndexError:
            print(code)

    return lookup_df


def extract_all_html_tables(soup):
    tables = soup.find_all("table")

    df = pd.DataFrame()

    for table in tables:
        table_df = html_table_to_dataframe(table)
        df = pd.concat([df, table_df], ignore_index=False)

    return df


def html_table_to_dataframe(table):

    rows = table.find_all("tr")
    data = []
    for row in rows:
        columns = row.find_all("td")
        row_data = [col.get_text(strip=True) for col in columns]
        data.append(row_data)

    df = pd.DataFrame(data)

    return df


def clean_unlocode_df(df):

    # the headers are on row 3
    df.columns = df.iloc[3]

    # only take rows after headers and first 6 columns
    df = df.iloc[4:, [1, 2, 3, 4, 5, 6]]

    # remove space in LOCODE
    df["LOCODE"] = df["LOCODE"].apply(lambda x: "".join(x.split()))

    # remove dashes and turn into a list of numbers
    df["Function"] = df["Function"].apply(lambda x: list(x.replace("-", "")))

    return df


# %% [markdown]
# __________________
# # Extracting UN-LOCODE lookup table
#
# The website urls for UN-LOCODE tables remain the same apart from the country code at the end, e.g. "https://service.unece.org/trade/locode/gb.htm", we can create a table containing LOCODEs for all countries by looping through all 2 letter country codes.
#
# We need a list of 2 letter country codes for this first though

# %%
# If you have problems accessing the websites set verify_bool to False
verify_bool = False

# %%
# grab a list of country codes
url = "https://www.iban.com/country-codes"
html = requests.get(url, verify=verify_bool).content
soup = BeautifulSoup(html, "html.parser")

country_codes_df = extract_all_html_tables(soup)

# clean the df
country_codes_df = country_codes_df.iloc[1:, [0, 1]].rename(
    columns={0: "country_name", 1: "alpha_2_code"}
)

country_codes = country_codes_df["alpha_2_code"]

# %% [markdown]
# now we have a list of country codes we can use them to create a lookup (this will take around 2.5 mins):

# %%
scrape_lookup = True

if scrape_lookup:
    unlocode_lookup_df = extract_and_clean_unlocde_table(
        country_codes, verify_url=verify_bool
    )

# %%
save_lookup = True

if save_lookup:

    # find outputs folder
    output_dir = Path.cwd().parent.joinpath("outputs")

    # save
    unlocode_lookup_df.to_csv(output_dir.joinpath("unlocode_lookup.csv"), index=False)

# %% [markdown]
# _______
# ### testing for any missing files
#
# Just to make sure

# %%
# find out what country codes not included
lookup_country_codes_set = set(unlocode_lookup_df["LOCODE"].apply(lambda x: x[:2]))
country_codes_set = set(country_codes)

print(country_codes_set.difference(lookup_country_codes_set))
