from pymorphy2 import MorphAnalyzer
import random
import telebot

morph = MorphAnalyzer()

    
def lemm_dict (): #делает разбор самых частотных словоформ из списка НКРЯ
    
    f = open ('.\\corpora.txt', 'r', encoding = 'utf-8')
    text = f.readlines ()
    f.close ()
    
    dd = {}
    
    for line in text[:100000]: #самые частотные из самых частотных для более быстрой работы программы
        line1 = line.strip ('\n')
        ana = morph.parse (line1)
        first = ana[0] # первый вариант разбора
        lemm = first.normal_form
        norm_tag_str = str (first.tag)
        all_types_tags = norm_tag_str.split (' ')
        const_tag = all_types_tags[0] # неизменяемые признаки слов
        dd[lemm] = const_tag # словарь, где леммам присвоены неизменяемые признаки
        
    return dd


def hello_user (): # предлагает пользователю ввести фразу

    print ('Давай поиграем: введи любую фразу и увидишь, что получится ;)')
    text = input () 

    return text


def change_the_line (dd, text): # подбирает слова с теми же грамматическими характеристиками, что и заданные пользователем
    
    final_line = ''
    arr1 = []
    arr = text.split (' ')
    for a in arr:
        a1 = a.strip(',.:;()[]-!?...')
        arr1.append (a1)
    
    for word in arr1:
        good_words = [] # массив для подходящих по постоянным признакам слов
        
        ana = morph.parse(word)
        first = ana[0]
        tags1 = str (first.tag)
        tags_arr = tags1.split (' ')
        temp_qual = tags_arr[-1] # непостоянные признаки
        const_qual = tags_arr[0] # постоянные признаки
        tags = temp_qual.split(',') 

        if first.tag.POS == 'PREP': # оставляем предлоги неизменными, чтобы итоговое предложение было согласованным
            new_word = first.word

        else:
            for elem in dd: # получаем подходящие слова
                if dd[elem] == const_qual:
                    good_words.append (elem)
                
            random_word = random.choice (good_words) # выбираем случайный элемент массива
            analyz = morph.parse(random_word)[0]
        
        
            for t in tags: # словоизменение - добавление непостоянных признаков выбранному слову
                form = analyz.inflect({t})
                if form == None: # если нет подходящего слова с такими непостоянными признаками, программа оставляет заданное пользователем слово
                    new_word = word
                    break
                else:
                    analyz = form
                    new_word = form.word

        final_line += new_word + ' '  # присоединяем  слово к итоговой строке 

    return final_line


def print_response (final_line):
    print (final_line)
    
fun1 = lemm_dict ()

def main ():
    fun2 = hello_user ()
    fun3 = change_the_line (fun1, fun2)
    fun4 = print_response (fun3)
    
while __name__ == '__main__':
    main() 


   
