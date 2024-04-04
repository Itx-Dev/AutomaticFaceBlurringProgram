import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage

from Backend.RenderBlur import RenderBlur

class RenderWidgets:
    def __init__(self, mainFrame):
        self.mainFrame = mainFrame
        self.uploadButton = self.renderUploadButton()
        self.submitButton = self.renderSubmitButton()
        self.progressBar = self.renderProgressBar()

        self.videoFilePath = None

    def renderUploadButton(self):
        buttonWidth = 100
        buttonHeight = 100
        icon = PhotoImage(file="./Icons/folderIcon.png")  # Define icon for button
        self.folderIcon = icon.subsample(icon.width() // buttonWidth, icon.height() // buttonHeight)

        uploadButton = tk.Button(self.mainFrame, text="Select Video", command=self.browseFiles, image=self.folderIcon,
                                 compound=tk.TOP, width=buttonWidth, height=buttonHeight + 20,
                                 bg="cornsilk2", activebackground="cornsilk2", borderwidth=0)
        uploadButton.grid(row=3, column=3, sticky='n')

        return uploadButton

    def renderSubmitButton(self):
        buttonWidth = 100
        buttonHeight = 100
        icon = PhotoImage(file="./Icons/uploadIcon.png")
        self.uploadIcon = icon.subsample(icon.width() // buttonWidth, icon.height() // buttonHeight)
        submitButton = tk.Button(self.mainFrame, text="Submit Video", command=self.submitFile, image=self.uploadIcon,
                                 compound=tk.TOP, width=buttonWidth, height=buttonHeight + 20,
                                 bg="cornsilk2", activebackground="cornsilk2", borderwidth=0)
        submitButton.grid(row=3, column=0, sticky='n')
        return submitButton

    def renderProgressBar(self):
        progress = ttk.Progressbar(self.mainFrame, orient="horizontal", length=300, mode="determinate")
        progress.grid(row=3, column=1, sticky='n', columnspan=2)

        return progress

    def browseFiles(self):
        fileName = filedialog.askopenfilename(initialdir="/", title="Select a Video to Blur")
        self.uploadButton.config(text="File Opened: " + fileName)
        self.videoFilePath = fileName  # Update file path
        return fileName

    def submitFile(self):
        if self.videoFilePath:
            renderBlurObject = RenderBlur(self.videoFilePath, self.progressBar, self.mainFrame)
            renderBlurObject.renderBlur()