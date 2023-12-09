# This file is used to manage the tag tree, it can add new tag, add parent tag, add synonym, delete tag, search tag and print tag info.

import classes
import pic_data_functions as dataFn

Tree = dataFn.loadTagTree()
history = [(Tree.toDict(), "Initial state")]

print("tag tree loaded\n")
userInput = ""
while userInput != "exit":
    print("Enter command to manage tag tree, enter 'help' for help, enter 'exit' to exit.\n")
    userInput = input()
    if userInput == "help": # print help
        print("an [newTag] [parentTag]: add a new tag to the parent tag, the new tag must not exist in the tree\n"
              "ap [subTag] [parentTag(s)]: add parent tag(s) to the sub tag, you can add more than one parent tag at once, tags in this command must exist in the tree\n"
              "as [synonym(s)] [tag]: add synonym(s) to the tag, you can add more than one synonym at once, tags in this command must exist in the tree\n"
              "del [tag] [parentTag]: delete a tag from the parent tag, the tag must exist in the parent tag. If the tag has no parent tag, it will be deleted from the tree\n"
              "st [tag]: search for a tag, then show all parent tags, synonym and sub tags of the tag\n"
              "s: save the tag tree\n"
              "ud: undo the last operation\n"
              "exit: exit the program\n")
        
    elif userInput == "s": # save tag tree
        print("saving...\n")
        dataFn.writeJson(Tree.toDict(), "", "tag_tree.json")
        print("tag tree saved\n")
        continue

    elif userInput == "exit": # exit the program
        print("exiting...\n")
        dataFn.writeJson(Tree.toDict(), "", "tag_tree.json")
        print("tag tree saved\n")
        continue

    elif userInput == "ud": # undo the last operation
        if len(history) > 1:
            _, undone_operation = history.pop()
            Tree = classes.TagTree(history[-1][0])
            print(f"Undone operation: {undone_operation}\n")
        else:
            print("no operation to undo\n")
        continue
    
    else: # process command with parameters
        userInput = userInput.split(" ")
        if userInput[0] == "an": # add new tag
            Tree.addNewTag(userInput[1], userInput[2])
            history.append((Tree.toDict(), f"Added new tag {userInput[1]} to {userInput[2]}"))

        elif userInput[0] == "ap": # add parent tag
            for parentTag in userInput[2:]:
                Tree.addParentTag(userInput[1], parentTag)
            history.append((Tree.toDict(), f"Added parent tag(s) {', '.join(userInput[2:])} to {userInput[1]}"))

        elif userInput[0] == "as": # add synonym
            for synonym in userInput[1:-1]:
                Tree.tagDict[userInput[-1]].addSynonym(synonym)
            history.append((Tree.toDict(), f"Added synonym(s) {', '.join(userInput[1:-1])} to {userInput[-1]}"))

        elif userInput[0] == "del": # delete tag
            Tree.deleteTag(userInput[1], userInput[2])
            history.append((Tree.toDict(), f"Deleted tag {userInput[1]} from {userInput[2]}"))

        elif userInput[0] == "st": # search tag and print info
            try:
                tagInfo = Tree.tagDict[userInput[1]].toDict()[userInput[1]]
                print(f"Parent tags: {', '.join(tagInfo['parent'])}\n"
                      f"Sub tags: {', '.join(tagInfo['subTags'])}\n"
                      f"Synonyms: {', '.join(tagInfo['synonyms'])}\n")
                continue
            except KeyError:
                print("tag not found\n")
                continue

        else:
            print("invalid command\n")