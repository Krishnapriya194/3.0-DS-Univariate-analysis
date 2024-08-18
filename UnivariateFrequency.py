class UnivariatePlacement():
    def quanQual(dataset): 
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            if(dataset[columnName].dtype=='O'):
                 qual.append(columnName)
            else:
                quan.append(columnName)
        return quan,qual
    def Univariate(dataset,quan):
        import pandas as pd
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","Q4:100%","IQR","1.5rule","Lesser","Greater","Min","Max"],columns=quan)
        for columnName in quan:
            descriptive.loc["Mean",columnName]=dataset[columnName].mean()
            descriptive.loc["Median",columnName]=dataset[columnName].median()
            descriptive.loc["Mode",columnName]=dataset[columnName].mode()[0]
            descriptive.loc["Q1:25%",columnName]=dataset.describe()[columnName]["25%"]
            descriptive.loc["Q2:50%",columnName]=dataset.describe()[columnName]["50%"]
            descriptive.loc["Q3:75%",columnName]=dataset.describe()[columnName]["75%"]
            descriptive.loc["Q4:100%",columnName]=dataset.describe()[columnName]["max"]
            descriptive.loc["IQR",columnName]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive.loc["1.5rule",columnName]=1.5*descriptive[columnName]["IQR"]
            descriptive.loc["Lesser",columnName]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5rule"]
            descriptive.loc["Greater",columnName]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5rule"]
            descriptive.loc["Min",columnName]=dataset[columnName].min()
            descriptive.loc["Max",columnName]=dataset[columnName].max()             
        return descriptive
    def OutlierColumn(quan,descriptive):    
        lesser=[]
        greater=[]
        for columnName in quan:
            if(descriptive[columnName]["Min"]<descriptive[columnName]["Lesser"]):
                lesser.append(columnName)
            if(descriptive[columnName]["Max"]>descriptive[columnName]["Greater"]):
               greater.append(columnName)
        return lesser,greater

    def replacing_outliers(descriptive,dataset,lesser,greater):
        for columnName in lesser:
            dataset.loc[dataset[columnName]<descriptive.loc["Lesser",columnName]]=descriptive.loc["Lesser",columnName]
        for columnName in greater:
            dataset.loc[dataset[columnName]>descriptive.loc["Greater",columnName]]=descriptive.loc["Greater",columnName]
        return descriptive

    def freqTable(quan,dataset):
        import pandas as pd
        freqTable=pd.DataFrame(columns=["unique_values","Frequency","Relative_Frequency","Cumsum"])  
        freqTable["unique_values"]=dataset[quan].value_counts().index
        freqTable["Frequency"]=dataset[quan].value_counts().values
        freqTable["Relative_Frequency"]=(freqTable["Frequency"]/103)
        freqTable["Cumsum"]=freqTable["Relative_Frequency"].cumsum()
        return freqTable