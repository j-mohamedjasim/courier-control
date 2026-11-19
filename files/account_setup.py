import customtkinter as ct
from tkinter import messagebox
import webbrowser
import requests


def SetupAccountWindow(root, goBack):

    global get_payment

    get_payment = 0.00

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Create Account")
    root.geometry("700x700")

    def start_payment():
        f_name = name.get()
        f_email = email.get()
        f_postcode = postcode.get()
        selected_plan = subscriptionType.get()

        if selected_plan == 'One Time':
            plan = "One Time"
        elif selected_plan == "Monthly":
            plan = "Monthly"
        else:
            plan = "Yearly"
        response = requests.post(
            "https://courierControl.onrender.com/create-checkout",
            json={
                "name": f_name,
                "email": f_email,
                "postcode": f_postcode,
                "selected_plan": plan,
            },
            timeout=40,
        )
        data = response.json()
        webbrowser.open(data["checkout_url"])

    def show_amount(choice):
        global get_payment
        pay = subscriptionType.get()

        if pay == 'One Time':
            payment.grid()
            payment.configure(text='£20.00', font=("Helvatica", 20, 'bold'), text_color='green')
            proceed_to_payment.grid()
            get_payment = 20.00
        elif pay =='Monthly':
            payment.grid()
            proceed_to_payment.grid()
            payment.configure(text='£10.00 Monthly', font=("Helvatica", 20, 'bold'), text_color='green')
            get_payment = 10.00
        elif pay == 'Yearly':
            payment.grid()
            payment.configure(text='£120.00 Annualy', font=("Helvatica", 20, 'bold'), text_color='green')
            proceed_to_payment.grid()
            get_payment = 120.00
        else:
            payment.grid_remove()


    def accountType_def(event=None):
        accType = accountType.get()

        global get_payment

        if accType == 'Basic':
            messagebox.showinfo("Information", 'This is basic account and it is free with limited access.', icon='info')
            subscriptionType.grid_remove()
        elif accType == 'Paid':
            response = messagebox.askyesno("Information", "This paid account and you will have access to everything and choose your options", icon='info')
            if response:
                subscriptionType.grid()
                subscriptionType.set("One Time")
                payment.configure(text='£7.00', font=("Helvatica", 20, 'bold'), text_color='green')
                get_payment = 7.00
            else:
                subscriptionType.grid_remove()

    backButton = ct.CTkLabel(root, text='< Back', cursor='hand2')
    backButton.grid(row=0, column=0, padx=(10,0), pady=(5,0), sticky='w')
    backButton.bind("<Button-1>", lambda event: goBack())

    company = ct.CTkEntry(root, placeholder_text="Your Company Name", width=300)
    company.grid(row=1, column=0, padx=(10,0), pady=(10,0), sticky='w')

    name = ct.CTkEntry(root, placeholder_text="Your Full Name", width=300)
    name.grid(row=2, column=0, padx=(10,0), pady=(10,0), sticky='w')

    address1 = ct.CTkEntry(root, placeholder_text="Company Address 1", width=300)
    address1.grid(row=3, column=0, padx=(10,0), pady=(10,0), sticky='w')

    address2 = ct.CTkEntry(root, placeholder_text="Company Address 2", width=300)
    address2.grid(row=4, column=0, padx=(10,0), pady=(10,0), sticky='w')

    city = ct.CTkEntry(root, placeholder_text="City", width=300)
    city.grid(row=5, column=0, padx=(10,0), pady=(10,0), sticky='w')

    postcode = ct.CTkEntry(root, placeholder_text="Postcode", width=300)
    postcode.grid(row=6, column=0, padx=(10,0), pady=(10,0), sticky='w')

    email = ct.CTkEntry(root, placeholder_text="email@email.com", width=300)
    email.grid(row=2, column=1, padx=(10,0), pady=(10,0), sticky='w')

    username = ct.CTkEntry(root, placeholder_text="Create Username", width=300)
    username.grid(row=3, column=1, padx=(10,0), pady=(10,0), sticky='w')

    password = ct.CTkEntry(root, placeholder_text="Enter Password", show="*", width=300)
    password.grid(row=4, column=1, padx=(10,0), pady=(10,0), sticky='w')

    reEnter = ct.CTkEntry(root, placeholder_text="Re Enter Password", show="*", width=300)
    reEnter.grid(row=5, column=1, padx=(10,0), pady=(10,0), sticky='w')

    userJobTitle = ct.CTkComboBox(root, values=['Manager', 'Managing Director', 'Supervisor'], state='readonly', width=200)
    userJobTitle.grid(row=1, column=1, padx=(10,0), pady=(10,0), sticky='w')
    userJobTitle.set("Select Job Title")

    accountInfo = ct.CTkScrollableFrame(root, width=320, height=320, label_text="Account Info")
    accountInfo.grid(row=7, column=0, padx=(10,0), pady=(10,0), columnspan=2)

    accountType = ct.CTkComboBox(accountInfo, values=['Basic', 'Paid'], state='readonly', command=accountType_def)
    accountType.grid(row=0, column=0, padx=(10,0), pady=(10,0), sticky='w')
    accountType.bind("<<ComboboxSelected>>", accountType_def)
    accountType.set("Account Type")

    subscriptionType = ct.CTkComboBox(accountInfo, values=['One Time', 'Monthly', 'Yearly'], state='readonly', command=show_amount)
    subscriptionType.grid(row=1, column=0, padx=(10,0), pady=(10,0), sticky='w')
    subscriptionType.grid_remove()

    payment = ct.CTkLabel(accountInfo, text='')
    payment.grid(row=2, column=0, padx=(10,0), pady=(10,0), sticky='w')
    payment.grid_remove()

    proceed_to_payment = ct.CTkButton(accountInfo, text='Proceed To Payment', command=start_payment)
    proceed_to_payment.grid(row=3, column=0, padx=(10,0), pady=(10,0), sticky='w')
    proceed_to_payment.grid_remove()

    submitButton = ct.CTkButton(root, text="Create Account")
    submitButton.grid(row=7, column=1, padx=(10,0), pady=(10,0), sticky='e')