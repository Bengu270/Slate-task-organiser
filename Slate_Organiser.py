import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import date

# Window setup
root = ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("300x400+1400+60")
root.title("Slate - Organiser")

# Stylings
font1 = "Consolas"
colour1 = "#a2ded8"
colour2 = "#2B2B2B"
colour3 = "#365c58"

# Memory storage
memory = "Slate_Memory.txt"
memoryFile = open(memory, "r")
memoryList = [line.strip() for line in memoryFile.readlines()]
memoryFile.close()

# Widgets
titleLabel = ctk.CTkLabel(root, 
                         text = "SLATE", 
                         anchor = "e", 
                         font = (font1, 24, "bold"),
                         text_color = colour1
                         )
titleLabel.pack(padx = 40, 
               pady = 5, 
               fill = "x"
               )


divider = ctk.CTkFrame(root,
                       height = 4,
                       fg_color = colour3,
                       bg_color ="transparent"
                       )
divider.pack(fill = "x", 
             padx = 40, 
             pady = 3
             )


todoLabel = ctk.CTkLabel(root, 
                         text = "To-dos", 
                         anchor = "w", 
                         font = (font1, 16),
                         text_color = colour1
                         )
todoLabel.pack(padx = 40, 
               pady = 5, 
               fill = "x"
               )


todoFrame = ctk.CTkFrame(root, 
                         corner_radius = 10,
                         )
todoFrame.pack(padx = 20, 
               pady = 5, 
               fill="x", 
               expand=True, 
               side = "top", 
               anchor = "n"
               )
todoFrame.pack_propagate(True)


def createTodoCheckBox(event=None, input=None, destroy = True):
    # Either takes an input or takes input from the todo entry box
    if input != None:
        text = input.strip()
    else:
        text = "- " + todoEntry.get()
        memoryFile = open(memory,"a")
        memoryFile.write(str("- " + todoEntry.get() + "\n"))
        memoryFile.close()
        memoryList.append(str("- " + todoEntry.get())) 
    
    # If entry box not blank, create checkbox
    if text.strip():

        def onClick():
            todoCheckBox.destroy()
            remove = memoryList.index(todoCheckBox.cget("text"))

            if " -r:" not in memoryList[remove]: # Will not remove if its a repeatable to-dos
                memoryList.pop(remove)

                memoryFile = open(memory, "w")
                for element in memoryList:
                    memoryFile.write(str(element + "\n"))
                memoryFile.close()
        
        todoCheckBox = ctk.CTkCheckBox(todoFrame, 
                                       text = text,
                                       font = (font1, 16),
                                       text_color = colour1,
                                       command = onClick
                                       )
        todoCheckBox.pack(
                       padx =20,
                       pady = 5,
                       anchor = "w",
                       fill = "x",
                       before = todoEntry
                       )
        
        todoEntry.delete(0, "end")
    return


todoEntry = ctk.CTkEntry(todoFrame)
todoEntry.pack(padx = 20,
               pady = 15,
               anchor = "w"
               )
todoEntry.bind("<Return>", createTodoCheckBox) # Binds enter key to make new checkbox


