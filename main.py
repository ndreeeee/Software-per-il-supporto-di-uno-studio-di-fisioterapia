import tkinter as tkk
from model.login import Login
from views.login_view import LoginView

def main():
    root = tkk.Tk()
    root.geometry("900x700")
    controller = Login(root)
    LoginView(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()