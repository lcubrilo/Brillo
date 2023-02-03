# First steps with Brillo (Copy)
### [Made by Luka Čubrilo with Scribe](https://scribehow.com/shared/First_steps_with_Brillo_Copy__rJ1umJPwT0mfkvTAks2i5w)


# Let's start by opening up the software

Open the **Brillo** software<br>  
You can press <kbd>ctrl</kbd> <kbd>+</kbd> to zoom in / increase font size as much as you need.  
Likewise, you can press <kbd>ctrl</kbd> <kbd>-</kbd> to zoom out.

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/f804d773-b423-4766-9429-775ea1207c1f/stack_animation.webp)

# Loading your data

Click "Browse directories" to input your files  
A popup menu appears. It shows your files and folders. Navigate through your folders until you find the desired data.  
For example, I have data of several people, let's open Antonio's file.  
Note: For aixACCT, only [.dat] files will work. Make sure you exported in this format.  
Select the files you want.

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/803bd697-2d6e-4df5-9c11-902149019153/stack_animation.webp)

Now the right side of the app is available to you, including the following options:
   1. Show table data
   2. Edit table data
   3. Plotting data
   4. Macros

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/9a01d3f0-85da-4575-a848-f38f5c096506/File.jpeg?tl_px=950,0&amp;br_px=1696,420&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,28)

**Note:** You will be able to use the right portion of the program only if you actually loaded some files.

Great! You have now successfully loaded your files. If you want to load different files, reopen the program.

You can also load multiple files from the same folder.



<br>

# Taking our first steps with the data

## 1. Tabular data, columns

5. On the left side you have a tree-view of all of the loaded files, as well as each of the tables within this file.

In this case our file is called <kbd>BFO_BT_react_sint_1040_6h_P_E.dat</kbd>.
Within it we have 9 tables, each named according to the range of electric field applied to the sample.
In a general case (let's say loading data from a software different to aixACCT) tables will have a much more generic and non-descriptive names.
As you are clicking through the tables on the left - you will see its data on the right.

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/634c2723-5ef3-4900-83ef-b9d5ce12cee4/stack_animation.webp)

6. Scroll left-right to see all of the columns.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/02f1b1d2-86b2-4d8b-bbb7-47753b35c86c/File.jpeg?tl_px=641,743&amp;br_px=1387,1163&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,248)

7. Also note that pre-table constants will show up above (in the case of aixACCT it will only read <kbd>area</kbd> and <kbd>thickness</kbd>, but you can always add your own by clicking the <kbd>+</kbd> button next to them)

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/3a9d7208-241a-4e45-a47f-ffcc615ae686/File.jpeg?tl_px=0,146&amp;br_px=746,566&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=-580,139)

## 2. Constant data (pre-table data)

None. Keep in mind - the constants apply to exactly one table each.

In the case of aixACCT they are automatically loaded from the pre-table section of the files.

8. You can change the unit of this constant across all tables by clicking on the current unit.
This shows a dropdown menu of all possible prefixes (from Terra to Nano)
It is able to recognize this unit (area) is squared (denoted by just a '2' at the end) and will properly convert the unit. 
It is also able to recognize cubed, all the way to the power of 9 (single-digit powers)
After selecting cm^2 - the value for <kbd>area</kbd> constant updates across the entire dataset (all tables of all files) to this unit
You can change the units as much as you want.
The values update once more.
You can do the same with the thickness.
Let's change the unit to <kbd>cm</kbd>.

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/1ae449ce-5997-4a0b-9715-775832f280fe/stack_animation.webp)

# Editing your table data

9. After we played around with everything <kbd>show table data</kbd> has to offer - let's move onto <kbd>edit table data</kbd>

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/5752bc5d-b627-4829-b416-025104956ec9/File.jpeg?tl_px=926,0&amp;br_px=1672,420&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,28)

## 1. Deleting columns

10. One of the first things you can do is to unselect any number of these columns. Once you're satisfied with your final set of unselected columns, proceed to the next step.
In this case we only unselected CH3, as this column is entirely filled with zeros and is useless to us.
Now we can click the trash bin button <kbd>"🗑"</kbd> to delete the columns we unselected.

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/b25db521-be2a-4cc2-9868-2932069c6d32/stack_animation.webp)

11. This notification explains that the only way to reverse this deletion is to reverse all changes you made to your data (by reloading the files from scratch).

So think twice, delete once.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/187d45d7-901b-4ea6-a8bf-3b3ef9682f72/File.jpeg?tl_px=1663,446&amp;br_px=2409,866&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,139)

12. Let's go to <kbd>"Show table data"</kbd> to see if it has truly been deleted.
Select any table on the left to refresh the table data.

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/5d46a5f0-0a2e-4723-8c8e-6c07920f6656/stack_animation.webp)

13. As we can see -  the <kbd>CH3 [V] </kbd> column is no more.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/169539c2-1226-4db9-ac39-53a3bb56ca4f/File.jpeg?tl_px=1080,0&amp;br_px=1826,420&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,29)

## 2. Creating new columns

14. We can do other things with <kbd>Edit table data</kbd> as well, let's open it back up.
We can <kbd>Create new columns</kbd> from existing columns in our data.

First, select your input column:

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/518779dc-21a4-4202-8066-da4547119fc6/stack_animation.webp)