# New window for adding timed to-dos
def newSubRoot(event=None):
    subRoot = ctk.set_appearance_mode("dark")
    subRoot = ctk.CTk()
    subRoot.geometry("300x300+950+60")
    subRoot.title("Slate - Add")

    
    addLabel = ctk.CTkLabel(subRoot, 
                            text = "New item:", 
                            anchor = "w", 
                            font = (font1, 16),
                            text_color = colour1
                            )
    addLabel.pack(padx = 40, 
                   pady = 5, 
                   fill = "x"
                   )
    

    addEntry = ctk.CTkEntry(subRoot,
                            height = 40,
                            width = 200,
                            )
    addEntry.pack(padx = 40,
                  pady = 10,
                  anchor = "w"
                  )
    
    addDateEntry = DateEntry(subRoot, 
                             width=24, 
                             background=colour3, 
                             foreground=colour2,
                             borderwidth=4
                             )
    addDateEntry.pack(padx=60,
                      pady=10, 
                      anchor="w"
                      )
    
    addRepeatEntry = ctk.CTkEntry(subRoot,
                                  height = 30,
                                  width = 100
                                  )
    addRepeatEntry.pack(padx = 40,
                        pady = 10,
                        anchor = "w"
                        )


    def createListElement():
        text = str(addEntry.get())
        date = addDateEntry.get_date()
        repeat = str(addRepeatEntry.get())
        repeating = False
        if repeat.strip(): # Checks if the number of repeats is an integer value, ignores if not
            try:
                repeat = int(repeat)
                repeating = True
            except:
                return
        
        if text.strip(): # Checks for text in entry box
            # Checks if repeat is used
            if repeating == True:
                listElement = "- " + text.strip() + " -r:" + str(repeat) + "/" + str(repeat) + "#" + str(date.strftime("%d/%m/%Y"))
            else:
                listElement = "- " + text.strip() + "#" + str(date.strftime("%d/%m/%Y"))
            memoryList.append(listElement)
            memoryFile = open(memory, "w")
            for element in memoryList:
                memoryFile.write(str(element + "\n"))
            memoryFile.close()

            subRoot.destroy()
        return


    submitButton = ctk.CTkButton(subRoot,
                                 text = "Submit",
                                 width = 50,
                                 height = 50,
                                 corner_radius = 50,
                                 fg_color=colour3,
                                 hover_color = colour2,
                                 font = (font1, 16),
                                 command = createListElement
                                 )
    submitButton.pack(padx = 20, 
                      pady = 20,
                      anchor = "e"
                      )


    subRoot.mainloop()
    return

# Button to create new window
addButton = ctk.CTkButton(root,
                          text = "+",
                          width = 50,
                          height = 50,
                          corner_radius = 50,
                          font = (font1, 28),
                          fg_color=colour3,
                          hover_color = colour2,
                          command = newSubRoot
                          )
addButton.pack(padx = 20, 
               pady = 20,
               anchor = "e"
               )


# Initiate past lists

today = date.today()
newDay = False

# Checks for date change
oldDate = open("oldDate.txt","r")
oldDay = oldDate.readline()
oldDate.close()
if str(oldDay) != str(today):
    print("trigger")
    newDay = True
    oldDate = open("oldDate.txt","w")
    oldDate.write(str(today))
    oldDate.close()

# Checks for to-dos which are timed or repeats
for listItem in memoryList:
    if "#" in listItem:
        index = listItem.index("#")
        compareDate = listItem[index + 1:]
        if str(compareDate) == str(today.strftime("%d/%m/%Y")):
            newElement = listItem[:index]
            old_index = memoryList.index(listItem)
            memoryList.remove(listItem)
            memoryList.insert(old_index, newElement)
            createTodoCheckBox(input=newElement)
        
    elif " -r:" in listItem and newDay == True:
        index = listItem.index(" -r:") + 4
        repeatDays = int(listItem[index:index + (len(listItem[index:])//2)])
        newRepeatDays = repeatDays-1

        if newRepeatDays == 0:
            newRepeatDays = str(listItem[index + (len(listItem[index:])//2) + 1:])

            newListItem = listItem.replace(str(repeatDays), str(newRepeatDays), 1)
            old_index = memoryList.index(listItem)
            memoryList.remove(listItem)
            memoryList.insert(old_index, newListItem)

            createTodoCheckBox(input=listItem)
        else:
            newListItem = listItem.replace(str(repeatDays), str(newRepeatDays), 1)
            old_index = memoryList.index(listItem)
            memoryList.remove(listItem)
            memoryList.insert(old_index, newListItem)

    elif " -r:" in listItem:
        index = listItem.index(" -r:") + 4
        repeatDays = int(listItem[index:index + (len(listItem[index:])//2)])
        if repeatDays == 0:
            createTodoCheckBox(input=listItem, destroy = False)

    else:
        createTodoCheckBox(input=listItem)

    memoryFile = open(memory, "w")
    for element in memoryList:
        memoryFile.write(str(element + "\n"))
    memoryFile.close()

newDay = False

# Run

root.mainloop()
