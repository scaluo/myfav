# from goose import Goose
# from goose.text import StopWordsChinese
# url  = 'http://www.bbc.co.uk/zhongwen/simp/chinese_news/2012/12/121210_hongkong_politics.shtml'
# g = Goose({'stopwords_class': StopWordsChinese})
# article = g.extract(url=url)
# print article.cleaned_text[:150]


from goose import Goose
url = 'http://weibo.com/ttarticle/p/show?hmsr=toutiao.io&id=2309404003654557427834&utm_medium=toutiao.io&utm_source=toutiao.io'
g = Goose()
article = g.extract(url=url)
print article.title
print article.cleaned_text[:150]