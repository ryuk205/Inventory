import pandas as pd
import json

df = pd.read_excel('d:/t/Automate/Book1.xlsx')
data = {
    'columns': df.columns.tolist(),
    'first_row': df.head(1).astype(str).to_dict(orient='records')[0]
}
with open('d:/t/Automate/book1_info.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
