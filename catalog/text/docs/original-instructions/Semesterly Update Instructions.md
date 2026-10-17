<!-- text mirror of docs/original-instructions/Semesterly Update Instructions.docx — edit the .docx, not this file -->

## Semesterly Update Instructions and Notes

### Create folder for semester: “Fall 2024 - Datasets”

### Inside, create “raw_data” and “2019-x cleaned” where x is the new year. For example “2019-2023 cleaned” in “Fall 2024 - Datasets”

### Run data upload:

Write instructions here

### Make sure the following datasets exist:

“Xclean.csv” where X are the years 2019 to the most recent year. For example, in 2024 we will have

2019clean.csv

2020clean.csv

2021clean.csv

2022clean.csv

2023clean.csv

“GDP_X.csv” where X is the most recent year. In 2024, we have “GDP_2023.csv”

### Update code

Let X be the most recent year. Consistent with above examples, let X = 2023

Let # be the index of the most recent year. In this example, # = 5

#### Cells to Update:

1:

Update variables:

folder

data_folder

GDP4_path

sdv_path

End_year

5:

add line:

df# = pd.read_csv(path_to_data data_folder+'/Xclean.csv')

6:

Update variables:

Dataframes

Add Variables:

matrix#

10

Update variables

gdp_df_filtered

print statement

18

Add variables:

eci_X

19

Update:

eci_list

Note: variable name here is called eci_19to21_dict. This might be confusing but there’s no need to update the name

49

Update:

File path, ‘GDP_X.csv’
