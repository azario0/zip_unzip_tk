# Zip Unzip TK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, user-friendly graphical application for zipping and unzipping files and folders, built with Python's native Tkinter library.

This tool provides a clean, tabbed interface for both compressing files into a `.zip` archive and extracting contents from an existing `.zip` archive.


## Features

-   **Clean Tabbed Interface**: Easily switch between "Compress (Zip)" and "Extract (Unzip)" modes.
-   **Compress Multiple Items**: Add multiple files and entire folders to be compressed into a single `.zip` archive.
-   **File Management**: A listbox allows you to easily manage the files and folders you want to zip (add, remove selected, clear all).
-   **Extract Archives**: Select a `.zip` file and a destination folder to extract its contents.
-   **Smart Unzipping**: Automatically renames files during extraction to prevent overwriting existing files in the destination folder (e.g., `file.txt` becomes `file (1).txt`).
-   **Responsive GUI**: Uses Python's `threading` module to perform zipping and unzipping operations in the background, preventing the interface from freezing on large files.
-   **Cross-Platform**: Built entirely with standard Python libraries (`tkinter`, `zipfile`), ensuring it runs on Windows, macOS, and Linux without any external dependencies.

## Requirements

-   Python 3.x

That's it! No external libraries are needed.

## How to Run

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/azario0/zip_unzip_tk.git
    ```

2.  **Navigate to the project directory:**
    ```sh
    cd zip_unzip_tk
    ```

3.  **Run the application:**
    ```sh
    python zipper_app.py
    ```
    *(Assuming the main script is named `zipper_app.py`)*

### To Compress Files:

1.  Open the **Compress (Zip)** tab.
2.  Click "Add File(s)" or "Add Folder" to add items to the list.
3.  Use "Remove Selected" or "Clear All" to manage the list if needed.
4.  Click the **ZIP FILES** button.
5.  Choose a name and location to save your new `.zip` file.

### To Extract an Archive:

1.  Open the **Extract (Unzip)** tab.
2.  Click "Browse..." to select the `.zip` file you want to extract.
3.  Click "Browse..." to choose the destination folder where the files will be saved.
4.  Click the **UNZIP FILE** button.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## Tutorial

https://softwarejournal.blog/blog/building-zip-unzip-gui-tool-python-tkinter/

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
