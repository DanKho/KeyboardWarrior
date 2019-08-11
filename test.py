from tkinter import  *
root = Tk()
test_word = "hello"
check_list = []
letter_num = 0

for i in test_word:
    check_list.append(i)

def checkInput(event):
    global letter_num
    letter = event.char
    if check_list[letter_num] == letter:
        print("Correct: ", letter)
        letter_num += 1
    else:
        print("incorrect: ", letter)

root.bind("<Key>", checkInput)
root.mainloop()

