import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("medical_examination.csv") # Load the datasetd_csv("medical_examination.csv")

df["overweight"] = (df["weight"] / ((df["height"] / 100) ** 2) > 25).astype(int) # Add 'overweight' column
df["cholesterol"] = (df["cholesterol"] > 1).astype(int) # Normalize 'cholesterol' column
df["gluc"] = (df["gluc"] > 1).astype(int) # Normalize 'gluc' column

print(df[["weight", "height", "overweight"]].head(5)) # Print first 5 rows of specific columns
print(df[["cholesterol", "gluc"]].head(5)) # Print first 5 rows of specific columns

#categorical plot
def draw_cat_plot(): # Define function to draw categorical plot
    df_cat = pd.melt( # Melt the  DataFrame
        df,
        id_vars=["cardio"], # fixed columns (cardio = 0 or 1) to know if the person has cardiovascular disease
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"] # columns to unpivot (caterogical features)
    )
    df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="total") # Group by cardio, variable, and value; count occurrences in 'total'
    fig = sns.catplot( # Create categorical plot
        x="variable", # X-axis = variable name
        y="total", # Y-axis = total count = number of occurrences
        hue="value", # Different colors for different values (0 or 1)
        col="cardio", # Separate plots for cardio = 0 and cardio = 1
        data=df_cat,  # DataFrame to plot
        kind="bar" # Type of plot = bar plot
    ).fig # Get the figure object

    fig.savefig("catplot.png") # Save the figure
    return fig # Return the figure 



#heatmap
def draw_heat_map(): # Define function to draw heat map
    #clean the data 
    #keep only the rows with ap_lo <= ap_hi
    df_heat = df.copy()
    df_heat = df_heat[df_heat["ap_lo"] <= df_heat["ap_hi"]]
    #keep only the rows with height and weight within the 2.5th and 97.5th percentiles
    df_heat = df_heat[
        (df_heat["height"] >= df_heat["height"].quantile(0.025)) &
        (df_heat["height"] <= df_heat["height"].quantile(0.975)) &
        (df_heat["weight"] >= df_heat["weight"].quantile(0.025)) &
        (df_heat["weight"] <= df_heat["weight"].quantile(0.975))
    ]
    corr = df_heat.corr() # Calculate the correlation matrix
    mask = np.triu(np.ones_like(corr, dtype=bool)) # Generate a mask for the upper triangle
    fig, ax = plt.subplots(figsize=(10, 8)) # Set up the matplotlib figure
    sns.heatmap( # Draw the heatmap
        corr,
        mask=mask, # Apply the mask
        annot=True, # Annotate the cells with correlation values
        fmt=".1f", # Format for the annotations
        center=0, # Center the colormap at 0
        square=True, # Make the cells square
        linewidths=.5, # Width of the lines that will divide each cell
        cbar_kws={"shrink": .5}, # Color bar settings
    )
    fig.savefig("heatmap.png") # Save the figure
    return fig # Return the figure

draw_cat_plot() # Call the function to draw categorical plot
draw_heat_map() # Call the function to draw heat map

