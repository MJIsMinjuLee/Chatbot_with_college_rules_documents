import aspose.words as aw
import re
import os

filePath = "currentFilePath"
files = [f for f in os.listdir(filePath) if re.match('.*[.]pdf', f)]

for file in files :
    pre, ext = os.path.splitext(file)
    file = os.path.join(filePath, pre + ".pdf")
    doc = aw.Document('../docs/{name}.pdf'.format(name = pre))
    doc.save('../docs/{name}.txt'.format(name = pre))
