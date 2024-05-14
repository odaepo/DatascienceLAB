import pandas as pd
import numpy as np

PROPERTY_TYPES = ['villa', 'appartamento', 'attico', 'loft', 'mansarda', 'rustico', 'terratetto', 'cascina', 'intera proprietà', 'classe immobile media', 'classe immobile signorile']
OTHER_CHARACTERISTICS = ['arredato', 'balcone', 'impianto tv', 'impianto tv centralizzato', 'esposizione interna', 'esposizione esterna', 'fibra ottica', 'cancello elettrico', 'cantina', 'giardino comune', 'giardino privato', 'impianto allarme', 'portiere', 'piscina', 'terrazza', ]
HEATING = ['autonomo', 'centralizzato']
AIR_CONDITIONING = ['autonomo', 'freddo/caldo', 'predisposizione']

# Load the raw dataset
df=pd.read_csv('Dataset/sale_raw.csv', low_memory=False)

# Drop rows with 'Affitto' and 'Progetto' values
df = df.drop(df[df['contratto'].str.contains('Affitto')].index)
df = df.drop(df[df['tipologia'].str.contains('Progetto')].index)

# Cleaning column 'prezzo'
def price(df):
    df['prezzo'] = df['prezzo'].str.replace('da', '')
    df['prezzo'] = df['prezzo'].str.replace('€', '')
    df['prezzo'] = df['prezzo'].str.replace(',00', '')
    df['prezzo'] = df['prezzo'].str.replace(r'[^0-9]+', '')
    df['prezzo'] = df['prezzo'].str.replace(r'.', '')
    df.loc[df['prezzo'] == '', 'prezzo'] = np.nan
    df['prezzo'] = pd.to_numeric(df['prezzo'], downcast='float', errors='coerce')
    df['prezzo'] = df['prezzo'].astype(float)
    df = df.drop(df[df['prezzo'] < 20000].index)
    df = df.drop(df[df['prezzo'] > 10000000].index)
    return df

# Cleaning column 'stanze'
def rooms(df):
    df['stanze'] = df['stanze'].str.replace('+', '')
    df['stanze'] = df['stanze'].str.replace(r'[^0-9]+', '')
    df['stanze'] = df['stanze'].str.replace(r'.', '')
    df.loc[df['stanze'] == '', 'stanze'] = np.nan
    df['stanze'] = pd.to_numeric(df['stanze'], downcast='float', errors='coerce')
    df['stanze'] = df['stanze'].astype(float)
    return df

# Cleaning column 'superfice'
def surface(df):
    df['superfice'] = df['superfice'].str.replace('m²', '')
    df['superfice'] = df['superfice'].str.replace(r'[^0-9]+', '')
    df['superfice'] = df['superfice'].str.replace(r'.', '')
    df.loc[df['superfice'] == '', 'superfice'] = np.nan
    df['superfice'] = pd.to_numeric(df['superfice'], downcast='float', errors='coerce')
    df['superfice'] = df['superfice'].astype(float)
    df = df.drop(df[df['superfice'] < 20].index)
    df = df.drop(df[df['superfice'] > 2000].index)
    return df

# Cleaning column 'bagni'
def bathrooms(df):
    df['bagni'] = df['bagni'].str.replace('+', '')
    df['bagni'] = df['bagni'].str.replace(r'[^0-9]+', '')
    df['bagni'] = df['bagni'].str.replace(r'.', '')
    df.loc[df['bagni'] == '', 'bagni'] = np.nan
    df['bagni'] = pd.to_numeric(df['bagni'], downcast='float', errors='coerce')
    df['bagni'] = df['bagni'].astype(float)
    df = df.drop(df[df['bagni'] > 5].index)
    return df

# Create column 'ascensore'
def elevator(df):
    df['ascensore'] = df['piano'].str.contains('ascensore')
    df['ascensore'] = df['ascensore'].map({True: 1, False: 0})
    df['ascensore'] = pd.to_numeric(df['ascensore'], downcast='integer', errors='coerce')
    df['ascensore'] = df['ascensore'].fillna(0).astype(int)
    return df

# Create column 'accessibilita'
def accessibility(df):
    df['accessibilita'] = df['piano'].str.contains('accesso disabili')
    df['accessibilita'] = df['accessibilita'].map({True: 1, False: 0})
    df['accessibilita'] = pd.to_numeric(df['accessibilita'], downcast='integer', errors='coerce')
    df['accessibilita'] = df['accessibilita'].fillna(0).astype(int)
    return df

