from tkinter import *

pypad = Tk() #toplevel widget
pypad.title('G-Text editor')
import tkinter.filedialog
import os
import tkinter.messagebox
pypad.geometry('350x350') #the root window geometry
#self.pypad.wm_iconbitmap('icons/icon.ico')




#defining pop-up 
def pop_up(event):
    cmenu.tk_popup(event.x_pypad, event.y_pypad, 0)



#showing info bar
def show_info_bar():
    val = showinbar.get()
    if val:
            infobar.pack(expand = NO, fill = None, side = RIGHT, anchor = SE)
    elif not val:
            infobar.pack_forget()
#theme choice
def theme(event=None):
    global bgc, fgc
    val = themechoice.get()
    clrs = clrschms.get(val)
    fgc, bgc = clrs.split('.')
    fgc, bgc = '#'+fgc, '#'+bgc
    textpad.config(bg = bgc, fg = fgc)
#Displaying line numbers
def update_line_numbers(event=None):
    txt = ''
    if showln.get():
        endline, endcolumn = textpad.index('end-1c').split('.')
        txt = '\n'.join(map(str, range(1, int(endline))))
        lnlabel.config(text = txt, anchor = 'nw')

#Defining line highlighting
def highlight_line(interval=100):
        textpad.tag_remove('active_line', 1.0, 'end')
        textpad.tag_add('active', 'insert linestart', 'insert lineend+1c')
        textpad.after(interval, toggle_highlight)

def toggle_highlight(event=None):
    val = htln.get()
    undo_highlight() if not val else highlight_line()


#Defining the about method
def about(event=None):
    tkinter.messagebox.showinfo('About', 'TKinter GUI Application\n Development Hotshot')

#Defining help method
def help_box(event=None):
    tkinter.messagebox.showinfo('Help', 'For help refer to book\n Tkinter GUI Application\n Development Hotshot', icon = 'question')

#defining help method
def exit_editor(event=None):
    if tkinter.messagebox.askokcancel('Quit', 'Do you really want to quit'):
        pypad.destroy()

pypad.protocol('WM_DELETE_WINDOW', exit_editor) #override close button and redirect to exit editor



def new_file():
    pypad.title('untitled')
    global filename
    filename = None
    textpad.delete(1.0,END)
def open_file():
    global filename
    filename = tkinter.filedialog.askopenfilename(defaultextension='.txt', filetypes=([('All files', '**'), ('Text Documents', '*.txt')]))
    if filename == "": #if no title choosen
         filename == None
    else:
        pypad.title(os.path.basename(filename) + ' - pyPad')#Returning the basename of the filename
        textpad.delete(1.0,END)
        fh = open(filename, 'r')
        textpad.insert(1.0,fh.read())
        fh.close()
#defining a save method
def save():
       global filename
       try:
           f = open(filename, 'w')
           letter = textpad.get(1.0,END)
           f.write(letter)
           f.close
       except:
           save_as()

#defining save as
def save_as():
    try:
        f = tkinter.filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension='.txt', filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')])
        fh = open(f, 'w')
        textoutput = textpad.get(0.0, END)
        fh.write(textoutput)
        fh.close()
        pypad.title(os.path.basename(f)+ '- pyPad')
    except:
        pass

#demo on indexing and tagging features of text widget

def select_all():
    textpad.tag_add('sel', '1.0', 'end')
def on_find():
    t2 = Toplevel(pypad)#creating a small window for the find tool
    t2.title('Find')#title of the new find window
    t2.geometry('262x65+200+250')#size and location of our new window
    t2.transient(pypad)#setting this means the find tool will always display above the root window
    Label(t2, text = 'Find all:').grid(row = 0, column = 0, sticky = 'e')#label for our new window
    v = StringVar()
    e = Entry(t2, width = 25, textvariable=v)#entry box for the word we are searching
    e.grid(row = 0, column = 1, padx = 2, pady = 2, sticky = 'we')
    e.focus_set()
    c = IntVar()
    Checkbutton(t2, text = 'Ignore case', variable=c).grid(row = 0, column = 1, sticky = 'e', padx = 2, pady = 2)
    Button(t2, text = 'Find All', underline = 0, command =lambda: search_for(v.get(),c.get(), textpad, t2, e)).grid(row = 0, column = 0, sticky = 'e'+'w', padx = 2, pady = 2)
    def close_search():
            textpad.tag_remove('match', '1.0', END)
            t2.destroy()
    t2.protocol('WM_DELETE_WINDOW', close_search)#override close button
