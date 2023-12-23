import pandas as pd
from vertexai.language_models import TextGenerationModel

def readTestData(fileName,sheetName):
    testDataAttributes = pd.read_excel(fileName,sheetName)
    return testDataAttributes

def createPrompt(testDataAttributes):
    prompt = "Generate testdata in CSV format to test Employee details screen with fields : " + "\n"

    for rowCount, (index,attributeName) in enumerate(testDataAttributes.iterrows()):
        #prompt = prompt + attributeName[0]
        prompt = prompt + attributeName.iloc[0]
        if (rowCount != len(testDataAttributes) - 1):
            prompt = prompt + " , "

    prompt = prompt + "\nGenerate 10 records.\n"

    for index in testDataAttributes.index:
        if (testDataAttributes['FewShotsValues'][index] != " "):
            prompt = prompt + "Few-shots for " + testDataAttributes['AttributeName'][index] + " : \n" + testDataAttributes['FewShotsValues'][index]
    return prompt

def createTestData(prompt):
    generation_model = TextGenerationModel.from_pretrained("text-bison@001")
    response = generation_model.predict(
        prompt=prompt,
        temperature=0.99,
        max_output_tokens=800)
    return response.text

def writeToFile(outputFolderName,content,fileName):
    fName = outputFolderName + fileName
    f = open(fName, "w")
    f.write(content)
    f.close()

#Testdata generation
if __name__ == '__main__':

    #read file for generating testdata
    inputFileName = 'D:\Anjali\TestAssetGeneration\TestAssests\TestDataAttributes.xlsx'
    outputFolderName = "D:\\Anjali\\TestAssetGeneration\\TestAssests\\TestData\\"

    print ("Generating testdata. Data attributes from file : ",inputFileName)

    # get sheet name
    xls = pd.ExcelFile(inputFileName)
    sheets = xls.sheet_names

    # iterate over the sheets array to generate testscripts for a fucntionality
    for sheetName in sheets:

        testDataAttributes = readTestData(inputFileName, sheetName)

        # convert each row of the sheet to a prompt
        prompt = createPrompt(testDataAttributes)

        fileName = sheetName + "-Prompt"+".txt"
        writeToFile(outputFolderName,prompt,fileName)

        # prompt sent to API as inout
        testData = createTestData(prompt)

        fileName = sheetName + ".csv"
        writeToFile(outputFolderName,testData,fileName)
        print("Testdata created for sheet:" + sheetName)


