from search_engine.Search_Engine import search

if __name__ == '__main__':
    query = input("How was your day?")
    mood_item = search(query=query)
    print(mood_item)




