from tastypie.resources import ModelResource
from tastypie import fields
from reader.models import Feed, Subscription

class FeedResource (ModelResource):
    class Meta:
        queryset = Feed.objects.all()

class SubscriptionResource (ModelResource):
    feed = fields.ToOneField(FeedResource, 'feed', full=True)

    class Meta:
        queryset = Subscription.objects.all()

    def get_object_list(self, request):
        return super(SubscriptionResource, self).get_object_list(request).filter(user=request.user)
