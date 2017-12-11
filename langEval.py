import ast
import language_check
import progressbar
with open("Raw/parsed.json", "r") as dataFile:
    corpus = ast.literal_eval(dataFile.read())

corpus = [i.encode('ascii', 'ignore').decode('ascii') for i in list(corpus.keys())+list(corpus.values())]
lang_tool = language_check.LanguageTool("en-US")
count = 0
errorCount = 0
bar = progressbar.ProgressBar()
for i in bar(corpus):
    count += 1
    errors = lang_tool.check(i)
    if len(errors) > 0:
        errorCount += 1

print("Correct Rate: ", str(((count-errorCount)/count)*100)+"%")
