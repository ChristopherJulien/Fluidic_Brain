import pandas as pd

# Your cdict containing pressure values
cdict = {
    "25kPa": 0.018,
    "7kPa": 0.057,
    "2kPa": 0.2,
}


data1 = {
    's': [1, 2, 3, 4, 5],
    '25kPa': [0.1, 0.2, 0.3, 0.4, 0.5],
    '2kPa': [0.01, 0.02, 0.03, 0.04, 0.05],
    '7kPa': [0.07, 0.14, 0.21, 0.28, 0.35],
    'V_source': [1.0, 1.0,1.0, 1.0, 1.0]
}
df1 = pd.DataFrame(data1)
data2 = {
    's': [1, 2, 3, 4, 5],
    '25kPa': [0.1, 0.2, 0.3, 0.4, 0.5],
    '2kPa': [0.01, 0.02, 0.03, 0.04, 0.05],
    '7kPa': [0.07, 0.14, 0.21, 0.28, 0.35],
    'V_source': [1.0, 2.5,3.0, 1.0, 1.0]
}
df2 = pd.DataFrame(data2)


# Applying the equation to modify the "25kPa" column
df1["25kPa"] = (df1["25kPa"] / df1["V_source"] - 0.5) / cdict["25kPa"] * 10
df2["25kPa"] = (df2["25kPa"] / df2["V_source"] - 0.5) / cdict["25kPa"] * 10

print(df1)
print(df2)