# Cleaning column 'piano'
def floor(df):
    df['piano'] = df['piano'].str.replace('Piano terra', '0')
    df['piano'] = df['piano'].str.replace('piano', '')
    df['piano'] = df['piano'].str.replace('con accesso disabili', '')
    df['piano'] = df['piano'].str.replace('con ascensore', '')
    df['piano'] = df['piano'].str.replace('°', '')
    df['piano'] = df['piano'].str.replace(',', '')
    df['piano'] = df['piano'].str.replace(r'.', '')
    df.loc[df['piano'] == '', 'piano'] = np.nan
    df['piano'] = pd.to_numeric(df['piano'], downcast='integer', errors='coerce')
    df['piano'] = df['piano'].fillna(0).astype(int)
    return df

# Create column 'totale_piani'
def total_floor(df):
    df['totale_piani'] = df['totale_piani'].str.replace('piano', '')
    df['totale_piani'] = df['totale_piani'].str.replace('piani', '')
    df['totale_piani'] = df['totale_piani'].str.replace(r'[^0-9]+', '')
    df['totale_piani'] = pd.to_numeric(df['totale_piani'], downcast='integer', errors='coerce')
    df['totale_piani'] = df['totale_piani'].fillna(0).astype(int)
    return df

# Create column 'ultimo_piano'
def last_floor(df):
    df['ultimo_piano'] = df['piano'] == df['totale_piani']
    df['ultimo_piano'] = df['ultimo_piano'].map({True: 1, False: 0})
    df['ultimo_piano'] = df['ultimo_piano'].fillna(0).astype(int)
    return df

# Create columns for each property type
def property_type(df):
    for property_type in PROPERTY_TYPES:
        df[property_type] = df['tipologia'].apply(lambda x: property_type in x.lower() if x else 0)
        df[property_type] = df[property_type].map({True: 1, False: 0})
        df[property_type] = df[property_type].fillna(0).astype(int)
    return df

# Create column 'vista_mare'
def sea_view(df):
    df['vista_mare'] = df['descrizione'].str.contains('vista mare')
    df['vista_mare'] = df['vista_mare'].map({True: 1, False: 0})
    df['vista_mare'] = df['vista_mare'].fillna(0).astype(int)
    return df

# Create columns for each heating type
def heating(df):
    for characteristic in HEATING:
        df[characteristic] = df['riscaldamento'].astype(str).apply(lambda x: characteristic in x.lower() if x else 0)
        df[characteristic] = df[characteristic].map({True: 1, False: 0})
        df[characteristic] = df[characteristic].fillna(0).astype(int)
    return df

# Create columns for each air conditioning type
def air_conditioning(df):
    for characteristic in AIR_CONDITIONING:
        df[characteristic] = df['climatizzatore'].astype(str).apply(lambda x: characteristic in x.lower() if x else 0)
        df[characteristic] = df[characteristic].map({True: 1, False: 0})
        df[characteristic] = df[characteristic].fillna(0).astype(int)
    return df

# Create columns for each other characteristic
def characteristic(df):
    for characteristic in OTHER_CHARACTERISTICS:
        df[characteristic] = df['altre_caratteristiche'].astype(str).apply(lambda x: characteristic in x.lower() if x else 0)
        df[characteristic] = df[characteristic].map({True: 1, False: 0})
        df[characteristic] = df[characteristic].fillna(0).astype(int)
    return df

# Apply cleaning functions
df = price(df)
df = rooms(df)
df = surface(df)
df = bathrooms(df)
df = elevator(df)
df = accessibility(df)
df = floor(df)
df = total_floor(df)
df = last_floor(df)
df = property_type(df)
df = sea_view(df)
df = heating(df)
#df = air_conditioning(df)
df = characteristic(df)
df.head(3)

# Prepare the clean dataset
final_columns = ['citta', 'provincia', 'regione', 'ripartizione_geografica', 'indirizzo', 'stanze', 'superfice', 'bagni', 'piano', 'totale_piani', 'ultimo_piano', 'ascensore', 'accessibilita', 'vista_mare', 'anno_costruzione', 'classe_energetica']
final_columns.extend(PROPERTY_TYPES)
final_columns.extend(HEATING)
#final_columns.extend(AIR_CONDITIONING)
final_columns.extend(OTHER_CHARACTERISTICS)
final_columns.append('prezzo')
df = df[final_columns]

# Save the clean dataset
df.to_csv('Dataset/sale_clean.csv', index=False)