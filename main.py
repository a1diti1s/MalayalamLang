import tkinter as tk
from tkinter import scrolledtext, messagebox
from interpreter import execute_malayalam_code 

def run_code():
    code = editor.get("1.0", tk.END).strip()  
    try:
        output_text = execute_malayalam_code(code)
        output_console.config(state=tk.NORMAL)
        output_console.delete("1.0", tk.END)
        output_console.insert(tk.END, output_text)
        output_console.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("MalayalamLang IDE")

editor_label = tk.Label(root, text="Write Your Code Here:")
editor_label.pack(padx=10, pady=5)
editor = scrolledtext.ScrolledText(root, width=80, height=15)
editor.pack(padx=10, pady=5)

run_button = tk.Button(root, text="Run Code", command=run_code)
run_button.pack(pady=10)

output_label = tk.Label(root, text="Output:")
output_label.pack(padx=10, pady=5)
output_console = scrolledtext.ScrolledText(root, width=80, height=10, state=tk.DISABLED)
output_console.pack(padx=10, pady=5)

root.mainloop()
