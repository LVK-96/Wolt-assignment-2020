def match_name(query, name):
    return query in name.lower()


def match_description(query, description):
    return query in description.lower()


def match_tags(query, tags):
    tags_lower = [tag.lower() for tag in tags]
    return query in tags_lower


def match_query(query, restaurant):
    query = query.lower()
    return(match_name(query, restaurant['name'])
           or match_description(query, restaurant['description'])
           or match_tags(query, restaurant['tags']))
