import tkinter as tk
from ttkbootstrap import Style
from tkinter import ttk
from gui_database import load_database, table_double_click
from gui_query_execution import execute_query
from gui_export import export_results
from gui_charts import generate_chart, export_chart


default_query = """select aircraft_code, fare_conditions, count(seat_no)  from seats group by aircraft_code, fare_conditions"""

def create_main_window():
    """Creates and returns the main application window."""
    root = Style(theme="darkly").master
    root.title("SQLite Data Explorer")
    root.geometry("700x400")

    # Notebook (Tabbed Interface)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Database Tab
    tab_db = ttk.Frame(notebook)
    notebook.add(tab_db, text="Database")
    
    # Query Execution Tab
    tab_query = ttk.Frame(notebook)
    notebook.add(tab_query, text="Query Execution")

    #Charts Tab
    tab_chart = ttk.Frame(notebook)
    notebook.add(tab_chart, text="Charts")

    def exit_app():
        root.quit()
    
    # Load Database Button
    ttk.Button(tab_db, text="Load Database", command=lambda: load_database(tables_listbox)).pack(pady=5, fill="x")
    
    # Tables Listbox
    tables_listbox = tk.Listbox(tab_db, height=15)
    tables_listbox.pack(fill="both", expand=True, padx=10, pady=5)
    tables_listbox.bind("<Double-Button-1>", lambda event: table_double_click(event, tables_listbox))

    exit_button_db = ttk.Button(tab_db, text="Exit", bootstyle="danger", command=exit_app)
    exit_button_db.pack(pady=10, fill="x")

    # Query Execution UI
    query_entry = tk.Text(tab_query, height=5, width=120)
    query_entry.insert("1.0", default_query)
    query_entry.pack(pady=5, padx=10)

    execute_button = ttk.Button(tab_query, text="Execute Query",
                                command=lambda: execute_query(query_entry, result_frame, x_axis_dropdown, y_axis_dropdown))
    execute_button.pack(pady=5, fill="x")

    export_button = ttk.Button(tab_query, text="Export Data", command=export_results)
    export_button.pack(pady=5, fill="x")

    # Frame to Display Query Results
    result_frame = ttk.Frame(tab_query)
    result_frame.pack(fill="both", expand=True, padx=10, pady=5)

    exit_button_query = ttk.Button(tab_query, text="Exit", bootstyle="danger", command=exit_app)
    exit_button_query.pack(pady=10, fill="x")

    # Chart Sectior
    chart_controls_frame = ttk.Frame(tab_chart)
    chart_controls_frame.pack(fill="x")

    # X-Axis Selection
    ttk.Label(chart_controls_frame, text="X-Axis:").grid(row=0, column=0, padx=5, pady=5)
    x_axis_var = tk.StringVar()
    x_axis_dropdown = ttk.Combobox(chart_controls_frame, textvariable=x_axis_var, state="readonly")
    x_axis_dropdown.grid(row=0, column=1, padx=5, pady=5)

    # Y-Axis Selection
    ttk.Label(chart_controls_frame, text="Y-Axis:").grid(row=0, column=2, padx=5, pady=5)
    y_axis_var = tk.StringVar()
    y_axis_dropdown = ttk.Combobox(chart_controls_frame, textvariable=y_axis_var, state="readonly")
    y_axis_dropdown.grid(row=0, column=3, padx=5, pady=5)

    # Chart Type Selection
    ttk.Label(chart_controls_frame, text="Chart Type:").grid(row=1, column=0, padx=5, pady=5)
    chart_type_var = tk.StringVar(value="Bar")
    chart_type_dropdown = ttk.Combobox(chart_controls_frame, textvariable=chart_type_var, state="readonly",
                                       values=["Bar", "Heatmap"])
    chart_type_dropdown.grid(row=1, column=1, padx=5, pady=5)

    # Grid Checkbox
    grid_var = tk.BooleanVar(value=False)
    grid_check = ttk.Checkbutton(chart_controls_frame, text="Show Grid", variable=grid_var)
    grid_check.grid(row=1, column=2, padx=5, pady=5)

    # Labels Checkbox
    labels_var = tk.BooleanVar(value=False)
    labels_check = ttk.Checkbutton(chart_controls_frame, text="Show Labels", variable=labels_var)
    labels_check.grid(row=1, column=3, padx=5, pady=5)

    # Marker Size Slider
    ttk.Label(chart_controls_frame, text="Marker Size:").grid(row=2, column=1, padx=5, pady=5)
    marker_size_var = tk.IntVar(value=5)
    marker_size_slider = ttk.Scale(chart_controls_frame, from_=1, to=20, variable=marker_size_var, orient="horizontal")
    marker_size_slider.grid(row=2, column=2, padx=5, pady=5)

    ttk.Label(tab_chart, text="Chart Title:").pack()
    title_var = tk.StringVar(value="Title")  # Default Title
    title_entry = ttk.Entry(tab_chart, textvariable=title_var, width=40)
    title_entry.pack(pady=5)

    # Generate Chart Button
    generate_button = ttk.Button(tab_chart, text="Generate Chart",
                            command=lambda: generate_chart(x_axis_var, y_axis_var, chart_type_var, grid_var, labels_var, marker_size_var, plot_frame, title_var))
    generate_button.pack(pady=5, fill="x")

    # Save Chart Button
    save_chart_button = ttk.Button(tab_chart, text="Save Chart", command=export_chart)
    save_chart_button.pack(pady=5, fill="x")

    exit_button_chart = ttk.Button(tab_chart, text="Exit", bootstyle="danger", command=exit_app)
    exit_button_chart.pack(pady=10, fill="x")

    # Frame to Display Chart
    plot_frame = ttk.Frame(tab_chart)
    plot_frame.pack(fill="both", expand=True, padx=10, pady=10)


    
    return root
