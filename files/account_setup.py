import customtkinter as ct
from tkinter import messagebox
import webbrowser
import requests

plan_price = {"One time": 0.00,
              "Monthly": 0.00,
              "Annually": 0.00}

payment_success = False
session_id = ''

def get_prices():
    try:
        response = requests.post(
            "https://courier-control.onrender.com/price-plan",
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()

        plan_price["One time"] = data["One time"]
        plan_price["Monthly"] = data["Monthly"]
        plan_price["Annually"] = data["Annually"]
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    
#get_prices()

def checkIfPaid():
    global payment_success
    try:
        response = requests.post(
            "https://courier-control.onrender.com/check-paid",
            json={
                "session_id": session_id,
                "email": email,
                "username": username,
            },
            timeout=60,
        )
        if response.status_code == 404:
            payment_success = False
            messagebox.showerror(
                "Error",
                "Payment did not go through or it was cancelled. Please double check and contact us if needed.",
            )
            return

        response.raise_for_status()
        data = response.json()

        is_paid = bool(data.get("success")) and bool(data.get("active", True))

        if is_paid:
            payment_success = True
            messagebox.showinfo(
                "Success",
                "You have paid! Please proceed to create account.",
            )
        else:
            payment_success = False
            messagebox.showerror(
                "Error",
                "Payment did not go through or it was cancelled. Please double check and contact us if needed.",
            )
    except Exception as e:
        payment_success = False
        messagebox.showerror("Error", str(e))

def SetupAccountWindow(root, goBack):

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Create Account")
    root.geometry("700x700")

    def noToPayAgain():
        proceed_to_payment.configure(state='normal')
        lable_assurance.grid_remove()
        yesButton.grid_remove()
        noButton.grid_remove()

    def start_payment():
        f_name = name.get().strip().title()
        f_email = email.get().strip()
        f_postcode = postcode.get().strip().upper()
        selected_plan = subscriptionType.get().strip()

        if f_name == '' or f_email == '' or f_postcode == '':
            if f_name == '':
                messagebox.showerror('Error', "Please fill your name before select plan and pay for it.")
                name.focus_set()
                return
            elif f_email == '':
                messagebox.showerror('Error', 'Please fill your vaild email before select plan and pay for it.')
                email.focus_set()
                return
            elif f_postcode == '':
                messagebox.showerror('Error', 'Please fill your postcode before select plan and pay for it.')
                postcode.focus_set()
                return
        proceed_to_payment.configure(state='disabled')
        lable_assurance.grid()
        yesButton.grid()
        noButton.grid()

        if selected_plan == 'One Time':
            plan = "One Time"
        elif selected_plan == "Monthly":
            plan = "Monthly"
        else:
            plan = "Yearly"
        response = requests.post(
            "https://courier-control.onrender.com/create-checkout",
            json={
                "name": f_name,
                "email": f_email,
                "postcode": f_postcode,
                "selected_plan": plan,
            },
            timeout=60,
        )

        data = response.json()
        if response.ok and "checkout_url" in data:
            global session_id
            session_id = data["session_id"]
            webbrowser.open(data["checkout_url"])

    def show_amount(choice):
        pay = subscriptionType.get()

        if pay == 'One Time':
            payment.grid()
            payment.configure(text=f"£{plan_price['One time']:.2f}", font=("Helvatica", 20, "bold"), text_color="green")
            proceed_to_payment.grid()
        elif pay =='Monthly':
            payment.grid()
            proceed_to_payment.grid()
            payment.configure(text=f"{plan_price['Monthly']:.2f} Month", font=("Helvatica", 20, "bold"), text_color="green")
        elif pay == 'Yearly':
            payment.grid()
            payment.configure(text=f"{plan_price['Annually']:.2f} Annually", font=("Helvatica", 20, "bold"), text_color="green")
            proceed_to_payment.grid()
        else:
            payment.grid_remove()


    def accountType_def(event=None):
        accType = accountType.get()

        if accType == 'Basic':
            messagebox.showinfo("Information", 'This is basic account and it is free with limited access.', icon='info')
            subscriptionType.grid_remove()
            lable_assurance.grid_remove()
            yesButton.grid_remove()
            noButton.grid_remove()
        elif accType == 'Paid':
            response = messagebox.askyesno("Information", "This paid account and you will have access to everything and choose your options", icon='info')
            if response:
                subscriptionType.grid()
                subscriptionType.set("One Time")
                payment.configure(text=plan_price['One time'], font=("Helvatica", 20, 'bold'), text_color='green')
            else:
                subscriptionType.grid_remove()

    def createAccount():
        companyName = company.get().strip().title()
        fullName = name.get().strip().title()
        address_1 = address1.get().strip().title()
        address_2 = address2.get().strip().title()
        cityName = city.get().strip().title()
        fullPostcode = postcode.get().strip().upper()
        fullEmail = email.get().strip().lower()
        user = username.get().strip().lower()
        password1 = password.get().strip()
        password2 = reEnter.get().strip()
        userJob = userJobTitle.get().strip()

        if not payment_success:
            messagebox.showerror("Payment Required", "Please verify your payment before creating an account.", icon='error')
            return

        if password1 != password2:
            messagebox.showerror("Error", "The passwords are mismatching. Please enter the same password.")
            return        

        if companyName == '' or fullName == '' or address_1 == '' or cityName == '' or fullPostcode == '' or fullEmail == '' or user == '' or password1 == '' or password2 == '' or userJob == '':
            if companyName == '':
                messagebox.showerror("Error", "Please fill company name.")
                company.focus_set()
                return
            elif fullName == '':
                messagebox.showerror("Error", "Please fill full name.")
                name.focus_set()
                return
            elif address_1 == '':
                messagebox.showerror("Error", "Please fill address field")
                address1.focus_set()
                return
            elif cityName == '':
                messagebox.showerror("Error", "Please fill city.")
                city.focus_set()
                return
            elif fullPostcode == '':
                messagebox.showerror("Error", "Please fill postcode.")
                postcode.focus_set()
                return
            elif user == '':
                messagebox.showerror("Error", "Please fill username.")
                username.focus_set()
                return
            elif password1 == '':
                messagebox.showerror("Error", "Please type password.")
                password.focus_set()
                return
            elif password2 == '':
                messagebox.showerror("Error", "Please repeat the password again.")
                reEnter.focus_set()
                return
            elif userJob == '':
                messagebox.showerror("Error", "Please select the user job title.")
                userJobTitle.focus_set()
                return

        submitButton.configure(state='disabled')

        response = requests.post(
            "https://courier-control.onrender.com/check-unique",
            json={
                "email": fullEmail,
                "username": user,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("unique") is True or data.get("success") is True:
            pass
        else:
            messagebox.showerror("Error", "Please select unique email or username as one of them already exist.")
            submitButton.configure(state='normal')
            return
        
        try:
            response1 = requests.post(
                "https://courier-control.onrender.com/create-account",
                json={
                    "company": companyName,
                    "name": fullName,
                    "address1": address_1,
                    "address2": address_2,
                    "city": cityName,
                    "postcode": fullPostcode,
                    "username": user,
                    "password": password1,
                    "userJob": userJob,
                    "email": fullEmail,
                },
                timeout=60,
            )
            if response1.status_code == 404:
                messagebox.showerror(
                    "Error",
                    "No matching payment record was found. Please check your email and try again.",
                    icon="error",
                )
                submitButton.configure(state="normal")
                return
            
            response1.raise_for_status()
            data1 = response1.json()

            if data1.get("success") is True:
                messagebox.showinfo("Success", "You have successfully created an account. Please go back and login with the credentials provided", icon='info')
                goBack()
            else:
                messagebox.showerror("Error", "Account is not created. Please try again.", icon='error')
                submitButton.configure(state='normal')
                return
        except Exception as e:
            messagebox.showerror("Error", str(e), icon="error")
            submitButton.configure(state="normal")
            return

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

    global email, username

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
    accountInfo._scrollbar.grid_forget()

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

    lable_assurance = ct.CTkLabel(accountInfo, text="Click 'Yes' below after paid", font=("Helvatica", 18, "italic"), text_color="brown")
    lable_assurance.grid(row=4, column=0, padx=(10,0), pady=(10,0), columnspan=2)
    lable_assurance.grid_remove()

    yesButton = ct.CTkButton(accountInfo, text="Yes", fg_color="green", command=checkIfPaid)
    yesButton.grid(row=5, column=0, padx=(10,0), pady=(10,0), sticky='w')
    yesButton.grid_remove()

    noButton = ct.CTkButton(accountInfo, text="No", fg_color="red", command=noToPayAgain)
    noButton.grid(row=5, column=1, padx=(10,0), pady=(10,0), sticky='w')
    noButton.grid_remove()

    submitButton = ct.CTkButton(root, text="Create Account", command=createAccount)
    submitButton.grid(row=8, column=1, padx=(10,0), pady=(10,0), sticky='e')