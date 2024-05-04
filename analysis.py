import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = 'C:\\Users\\haoha\\OneDrive\\Desktop\\personal\\Projects\\Personal\\WIP\\omg-snowflakes--main\\snowflake_data.csv'

df['X Position'] = pd.to_numeric(df['X Position'], errors='coerce')
df['Y Position'] = pd.to_numeric(df['Y Position'], errors='coerce')


df.dropna(inplace=True)

print(df.info())

print(df.describe())

print(df[['X Position', 'Y Position']].corr())

plt.figure(figsize=(10, 6))
sns.histplot(df['Y Position'], bins=30, kde=True)
plt.title('Distribution of Y Positions of Snowflakes')
plt.xlabel('Y Position')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='X Position', y='Y Position', data=df)
plt.title('X Position vs Y Position')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()

state_counts = df['State'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=state_counts.index, y=state_counts.values)
plt.title('Distribution of Snowflake States')
plt.xlabel('State')
plt.ylabel('Count')
plt.show()