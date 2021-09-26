from clean import *
from ml import *

clean = Clean()
clean.clean_df(r'C:\Users\mxr29\Desktop\ML_TEST\wine.csv', drop_method=0)
#clean.auto_format(0, auto=False)
df = clean.return_df()

ml = Ml()
ml.tts(df, transform=1, stratify=1, random_state=999)
ml.model(type='RF')

