<!-- text mirror of docs/original-instructions/Code Execution Instructions [Fall 2023].docx — edit the .docx, not this file -->

Comprehensive

Set up/Import Data

Make this file path: “drive/My Drive/ECI Research/5. Datasets/2023 Fall - Data/2019-2022 cleaned"

Make a copy of GDP_2022.csv found in Data and move to Drive

Make a copy of 2019clean.csv, 2020clean.csv, 2021clean.csv, 2022clean.csv; move to your Drive

Change main_country and comparable_countries and sdv_comparable_countries

If updating country report for 2021/2022, make sure comparable countries are same as previous version

Double-check years are correct (2019, 2022)

Import data: double-check formatting of country name and ECI/GDP dictionaries match

ECI & PCI

Run cells as is

Save the following:

2019-2022 ECI of main country and comparable countries

GDP comparison graph

Aagrate of GDP for main country and comparable countries

ECI comparison graph

ECI change of 4 countries

GDP and ECI trend for main country

Proximity, Distance, and RID

Run cells as is

Sequential Strategy

Run cells as is

SDV & SIDS

Run cells as is

After running the cell that starts with “# UPDATED - SDV for multiple countries with main_country”

Navigate to the folder icon on the left banner; download the sequential vector xls file of your 4 countries. Combine the columns into a single dataframe in excel

Add ECI for each country to bottom row

Formatting (follow image or template)

Copy your assigned country to the leftmost column

Add the 3 chosen countries to the right

Label the columns with the corresponding country name

Center the text in the first column, first row, and last row

Expand the columns so that the text does not overlap

Remove gridlines

SOI

Run as is

SOI w/ ADI

Run as is

Make sure country_list in compute_soi_adi function is updated with main country and comparable countries

Save SOI plot

Record R^2 value directly above SOI plot

Greedy Algorithm

Prep: add a folder in 5. Datasets in My Drive named New_result_update

Make sure file path is correct

Run metrics calculations as is

Run Greedy and Plot cells as is

Running greedy

Check country, end year (2022) is correct

Run 5% and dump into pickle file; check that pickle file has saved in New_result_update

Run 10% and dump into pickle file

Run 15% and dump into pickle file

Run 20% and dump into pickle file

Plot budget allocation

Check country and file paths are correct

Run cells as is

Download 2 figures

ECI growth optimization result

ECI increment

Run tableau cells as is

Download tableau [main country] 2022.xls from left hand side folder icon

Format the Excel like this and export as pdf/screenshot

Add in a line in the second row of the original ECI form Step 3a of this doc

Format the values in scientific notations and merge/center

Color the border cells dark blue and body light blue

Sensitivity

Run import packages, read data, and metrics calculations as is

Check for print statement “Sensitivity defined”

Make sure raw_matrix is defined with 2022 data

raw_matrix=read_country(root_path + '2022clean.csv')

Download positive and negative shocking plots

SDV sensitivity and contingency strategy

Add or find the cells that say sensitivity_new(raw_matrix, main_country, “High-complexity Products, root_path) and sensitivity_new(raw_matrix, main_country, "Clothing and Accessories", root_path)

Find the two .xlsx files main_countryHigh-complexity Products.xlsx and main_countryClothing and Accessories.xlsx in drive/My Drive/ECI Research/5. Datasets/2023 Fall - Data/2019-2022 cleaned

Format like below: In the first sheet, there are columns with percentages and numbers to the right. The numbers directly to the right indicate if color of the percentage column (shown below). Dark blue is positive, white is 0, and light blue is negative

Contingency

Add cell or find cont(main_country,raw_matrix, root_path)

Go to drive/My Drive/ECI Research/5. Datasets/2023 Fall - Data/2019-2022 cleaned and download main_country_contingency.xlsx

Center and bold cells like below
