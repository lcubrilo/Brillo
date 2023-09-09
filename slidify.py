import nbformat

# Load the notebook
notebook_path = 'ProbostatShowcaseNotebook.ipynb'
with open(notebook_path, 'r') as f:
    notebook_content = f.read()

# Parse the notebook content
notebook = nbformat.reads(notebook_content, as_version=4)

# Initialize flags and counters
new_slide = False
code_cell_count = 0

# Iterate through cells to set slide types
for cell in notebook.cells:
    if cell.cell_type == 'markdown':
        contains_level2 = False
        for line in cell.source.split("\n"):
            if line.startswith('## ') or line.startswith('# '):
                contains_level2 = True
                break
        if contains_level2:
            cell.metadata.slideshow.slide_type = 'slide'
            new_slide = True
        else:
            cell.metadata.slideshow.slide_type = 'subslide'
    elif cell.cell_type == 'code':
        if new_slide and code_cell_count == 0:
            cell.metadata.slideshow.slide_type = 'fragment'
            code_cell_count += 1
        else:
            cell.metadata.slideshow.slide_type = 'subslide'
        
        if new_slide and code_cell_count > 0:
            new_slide = False
            code_cell_count = 0

# Write the modified notebook back to disk
with open(notebook_path, 'w') as f:
    nbformat.write(notebook, f)
