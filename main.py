import os.path

import creopyson
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class MainWindow:
    def validate_input(self, inp):
        try:
            if inp == "":
                return True
            elif float(inp):
                return True
        except:
            return False

    def __init__(self, win):
        self.c = creopyson.Client()
        self.c.connect()
        self.c.creo_set_creo_version(7)
        win.title('Kamil Madej Projekt 1')
        win.geometry("800x600")
        self.create_widgets(win)
        self.get_current_values()
        win.mainloop()

    def create_widgets(self, win):

        # Labels
        self.titleLabel = Label(win, text="Programowanie API", font=("Arial", 25))
        self.currentWorkFolderPathLabel = Label(win, text="Katalog Roboczy", font=("Arial", 11))
        self.materialChooseLabel = Label(win, text="Materiał z grupy Ferrous_metals", font=("Arial", 11))
        self.boxHeightLabel = Label(win, text="Wysokość pudełka", font=("Arial", 11))
        self.boxLengthLabel = Label(win, text="Długość pudełka", font=("Arial", 11))
        self.boxDepthLabel = Label(win, text="Głebokość pudełka", font=("Arial", 11))
        self.textHeightLabel = Label(win, text="Wysokość tekstu", font=("Arial", 11))
        self.textDistFromBoxEdgeLabel = Label(win, text="Odległość tekstu od krawędzi pudełka", font=("Arial", 11))
        self.textDepthLabel = Label(win, text="Głębokość tekstu", font=("Arial", 11))
        self.textValueLabel = Label(win, text="Napis", font=("Arial", 11))

        # Inputs
        self.currentWorkFolderPathInputField = Entry()
        self.boxHeightInputField = Entry()
        self.boxLengthInputField = Entry()
        self.boxDepthInputField = Entry()
        self.textHeightInputField = Entry()
        self.textDistFromBoxEdgeInputField = Entry()
        self.textDepthInputField = Entry()
        self.textValueInputField = Entry()

        # Buttons
        self.currentWorkFolderPathButton = Button(win, text="Zmień katalog")
        self.currentFileButton = Button(win, text="Wybierz plik")
        self.submitButton = Button(win, text="Zapisz wymiary")

        # Dropdown menu
        materialsList = ["Steel_cast", "Stainless_steel_ferritic", "Steel_HSLA", "Tool_steel_high_speed",
                         "Steel_low_carbon", "Steel_medium_carbon", "Steel_high_carbon", "Cast_iron_ductile",
                         "Stainless_steel_austenitic", "Steel_galvanized"]
        self.optionVar = StringVar(win)
        self.optionVar.set(materialsList[0])
        self.materialChooseMenu = OptionMenu(win, self.optionVar, *materialsList)

        # Input validation
        req = win.register(self.validate_input)
        self.boxHeightInputField.config(validate="key", validatecommand=(req, "%P"))
        self.boxLengthInputField.config(validate="key", validatecommand=(req, "%P"))
        self.boxDepthInputField.config(validate="key", validatecommand=(req, "%P"))
        self.textHeightInputField.config(validate="key", validatecommand=(req, "%P"))
        self.textDistFromBoxEdgeInputField.config(validate="key", validatecommand=(req, "%P"))
        self.textDepthInputField.config(validate="key", validatecommand=(req, "%P"))

        # Layout
        btnInternalPaddingX = 10
        btnInternalPaddingY = 5
        btnOuterPaddingY = 10
        self.titleLabel.pack()
        self.currentFileButton.pack(ipadx=btnInternalPaddingX, ipady=btnInternalPaddingY, pady=btnOuterPaddingY)
        self.currentWorkFolderPathLabel.pack()
        self.currentWorkFolderPathInputField.pack(fill="both", padx=10)
        self.currentWorkFolderPathButton.pack(ipadx=btnInternalPaddingX, ipady=btnInternalPaddingY,
                                              pady=btnOuterPaddingY)
        self.materialChooseLabel.pack()
        self.materialChooseMenu.pack()
        self.boxHeightLabel.pack()
        self.boxHeightInputField.pack()
        self.boxLengthLabel.pack()
        self.boxLengthInputField.pack()
        self.boxDepthLabel.pack()
        self.boxDepthInputField.pack()
        self.textHeightLabel.pack()
        self.textHeightInputField.pack()
        self.textDistFromBoxEdgeLabel.pack()
        self.textDistFromBoxEdgeInputField.pack()
        self.textDepthLabel.pack()
        self.textDepthInputField.pack()
        self.textValueLabel.pack()
        self.textValueInputField.pack()
        self.submitButton.pack(ipadx=btnInternalPaddingX, ipady=btnInternalPaddingY, pady=btnOuterPaddingY)

        # Event listeners
        self.currentWorkFolderPathButton.bind("<Button-1>", self.choose_working_dir)
        self.currentFileButton.bind("<Button-1>", self.choose_file)
        self.submitButton.bind("<Button-1>", self.save_values)
        win.bind("<Return>", self.save_values)

    def choose_working_dir(self, event):
        path = filedialog.askdirectory(title='Wybierz katalog roboczy')
        self.currentWorkFolderPathInputField.delete(0, END)
        self.currentWorkFolderPathInputField.insert(0, path)
        self.c.creo_cd(path)

    def choose_file(self, event):
        filePathObj = filedialog.askopenfile(title="Wybierz plik", filetypes=[("Part name", "*.prt")])
        filePath = os.path.split(filePathObj.name)[0]
        fileName = os.path.split(filePathObj.name)[1]
        self.currentWorkFolderPathInputField.delete(0, END)
        self.currentWorkFolderPathInputField.insert(0, filePath)
        self.c.creo_cd(filePath)
        self.c.file_open(fileName)
        self.get_current_values()

    def save_values(self, event):

        creoMatPath = "C:/Program Files/PTC/Creo 7.0.1.0/Common Files/text/materials-library/Standard-Materials_GrantaDesign"

        try:
            material = self.optionVar.get()
            self.c.file_load_material_file(material, creoMatPath)
            self.c.file_set_cur_material(material)
        except RuntimeError:
            messagebox.showerror("Błąd", "Zła ścieżka do folderu z materiałami. Prosze zmienić w kodzie na poprawną")
            return

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

        self.get_current_values()

    def get_current_values(self):

        self.currentWorkFolderPathInputField.delete(0, END)
        self.currentWorkFolderPathInputField.insert(0, self.c.creo_pwd())

        a = self.c.parameter_list()
        for param in a:
            if param.get("name") == "H":
                self.boxHeightInputField.delete(0, END)
                self.boxHeightInputField.insert(0, param.get("value"))
            elif param.get("name") == "W":
                self.boxDepthInputField.delete(0, END)
                self.boxDepthInputField.insert(0, param.get("value"))
            elif param.get("name") == "L":
                self.boxLengthInputField.delete(0, END)
                self.boxLengthInputField.insert(0, param.get("value"))
            elif param.get("name") == "T_L":
                self.textDistFromBoxEdgeInputField.delete(0, END)
                self.textDistFromBoxEdgeInputField.insert(0, param.get("value"))
            elif param.get("name") == "T_W":
                self.textDepthInputField.delete(0, END)
                self.textDepthInputField.insert(0, param.get("value"))
            elif param.get("name") == "T_H":
                self.textHeightInputField.delete(0, END)
                self.textHeightInputField.insert(0, param.get("value"))
            elif param.get("name") == "TEXT":
                self.textValueInputField.delete(0, END)
                self.textValueInputField.insert(0, param.get("value"))


MainWindow(Tk())
