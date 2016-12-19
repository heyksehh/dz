import os
import re

def textread ():
    f = open ('.\\text.txt', 'r', encoding = 'utf-8')
    text = f.readlines ()
    arr = []
    for line in text:
        words = line.split ()
        for w in words:
            arr.append (w)
    f.close()
    return arr



def commtokens (arr):
    numid = 0
    numnum = 1
    all_comm_tok = []
    
    for token in arr:
        if token != '﻿-':
            wordform = token.strip ('.,!?..."(«»)0123456789 -')
            if wordform != '':
                symb = list (token)
                if symb[0] not in list (wordform):
                    amark = symb[0]
                else:
                    amark = ''
                symb2 = token.split (wordform)
                if symb2[-1] != wordform:
                    bmark = symb2[-1]
                genercomm = 'INSERT INTO alltokens (id, wordform, amark, bmark, num, lemmaid) \
VALUES (' + str(numid) + ', "' + wordform + '", "' + amark + '", "' + bmark + '", ' + str(numnum) + ', 0)\n' 
                numid += 1
                numnum += 1
                all_comm_tok.append (genercomm)
    return all_comm_tok



def filewithcomm_t (all_comm_tok):
    f = open ('.\\all_comm_tok.txt', 'w', encoding = 'utf-8')
    for line in all_comm_tok:
        f.write (line)
    f.close()


    
def mystem (arr):
    arr1 = []
    x = set ()
    for word in arr:
        if word != '':
            arr1.append (word)
    for w in arr1:
        word0 = w.strip ('.,!?..."()«»0123456789 -')
        word1 = word0.lower ()
        f = open ('.\\source.txt', 'a', encoding = 'utf-8')
        f.write (word1 + '\n')
        f.close ()
        os.system ('C:\\Users\\Ксения\\Desktop\\mystem.exe -cnd source.txt results.txt')
    res = open ('.\\results.txt', 'r', encoding = 'utf-8')
    text = res.readlines ()
    items = []
    for line in text:
        line1 = line.replace('\n', '')
        if '{' in line1:
            x.add (line1)
    for ln in x:
        items.append (ln)
    return items 



def commlemmas (items):
    numid = 0
    all_comm_lem = []
    for item in items:
        item1 = item.strip ('}')
        i = item1.split ('{')
        i0 = i[0]
        i1 = i[1]
        genercomm = 'INSERT INTO alllemmas (id, wordform, lemma) VALUES (' + str(numid) + ', "' + i0 + '", "' + i1 + '")\n' 
        all_comm_lem.append (genercomm)
        numid += 1
    return all_comm_lem


        
def filewithcomm_l (all_comm_lem):
    f = open ('.\\all_comm_lem.txt', 'w', encoding = 'utf-8')
    for line in all_comm_lem:
        f.write (line)
    f.close()



def main ():
    fun1 = textread ()
    fun2 = commtokens (fun1)
    fun3 = filewithcomm_t (fun2)
    fun4 = mystem (fun1)
    fun5 = commlemmas (fun4)
    fun6 = filewithcomm_l (fun5)
    
if __name__ == '__main__':
    main()

