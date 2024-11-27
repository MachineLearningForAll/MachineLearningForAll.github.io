import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib as mpl

# Set global font size
mpl.rcParams['font.size'] = 17  # Set to desired size (e.g., 14)
mpl.rcParams['axes.titlesize'] = 30  # Title font size
mpl.rcParams['axes.labelsize'] = 17  # Axis label font size
mpl.rcParams['legend.fontsize'] = 17  # Legend font size
mpl.rcParams['xtick.labelsize'] = 16  # X-axis tick label size
mpl.rcParams['ytick.labelsize'] = 16  # Y-axis tick label size

# Load the data from the CSV file
file_path = "KustaviIsokari.csv"  # Replace with the actual file path
data = pd.read_csv(file_path)

# Extract relevant columns
data = data[["Maximum temperature [°C]", "Minimum temperature [°C]"]]

# Randomly select a specified number of data points
num_data_points = 15  # Specify the number of data points to select
data = data.sample(n=num_data_points, random_state=42)

# Split data into predictors and target
X = data[["Minimum temperature [°C]"]]  # Predictor
y = data["Maximum temperature [°C]"]    # Target

# Augment the training set
augmented_data = data.copy()
augmented_data["Minimum temperature [°C]"] = data["Minimum temperature [°C]"] + 0
augmented_data["Maximum temperature [°C]"] = data["Maximum temperature [°C]"] + 0

augmented_data_minus = data.copy()
augmented_data_minus["Minimum temperature [°C]"] = data["Minimum temperature [°C]"] - 0
augmented_data_minus["Maximum temperature [°C]"] = data["Maximum temperature [°C]"] - 0

# Combine original and augmented data
data_augmented = pd.concat([data, augmented_data, augmented_data_minus], ignore_index=True)

# Split augmented data into predictors and target
X_augmented = data_augmented[["Minimum temperature [°C]"]]
y_augmented = data_augmented["Maximum temperature [°C]"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_augmented, y_augmented, test_size=0.2, random_state=42)

# Train a Decision Tree Regressor
dt_model = DecisionTreeRegressor(random_state=42, max_depth=3)
dt_model.fit(X_train, y_train)

# Train a Polynomial Regression model
poly_degree = 7  # Specify the degree of the polynomial
poly_features = PolynomialFeatures(degree=poly_degree)
X_train_poly = poly_features.fit_transform(X_train)
X_test_poly = poly_features.transform(X_test)

poly_model = LinearRegression()
poly_model.fit(X_train_poly, y_train)

# Generate a range of values for the predictor with the same column name as training data
min_temp_range = pd.DataFrame(
    np.linspace(X["Minimum temperature [°C]"].min(), X["Minimum temperature [°C]"].max(), 500),
    columns=["Minimum temperature [°C]"]
)

# Predict maximum temperatures for the range using both models
predicted_max_temp_dt = dt_model.predict(min_temp_range)
min_temp_range_poly = poly_features.transform(min_temp_range)
predicted_max_temp_poly = poly_model.predict(min_temp_range_poly)


# Generate scatter plot with original and augmented data
plt.figure(figsize=(10, 6))

# Plot the original data points
plt.scatter(
    X, y, color='blue', label="Original Data", marker='o'
)

# Plot the augmented data points with +1 shifts
plt.scatter(
    augmented_data["Minimum temperature [°C]"],
    augmented_data["Maximum temperature [°C]"],
    color='orange', label="Augmented Data (+1 Shift)", marker='^'
)

# Plot the augmented data points with -1 shifts
plt.scatter(
    augmented_data_minus["Minimum temperature [°C]"],
    augmented_data_minus["Maximum temperature [°C]"],
    color='green', label="Augmented Data (-1 Shift)", marker='v'
)

# Plot the prediction lines
plt.plot(min_temp_range, predicted_max_temp_dt, color='red', label="Decision Tree Prediction", linewidth=2)
plt.plot(min_temp_range, predicted_max_temp_poly, color='purple', label=f"Polynomial Regression (Degree {poly_degree})", linewidth=2)

# Add axis labels, title, and legend
plt.xlabel("Minimum Temperature [°C]", fontsize=14)
plt.ylabel("Maximum Temperature [°C]", fontsize=14)
plt.title("Decision Tree and Polynomial Regression Predictions with Augmented Data", fontsize=16)
plt.legend(fontsize=12)
plt.show()

plt.savefig("decision_tree_vs_polynomial_regression.png", dpi=300, bbox_inches='tight')
