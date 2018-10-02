import glob
import os

dirPath = os.path.dirname(os.path.realpath(__file__))
pattern = os.path.join(dirPath, '../', 'FALLOUT DATA/*.xlsx')


input('Press enter to move files')
# Move files
old_files = glob.glob(pattern)
for f in old_files:
    new_file = f.replace('FALLOUT DATA', 'FALLOUT DATA/ARCHIVE')
    print(f)
    print(new_file)
    os.rename(f, new_file)

filesDict = {'CHARTER-NORTHEAST-SOUTHERN NEW ENGLAND': '1',
             'CHARTER-NYC-BROOKLYN-QUEENS': '2',
             'CHARTER-NYC-N MANHATTAN  STATEN ISLAND': '3'}

input('Press enter to rename files')
new_files = glob.glob(pattern)
new_files.sort(key=os.path.getmtime)

for i, (key, value) in enumerate(filesDict.items()):
    print(i, key, value)
    old_name = new_files[i]
    new_name = old_name.replace('EZTracking_BulkUploadErrorReport', key)
    print(old_name)
    print(new_name)
    os.rename(old_name, new_name)
