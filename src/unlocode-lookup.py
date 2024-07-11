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
import requests
from bs4 import BeautifulSoup
import pandas as pd


from pathlib import Path

from support_functions import *

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

# setting up outputs directory
outputs_dir = Path.cwd().parent.joinpath("outputs")

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
# get lookup_df
try:
    # load lookup first
    unlocode_lookup_df = pd.read_csv(outputs_dir.joinpath("unlocode_lookup.csv"))
except FileNotFoundError:
    # create look up if none found
    unlocode_lookup_df = extract_and_clean_unlocde_table(
        country_codes, verify_url=verify_bool
    )

    # save to outputs
    unlocode_lookup_df.to_csv(outputs_dir.joinpath("unlocode_lookup.csv"), index=False)

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
