import math
import os
import random
import re
import sys
import numpy as np
import pandas as pd

files = ['a_example.txt','b_read_on.txt','c_incunabula.txt','d_tought_choices.txt','e_so_many_books.txt','f_libraries_of_the_world.txt']
for file_name in files:
    input_file = file_name
    with open(input_file, 'r') as my_file:
        content = my_file.read().split('\n')
        B, L, D = (int(x) for x in content[0].split(' '))
        scores = content[1].split(' ')

        d = {"ID_book" : [],
            "score" : []}
        i = 0
        for s in scores:
            d["ID_book"].append(i)
            i+= 1
            d["score"].append(s)
        books_dataframe = pd.DataFrame(data= d)

        libraries = {}
        books = {}
        lib_i = 0

        libs = {"ID_lib" : [],
            "num_books" : [],
            "signup_days" : [],
            "books_per_day" : []
            }

        libs_books = {"ID_lib" : [],
            "ID_book" : [],
            "score" : []
            }

        total_dataset = {
            "ID_lib" : [],
            "num_books" : [],
            "signup_days" : [],
            "books_per_day" : [],
            "ID_book" : [],
            "score" : [],
        }

        for i in np.arange(2, len(content)-1, 2):
            N, T, M = (int(x) for x in content[i].split(' '))
            book_idxs = [int(x) for x in content[i+1].split(' ')]
            libraries[lib_i] = book_idxs

            libs["ID_lib"].append(lib_i)
            libs["num_books"].append(N)
            libs["signup_days"].append(T)
            libs["books_per_day"].append(M)

            for bid in book_idxs:
                libs_books["ID_lib"].append(lib_i)
                libs_books["ID_book"].append(bid)

            lib_i += 1

        library_dataframe = pd.DataFrame(data= libs)
        libs_books_dataframe = pd.DataFrame(data = libs_books)

        pass
        # for line in my_file

        tots =[]

        for index, row in library_dataframe.iterrows():
            df1 = libs_books_dataframe[libs_books_dataframe["ID_lib"] == row["ID_lib"]]
            tot = 0
            for index, row in df1.iterrows():
                tot += int(scores[row["ID_book"]])
            tots.append(tot)
            
    all_t = []
    for i in np.arange(0,len (tots)):
        df1 = library_dataframe[library_dataframe["ID_lib"] == i]
        t = float(tots[i] / (df1['signup_days'] + (df1['num_books'] / df1['books_per_day'])))
        all_t.append(t)

    library_dataframe['lib_score'] = all_t
    sorted_lib = library_dataframe.sort_values(by=["lib_score"], ascending=False)

    output = []
    count = 0
    r_days = D
    for index, row in sorted_lib.iterrows():
        if r_days > row['signup_days']:
            d = {
                'line1': [],
                'line2': []
            }
            d['line1'].append(row['ID_lib'])
            r_days = r_days - row['signup_days']
            numlib = r_days * row['books_per_day']
            n = 0
            if row['num_books'] < numlib:
                d['line1'].append(row['num_books'])
                n = row['num_books']
            else:
                d['line1'].append(numlib)
                n = numlib
            df1 = libs_books_dataframe[libs_books_dataframe["ID_lib"] == row['ID_lib']]
            df2 = pd.merge(df1, books_dataframe, on = "ID_book")
            df2_sorted = df2.sort_values(by=["score"], ascending=False)
            first_n_books = df2_sorted[:int(n)]['ID_book']
            d['line2'] = list(first_n_books)
            output.append(d)
            count += 1

    with open("result"+input_file+".txt", 'w+') as my_file:
        my_file.write(str(count) + "\n")
        for o in output:
            for item in o['line1']:
                my_file.write("%s " % int(item))
            my_file.write("\n")
            for item in o['line2']:
                my_file.write("%s " % int(item))
            my_file.write("\n")