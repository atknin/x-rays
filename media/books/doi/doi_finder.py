from habanero import cn
doi = "10.1021/ie50175a011"
a = cn.content_negotiation(ids = doi, format = "text")
a = cn.content_negotiation(ids = doi, format = "bibentry")
print(a)
