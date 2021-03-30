

''' Expecting input in format:
    doc = {
        "_id": 'TestingID.com',
        "text": 'TestingText',
        "title": 'TestingTitle',
        "inlinks": ['in.com/E', 'in.com/D'],
        "outlinks": ['out.com/E', 'out.com/D'],
        "author": "Alice",
    }
'''
def index_document(doc):
    author = "Alice"
    doc_id = doc['_id']
    res = find_document(doc_id)

    # If the document is in the index already, update it
    # Keep ID, text, title. Append my inlinks and outlinks & name.
    if len(res["hits"]["hits"]) == 1:

        doc_found = res["hits"]["hits"][0]
        cur_inlinks = doc_found['_source']['inlinks']
        cur_outlinks = doc_found['_source']['inlinks']

        # Merge inlinks
        try:
            inlinks = list(cur_inlinks)
            inlinks.extend(x for x in doc['inlinks'] if x not in inlinks)

        # If there are no existing inlinks, inlinks are what I have
        except (AttributeError, TypeError):
            inlinks = doc['inlinks']

        try:
            outlinks = list(cur_outlinks)
            outlinks.extend(x for x in doc['outlinks'] if x not in outlinks)

        # If there are no existing outlinks, outlinks are what I have
        except (AttributeError, TypeError):
            outlinks = doc['outlinks']

        author = doc_found['_source']['author'] + ", " + author
        source_to_update = {"doc": {
            'inlinks': inlinks,
            'outlinks': outlinks,
            'author': author,
            }
        }

        es.update(index=es_index, id=doc_id, body=source_to_update)
        es.indices.refresh(index=es_index)
        find_document(doc_id)


    # Otherwise, insert it
    else:

        doc = {
            "text": doc['text'],
            "title": doc['title'],
            "inlinks": doc['inlinks'],
            "outlinks": doc['outlinks'],
            "author": doc['author'],
        }

        es.index(index=es_index, body=doc, id=doc_id)


def find_document(doc_id):
    body = {
        "from": 0,
        "size": 1,
        "query": {
            "terms": {
                "_id": [doc_id]
            }
        }
    }

    res = es.search(index=es_index, body=body)
    return res

