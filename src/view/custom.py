import ttkbootstrap as ttk
from model.config_loader import get_image


class CollapsibleFrame(ttk.Frame):  
    def __init__(self, master, title, data, open_text, style='Outline.TButton', **kwargs):  
        super().__init__(master, **kwargs) 
        self.data = data
        self.open_text = open_text
        self.is_open = data.IS_OPEN[open_text]
        self.fold_image = get_image('fold')
        self.unfold_image = get_image('unfold')     
            
        self.top_fra = ttk.Frame(self)
        self.title_lab = ttk.Label(self.top_fra, text=title, font=(self.data.FONT, 11))
        self.toggle_but = ttk.Button(self.top_fra, image=self.unfold_image if self.is_open else self.fold_image, command=self.toggle_content, style=style)  
        self.frame = ttk.Frame(self)

        self.title_lab.pack(side='left', padx=2)  
        self.toggle_but.pack(side='right', padx=2)
        self.top_fra.pack(side='top', fill='x', expand=True, pady=10)
        self.frame.pack(side='top', fill='both', expand=True)

        self.toggle_content()

    def toggle_content(self):  
        if not self.is_open:
            image = self.unfold_image
            self.frame.pack_forget()
        else: 
            image = self.fold_image
            self.frame.pack(side='top', fill='both', expand=True)  
        self.data.IS_OPEN[self.open_text] = self.is_open
        self.is_open = not self.is_open  
        self.toggle_but.config(image=image)


class DiskFrame(ttk.Frame):  
    def __init__(self, master, image, title, value, text, font, **kwargs):  
        super().__init__(master, **kwargs)  
        self.image_lab = ttk.Label(self, image=image)
        self.title_lab = ttk.Label(self, text=title, font=(font, 10))
        self.progress_bar = ttk.Progressbar(self, mode='determinate')
        self.info_lab = ttk.Label(self, text=text, font=(font, 9))

        self.image_lab.pack(side='left')
        self.title_lab.pack(anchor='nw', side='top')
        self.progress_bar.pack(anchor='nw', fill='x', padx=(2, 12))
        self.info_lab.pack(anchor='nw', side='left')

        self.progress_bar['value'] = value
        self.on_leave()  
        
        self.bind('<Enter>', self.on_enter)  
        self.bind('<Leave>', self.on_leave)  

    def on_enter(self, event):  
        self.config(relief='sunken', borderwidth=3)  
  
    def on_leave(self, event=None):  
        self.config(relief='ridge', borderwidth=3)
