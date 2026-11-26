from tkinter import *
import customtkinter as ct

#import files:
from files.account_setup import SetupAccountWindow
from files.forgetPassword import forget_password

ct.set_appearance_mode("System")
ct.set_default_color_theme("dark-blue")

def setupAccount(goBack, event=None):

    for widget in root.winfo_children():
        widget.destroy()
    SetupAccountWindow(root, goBack)

def forget_password_link(goBack, event=None):
    for widget in root.winfo_children():
        widget.destroy()
    forget_password(root, goBack)

root = ct.CTk()

def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Driver Control")
    root.geometry("600x350")

    loginId = ct.CTkEntry(root, width=200, placeholder_text="Enter Your Login")
    loginId.pack(pady=(40,5))
    loginId.focus_set()

    passwordEntry = ct.CTkEntry(root, width=200, placeholder_text="Password", show="*")
    passwordEntry.pack(pady=5)

    loginButton = ct.CTkButton(root, text='LogIn')
    loginButton.pack(pady=20)

    forgotPassword = ct.CTkLabel(root, text='Forgot Password?', cursor='hand2')
    forgotPassword.pack(pady=(20,0), padx=(20,5))
    forgotPassword.bind("<Button-1>", lambda event: forget_password_link(show_login_screen, event))

    create_account = ct.CTkLabel(root, text="Setup Account", cursor='hand2')
    create_account.pack(pady=(5,5), padx=(20,5))
    create_account.bind("<Button-1>", lambda event: setupAccount(show_login_screen, event))

show_login_screen()

root.mainloop()