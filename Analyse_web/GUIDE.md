# 🎯 Universal Data Analyzer - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install & Run

**Windows Users:**
```bash
# Double-click start.bat
```

**Mac/Linux Users:**
```bash
# In terminal, run:
./start.sh
```

**Manual Start:**
```bash
pip install -r requirements.txt
python app.py
# Then open index.html in your browser
```

---

## 📊 Workflow Overview

### 1️⃣ Upload Your Data
- **Drag & drop** or **click to upload** any dataset
- Supported formats: `.csv`, `.xlsx`, `.xls`, `.json`
- Maximum size: 100MB
- The system automatically detects delimiters and encodings

**What happens:** The system loads your data and shows you a preview with:
- Number of rows and columns
- Data types for each column
- Missing values count
- First 5 rows preview

---

### 2️⃣ Clean Your Data

**Missing Values Options:**
- `Keep as is` - No changes
- `Drop rows` - Remove rows with any missing values
- `Fill with mean` - Replace with column average (numeric only)
- `Fill with median` - Replace with middle value (numeric only)
- `Fill with mode` - Replace with most common value (all types)

**Outlier Handling:**
- `Keep all` - No changes
- `Remove outliers` - Use IQR method (Q1 - 1.5×IQR to Q3 + 1.5×IQR)

**Other Options:**
- ✅ Remove duplicate rows

**Pro Tip:** Start conservative (e.g., "Keep as is") and only apply aggressive cleaning if needed.

---

### 3️⃣ Select Variables

**Dependent Variable:**
- This is your **target** or **outcome** variable
- What you're trying to predict or understand
- Example: "Sales", "Price", "Pass/Fail"

**Independent Variables:**
- These are your **predictors** or **features**
- What might influence your dependent variable
- Select multiple variables to see relationships
- Example: "Age", "Income", "Location"

---

### 4️⃣ View Results

The analyzer provides comprehensive insights:

#### 📈 Descriptive Statistics
For your dependent variable:
- Mean (average)
- Median (middle value)
- Standard Deviation (spread)
- Min/Max values
- 25th and 75th percentiles

#### 🔬 Statistical Tests

**Automatic test selection based on variable types:**

| Dependent Type | Independent Type | Test Applied |
|---------------|-----------------|--------------|
| Numeric | Numeric | Pearson Correlation |
| Numeric | 2 Categories | Independent T-Test |
| Numeric | 3+ Categories | One-Way ANOVA |

**Interpreting P-Values:**
- p < 0.05 ✅ = Statistically significant relationship
- p ≥ 0.05 ❌ = No significant relationship

#### 📊 Visualizations

You'll automatically get:
1. **Distribution plot** - Shows how your dependent variable is distributed
2. **Relationship plots** - Scatter plots or box plots for each independent variable
3. **Correlation heatmap** - Visual matrix of all numeric variable relationships

---

## 💡 Use Case Examples

### Example 1: Predicting House Prices
```
Dependent Variable: Price
Independent Variables: Bedrooms, Bathrooms, Square_Footage, Location
```
**Expected Output:**
- Correlation between price and square footage
- ANOVA comparing prices across locations
- Scatter plots showing relationships

### Example 2: Student Performance Analysis
```
Dependent Variable: Final_Grade
Independent Variables: Study_Hours, Attendance, Previous_GPA
```
**Expected Output:**
- Correlation between study hours and grades
- Descriptive stats for grade distribution
- Scatter plots for each predictor

### Example 3: Customer Churn Prediction
```
Dependent Variable: Churned (Yes/No)
Independent Variables: Months_Subscribed, Monthly_Charges, Contract_Type
```
**Expected Output:**
- T-tests comparing churned vs retained customers
- Box plots showing charge differences
- Distribution of subscription lengths

---

## 🎓 Statistical Concepts Explained

### Correlation Coefficient (r)
- Range: -1 to +1
- **r = +1**: Perfect positive relationship
- **r = 0**: No relationship
- **r = -1**: Perfect negative relationship
- |r| > 0.7 = Strong correlation
- |r| = 0.3-0.7 = Moderate correlation
- |r| < 0.3 = Weak correlation

### T-Test
Compares means of two groups
- **Use when:** Comparing numeric variable across 2 categories
- **Example:** Average salary of Male vs Female employees

### ANOVA (Analysis of Variance)
Compares means across multiple groups
- **Use when:** Comparing numeric variable across 3+ categories
- **Example:** Average test scores across different teaching methods

### Outliers (IQR Method)
- Q1 = 25th percentile
- Q3 = 75th percentile
- IQR = Q3 - Q1
- Outliers: Values < Q1 - 1.5×IQR or > Q3 + 1.5×IQR

---

## 🔧 Troubleshooting

### "Failed to upload file"
- ✅ Check file format (CSV, Excel, JSON)
- ✅ Check file size (< 100MB)
- ✅ Ensure file is not corrupted
- ✅ Try different encoding if CSV (save as UTF-8)

### "No significant results"
- ✅ Try more independent variables
- ✅ Check if variables are actually related
- ✅ Ensure sufficient sample size (n > 30 recommended)
- ✅ Remove excessive outliers that might mask relationships

### Backend not starting
- ✅ Check Python version: `python --version` (need 3.8+)
- ✅ Install dependencies: `pip install -r requirements.txt`
- ✅ Check if port 5000 is available
- ✅ Look for error messages in terminal

### Visualizations not showing
- ✅ Ensure Flask server is running
- ✅ Check browser console for errors (F12)
- ✅ Try refreshing the page
- ✅ Check if matplotlib/seaborn installed correctly

---

## 📚 Advanced Tips

### 1. Data Preparation
Before uploading:
- Remove unnecessary columns
- Ensure consistent date formats
- Check for obviously wrong values
- Standardize categorical values (e.g., "Yes/yes/YES" → "Yes")

### 2. Choosing Variables
- Start with domain knowledge - what *should* be related?
- Don't include redundant variables (e.g., both "age" and "birth_year")
- Be careful with time-based variables
- Consider creating derived variables (e.g., BMI from height/weight)

### 3. Interpreting Results
- Correlation ≠ Causation
- Check for confounding variables
- Consider sample size and representativeness
- Look for patterns across multiple tests
- Visualizations often reveal more than statistics

### 4. Next Steps After Analysis
- Export cleaned data for further processing
- Use insights to build predictive models
- Share visualizations in reports
- Iterate with different variable combinations

---

## 🎨 Feature Highlights

✨ **Automatic Format Detection** - Works with any delimiter, encoding
🧹 **Smart Cleaning** - Multiple strategies for missing values and outliers
📊 **Publication-Ready Plots** - Professional visualizations
🚀 **Fast Processing** - Pandas-powered backend
💾 **Export Everything** - Download cleaned data anytime
🎯 **Intuitive Interface** - Beautiful, modern design
📱 **Responsive** - Works on desktop, tablet, and mobile

---

## 📞 Need Help?

- 📖 Check README.md for technical details
- 🐛 Report bugs via GitHub issues
- 💡 Request features via GitHub discussions
- 📧 Contact support for urgent issues

---

**Happy Analyzing! 📊✨**
