from clean import *
from ml import *

# Example of ml project
clean = Clean()
clean.clean_df(r'C:\Users\mxr29\Desktop\ML_TEST\creditcard.csv', drop_method=0)
clean.df_stats(level=0)
clean.format(format_type='bucket', num_buckets=3, col=['Amount'])
clean.format(format_type='target', col=['Amount'])
# clean.print_df()
df = clean.return_df()

ml = Ml()
ml.tts(df, transform=1, stratify=1, random_state=999)
ml.model(mod='RF', hyper=0)

