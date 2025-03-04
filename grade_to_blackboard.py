import pandas as pd

# Load the CSV file into a DataFrame
blackboard_csv_file_path = "462_IT315_4589.csv"  # Replace with the path to your CSV file
full_report_csv_path = "students/try1/reports/project2-full-report.csv"
grade_column_blackboard = 'Project 02 [Total Pts: 100 Score] |1702852'
backboard_df = pd.read_csv(blackboard_csv_file_path)
grade_df = pd.read_csv(full_report_csv_path)

username_column_blackboard = "Username"
# Convert both columns to string type before merging
backboard_df['Username'] = backboard_df['Username'].astype(str)
grade_df['sid'] = grade_df['sid'].astype(str)

print("Please wait ...")
# Check if the required columns exist in the DataFrame
if username_column_blackboard in backboard_df.columns and grade_column_blackboard in backboard_df.columns:
    backboard_df = backboard_df.merge(grade_df[['sid', 'total']], left_on=username_column_blackboard, right_on='sid', how='left')
    backboard_df[grade_column_blackboard] = backboard_df['total']
    backboard_df.drop(columns=['total', 'sid'], inplace=True)  # Remove extra columns
else:
    print(f"Required columns 'sid' and {grade_column_blackboard} are not present in the CSV file.")

# Save the updated DataFrame back to a CSV file
output_file = f"{grade_column_blackboard}_updated_file.csv"  # Replace with the desired output file path
backboard_df.to_csv(output_file, index=False)
print(f"Updated CSV file is saved as {output_file}")