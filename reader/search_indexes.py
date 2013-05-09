from haystack import indexes
from reader.models import Story

class StoryIndex (indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, stored=False)
    feed_id = indexes.IntegerField(stored=True, indexed=False, model_attr='feed_id')
    date_published = indexes.DateField(stored=True, indexed=False, model_attr='date_published')

    def get_model(self):
        return Story

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
