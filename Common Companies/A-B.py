import numpy as np
import pandas as pd

sheet1=pd.read_excel('companyData.xlsx',header=None,sheet_name=[0])[0].to_numpy()

sheet2=pd.read_excel('companyData.xlsx',header=None,sheet_name=[1])[1].to_numpy()

newarr = np.setdiff1d(sheet1, sheet2, assume_unique=True)

df = pd.DataFrame (newarr)

filepath = 'final_list.xlsx'

df.to_excel(filepath, index=False)

