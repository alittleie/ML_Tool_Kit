from clean import *
from ml import *

# Example of ml project
clean = Clean()
clean.clean_df(r'C:\Users\mxr29\Desktop\ML_TEST\titan.csv', drop_method=None)

clean.format(format_type='drop', col=['Age', 'Cabin', 'Name', 'Em'])
clean.format(format_type='label_encode', col=['Sex', 'Ticket'])
clean.format(format_type='dummies', col=['Embarked'])
clean.format(format_type='target', col=['Survived'])

df = clean.return_df()
print(df)
df.to_csv(r'C:\Users\mxr29\Desktop\ML_TEST\titan_clean.csv')
ml = Ml()
ml.tts(df, transform=1, stratify=1, random_state=999)
ml.model(mod='RF', hyper=1)

