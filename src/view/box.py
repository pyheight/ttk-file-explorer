from tkinter import messagebox

from ttkbootstrap.toast import ToastNotification  

from model.config_loader import get_text


class MessageBox: 
    @staticmethod  
    def _show_toast(title, message, icon, bootstyle):  
        ToastNotification(  
            title=get_text(title),  
            message=f' {message} ',  
            duration=4000,  
            icon=icon, 
            position=(100, 100, 'n'),  
            bootstyle=bootstyle,  
            minsize=(0, 0)  
        ).show_toast()  
  
    @staticmethod  
    def info(message, title='info'):  
        MessageBox._show_toast(title, message, 'ℹ', 'info')  
  
    @staticmethod  
    def error(message, title='error'):  
        MessageBox._show_toast(title, message, '❌', 'danger')  
  
    @staticmethod
    def warning(message, title='warning'):  
        MessageBox._show_toast(title, message, '⚠', 'warning')  

    @staticmethod  
    def showinfo(message, title='info'):  
        messagebox.showinfo(title=get_text(title), message=message)
  
    @staticmethod  
    def showerror(message, title='error'):  
        messagebox.showerror(title=get_text(title), message=message)  

    @staticmethod
    def showwarning(message, title='warning'):  
        messagebox.showwarning(title=get_text(title), message=message)
