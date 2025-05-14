from gdeltdoc import GdeltDoc, Filters

f = Filters(
    start_date = "2024-05-01",
    end_date = "2024-11-02",
    num_records = 250,
    keyword = "microsoft",
    domain = "nytimes.com",
    country = "US",
)


gd = GdeltDoc()

# Search for articles matching the filters
articles = gd.article_search(f)
print(articles)
# Get a timeline of the number of articles matching the filters
# timeline = gd.timeline_search("timelinevol", f)