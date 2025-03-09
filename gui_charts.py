import seaborn as sns
from tkinter import messagebox, filedialog
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

    sns.set_style("whitegrid")

    fig, ax = plt.subplots(figsize=(7, 4), dpi=200)

    if chart_type == "Bar":
        # All unique categories are preserved
        categorical_cols = df_result.select_dtypes(include=['object']).columns.tolist()
        
        # Use hue if another categorical variable exists
        hue_col = "fare_conditions" if "fare_conditions" in categorical_cols and x_col != "fare_conditions" else None

        # Sorting the X-axis
        df_result[x_col] = df_result[x_col].astype(str)
        df_result = df_result.sort_values(by=[x_col, y_col])

        # Seaborn Bar Plot
        sns.barplot(
            data=df_result,
            x=x_col, 
            y=y_col,
            hue=hue_col,
            palette="viridis",
            alpha=0.85,
            ax=ax
        )

        # Rotate X-axis labels
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)

        # Show labels on bars
        if show_labels:
            for container in ax.containers:
                ax.bar_label(container, fmt="%.2f", fontsize=8, padding=3)

    # Enable grid if required
    if enable_grid:
        ax.grid(True, linestyle="-", alpha=0.5)

    # Set default title if none is given
    if not custom_title:
        custom_title = f"{x_col} and {y_col}"

    # Set Labels & Titles
    ax.set_title(custom_title, fontsize=9, fontweight="bold")
    ax.set_xlabel(x_col, fontsize=8, fontweight="bold")
    ax.set_ylabel(y_col, fontsize=8, fontweight="bold")

    plt.tight_layout()

    # Clear previous chart before embedding the new one
    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()

    if chart_type == "Heatmap":
        # Extract categorical columns
        categorical_cols = df_result.select_dtypes(include=['object']).columns.tolist()

        # Ensure at least two categorical columns
        group_by_cols = [x_col] + [col for col in categorical_cols if col != x_col]
        
        if len(group_by_cols) < 2:
            messagebox.showerror("Error", "⚠️ Need at least two categorical columns for a Heatmap!")
            return

        y_col = group_by_cols[1]  # Set Y-axis to the second categorical column
        values_col = y_axis_var.get()  # Selected numerical column

        # Aggregate data for the heatmap
        df_heatmap = df_result.groupby([x_col, y_col], as_index=False)[values_col].sum()

        # Pivot data to heatmap format
        df_pivot = df_heatmap.pivot(index=y_col, columns=x_col, values=values_col).fillna(0)

        if df_pivot.empty:
            messagebox.showerror("Error", "⚠️ No valid data for Heatmap!")
            return

        # Create Figure & Axes
        fig, ax = plt.subplots(figsize=(7, 4), dpi=120)  # Higher DPI for clarity

        # Generate Heatmap with Seaborn
        sns.heatmap(
            df_pivot, 
            cmap="viridis", 
            annot=True,  # Display values inside cells
            fmt=".1f",   # Format to 1 decimal place
            linewidths=0.5, 
            linecolor="gray",
            cbar_kws={'shrink': 0.8},  # Shrink color bar for better layout
            ax=ax
        )

        # Customize labels
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=9)

        # Set title dynamically
        if not custom_title:
            custom_title = f"Heatmap: {x_col} vs {y_col}"

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
