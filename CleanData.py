import os
import json
from stanfordcorenlp import StanfordCoreNLP


def clean_data(soup,save_name,nlp):
    soup['email'] = []
    if soup['institute'] != []:
        for a in soup['institute']:
            i = 0
            while i < len(a):
                if '@' in a[i]:
                    str0 = ''
                    soup['email'].append((str0.join(a)).split())
                    soup['institute'].remove(a)
                    break
                else:
                    i += 1

    j = 0
    for a in soup['author']:
        i = 0
        while i < len(a):
            if '@' in a[i]:
                soup['email'].append(a[i].split())
                del soup['author'][j][i]
                break
            else:
                i += 1
        j += 1

    if soup['institute'] == []:
        j = 0
        for a in soup['author']:
            i = 0
            while i < len(a):
                for b in nlp.ner(a[i]):
                    if 'ORGANIZATION' in b:
                        str0 = ''
                        tar = str0.join(a[i])
                        soup['institute'].append(list(tar.split('$')))
                        soup['author'][j].remove(a[i])
                        break
                i += 1
            j += 1
    else:
        j = 0
        for a in soup['author']:
            i = 0
            while i < len(a):
                for b in nlp.ner(a[i]):
                    if 'ORGANIZATION' in b:
                        str0 = ''
                        tar = str0.join(a[i])
                        if j > len(soup['institute']):
                            soup['institute'].append(list(tar.split('$')))
                        else:
                            soup['institute'].insert(j, list(tar.split('$')))
                        soup['author'][j].remove(a[i])
                        break
                i += 1
            j += 1
    if soup['email'] != []:
        j = 0
        for a in soup['email']:
            if len(a) > 1:
                soup['email'][j] = list((''.join(a)).split())
        j += 1
    json.dump(soup, open(save_name, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)


if __name__ == "__main__":
    path = r'C:\Users\Songxiao Yang\Desktop\TASK\Ans0'
    save_path = r'C:\Users\Songxiao Yang\Desktop\TASK\Ans1'
    files = os.listdir(path)  # 获得文件夹中所有文件的名称列表
    nlp = StanfordCoreNLP(r'C:\Users\Songxiao Yang\Desktop\TASK\stanford-corenlp-full-2018-10-05')
    for file in files:
        f = open(path + "/" + file, "r", encoding="utf-8")
        soup = json.load(f)
        save_name = os.path.join(save_path, file)
        clean_data(soup,save_name,nlp)
        print(file, "is cleaned completely!")
    print("metadata has been cleaned successfully!")






