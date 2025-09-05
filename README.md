# ShuffleRooster - Student Grouper

A simple solution for randomly shuffling students into groups, available as both a desktop application and web application.

## Web Application

A modern, responsive web application built with HTML5, CSS3 and Vanilla JavaScript.

**Live**: [shufflerooster.vercel.app](https://shufflerooster.vercel.app/)

### Web App Features:
- **Clean, Dark Theme Interface**: Professional design with intuitive navigation
- **File Upload**: Supports CSV and Excel files (XLSX, XLS)
- **Real-time Preview**: Interactive table display of student data
- **Responsive Design**: Works seamlessly on desktop, tablet and mobile devices
- **Group Management**: Customizable group sizes with intelligent distribution
- **Multiple Export Options**: Download results as CSV, XLSX or XLS formats
- **No Server Requirements**: Fully client-side processing using SheetJS library

### Web Technology Stack:
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **File Processing**: SheetJS library for Excel/CSV parsing
- **Styling**: Custom CSS with Flexbox/Grid layout
- **Icons**: Font Awesome for UI icons
- **Hosting**: Vercel platform

## Desktop Application

A feature-rich desktop application built with Python and CustomTkinter.

### Desktop App Features:
- **Modern GUI**: Dark theme interface with professional styling
- **Extended File Support**: CSV, Excel (XLSX, XLS) import capabilities
- **Advanced Export Options**: Save groups as CSV, Excel (XLSX/XLS) or PDF
- **Native Experience**: Desktop-optimized interface with file dialogs
- **Group Balancing**: Intelligent algorithm that ensures balanced group sizes
- **Table Preview**: Interactive treeview for data visualization

### Desktop Technology Stack:
- **GUI Framework**: CustomTkinter for modern UI components
- **Data Processing**: Pandas for data manipulation
- **PDF Export**: ReportLab for PDF generation
- **Excel Support**: Openpyxl for Excel file handling

## Installation Options

### Web Application:
Simply visit [shufflerooster.vercel.app](https://shufflerooster.vercel.app/) in any modern browser - no installation required.

### Desktop Application:
1. Ensure you have Python 3.8+ installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```


## Usage

1. **Import Student List**: Select a file containing student data (CSV or Excel format).
2. **Set Group Size**: Specify how many students should be in each group.
3. **Toggle Shuffle**: Turn shuffle mode **on** or **off** to control whether students are grouped randomly.
4. **Create Groups**: Click to generate balanced groups based on your settings.
5. **Export Results**: Save the grouped data in your preferred format (e.g., CSV, Excel).

## Project Structure

```
shufflerooster/
├── app/
│   ├── main.py              # Main application entry point
│   └── requirements.txt     # Python dependencies
│
└── web/
    ├── index.html           # Main HTML file
    ├── styles.css           # Styling and responsive design
    └── script.js            # Application logic
```

## Development History

- **Web Application**: Developed as a lightweight, accessible solution using vanilla web technologies
- **Desktop Application**: Created to provide extended functionality and native system integration
- **Cross-Platform Compatibility**: Both versions maintain consistent functionality across platforms

## License

This project is designed for educational and institutional use. The web version is freely accessible, while the desktop application requires local installation.

## Support

For issues or feature requests, please contact me through [Github](https://github.com/sanodmendis) or [Personal Website](https://sanodmendis.pages.dev/).

Email: sanodmendis@outlook.com