def search_for(needle, cssnstv, textpad, t2, e):
        textpad.tag_remove('match', '1.0', END)
        count = 0
        if needle:
                pos = '1.0'
                while True:
                    pos = textpad.search(needle, pos, nocase = cssnstv, stopindex = END)
                    if not pos: break
                    lastpos = '%s+%dc' % (pos, len(needle))
                    textpad.tag_add('match', pos, lastpos)
                    count+=1
                    pos = lastpos
                textpad.tag_config('match', foreground = 'red', background = 'yellow')
        e.focus_set()
        t2.title('%d matches found' %count)

#leveraging in-built text widget functionalities 
def undo():
    textpad.event_generate("<<Undo>>")
    update_line_numbers()

def redo():
    textpad.event_generate("<<Redo>>")
    update_line_numbers()

def cut():
    textpad.event_generate("<<Cut>>")
    update_line_numbers()

def copy():
    textpad.event_generate("<<Copy>>")
    update_line_numbers()

def paste():
    textpad.event_generate("<<Paste>>")
    update_line_numbers()


mymenu1 = Menu(pypad)   #frame to hold all menus

filemenu = Menu(mymenu1, tearoff=0)     #File menu

mymenu1.add_cascade(label='File', menu=filemenu)

editmenu = Menu(mymenu1, tearoff=0)     #edit menu

mymenu1.add_cascade(label='Edit', menu=editmenu)    

viewmenu = Menu(mymenu1, tearoff=0)     #view menu

mymenu1.add_cascade(label='View', menu=viewmenu)

aboutmenu = Menu(mymenu1, tearoff=0)

mymenu1.add_cascade(label='About', menu=aboutmenu)

themesmenu = Menu(mymenu1, tearoff=0)
mymenu1.add_cascade(label='Themes', menu=themesmenu)


pypad.config(menu=mymenu1)  #displaying the top menu

#creating a shortcut 
shortcutbar = Frame(pypad, height = 25)

icons = ['new_file', 'open_file', 'save', 'cut', 'copy', 'paste', 'undo', 'redo', 'on_find', 'about']
for  i, icon in  enumerate(icons):
    tbicon = PhotoImage(file = 'icons/'+icon+'.gif')
    cmd  = eval(icon)
    toolbar = Button(shortcutbar, image = tbicon, command = cmd)
    toolbar.image = tbicon
    toolbar.pack(side = LEFT)
shortcutbar.pack(expand = NO, fill = X)

#defining the icons for compound menu demo
newicon = PhotoImage(file='icons/new_file.gif')
openicon = PhotoImage(file = 'icons/open_file.gif')
saveicon = PhotoImage(file = 'icons/save.gif')
cuticon = PhotoImage(file ='icons/cut.gif')
copyicon = PhotoImage(file = 'icons/copy.gif')
pasteicon = PhotoImage(file = 'icons/paste.gif')
undoicon = PhotoImage(file = 'icons/undo.gif')
redoicon = PhotoImage(file = 'icons/redo.gif')

#File menu, for open,save,save as and quit
filemenu.add_command(label='New', accelerator='Ctrl+N', compound=LEFT, image=newicon, underline=0, command = new_file)
filemenu.add_command(label='Open', accelerator='Ctrl+O', compound=LEFT, image=openicon, underline=0, command=open_file)
filemenu.add_command(label='Save', accelerator='Ctrl+S', compound=LEFT, image=saveicon, underline=0, command = save)
filemenu.add_command(label='Save as', accelerator='Shift+Ctrl+S', compound=LEFT, command = save_as)

