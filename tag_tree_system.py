# This file is used to manage the tag tree, it can add new tag, add parent tag, add synonym, delete tag, search tag and print tag info.

import re
import classes
import pic_data_functions as dataFn

def parseCommand(command):
    global Tree, history
    if command == "help": # print help
        print("an [newTag] [parentTag]: add a new tag to the parent tag, the new tag must not exist in the tree\n"
              "ap [subTag] [parentTag(s)]: add parent tag(s) to the sub tag, you can add more than one parent tag at once, tags in this command must exist in the tree\n"
              "as [synonym(s)] [tag]: add synonym(s) to the tag, you can add more than one synonym at once, tag must exist in the tree\n"
              "del [tag] [parentTag]: delete a tag from the parent tag, the tag must exist in the parent tag. If the tag has no parent tag, it will be deleted from the tree\n"
              "st [tag]: search for a tag, then show all parent tags, synonym and sub tags of the tag\n"
              "s: save the tag tree\n"
              "ud: undo the last operation\n"
              "exit: exit the program\n")
        return
        
    elif command == "s": # save tag tree
        print("saving...")
        dataFn.writeJson(Tree.toDict(), "", "tag_tree.json")
        print("tag tree saved")
        return

    elif command == "exit": # exit the program
        print("exiting...")
        dataFn.writeJson(Tree.toDict(), "", "tag_tree.json")
        print("tag tree saved")
        return

    elif command == "ud": # undo the last operation
        if len(history) > 1:
            _, undone_operation = history.pop()
            Tree = classes.TagTree(history[-1][0])
            print(f"Undone operation: {undone_operation}")
        else:
            print("no operation to undo")
        return
    
    else: # process command with parameters
        command = command.split(" ")
        if command[0] == "an": # add new tag
            Tree.addNewTag(command[1], command[2])
            history.append((Tree.toDict(), f"Added new tag {command[1]} to {command[2]}"))
            return

        elif command[0] == "ap": # add parent tag
            for parentTag in command[2:]:
                Tree.addParentTag(command[1], parentTag)
            history.append((Tree.toDict(), f"Added parent tag(s) {', '.join(command[2:])} to {command[1]}"))
            return

        elif command[0] == "as": # add synonym
            for synonym in command[1:-1]:
                Tree.tagDict[command[-1]].addSynonym(synonym)
            history.append((Tree.toDict(), f"Added synonym(s) {', '.join(command[1:-1])} to {command[-1]}"))
            return

        elif command[0] == "del": # delete tag
            Tree.deleteTag(command[1], command[2])
            history.append((Tree.toDict(), f"Deleted tag {command[1]} from {command[2]}"))
            return

        elif command[0] == "st": # search tag and print info
            try:
                tagInfo = Tree.tagDict[command[1]].toDict()[command[1]]
                print(f"Parent tags: {', '.join(tagInfo['parent'])}\n"
                      f"Sub tags: {', '.join(tagInfo['subTags'])}\n"
                      f"Synonyms: {', '.join(tagInfo['synonyms'])}")
                return
            except KeyError:
                print("tag not found")
                return

        else:
            print("invalid command")
            return
        
# load tag tree
Tree = dataFn.loadTagTree()
history = [(Tree.toDict(), "Initial state")]

print("tag tree loaded")
userInput = ""
print("Enter command to manage tag tree, use simicolon to separate multiple commands, enter 'help' to see all commands, enter 'exit' to exit.")
while userInput != "exit":
    userInput = input()
    userInput = userInput.split(";")# split multiple commands
    for command in userInput:
        command = re.sub(r"\s+", " ", command) # remove extra spaces
        command = command.strip() # remove spaces at the beginning and end
        if command != "":
            parseCommand(command)
            print("\n")