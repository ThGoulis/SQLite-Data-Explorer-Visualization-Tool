from tkinter import filedialog, messagebox, Toplevel, Listbox, Scrollbar
import db_connection  # ✅ Import the new connection manager

def load_database(tables_listbox):
    """Loads an SQLite database and shows its tables."""
    db_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.sqlite"), ("All Files", "*.*")])
    if db_path:
        db_connection.set_connection(db_path)  # ✅ Set connection
        messagebox.showinfo("Success", "✅ Database Loaded Successfully!")
        show_tables(tables_listbox)

def show_tables(tables_listbox):
    """Displays available tables in the loaded database."""
    conn = db_connection.get_connection()
    if conn is None:
        messagebox.showerror("Error", "⚠️ Load a database first!")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    tables_listbox.delete(0, "end")  # Clear existing items
    for table in tables:
        tables_listbox.insert("end", table[0])  # Add table names to listbox

def table_double_click(event, tables_listbox):
    """Fetches the table columns and shows them in a popup when a table is double-clicked."""
    selected = tables_listbox.curselection()

    if selected:
        table_name = tables_listbox.get(selected[0])
        conn = db_connection.get_connection()
        
        if conn is None:
            messagebox.showerror("Error", "⚠️ Load a database first!")
            return

        # Get column names using PRAGMA
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]  # Column names are in the second field

        # ✅ Show Popup Window
        popup = Toplevel()
        popup.title(f"Columns in {table_name}")
        popup.geometry("300x300")

        # Scrollable Listbox for Columns
        scrollbar = Scrollbar(popup)
        scrollbar.pack(side="right", fill="y")

        column_listbox = Listbox(popup, yscrollcommand=scrollbar.set)
        column_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columns:
            column_listbox.insert("end", col)

        scrollbar.config(command=column_listbox.yview)
