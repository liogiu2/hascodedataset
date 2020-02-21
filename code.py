import math
import os
import random
import re
import sys
import numpy as np
import pandas as pd

def calculateLibraryScore(pd_total_dataset):
    library_score = {
        "ID_lib" : [],
        "total_score" : [],
        "lib_score" : [],
    }

    for idlib in pd_total_dataset.ID_lib.unique():
        tot = pd_total_dataset[(pd_total_dataset["ID_lib"] == idlib) & (pd_total_dataset["book_done"] == 0) ].score.sum()
        one_record = pd_total_dataset[pd_total_dataset["ID_lib"] == idlib].head(1)
        lib_S = float(tot / (one_record['signup_days'].item() + (one_record['num_books'].item() / one_record['books_per_day'].item())))
        library_score["ID_lib"].append(idlib)
        library_score["total_score"].append(tot)
        library_score["lib_score"].append(lib_S)
    

    library_dataframe = pd.DataFrame(data = library_score)
    sorted_lib = library_dataframe.sort_values(by=["lib_score"], ascending=False)
    return sorted_lib

def updateLibDone(pd_total_dataset_loc, first_n_books_loc):
    for idbook in list(first_n_books_loc):
        pd_total_dataset_loc.loc[pd_total_dataset_loc['ID_book'] == idbook, 'book_done'] = 1
    return pd_total_dataset_loc

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
        #libs_books_dataframe = pd.DataFrame()

        pd_total_dataset = pd.DataFrame(data = total_dataset)
        #pd_total_dataset['score'] = pd.to_numeric(pd_total_dataset['score'])

    #calcolo score totale potenziale di ogni libreria
    sorted_lib = calculateLibraryScore(pd_total_dataset)

    output = []
    count = 0
    r_days = D
    for index, row in sorted_lib.iterrows():
        one_record = pd_total_dataset[pd_total_dataset["ID_lib"] == row['ID_lib']].head(1)
        #TODO: dividere processo di signup e calcolo libri perchè mentre un libro sta in copia una libreria può fare il signup
        if r_days > one_record['signup_days'].item():
            d = {
                'line1': [],
                'line2': []
            }
            d['line1'].append(one_record['ID_lib'].item())
            r_days = r_days - one_record['signup_days'].item()
            #libri fatti
            n_books_done = pd_total_dataset[(pd_total_dataset["ID_lib"] == row['ID_lib']) & (pd_total_dataset["book_done"] == 1)].shape[0]
            numlib = (r_days * one_record['books_per_day'].item())
            n = 0
            if (one_record['num_books'].item() - n_books_done) < numlib:
                d['line1'].append(one_record['num_books'].item() - n_books_done)
                n = one_record['num_books'].item() - n_books_done
            else:
                d['line1'].append(numlib - n_books_done)
                n = numlib  - n_books_done

            df1 = pd_total_dataset[(pd_total_dataset["ID_lib"] == row['ID_lib']) & (pd_total_dataset["book_done"] == 0)]
            df2_sorted = df1.sort_values(by=["score"], ascending=False)
            first_n_books = df2_sorted[:int(n)]['ID_book']
            d['line2'] = list(first_n_books)
            output.append(d)
            count += 1

            pd_total_dataset = updateLibDone(pd_total_dataset, first_n_books)


    with open("result/result"+input_file, 'w+') as my_file:
        my_file.write(str(count) + "\n")
        for o in output:
            for item in o['line1']:
                my_file.write("%s " % int(item))
            my_file.write("\n")
            for item in o['line2']:
                my_file.write("%s " % int(item))
            my_file.write("\n")
    break
