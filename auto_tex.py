
# Written by Angus Lewis
# Version 1.0

# SUMMARY
# This script takes all the png, eps, tex, and excel files in a folder and creates a .tex file that includes them all within floats.
# Floats are titled with the file names.
# The files are ordered intelligently.
# There are options to incorporate subfigures.
# Child tex files are included with fileinput (same as the input command), because otherwise LyX saves a separate version upon import.
# fileinput is commented, so you need to remove the comments in LyX or in the tex file.

# NAMING
# Any underscores will be stripped from the file names.
# Otherwise the file name will appear as entered in the .tex file output.

# ORDERING
# Ordering is done by a smart sort, which sorts based on words not characters.
# It will put a file called "figure_10" after a file called "figure_9" evern though 1 comes before 9.
# You can also order floats by prefixing them them with "F#_", where # is any number.
# They will sorted acoording to #, and the script with remove the prefic "F#_" when it names the floats.

# SUBFIGURES
# To include subfloats, split the file name into two parts connected with "_SUB_".
# Figures with the same first part will be grouped together.
# As an example, if you have the files "figure_1_SUB_a" "figure_1_SUB_b" "figure_2_SUB_a" "figure_2_SUB_b",
# the .tex file will have two figures floats titled "figure 1" and "figure 2",
# each of which will have two subfloats titled "a" and "b" containing the repesctive figure.
# There is no mechanism to have subtables.
# You can order subfloats by naming them figure_1_SUB_SF#_a where # is their order. As with ordering the floats the SF# will be stipped form the title.

# INSTRUCTIONS
# The script needs to run within the folder. So set the folder with the files as the cd then call this script.
# A file called "all_png_and_tex_files_in_folder.tex" will appear in the folder.
# Running the script again will overwite any file called "all_png_and_tex_files_in_folder.tex".




import os
import re
from natsort import natsorted, ns
import pandas as pd

# tex preamble
preamble=r"""%% Created with a script written by Angus Lewis.
%% Based on the LyX template for LaTeX files:
%% LyX 2.3.3 created this file.  For more info, see http://www.lyx.org/.
%% Do not edit unless you really know what you are doing.
\documentclass[english]{article}
\usepackage[T1]{fontenc}
\usepackage[latin9]{inputenc}
\usepackage{geometry}
\geometry{verbose,tmargin=1in,bmargin=1in,lmargin=1in,rmargin=1in}
\usepackage{color}
\usepackage{babel}
\usepackage{array}
\usepackage{float}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{graphicx}
\usepackage{setspace}
\usepackage[authoryear]{natbib}
\doublespacing
\usepackage[unicode=true,
 bookmarks=false,
 breaklinks=false,pdfborder={0 0 1},backref=false,colorlinks=true]
 {hyperref}
\hypersetup{
 linkcolor=black, citecolor=black, urlcolor=NavyBlue}



\makeatletter

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LyX specific LaTeX commands.
%% Because html converters don't know tabularnewline
\providecommand{\tabularnewline}{\\}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% User specified LaTeX commands.
% packages
\usepackage[dvipsnames]{xcolor}
\usepackage{pdflscape}

% replace input with fileinput to hide it from Lyx when importing
% without this LyX makes temp versions of the child .tex files that then do not update
\let\fileinput\input
\let\fileinclude\include

\@ifundefined{showcaptionsetup}{}{%
 \PassOptionsToPackage{caption=false}{subfig}}
\usepackage{subfig}
\makeatother

\begin{document}
"""

# convert excel files to tex tables
def excel_to_tex(path):
    excel_df = pd.read_excel(path , sheet_name="Sheet1")
    with pd.option_context("max_colwidth", 1000):
        tex_code = excel_df.to_latex(na_rep='', index=False)
    return tex_code

# start a float with a given title and type
def start_float(title, fig_or_tab):
    tex_code = r"""
\begin{""" + fig_or_tab + """}[H]
\caption{""" + rgx_ob_F.sub("", title.replace("_"," ")) + r"""}
\bigskip{}
\begin{centering}
"""
    return tex_code

# add a subfloat for a given file and width
def add_subfloat(path, col_w):
    folder, file = os.path.split(path)
    path_no_ext, ext = os.path.splitext(path)
    rgx_match = rgx_ob_sub.search(file)
    title = rgx_ob_F.sub("", rgx_match.group(2).replace("_"," ").replace(ext,""))
    if ext in ['.eps','.png']:
        tex_code = r"""\subfloat[""" + title + r"""]{
\bigskip{}
\includegraphics[width=0""" +col_w+ r"""\columnwidth]{\string""" +'"'+path_no_ext+r"""\string"."""+ext.replace(".","")+"""}}"""
    elif rgx_match.group(4) in ['xls','xlsx']:
        tex_code = r"""\subfloat[""" +title+ r"""]{
\bigskip{}
""" + excel_to_tex(path) + """
        }"""
    return tex_code

