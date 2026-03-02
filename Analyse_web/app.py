from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import os
import json
import base64
from io import BytesIO
from pathlib import Path
import traceback

warnings.filterwarnings("ignore")
plt.switch_backend("Agg")  # Use non-interactive backend

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("outputs")
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB max file size


class DataAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.df_original = None
        self.numeric_cols = []
        self.categorical_cols = []
        self.dependent_var = None
        self.independent_vars = []

    def load_data(self):
        """Load data with automatic delimiter detection"""
        try:
            if self.filepath.endswith((".xlsx", ".xls")):
                self.df = pd.read_excel(self.filepath)
            elif self.filepath.endswith(".json"):
                self.df = pd.read_json(self.filepath)
            else:
                # Try different delimiters
                delimiters = [",", ";", "\t", "|"]
                for delim in delimiters:
                    try:
                        test_df = pd.read_csv(
                            self.filepath, delimiter=delim, nrows=5, encoding="utf-8"
                        )
                        if len(test_df.columns) > 1:
                            self.df = pd.read_csv(
                                self.filepath,
                                delimiter=delim,
                                encoding="utf-8",
                                low_memory=False,
                            )
                            break
                    except:
                        continue

                # Try different encodings
                if self.df is None:
                    for encoding in ["latin-1", "iso-8859-1", "cp1252"]:
                        for delim in delimiters:
                            try:
                                test_df = pd.read_csv(
                                    self.filepath,
                                    delimiter=delim,
                                    nrows=5,
                                    encoding=encoding,
                                )
                                if len(test_df.columns) > 1:
                                    self.df = pd.read_csv(
                                        self.filepath,
                                        delimiter=delim,
                                        encoding=encoding,
                                        low_memory=False,
                                    )
                                    break
                            except:
                                continue
                        if self.df is not None:
                            break

            if self.df is None:
                raise Exception("Could not load file with any known format")

            self.df_original = self.df.copy()
            return True
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

    def get_preview(self):
        """Get data preview information"""
        return {
            "shape": self.df.shape,
            "columns": self.df.columns.tolist(),
            # 'head': self.df.head(10).to_dict('records'),
            "head": (self.df.head(10).replace({np.nan: None}).to_dict("records")),
            "dtypes": self.df.dtypes.astype(str).to_dict(),
            "missing": self.df.isnull().sum().to_dict(),
            "numeric_cols": self.df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_cols": self.df.select_dtypes(
                exclude=[np.number]
            ).columns.tolist(),
        }

    def clean_data(self, options):
        """Clean data based on user options"""
        # Handle missing values
        if options.get("handle_missing") == "drop":
            self.df = self.df.dropna()
        elif options.get("handle_missing") == "mean":
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(
                self.df[numeric_cols].mean()
            )
        elif options.get("handle_missing") == "median":
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(
                self.df[numeric_cols].median()
            )
        elif options.get("handle_missing") == "mode":
            for col in self.df.columns:
                if self.df[col].isnull().sum() > 0:
                    self.df[col].fillna(
                        self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 0,
                        inplace=True,
                    )

        # Handle duplicates
        if options.get("remove_duplicates"):
            self.df = self.df.drop_duplicates()

        # Handle outliers
        if options.get("handle_outliers") == "remove":
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                self.df = self.df[(self.df[col] >= lower) & (self.df[col] <= upper)]

        return {
            "new_shape": self.df.shape,
            "rows_removed": self.df_original.shape[0] - self.df.shape[0],
        }

    def get_statistics(self, dependent_var, independent_vars):
        """Calculate statistics"""
        self.dependent_var = dependent_var
        self.independent_vars = independent_vars

        stats_result = {"descriptive": {}, "correlations": {}, "tests": {}}

        # Descriptive statistics
        if dependent_var in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[dependent_var]):
                stats_result["descriptive"][dependent_var] = {
                    "mean": float(self.df[dependent_var].mean()),
                    "median": float(self.df[dependent_var].median()),
                    "std": float(self.df[dependent_var].std()),
                    "min": float(self.df[dependent_var].min()),
                    "max": float(self.df[dependent_var].max()),
                    "q25": float(self.df[dependent_var].quantile(0.25)),
                    "q75": float(self.df[dependent_var].quantile(0.75)),
                }

        # Correlations for numeric variables
        numeric_vars = [
            v
            for v in [dependent_var] + independent_vars
            if pd.api.types.is_numeric_dtype(self.df[v])
        ]
        if len(numeric_vars) > 1:
            corr_matrix = self.df[numeric_vars].corr()
            stats_result["correlations"] = corr_matrix.to_dict()

        # Statistical tests
        for ind_var in independent_vars:
            if ind_var not in self.df.columns:
                continue

            if pd.api.types.is_numeric_dtype(
                self.df[dependent_var]
            ) and pd.api.types.is_numeric_dtype(self.df[ind_var]):
                # Correlation test
                corr, p_val = stats.pearsonr(
                    self.df[dependent_var].dropna(), self.df[ind_var].dropna()
                )
                stats_result["tests"][f"{dependent_var}_vs_{ind_var}"] = {
                    "test": "Pearson Correlation",
                    "statistic": float(corr),
                    "p_value": float(p_val),
                }
            elif pd.api.types.is_numeric_dtype(
                self.df[dependent_var]
            ) and not pd.api.types.is_numeric_dtype(self.df[ind_var]):
                # ANOVA or t-test
                groups = [
                    group[dependent_var].dropna()
                    for name, group in self.df.groupby(ind_var)
                ]
                if len(groups) == 2:
                    stat, p_val = stats.ttest_ind(groups[0], groups[1])
                    stats_result["tests"][f"{dependent_var}_vs_{ind_var}"] = {
                        "test": "Independent T-Test",
                        "statistic": float(stat),
                        "p_value": float(p_val),
                    }
                elif len(groups) > 2:
                    stat, p_val = stats.f_oneway(*groups)
                    stats_result["tests"][f"{dependent_var}_vs_{ind_var}"] = {
                        "test": "One-Way ANOVA",
                        "statistic": float(stat),
                        "p_value": float(p_val),
                    }

        return stats_result

    def create_visualizations(self, dependent_var, independent_vars):
        """Create visualizations and return as base64 images"""
        visualizations = []

        # Set style
        sns.set_style("whitegrid")

        # Distribution of dependent variable
        if pd.api.types.is_numeric_dtype(self.df[dependent_var]):
            fig, ax = plt.subplots(figsize=(10, 6))
            self.df[dependent_var].hist(bins=30, ax=ax, edgecolor="black")
            ax.set_title(f"Distribution of {dependent_var}")
            ax.set_xlabel(dependent_var)
            ax.set_ylabel("Frequency")
            visualizations.append(
                {
                    "title": f"Distribution of {dependent_var}",
                    "image": self._fig_to_base64(fig),
                }
            )
            plt.close(fig)

        # Relationships with independent variables
        for ind_var in independent_vars[:4]:  # Limit to 4 to avoid too many plots
            if ind_var not in self.df.columns:
                continue

            fig, ax = plt.subplots(figsize=(10, 6))

            if pd.api.types.is_numeric_dtype(
                self.df[dependent_var]
            ) and pd.api.types.is_numeric_dtype(self.df[ind_var]):
                # Scatter plot
                ax.scatter(self.df[ind_var], self.df[dependent_var], alpha=0.5)
                ax.set_xlabel(ind_var)
                ax.set_ylabel(dependent_var)
                ax.set_title(f"{dependent_var} vs {ind_var}")
                visualizations.append(
                    {
                        "title": f"{dependent_var} vs {ind_var}",
                        "image": self._fig_to_base64(fig),
                    }
                )
            elif pd.api.types.is_numeric_dtype(self.df[dependent_var]):
                # Box plot
                self.df.boxplot(column=dependent_var, by=ind_var, ax=ax)
                ax.set_title(f"{dependent_var} by {ind_var}")
                visualizations.append(
                    {
                        "title": f"{dependent_var} by {ind_var}",
                        "image": self._fig_to_base64(fig),
                    }
                )

            plt.close(fig)

        # Correlation heatmap
        numeric_vars = [
            v
            for v in [dependent_var] + independent_vars
            if pd.api.types.is_numeric_dtype(self.df[v])
        ]
        if len(numeric_vars) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            corr_matrix = self.df[numeric_vars].corr()
            sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
            ax.set_title("Correlation Matrix")
            visualizations.append(
                {"title": "Correlation Matrix", "image": self._fig_to_base64(fig)}
            )
            plt.close(fig)

        return visualizations

    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        buffer = BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight", dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        return f"data:image/png;base64,{image_base64}"


