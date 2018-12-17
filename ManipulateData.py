#! python3
# ManipulateData.py -> To clean JIRA issues data.

import os
import re
import pandas as pd

def FileFinder():
    ''' This function will look for a CSV file with the word JIRA in it to extract the target information.
    If it does not find the file will raise an error. '''

    target = ''
    folder = os.path.join('C:\\', 'Users', os.getlogin(),'Downloads')
    for file in os.listdir(folder):
        if '(JIRA).csv' in file:
            JiraFile = file
            target = os.path.join(folder, JiraFile)
    if target == '':
        raise FileNotFoundError
    else:
        return target


def DataFrameCleaner(JiraFile, columnvalues):
    ''' This function will create a new csv file with the target values,
    merging all the link values in just one column and sorting the rows by date. '''

    df = pd.read_csv(JiraFile, delimiter=',')
    Jiradf = df[columnvalues].copy()
    Jiradf['Links'] = df.iloc[:, -11:].fillna('').astype(str).apply(lambda x: ','.join(x), axis=1)
    for i in range(0, Jiradf.shape[0],1):
       Jiradf.iloc[i, -1] = re.sub(r'^\W*', '', Jiradf.iloc[i, -1])
       Jiradf.iloc[i, -1] = re.sub(r'\W*$', '', Jiradf.iloc[i, -1])
       Jiradf.iloc[i, -1] = re.sub(r',{2,}', ',', Jiradf.iloc[i, -1])
       Jiradf.iloc[i,-2] = re.sub(r' (\d+:)*(\d+)', '', Jiradf.iloc[i, -2])


    Jiradf['Updated'] = pd.to_datetime(Jiradf.Updated)
    Jiradf.sort_values(by='Updated', inplace=True, ascending=False)


    Jiradf.to_csv((os.path.splitext(JiraFile)[0] + '_results.csv'), index=False)
    #print(Jiradf.columns)
    print(Jiradf.head(5))

    #Remove file
    #os.remove(JiraFile)

    return (os.path.splitext(JiraFile)[0] + '_results.csv')

if __name__ == "__main__":
    print('Start')
    columnvalues = ['Issue Type','Issue key','Summary','Assignee','Reporter','Updated']
    target = FileFinder()
    target = DataFrameCleaner(target, columnvalues)
