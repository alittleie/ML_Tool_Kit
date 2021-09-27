import os.path
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from time import sleep


class Clean:
    df = None

    # inputs the data and will clean want to be abel to handle most data types
    def clean_df(self, path, sheet_name=None, drop_method=None):

        name, extension = os.path.splitext(path)

        # checks for file type and read in file type
        # xlsx requires sheet name
        if extension == '.csv':
            self.df = pd.read_csv(path)

        elif extension == '.xlsx' or 'xls':
            self.df = pd.read_excel(path, sheet_name=sheet_name)

        # segment for basic quick drops to test algorithms
        print('--------------------------------------------------------------')
        if drop_method == 0:
            # sets bool for drop check
            col_bool = False
            row_bool = False

            # check # of columns before and after drop nan if all on column axis
            col_len_0 = len(self.df.columns)
            self.df = self.df.dropna(axis=1, how='all')
            col_len_1 = len(self.df.columns)

            if col_len_0 != col_len_1:
                col_bool = True
                print("****** %d columns removed with all NAN *****" % (col_len_0 - col_len_1))

            # same as previous but no drop any rows containing NAN
            row_len_0 = len(self.df)
            self.df = self.df.dropna(axis=0, how='any')
            row_len_1 = len(self.df)

            if row_len_0 != row_len_1:
                row_bool = True
                print("***** %d rows removed with any NAN *****" % (row_len_0 - row_len_1))

            if col_bool is False and row_bool is False:
                print('No rows or columns were dropped due to Nan')
        print('--------------------------------------------------------------')

    # segment to either auto format columns or go through individually to convert to usable format
    def format(self,  format_type=None, col=None, auto=False, num_buckets = 2):

        def label_encode_nominal(col_in):
            self.df[col_in] = le.fit_transform(self.df[col_in].astype(str))
            print(self.df[col_in])
            sleep(1.5)

        def map_ordinal(col_in):
            mapping_bool = False
            map_list = None
            while mapping_bool is False:
                map_dic = {}
                working = False
                while working is False:
                    map_list = []
                    print(self.df[col_in].unique())
                    input_string = input('Enter mapping list separated by space ')
                    print("\n")
                    user_list = input_string.split()

                    # convert each item to int type
                    for s in range(len(user_list)):
                        # convert each item to int type
                        map_list.append(int(user_list[s]))
                    if len(map_list) != len(self.df[col_in].unique()):
                        print("len of values or format doesn't seem to match... \n")
                    else:
                        working = True

                for q in range(len(self.df[col_in].unique())):
                    map_dic[self.df[col_in].unique()[q]] = map_list[q]
                print(map_dic, '\n')
                final_check = input('Does the mapping look correct 0 for yes 1 for no: \n')
                if final_check == '0':
                    self.df[col_in] = self.df[col_in].map(map_dic)
                    print(self.df[col_in])
                    sleep(1.5)
                    mapping_bool = True
                else:
                    pass

        def set_target(col_in):
            self.df['Target'] = self.df[col_in]
            self.df = self.df.drop(axis=1, columns=[col_in])
            print(col_in, 'set as Target.')

        def drop_col(col_in):
            self.df = self.df.drop(axis=1, columns=[col_in])
            print('\n')
            print('Column Dropped')
            sleep(1.5)

        def buckets(col_in, buckets_count=2 ):
            mean = self.df[col_in].mean()
            max_val = self.df[col_in].max()
            min_val = self.df[col_in].min()
            print("Mean: %f, Min: %f, Max %f" % (mean, min_val, max_val))
            print("Number of Buckets for Target Encoding %d" % num_buckets)
            bucket_method = input('Do you want to manully define cut off points? 1 for Yes 0 for No ' )
            if bucket_method == '1':
                bucket_bool = False
                while bucket_bool is False:
                    bucket_points = None
                    bucket_points = input("%d Buckets Spaces were Selected enter %d values: " % (buckets_count, buckets_count-1))
                    if len(bucket_points) == buckets_count:
                        print(bucket_points)
                        last_bucket_check = input("Do the Bucket Points look correct? 1 for Yes 0 for No ")
                        if last_bucket_check == '1':
                            bucket_bool = True
                        else:
                            pass
                if buckets_count == 2:
                    map_val = []
                    for k in range(len(self.df)):
                        if self.df[col_in].iloc[k] < float(bucket_points):
                            map_val.append(0)
                        else:
                            map_val.append(1)
                    self.df[col_in] = map_val
                    print(self.df[col_in].head())



            else:
                pass
        print('--------------------------------------------------------------')

        # this is basic conversion of data and target selection going through each column manually
        if auto is True:
            # loops through each column
            j = len(self.df.columns)
            counter = 0
            for col in self.df:
                col_bool = False
                while col_bool is False:
                    print("Column number %d out of %d" % (counter, j), '\n')
                    counter += 1
                    # prints out column info
                    print(self.df[col].head, '\n')

                    detail = input(
                        "Do you want to see more info about the column values \n enter 0 for yes or 1 no: \n")
                    if detail == '1':
                        pass
                    else:
                        print(self.df[col].unique(), '\n')

                    method = input(
                        "Enter:  \n 0 for pass \n 1 for nominal features \n 2 for ordinal"
                        " \n 3 One Hot \n 4 for target \n 6 for drop: \n ")

                    if method == '0':
                        col_bool = True

                    if method == '1':
                        le = LabelEncoder()
                        label_encode_nominal(col)
                        col_bool = True

                    if method == '2':
                        map_ordinal(col)
                        col_bool = True

                    if method == '4':
                        set_target(col)
                        target_change = input('Do you want to change the target further 0 for yes 1 for no: ')
                        if target_change == '0':
                            col = "Target"
                        else:
                            col_bool = True

                    if method == '6':
                        drop_col(col)
                        col_bool = True

                print('--------------------------------------------------------------')

        # this segment allows you to choose formatting type by col
        elif auto is False:
            index_bool = True
            col_list = self.df.columns

            if col[0] in col_list:
                index_bool = False

            if format_type is None:
                pass

            # nominal feature
            elif format_type == 'label_encode':
                le = LabelEncoder()
                if index_bool is True:
                    for i in col:
                        col_found = col_list[i]
                        label_encode_nominal(col_found)
                elif index_bool is False:
                    for col in col:
                        label_encode_nominal(col)

            # ordinal features
            elif format_type == 'dic_map':

                if index_bool is True:
                    for i in col:
                        col_found = col_list[i]
                        map_ordinal(col_found)

                elif index_bool is False:
                    for col in col:
                        map_ordinal(col)

            # one hot encoding
            elif format_type == 'target':
                # target
                if index_bool is True:
                    for i in col:
                        col_found = col_list[i]
                        set_target(col_found)

                elif index_bool is False:
                    for col in col:
                        set_target(col)

            # bucket_encode
            elif format_type == 'bucket':
                if index_bool is True:
                    for i in col:
                        col_found = col_list[i]
                        buckets(col_found)

                elif index_bool is False:
                    for col in col:
                        buckets(col, buckets_count=num_buckets)

            # drop
            elif format_type == 'drop':
                if index_bool is True:
                    for i in col:
                        col_found = col_list[i]
                        drop_col(col_found)

                elif index_bool is False:
                    for col in col:
                        drop_col(col)
        print('--------------------------------------------------------------')

    # returns different statistics based on entry level
    def df_stats(self, level):
        print('--------------------------------------------------------------')
        if level == 0:
            print(self.df.info())

        # level 1 explores the NAN and attempts to show reasonable methods for filling
        if level == 1:
            if (len(self.df[self.df.isnull().any(axis=1)])) == 0:
                print('Seems to be no NAN...')
            else:
                print(self.df[self.df.isnull().any(axis=1)])
        print('--------------------------------------------------------------')

    # prints data frame
    def print_df(self):
        print(self.df)

    def return_df(self):
        dataframe = self.df
        return dataframe
