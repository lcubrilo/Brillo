def changed(b):
    from time import sleep
    #sleep(1)
    print("\n========\n")
    """for key in b:
        print("{} : {}".format(key, b[key]))"""
    #print(b["description"])
    print("{}: switched to {}".format(b["owner"].description, b["owner"].value))

from IPython.display import display
from ipywidgets import Checkbox

contours = ["a", 'b', 'c', 'd', 'gg', 'f']
checkboxes = []

for contour in contours:
    checkboxes.append(Checkbox(False, description=contour))

for chkBx in checkboxes:
    display(chkBx)
    chkBx.observe(changed, names=['value'])