# Global analyzer instance
current_analyzer = None


@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Handle file upload"""
    global current_analyzer

    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Save file
        filepath = app.config["UPLOAD_FOLDER"] / file.filename
        file.save(str(filepath))

        # Initialize analyzer
        current_analyzer = DataAnalyzer(str(filepath))
        current_analyzer.load_data()

        # Get preview
        preview = current_analyzer.get_preview()

        return jsonify({"success": True, "filename": file.filename, "preview": preview})

    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


@app.route("/api/clean", methods=["POST"])
def clean_data():
    """Clean the data"""
    global current_analyzer

    try:
        if current_analyzer is None:
            return jsonify({"error": "No data loaded"}), 400

        options = request.json
        result = current_analyzer.clean_data(options)
        preview = current_analyzer.get_preview()

        return jsonify({"success": True, "result": result, "preview": preview})

    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Perform statistical analysis"""
    global current_analyzer

    try:
        if current_analyzer is None:
            return jsonify({"error": "No data loaded"}), 400

        data = request.json
        dependent_var = data.get("dependent_var")
        independent_vars = data.get("independent_vars", [])

        if not dependent_var:
            return jsonify({"error": "Dependent variable not specified"}), 400

        # Get statistics
        statistics = current_analyzer.get_statistics(dependent_var, independent_vars)

        # Create visualizations
        visualizations = current_analyzer.create_visualizations(
            dependent_var, independent_vars
        )

        return jsonify(
            {
                "success": True,
                "statistics": statistics,
                "visualizations": visualizations,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


@app.route("/api/download", methods=["POST"])
def download_results():
    """Download cleaned data"""
    global current_analyzer

    try:
        if current_analyzer is None:
            return jsonify({"error": "No data loaded"}), 400

        output_path = app.config["OUTPUT_FOLDER"] / "cleaned_data.csv"
        current_analyzer.df.to_csv(output_path, index=False, encoding="utf-8")

        return send_file(
            str(output_path), as_attachment=True, download_name="cleaned_data.csv"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
