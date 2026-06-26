import pandas as pd

# TODO Naming: 'f' is not descriptive
# TODO Inputs: this should be a command-line argument, not hardcoded
f = 'eva_data.json'
# TODO Naming: 'o' is not descriptive
# TODO Inputs: this should be a command-line argument, not hardcoded
o = 'eva_data.csv'

print("--START--")

print(f'Reading JSON data file {f}')
# TODO Naming: 'd' is not descriptive
d = pd.read_json(f, convert_dates=['date'], encoding='ascii')
d['eva'] = d['eva'].astype(float)
d.dropna(axis=0, subset=['duration', 'date'], inplace=True)

print(f'Saving data to CSV file {o}')
d.to_csv(o, index=False, encoding='utf-8')

# TODO Descriptive comment: add an explanation of that the 3 lines below do
subset = d.loc[:, ['crew', 'duration']]
subset.crew = subset.crew.str.split(';').apply(lambda x: [i for i in x if i.strip()])
subset = subset.explode('crew')

# TODO DRY: this duration-string-to-hours conversion is repeated again below
# for the main dataframe - it should be a single reusable function
hrs = []
for val in subset['duration']:
    h, m = val.split(":")
    hrs.append(int(h) + int(m) / 60)
subset['duration_hours'] = hrs
subset = subset.drop('duration', axis=1)
subset = subset.groupby('crew').sum()

dur_out = 'duration_by_astronaut.csv'
print(f'Saving to CSV file {dur_out}')
subset.to_csv(dur_out, index=False, encoding='utf-8')

d.sort_values('date', inplace=True)

# TODO DRY: duplicate of the hours-conversion logic above - violates DRY
hrs2 = []
for val in d['duration']:
    h, m = val.split(":")
    hrs2.append(int(h) + int(m) / 60)
d['duration_hours'] = hrs2

d['cumulative_time'] = d['duration_hours'].cumsum()

#TODO: import statements should be grouped at the top
import matplotlib.pyplot as plt

# TODO Inputs: graph save location should be a flexible command-line argument
g = 'cumulative_eva_graph.png'
print(f'Plotting cumulative spacewalk duration and saving to {g}')
plt.plot(d['date'], d['cumulative_time'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(g)
plt.show()

#TODO: import statements should be grouped at the top
import re

# TODO: this function is never used anywhere - candidate for removal,
# or for wiring into the analysis (left as unused/dead code on purpose)
def calculate_crew_size(crew):
    if crew.split() == []:
        return None
    else:
        return len(re.split(r';', crew)) - 1

print("--END--")
