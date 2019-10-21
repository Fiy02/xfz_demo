from haystack import indexes
from .models import News

# 创建索引类，给 news 做索引所以在 news 文件下创建该类；
class NewsIndex(indexes.SearchIndex,indexes.Indexable):
    # 作为索引的主要字段；
    text = indexes.CharField(document=True,use_template=True)

    # 指明该索引为哪个模型服务；
    def get_model(self):
        return News

    # 索引时在模型中返回哪些值，这里返回所有数据；
    def index_queryset(self, using=None):
        return self.get_model().objects.all()