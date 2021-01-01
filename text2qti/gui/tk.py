# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Dana Lehman
# Copyright (c) 2020, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


import os
import pathlib
import shutil
import time
import tkinter as tk
import tkinter.filedialog
import webbrowser
from ..config import Config
from ..err import Text2qtiError
from ..qti import QTI
from ..quiz import Quiz
from .. import version
#from tkinter.ttk import * #possibly not needed



def main():
    config = Config()
    config.load()
    file_name = ''

    window = tk.Tk()
    window.title('text2CC')
    # Bring window to front and put in focus
    window.iconify()
    window.update()
    window.deiconify()

    # Window grid setup
    current_row = 0
    column_count = 4


    header_label = tk.Label(
        window,
        text='text2cc – Create quizzes in Common Cartridge format from Markdown-based plain text',
        font=(None, 16),
    )
    header_label.grid(
        row=current_row, column=0, columnspan=column_count, padx=(30, 30),
        sticky='nsew',
    )
    #current_row += 1
    # header_link_label = tk.Label(
        # window,
        # text='github.com/gpoore/text2qti',
        # font=(None, 14), fg='blue', cursor='hand2',
    # )
    # header_link_label.bind('<Button-1>', lambda x: webbrowser.open_new('https://github.com/gpoore/text2qti'))
    # header_link_label.grid(
        # row=current_row, column=0, columnspan=column_count, padx=(30, 30),
        # sticky='nsew',
    # )
    current_row += 1
    version_label = tk.Label(
        window,
        text=f'Version:   {version.__version__}',
    )
    version_label.grid(
        row=current_row, column=0, columnspan=column_count, padx=(30, 30), pady=(0, 30),
        sticky='nsew',
    )
    current_row += 1


    file_browser_label = tk.Label(
        window,
        text='Quiz file:\n(plain text file)',
        justify='right',
    )
    file_browser_label.grid(
        row=current_row, column=0, padx=(30, 5), pady=(5, 25),
        sticky='nse',
    )
    last_dir = None
    def browse_files():
        nonlocal file_name
        nonlocal last_dir
        if last_dir is None:
            initialdir = pathlib.Path('~').expanduser()
        else:
            initialdir = last_dir
        file_name = tkinter.filedialog.askopenfilename(
            initialdir=initialdir,
            title='Select a quiz file',
            filetypes=[('Quiz files', '*.md;*.txt')],
        )
        if file_name:
            if last_dir is None:
                last_dir = pathlib.Path(file_name).parent
            file_browser_button.config(text=f'"{file_name}"', fg='green')
        else:
            file_browser_button.config(text=f'<none selected>', fg='red')

    file_browser_button = tk.Button(
        window,
        text='<none selected>',
        fg='red',
        command=browse_files,
    )
    file_browser_button.grid(
        row=current_row, column=1, columnspan=column_count-1, padx=(0, 30), pady=(5, 25),
        sticky='nsew',
    )
    file_browser_button.bind('<Return>', lambda e: browse_files())
    current_row += 1

 #Above here set good
    # advanced_options_label = tk.Label(
        # window,
        # text='Advanced options – LaTeX math & executable code',
        # justify='right',
    # )
    # advanced_options_label.grid(
        # row=current_row, column=1, columnspan=2, padx=(0, 0), pady=(5, 5),
        # sticky='nsw',
    # )
    # current_row += 1


    # latex_url_label = tk.Label(
        # window,
        # text='LaTeX math rendering URL:\n(for Canvas and similar systems)',
        # justify='right',
    # )
    # latex_url_label.grid(
        # row=current_row, column=0, padx=(30, 5), pady=(5, 5),
        # sticky='nse',
    # )
    # latex_url_entry = tk.Entry(window, width=100)
    # latex_url_entry.grid(
        # row=current_row, column=1, columnspan=column_count-1, padx=(0, 30), pady=(5, 5),
        # sticky='nsew',
    # )
    # if 'latex_render_url' in config:
        # latex_url_entry.insert(1, f"{config['latex_render_url']}")
    # current_row += 1


    # pandoc_exists = bool(shutil.which('pandoc'))
    # pandoc_mathml_label = tk.Label(
        # window,
        # text='Convert LaTeX math to MathML:\n(requires Pandoc; ignores rendering URL)',
        # justify='right',
    # )
    # if not pandoc_exists:
        # pandoc_mathml_label['fg'] = 'gray'
    # pandoc_mathml_label.grid(
        # row=current_row, column=0, padx=(30, 5), pady=(5, 5),
        # sticky='nse',
    # )
    # pandoc_mathml_bool = tk.BooleanVar()
    # def pandoc_mathml_command():
        # if pandoc_mathml_bool.get():
            # latex_url_label['fg'] = 'gray'
            # latex_url_entry['fg'] = 'gray'
        # else:
            # latex_url_label['fg'] = 'black'
            # latex_url_entry['fg'] = 'black'
    # if pandoc_exists:
        # pandoc_mathml_button = tk.Checkbutton(
            # window,
            # variable=pandoc_mathml_bool,
            # command=pandoc_mathml_command,
        # )
        # pandoc_mathml_bool.set(config['pandoc_mathml'])
    # else:
        # pandoc_mathml_button = tk.Checkbutton(
            # window,
            # state=tk.DISABLED,
        # )
    # pandoc_mathml_button.grid(
        # row=current_row, column=1, sticky='w',
    # )
    # current_row += 1


    def run():
        run_message_text.delete(1.0, tk.END)
        run_message_text['fg'] = 'gray'
        run_message_text.insert(tk.INSERT, 'Starting...')
        run_message_text.update()
        error_message = None
        if not file_name:
            error_message = 'Must select a quiz file'
            run_message_text.delete(1.0, tk.END)
            run_message_text.insert(tk.INSERT, error_message)
            run_message_text['fg'] = 'red'
            return
        #if latex_url_entry.get():
            #config['latex_render_url'] = latex_url_entry.get()
        
        #config['pandoc_mathml'] = pandoc_mathml_bool.get()

        file_path = pathlib.Path(file_name)
        try:
            text = file_path.read_text(encoding='utf-8-sig')  # Handle BOM for Windows
        except FileNotFoundError:
            error_message = f'File "{file_path}" does not exist.'
        except PermissionError as e:
            error_message = f'File "{file_path}" cannot be read due to permission error. Technical details:\n\n{e}'
        except UnicodeDecodeError as e:
            error_message = f'File "{file_path}" is not encoded in valid UTF-8. Technical details:\n\n{e}'
        except Exception as e:
            error_message = f'An error occurred in reading the quiz file. Technical details:\n\n{e}'
        if error_message:
            run_message_text.delete(1.0, tk.END)
            run_message_text.insert(tk.INSERT, error_message)
            run_message_text['fg'] = 'red'
            return
        cwd = pathlib.Path.cwd()
        os.chdir(file_path.parent)
        try:
            quiz = Quiz(text, config=config, source_name=file_path.as_posix())
            qti = QTI(quiz)
            qti.save(f'{file_path.stem}.zip')
        except Text2qtiError as e:
            error_message = f'Quiz creation failed:\n\n{e}'
        except Exception as e:
            error_message = f'Quiz creation failed unexpectedly. Technical details:\n\n{e}'
        finally:
            os.chdir(cwd)
        if error_message:
            run_message_text.delete(1.0, tk.END)
            run_message_text.insert(tk.INSERT, error_message)
            run_message_text['fg'] = 'red'
        else:
            run_message_text.delete(1.0, tk.END)
            run_message_text.insert(tk.INSERT, f'Created quiz "{file_path.parent.as_posix()}/{file_path.stem}.zip"')
            run_message_text['fg'] = 'green'
    run_button = tk.Button(
        window,
        text='RUN',
        font=(None, 14),
        command=run,
    )
    run_button.grid(
        row=current_row, column=1, columnspan=2, padx=(0, 0), pady=(30, 30),
        sticky='nsew',
    )
    run_button.bind('<Return>', lambda e: run())
    current_row += 1


    run_message_label = tk.Label(
        window,
        text='\nRun Summary:\n',
        relief='ridge',
        width=120,
    )
    run_message_label.grid(
        row=current_row, column=0, columnspan=column_count, padx=(30, 30), pady=(0, 0),
        sticky='nsew',
    )
    current_row += 1


    run_message_frame = tk.Frame(
        window,
        width=120, height=40,
        borderwidth=1, relief='sunken', bg='white',
    )
    run_message_frame.grid(
        row=current_row, column=0, columnspan=column_count, padx=(30, 30), pady=(0, 30),
        sticky='nsew',
    )
    run_message_scrollbar = tk.Scrollbar(run_message_frame)
    run_message_scrollbar.pack(
        side='right', fill='y',
    )
    run_message_text = tk.Text(
        run_message_frame,
        width=10, height=10, borderwidth=0, highlightthickness=0,
        wrap='word',
        yscrollcommand=run_message_scrollbar.set,
    )
    run_message_text.insert(tk.INSERT, 'Waiting...')
    run_message_text['fg'] = 'gray'
    run_message_scrollbar.config(command=run_message_text.yview)
    run_message_text.pack(
        side='left', fill='both', expand=True,
        padx=(5, 5), pady=(5, 5),
    )
    
    def About_page():
            
         abt = tk.Toplevel(window)
         def close_about():
            abt.destroy()

         abt.grab_set()
         
         abt.title("About")
          
         lbl=tk.Label(
             abt,
             text ='Text2CC \n \n Copyright © 2021, Dana Lehman \n Copyright © 2020, Geoffrey M. Poore \n  ',
             #anchor='e',
             justify='center',
             
             )
         lbl.grid(
            #  column=0,
            #  columnspan=4,
            #  row=1,
            #  rowspan=4,
              pady=3,
              padx=30,
            #  sticky="NW"
             )

         vlbl=tk.Label(
             abt,
             text =f'Version:   {version.__version__} \n',
             #bg = 'red',
             #anchor="CENTER",
             #width=max((len(text)))
            )
         vlbl.grid(
            #  column=0,
            #  columnspan=4,
            #  row=2,
            #  rowspan=4,
              pady=3,
            #  padx=30,
            #  sticky="NW"
             )  

         liclbl = tk.Label(
                abt,
                text='License: BSD 3-Clause', 
                #font=(None, 14), 
                fg='blue', cursor='hand2',
                )
         liclbl.bind('<Button-1>', lambda x: webbrowser.open_new('https://opensource.org/licenses/BSD-3-Clause'))
         liclbl.grid(
                row=current_row, column=0, columnspan=column_count, padx=(30, 30),
                #sticky='nsew',
            )  

         OK_BTN=tk.Button(
             abt,
             text="OK",
             command=close_about,
             anchor= 'center',
            )
         OK_BTN.bind('<Return>', lambda e: close_about())
         OK_BTN.grid(
            #  column=2,
            #  columnspan=1,
            #  row=5,
            #  padx=30,
              pady=30,
            #  sticky="se"
             )
         OK_BTN.focus_set()
        
         # Gets the requested values of the height and widht.
         windowWidth = abt.winfo_reqwidth()
         windowHeight = abt.winfo_reqheight()

         # Gets both half the screen width/height and window width/height
         positionRight = int(abt.winfo_screenwidth()/2 - windowWidth/2)
         positionDown = int(abt.winfo_screenheight()/2 - windowHeight/2)
 
         # Positions the window in the center of the page.
         abt.geometry("+{}+{}".format(positionRight, positionDown))
         #abt.geometry("225x100+{}+{}".format(positionRight, positionDown))
         abt.resizable(height= None, width= None)
         abt.focus()
         
         #abt.bind('<Return>', close_about)
    
    def open_help():
        webbrowser.open_new('https://github.com/dlehman83/text2cc/blob/master/README.md')

    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=False)
    filemenu.add_command(label="Open",command=browse_files,underline=0)
    filemenu.add_command(label="Run",command=run,underline=0)
    filemenu.add_command(label="Exit",command=window.quit,underline=1)
    menubar.add_cascade(label="File", menu=filemenu,underline=0)
    helpmenu = tk.Menu(menubar, tearoff=False)
    helpmenu.add_command(label="Help",underline=0,command=open_help)
    helpmenu.add_command(label="About",command=About_page,underline=0)
    menubar.add_cascade(label="Help", menu=helpmenu,underline=0)

    # Gets the requested values of the height and widht.
    windowWidth = window.winfo_reqwidth()
    windowHeight = window.winfo_reqheight()

    # Gets both half the screen width/height and window width/height
    positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)
 
    # Positions the window in the center of the page.
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.config(menu=menubar)
    window.bind('<Return>',run)
    window.mainloop()
