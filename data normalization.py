import pandas as pd

mapping_df = pd.read_excel('Ingestion Mapping.xlsx', sheet_name='Default Mapping 4 All')

database_df = pd.read_excel('Recon.xlsx')

mapping_df['default value'] = mapping_df['default value'].astype(str).str.lower()

for index, row in database_df.iterrows():
    for mapping_index, mapping_row in mapping_df.iterrows():
        value_from_db = str(row[mapping_row['column name']])

        if value_from_db.lower() in mapping_row['default value']:
            if 'priority' in mapping_row and not pd.isna(mapping_row['priority']):
                highest_priority = mapping_df.loc[mapping_df['column name'] == mapping_row['column name'], 'priority'].min()
                default_value = mapping_df.loc[(mapping_df['column name'] == mapping_row['column name']) & 
                                               (mapping_df['priority'] == highest_priority), 'default value'].iloc[0]
            else:
                default_value = mapping_row['default value']

            database_df.at[index, mapping_row['column name']] = default_value

database_df.to_excel('Normalized_Recon.xlsx', index=False)
