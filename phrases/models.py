from django.db import models
from django.utils.translation import ugettext as _

def normalize(s):
    """
    Used to normalize phrase_text consistently for both object creation and
    retreival. Currently just strips extra leading and trailing whitespace and 
    lowercases the string.
    TODO: strip extra whitespace out of the middle of the string as well.
    """
    s = s.strip().lower()
    return s

class CIQuerySet(models.query.QuerySet):
    """
    Case insensitivity and less whitespace sensitivity for phrase_text.
    """
    def _filter_or_exclude(self, mapper, *args, **kwargs):
        if 'phrase_text' in kwargs:
            kwargs['phrase_text'] = normalize(kwargs['phrase_text'])
        return super(CIQuerySet, self)._filter_or_exclude(mapper, *args, **kwargs)

class PhraseManager(models.Manager):
    """
    This manager uses case-insensitive and less sensitive to whitespace
    QuerySet().
    """
    def get_query_set(self):
        return CIQuerySet(self.model)

class Phrase(models.Model):
    """
    A phrase that someone has searched for in the app. Text is normalized
    somewhat into a unique field to get better counts of searches.
    """
    phrase_text = models.CharField(max_length=200, unique=True, db_index=True)
    search_count = models.IntegerField(_('search count'), default=1)
    last_searched = models.DateTimeField(_('last searched'), auto_now=True)
    objects = PhraseManager()


    def __unicode__(self):
        return self.phrase_text

    def save(self, *args, **kwargs):
        self.phrase_text = normalize(self.phrase_text)
        super(Phrase, self).save(*args, **kwargs)
