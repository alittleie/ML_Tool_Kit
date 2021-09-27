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
    def format(self, level, format_type=0, col=None, auto=False):

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

        def drop_col(col_in):
            self.df = self.df.drop(axis=1, columns=[col_in])
            print('\n')
            print('Column Dropped')
            sleep(1.5)

        print('\n')
        print('--------------------------------------------------------------')

        # this is basic conversion of data and target selection going through each column manually
        if level == 0 and auto is False:
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

                print('\n')
                print('--------------------------------------------------------------')

        # this segment allows you to choose formatting type by col
        elif level == 1 and auto is False:
            index_bool = True
            col_list = self.df.columns

            if col[0] in col_list:
                index_bool = False

            if format_type == 0:
                pass

            # nominal feature
            elif format_type == 1:
                le = LabelEncoder()
                if index_bool is True:
                    for i in col:
                        col_found = col_list[i]
                        label_encode_nominal(col_found)
                elif index_bool is False:
                    for col in col:
                        label_encode_nominal(col)

            # ordinal features
            elif format_type == 2:

                if index_bool is True:
                    for i in col:
                        col_found = col_list[i]
                        map_ordinal(col_found)

                elif index_bool is False:
                    for col in col:
                        map_ordinal(col)

            # one hot encoding
            elif format_type == 3:
                # target
                if index_bool is True:
                    for i in col:
                        col_found = col_list[i]
                        set_target(col_found)

                elif index_bool is False:
                    for col in col:
                        set_target(col)

            # drop
            elif format_type == 6:
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
