import math
import os
import random
import re
import sys
import numpy as np
import pandas as pd


files = ['a_example.txt','b_read_on.txt','c_incunabula.txt','d_tough_choices.txt','e_so_many_books.txt','f_libraries_of_the_world.txt']
for file_name in files:
    input_file = file_name
    with open(input_file, 'r') as my_file:
        content = my_file.read().split('\n')
        B, L, D = (int(x) for x in content[0].split(' '))
        scores = content[1].split(' ')

        d = {}
        i = 0
        for s in scores:
            d[i] = s
            i+= 1

        books_dataframe = pd.DataFrame()

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
            'book_done' : []
        }

        for i in np.arange(2, len(content)-1, 2):
            N, T, M = (int(x) for x in content[i].split(' '))
            book_idxs = [int(x) for x in content[i+1].split(' ')]
            libraries[lib_i] = book_idxs

            for bid in book_idxs:
                total_dataset["ID_lib"].append(int(lib_i))
                total_dataset["num_books"].append(int(N))
                total_dataset["signup_days"].append(int(T))
                total_dataset["books_per_day"].append(int(M))
                total_dataset["ID_book"].append(int(bid))
                total_dataset['score'].append(int(d[bid]))
                total_dataset['book_done'].append(0)

            lib_i += 1

        #library_dataframe = pd.DataFrame()
        libs_books_dataframe = pd.DataFrame()

        pd_total_dataset = pd.DataFrame(data = total_dataset)
        #pd_total_dataset['score'] = pd.to_numeric(pd_total_dataset['score'])

    #calcolo score totale potenziale di ogni libreria
    library_score = {
        "ID_lib" : [],
        "total_score" : [],
        "lib_score" : [],
    }

    for idlib in pd_total_dataset.ID_lib.unique():
        tot = pd_total_dataset[pd_total_dataset["ID_lib"] == idlib].score.sum()
        one_record = pd_total_dataset[pd_total_dataset["ID_lib"] == idlib].head(1)
        lib_S = float(tot / (one_record['signup_days'].item() + (one_record['num_books'].item() / one_record['books_per_day'].item())))
        library_score["ID_lib"].append(idlib)
        library_score["total_score"].append(tot)
        library_score["lib_score"].append(lib_S)
    

    library_dataframe = pd.DataFrame(data = library_score)
    sorted_lib = library_dataframe.sort_values(by=["lib_score"], ascending=False)

    output = []
    count = 0
    r_days = D
    for index, row in sorted_lib.iterrows():
        one_record = pd_total_dataset[pd_total_dataset["ID_lib"] == row['ID_lib']].head(1)

        if r_days > one_record['signup_days'].item():
            d = {
                'line1': [],
                'line2': []
            }
            d['line1'].append(one_record['ID_lib'].item())
            r_days = r_days - one_record['signup_days'].item()
            numlib = r_days * one_record['books_per_day'].item()
            n = 0
            if one_record['num_books'].item() < numlib:
                d['line1'].append(one_record['num_books'].item())
                n = one_record['num_books'].item()
            else:
                d['line1'].append(numlib)
                n = numlib

            df1 = pd_total_dataset[pd_total_dataset["ID_lib"] == one_record['ID_lib'].item()]
            df2_sorted = df1.sort_values(by=["score"], ascending=False)
            first_n_books = df2_sorted[:int(n)]['ID_book']
            d['line2'] = list(first_n_books)
            output.append(d)
            count += 1

    with open("result/result"+input_file, 'w+') as my_file:
        my_file.write(str(count) + "\n")
        for o in output:
            for item in o['line1']:
                my_file.write("%s " % int(item))
            my_file.write("\n")
            for item in o['line2']:
                my_file.write("%s " % int(item))
            my_file.write("\n")
