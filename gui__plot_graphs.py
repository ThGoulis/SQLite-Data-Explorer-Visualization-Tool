import os
import sqlite3
import ttkbootstrap as ttk  
from ttkbootstrap import Style
from tkinter import filedialog, messagebox, Toplevel
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main():
    # Create Main Window
    root = ttk.Window(themename="darkly")  
    style = Style(theme="darkly")
    root.title("SQLite Data Explorer")
    root.geometry("1300x800")

    # Function to Load Database
    def load_database():
        global conn
        db_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.sqlite"), ("All Files", "*.*")])
        if db_path:
            if conn:
                conn.close()  # Close existing connection
            conn = sqlite3.connect(db_path)
            messagebox.showinfo("Success", "Database Loaded Successfully!")
            show_tables()

    # Function to Show Tables in a Pop-up Window
    def show_tables():
        if not conn:
            messagebox.showerror("Error", "Load a database first!")
            return
        
        tables_window = Toplevel(root)
        tables_window.title("Database Tables")
        tables_window.geometry("400x500")
        tables_window.transient(root)  # Allows user to interact with the main window
        
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        ttk.Label(tables_window, text="Tables in Database:", font=("Arial", 12, "bold")).pack(pady=10)
        
        for table in tables:
            ttk.Label(tables_window, text=table[0], font=("Arial", 10)).pack(anchor="w", padx=10)

    # Function to Execute SQL Query
    def execute_query():
        global df_result
        if not conn:
            messagebox.showerror("Error", "Load a database first!")
            return
        
        query = query_entry.get("1.0", "end-1c")
        if not query.strip():
            messagebox.showerror("Error", "Enter a SQL query!")
            return
        
        try:
            df_result = pd.read_sql_query(query, conn)
            update_column_selection()
            messagebox.showinfo("Success", "Query Executed Successfully!")
        except Exception as e:
            messagebox.showerror("SQL Error", str(e))

    # Function to Update Column Selection After Query Execution
    def update_column_selection():
        columns = df_result.columns.tolist()
        x_axis_dropdown["values"] = columns
        y_axis_dropdown["values"] = columns
        x_axis_dropdown.current(0) if columns else None
        y_axis_dropdown.current(1) if len(columns) > 1 else None

    # Function to Generate Chart
    def generate_chart():
        global fig
        if df_result is None or df_result.empty:
            messagebox.showerror("Error", "No data to plot! Run a query first.")
            return
        
        x_col = x_axis_var.get()
        y_col = y_axis_var.get()
        chart_type = chart_type_var.get()
        
        if not x_col or not y_col:
            messagebox.showerror("Error", "Select both X and Y axis!")
            return
        
        fig, ax = plt.subplots(figsize=(8, 5))

        if chart_type == "Bar":
            colors = plt.cm.viridis(range(len(df_result)))  
            ax.bar(df_result[x_col], df_result[y_col], color=colors, alpha=0.7)
        elif chart_type == "Line":
            ax.plot(df_result[x_col], df_result[y_col], marker="o", linestyle="-", color="blue")
        elif chart_type == "Scatter":
            colors = plt.cm.plasma(range(len(df_result)))
            ax.scatter(df_result[x_col], df_result[y_col], color=colors, alpha=0.7)

        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{chart_type} Chart: {x_col} vs {y_col}")
        
        for widget in plot_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()

    # Function to Export Chart as PNG
    def export_as_png():
        global fig
        if fig is None:
            messagebox.showerror("Error", "No chart available to export!")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            fig.savefig(file_path, dpi=300)
            messagebox.showinfo("Success", "Chart saved as PNG!")

    # Function to Export Chart as PDF
    def export_as_pdf():
        global fig
        if fig is None:
            messagebox.showerror("Error", "No chart available to export!")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            fig.savefig(file_path, format="pdf", dpi=300)
            messagebox.showinfo("Success", "Chart saved as PDF!")

    # Function to Export Query Results as CSV
    def export_as_csv():
        global df_result
        if df_result is None or df_result.empty:
            messagebox.showerror("Error", "No data available to export!")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            df_result.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Data exported as CSV!")

    # Function to Exit the Application
    def exit_application():
        root.quit()
        root.destroy()

    # LAYOUT - Two Column Design
    left_frame = ttk.Frame(root)
    left_frame.pack(side="left", padx=10, pady=10, fill="y")
    right_frame = ttk.Frame(root)
    right_frame.pack(side="right", padx=10, pady=10, expand=True, fill="both")

    # LEFT PANEL - Database & Query
    load_db_button = ttk.Button(left_frame, text="Load Database", bootstyle="primary", command=load_database)
    load_db_button.pack(pady=5, fill="x")

    query_entry = ttk.Text(left_frame, height=5, width=50)
    query_entry.pack(pady=5)

    execute_button = ttk.Button(left_frame, text="Execute Query", bootstyle="success", command=execute_query)
    execute_button.pack(pady=5, fill="x")

    # Chart Type Selection
    chart_type_var = ttk.StringVar(value="Bar")
    chart_type_dropdown = ttk.Combobox(left_frame, textvariable=chart_type_var, values=["Bar", "Line", "Scatter"])
    chart_type_dropdown.pack(pady=5, fill="x")

    # X & Y Axis Selection
    ttkwrap = ttk.LabelFrame(left_frame, text="Select Axis")
    ttkwrap.pack(pady=5, fill="x")

    x_axis_var = ttk.StringVar()
    y_axis_var = ttk.StringVar()

    x_axis_dropdown = ttk.Combobox(ttkwrap, textvariable=x_axis_var)
    x_axis_dropdown.pack(pady=2, fill="x")

    y_axis_dropdown = ttk.Combobox(ttkwrap, textvariable=y_axis_var)
    y_axis_dropdown.pack(pady=2, fill="x")

    plot_button = ttk.Button(left_frame, text="Generate Chart", bootstyle="info", command=generate_chart)
    plot_button.pack(pady=10, fill="x")

    # Export Buttons
    export_csv_button = ttk.Button(left_frame, text="Export as CSV", bootstyle="secondary", command=export_as_csv)
    export_csv_button.pack(pady=5, fill="x")

    export_png_button = ttk.Button(left_frame, text="Export as PNG", bootstyle="secondary", command=export_as_png)
    export_png_button.pack(pady=5, fill="x")

    export_pdf_button = ttk.Button(left_frame, text="Export as PDF", bootstyle="secondary", command=export_as_pdf)
    export_pdf_button.pack(pady=5, fill="x")

    # Exit Button
    exit_button = ttk.Button(left_frame, text="Exit", bootstyle="danger", command=exit_application)
    exit_button.pack(pady=10, fill="x")

    # RIGHT PANEL - Visualization
    plot_frame = ttk.Frame(right_frame)
    plot_frame.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == '__main__':
    main()