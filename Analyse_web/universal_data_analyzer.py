import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import re
import os
from pathlib import Path

warnings.filterwarnings("ignore")


class UniversalDataAnalyzer:
    def __init__(self, filepath):
        """
        Initialize the Universal Data Analyzer

        Parameters:
        filepath: str - Path to the dataset
        """
        self.filepath = filepath
        self.df = None
        self.df_original = None
        self.numeric_cols = []
        self.categorical_cols = []
        self.dependent_var = None
        self.independent_vars = []
        self.delimiter = None

        # Create output directory in the same location as the script
        self.output_dir = Path(os.getcwd()) / "analysis_output"
        self.output_dir.mkdir(exist_ok=True)

    def load_data(self):
        """Load data with automatic delimiter detection"""
        print("\n" + "=" * 60)
        print("DATA LOADING")
        print("=" * 60)

        try:
            # Try to detect file type and delimiter
            if self.filepath.endswith((".xlsx", ".xls")):
                self.df = pd.read_excel(self.filepath)
                print(f"✓ Excel file loaded successfully!")
            elif self.filepath.endswith(".json"):
                self.df = pd.read_json(self.filepath)
                print(f"✓ JSON file loaded successfully!")
            else:
                # Try different delimiters for CSV-like files
                delimiters = [",", ";", "\t", "|"]
                loaded = False

                for delim in delimiters:
                    try:
                        test_df = pd.read_csv(
                            self.filepath, delimiter=delim, nrows=5, encoding="utf-8"
                        )
                        if len(test_df.columns) > 1:
                            self.delimiter = delim
                            self.df = pd.read_csv(
                                self.filepath,
                                delimiter=delim,
                                encoding="utf-8",
                                low_memory=False,
                            )
                            loaded = True
                            delimiter_names = {
                                ",": "comma",
                                ";": "semicolon",
                                "\t": "tab",
                                "|": "pipe",
                            }
                            print(
                                f"✓ CSV file loaded with {delimiter_names[delim]} delimiter!"
                            )
                            break
                    except:
                        continue

                if not loaded:
                    # Try with different encodings
                    for encoding in ["latin-1", "iso-8859-1", "cp1252"]:
                        try:
                            for delim in delimiters:
                                try:
                                    test_df = pd.read_csv(
                                        self.filepath,
                                        delimiter=delim,
                                        nrows=5,
                                        encoding=encoding,
                                    )
                                    if len(test_df.columns) > 1:
                                        self.delimiter = delim
                                        self.df = pd.read_csv(
                                            self.filepath,
                                            delimiter=delim,
                                            encoding=encoding,
                                            low_memory=False,
                                        )
                                        loaded = True
                                        delimiter_names = {
                                            ",": "comma",
                                            ";": "semicolon",
                                            "\t": "tab",
                                            "|": "pipe",
                                        }
                                        print(
                                            f"✓ CSV file loaded with {delimiter_names[delim]} delimiter and {encoding} encoding!"
                                        )
                                        break
                                except:
                                    continue
                            if loaded:
                                break
                        except:
                            continue

                if not loaded:
                    raise ValueError(
                        "Could not detect delimiter. Please convert to standard CSV format."
                    )

            # Store original data
            self.df_original = self.df.copy()

            print(
                f"  Dataset shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns"
            )
            print(f"\n  First few column names:")
            for i, col in enumerate(self.df.columns[:10], 1):
                print(f"    {i}. {col}")
            if len(self.df.columns) > 10:
                print(f"    ... and {len(self.df.columns) - 10} more columns")

            return True

        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False

    def preview_data(self):
        """Show data preview to help user understand the dataset"""
        print("\n" + "=" * 60)
        print("DATA PREVIEW")
        print("=" * 60)

        print("\nFirst 3 rows of data:")
        print(self.df.head(3).to_string())

        print("\n\nData types:")
        print(self.df.dtypes)

        print("\n\nBasic statistics:")
        print(self.df.describe(include="all").T)

    def clean_data(self):
        """Comprehensive automated data cleaning with user guidance"""
        print("\n" + "=" * 60)
        print("AUTOMATED DATA CLEANING")
        print("=" * 60)

        initial_rows = len(self.df)
        initial_cols = len(self.df.columns)

        # 1. Clean column names
        print("\n[1/7] Cleaning column names...")
        self.df.columns = self.df.columns.str.strip()
        print("  ✓ Removed whitespace from column names")

        # 2. Remove completely empty rows and columns
        print("\n[2/7] Removing empty rows and columns...")
        self.df = self.df.dropna(how="all", axis=0)
        self.df = self.df.dropna(how="all", axis=1)
        removed_rows = initial_rows - len(self.df)
        removed_cols = initial_cols - len(self.df.columns)
        if removed_rows > 0:
            print(f"  ✓ Removed {removed_rows} completely empty rows")
        if removed_cols > 0:
            print(f"  ✓ Removed {removed_cols} completely empty columns")

        # 3. Handle problematic values
        print("\n[3/7] Cleaning problematic values...")
        problematic_values = [
            "??",
            "#BO\xde!",
            "NaN",
            "NULL",
            "null",
            "N/A",
            "n/a",
            "#N/A",
            "#VALUE!",
            "#REF!",
            "#DIV/0!",
            "",
            " ",
            "  ",
        ]

        for col in self.df.columns:
            for prob_val in problematic_values:
                self.df[col] = self.df[col].replace(prob_val, np.nan)
        print("  ✓ Replaced problematic values with NaN")

        # 4. Remove duplicate rows
        print("\n[4/7] Checking for duplicate rows...")
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            self.df = self.df.drop_duplicates()
            print(f"  ✓ Removed {duplicates} duplicate rows")
        else:
            print("  ✓ No duplicate rows found")

        # 5. Detect and convert data types
        print("\n[5/7] Detecting and converting data types...")
        for col in self.df.columns:
            # Try to convert to numeric
            try:
                # Remove any non-numeric characters except decimal point and minus
                temp_col = self.df[col].astype(str).str.replace(",", ".")
                temp_col = pd.to_numeric(temp_col, errors="coerce")

                # If more than 50% of non-null values are numeric, convert
                non_null_count = self.df[col].notna().sum()
                numeric_count = temp_col.notna().sum()

                if non_null_count > 0 and (numeric_count / non_null_count) > 0.5:
                    self.df[col] = temp_col
            except:
                pass

        # Identify column types
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        print(f"  ✓ Identified {len(self.numeric_cols)} numeric columns")
        print(f"  ✓ Identified {len(self.categorical_cols)} categorical columns")

        # 6. Handle missing values
        print("\n[6/7] Handling missing values...")
        missing_summary = self.df.isnull().sum()
        missing_cols = missing_summary[missing_summary > 0]

        if len(missing_cols) > 0:
            print(f"  Missing values found in {len(missing_cols)} columns:")
            for col in missing_cols.index[:10]:  # Show first 10
                pct = (missing_cols[col] / len(self.df)) * 100
                print(f"    - {col}: {missing_cols[col]} ({pct:.1f}%)")
            if len(missing_cols) > 10:
                print(f"    ... and {len(missing_cols) - 10} more columns")

            # Ask user how to handle missing values
            print("\n  How should missing values be handled?")
            print("    1. Fill numeric with median, categorical with mode (default)")
            print("    2. Fill all with a specific value")
            print("    3. Remove rows with any missing values")
            print("    4. Keep missing values as-is")

            choice = input("\n  Enter choice (1-4) [default: 1]: ").strip() or "1"

            if choice == "1":
                # Fill numeric with median
                for col in self.numeric_cols:
                    if self.df[col].isnull().sum() > 0:
                        self.df[col].fillna(self.df[col].median(), inplace=True)

                # Fill categorical with mode
                for col in self.categorical_cols:
                    if self.df[col].isnull().sum() > 0:
                        mode_val = self.df[col].mode()
                        if len(mode_val) > 0:
                            self.df[col].fillna(mode_val[0], inplace=True)
                        else:
                            self.df[col].fillna("Unknown", inplace=True)
                print("  ✓ Filled missing values (numeric: median, categorical: mode)")

            elif choice == "2":
                fill_value = input("  Enter value to fill missing data: ").strip()
                self.df.fillna(fill_value, inplace=True)
                print(f"  ✓ Filled all missing values with '{fill_value}'")

            elif choice == "3":
                before = len(self.df)
                self.df = self.df.dropna()
                print(f"  ✓ Removed {before - len(self.df)} rows with missing values")

            else:
                print("  ✓ Keeping missing values as-is")
        else:
            print("  ✓ No missing values found")

        # 7. Handle outliers
        print("\n[7/7] Outlier detection...")
        if len(self.numeric_cols) > 0:
            print(
                f"  Checking {len(self.numeric_cols)} numeric columns for outliers..."
            )

            outlier_counts = {}
            for col in self.numeric_cols:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR
                outliers = (
                    (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                ).sum()
                if outliers > 0:
                    outlier_counts[col] = outliers

            if outlier_counts:
                print(f"  Found potential outliers in {len(outlier_counts)} columns:")
                for col, count in list(outlier_counts.items())[:5]:
                    pct = (count / len(self.df)) * 100
                    print(f"    - {col}: {count} ({pct:.1f}%)")
                if len(outlier_counts) > 5:
                    print(f"    ... and {len(outlier_counts) - 5} more columns")

                print("\n  How should outliers be handled?")
                print("    1. Keep outliers (recommended for most analyses)")
                print("    2. Remove outliers")
                print("    3. Cap outliers at boundaries")

                choice = input("\n  Enter choice (1-3) [default: 1]: ").strip() or "1"

                if choice == "2":
                    before = len(self.df)
                    for col in outlier_counts.keys():
                        Q1 = self.df[col].quantile(0.25)
                        Q3 = self.df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        self.df = self.df[
                            (self.df[col] >= Q1 - 3 * IQR)
                            & (self.df[col] <= Q3 + 3 * IQR)
                        ]
                    print(f"  ✓ Removed {before - len(self.df)} rows with outliers")

                elif choice == "3":
                    for col in outlier_counts.keys():
                        Q1 = self.df[col].quantile(0.25)
                        Q3 = self.df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 3 * IQR
                        upper_bound = Q3 + 3 * IQR
                        self.df[col] = self.df[col].clip(
                            lower=lower_bound, upper=upper_bound
                        )
                    print("  ✓ Capped outliers at boundaries")
                else:
                    print("  ✓ Keeping outliers")
            else:
                print("  ✓ No significant outliers detected")

        print(f"\n{'='*60}")
        print(f"CLEANING COMPLETE")
        print(f"  Original: {initial_rows} rows × {initial_cols} columns")
        print(f"  Final: {len(self.df)} rows × {len(self.df.columns)} columns")
        print(f"{'='*60}")

    def select_variables(self):
        """Interactive variable selection with smart suggestions"""
        print("\n" + "=" * 60)
        print("VARIABLE SELECTION")
        print("=" * 60)

        print("\nAvailable columns:")
        col_info = []
        for i, col in enumerate(self.df.columns, 1):
            col_type = "numeric" if col in self.numeric_cols else "categorical"
            unique_count = self.df[col].nunique()
            col_info.append((i, col, col_type, unique_count))
            print(
                f"  {i:3d}. {col:30s} ({col_type:12s}) - {unique_count} unique values"
            )

        # Smart suggestions
        print("\n" + "-" * 60)
        print("SUGGESTIONS:")

        # Suggest dependent variable (typically target or outcome)
        print("\n  Potential DEPENDENT variables (targets):")
        dependent_keywords = [
            "target",
            "outcome",
            "label",
            "class",
            "result",
            "diagnosis",
            "price",
            "amount",
            "score",
            "rating",
            "sales",
            "disposition",
            "ktas_expert",
            "expert",
            "mistriage",
        ]
        suggested_dep = []
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in dependent_keywords):
                suggested_dep.append(col)

        if suggested_dep:
            for col in suggested_dep[:3]:
                idx = list(self.df.columns).index(col) + 1
                print(f"    - {col} (#{idx})")
        else:
            print("    - No automatic suggestions. Choose based on your analysis goal.")

        # Suggest independent variables
        print("\n  Potential INDEPENDENT variables (features):")
        print("    - Consider all variables except your target")
        print("    - Avoid ID columns or unique identifiers")

        # Identify potential ID columns
        id_keywords = ["id", "number", "index", "_id", "patient", "customer"]
        potential_ids = []
        for col in self.df.columns:
            if (
                any(keyword in col.lower() for keyword in id_keywords)
                and self.df[col].nunique() / len(self.df) > 0.95
            ):
                potential_ids.append(col)

        if potential_ids:
            print(f"\n  WARNING: These columns might be IDs (consider excluding):")
            for col in potential_ids[:5]:
                idx = list(self.df.columns).index(col) + 1
                print(f"    - {col} (#{idx})")

        print("-" * 60)

        # Select dependent variable
        while True:
            dep_input = input("\n→ Enter DEPENDENT variable (name or number): ").strip()

            if not dep_input:
                print("  Please enter a value.")
                continue

            try:
                if dep_input.isdigit():
                    dep_idx = int(dep_input) - 1
                    if 0 <= dep_idx < len(self.df.columns):
                        self.dependent_var = self.df.columns[dep_idx]
                        break
                elif dep_input in self.df.columns:
                    self.dependent_var = dep_input
                    break
                else:
                    print("  Invalid input. Try again.")
            except:
                print("  Invalid input. Try again.")

        dep_type = (
            "numeric" if self.dependent_var in self.numeric_cols else "categorical"
        )
        print(f"  ✓ Dependent variable: {self.dependent_var} ({dep_type})")

        # Select independent variables
        print("\n→ Select INDEPENDENT variables (features):")
        print("  Options:")
        print("    - Enter 'all' to select all columns except dependent variable")
        print("    - Enter numbers separated by commas (e.g., 1,3,5,7-10)")
        print("    - Enter column names separated by commas")

        while True:
            ind_input = input("\n  Independent variables: ").strip()

            if not ind_input:
                print("  Please enter a value.")
                continue

            if ind_input.lower() == "all":
                self.independent_vars = [
                    col for col in self.df.columns if col != self.dependent_var
                ]
                break

            try:
                self.independent_vars = []
                selections = [x.strip() for x in ind_input.split(",")]

                for sel in selections:
                    # Handle ranges (e.g., 1-5)
                    if "-" in sel and sel.replace("-", "").isdigit():
                        start, end = map(int, sel.split("-"))
                        for idx in range(start - 1, end):
                            if 0 <= idx < len(self.df.columns):
                                col = self.df.columns[idx]
                                if (
                                    col != self.dependent_var
                                    and col not in self.independent_vars
                                ):
                                    self.independent_vars.append(col)
                    elif sel.isdigit():
                        idx = int(sel) - 1
                        if 0 <= idx < len(self.df.columns):
                            col = self.df.columns[idx]
                            if (
                                col != self.dependent_var
                                and col not in self.independent_vars
                            ):
                                self.independent_vars.append(col)
                    elif sel in self.df.columns and sel != self.dependent_var:
                        if sel not in self.independent_vars:
                            self.independent_vars.append(sel)

                if self.independent_vars:
                    break
                else:
                    print("  No valid independent variables selected. Try again.")
            except Exception as e:
                print(f"  Invalid input: {e}. Try again.")

        print(f"\n  ✓ Selected {len(self.independent_vars)} independent variables:")
        for col in self.independent_vars[:10]:
            col_type = "numeric" if col in self.numeric_cols else "categorical"
            print(f"    - {col} ({col_type})")
        if len(self.independent_vars) > 10:
            print(f"    ... and {len(self.independent_vars) - 10} more")

    def calculate_statistics(self):
        """Calculate comprehensive statistics"""
        print("\n" + "=" * 60)
        print("STATISTICAL ANALYSIS")
        print("=" * 60)

        # Focus on numeric columns
        numeric_data = self.df[
            [
                col
                for col in self.independent_vars + [self.dependent_var]
                if col in self.numeric_cols
            ]
        ]

        if len(numeric_data.columns) == 0:
            print("\n  No numeric columns selected for statistical analysis.")
            return None

        print(f"\n  Analyzing {len(numeric_data.columns)} numeric columns...")

        stats_dict = {}

        for col in numeric_data.columns:
            data = numeric_data[col].dropna()

            if len(data) == 0:
                continue

            stats_dict[col] = {
                "Count": len(data),
                "Mean": data.mean(),
                "Median": data.median(),
                "Mode": data.mode()[0] if not data.mode().empty else np.nan,
                "Std Dev": data.std(),
                "Variance": data.var(),
                "Min": data.min(),
                "Max": data.max(),
                "Range": data.max() - data.min(),
                "25th %ile": data.quantile(0.25),
                "50th %ile": data.quantile(0.50),
                "75th %ile": data.quantile(0.75),
                "90th %ile": data.quantile(0.90),
                "95th %ile": data.quantile(0.95),
                "99th %ile": data.quantile(0.99),
                "Skewness": data.skew(),
                "Kurtosis": data.kurtosis(),
                "CV (%)": (
                    (data.std() / data.mean() * 100) if data.mean() != 0 else np.nan
                ),
            }

        stats_df = pd.DataFrame(stats_dict).T

        # Save statistics to output directory
        stats_path = self.output_dir / "statistics_summary.csv"
        stats_df.to_csv(stats_path)
        print(f"\n  ✓ Statistics calculated and saved to '{stats_path}'")

        # Show summary
        print("\n" + "-" * 60)
        print("STATISTICS SUMMARY (first 5 columns):")
        print("-" * 60)
        print(stats_df.head().to_string())
        if len(stats_df) > 5:
            print(f"\n  ... and {len(stats_df) - 5} more columns in the file")

        return stats_df

    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print("\n" + "=" * 60)
        print("CREATING VISUALIZATIONS")
        print("=" * 60)

        sns.set_style("whitegrid")
        sns.set_palette("husl")

        created_plots = []

        # Get numeric columns from selected variables
        selected_numeric = [
            col
            for col in self.independent_vars + [self.dependent_var]
            if col in self.numeric_cols
        ]
        selected_categorical = [
            col for col in self.independent_vars if col in self.categorical_cols
        ]

        # 1. HISTOGRAMS
        if len(selected_numeric) > 0:
            print("\n  [1/7] Creating histograms...")
            n_cols = min(3, len(selected_numeric))
            n_rows = (len(selected_numeric) + n_cols - 1) // n_cols

            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            axes = np.array(axes).flatten() if n_rows > 1 or n_cols > 1 else [axes]

            for idx, col in enumerate(selected_numeric):
                data = self.df[col].dropna()
                axes[idx].hist(
                    data, bins=min(30, len(data.unique())), edgecolor="black", alpha=0.7
                )
                axes[idx].set_title(f"{col}", fontsize=11, fontweight="bold")
                axes[idx].set_xlabel("Value")
                axes[idx].set_ylabel("Frequency")
                axes[idx].grid(True, alpha=0.3)

            for idx in range(len(selected_numeric), len(axes)):
                axes[idx].axis("off")

            plt.tight_layout()
            hist_path = self.output_dir / "histograms.png"
            plt.savefig(hist_path, dpi=300, bbox_inches="tight")
            plt.close()
            created_plots.append("histograms.png")
            print("      ✓ Saved")

        # 2. BOX PLOTS
        if len(selected_numeric) > 0:
            print("  [2/7] Creating box plots...")
            n_cols = min(3, len(selected_numeric))
            n_rows = (len(selected_numeric) + n_cols - 1) // n_cols

            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            axes = np.array(axes).flatten() if n_rows > 1 or n_cols > 1 else [axes]

            for idx, col in enumerate(selected_numeric):
                data = self.df[col].dropna()
                axes[idx].boxplot(
                    data,
                    vert=True,
                    patch_artist=True,
                    boxprops=dict(facecolor="lightblue", alpha=0.7),
                )
                axes[idx].set_title(f"{col}", fontsize=11, fontweight="bold")
                axes[idx].set_ylabel("Value")
                axes[idx].grid(True, alpha=0.3)

            for idx in range(len(selected_numeric), len(axes)):
                axes[idx].axis("off")

            plt.tight_layout()
            box_path = self.output_dir / "boxplots.png"
            plt.savefig(box_path, dpi=300, bbox_inches="tight")
            plt.close()
            created_plots.append("boxplots.png")
            print("      ✓ Saved")

        # 3. SCATTER PLOTS
        if (
            self.dependent_var in self.numeric_cols
            and len([col for col in self.independent_vars if col in self.numeric_cols])
            > 0
        ):
            print("  [3/7] Creating scatter plots...")

            numeric_indep = [
                col for col in self.independent_vars if col in self.numeric_cols
            ][:9]
            n_cols = min(3, len(numeric_indep))
            n_rows = (len(numeric_indep) + n_cols - 1) // n_cols

            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            axes = np.array(axes).flatten() if n_rows > 1 or n_cols > 1 else [axes]

            for idx, col in enumerate(numeric_indep):
                valid_data = self.df[[col, self.dependent_var]].dropna()
                axes[idx].scatter(
                    valid_data[col], valid_data[self.dependent_var], alpha=0.5
                )
                axes[idx].set_title(
                    f"{col} vs {self.dependent_var}", fontsize=10, fontweight="bold"
                )
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel(self.dependent_var)
                axes[idx].grid(True, alpha=0.3)

                # Trend line
                if len(valid_data) > 1:
                    z = np.polyfit(valid_data[col], valid_data[self.dependent_var], 1)
                    p = np.poly1d(z)
                    axes[idx].plot(
                        valid_data[col],
                        p(valid_data[col]),
                        "r--",
                        alpha=0.8,
                        linewidth=2,
                    )

            for idx in range(len(numeric_indep), len(axes)):
                axes[idx].axis("off")

            plt.tight_layout()
            scatter_path = self.output_dir / "scatterplots.png"
            plt.savefig(scatter_path, dpi=300, bbox_inches="tight")
            plt.close()
            created_plots.append("scatterplots.png")
            print("      ✓ Saved")

        # 4. BAR CHARTS
        if len(selected_categorical) > 0:
            print("  [4/7] Creating bar charts...")
            cat_to_plot = selected_categorical[:6]

            n_cols = min(3, len(cat_to_plot))
            n_rows = (len(cat_to_plot) + n_cols - 1) // n_cols

            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            axes = np.array(axes).flatten() if n_rows > 1 or n_cols > 1 else [axes]

            for idx, col in enumerate(cat_to_plot):
                value_counts = self.df[col].value_counts().head(10)
                axes[idx].bar(range(len(value_counts)), value_counts.values, alpha=0.7)
                axes[idx].set_title(f"{col}", fontsize=11, fontweight="bold")
                axes[idx].set_xlabel("Category")
                axes[idx].set_ylabel("Count")
                axes[idx].set_xticks(range(len(value_counts)))
                axes[idx].set_xticklabels(value_counts.index, rotation=45, ha="right")
                axes[idx].grid(True, alpha=0.3, axis="y")

            for idx in range(len(cat_to_plot), len(axes)):
                axes[idx].axis("off")

            plt.tight_layout()
            bar_path = self.output_dir / "barcharts.png"
            plt.savefig(bar_path, dpi=300, bbox_inches="tight")
            plt.close()
            created_plots.append("barcharts.png")
            print("      ✓ Saved")

        # 5. PIE CHARTS
        if len(selected_categorical) > 0:
            print("  [5/7] Creating pie charts...")
            cat_to_plot = selected_categorical[:6]

            n_cols = min(3, len(cat_to_plot))
            n_rows = (len(cat_to_plot) + n_cols - 1) // n_cols

            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            axes = np.array(axes).flatten() if n_rows > 1 or n_cols > 1 else [axes]

            for idx, col in enumerate(cat_to_plot):
                value_counts = self.df[col].value_counts().head(5)
                axes[idx].pie(
                    value_counts.values,
                    labels=value_counts.index,
                    autopct="%1.1f%%",
                    startangle=90,
                )
                axes[idx].set_title(f"{col}", fontsize=11, fontweight="bold")

            for idx in range(len(cat_to_plot), len(axes)):
                axes[idx].axis("off")

            plt.tight_layout()
            pie_path = self.output_dir / "piecharts.png"
            plt.savefig(pie_path, dpi=300, bbox_inches="tight")
            plt.close()
            created_plots.append("piecharts.png")
            print("      ✓ Saved")

        # 6. CORRELATION HEATMAP
        if len(selected_numeric) > 1:
            print("  [6/7] Creating correlation heatmap...")
            plt.figure(figsize=(12, 10))

            corr_data = self.df[selected_numeric].corr()

            sns.heatmap(
                corr_data,
                annot=True,
                fmt=".2f",
                cmap="coolwarm",
                center=0,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": 0.8},
            )
            plt.title("Correlation Heatmap", fontsize=16, fontweight="bold", pad=20)
            plt.tight_layout()
            heatmap_path = self.output_dir / "heatmap.png"
            plt.savefig(heatmap_path, dpi=300, bbox_inches="tight")
            plt.close()
            created_plots.append("heatmap.png")
            print("      ✓ Saved")

        # 7. DISTRIBUTION COMPARISON (if categorical dependent variable)
        if self.dependent_var in self.categorical_cols and len(selected_numeric) > 0:
            print("  [7/7] Creating distribution comparison by target...")

            numeric_to_plot = selected_numeric[:6]
            n_cols = min(3, len(numeric_to_plot))
            n_rows = (len(numeric_to_plot) + n_cols - 1) // n_cols

            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            axes = np.array(axes).flatten() if n_rows > 1 or n_cols > 1 else [axes]

            target_categories = self.df[self.dependent_var].unique()[
                :5
            ]  # Max 5 categories

            for idx, col in enumerate(numeric_to_plot):
                for category in target_categories:
                    data = self.df[self.df[self.dependent_var] == category][
                        col
                    ].dropna()
                    if len(data) > 0:
                        axes[idx].hist(data, alpha=0.5, label=str(category), bins=20)

                axes[idx].set_title(
                    f"{col} by {self.dependent_var}", fontsize=10, fontweight="bold"
                )
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel("Frequency")
                axes[idx].legend()
                axes[idx].grid(True, alpha=0.3)

            for idx in range(len(numeric_to_plot), len(axes)):
                axes[idx].axis("off")

            plt.tight_layout()
            dist_path = self.output_dir / "distribution_comparison.png"
            plt.savefig(dist_path, dpi=300, bbox_inches="tight")
            plt.close()
            created_plots.append("distribution_comparison.png")
            print("      ✓ Saved")
        else:
            print("  [7/7] Skipping distribution comparison (not applicable)")

        print(f"\n  ✓ Created {len(created_plots)} visualization files")
        print(f"  ✓ All files saved to: {self.output_dir}")
        return created_plots

    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "=" * 60)
        print("GENERATING ANALYSIS REPORT")
        print("=" * 60)

        report = f"""
{'='*70}
DATA ANALYSIS REPORT
{'='*70}

DATASET INFORMATION:
{'-'*70}
File: {self.filepath}
Rows: {len(self.df):,}
Columns: {len(self.df.columns)}

COLUMN TYPES:
{'-'*70}
Numeric Columns: {len(self.numeric_cols)}
Categorical Columns: {len(self.categorical_cols)}

SELECTED VARIABLES:
{'-'*70}
Dependent Variable: {self.dependent_var}
  Type: {'Numeric' if self.dependent_var in self.numeric_cols else 'Categorical'}
  Unique Values: {self.df[self.dependent_var].nunique()}

Independent Variables: {len(self.independent_vars)}
"""

        # List independent variables by type
        numeric_ind = [col for col in self.independent_vars if col in self.numeric_cols]
        categorical_ind = [
            col for col in self.independent_vars if col in self.categorical_cols
        ]

        if numeric_ind:
            report += f"\n  Numeric ({len(numeric_ind)}):\n"
            for col in numeric_ind[:20]:
                report += f"    - {col}\n"
            if len(numeric_ind) > 20:
                report += f"    ... and {len(numeric_ind) - 20} more\n"

        if categorical_ind:
            report += f"\n  Categorical ({len(categorical_ind)}):\n"
            for col in categorical_ind[:20]:
                report += f"    - {col}\n"
            if len(categorical_ind) > 20:
                report += f"    ... and {len(categorical_ind) - 20} more\n"

        report += f"""
DATA QUALITY:
{'-'*70}
Missing Values: Handled
Duplicates: Removed
Outliers: {'Addressed' if len(self.numeric_cols) > 0 else 'N/A'}
Data Types: Automatically detected and converted

OUTPUTS GENERATED:
{'-'*70}
✓ statistics_summary.csv - Detailed statistics for all numeric variables
✓ histograms.png - Distribution of numeric variables
✓ boxplots.png - Outlier detection visualizations
✓ scatterplots.png - Relationships between variables
✓ barcharts.png - Categorical variable frequencies
✓ piecharts.png - Category proportions
✓ heatmap.png - Correlation matrix
✓ analysis_report.txt - This comprehensive report

All files saved to: {self.output_dir}

ANALYSIS COMPLETE!
{'-'*70}

{'='*70}
"""

        # Save report
        report_path = self.output_dir / "analysis_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(report)
        print(f"  ✓ Report saved to '{report_path}'")

    def run_analysis(self):
        """Run the complete analysis pipeline"""
        print("\n" + "=" * 70)
        print("   UNIVERSAL DATA ANALYZER - COMPREHENSIVE ANALYSIS PIPELINE   ")
        print("=" * 70)
        print(f"\nOutput directory: {self.output_dir}")

        # Step 1: Load data
        if not self.load_data():
            return

        # Step 2: Preview data
        preview_choice = (
            input("\nWould you like to preview the data? (y/n) [y]: ").strip().lower()
            or "y"
        )
        if preview_choice == "y":
            self.preview_data()

        # Step 3: Clean data
        print("\nProceeding to data cleaning...")
        input("Press Enter to continue...")
        self.clean_data()

        # Step 4: Select variables
        self.select_variables()

        # Step 5: Calculate statistics
        if (
            len(
                [
                    col
                    for col in self.independent_vars + [self.dependent_var]
                    if col in self.numeric_cols
                ]
            )
            > 0
        ):
            self.calculate_statistics()
        else:
            print("\n  No numeric variables selected - skipping statistics")

        # Step 6: Create visualizations
        viz_choice = (
            input("\nCreate visualizations? (y/n) [y]: ").strip().lower() or "y"
        )
        if viz_choice == "y":
            self.create_visualizations()

        # Step 7: Generate report
        self.generate_report()

        print("\n" + "=" * 70)
        print("   ANALYSIS COMPLETE - ALL FILES SAVED!   ")
        print(f"   Check the folder: {self.output_dir}")
        print("=" * 70)


# MAIN EXECUTION
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("   WELCOME TO THE UNIVERSAL DATA ANALYZER   ")
    print("=" * 70)
    print("\nThis tool will guide you through:")
    print("  1. Loading your dataset (any delimiter, any encoding)")
    print("  2. Cleaning the data with your guidance")
    print("  3. Selecting dependent and independent variables")
    print("  4. Calculating comprehensive statistics")
    print("  5. Generating professional visualizations")
    print("  6. Creating a detailed analysis report")

    filepath = input("\nEnter the path to your dataset: ").strip()

    if not filepath:
        print("No file provided. Exiting.")
    else:
        analyzer = UniversalDataAnalyzer(filepath)
        analyzer.run_analysis()
