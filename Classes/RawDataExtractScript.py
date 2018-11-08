import pandas as pd
from os.path import expanduser as ospath

pd.set_option('display.expand_frame_repr', False)

fileVersion = "2.14"
filePath = '~/Box Sync/Shared/Lock-up Fund Client Holdings & Performance Tracker/Cash Flow Model/CBA Cash Flow Model - v{} - Far Hills.xlsx'.format(fileVersion)
df = pd.read_excel(ospath(filePath), sheet_name='Raw_Data', header=1)

df = df.drop(df.columns[14:-1], axis=1)

####

validationDf = pd.read_excel(ospath(filePath), sheet_name='Validation', header=1)

sponsorDf = validationDf[['Sponsor_List', 'Sponsor_Code']]
sponsorDf = sponsorDf.dropna()
sponsorDf['Sponsor_List'] = sponsorDf['Sponsor_List'].str.strip()

fundStyleDf = validationDf[['Fund_Style', 'Fund_Code']]
fundStyleDf = fundStyleDf.dropna()
fundStyleDf['Fund_Style'] = fundStyleDf['Fund_Style'].str.strip()

clientDf = validationDf[["Client_List", "Client_Code"]]
clientDf = clientDf.dropna()
clientDf['Client_List'] = clientDf['Client_List'].str.strip()

###


sponsorDataTableDf = pd.read_excel(ospath(filePath), sheet_name='Sponsor Data Table', header=1)

familyDf = sponsorDataTableDf[["Sponsor", "Fund Family"]]
familyDf = familyDf.dropna()
familyDf['Sponsor'] = familyDf['Sponsor'].str.strip()
familyDf['Fund Family'] = familyDf['Fund Family'].str.strip()

mergedDf = pd.merge(sponsorDf, familyDf, left_on='Sponsor_List', right_on='Sponsor')[['Sponsor_Code', 'Fund Family']]
mergedDf = mergedDf.drop_duplicates()


print df
print sponsorDf
print fundStyleDf
print clientDf
print familyDf
print mergedDf