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

            if col_bool == False and row_bool == False:
                print('No rows or columns were dropped due to Nan')
        print('--------------------------------------------------------------')

    # segment to either auto format columns or go through individually to convert to usable format
    def format(self, level, format_type=0, col=None, auto=False):
        print('\n')
        print('--------------------------------------------------------------')

        # this is basic conversion of data and target selection going through each column manually
        if level == 0 and auto == False:
            # loops through each column
            j = len(self.df.columns)
            l = 0
            for col in self.df:
                col_bool = False
                while col_bool == False:
                    print("Column number %d out of %d" % (l, j), '\n')
                    l += 1
                    # prints out column info
                    print(self.df[col].head, '\n')

                    detail = input(
                        "Do you want to see more info about the column values \n enter 0 for yes or 1 no: \n")
                    if detail == '1':
                        pass
                    else:
                        print(self.df[col].unique(), '\n')

                    method = input(
                        "Enter:  \n 0 for pass \n 1 for nominal features \n 2 for ordinal \n 3 One Hot \n 4 for target \n 6 for drop: \n ")

                    if method == '0':
                        col_bool = True
                    if method == '1':
                        le = LabelEncoder()
                        self.df[col] = le.fit_transform(self.df[col].astype(str))
                        print(self.df[col])
                        sleep(1.5)
                        col_bool = True
                    if method == '2':
                        mapping_bool = False
                        while mapping_bool == False:
                            map_dic = {}
                            working = False
                            while working == False:
                                map_list = []
                                print(self.df[col].unique())
                                input_string = input('Enter mapping list separated by space ')
                                print("\n")
                                user_list = input_string.split()

                                # convert each item to int type
                                for i in range(len(user_list)):
                                    # convert each item to int type
                                    map_list.append(int(user_list[i]))
                                if len(map_list) != len(self.df[col].unique()):
                                    print("len of values or format doesn't seem to match... \n")
                                else:
                                    working = True

                            for i in range(len(self.df[col].unique())):
                                map_dic[self.df[col].unique()[i]] = map_list[i]
                            print(map_dic, '\n')
                            final_check = input('Does the mapping look correct 0 for yes 1 for no: \n')
                            if final_check == '0':
                                self.df[col] = self.df[col].map(map_dic)
                                print(self.df[col])
                                sleep(1.5)
                                mapping_bool = True
                            else:
                                pass
                        col_bool = True
                    if method == '4':
                        self.df['Target'] = self.df[col]
                        self.df = self.df.drop(axis=1, columns=[col])
                        target_change = input('Do you want to change the target further 0 for yes 1 for no: ')
                        if target_change == '0':
                            col = "Target"
                        else:
                            col_bool = True
                    if method == '6':
                        self.df = self.df.drop(axis=1, columns=[col])
                        print('\n')
                        print('Column Dropped')
                        sleep(1.5)
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
                print('here')
                le = LabelEncoder()
                if index_bool is True:
                    for i in col:
                        self.df[col_list[i]] = le.fit_transform(self.df[col_list[i]].astype(str))
                        print(self.df[col_list[i]])
                        sleep(1.5)
                elif index_bool is False:
                    for col in col:
                        self.df[col] = le.fit_transform(self.df[col].astype(str))
                        print(self.df[col])
                        sleep(1.5)
            # ordinal features
            elif format_type == 2:

                if index_bool is True:
                    for i in col:
                        print(i)
                        mapping_bool = False
                        while mapping_bool == False:
                            map_dic = {}
                            working = False
                            while working == False:
                                map_list = []
                                print(self.df[col_list[i]].unique())
                                input_string = input('Enter mapping list separated by space ')
                                print("\n")
                                user_list = input_string.split()

                                # convert each item to int type
                                for j in range(len(user_list)):
                                    # convert each item to int type
                                    map_list.append(int(user_list[j]))
                                if len(map_list) != len(self.df[col_list[i]].unique()):
                                    print("len of values or format doesn't seem to match... \n")
                                else:
                                    working = True

                            for j in range(len(self.df[col_list[i]].unique())):
                                map_dic[self.df[col_list[i]].unique()[j]] = map_list[j]
                            print(map_dic, '\n')
                            final_check = input('Does the mapping look correct 0 for yes 1 for no: \n')
                            if final_check == '0':
                                self.df[col_list[i]] = self.df[col_list[i]].map(map_dic)
                                print(self.df[col_list[i]])
                                sleep(1.5)
                                mapping_bool = True
                            else:
                                pass
                elif index_bool is False:
                    for col in col:
                        mapping_bool = False
                        while mapping_bool == False:
                            map_dic = {}
                            working = False
                            while working == False:
                                map_list = []
                                print(self.df[col].unique())
                                input_string = input('Enter mapping list separated by space ')
                                print("\n")
                                user_list = input_string.split()

                                # convert each item to int type
                                for i in range(len(user_list)):
                                    # convert each item to int type
                                    map_list.append(int(user_list[i]))
                                if len(map_list) != len(self.df[col].unique()):
                                    print("len of values or format doesn't seem to match... \n")
                                else:
                                    working = True

                            for i in range(len(self.df[col].unique())):
                                map_dic[self.df[col].unique()[i]] = map_list[i]
                            print(map_dic, '\n')
                            final_check = input('Does the mapping look correct 0 for yes 1 for no: \n')
                            if final_check == '0':
                                self.df[col] = self.df[col].map(map_dic)
                                print(self.df[col])
                                sleep(1.5)
                                mapping_bool = True
                            else:
                                pass
            # one hot ecnconding
            elif format_type == 3:
                pass
            # target
            if index_bool is True:
                for i in col:
                        self.df['Target'] = self.df[col_list[i]]
                        self.df = self.df.drop(axis=1, columns=[col_list[i]])
            elif index_bool is False:
                for col in col:
                    self.df['Target'] = self.df[col]
                    self.df = self.df.drop(axis=1, columns=[col])
            # drop
            elif format_type == 6:
                pass
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
