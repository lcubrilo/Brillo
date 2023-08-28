def are_adjacent_integers(df):
    """
    Checks if the rows/indeces in the DataFrame are adjacent.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        tuple: A boolean value indicating if the rows are adjacent, and an integer representing the index where
            the interruption happened
    """
    if not df.empty:
        prevIndex = df.index[0]
        for index in df.index[1:]:
            if index - prevIndex != 1:
                return False, index
            prevIndex = index

    return True, -1

def chop_up_to_be_adjacent(df):
    """
    Splits the DataFrame into segments of adjacent integers (for now - difference of precisely one - this could be modified in the future) in the specified column (for example the first one being indeces).
    
    This is useful for detecting and handling gaps in a column of integers, especially after intentionally removing sections of rows (e.g., via removeMinMax), to ensure that the remaining segments maintain adjacency.

    Args:
        df (pandas.DataFrame): The DataFrame to be chopped, potentially with missing sections.
        columnName (str): The name of the column with integers for adjacency check.

    Returns:
        list: A list of DataFrames, each containing a segment of adjacent integers, preserving continuity.

    Example:
        df = pd.DataFrame({'A': [1, 2, 4, 5, 7]})
        segments = chop_up_to_be_adjacent(df, 'A')  
        # This returns three DataFrames with adjacent integers
        # [[1,2], [4,5], [7]]
    """
    retVal = []
    df2 = df
    boolVal, problemIndex = are_adjacent_integers(df2)
    while not boolVal:
        if df2.empty:
            break
        first, second = df2.loc[:problemIndex-1], df2.loc[problemIndex:]
        retVal.append(first)
        df2 = second
        boolVal, problemIndex = are_adjacent_integers(df2)
    if not df2.empty:
        retVal.append(df2)
    return retVal

import pandas as pd

# Create a DataFrame with a non-continuous index and a column 'A'
df = pd.DataFrame({'A': [10, 20, 30, 40, 50, 60, 70]}, index=[0, 1, 3, 4, 6, 7, 9])

# Chop up the DataFrame into segments where the index is continuous
segments = chop_up_to_be_adjacent(df)

# Print the chopped-up segments
for i, segment in enumerate(segments):
    print(f"Segment {i + 1}:")
    print(segment)
