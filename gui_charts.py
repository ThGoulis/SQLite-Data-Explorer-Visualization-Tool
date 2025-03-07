import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui_query_execution import get_query_results
import numpy as np

fig = None  # Global figure for the chart

def generate_chart(x_axis_var, y_axis_var, chart_type_var, grid_var, labels_var, plot_frame, title_var):
    """Dynamically updates the chart when user modifies selections."""
    global fig
    df_result = get_query_results()
    
    if df_result is None or df_result.empty:
        messagebox.showerror("Error", "⚠️ No data to plot! Run a query first.")
        return

    x_col = x_axis_var.get()
    y_col = y_axis_var.get()
    chart_type = chart_type_var.get()
    enable_grid = grid_var.get()
    show_labels = labels_var.get()
    custom_title = title_var.get().strip()

    if not x_col or not y_col:
        messagebox.showerror("Error", "⚠️ Select both X and Y axis!")
        return

    # Handle Categorical vs Numeric X-Axis
    is_x_categorical = not pd.api.types.is_numeric_dtype(df_result[x_col])

    # Ensure Y-Axis is numeric
    try:
        df_result[y_col] = pd.to_numeric(df_result[y_col], errors='coerce')
    except ValueError:
        messagebox.showerror("Error", "⚠️ Y-axis must contain numeric data!")
        return

    fig, ax = plt.subplots(figsize=(9, 5))

    # Handle Dynamic Colors
    num_colors = len(df_result)
    colors = plt.cm.get_cmap("viridis", num_colors)(range(num_colors))

    if chart_type == "Bar":
        # All unique categories are preserved
        categorical_cols = df_result.select_dtypes(include=['object']).columns.tolist()

        # The X-axis column is not mistakenly removed from grouping
        group_by_cols = [x_col] + [col for col in categorical_cols if col != x_col] 

        # Group dynamically if multiple categorical columns exist
        if len(group_by_cols) > 1:
            df_bar = df_result.groupby(group_by_cols, as_index=False)[y_col].sum()
        else:
            df_bar = df_result.copy()
        
        # Convert X-axis to string to ensure categorical plotting
        df_bar["x_labels"] = df_bar[group_by_cols].astype(str).agg(' '.join, axis=1)

        fig, ax = plt.subplots(figsize=(9, 5))

        bars = ax.bar(
            df_bar["x_labels"], 
            df_bar[y_col], 
            color=plt.cm.viridis(np.linspace(0, 1, len(df_bar))),
            alpha=0.7
        )

        # Rotate X-labels for better readability
        ax.set_xticks(range(len(df_bar)))
        ax.set_xticklabels(df_bar["x_labels"], rotation=45, ha="right", fontsize=9)

        # Add labels if enabled
        if show_labels:
            ax.bar_label(bars, fmt="%.2f", fontsize=8, padding=3)

        # Add grid if enabled
        if enable_grid:
            ax.grid(True, linestyle="--", alpha=0.5)

        # Default title
        if not custom_title:
            custom_title = f"{x_col} and {y_col}"  # Default Title if None

        ax.set_title(custom_title, fontsize=12, fontweight="bold")
        ax.set_xlabel(x_col, fontsize=11, fontweight="bold")
        ax.set_ylabel(y_col, fontsize=11, fontweight="bold")
        plt.tight_layout()


        # Clear previous chart before embedding the new one
    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()

    if chart_type == "Heatmap":
        # Extract categorical columns from the DataFrame
        categorical_cols = df_result.select_dtypes(include=['object']).columns.tolist()

        # Ensure X-axis and Y-axis columns exist
        group_by_cols = [x_col] + [col for col in categorical_cols if col != x_col]

        # Check if we have enough categorical data
        if len(group_by_cols) < 2:
            messagebox.showerror("Error", "⚠️ Need at least two categorical columns for a Heatmap!")
            return

        y_col = group_by_cols[1]  # Y-axis is categorical
        values_col = y_axis_var.get()  # Selected numerical column

        # Group by X and Y, then sum numerical values
        df_heatmap = df_result.groupby([x_col, y_col], as_index=False)[values_col].sum()

        # Pivot for Heatmap Format (Rows = X, Columns = Y)
        df_pivot = df_heatmap.pivot(index=x_col, columns=y_col, values=values_col)

        # DataFrame is not empty
        if df_pivot.empty:
            messagebox.showerror("Error", "⚠️ No valid data for Heatmap!")
            return

        # Convert pivot table to NumPy array for Matplotlib
        heatmap_data = df_pivot.to_numpy()

        # Create Figure & Axes
        fig, ax = plt.subplots(figsize=(9, 5))

        # Generate Heatmap using Matplotlib's imshow()
        heatmap = ax.imshow(heatmap_data, cmap="viridis", aspect="auto")

        # Add Color Bar
        cbar = plt.colorbar(heatmap)
        cbar.set_label(values_col, fontsize=10)

        # Set Tick Labels (Ensure readable format)
        ax.set_xticks(range(len(df_pivot.columns)))
        ax.set_xticklabels(df_pivot.columns, rotation=45, ha="right", fontsize=9)

        ax.set_yticks(range(len(df_pivot.index)))
        ax.set_yticklabels(df_pivot.index, fontsize=9)

        # Add Data Labels (Annotations)
        for i in range(len(df_pivot.index)):
            for j in range(len(df_pivot.columns)):
                ax.text(j, i, f"{heatmap_data[i, j]:.1f}", ha="center", va="center", color="white", fontsize=8)

        # Get the title from the user input
        if not custom_title:
            custom_title = f"{x_col} and {y_col}"  # Default Title if None

        ax.set_title(custom_title, fontsize=12, fontweight="bold")
        ax.set_xlabel(x_col, fontsize=11, fontweight="bold")
        ax.set_ylabel(y_col, fontsize=11, fontweight="bold")

        plt.tight_layout()

    # Clear previous chart before embedding the new one
    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()


def export_chart():
    """Saves the chart in PNG, PDF, or SVG format."""
    global fig
    if not fig:
        messagebox.showerror("Error", "⚠️ No chart available to save!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Image", "*.png"),
                                                        ("PDF Document", "*.pdf"),
                                                        ("SVG File", "*.svg")])
    if file_path:
        fig.savefig(file_path, bbox_inches="tight", dpi=300)
        messagebox.showinfo("Success", f"✅ Chart saved successfully: {file_path}")
