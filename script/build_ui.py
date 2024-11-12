import os

for root, dirs, filenames in os.walk("../ui/"):
    for name in filenames:
        if name[-2:] != "ui":
            continue
        outName = name[:-3]
        sts = os.system(
            "pyside6-uic.exe {}.ui -o {}.py".format(
                os.path.join(root, outName), 
                os.path.join("../src/interface/Ui_", outName)
            )
        )
        pass

print('Finished!')