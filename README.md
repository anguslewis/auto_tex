# auto_tex


Written by Angus Lewis

Version 1.0

# SUMMARY
This script takes all the png, eps, tex, and excel files in a folder and creates a .tex file that includes them all within floats. Floats are titled with the file names. The files are ordered intelligently. There are options to incorporate subfigures. 

# NAMING
Any underscores will be stripped from the file names. Otherwise the file name will appear as entered in the .tex file output.

# ORDERING
Ordering is done by a smart sort, which sorts based on words not characters. It will put a file called "figure_10" after a file called "figure_9" evern though 1 comes before 9. You can also order floats by prefixing them them with "F#_", where # is any number. They will sorted acoording to #, and the script with remove the prefic "F#_" when it names the floats.

# SUBFIGURES
To include subfloats, split the file name into two parts connected with "_SUB_". Figures with the same first part will be grouped together. As an example, if you have the files "figure_1_SUB_a" "figure_1_SUB_b" "figure_2_SUB_a" "figure_2_SUB_b", the .tex file will have two figures floats titled "figure 1" and "figure 2",  each of which will have two subfloats titled "a" and "b" containing the repesctive figure. There is no mechanism to have subtables. You can order subfloats by naming them figure_1_SUB_SF#_a where # is their order. As with ordering the floats the SF# will be stipped form the title.

# CHILD TEX FILES 
Child tex files are included with fileinput (same as the input command), because otherwise LyX saves a separate version upon import. fileinput is commented, so you need to remove the comments in the tex file or in LyX. I.e., replacing all instances of ``%\fileinput`` with ``\fileinput`` will do the trick.

# INSTRUCTIONS
The script needs to run within the folder. So set the folder with the files as the cd then call this script. A file called "all_png_and_tex_files_in_folder.tex" will appear in the folder. Running the script again will overwite any file called "all_png_and_tex_files_in_folder.tex".