# end a float
def end_float():
    tex_code = r"""
\end{centering}
\end{figure}
"""
    return tex_code

# add a single element
def add_single(path):
    folder, file = os.path.split(path)
    path_no_ext, ext = os.path.splitext(path)
    title = rgx_ob_F.sub("", file.replace("_"," ").replace(ext,""))
    if ext in ['.eps', '.png']:
        tex_code = r"""
\begin{figure}[H]
\caption{""" + title + r"""}

\bigskip{}
\begin{centering}
\includegraphics[width=0.75\columnwidth]{\string""" +'"'+path_no_ext+r"""\string"."""+ext.replace(".","")+"""}
\end{centering}
\end{figure}
"""
    # for single tex files
    elif ext in ['.tex']:
        tex_code = r"""
\begin{table}[H]
\caption{""" + title + r"""}

\bigskip{}
\begin{centering}
%\fileinput{\string""" +'"'+path_no_ext+ r"""\string".tex}
\end{centering}
\end{table}
"""
    # for single excel files
    elif ext in ['.xls', '.xlsx']:
        tex_code = r"""
\begin{table}[H]
\caption{""" + title + r"""}

\bigskip{}
\begin{centering}
""" + excel_to_tex(path) + """
\end{centering}
\end{table}
"""
    else:
        tex_code=" "
    return tex_code

# smart ordering that sorts by entire numbers rather than digits
def smart_sort(list):
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key)]
    list.sort(key=alphanum)
    return list

# for can testing uncomment next line
#os.chdir(r'C:\Users\ajl2282\Dropbox (CBS)\CBS\scripts\test_every_file_to_lyx')

# list of every file in directory
os.getcwd()
files_path = [os.path.abspath(x) for x in os.listdir()]
files_path = natsorted(files_path)

# check if there already exists all_png_and_tex_files_in_folder document
tex_check=os.path.join(os.getcwd(),'all_png_and_tex_files_in_folder.tex')
if tex_check in files_path:
    os.remove(r'all_png_and_tex_files_in_folder.tex')
    files_path.remove(tex_check)

# regexs for different file types
rgx_ob_sub = re.compile(r'(.*?)_SUB_(.*?).(png|eps|xls|xlsx)$')
# regexs to clean file names
rgx_ob_F = re.compile(r"^(S)?F\d+ ")

# loop over files, add to body of document
body=preamble
i=0
included=[]
for path in files_path:
    if path in included:
        continue
    i=i+1
    # save folder and path separately
    folder, file = os.path.split(path)
    path_no_ext, ext = os.path.splitext(path)
    # for documents with SUB in file name
    # prefix to sub will head figure float and each suffix and file will get own subflat
    if "SUB" in file:
        rgx_match = rgx_ob_sub.search(file)
        par_name = rgx_match.group(1)
        par_title = rgx_match.group(1)+"_SUB_"
        child_list = [path]
        for pot_child in files_path:
            if par_title in pot_child:
                if pot_child!=path:
                    child_list.append(pot_child)
                    included.append(pot_child)
        child_list=natsorted(child_list)
        child_num=len(child_list)
        # set dimensions for subfloats
        if child_num==1 or child_num==2:
            width='.5'
            col=1
        elif child_num<7:
            width=".5"
            col=2
        elif child_num==9:
            width=".33"
            col=3
        elif child_num==10:
            width=".3"
            col=2
        elif child_num==8 or child_num==7:
            width=".35"
            col=2
        else:
            width=".25"
            col=3
        # start either table or figure float
        if ext in ['.eps','.png']:
            float_type = 'figure'
        else:
            float_type = 'table'
        float_code = start_float(par_name, float_type)
        # iterate over child figures
        newline_test=0
        for child in child_list:
            newline_test=newline_test+1
            float_code = float_code + add_subfloat(child, width)
            # test if new column should start, if so newline and counter goes to 0
            if newline_test==col:
                float_code=float_code+'\n\n'
                newline_test=0
        float_code = float_code + end_float()

    # for single items
    else:
        float_code = add_single(path)

    # Add tex code from iteration of loop
    body = body + float_code
    included.append(file)

# End document
body = body + r"""
\end{document}"""

tex_file=open("all_png_and_tex_files_in_folder.tex", "w")
tex_file.write(body)
tex_file.close()

print(" ")
print("A .tex file called all_png_and_tex_files_in_folder.tex is saved in this folder.")
print("It contains every .png and .tex file in this folder.")
print(" ")
