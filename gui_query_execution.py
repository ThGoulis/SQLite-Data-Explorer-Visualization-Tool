import pandas as pd
from tkinter import messagebox, ttk
import db_connection

_df_result = None  # Private variable to store query results

def execute_query(query_entry, result_frame, x_axis_dropdown, y_axis_dropdown):
    """Executes the SQL query and displays the results in a table."""
    global _df_result

    conn = db_connection.get_connection()  # ✅ Use db_connection instead
    if not conn:
        messagebox.showerror("Error", "⚠️ Load a database first!")
        return

    query = query_entry.get("1.0", "end-1c").strip()
    if not query:
        messagebox.showerror("Error", "⚠️ Enter a valid SQL query!")
        return

    try:
        _df_result = pd.read_sql_query(query, conn)
        display_results_table(_df_result, result_frame)
        update_column_selection(x_axis_dropdown, y_axis_dropdown)  # ✅ Update dropdowns
        messagebox.showinfo("Success", "✅ Query Executed Successfully!")
        
    except Exception as e:
        messagebox.showerror("SQL Error", f"❌ SQL Execution Failed:\n{str(e)}")


def display_results_table(df, result_frame):
    """Displays the query results in a Treeview widget."""
    # Clear old data
    for widget in result_frame.winfo_children():
        widget.destroy()

    if df.empty:
        ttk.Label(result_frame, text="⚠️ No data returned from the query!", font=("Arial", 10, "bold"), foreground="red").pack()
        return

    # Create Scrollbars
    tree_scroll_y = ttk.Scrollbar(result_frame, orient="vertical")
    tree_scroll_x = ttk.Scrollbar(result_frame, orient="horizontal")

    # Create Treeview
    tree = ttk.Treeview(
        result_frame,
        bootstyle="primary",
        show="headings",
        xscrollcommand=tree_scroll_x.set,  # Link horizontal scroll
        yscrollcommand=tree_scroll_y.set   # Link vertical scroll
    )
    
    # Pack Scrollbars
    tree_scroll_y.pack(side="right", fill="y")
    tree_scroll_x.pack(side="bottom", fill="x")

    # Configure Scrollbars
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    # Define columns
    tree["columns"] = list(df.columns)

    # Set column headings and adjust column width dynamically
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="w")  # Adjust column width

    # Insert rows
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    # Pack Treeview
    tree.pack(expand=True, fill="both")

def update_column_selection(x_axis_dropdown, y_axis_dropdown):
    """Updates X and Y dropdown menus with the column names from query results."""
    global _df_result
    if _df_result is None or _df_result.empty:
        return

    columns = _df_result.columns.tolist()
    
    # ✅ Update dropdown values
    x_axis_dropdown["values"] = columns
    y_axis_dropdown["values"] = columns

    # ✅ Set defaults
    if columns:
        x_axis_dropdown.current(0)
        if len(columns) > 1:
            y_axis_dropdown.current(1)

def get_query_results():
    """Returns the stored DataFrame with query results."""
    global _df_result
    return _df_result
