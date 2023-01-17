import csv
import itertools
import os
import subprocess
import calendar

class BlockFormat(object):
    def __init__(self):
        self.header = "\documentclass[16pt]{extarticle}"
        self.header += "\usepackage[top=1cm, bottom=1cm, outer=1cm, inner=2cm, marginparwidth=1cm, marginparsep=0.5cm]{geometry}"
        self.header += "\usepackage{tikz,lipsum, dashrule, comment, eso-pic, ifthen, changepage, xcolor, graphicx, marginnote}"
        self.header += "\usepackage[most]{tcolorbox} \\tcbuselibrary{listings,breakable}"
        self.header += "\usepackage{lmodern} \usepackage[default]{lato} \usepackage[T1]{fontenc}" # Fonts technically its \usepackage{mlmodern}
        self.header += "\\reversemarginpar"

        colors = "\definecolor{textGrey}{RGB}{0, 0, 0}" 
        colors += "\definecolor{buildBlue}{RGB}{212, 217, 222}"
        colors += "\definecolor{codeBlue}{RGB}{214, 223, 222}"
        colors += "\definecolor{businessBlue}{RGB}{222, 217, 227}" 
        colors += "\definecolor{wholeBlue}{RGB}{231, 228, 223}"
        colors += "\definecolor{backgroundColor}{RGB}{85, 102, 115}"

        self.header += colors
        self.header += "\color{white} \\renewcommand{\\baselinestretch}{1.3} \\pagestyle{empty} \\begin{document}"
        self.header += "\pagecolor{backgroundColor}" 
        self.footer = "\end{document}"

        self.wholeHeader = "\marginnote{\\begin{tcolorbox}[enhanced, colback=wholeBlue,colframe=white,coltext=textGrey, arc=0pt,outer arc=0pt, boxrule=1mm, tikz={rotate=90}, width=3.8cm] {\Large \\textbf{whole~\hspace{0.1cm}~team}} \end{tcolorbox}}"
        self.buildingHeader = "\marginnote{\\begin{tcolorbox}[enhanced, colback=buildBlue,colframe=white,coltext=textGrey, arc=0pt,outer arc=0pt, boxrule=1mm, tikz={rotate=90}, width=3.8cm] {\Large \\textbf{building}} \end{tcolorbox}}"
        self.buildingHeaderOffset = '[-0.7cm]' 
        self.codingHeader = "\marginnote{\\begin{tcolorbox}[enhanced, colback=codeBlue,colframe=white,coltext=textGrey, arc=0pt,outer arc=0pt, boxrule=1mm, tikz={rotate=90}, width=3.8cm] {\Large \\textbf{coding}} \end{tcolorbox}}[-0.7cm]"
        self.businessHeader = "\marginnote{\\begin{tcolorbox}[enhanced, colback=businessBlue,colframe=white,coltext=textGrey, arc=0pt,outer arc=0pt, boxrule=1mm, tikz={rotate=90}, width=3.8cm] {\Large \\textbf{business}} \end{tcolorbox}}[-0.7cm]"


    def formatDate(self, date_pretty, month):
        if month == 1:
            dist = '0.5'
        if month == 9:
            dist = '4'
        elif month == 10:
            dist = '2.75'
        else: 
            dist = '3'
        return "\makebox[" + dist + "cm]{{\Huge " + date_pretty + " }} \\\\ "

    def buildBlock(self, data, i):
        # "data" is the text, "i" is index. +1 to make it one indexed instead of zero indexed
        txt = "\\begin{tcolorbox}[colback=buildBlue,colframe=white,coltext=textGrey, breakable, arc=0pt,outer arc=0pt, boxrule=1mm, left=2mm]"
        txt += "\\textit{\\textbf{focus: }} \\\\" + data['Focus'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{summary: }} \\\\" + data['Summary'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{challenges: }} \\\\" + data['Challenges/Problems'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{next steps: }} \\\\" + data['Next Steps']
        txt += "\end{tcolorbox}"
        return txt

    def codingBlock(self, data, i):
        # "data" is the text, "i" is "Afternoon" or "Morning". 
        txt = "\\begin{tcolorbox}[colback=codeBlue,colframe=white,coltext=textGrey, breakable, arc=0pt,outer arc=0pt, boxrule=1mm, left=2mm]"
        txt += "\\textit{\\textbf{focus: }} \\\\" + data['Focus'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{summary: }} \\\\" + data['Summary'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{challenges: }} \\\\" + data['Challenges/Problems'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{next steps: }} \\\\" + data['Next Steps'] 
        txt += "\end{tcolorbox}"
        return txt

    def businessBlock(self, data, i):
        # "data" is the text, "i" is "Afternoon" or "Morning". 
        txt = "\\begin{tcolorbox}[colback=businessBlue,colframe=white,coltext=textGrey, breakable, arc=0pt,outer arc=0pt, boxrule=1mm, left=2mm]"
        txt += "\\textit{\\textbf{focus: }} \\\\" + data['Focus'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{summary: }} \\\\" + data['Summary'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{challenges: }} \\\\" + data['Challenges/Problems'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{next steps: }} \\\\" + data['Next Steps'] 
        txt += "\end{tcolorbox}"
        return txt

    def wholeBlock(style, data, i):
        # "data" is the text, "i" is "Afternoon" or "Morning". 
        txt = "\\begin{tcolorbox}[colback=wholeBlue,colframe=white,coltext=textGrey, breakable, arc=0pt,outer arc=0pt, boxrule=1mm, left=2mm]"
        txt += "\\textit{\\textbf{focus: }} \\\\" + data['Focus'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{summary: }} \\\\" + data['Summary'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{challenges: }} \\\\" + data['Challenges/Problems'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{next steps: }} \\\\" + data['Next Steps']
        txt += "\end{tcolorbox}"
        return txt
