# main process of the program (with UI)
import classes
import pic_data_functions as dataFn
import pic_file_functions as fileFn
import program_functions as progFn




# from cfg
picDataPath = "D:/Pixiv_Pictures/pixiv_picture_data"
picFilePath = "D:/Pixiv_Pictures/pixiv"

tagTree = dataFn.loadTagTree()


metadataDict = fileFn.getAllData(picFilePath)
dataFn.writeJson(metadataDict, picDataPath, "Metadata.json")