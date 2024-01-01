# main process of the program (with UI)
import program_objects as progObjs
import pic_data_functions as dataFn
import pic_file_functions as fileFn
import program_functions as progFn



# just for test

# from cfg
# picDataPath = "D:/Pixiv_Pictures/pixiv_picture_data"
# picFilePath = "D:/Pixiv_Pictures/pixiv"

tagTree = dataFn.loadTagTree()

# parent = tagTree.getAllParentTag(includeSynonyms=True)

# for i in parent:
#     print(f"{i}: {parent[i]}")

for i in tagTree.tagDict.keys():
    print(i)