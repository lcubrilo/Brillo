import pandas as pd

# Create a sample DataFrame
df = pd.DataFrame({'Score': [[50, 60], [70, 80], [90, 100]], 'Grade': ['A', 'B', 'C']})

# Flatten the 'Score' column using ravel()
df['Score'] = df['Score'].ravel()

# Now the condition will return a single-dimensional key
subset = df.loc[df['Score'] > 50]
