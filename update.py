import pandas


def update():

   	
    df = pandas.read_csv("../keys/Warnings.csv",encoding='utf-8-sig')

    data = df["Tweet_ID"].drop_duplicates()
    sources = data.tolist()
    sources.remove("None")



    main_data = pandas.read_csv("../keys/Data.csv",encoding='utf-8-sig')
    main_data["Text"].replace(regex=True, inplace=True, to_replace=r'\n|\r|\t', value=r'')
    main_data["Translation"].replace(regex=True, inplace=True, to_replace=r'\n|\r|\t', value=r'')
    main_data.loc[main_data.Tweet_ID.isin(sources), "Source"] = True
    main_data.to_csv("../keys/Data.csv",encoding='utf-8-sig',index=False)
    print("Sources Updated")
    


if __name__ == '__main__':
    update()

