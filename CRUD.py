from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import mysql.connector

def add_user_window():
    add_user_win = Toplevel()
    add_user_win.title("Add User")

    #create labels' entry widgets' add button for adding a user
    Label(add_user_win, text= "First Name").pack()
    first_name_entry = Entry(add_user_win)
    first_name_entry.pack()

    Label(add_user_win, text="Last Name").pack()
    last_name_entry = Entry(add_user_win)
    last_name_entry.pack()

    Label(add_user_win, text="Email").pack()
    email_entry = Entry(add_user_win)
    email_entry.pack()


    #connect to the database and insert the new user data
    def add_user():
        try:
            conn = mysql.connector.connect(host= "localhost", user= "root", password= "", database= "crud")
            cursor = conn.cursor()


        # create table
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users"
                "(id int auto_increment primary key, firstname TEXT, lastname TEXT, email TEXT)")

        #     INSERT USER DATA INTO DATABASE
            insert_query = "INSERT INTO users (firstname, lastname, email) VALUES (%s, %s, %s)"
            user_data = (first_name_entry.get(), last_name_entry.get(), email_entry.get())
            cursor.execute(insert_query, user_data)
            conn.commit()

            messagebox.showinfo("Success", "User added successfully!")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to add user: {e}")

            # def add_user(name):
            #     name = name.strip()
            #     if not name:
            #         messagebox.showerror("Error", "Name cannot be empty")
            #         return

        finally:
            if conn.is_connected():
               cursor.close()
               conn.close()

#      Create a button to addd the user
    add_button = Button(add_user_win, text= 'Add User', command= add_user)
    add_button.pack()

def delete_user_window():
    delete_user_win = Toplevel()
    delete_user_win.title("Delete User")

    # create labels' entry widgets' add button for adding a user
    Label(delete_user_win, text="User ID").pack()
    user_id_entry = Entry(delete_user_win)
    user_id_entry.pack()

    def delete_user():
        try:
            conn = mysql.connector.connect(host= "localhost", user= "root", password= "", database= "crud")
            cursor = conn.cursor()

            # delete user from database
            delete_query = "DELETE FROM users WHERE id = %s"
            user_id = (user_id_entry.get(),)
            cursor.execute(delete_query, user_id)
            conn.commit()

            messagebox.showinfo("Success", "User deleted successfully")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to add user: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

   # Create a button to addd the user
    delete_button = Button(delete_user_win, text= 'Delete User', command= delete_user)
    delete_button.pack()

def update_user_window():
    update_user_win = Toplevel()
    update_user_win.title("Update User")

    Label(update_user_win, text="User ID:").pack()
    userid_entry = Entry(update_user_win)
    userid_entry.pack()

    Label(update_user_win, text="First Name:").pack()
    first_name_entry = Entry(update_user_win)
    first_name_entry.pack()

    Label(update_user_win, text="Last Name:").pack()
    last_name_entry = Entry(update_user_win)
    last_name_entry.pack()

    Label(update_user_win, text="Email:").pack()
    email_entry = Entry(update_user_win)
    email_entry.pack()

    def update_user():
        user_id_str = userid_entry.get()
        first_name = first_name_entry.get().strip()
        last_name = last_name_entry.get().strip()
        email = email_entry.get().strip()

        if not user_id_str.isdigit():
            messagebox.showerror("Error", "User ID must be a number")
            return
        user_id = int(user_id_str)

        if not first_name:
            messagebox.showerror("Error", "First name cannot be empty")
            return
        if not last_name:
            messagebox.showerror("Error", "Last name cannot be empty")
            return
        if not email:
            messagebox.showerror("Error", "Email cannot be empty")
            return

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="crud")
            cursor = conn.cursor()

            update_query = """
                UPDATE users SET firstname = %s, lastname = %s, email = %s WHERE id = %s
            """
            cursor.execute(update_query, (first_name, last_name, email, user_id))
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showerror("Error", "User not found")
            else:
                messagebox.showinfo("Success", "User updated successfully")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update user: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    update_button = Button(update_user_win, text='Update User', command=update_user)
    update_button.pack()

def display_users_window():
    display_users_win = Toplevel()
    display_users_win.title("Display Users")

    Label(display_users_win,text = "User ID:").pack()
    user_id_entry = Entry(display_users_win)
    user_id_entry.pack()

    def view():
        # connect to the database and fetch al users
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="crud")
            cursor = conn.cursor()

        # Fetch all users from the database
            display = "SELECT * FROM users where id = %s"
            display_data = (user_id_entry.get(),)
            cursor.execute(display,display_data)
            users = cursor.fetchall()

        # Display users in a text widget
            users_text = Text(display_users_win)
            for user in users:
                print(user)
            users_text.insert(END, f"ID: {user[0]}," f"First Name: {user[1]}," f"Last Name: {user[2]}," f"Email: {user[3]}\n")
            users_text.pack()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to update user: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    btn = Button(display_users_win, text="Display", command=view)
    btn.pack()

def main():
    root = Tk()
    root.title("User Management App")
    root.geometry("400x400")
    root.resizable(False, False)

    # Load and display the background image
    background_image = Image.open("background.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # Create the rest of the UI on top of the background image
    btn_add_user = Button(root, text="Add User", width=10, command= add_user_window)
    btn_add_user.place(relx=0.1, rely=0.5)

    btn_update_user = Button(root, text="Update User", width=10, command=update_user_window)
    btn_update_user.place(relx=0.3, rely=0.5)

    btn_delete_user = Button(root, text="Delete User", width=10, command = delete_user_window)
    btn_delete_user.place(relx=0.5, rely=0.5)

    btn_display_users = Button(root, text="Display Users", width=10, command = display_users_window)
    btn_display_users.place(relx=0.7, rely=0.5)

    root.mainloop()
main()

