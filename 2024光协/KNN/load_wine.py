import sklearn
from sklearn.datasets import load_wine
import pandas as pd

lw=load_wine()
#print(dir(lw))
x=lw.data
x=x[:,:2]
y=lw.feature_names
y=y[:2]
z=lw.target
lw_df=pd.DataFrame(x,columns=y,index=z)
#print(lw_df)
lw_df.to_csv("load_wine.csv")

