# FileDataRecon
Purpose: Utility to compare two .csv flat files
Core Program Name: compare_two_csv_files

Limitations:
    1. Restricted to .csv file format
    2. Names of the source file and target file should be the same
    3. Files should be in flat structure: measure should be in just 1 column
    4. Measure file/column name should be 'Value' as it is hardcoded in the code in this version
    
Potential Future Enhancements:
    1. Check for empty records run - need to set an exception when both source and target has no data
    2. Performance benchmark
    3. Revisit both source and target measure null value check
    4. Convert the file to an .exe file
    5. Do not run the program, if available system memory is less than size of source + target file?
    6. Generalize the program for user provided measure name?
    7. Extend the program for multiple measures?

Dataset used to test the code added to the repo.
