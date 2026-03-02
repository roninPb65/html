# 📊 Universal Data Analyzer

A modern, beautiful web application for uploading, cleaning, and analyzing datasets with statistical insights and visualizations.

## ✨ Features

- 🚀 **Universal Dataset Support**: Works with CSV, Excel, JSON, and various delimiters
- 🧹 **Smart Data Cleaning**: Handle missing values, duplicates, and outliers
- 📈 **Statistical Analysis**: Descriptive stats, correlation analysis, t-tests, ANOVA
- 📊 **Beautiful Visualizations**: Interactive plots and charts
- 💾 **Export Results**: Download cleaned datasets
- 🎨 **Modern UI**: Cyberpunk-inspired design with smooth animations

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Install Python Dependencies**

```bash
pip install -r requirements.txt
```

2. **Start the Backend Server**

```bash
python app.py
```

The Flask server will start at `http://localhost:5000`

3. **Open the Web Interface**

Simply open `index.html` in your web browser. You can:
- Double-click the file
- Or open it from terminal: `open index.html` (Mac) or `start index.html` (Windows)
- Or serve it with Python: `python -m http.server 8000` and visit `http://localhost:8000`

## 📖 Usage Guide

### Step 1: Upload Dataset

- Click the upload zone or drag and drop your dataset
- Supported formats: CSV, Excel (.xlsx, .xls), JSON
- Maximum file size: 100MB

### Step 2: Clean Data

Configure cleaning options:

**Handle Missing Values:**
- Keep as is
- Drop rows with missing values
- Fill with mean (numeric columns)
- Fill with median (numeric columns)
- Fill with mode (all column types)

**Handle Outliers:**
- Keep all values
- Remove outliers using IQR method

**Other Options:**
- Remove duplicate rows

### Step 3: Select Variables

- Choose your **dependent variable** (target/outcome variable)
- Select one or more **independent variables** (predictors/features)

### Step 4: View Results

The analysis provides:

**Descriptive Statistics:**
- Mean, median, standard deviation
- Min, max, quartiles

**Statistical Tests:**
- Pearson correlation (numeric vs numeric)
- Independent t-test (numeric vs 2 categories)
- One-way ANOVA (numeric vs 3+ categories)

**Visualizations:**
- Distribution plots
- Scatter plots
- Box plots
- Correlation heatmap

## 🔧 Technical Details

### Backend (Flask + Pandas)

The backend is built with Flask and uses pandas for all data processing:

- **Data Loading**: Automatic delimiter detection, encoding handling
- **Data Cleaning**: pandas operations for missing values, duplicates, outliers
- **Statistical Analysis**: scipy.stats for hypothesis testing
- **Visualizations**: matplotlib and seaborn for plotting

### Frontend (React)

The frontend is a single-page React application with:

- Modern cyberpunk-inspired design
- Smooth animations and transitions
- Responsive layout
- Real-time feedback

## 📁 Project Structure

```
universal-data-analyzer/
├── app.py              # Flask backend API
├── index.html          # React frontend (single file)
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── uploads/           # Uploaded files (created automatically)
└── outputs/           # Generated outputs (created automatically)
```

## 🚀 API Endpoints

### POST /api/upload
Upload and preview a dataset

**Request:** multipart/form-data with 'file' field
**Response:**
```json
{
  "success": true,
  "filename": "data.csv",
  "preview": {
    "shape": [1000, 10],
    "columns": [...],
    "head": [...],
    "dtypes": {...},
    "missing": {...}
  }
}
```

### POST /api/clean
Clean the uploaded dataset

**Request:**
```json
{
  "handle_missing": "mean",
  "remove_duplicates": true,
  "handle_outliers": "remove"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "new_shape": [950, 10],
    "rows_removed": 50
  },
  "preview": {...}
}
```

### POST /api/analyze
Perform statistical analysis

**Request:**
```json
{
  "dependent_var": "target_column",
  "independent_vars": ["feature1", "feature2"]
}
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "descriptive": {...},
    "correlations": {...},
    "tests": {...}
  },
  "visualizations": [
    {
      "title": "Distribution of target_column",
      "image": "data:image/png;base64,..."
    }
  ]
}
```

### POST /api/download
Download cleaned dataset

**Response:** CSV file download

## 🎨 Customization

### Modify Color Scheme

Edit the CSS variables in `index.html`:

```css
:root {
    --primary: #0a0e27;
    --accent: #00ff88;
    /* ... other colors */
}
```

### Add New Statistical Tests

Extend the `get_statistics` method in `app.py`:

```python
def get_statistics(self, dependent_var, independent_vars):
    # Add your custom statistical tests here
    pass
```

### Add New Visualizations

Extend the `create_visualizations` method in `app.py`:

```python
def create_visualizations(self, dependent_var, independent_vars):
    # Add your custom plots here
    pass
```

## 🐛 Troubleshooting

### CORS Errors

If you see CORS errors in the browser console:
1. Make sure the Flask server is running
2. Check that CORS is enabled in `app.py`
3. Try using a proper HTTP server instead of opening the HTML file directly

### File Upload Issues

- Check file size (max 100MB)
- Ensure file format is supported (CSV, Excel, JSON)
- Check file encoding (UTF-8 preferred)

### Memory Issues with Large Files

For very large datasets (>50MB):
1. Increase system memory
2. Use data sampling for preview
3. Process data in chunks

## 📝 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Add more statistical tests (chi-square, regression models, etc.)
- Support for more file formats
- Real-time data preview while uploading
- Export visualizations as PDF/PNG
- Add data transformation options
- Implement machine learning models

## 📧 Support

For issues and questions, please create an issue in the repository or contact the maintainers.

---

Made with ❤️ using Python, Flask, pandas, and React
