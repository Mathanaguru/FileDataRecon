# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 17:46:22 2021
Last updatyed on Jan 3 2021
@author: Mathanaguru Gopalakrishnan
Purpose: Utility to compare two .csv files
Change history 
    v0.11: 10-Jan-2021 - Write outputs to user provided path
    v0.12: 17-Jan-2021 - Create summary output
    v0.13: 17-Jan-2021 - Include date and time in the summary output
    v0.14: 17-Jan-2021 - Change the Summary stats path as optional

Limitations:
    1. Restricted to .csv file format
    2. Source and target directories should be different
    3. Names of the source file and target file should be the same
    4. Files should be in flat structure: measure should be in just 1 column
    5. Only files in the parent dirtectory are considered
       i.e. files in the sub-folder or directory are not considered
    6. Measure file/column name should be 'Value' as it is hardcoded in the code in this version

Future Enhancements:
    1. Check for empty records run - need to set an exception when both source and target has no data
    2. Performance benchmark
    3. Revisit both source and target measure null value check
    4. Convert the file to an .exe file
    5. Do not run the program, if available system memory is less than size of source + target file?
    6. Generalize the program for user provided measure name?
    7. Extend the program for multiple measures?
"""
#*****************************************************************************
#  Import the modules required for the program
#*****************************************************************************
# To check for file availability and get basefile name
import os

# To exit the program
import sys

# To use the logging
import logging

# To import csv files and compare them
import pandas as pd

# To get the file name without extension
from pathlib import Path

# To get the current date and time
from datetime import datetime
now = datetime.now() # Get the current timestamp

#*****************************************************************************
#  Setup logging
#*****************************************************************************
# Default logging level is set as info
logging.basicConfig(filename='python.log', level=logging.INFO,
                    format='%(asctime)s:python program file name-%(filename)s:%(funcName)s:%(name)s:%(levelno)s:%(levelname)s:%(lineno)d:%(thread)d:%(threadName)s:%(process)d:%(processName)s:%(module)s:%(message)s')

# Program start log
logging.info('Program execution starts')

#*****************************************************************************
#  Initialize Flags/Variables
#*****************************************************************************
# Flags - Exit program
exit_program_flag = 0

#*****************************************************************************
#  Define class(s)
#*****************************************************************************
class InputFileValidations:
    '''Validate the user input for file prompt'''
    
    def __init__(self,file_name, file_type):
        ''' Initialize fullfile name and file type (source/target)'''
        self.file_name = file_name
        self.file_type = file_type
      
    def file_check_exists(self):
        '''Check if the file exists'''
        if os.path.isfile(self.file_name):
            exit_program_flag = 0
            logging.info(f"{self.file_type} file exists validation has passed: A file with user provided {self.file_type} full file name exists")
        else:
            exit_program_flag = 1
            logging.critical(f"Error, a file with user provided {self.file_type} full file name does not exists")
        return exit_program_flag
    
    def file_check_csv_ext(self):
        '''Check if the file extension is .csv '''
        if self.file_name.lower().endswith('.csv'):
            exit_program_flag = 0
            logging.info(f"{self.file_type} file extension is .csv validation has passed: User provide {self.file_type} file is a .csv file")
        else:
            exit_program_flag = 1
            logging.critical(f"Error, a file with user provided {self.file_type} full file name does not exists")
        return exit_program_flag    
 
class FileAttributes:
    '''Get the file attributes such as file name, number of records'''
    
    def __init__(self,file_name, file_type):
        '''Initialize file name'''
        self.file_name = file_name
        self.file_type = file_type
        
    def file_name_wo_extn(self):
        '''Get the file name only without extension'''
        name_wo_extn = Path(self.file_name).stem
        logging.debug(f"{self.file_type} file name without extension is {name_wo_extn}")
        return name_wo_extn
  
class CompareFilesValidation:
    '''Compare the file, including source and target file check validations'''
    
    def __init__(self, source_file, target_file):
        '''Initialize source file, target file, and measure name'''
        self.source_file = source_file
        self.target_file = target_file
    
    def files_are_same(self):
        '''Check if the source and target file is the same'''
        if self.source_file != self.target_file:
            exit_program_flag = 0
            logging.info("Source and target file is not the same validation has passed: Source and target files are different")
        else:
            exit_program_flag = 1
            logging.critical("Error, source and target file should not be the same")
        return exit_program_flag

class SummaryStasFileHeader:
    '''Summary Stats file column headers'''
    
    def __init__(self, summary_file):
        '''Initialize the summary file name'''
        self.summary_file = summary_file
       
#*****************************************************************************
#  User inputs for source and target files
#*****************************************************************************

text = 'Enter the full path and file name of the source .csv file with file extension:\n'
source_file = input(text)
logging.info(f"User provided source .csv full file name with extension is '{source_file}'")

text = 'Enter the full path and file name of the target .csv file with file extension:\n'
target_file = input(text)
logging.info(f"User provided target .csv full file name with extension is '{target_file}'")

#*****************************************************************************
#  User inputs for Output file path and Summary file path
#*****************************************************************************
text = 'Enter the Output directory path:\n'
output_dir_path = input(text)
logging.info(f"User provided output directory path is '{output_dir_path}'")

text = "Enter the full path and file name of the summary stats file with file extension (Optional)\n"
text = text + "Default path is Output directory and file name is Summary Stats csv File Compare_DateTime.csv:\n"
summary_stat_file = input(text)
logging.info(f"User provided summary directory path is '{summary_stat_file}'")

#*****************************************************************************
#  Validations - User input; If fails, exit the program
#*****************************************************************************

file_validations_fail = [InputFileValidations(file_name = source_file,file_type='Source').file_check_exists(),
               InputFileValidations(file_name = target_file,file_type='Target').file_check_exists(),
               InputFileValidations(file_name = source_file,file_type='Source').file_check_csv_ext(),
               InputFileValidations(file_name = target_file,file_type='Target').file_check_csv_ext(),
               CompareFilesValidation(source_file = source_file,target_file = target_file).files_are_same(),
               ]

if 1 in file_validations_fail:
    logging.critical("Enter valid inputs! Exiting the program...")
    print('Atleast one of the validations has failed. Refer to the log file for error details')
    sys.exit(0)

#*****************************************************************************
#  File attributes
#*****************************************************************************
## Export file name is the combination of source and target file
# Get file name with extension - To construct the compare output file name
source_file_name_wo_ext = FileAttributes(source_file,file_type='Source').file_name_wo_extn()
target_file_name_wo_ext = FileAttributes(target_file,file_type='Target').file_name_wo_extn()
# Data match export file name and directory
match_data_file_name = source_file_name_wo_ext + ' Vs. ' + target_file_name_wo_ext + ' - match records.csv'
logging.debug(f"Match data file name is {match_data_file_name}")
match_data_full_file_name = os.path.join(output_dir_path, match_data_file_name)
logging.info(f"Match data file name with directory path is {match_data_full_file_name}")
# Data mismatch export file name and directory
mismatch_data_file_name = source_file_name_wo_ext + ' Vs. ' + target_file_name_wo_ext + ' - mismatch records.csv'
logging.debug(f"Mismatch data file name is {mismatch_data_file_name}")
mismatch_data_full_file_name = os.path.join(output_dir_path, mismatch_data_file_name)
logging.info(f"Mismatch data file name with directory path is {mismatch_data_full_file_name}")

# Summary Stats file is combination of directory path and hardcoded file name
# Date string in the format: yyyy-mm-dd hh.mm.ss
dt_string = now.strftime("%Y-%m-%d %H.%M.%S")
if len(summary_stat_file) == 0:
    summary_stats_filename = 'Summary Stats csv File Compare_' + dt_string + '.csv'
    summary_stats_fullfilename = os.path.join(output_dir_path, summary_stats_filename)
else:
    summary_stats_fullfilename = summary_stat_file
logging.info(f"Summary stats file name with directory path is {summary_stats_fullfilename}")

#*****************************************************************************
#  Load the source and target file in a DataFrame and Compare
#*****************************************************************************
try:
    # Read the source and target .csv files
    source_df = pd.read_csv(source_file)
    logging.debug(f"Source file data read in dataframe:\n{source_df}")
        
    target_df = pd.read_csv(target_file)
    logging.debug(f"Target file data read in dataframe:\n{target_df}")

    # Get the length of source and target file
    no_source_records = len(source_df)
    logging.info(f'Number of records in source file:{no_source_records}')
        
    no_target_records = len(target_df)
    logging.info(f'Number of records in target file:{no_target_records}')
        
    # Source - Get all the index columns, except for the Value/Values as concat_col
    source_col_names = source_df.columns
    source_concat_key = []
    for source_col_name in source_col_names:
        if source_col_name.lower() != 'value' and source_col_name.lower() != 'values':
           source_concat_key.append(source_col_name)

    # Source - Set the concat_col as the multi-index
    source_df = source_df.set_index(list(source_concat_key))
    logging.debug(f"Source dataframe with concat key set as index:\n{source_df}")
        
    # Target - Get all the index columns, except for the Value/Values as concat_col
    target_col_names = target_df.columns
    target_concat_key = []
    for target_col_name in target_col_names:
        if target_col_name.lower() != 'value' and target_col_name.lower() != 'values':
            target_concat_key.append(target_col_name)
        
    # Target - Set the concat_col as the multi-index
    target_df = target_df.set_index(list(target_concat_key))
    logging.debug(f"Target dataframe with concat key set as index:\n{target_df}")
        
    # Merge the source and target file data with outer join
    combined_df = pd.merge(source_df,target_df, left_index=True, right_index=True, how='outer')
    logging.debug(f"Source and target comnbined dataframe:\n{combined_df}")
    merge_records = len(combined_df)
    logging.info(f"Number of records in the merged file is {merge_records}")

    # Source file and target file matches, when following conditions are met:
    # 1. Number of records in source and target file match
    # 2. Both source and target value has no mismatch records

    # Check for number of records match
    if no_source_records == no_target_records:
        no_records_match = 1
        logging.info('Number of records in source and target files records match')
    else:
        no_records_match = 0
        logging.info('Number of records in source and target files records does not match')
         
    # Create a new column, Match
    # If either/both source and target measure value is None, then Match is set as Flase by default
    combined_df['Match'] = combined_df.loc[:,'Value_x']==combined_df.loc[:,'Value_y']
    logging.debug(f"Combined dataframe prior to null records exception:\n{combined_df}")
    
    # If both the source and target measure value is None, then update the Match flag as True
    combined_df.loc[(combined_df['Value_x'].isnull() == True) & (combined_df['Value_y'].isnull() == True), 'Match'] = True
    logging.debug(f"Combined dataframe post to null records exception:\n{combined_df}")
        
    # Check if all the records of the data match
    if (combined_df['Match'] == True).all():
        files_match_flag = 1
        logging.info('Each data in the source file match with the target file')
    else:
        files_match_flag = 0
        logging.info('Atleast some source and target file data does not match')
        
    # Combine the number of records and data check
    if ((no_records_match == 1) and (files_match_flag == 1)):
        logging.info('Overall reconciliation result: Number of records and Each data in the source file match with the target file')
    else:
        logging.info('Overall reconciliation result: Atleast some source and target file data does not match')

#*****************************************************************************
#  Export the match and mismatch data to respective files
#*****************************************************************************
    # Export the data, only when match/mismatch data is available
    logging.info("Match/Misatch file is created, only when the corresponding dataset exist")
    
    match_records = len(combined_df[combined_df['Match']==True])
    mismatch_records = len(combined_df[combined_df['Match']==False])
        
    if match_records> 0:
        # Export match records
        combined_df[combined_df['Match']==True].to_csv(match_data_full_file_name)
        logging.info(f"{match_records} records has been exported to '{match_data_full_file_name}'")
    else:
        logging.info('Source and target file has no match records')
        
    if mismatch_records > 0:
        # Export mismatch records
        combined_df[combined_df['Match']==False].to_csv(mismatch_data_full_file_name)
        logging.info(f"{mismatch_records} records has been exported to '{mismatch_data_full_file_name}'")
    else:
        logging.info('Source and target file has no mismatch records')

    # Totals Check reconciliation
    if merge_records == match_records + mismatch_records:
        logging.info(f"Sum check has passed: Merge file data records {merge_records} in memory = Match records({match_records}) + Mismatch records({mismatch_records})")
    else:
        logging.info(f"Sum check has faled: Merge file data records {merge_records} in memory != Match records({match_records}) + Mismatch records({mismatch_records})")

#*****************************************************************************
#  Export the summary stats
#*****************************************************************************
    summary_stats_data = {'Source File Name': [source_file_name_wo_ext],
                          'Target File Name': [target_file_name_wo_ext],
                          'Date & Time': [now],
                          'Source File Directory & Path': [source_file],
                          'Target File Directory & Path': [target_file],
                          'No. of records in Source File': [no_source_records],
                          'No. of records in Target File': [no_target_records],
                          'No. of Match records': [match_records],
                          'No. of Mismatch records': [mismatch_records],
                          'Dataset Match Flag': [files_match_flag],
                          'Location of Match records': [match_data_full_file_name],
                          'Location of Mismatch records': [mismatch_data_full_file_name],
                          'Remarks': ''
                          }
    summary_stats_df = pd.DataFrame(data=summary_stats_data)
    logging.debug(f"Summary Stats dataframe data is:\n{summary_stats_df}")
    summary_stats_df.to_csv(summary_stats_fullfilename)
    logging.info('Summary Stats of two .csv file compare is exported successfully')
    
#*****************************************************************************
#  Program run successfully print message
#*****************************************************************************
    # Last info message of the program, if it successful
    logging.info("File compare Program has completed successfully without any errors")
    print("Program successfully completed")
    # Program End log
    logging.info('Program execution Ends')

except:
    logging.critical("Unexpected Error! Exiting the program...")
    print('Program failed witn an unexpected Error')