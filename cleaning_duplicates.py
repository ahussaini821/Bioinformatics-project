import pandas as pd

def cleaningduplicates(file_path, output_filepath):

    df = pd.read_csv(file_path, sep=",")

# Notes:
# - the `subset=None` means that every column is used
#    to determine if two rows are different; to change that specify
#    the columns as an array
# - the `inplace=True` means that the data structure is changed and
#   the duplicate rows are gone
    df.drop_duplicates(subset=None, keep="first", inplace=True)

# Write the results to a different file
    df.to_csv(output_filepath, index=False)


