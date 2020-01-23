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

def clean_isoforms():
    df = pd.read_csv("names_final.csv")

    for index, row in df.iterrows():

        if "-" in row["Main protein name"]:
            df.drop(index, inplace=True)

    df.to_csv("test.csv", index=False)


# cleaningduplicates("characteristics_final.csv", "characteristics_final.csv")
# cleaningduplicates("domains_final.csv", "domains_final.csv")
# cleaningduplicates("kinase target final.csv", "kinase target final.csv")
# cleaningduplicates("names_final.csv", "names_final.csv")

clean_isoforms()
