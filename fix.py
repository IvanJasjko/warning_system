import pandas

def restore():

    main_data = pandas.read_csv("../keys/Data.csv",encoding='utf-8-sig')
    main_data["Text"].replace(regex=True, inplace=True, to_replace=r'\n|\r|\t', value=r'')
    main_data["Translation"].replace(regex=True, inplace=True, to_replace=r'\n|\r|\t', value=r'')
    main_data.loc[main_data.User_ID != 4264276227, "Source"] = False
    main_data.to_csv("../keys/Data.csv",encoding='utf-8-sig',index=False)
    print("Sources Updated")
    


if __name__ == '__main__':
    restore()
