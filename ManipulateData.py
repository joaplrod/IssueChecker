#! python3
# ManipulateData.py -> To clean JIRA issues data.

import os
import re
import pandas as pd
import matplotlib.pyplot as plt

def FileFinder():
    ''' This function will look for a CSV file with the word JIRA in it to extract the target information.
    If it does not find the file will raise an error.
    @ return: (str) Specific path+file of the Jira .csv file
    '''

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
    merging all the link values in just one column and sorting the rows by date.
    @ JiraFile: (str) Specific path+file of the target csv
    @ coulmnvalues: (list) All the columns that must be copied directly from the csv
    @ return: (str) Specific path+file of the new dataframe converted into csv
    '''
    df = pd.read_csv(JiraFile, delimiter=',')
    Jiradf = df[columnvalues].copy()


    # Put all the Links column in one
    Jiradf['Links'] = ''
    aux = ""
    for rows in range(0, Jiradf.shape[0], 1):
        for columns in range(11, (df.shape[1]), 1):
            if(df.iloc[rows,columns] == df.iloc[rows, columns]):
                aux += ',' + df.iloc[rows,columns]
        Jiradf.iloc[rows,-1] = aux
        aux= ''

    # Clean the data
    for i in range(0, Jiradf.shape[0],1):
       Jiradf.iloc[i, -1] = re.sub(r'^\W*', '', Jiradf.iloc[i, -1])
       Jiradf.iloc[i, -1] = re.sub(r'\W*$', '', Jiradf.iloc[i, -1])
       Jiradf.iloc[i,-2] = re.sub(r' (\d+:)*(\d+)', '', Jiradf.iloc[i, -2])
       Jiradf.iloc[i, -2] = re.sub(r'\n$', '', Jiradf.iloc[i, -2])

    #print(Jiradf.iloc[0,:])
    #print(Jiradf['Links'])
    Jiradf['Updated'] = pd.to_datetime(Jiradf.Updated)
    Jiradf.sort_values(by='Updated', inplace=True, ascending=False)


    Jiradf.to_csv((os.path.splitext(JiraFile)[0] + '_results.csv'), index=False)
    #print(Jiradf.columns)
    #print(Jiradf.head(5))

    #Delete file
    #os.remove(JiraFile)

    return (os.path.splitext(JiraFile)[0] + '_results.csv')


def ExcelAppender(cleaneddf, exceldf):
    ''' This function will append the new tickets in the excel file.
       @ cleaneddf: (str) Specific path+file of the downloaded&cleaned csv
       @ exceldf: (str) Specific path+file of the excel file
       @ return: (str) Specific path+file of the new dataframe converted into csv
       '''
    exdf = pd.read_csv(exceldf)
    cldf = pd.read_csv(cleaneddf, nrows=50)

    exdf = exdf.append(cldf, ignore_index=True)
    exdf.drop_duplicates(subset='Issue key', inplace=True)
    exdf.sort_values(by='Updated', ascending=False, inplace=True)

    # Delete file
    # os.remove(cleaneddf)

def IssuesPlotter(exceldf):
    ''' This function will plot the logged tickets by month, by firmware version, by department.
       @ exceldf: (str) Specific path+file of the excel file
   '''
    exdf = pd.read_csv(exceldf)

    DateMax = exdf.iloc[0,-2]
    DateMin = exdf.iloc[-1,-2]

    binsplt = (int)(DateMax[:4]) - (int)(DateMin[:4])
    binsplt = binsplt * 12 + (int)(DateMax[5:7]) - (int)(DateMin[5:7]) + 1
    binspltStrings = []
    binspltStrings.append(DateMin[:7])

    auxmonth = (int)(DateMin[5:7])
    auxyear = (int)(DateMin[:4])

    for i in range(binsplt):
        auxmonth = auxmonth + 1
        if auxmonth == 13:
            auxmonth = 1
            auxyear = auxyear + 1
        binString = (str)(auxyear) + '-' + "{0:0=2d}".format(auxmonth)
        binspltStrings.append(binString)

    exdf.Updated = pd.to_datetime(exdf['Updated'])

    plt.hist(exdf['Updated'], bins=binsplt)
    plt.xlabel('Months')
    plt.ylabel('Amount of issues')
    plt.title('Amount of solved issues by month')
    plt.xticks(binspltStrings, binspltStrings)
    plt.xticks(rotation=60)
    plt.show()


if __name__ == "__main__":
    print('Start')
    columnvalues = ['Issue Type', 'Issue key', 'Summary', 'Assignee', 'Reporter', 'Updated']
    target = FileFinder()
    cleaneddf = DataFrameCleaner(target, columnvalues)
    exceldf = os.path.join('C:\\', 'Users', os.getlogin(), 'Downloads','JiraTickets.csv')
    #ExcelAppender(cleaneddf, exceldf)
    IssuesPlotter(cleaneddf)