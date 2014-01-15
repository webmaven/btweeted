from django.contrib import admin
from phrases.models import Phrase

class PhraseAdmin(admin.ModelAdmin):
    list_display = ['phrase_text', 'search_count', 'last_searched']
    fields = ['phrase_text', 'search_count']
    list_filter = ['last_searched']
    search_fields = ['phrase_text']

admin.site.register(Phrase, PhraseAdmin)
