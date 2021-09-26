from clean import *
from ml import *

# Example of ml project
clean = Clean()
clean.clean_df(r'C:\Users\mxr29\Desktop\New folder\farmed_twitter.csv', drop_method=0)
clean.format(level = 1, auto=False, format_type=3, col=['Retweets'])
clean.print_df()
df = clean.return_df()

# ml = Ml()
# ml.tts(df, transform=1, stratify=1, random_state=999)
# ml.model(type='RF')

