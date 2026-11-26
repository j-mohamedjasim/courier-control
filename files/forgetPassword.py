import customtkinter as ct
from tkinter import messagebox
import requests
import random
import threading
from email.message import EmailMessage
import os
import smtplib

def forget_password(root, goBack):

    for widget in root.winfo_children():
        widget.destroy()

    global random_number
    random_number = ''

    def random_generation():
        return random.randint(10000,100000)
    
    def email_in_thread(to):

        rand = random_generation()
        global random_number
        random_number = str(rand)

        try:

            response = requests.post(
                "https://courier-control.onrender.com/email-pass",
                timeout=60,
            )

            response.raise_for_status()
            data = response.json()

            email_id = "jasimbrothers@gmail.com"

            mail_password = (data("email") or "").replace(" ", "")

            if not mail_password:
                raise ValueError("Missing app password from /email-pass response.")

            msg = EmailMessage()
            msg["From"] = email_id
            msg["To"] = to
            msg["Subject"] = "One time password from JS Programming"
            body = random_number
            msg.set_content(body)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
                server.login(email_id, mail_password)
                server.send_message(msg)

            root.after(0, lambda: messagebox.showinfo("OTP Sent", "A one-time password has been sent to your email.",),)
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", str(e)))


    def checkIfEmailExist():
        emails = email.get().strip().lower()

        if not emails:
            messagebox.showerror("Error", "Please enter valid email to proceed reset.")
            email.focus_set()
            return

        emailButton.configure(state='disabled')

        try:

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
                randomCode.grid()
                newpassword1.grid()
                newpassword2.grid()
                resetButton.grid()
                threading.Thread(target=email_in_thread, args=(emails,), daemon=True).start()
            else:
                emailButton.configure(state='normal')
                randomCode.grid_remove()
                newpassword1.grid_remove()
                newpassword2.grid_remove()
                resetButton.grid_remove()
                messagebox.showerror("Does Not Exist", "The email you provide does not exist. Please recheck the email and try again.")
                return
        except Exception as e:
            emailButton.configure(state="normal")
            randomCode.grid_remove()
            newpassword1.grid_remove()
            newpassword2.grid_remove()
            resetButton.grid_remove()
            messagebox.showerror("Error", str(e))

    def reset_password():
        emails = email.get().lower().strip()
        rand = randomCode.get().strip()
        pass1 = newpassword1.get().strip()
        pass2 = newpassword2.get().strip()

        if rand != random_number:
            messagebox.showerror("Error", "The password does not match.")
            return

        if pass1 != pass2:
            messagebox.showerror("Error", "The password is not same. Please check and enter the same password.")
            return

        if not emails or not rand or not pass1 or not pass2:
            if not emails:
                messagebox.showerror("Error", "Please fill the email address before resetting.")
                email.focus_set()
                return
            elif not rand:
                messagebox.showerror("Error", "Please fill one time password sent to your email.")
                randomCode.focus_set()
                return
            elif not pass1:
                messagebox.showerror("Error", "Please fill in the password")
                newpassword1.focus_set()
                return
            else:
                messagebox.showerror("Error", "Please reenter the password")
                newpassword2.focus_set()
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

    randomCode = ct.CTkEntry(root, width=60)
    randomCode.grid(row=2, column=0, padx=(10,0), pady=(10,0), sticky='w')
    randomCode.grid_remove()

    newpassword1 = ct.CTkEntry(root, placeholder_text='Enter Your New Password', width=300)
    newpassword1.grid(row=3, column=0, padx=(10,0), pady=(10,0), sticky='w')
    newpassword1.grid_remove()

    newpassword2 = ct.CTkEntry(root, placeholder_text="Enter Your Password Again", width=300)
    newpassword2.grid(row=4, column=0, padx=(10,0), pady=(10,0), sticky='w')
    newpassword2.grid_remove()

    resetButton = ct.CTkButton(root, text="Reset", width=50, cursor='hand2', command=reset_password)
    resetButton.grid(row=5, column=0, padx=(10,0), pady=(10,0), sticky='e')
    resetButton.grid_remove()