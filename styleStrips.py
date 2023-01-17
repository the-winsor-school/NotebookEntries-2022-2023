import csv
import itertools
import os
import subprocess
import calendar

class StripsFormat(object):
    def __init__(self):
        self.header = "\documentclass[16pt]{extarticle}"
        self.header += "\usepackage[margin=0.6in]{geometry} \usepackage{tikz,lipsum, dashrule, comment, eso-pic, ifthen, changepage, xcolor}"
        self.header += "\usepackage[most]{tcolorbox} \\tcbuselibrary{listings,breakable}" 
        self.header += "\usepackage{lmodern} \usepackage[default]{lato} \usepackage[T1]{fontenc}"
        #self.header += "\usepackage[T1]{fontenc} \usepackage{tinos}"

        colors = "\definecolor{customBlack}{RGB}{120, 137, 129}"
        colors += "\definecolor{buildBlue}{RGB}{233, 235, 235}"
        colors += "\definecolor{codeBlue}{RGB}{214, 216, 218} "
        colors += "\definecolor{businessBlue}{RGB}{196, 200, 202}" 

        colors += "\definecolor{textGrey}{RGB}{0, 0, 0}"  
        colors += "\definecolor{wholeBlue}{RGB}{243, 245, 245}"
        colors += "\definecolor{backgroundColor}{RGB}{246, 251, 255}"

        self.header += colors
        self.header += "\color{textGrey} \\renewcommand{\\baselinestretch}{1.3} \\pagestyle{empty} \\begin{document}"
        self.header += "\pagecolor{backgroundColor}" 
        self.footer = "\end{document}"

        self.focusHeader = "\\begin{center} {\\rule[1mm]{8cm}{0.5mm}} {\Large FOCUS } {\\rule[1mm]{8cm}{0.5mm}} \\end{center}"
        self.summaryHeader = "\\begin{center} {\\rule[1mm]{7.45cm}{0.5mm}} {\Large SUMMARY } {\\rule[1mm]{7.45cm}{0.5mm}} \\end{center}"
        self.challengesHeader = "\\begin{center} {\\rule[1mm]{7.25cm}{0.5mm}} {\Large CHALLENGES } {\\rule[1mm]{7.25cm}{0.5mm}} \\end{center}"
        self.nextStepsHeader = "\\begin{center} {\\rule[1mm]{7.4cm}{0.5mm}} {\Large NEXT STEPS } {\\rule[1mm]{7.4cm}{0.5mm}} \\end{center}"

    def formatDate(self, date_pretty):
        return "\\begin{tcolorbox}[colback=customBlack,colframe=customBlack,coltext=white,sidebyside, lower separated=false, after skip=20pt plus 2pt]  {\Huge " + date_pretty + "}   \\tcblower \end{tcolorbox}" 

    def buildBlock(self, data, i):
        # "data" is the text, "i" is index. +1 to make it one indexed instead of zero indexed
        # If we have text (i.e. someone wrote something), create a LaTeX color box of the correct color, with a subtitle label and the text
        if len(data) == 0: 
            return ''
        else:
             return "\\begin{tcolorbox}[colback=buildBlue,colframe=buildBlue,coltext=textGrey]  \\textbf{building (Group " + str(i+1) + "): }" + data + "\end{tcolorbox}"

    def codingBlock(self, data, i):
        # "data" is the text, "i" is "Afternoon" or "Morning". 
        # If we have text (i.e. someone wrote something), create a LaTeX color box of the correct color, with a subtitle label and the text
        if len(data) == 0:
            return 0
        else: 
            return "\\begin{tcolorbox}[colback=codeBlue,colframe=codeBlue,coltext=textGrey]  \\textbf{coding (Group " + str(i+1) + "): } " + data + "\end{tcolorbox}"

    def businessBlock(self, data, i):
        # "data" is the text, "i" is "Afternoon" or "Morning". 
        # If we have text (i.e. someone wrote something), create a LaTeX color box of the correct color, with a subtitle label and the text
        if len(data) == 0: 
            return ''
        else:
            return "\\begin{tcolorbox}[colback=businessBlue,colframe=businessBlue,coltext=textGrey]  \\textbf{business (Group " + str(i+1) + "): }" + data + "\end{tcolorbox}"

    def wholeBlock(style, data, i):
        # "data" is the text, "i" is "Afternoon" or "Morning". 
        # If we have text (i.e. someone wrote something), create a LaTeX color box of the correct color, with a subtitle label and the text
        if len(data) == 0:
            return ''
        else:
            return "\\begin{tcolorbox}[colback=wholeBlue,colframe=wholeBlue,coltext=textGrey]  \\textbf{entire team: }" + data + "\end{tcolorbox}"

