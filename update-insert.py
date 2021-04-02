
########################################################################################################################
############################## Indexing My Documents ###################################################################
########################################################################################################################

author = "Alice"

def remove_single_letter_items(inlinks):
    for link in inlinks:
        if len(link) == 1:
            inlinks.remove(link)
    return inlinks


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
    print("\tIndexing....", doc['_id'])
    doc_id = doc['_id']
    res = find_document(doc_id)

    if len(doc['outlinks']) == 0:
        print(doc_id, "has no outlinks.")
        file = open("pages-without-outlinks.txt", "a")
        line = doc_id + "\n"
        file.write(line)

    if len(res["hits"]["hits"]) > 1:
        print("\tDuplicate documents found for ID:", doc_id)

    # If the document is in the index already, update it
    # Keep ID, text, title. Append my inlinks and outlinks & name.
    elif len(res["hits"]["hits"]) == 1:
        doc_found = res["hits"]["hits"][0]
        cur_inlinks = doc_found['_source']['inlinks']
        cur_outlinks = doc_found['_source']['outlinks']
        # print("\tIt has the inlinks:", cur_inlinks)
        # print("\tIt has the outlinks:", cur_outlinks)

        # Merge inlinks
        try:
            inlinks = list(cur_inlinks)
            inlinks = remove_single_letter_items(inlinks)
            inlinks.extend(x for x in doc['inlinks'] if x not in inlinks)

        # If there are no existing inlinks, inlinks are what I have
        except (AttributeError, TypeError):
            inlinks = doc['inlinks']

        try:
            outlinks = list(cur_outlinks)
            outlinks = remove_single_letter_items(outlinks)
            outlinks.extend(x for x in doc['outlinks'] if x not in outlinks)

        # If there are no existing outlinks, outlinks are what I have
        except (AttributeError, TypeError):
            outlinks = doc['outlinks']

        if not doc_found['_source']['author'] == 'Alice':
            author = doc_found['_source']['author'] + ", " + author

        source_to_update = {"doc": {
            'inlinks': list(inlinks),
            'outlinks': list(outlinks),
            'author': author,
            }
        }

        res = es.update(index=es_index, id=doc_id, body=source_to_update)
        es.indices.refresh(index=es_index)
        print("Updated!", res)

    # Otherwise, insert it
    else:
        doc = {
            "text": doc['text'],
            "title": doc['title'],
            "inlinks": doc['inlinks'],
            "outlinks": doc['outlinks'],
            "author": doc['author'],
        }
        res = es.index(index=es_index, body=doc, id=doc_id)
        print("\tIndexed for the first time!", res)


def find_document(doc_id):

    # es.indices.refresh(index=es_index)
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


def es_testing():
    query_text = "red and black pens available to them to draw the trees."
    body = {
        "from": 0,
        "size": 1,
        "query": {
            "match": {
                "text": str(query_text)
            }
        }
    }
    res = es.search(index=es_index, body=body)
    for doc in res["hits"]["hits"]:
        print(doc)


# Performs an API request to extract all doc IDs into local memory.
def get_all_doc_ids_via_api_call():
    print("Getting all document IDs in the database.")

    body = {
        "size": 1000,
        "query": {
            "match_all": {}
        }
    }

    # Make a search request to scroll documents.
    resp = es.search(index=es_index, body=body, scroll="2s")

    # Keep track of old scroll ID
    old_scroll_id = resp['_scroll_id']

    # scroll Elasticsearch docs with scroll() method
    count = 0
    while len(resp['hits']['hits']):

        # Before scroll, process current batch of hits
        count += len(resp['hits']['hits'])

        # Get the next batch
        resp = es.scroll(scroll_id=old_scroll_id, scroll='2s')
        old_scroll_id = resp['_scroll_id']

    print("\tTotal found: ", count)
