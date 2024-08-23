import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define the file path
file_path = 'C:/Users/FIZAAN/Desktop/New folder/Practice/Task_3/crypto_dataset.csv'  # Update this path as needed

# Check if the file exists
if os.path.exists(file_path):
    # Load the Cryptocurrency dataset
    df = pd.read_csv(file_path)
    
    # Display the first few rows of the dataset
    print("First few rows of the dataset:")
    print(df.head())

    # Display summary statistics
    print("\nSummary statistics:")
    print(df.describe(include='all'))

    # Display the dataset info
    print("\nDataset information:")
    print(df.info())

    # Filter data for Bitcoin (or any specific cryptocurrency)
    bitcoin_df = df[df['symbol'] == 'BTC']

    # Create a time series plot for Bitcoin price
    plt.figure(figsize=(12, 6))
    plt.plot(pd.to_datetime(bitcoin_df['date']), bitcoin_df['price'], label='Bitcoin Price', color='orange')
    plt.title('Bitcoin Price Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Create a plot for Bitcoin volume and market cap
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot volume
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Volume', color='tab:blue')
    ax1.plot(pd.to_datetime(bitcoin_df['date']), bitcoin_df['volume'], color='tab:blue', label='Volume')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a second y-axis to plot market cap
    ax2 = ax1.twinx()
    ax2.set_ylabel('Market Cap', color='tab:red')
    ax2.plot(pd.to_datetime(bitcoin_df['date']), bitcoin_df['market_cap'], color='tab:red', label='Market Cap')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title('Bitcoin Volume and Market Cap Over Time')
    fig.tight_layout()
    plt.show()

    # Select numerical columns for correlation matrix
    numerical_cols = df[['price', 'market_cap', 'volume']].dropna()
    correlation_matrix = numerical_cols.corr()

    # Create a heatmap for correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap of Cryptocurrency Features')
    plt.show()

else:
    print(f"File not found at {file_path}")
