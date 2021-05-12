from basefunction.FindUMethod import *

if __name__=="__main__":
    i=input("기능번호: 1(extract subtitle) or 2(ctrl+F)")
    
    if i=='1':
        URL=input("URL:")
        MakeVttFile(URL)
    if i=='2':
        SearchingValue = input("키워드입력:")
        URL=input("URL:")
        Ctrl_F(SearchingValue,URL)
    if i=='3':
        URL=input("URL:")
        Noun(URL)
        