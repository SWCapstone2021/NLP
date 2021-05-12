from basefunction.FindUMethod import Ctrl_F, MakeVttFile

if __name__=="__main__":
    i=input("기능번호:")
    
    if i=='1':
        URL=input("URL:")
        MakeVttFile(URL)
    if i=='2':
        SearchingValue = input("키워드입력:")
        URL=input("URL:")
        Ctrl_F(SearchingValue,'URL')