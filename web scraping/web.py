
##########  RENAMING FILE INPUT VALUES   ###############
import pandas as pd

# Load the CSV file into a DataFrame
csv_file = "Books.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Change the column name from "In-stock" to "instock"
df.rename(columns={"In-stock": "instock"}, inplace=True)
df.rename(columns={"Star Rating": "StarRating"}, inplace=True)
df.rename(columns={"Image URL": "Imageurl"}, inplace=True)

# Reset the index and drop the old index
df.reset_index(drop=True, inplace=True)

# Save the corrected DataFrame back to a CSV file
corrected_csv_file = "newoutput.csv"  # Replace with the desired output file path
df.to_csv(corrected_csv_file, index=False)

print("CSV file index corrected and 'In-stock' renamed to 'instock', saved as", corrected_csv_file)