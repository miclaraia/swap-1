################################################################
#

from swap.db import DB


def _controv_query(size=100):
    return [
        {
            '$group': {
                '_id': '$subject_id',
                'total': {'$sum': 1},
                'real': {'$sum': {'$cond': [{'$eq': ['$annotation', 1]},
                                            1, 0]}},
                'bogus': {'$sum': {'$cond': [{'$eq': ['$annotation', 0]},
                                             1, 0]}}
            }
        },
        {
            '$project': {
                '_id': 1, 'real': 1, 'bogus': 1, 'total': 1, 'controv': {
                    '$cond': [
                        {'$gt': ['$real', '$bogus']},
                        {'$pow': [{'$add': ['$real', '$bogus']},
                                  {'$divide': ['$bogus', '$real']}]},
                        {'$pow': [{'$add': ['$real', '$bogus']},
                                  {'$divide': ['$real', '$bogus']}]}
                    ]
                }
            }
        },
        {
            '$match': {
                'total': {'$lt': 50}
            }
        },
        {
            '$sort': {
                'controv': -1
            }
        },
        {
            '$limit': size
        }
    ]


def _consensus_query(size=100):
    return [
        {
            '$group': {
                '_id': '$subject_id',
                'total': {'$sum': 1},
                'real': {'$sum': {'$cond': [{'$eq': ['$annotation', 1]},
                                            1, 0]}},
                'bogus': {'$sum': {'$cond': [{'$eq': ['$annotation', 0]},
                                             1, 0]}}
            }
        },
        {
            '$project': {
                '_id': 1, 'real': 1, 'bogus': 1, 'total': 1, 'controv': {
                    '$cond': [
                        {'$gt': ['$real', '$bogus']},
                        {'$pow': [{'$abs': {'$subtract': ['$real', '$bogus']}},
                                  {'$subtract':
                                      [1, {'$divide': ['$bogus', '$real']}]}]},
                        {'$pow': [{'$abs': {'$subtract': ['$real', '$bogus']}},
                                  {'$subtract':
                                      [1, {'$divide': ['$real', '$bogus']}]}]},
                    ]
                }
            }
        },
        {
            '$match': {
                'total': {'$lt': 50}
            }
        },
        {
            '$sort': {
                'controv': -1
            }
        },
        {
            '$limit': size
        }
    ]


def get_controversial(size):
    query = _controv_query(size)
    cursor = DB().classifications.aggregate(query)
    subjects = []
    for item in cursor:
        subjects.append(item['_id'])

    return subjects


def get_consensus(size):
    query = _consensus_query(size)
    cursor = DB().classifications.aggregate(query)
    subjects = []
    for item in cursor:
        subjects.append(item['_id'])

    return subjects