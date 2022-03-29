import creopyson

from tkinter import *
from tkinter import filedialog


class MainWindow:
    def __init__(self, win):
        self.c = creopyson.Client()
        self.c.connect()
        self.c.creo_set_creo_version(7)
        self.currentWorkFolderPathLabel = Label(win, text="Katalog Roboczy")
        self.currentWorkFolderPathInputField = Entry()
        self.currentWorkFolderPathInputField.insert(0, self.c.creo_pwd())
        self.currentWorkFolderPathButton = Button(win, text="Wybierz")
        self.boxHeightLabel = Label(win, text="Wysokość pudełka")
        self.boxHeightInputField = Entry()
        self.boxLengthLabel = Label(win, text="Długość pudełka")
        self.boxLengthInputField = Entry()
        self.boxDepthLabel = Label(win, text="Głebokość pudełka")
        self.boxDepthInputField = Entry()
        self.textHeightLabel = Label(win, text="Wysokość tekstu")
        self.textHeightInputField = Entry()
        self.textDistFromBoxEdgeLabel = Label(win, text="Odległość tekstu od krawędzi pudełka")
        self.textDistFromBoxEdgeInputField = Entry()
        self.textDepthLabel = Label(win, text="Głębokość tekstu")
        self.textDepthInputField = Entry()
        self.submitButton = Button(win, text="Zapisz wymiary")
        self.currentWorkFolderPathLabel.pack()
        self.currentWorkFolderPathInputField.pack(fill="both")
        self.currentWorkFolderPathButton.pack()
        self.boxHeightLabel.pack()
        self.boxHeightInputField.pack(fill="both")
        self.boxLengthLabel.pack()
        self.boxLengthInputField.pack(fill="both")
        self.boxDepthLabel.pack()
        self.boxDepthInputField.pack(fill="both")
        self.textHeightLabel.pack()
        self.textHeightInputField.pack(fill="both")
        self.textDistFromBoxEdgeLabel.pack()
        self.textDistFromBoxEdgeInputField.pack(fill="both")
        self.textDepthLabel.pack()
        self.textDepthInputField.pack(fill="both")
        self.submitButton.pack()
        self.submitButton.bind("<Button-1>", self.save_values)
        self.currentWorkFolderPathButton.bind("<Button-1>", self.choose_working_dir)

    def choose_working_dir(self, event):
        path = filedialog.askdirectory(title='Wybierz katalog roboczy')
        self.currentWorkFolderPathInputField.delete(0, END)
        self.currentWorkFolderPathInputField.insert(0, path)

    def save_values(self, event):
        # ! Error Handling
        boxLength = float(self.boxLengthInputField.get())
        boxHeight = float(self.boxHeightInputField.get())
        boxDepth = float(self.boxDepthInputField.get())

        textDepth = float(self.textDepthInputField.get())
        textHeight = float(self.textHeightInputField.get())
        textDistanceFromEdge = float(self.textDistFromBoxEdgeInputField.get())

        workingDirectory = self.currentWorkFolderPathInputField.get()

        self.c.parameter_set("W", boxDepth)
        self.c.parameter_set("L", boxLength)
        self.c.parameter_set("H", boxHeight)

        self.c.parameter_set("T_H", textHeight)
        self.c.parameter_set("T_L", textDistanceFromEdge)
        self.c.parameter_set("T_W", textDepth)

        # If sth does't exist make it
        self.c.creo_cd(workingDirectory)

        self.c.file_regenerate()

    def get_current_values(self):
        self.c.parameter_list()


window = Tk()
mainwin = MainWindow(window)
window.title('Kamil Madej Projekt 1')
window.geometry("500x400")
window.mainloop()

"""
def input_validator(input):
    try:
        float(input)
    except:
        raise ValueError
    return input



c = creopyson.Client()

c.connect()

c.creo_set_creo_version(7)

print(c.is_creo_running())

print(c.creo_pwd())

try:
    boxLength = input_validator(input("Podaj długość kostki: "))
except ValueError:
    print("Value out of reach")
    # print("Wpisz poprawną wartość parametru!")

"""
