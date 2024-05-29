import pandas as pd
import os
import json

def load_contents(filepath):
    abs_path = os.path.abspath(filepath)
    print(f"Cargando contenido desde {abs_path}")
    return pd.read_csv(abs_path)

def load_tags_schema(filepath):
    abs_path = os.path.abspath(filepath)
    print(f"Cargando esquema de etiquetas desde {abs_path}")
    with open(abs_path, 'r') as file:
        tags = json.load(file)
        
        # Procesar etiquetas con valores anidados
        processed_tags = []
        for tag in tags:
            if isinstance(tag.get('values'), dict):
                for key, value in tag['values'].items():
                    nested_tag = tag.copy()
                    nested_tag['name'] = f"{tag['name']} ({key})"
                    nested_tag['values'] = value['items']
                    nested_tag['aggregation_level'] = value['aggregation_level']
                    processed_tags.append(nested_tag)
            else:
                processed_tags.append(tag)
        
        return processed_tags
