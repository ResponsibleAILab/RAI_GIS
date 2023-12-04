from googlesearch import search

query = "something"
for result in search(query, num=10, stop=10, pause=2):
    print("Title: " + result)
