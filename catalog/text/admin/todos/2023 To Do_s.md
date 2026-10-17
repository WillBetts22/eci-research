<!-- text mirror of admin/todos/2023 To Do_s.docx — edit the .docx, not this file -->

Code Cleanup To Do

First, new code files are located here. They are named in the order that you should run them. Do NOT modify the main version until you have tested it on your end and got a confirmation from others on the team.

To-Do Items we need to address by Sunday:

Main idea: make the code more user-friendly, readable, and efficient

0. General:

Each code file needs to have a description on top briefly explaining what it does and what it produces

ex. “It takes in and cleans GDP and __ files. Then, it outputs graphs for GDP and ECI for a specific country, and  GDP and ECI graphs for the main country and the comparable ones, …”

Identify any irrelevant parts of the code (but do NOT delete them. Leave a comment #TO FIX or flag & group it otherwise )

consolidate old/unused code

Sections: each code needs to be split into clear sections and subsections for easier navigation by topic

1. Datasets:

Fix any mixed matches in country’s names between the ECI and GDP dicts (easier & better is to do country names’ cleanups in the initial datasets)

Data Cleanup: if a piece of data for the country is missing, you want to do that fixing at the top of the code

Add file reading into a loop that is parametrized by years:

You might need to re-upload data for 2013-2018 into folders

Make sure you are able to read data from 2013-2018 and 2019-2021 together and separately (i.e. as a user, I only want to provide start and end year. You should handle any cleanups that are currently in the code or different ways of reading the data)

Make sure you make it is easy to be able to add/incorporate more years of analysis if needed

Same applies to paths to folders

2. Make all output automatically exportable / saved on the left menu under “files”:

1. Any relevant (text) output should be saved by printing output into a file and into command lines:

with open('my_file.txt', 'w')

Because it can be difficult to look for which part of the output is relevant when there are progress updates; clearly outline which part of the output should be put into the report

E.g., Greedy code in 1. (below)  - refer to exporting all text output into a file

2. Tables export

(as you’ll see in some reports, there is more information on other regions’ countries’ performances) - make sure to parametrize them as well! Give users a choice of which tables to produce for what metrics - see section 3.

#Any tables should be saved using something like:

data.to_csv('YOUR_FILE/HERE.csv')

3. Graphs export

Any graphs should be saved with files on the left as well (one of the codes has an example)

Fix graph outputs: in particular, ECI and GDP graphs have a weird x-axis with ticks

3. Parametrizing any variable names:

See file exporting and path by years above

Anything that needs manual changes should only be changed at the top of the code with a comment #TO DO and what exactly is needed to be done.

Pay attention to paths to the files, anything with “main_country”, any tables that appear in some reports

Make variable names clearer/more accurate/intuitive and include a brief description

For instance:

4. Code-specific:

Fix SOI code so it doesn’t throw an error at the very end

Fix SDV code so the SDV ECI table works

Country names

Export graphs

Modifying paths,

Adding for loops

Changing variable names

Questions:

Fall 23 edits:

SOI:

Soi_adi is defaulting to three countries, needs to be the entire list

Errors for regression

Cannot get r^2

Greedy:

**Table 1**

| 11/10/2023 Updates  sdv_comparable_countries that are not working (so far): Ethiopia, Burkina Faso not working - check data  Allison: csv export - TBU Daniel: didn’t have a defined task, so ran code for Niger - problems with opening ECI files (?) - increment graph / tick marks?  Transfer all edits Navia - finalize SDV Allison - finalize csv export Daniel - Fix graph outputs: in particular, ECI and GDP graphs have a weird x-axis with ticks Jane - finalize data clean up  Ryo - ???   10/20/2023 To Do’s:  Jane - data clean up (checking for 0’s in data + making sure the names of the countries are the same across data sets) Navia - SDV / eci _19to21_dict fix + fix SDV output tables (sorted properly, ECI at the bottom) Allison - output for data, charts, graphs Daniel & Ryo - each identify a problem in the code to fix before the next meeting  10/6/2023 Updates  Greedy code: not showing |
|---|