#Edit menu, for undo, redo, cut, and copy and paste
editmenu.add_command(label='Undo', compound=LEFT, image=undoicon, accelerator='Ctrl+Z', command = undo)
editmenu.add_command(label='Redo', compound=LEFT, image=redoicon, accelerator='Ctrl+Y', command = redo)
editmenu.add_separator()
editmenu.add_command(label='Cut', compound=LEFT, image=cuticon, accelerator='Ctrl+X', command = cut)
editmenu.add_command(label='Copy', compound=LEFT, image=copyicon, accelerator='Ctrl+C', command = copy)
editmenu.add_command(label='Paste', compound=LEFT, image=pasteicon, accelerator='Ctrl+V', command = paste)
editmenu.add_separator()
editmenu.add_command(label='Find', underline=0, accelerator='Ctrl+F', command = on_find)
editmenu.add_command(label='Select All', underline=7, accelerator='Ctrl+A', command = select_all)

#View menu
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label='Show line number', variable=showln)
showinbar = IntVar()
showinbar.set(1)
viewmenu.add_checkbutton(label='Show info bar at bottom', variable=showinbar, command = show_info_bar)
hltln = IntVar()
viewmenu.add_checkbutton(label='Highlight Current line', onvalue=1, offvalue=0, variable=hltln, command = toggle_highlight)

#we define a color scheme dictionary containing name and hex value 
clrschms = {
'1. Default White': '000000.FFFFFF',
'2. Greygarious Grey': '83406A.D1D4D1',
'3. Lovely lavender': '202B4B.E1E1FF',
'4. Aquamarine': '5B8340.D1E7E0',
'5. Bold Beige': '4B4620.FFF0E1',
'6. Cobalt Blue': 'ffffBB.333aa',
'7. Olive Green': 'D1E7E0.5B8340',

}
themechoice= StringVar()
themechoice.set('1. Default White')
for k in sorted(clrschms):
    themesmenu.add_radiobutton(label=k, variable=themechoice, command = theme)

#About menu 
aboutmenu.add_command(label='About', command = about)
aboutmenu.add_command(label='Help', accelerator='F1', command = help_box)

#Adding top label to  hold top and left labels-left hold number lines and top for shortcuts
shortcut = Frame(pypad, height = 25, bg = 'light sea green').pack(expand = NO, fill=X)
lnlabel = Frame(pypad, width = 25, bg = 'antique white').pack(side = LEFT, anchor = 'nw', fill=Y)

#Adding text widget and scroll bar
textpad = Text(pypad)
textpad.pack(expand = YES, fill=BOTH)
scrollbar = Scrollbar(textpad)
textpad.configure(yscrollcommand=scrollbar.set)
scrollbar.config(command=textpad.yview)
scrollbar.pack(side=RIGHT,fill=Y)

#Adding an info bar at the bottom
infobar = Label(textpad, text = 'Line: 1 | Column: 0')
infobar.pack(expand = NO, fill = None, side = RIGHT, anchor = SE)
#context menu popup menu
cmenu = Menu(textpad)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    cmenu.add_command(label=i, compound=LEFT, command=cmd)
cmenu.add_separator()
cmenu.add_command(label='select all', underline=7, command=select_all)
textpad.bind('<Button-2>', pop_up)

#Binding events
"""textpad.bind("<Control-N>", new_file)
textpad.bind('<Control-n>', new_file)
textpad.bind('<Control-O>', open_file)
textpad.bind('<Control-o>', open_file)
textpad.bind('<Control-S>', save)
textpad.bind('<Control-s>', save)
textpad.bind('<Control-A>', select_all)
textpad.bind('<Control-a>', select_all)
textpad.bind('<Control-f>', on_find)
textpad.bind('<Control-F>', on_find)
textpad.bind('<Control-F1>', help_box)"""



textpad.bind('<Any-KeyPress>', update_line_numbers)
textpad.tag_configure('active_line', background = 'ivory2')












pypad.mainloop()
