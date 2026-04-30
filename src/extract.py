from typing import Dict

import requests
from pandas import DataFrame, read_csv, read_json, to_datetime


def get_public_holidays(public_holidays_url: str, year: str) -> DataFrame:
    """Get the public holidays for the given year for Brazil.

    Args:
        public_holidays_url (str): url to the public holidays.
        year (str): The year to get the public holidays for.

    Raises:
        SystemExit: If the request fails.

    Returns:
        DataFrame: A dataframe with the public holidays.
    """
    # TODO: Implement this function.
    # You must use the requests library to get the public holidays for the given year.
    # The url is public_holidays_url/{year}/BR.
    # You must delete the columns "types" and "counties" from the dataframe.
    # You must convert the "date" column to datetime.
    # You must raise a SystemExit if the request fails. Research the raise_for_status
    # method from the requests library.
    # raise NotImplementedError   
    try:
        response = requests.get(f"{public_holidays_url}/{year}/BR")
        response.raise_for_status()  # this raises error if request fails
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise SystemExit 

    # Convert JSON to DataFrame
    data = response.json()
    df = DataFrame(data)

    # Drop unwanted columns (ignore in case they don't exist)
    df = df.drop(columns=["types", "counties"], errors="ignore")

    # Convert date column
    df["date"] = to_datetime(df["date"])

    # Save to CSV if path provided
    #if output_file:
    df.to_csv("test", index=False)

    return df




def extract(
    csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str
) -> Dict[str, DataFrame]:
    """Extract the data from the csv files and load them into the dataframes.
    Args:
        csv_folder (str): The path to the csv's folder.
        csv_table_mapping (Dict[str, str]): The mapping of the csv file names to the
        table names.
        public_holidays_url (str): The url to the public holidays.
    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the table names and values as
        the dataframes.
    """
    dataframes = {
        table_name: read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }

    holidays = get_public_holidays(public_holidays_url, "2017")

    dataframes["public_holidays"] = holidays

    return dataframes
