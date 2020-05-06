import json


def englishCards(database):
    if not isinstance(database, str):
        raise ValueError('database must be of type string!')
    
    return json.loads(databse)


def germanCards(database):
    if not isinstance(database, str):
        raise ValueError('database must be of type string!')
    
    germanCards = []
    cards = json.loads(database)
    for card in cards:
        if not len(cards[card]['foreignData']) == 0:
            for data in cards[card]['foreignData']:
                language = data['language']
                if language == 'German':
                    germanCards.append(card)
                    
    return germanCards
        
