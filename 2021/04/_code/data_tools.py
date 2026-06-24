import numpy as np
import pandas as pd

def create_sample_data(rows=100):
    np.random.seed(42)
    return pd.DataFrame({
        'id': range(rows),
        'category': np.random.choice(['A', 'B', 'C'], rows),
        'value': np.random.randn(rows) * 100,
        'quantity': np.random.randint(1, 100, rows)
    })

def numpy_operations():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = np.array([[7, 8, 9], [10, 11, 12]])

    c = a + b
    d = np.dot(a, b.T)
    e = a * 2

    print("NumPy addition shape:", c.shape)
    print("NumPy dot product shape:", d.shape)
    print("NumPy broadcast shape:", e.shape)

    return c, d, e

def pandas_operations():
    df = create_sample_data()

    filtered = df[df['value'] > 0]
    aggregated = df.groupby('category').agg({
        'value': 'mean',
        'quantity': 'sum'
    })

    transformed = df.assign(
        total=df['value'] * df['quantity'],
        normalized=(df['value'] - df['value'].mean()) / df['value'].std()
    )

    print("Filtered shape:", filtered.shape)
    print("Aggregated result:", aggregated.to_dict())
    print("Transformed columns:", transformed.columns.tolist())

    return transformed

def grouped_aggregation():
    df = create_sample_data()

    result = df.groupby('category').agg(
        count=('id', 'count'),
        mean_value=('value', 'mean'),
        sum_quantity=('quantity', 'sum'),
        std_value=('value', 'std')
    ).reset_index()

    print("Grouped aggregation result:")
    print(result)

    return result

def process_data_pipeline(df):
    df = df.copy()

    df = df[df['quantity'] > 0]

    df['unit_price'] = df['value'] / df['quantity']

    df['revenue'] = df['unit_price'] * df['quantity']

    result = df.groupby('category').agg({
        'revenue': 'sum',
        'quantity': 'mean',
        'unit_price': 'mean'
    }).round(2)

    return result

def demo():
    print("=== NumPy Operations ===")
    numpy_operations()

    print("\n=== Pandas Operations ===")
    pandas_operations()

    print("\n=== Grouped Aggregation ===")
    grouped_aggregation()

    print("\n=== Data Pipeline ===")
    df = create_sample_data(50)
    result = process_data_pipeline(df)
    print("Pipeline result:")
    print(result)

    print("\nDemo OK")

if __name__ == "__main__":
    demo()