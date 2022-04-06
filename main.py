import os.path
import creopyson
from tkinter import *
from tkinter import filedialog


class MainWindow:
    def __init__(self, win):
        super().__init__()
        win.columnconfigure(0, weight=1)
        win.columnconfigure(1, weight=3)
        self.c = creopyson.Client()
        self.c.connect()
        self.c.creo_set_creo_version(7)
        self.currentWorkFolderPathLabel = Label(win, text="Katalog Roboczy")
        self.currentWorkFolderPathInputField = Entry()
        self.currentWorkFolderPathInputField.insert(0, self.c.creo_pwd())
        self.currentWorkFolderPathButton = Button(win, text="Wybierz")
        self.currentFileLabel = Label(win, text="Wybierz plik")
        self.currentFileButton = Button(win, text="Wybierz plik")
        self.materialChooseLabel = Label(win, text="Materiał z grupy Ferrous_metals")
        materialsList = ["Steel_cast", "Stainless_steel_ferritic", "Steel_HSLA", "Tool_steel_high_speed",
                         "Steel_low_carbon", "Steel_medium_carbon", "Steel_high_carbon", "Cast_iron_ductile",
                         "Stainless_steel_austenitic" "Steel_galvanized", "Tool_steel_water_hardening"]
        self.optionVar = StringVar(win)
        self.optionVar.set(materialsList[0])
        self.materialChooseMenu = OptionMenu(win, self.optionVar, *materialsList)
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
        self.textValueLabel = Label(win, text="Napis")
        self.textValueInputField = Entry()
        self.submitButton = Button(win, text="Zapisz wymiary")
        self.currentWorkFolderPathLabel.pack()
        self.currentWorkFolderPathInputField.pack(fill="both")
        self.currentWorkFolderPathButton.pack()
        self.currentFileLabel.pack()
        self.currentFileButton.pack()
        self.materialChooseLabel.pack()
        self.materialChooseMenu.pack(fill="both")
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
        self.textValueLabel.pack()
        self.textValueInputField.pack(fill="both")
        self.submitButton.pack()
        self.currentWorkFolderPathButton.bind("<Button-1>", self.choose_working_dir)
        self.currentFileButton.bind("<Button-1>", self.choose_file)
        self.submitButton.bind("<Button-1>", self.save_values)

    def choose_working_dir(self, event):
        path = filedialog.askdirectory(title='Wybierz katalog roboczy')
        self.currentWorkFolderPathInputField.delete(0, END)
        self.currentWorkFolderPathInputField.insert(0, path)
        self.c.creo_cd(path)

    def choose_file(self, event):
        filePath = filedialog.askopenfile(title="Wybierz plik", filetypes=[("Part name", "*.prt")])
        fileName = os.path.basename(filePath.name)
        print(fileName)
        self.c.file_open(fileName)

    def save_values(self, event):
        material = self.optionVar.get()
        # self.c.file_load_material_file(material,"C:/Program Files/PTC/Creo 7.0.1.0/Common Files/text/materials-library/Standard-Materials_GrantaDesign")
        self.c.file_load_material_file(material,
                                       "D:/Creo/Creo 7.0.1.0/Common Files/text/materials-library/Standard-Materials_Granta-Design/Ferrous_metals")
        self.c.file_set_cur_material(material)

        # TODO Error Handling
        boxLength = float(self.boxLengthInputField.get())
        boxHeight = float(self.boxHeightInputField.get())
        boxDepth = float(self.boxDepthInputField.get())

        textDepth = float(self.textDepthInputField.get())
        textHeight = float(self.textHeightInputField.get())
        textDistanceFromEdge = float(self.textDistFromBoxEdgeInputField.get())

        textValue = self.textValueInputField.get()

        workingDirectory = self.currentWorkFolderPathInputField.get()

        self.c.parameter_set("W", boxDepth)
        self.c.parameter_set("L", boxLength)
        self.c.parameter_set("H", boxHeight)

        self.c.parameter_set("T_H", textHeight)
        self.c.parameter_set("T_L", textDistanceFromEdge)
        self.c.parameter_set("T_W", textDepth)

        self.c.parameter_set("TEXT", textValue)

        self.c.creo_cd(workingDirectory)

        self.c.file_regenerate()

    def get_current_values(self):
        self.c.parameter_list()


window = Tk()
mainwin = MainWindow(window)
window.title('Kamil Madej Projekt 1')
window.geometry("800x600")
window.mainloop()
print("KONIEC")
