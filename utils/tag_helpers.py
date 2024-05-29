def get_tags_for_level(tags_schema, level):
    return [tag for tag in tags_schema if level in tag['aggregation_level']]
