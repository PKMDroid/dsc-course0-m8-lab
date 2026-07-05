import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# cleaning workflow

df = pd.read_csv('data/AviationData.csv', encoding='cp1252', low_memory=False)
df = df.copy()
df['Event.Date'] = pd.to_datetime(df['Event.Date'], errors='coerce')
df = df[(df['Event.Date'].dt.year >= 1983) & (df['Aircraft.Category'].fillna('').str.lower() == 'airplane') & (df['Amateur.Built'].fillna('').str.lower() != 'yes')].copy()
df = df.dropna(subset=['Make', 'Model']).reset_index(drop=True)

injury_cols = ['Total.Fatal.Injuries', 'Total.Serious.Injuries', 'Total.Minor.Injuries', 'Total.Uninjured']
for col in injury_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
df['Total.Passengers.Est'] = df[injury_cols].sum(axis=1)
df['Serious.Fatal.Fraction'] = np.where(df['Total.Passengers.Est'] > 0, (df['Total.Fatal.Injuries'] + df['Total.Serious.Injuries']) / df['Total.Passengers.Est'], np.nan)
df['Fatal.Fraction'] = np.where(df['Total.Passengers.Est'] > 0, df['Total.Fatal.Injuries'] / df['Total.Passengers.Est'], np.nan)

df['Aircraft.Damage.Clean'] = df['Aircraft.damage'].fillna('Unknown').astype(str).str.strip().str.title()
df['Destroyed.Flag'] = df['Aircraft.Damage.Clean'].eq('Destroyed').astype(int)

make_map = {'CESSNA': 'Cessna', 'PIPER': 'Piper', 'BOEING': 'Boeing', 'BEECH': 'Beech', 'BELL': 'Bell', 'MCDONNELL DOUGLAS': 'McDonnell Douglas', 'DOUGLAS': 'Douglas', 'SIKORSKY': 'Sikorsky', 'AIRBUS': 'Airbus', 'DE HAVILLAND': 'De Havilland'}
df['Make.Clean'] = df['Make'].fillna('Unknown').astype(str).str.strip()
df['Make.Clean'] = df['Make.Clean'].str.upper().replace(make_map)
df['Make.Clean'] = df['Make.Clean'].replace({'UNKNOWN': 'Unknown'})
make_counts = df['Make.Clean'].value_counts()
df = df[df['Make.Clean'].isin(make_counts[make_counts >= 50].index)].copy()

df['Model.Clean'] = df['Model'].fillna('Unknown').astype(str).str.strip()
df['Plane.Type'] = df['Make.Clean'] + ' ' + df['Model.Clean']

for col in ['Engine.Type', 'Weather.Condition', 'Purpose.of.flight', 'Broad.phase.of.flight']:
    df[col] = df[col].fillna('Unknown').astype(str).str.strip()
    df[col] = df[col].replace({'': 'Unknown', 'UNK': 'Unknown', 'Unk': 'Unknown'})

df['Number.of.Engines.Clean'] = pd.to_numeric(df['Number.of.Engines'], errors='coerce')
df['Number.of.Engines.Clean'] = df['Number.of.Engines.Clean'].fillna(df['Number.of.Engines.Clean'].median())

keep_cols = [c for c in df.columns if df[c].isna().mean() <= 0.5]
df = df[keep_cols]
df.to_csv('data/aviation_accidents_cleaned.csv', index=False)

# analysis workflow
analysis = pd.read_csv('data/aviation_accidents_cleaned.csv', low_memory=False)
analysis['Passenger.Capacity'] = pd.to_numeric(analysis.get('Total.Passengers.Est', pd.Series(np.nan)), errors='coerce')
analysis['Passenger.Capacity'] = analysis['Passenger.Capacity'].fillna(analysis['Passenger.Capacity'].median())
analysis['Small.Aircraft'] = analysis['Passenger.Capacity'] <= 20

small = analysis[analysis['Small.Aircraft']].copy()
large = analysis[~analysis['Small.Aircraft']].copy()

small_make_stats = small.groupby('Make.Clean').apply(lambda g: pd.Series({'mean_injury_rate': g['Serious.Fatal.Fraction'].mean(), 'count': g.shape[0]})).reset_index().sort_values('mean_injury_rate')
large_make_stats = large.groupby('Make.Clean').apply(lambda g: pd.Series({'mean_injury_rate': g['Serious.Fatal.Fraction'].mean(), 'count': g.shape[0]})).reset_index().sort_values('mean_injury_rate')

print('cleaned_shape', df.shape)
print('saved_file', os.path.exists('data/aviation_accidents_cleaned.csv'))
print('analysis_shape', analysis.shape)
print('small_large_counts', small.shape[0], large.shape[0])
print('small_top_make', small_make_stats.head(3).to_string(index=False))
print('large_top_make', large_make_stats.head(3).to_string(index=False))
