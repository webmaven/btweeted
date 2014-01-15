from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.utils import timezone
from django.views import generic

from phrases.models import Phrase

def index(request, q=None):
    """
    The home page for the phrases app handles both the default view as well as
    the search results, depending on whether the 'q' parameter is present.
    """
    query = request.GET.get('q', q)
    if not query:
        # Just render the home page
        context = RequestContext(request, {})
        return render(request, 'phrases/index.html', context)

    else:
        # Show the searched-for query
        phrase, created = Phrase.objects.get_or_create(phrase_text=query)
        if not created:
            # If it isn't a new search phrase, increment the search count
            # We use an F() object for search count to avoid race conditions
            # update() doesn't honor DateField.auto_now, so set it directly
            Phrase.objects.filter(pk=phrase.pk).update(
                search_count=F('search_count')+1,
                last_searched=timezone.now())

        context = RequestContext(request, {'query': query,
            'phrase': phrase})
        return render(request, 'phrases/searchresults.html', context)

class RecentView(generic.ListView):
    """Display the last 10 searches."""
    model = Phrase
    template_name = 'phrases/recent.html'
    context_object_name = 'latest_search_list'

    def get_queryset(self):
        return Phrase.objects.order_by('-last_searched')[:10]

class PopularView(generic.ListView):
    """Display the 10 most frequent searches."""
    model = Phrase
    template_name = 'phrases/popular.html'
    context_object_name = 'popular_search_list'

    def get_queryset(self):
        return Phrase.objects.order_by('-search_count')[:10]
