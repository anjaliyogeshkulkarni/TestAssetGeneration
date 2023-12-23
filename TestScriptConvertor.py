import pandas as pd
from vertexai.language_models import CodeGenerationModel

def readTestData(fileName,sheetName):
    testSteps = pd.read_excel(fileName,sheetName)
    return testSteps

def createPrompt(testSteps):
    prompt = "Generate TestNG Selenium code for following test steps. "
    for index in testSteps.index:
        prompt = prompt + "\n" + testSteps['Action'][index] + " " + testSteps['InputData'][index] + " " + testSteps['Locator'][index]
    return prompt

def createTestcase(prompt):
    generation_model = CodeGenerationModel.from_pretrained("code-bison@001")
    response = generation_model.predict(
        prefix=prompt,
        temperature=0,
        max_output_tokens=800)
    return response.text

def writeToFile(seleniumTestcase,sheetName):
    fName = "D:\\Anjali\\TestAssetGeneration\\TestAssests\\AutomatedScripts\\" + sheetName + ".java"
    f = open(fName, "w")
    f.write(seleniumTestcase)
    f.close()
    print(sheetName)

#Testcase generation
if __name__ == '__main__':

    #read file for teststeps
    fileName = 'D:\Anjali\TestAssetGeneration\TestAssests\ManualTestcases.xlsx'
    print ("Converting manual testcases from file : ",fileName)

    # get sheet name
    xls = pd.ExcelFile(fileName)
    sheets = xls.sheet_names

    print ("Teststeps converted from following sheets:")

    # iterate over the sheets array to generate testscripts for a fucntionality
    for sheetName in sheets:

        testSteps = readTestData(fileName, sheetName)

        # convert each row of the sheet to a prompt
        prompt = createPrompt(testSteps)

        # prompt sent to API as inout
        seleniumTestcase = createTestcase(prompt)

        writeToFile(seleniumTestcase,sheetName)