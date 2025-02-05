import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import platform
import os
import requests
import json
import base64
import random
import string
import smtplib
from email.mime.text import MIMEText

password_verification=""

def generate_password(min_length=9, max_length=27):
  password_length = random.randint(min_length, max_length)
  characters = string.ascii_letters + string.digits + string.punctuation
  password = ''.join(random.choice(characters) for _ in range(password_length))
  return password

def send_mail(mail, pwd):
  sender_email = "davuaman9@gmail.com"
  password = "jgpm xbrv rzqs lcgh" 

  receiver_email = email_entry.get()
  message = MIMEText(pwd)
  message["Subject"] = "Test Email"
  message["From"] = sender_email
  message["To"] = receiver_email

  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, message.as_string())

  print("Email sent successfully!")

def check_virustotal(url):
  url_ascii = url.encode("ascii")
  base64_url = base64.b64encode(url_ascii)
  url_id = base64_url.decode("ascii")
  if "==" in url_id:
    url_id = url_id[:-2]
  urls = "https://www.virustotal.com/api/v3/urls/"
  urls = urls+url_id
  
  headers = {"accept": "application/json", "x-apikey": "91c9d080cc7f315dc33f58fa7354d79fccd01c81a898c57efda8bfd3d0f3ba6d"}
  response = requests.get(urls, headers=headers)  
  response = response.json()
  print(response['data']['attributes']['last_analysis_stats']['malicious'])
  if response['data']['attributes']['last_analysis_stats']['malicious'] >= 2 :
    return True
  else:
    return False


def block_website():
  password = generate_password()
  send_mail(email_entry.get(), password)
  password_verification = simpledialog.askstring("Enter Password", "Enter the password sent to your email:")
  #print(password_verification)
  block = check_virustotal(website_entry.get())
  
  if website_entry.get()=="":
    messagebox.showerror("Error","Please Enter a Website")
    return
  if password_verification=="":
    messagebox.showerror("Error","Please Enter a Password")
    return
  if password_verification!=password:
    messagebox.showerror("Error","Please Enter a Password")
    return
  if password_verification == password and block:
    websites_to_block=website_entry.get()
    system_name=platform.system()
    if system_name == "Windows":
      hosts_path=r"C:\Windows\System32\drivers\etc\hosts"
    elif system_name == "Linux" or system_name == "Darwin" :
      hosts_path = "/etc/hosts"
    else:
      messagebox.showerror("Error","Unsupported operating system:"+system_name)
      return

    with open(hosts_path,"a") as hosts_file:
      entry = "127.0.0.1 " + website_entry.get() + "\n"
      hosts_file.write(entry)
    messagebox.showinfo("Blocked" , "Successfully website blocked")
  else:
    messagebox.showinfo("Not Blocked", "The website is not malicious")


def unblock_website():
    password = generate_password()
    send_mail(email_entry.get(), password)
    password_verification = simpledialog.askstring("Enter Password", "Enter the password sent to your email:")
    print(password_verification + " pass:" + password)
    unblock = check_virustotal(website_entry.get())
    if website_entry.get() == "":
        messagebox.showerror("Error","please enter a website")
        return
    if password_verification == "":
        messagebox.showerror("Error","please enter a passowrd")
        return
    if password_verification !=password:
        messagebox.showerror("error","please enter a valid password")
        return
    if password_verification == password and unblock==False:
        websites_to_unblock = website_entry.get()
        system_name=platform.system()
        if system_name=="Windows":
            hosts_path=r"C:\Windows\System32\drivers\etc\hosts"
        elif system_name == "Linux" or system_name =="Darwin":
            hosts_path="/etc/hosts"
        else:
            messagebox.showerror("error","unsupported operating system:"+system_name)
            return
        with open(hosts_path,"r") as hosts_file:
            lines = hosts_file.readlines()
        with open(hosts_path, "w")as hosts_file:
            print(lines)
            for line in lines:
                should_remove=False
                if website_entry.get() in line:
                    should_remove = True
                    break
                if not should_remove:
                    hosts_file.write(line)
        messagebox.showinfo("unblocked","successfully website unblocked")
    else:
      messagebox.showinfo("Cannot Unblock", "This is a malicious site cannot unblock")

root = tk.Tk()
root.title("Website Blocker")

# Gruvbox color palette
bg_color = "#282828"
fg_color = "#fbf1c7"
accent_color = "#d79921"

button_bg_color = "#ebdbb2"
button_fg_color = "#282828"
button_border_color = "#b8bb26"

#background
root.configure(bg=bg_color)

root.geometry("800x600")

# Create style
style = ttk.Style()
style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color, foreground="#d65d0e", font=("Arial", 12))
style.configure("TButton", background=button_bg_color, foreground=button_fg_color, bordercolor=button_border_color, font=("Arial", 12)) 
style.map("TButton", background=[("active", "#b16286")])

# Entry for website URL
website_label = ttk.Label(root, text="Website URL:", style="TLabel")
website_label.pack(pady=5)
website_entry = ttk.Entry(root)
website_entry.pack(pady=5)

# Entry for password
"""
password_label = ttk.Label(root, text="Password:", style="TLabel")
password_label.pack(pady=5)
password_entry = ttk.Entry(root, show="*")
password_entry.pack(pady=5)
"""
email_label = ttk.Label(root, text="Enter Email:", style="TLabel")
email_label.pack(pady=5)

email_entry = ttk.Entry(root)
email_entry.pack(pady=5)

# block button
block_button = ttk.Button(root, text="Block", command = block_website, style="TButton")
block_button.pack(side=tk.TOP, pady=(50, 10))

# Unblock website
unblock_button = ttk.Button(root, text="Unblock", command = unblock_website, style="TButton")
unblock_button.pack(side=tk.TOP, pady=10)

root.mainloop()