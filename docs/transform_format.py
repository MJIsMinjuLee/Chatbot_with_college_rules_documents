import win32com.client
import os
import re

hwp = win32com.client.gencache.EnsureDispatch('HWPFrame.HwpObject')
hwp.RegisterModule('FilePathCheckDLL', 'SecurityModule')

getPath = "currentFilePath"
savePath = "currentFilePath"

files = [f for f in os.listdir(getPath) if re.match('.*[.]hwp', f)]

for file in files :
    hwp.Open(os.path.join(getPath, file))
    pre, ext = os.path.splitext(file)
    hwp.HAction.GetDefault("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)
    hwp.HParameterSet.HFileOpenSave.filename = os.path.join(savePath, pre + ".pdf")
    hwp.HParameterSet.HFileOpenSave.Format = "PDF"
    hwp.HAction.Execute("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)

hwp.Quit()