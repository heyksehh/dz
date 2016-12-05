import urllib.request
import re

def pages_list ():
    f = open ('.\\links.txt', 'r', encoding = 'utf-8')
    links = f.readlines ()
    return links

def texts (links):
    array = []
    for l in links:
        arr = []
        page = urllib.request.Request (l)
        with urllib.request.urlopen(page) as response:
            link = response.read().decode('utf-8')
        regtext = re.compile('<p>(.*?)</p>')
        text = regtext.findall (link)
        for line in text:
            words0 = line.split ()
            for word in words0:
                word0 = word.lower ()
                word1 = word0.strip('—–-…№&,./"<>=\«»:;!?()0123456789')
                if '>' in word1:
                    word1 = ''
                if '=' in word1:
                    word1 = ''
                if '<' in word1:
                    word1 = ''
                if '/' in word1:
                    word1 = ''
                if '.' in word1:
                    word1 = ''
                if word1 != '':
                    arr.append (word1)
                x = set(arr)
        array.append (x)
    return (array)

def mnozh (array):
    set1 = array[0]
    set2 = array[1]
    set3 = array[2]
    set4 = array[3]
    set5 = array[4]
    set_common = set1 & set2 & set3 & set4 & set5
    set_com = sorted (set_common)
    f1 = open ('.\\intersection.txt', 'w', encoding = 'utf-8')
    f1.write ('Общие для всех заметок слова:\n') 
    for word in set_com:
        f1.write (word + '\n')
    f1.close ()

    print (set_com)


    s1 = set2 | set3 
    s2 = set1 | set3 
    s3 = set1 | set2 
    s4 = set1 | set2 
    s5 = set1 | set2
    
    dif1 = set1 - s1
    dif2 = set2 - s2
    dif3 = set3 - s3
    dif4 = set4 - s4
    dif5 = set5 - s5
    
    d1 = sorted (dif1)
    d2 = sorted (dif2)
    d3 = sorted (dif3)
    d4 = sorted (dif4)
    d5 = sorted (dif5)

    f2 = open ('.\\symmetric_difference.txt', 'w', encoding = 'utf-8')
    f2.write ('Уникальные слова для заметки №1:\n')
    for elem1 in d1:
        f2.write (elem1 + '\n')
    f2.write ('\nУникальные слова для заметки №2:\n')
    for elem2 in d2:
        f2.write (elem2 + '\n')
    f2.write ('\nУникальные слова для заметки №3:\n')
    for elem3 in d3:
        f2.write (elem3 + '\n')
    f2.write ('\nУникальные слова для заметки №4:\n')
    for elem4 in d4:
        f2.write (elem4 + '\n')
    f2.write ('\nУникальные слова для заметки №5:\n')
    for elem5 in d5:
        f2.write (elem5 + '\n')
    f2.close ()
            
def main ():
    fun1 = pages_list ()
    fun2 = texts (fun1)
    fun3 = mnozh (fun2)
    
if __name__ == '__main__':
    main() 
