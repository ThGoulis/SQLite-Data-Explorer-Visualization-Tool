# SQLite-Data-Explorer-Visualization-Tool
A GUI-based tool for exploring SQLite databases, executing SQL queries, and visualizing query results with interactive charts. This application provides an intuitive user interface built with **Tkinter** and **ttkbootstrap** for a seamless database interaction experience.

## Features

- **Database Management:** Load and inspect SQLite databases effortlessly.

- **Query Execution:** Execute SQL queries with a structured result display.

- **Data Visualization:** Generate bar and heatmaps.

- **Export Capabilities:** Save query results as CSV, JSON, Excel, and export charts as PNG, PDF, or SVG.

- **Modern UI**: Leverages ttkbootstrap for a sleek and interactive design.

## Dataset

This project utilizes an airline dataset, which can be accessed here: [Airlines Dataset on Kaggle](https://www.kaggle.com/datasets/saadharoon27/airlines-dataset)

Users can **load any SQLite dataset** they want. The application is not restricted to a single dataset and allows for **dynamic database loading**. Additionally, the application includes a **preloaded query specifically designed for the Airlines Dataset on Kaggle** to help users get started quickly.

### How to Use the Dataset:

1. Download the SQLite file from Kaggle.

2. Load it into the application using the **Load Database** button.

3. Execute SQL queries and visualize data with interactive charts.

## Installation

Prerequisites

Ensure you have Python 3.7+ installed. Install the required dependencies using:

`pip install -r requirements.txt`

## Usage

### Run the Application

`python main.py`

### Steps to Use the Application
1. **Load a Database:** Click `Load Database` and select an SQLite file.
   - After the database is loaded, double-click a table to open a pop-up window previewing the columns of the table.
2. **Execute Queries:** Enter an SQL query and click `Execute Query`.
   
3. **Visualize Data:** Select columns for X/Y axes and generate charts.
   - ⚠️ _If you load incorrect data in the chart, you must rerun the query to refresh the results_
4. **Export Data:** Save query results or charts in various formats.

## Workflow

1. Load a Database: Click Load Database and select an SQLite file.

2. Execute Queries: Enter an SQL query and click Execute Query to view results.

3. Visualize Data: Choose X/Y axes and generate various chart types.

4. Export Data: Save query results or charts in multiple formats.

## File Structure
```
📦 project_root
├── db_connection.py       # Handles SQLite database connection
├── gui.py                 # Main GUI setup
├── gui_charts.py          # Chart generation logic
├── gui_query_execution.py # SQL query execution
├── gui_export.py          # Exporting query results
├── gui_database.py        # Database loading & table inspection
├── main.py                # Entry point of the application
├── utils.py               # Utility functions
├── requirements.txt       # Requirement libraries
└── README.md              # Project documentation
```

## License

This project is licensed under the GNU Affero General Public License v3.0.

## Contribution

Feel free to fork this repository and submit pull requests for improvements.
