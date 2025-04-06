import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from FEM_solver import FEM


def plot_fem():
    try:
        N = int(entry.get())
        if N <= 0:
            raise ValueError("N must be positive.")

        x, phi = FEM(N)

        for widget in frame_plot.winfo_children():
            widget.destroy()

        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
        ax.plot(x, phi, 'b-')
        ax.set_title("Electromagnetic Potential")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except ValueError as e:
        messagebox.showerror("Error", f"Wrong value of N: {e}")

window = Tk()
window.title("Finite Element Method (FEM)")
window.geometry("600x500")

Label(window, text="Number of points:").pack()
entry = Entry(window)
entry.pack()

Button(window, text="Draw", command=plot_fem).pack()

frame_plot = Frame(window, width=600, height=400)
frame_plot.pack_propagate(False)
frame_plot.pack(pady=10)

window.mainloop()
