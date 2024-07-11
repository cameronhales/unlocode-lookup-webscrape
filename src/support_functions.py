import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract_and_clean_unlocde_table(code_list, verify_url=True):
    """Extracts and prepares a UNLOCODE lookup table, using the given ISO-AlPHA 2 country codes.

    Args:
        code_list (lst): list containing the country codes from desired countries
        verify_url (bool, optional): will verify url if True. Defaults to True.

    Returns:
        DataFrame: A lookup df of UNLOCODES for all countries
    """
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
    """Will extract all html tables found within a BeautifulSoup Object

    Args:
        soup (???): BeautifulSoup object from html webpage

    Returns:
        DataFrame: DataFrame of all tables concatenated together from given webpage
    """
    tables = soup.find_all("table")

    df = pd.DataFrame()

    for table in tables:
        table_df = html_table_to_dataframe(table)
        df = pd.concat([df, table_df], ignore_index=False)

    return df


def html_table_to_dataframe(table):
    """Will convert from a html table to pandas DataFrame

    Args:
        table (???): html table

    Returns:
        DataFrame: pandas DataFrame
    """
    rows = table.find_all("tr")
    data = []
    for row in rows:
        columns = row.find_all("td")
        row_data = [col.get_text(strip=True) for col in columns]
        data.append(row_data)

    df = pd.DataFrame(data)

    return df


def clean_unlocode_df(df):
    """applies basic cleaning steps to the UNLOCODE table, will remove certain columns and clean the text a bit

    Args:
        df (DataFrame): UNLOCDE dataframe as seen on the UNCE website

    Returns:
        DataFrame: Dataframe with basic cleaning steps applied
    """

    # the headers are on row 3
    df.columns = df.iloc[3]

    # only take rows after headers and first 6 columns
    df = df.iloc[4:, [1, 2, 3, 4, 5, 6]]

    # remove space in LOCODE
    df["LOCODE"] = df["LOCODE"].apply(lambda x: "".join(x.split()))

    # remove dashes and turn into a list of numbers
    df["Function"] = df["Function"].apply(lambda x: list(x.replace("-", "")))

    return df
