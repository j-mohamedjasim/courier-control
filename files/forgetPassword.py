import customtkinter as ct
from tkinter import messagebox
import webbrowser
import requests

def forget_password(root, goBack):

    for widget in root.winfo_children():
        widget.destroy()

    def checkIfEmailExist():
        emails = email.get().strip().lower()

        if not emails:
            messagebox.showerror("Error", "Please enter valid email to proceed reset.")
            email.focus_set()
            return

        emailButton.configure(state='disabled')

        response = requests.post(
            "https://courier-control.onrender.com/check-email",
            json={
                "email": emails,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success") is True:
            newpassword1.grid()
            newpassword2.grid()
            resetButton.grid()
        else:
            emailButton.configure(state='normal')
            newpassword1.grid_remove()
            newpassword2.grid_remove()
            resetButton.grid_remove()
            messagebox.showerror("Does Not Exist", "The email you provide does not exist. Please recheck the email and try again.")
            return

    root.title("Reset Password")
    root.geometry("700x700")

    backButton = ct.CTkLabel(root, text='< Back', cursor='hand2')
    backButton.grid(row=0, column=0, padx=(10,0), pady=(5,0), sticky='w')
    backButton.bind("<Button-1>", lambda event: goBack())

    email = ct.CTkEntry(root, placeholder_text="Enter Your Email", width=300)
    email.grid(row=1, column=0, padx=(10,0), pady=(10,0), sticky='w')

    emailButton = ct.CTkButton(root, text="->", cursor='hand2', width=15, command=checkIfEmailExist)
    emailButton.grid(row=1, column=1, padx=(10,0), pady=(10,0), sticky='w')

    newpassword1 = ct.CTkEntry(root, placeholder_text='Enter Your New Password', width=300)
    newpassword1.grid(row=2, column=0, padx=(10,0), pady=(10,0), sticky='w')
    newpassword1.grid_remove()

    newpassword2 = ct.CTkEntry(root, placeholder_text="Enter Your Password Again", width=300)
    newpassword2.grid(row=3, column=0, padx=(10,0), pady=(10,0), sticky='w')
    newpassword2.grid_remove()

    resetButton = ct.CTkButton(root, text="Reset", width=50, cursor='hand2')
    resetButton.grid(row=4, column=0, padx=(10,0), pady=(10,0), sticky='e')
    resetButton.grid_remove()