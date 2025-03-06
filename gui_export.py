import os
from tkinter import filedialog, messagebox
import gui_query_execution  # Import the module, not `df_result`

def export_results():
    """Exports the query results to CSV, JSON, or Excel."""
    df_result = gui_query_execution.get_query_results()  # Fetch results dynamically

    if df_result is None or df_result.empty:
        messagebox.showerror("Error", "⚠️ No data to export! Run a query first.")
        return

    file_type = filedialog.asksaveasfilename(
        defaultextension="",
        filetypes=[
            ("CSV File", "*.csv"),
            ("JSON File", "*.json"),
            ("Excel File", "*.xlsx"),
        ],
        title="Save File As"
    )

    if not file_type:
        return  # User canceled

    try:
        if file_type.endswith(".csv"):
            df_result.to_csv(file_type, index=False)
        elif file_type.endswith(".json"):
            df_result.to_json(file_type, orient="records", indent=4)
        elif file_type.endswith(".xlsx"):
            df_result.to_excel(file_type, index=False)

        messagebox.showinfo("Success", f"✅ Data exported successfully as {os.path.basename(file_type)}!")

    except Exception as e:
        messagebox.showerror("Export Error", f"❌ Failed to export data:\n{str(e)}")
