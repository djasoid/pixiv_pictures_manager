import os

def convert_ui_files(ui_directory, output_directory):
    for root, dirs, filenames in os.walk(ui_directory):
        for name in filenames:
            if not name.endswith(".ui"):
                continue
            outName = name[:-3]
            input_path = os.path.join(root, name)
            output_path = os.path.join(output_directory, "Ui_" + outName + ".py")
            command = f"pyside6-uic {input_path} -o {output_path}"
            sts = os.system(command)
            if sts != 0:
                print(f"Error processing {name}")
                break

if __name__ == "__main__":
    ui_directory = "./ui/"
    output_directory = "./src/ui_compiled/"
    convert_ui_files(ui_directory, output_directory)
    print('Finished!')