15. We will be offered to chose from any remaining columns in our dataset. Let's select "Time [s]"

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/da98c36f-57aa-458a-92e6-7e410b9de430/File.jpeg?tl_px=1022,586&amp;br_px=1768,1006&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,139)

### Operation 1: Convert unit

16. Now we can choose our operation.
Bottom 4 options transform the column data using one of the constants mentioned previously. 

Top 4 do not need any constants and can perform directly with the input column.
Let's convert the unit of our Time [s] column to miliseconds, since the values are very small.
Let's type "Time [ms]" as the new of our newly-outputted column
Now, we can name the column any way we want, using alphanumerical characters...
...the only rule is to end with square brackets.

Inside of them, clearly say the prefix of the unit we want, and keep the base unit. ("[km]" becomes "[cm]" etc)
So for miliseconds we will type "[ms]" to inform the program to multiply all values by 1000.
Alright, we have set up all of the options within the <kbd>Create new columns</kbd> menu.

When you're satisfied with your choices, click "Execute edit"

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/9b47ed3e-1de5-4310-a0fb-6dbb7ef4df2d/stack_animation.webp)

17. Click on <kbd>Show table data</kbd> to see this new column pop up.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/0e44f730-aecb-4c3f-aa46-241e9a4b4380/File.jpeg?tl_px=815,0&amp;br_px=1561,420&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,16)

18. Select any table to refresh the table view.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/a7141053-3ce6-42fb-bf7f-e4043ff988d4/File.jpeg?tl_px=205,110&amp;br_px=951,530&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,139)

19. Scroll all the way to the right to reveal it.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/ba0fa252-255a-4637-aaf6-b13e1243c039/File.jpeg?tl_px=1095,1020&amp;br_px=1841,1440&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,183)

None. The newest columns always show up on the far right.

20. We now have a new column that shows time in miliseconds :)

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/620a512d-c686-4d58-bc59-bbf2b7b30952/File.jpeg?tl_px=1813,20&amp;br_px=2559,440&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=470,139)

### Operation 2: Inverse

21. Let's try out another operation of <kbd>Edit table data</kbd>

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/53c637d0-82eb-46da-a37c-8ea9d5002087/File.jpeg?tl_px=950,0&amp;br_px=1696,420&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,23)

22. Select a new operation.
Let's try the inverse value (1 divided by input)
Let's give this column a reasonable name.
Physically, this would correspond to some kind of "Frequency [Hz]".
Let's "Execute edit"

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/b7892261-f7b2-4808-ad99-dba1c5d69ab7/stack_animation.webp)

23. Check if this column showed up in <kbd>Show table data</kbd>

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/15479bd2-8b41-4aa0-9fcc-bcb8b212560f/File.jpeg?tl_px=806,0&amp;br_px=1552,420&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,14)

24. Select any table to refresh.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/65e4c18f-0b60-4764-b89f-b44064f22fe8/File.jpeg?tl_px=131,173&amp;br_px=877,593&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,139)

25. Scroll all the way to the right

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/e6f2d1ed-af2a-459c-85b2-88bce1191b7f/File.jpeg?tl_px=875,1020&amp;br_px=1621,1440&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,181)

26. Here is our frequency! Note "NaN", meaning "not a number" since we tried to divide by 0; an undefined operation.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/102887ad-7ae9-4638-908e-5b7cbfc6f7ac/File.jpeg?tl_px=1813,21&amp;br_px=2559,441&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=433,139)

None. NaNs can easily cause problems in any dataset and with any software. 

At best, they will slow a software down. At worst, it will crash it.

Generally try to minimize how much they appear in your data.

None. Same goes with any special symbols, such as ° for degrees etc.

My program tries to erase them anywhere it sees them, but still try to avoid them.

### Operation 3: Squaring a column

27. Let's try another operation.

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2023-02-02/d340df2d-cfc7-4271-89ab-42d37abd4eab/File.jpeg?tl_px=939,0&amp;br_px=1685,420&amp;sharp=0.8&amp;width=560&amp;wat_scale=50&amp;wat=1&amp;wat_opacity=0.7&amp;wat_gravity=northwest&amp;wat_url=https://colony-labs-public.s3.us-east-2.amazonaws.com/images/watermarks/watermark_default.png&amp;wat_pad=262,23)

### Operation 4: Square root

28. Select a new operation.
Let's take the square of an input column.
Physically, it doesn't make much sense to square the time...

There isn't a great choice to name the output column, so for demonstration purposes I will write a random name.
Let's call it "Time_squared [s2]"
If you have squared units, make sure to write the 2 in the square brackets, so that unit conversions will work for that column.
Click "Execute edit"
Let's try another operation.
Square root the time.
Again, not much physical sense in this specific case. We can name the output column anything.
Here we named it "Time_rooted [s0.5]"
The unit conversions will not work properly for fractional exponents (like 0.5 for square root)

Avoid if at all possible.
Click "Execute edit"
That concludes our constant-less operations.
We will cover the remaining operations in the next tutorial.

![](https://colony-recorder.s3.amazonaws.com/files/2023-02-02/514ebb69-e372-497e-aaf5-022d3ed7ae9a/stack_animation.webp)
### [Made with Scribe](https://scribehow.com/shared/First_steps_with_Brillo_Copy__rJ1umJPwT0mfkvTAks2i5w)


