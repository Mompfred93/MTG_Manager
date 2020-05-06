def readDatabase(database):
    data = []
    with open(database) as input:
        data = input.read()
        
    return data
