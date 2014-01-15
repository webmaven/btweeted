from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase

from bs4 import BeautifulSoup

from phrases.models import Phrase

class PhraseTests(TestCase):
    def test_phrase_is_created(self):
        """
        Test that a Phrase can be created, and the search count defaults to 1.
        """
        phrase = Phrase.objects.create(phrase_text = 'test phrase')
        self.assertEqual(phrase.phrase_text, 'test phrase')
        self.assertEqual(phrase.pk, 1)
        self.assertEqual(phrase.search_count, 1)

    def test_phrase_is_normalized_on_creation(self):
        """
        Test that when a phrase is created that the text is properly normalized.
        """
        phrase = Phrase.objects.create(phrase_text = 'Test phrase ')
        self.assertEqual(phrase.pk, 1)
        self.assertEqual(phrase.phrase_text, 'test phrase')

    def test_phrase_no_duplicates(self):
        """
        Test that a phrase with duplicate phrase text or a slight variation
        can't be created.
        """
        phrase = Phrase.objects.create(phrase_text='test phrase')
        # Test that the identical string fails
        self.assertRaises(IntegrityError,
            Phrase.objects.create, 
            phrase_text='test phrase')
        # Test that a slightly different string fails
        self.assertRaises(IntegrityError,
            Phrase.objects.create,
            phrase_text='Test phrase ')

    def test_phrase_get_or_create_normalized(self):
        """
        Test that get_or_create() correctly returns the same object when using
        slightly different text.
        """
        phrase1 = Phrase.objects.get_or_create(phrase_text = 'test phrase')
        self.assertEqual(phrase1[1], True) # Check for object creation
        phrase2 = Phrase.objects.get_or_create(phrase_text = 'Test phrase ')
        self.assertEqual(phrase2[1], False) # Should not be created
        self.assertEqual(phrase1[0].pk, phrase2[0].pk) # Same object

class PhraseViewTests(TestCase):
    def test_index_view(self):
        """
        Make sure the front page of the app comes up.
        """
        response = self.client.get(reverse('phrases:index'))
        self.assertEqual(response.status_code, 200)

    def test_recent_view_with_no_phrases(self):
        """
        If no phrases have been added, an appropriate message should be
        displayed.
        """
        response = self.client.get(reverse('phrases:recent'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No searches have been done.")
        self.assertQuerysetEqual(response.context['latest_search_list'], [])

    def test_recent_view_with_phrase(self):
        """
        If a phrase is added, make sure it appears on the recent searches page.
        """
        phrase = Phrase.objects.create(phrase_text = 'test phrase')
        response = self.client.get(reverse('phrases:recent'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'test phrase')
        self.assertQuerysetEqual(response.context['latest_search_list'],
            ['<Phrase: test phrase>'])

    def test_recent_view_most_recent(self):
        """
        Regardless of the order they were created, phrases should be listed in
        the order they were last searched for.
        """
        #Create two phrases by searching for them
        search1 = self.client.get(reverse('phrases:index'),
            {'q':'test one'})
        search2 = self.client.get(reverse('phrases:index'),
            {'q':'test two'})
        # The second search is the more recent one
        response = self.client.get(reverse('phrases:recent'))
        self.assertQuerysetEqual(response.context['latest_search_list'],
            ['<Phrase: test two>','<Phrase: test one>'])
        # Search for the first again
        search3 = self.client.get(reverse('phrases:index'),
            {'q':'test one'})
        # Verify that the first search is now more recent
        response = self.client.get(reverse('phrases:recent'))
        self.assertQuerysetEqual(response.context['latest_search_list'],
            ['<Phrase: test one>','<Phrase: test two>'])

    def test_popular_view_with_no_phrases(self):
        """
        If no phrases have been added, an appropriate message should be 
        displayed.
        """
        response = self.client.get(reverse('phrases:popular'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No searches have been done.")
        self.assertQuerysetEqual(response.context['popular_search_list'], [])

    def test_popular_view_with_phrase(self):
        """
        If a phrase is added, make sure it appears on the popular searches page.
        """
        phrase = Phrase.objects.create(phrase_text = 'test phrase')
        response = self.client.get(reverse('phrases:popular'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test phrase')
        self.assertQuerysetEqual(response.context['popular_search_list'],
            ['<Phrase: test phrase>'])


    def test_popular_view_most_popular(self):
        """
        Phrases that are searched more often are displayed first.
        """
        #Create two phrases by searching for them
        search1 = self.client.get(reverse('phrases:index'), 
            {'q':'test one'})
        search2 = self.client.get(reverse('phrases:index'), 
            {'q':'test two'})
        # get the popular view
        response = self.client.get(reverse('phrases:popular'))
        self.assertQuerysetEqual(response.context['popular_search_list'],
             ['<Phrase: test one>','<Phrase: test two>'])
        # Search for the second again
        search3 = self.client.get(reverse('phrases:index'), 
            {'q':'test two'})
        # Verify that the second search is now more popular
        response = self.client.get(reverse('phrases:popular'))
        self.assertQuerysetEqual(response.context['popular_search_list'],
             ['<Phrase: test two>','<Phrase: test one>'])


    def test_search_result_view_with_no_phrases(self):
        """
        If a phrase is searched for, add it.
        """
        searchresult = self.client.get(reverse('phrases:index'), 
            {'q':'test phrase'})
        self.assertEquals(searchresult.status_code, 200)
        self.assertEquals(Phrase.objects.get(pk=1).phrase_text, 'test phrase')

    def test_search_result_view_with_phrase(self):
        """
        Phrases can be created even if other phrases have 
        already been created.
        """
        searchresult = self.client.get(reverse('phrases:index'), 
            {'q':'test phrase'})
        self.assertContains(searchresult, 'test phrase')
        searchresult2 = self.client.get(reverse('phrases:index'), 
            {'q':'another test phrase'})
        self.assertContains(searchresult2, 'another test phrase')
        self.assertEquals(Phrase.objects.get(pk=2).phrase_text,
            'another test phrase')

    def test_search_result_twitter_results(self):
        """
        When searching for a phrase, we get 15 results from Twitter.
        """
        searchresult = self.client.get(reverse('phrases:index'), 
            {'q':'test phrase'})
        soup = BeautifulSoup(searchresult.content)
        tweets = soup.find_all('div', class_='stream-item')
        self.assertEquals(len(tweets), 15)

    def test_search_result_view_with_similar_phrase(self):
        """
        If you search for a phrase that is close to an existing one, that a new
        Phrase object is not created, but that the search_count on the existing
        Phrase is incremented instead.
        """
        searchresult = self.client.get(reverse('phrases:index'), 
            {'q':'test phrase'})
        self.assertEquals(Phrase.objects.get(pk=1).search_count, 1)
        searchresult2 = self.client.get(reverse('phrases:index'), 
            {'q':'Test phrase '})
        self.assertEquals(Phrase.objects.get(pk=1).search_count, 2)

    def test_urlencoding_search_links(self):
        """
        Since searches can have characters that aren't allowed in URLs, search
        links need to have the query string URL-encoded.
        """
        phrase = Phrase.objects.create(phrase_text = 'punctuation:')
        recent = self.client.get(reverse('phrases:recent'))
        popular = self.client.get(reverse('phrases:popular'))
        self.assertContains(recent, '/?q=punctuation%3A')
        self.assertContains(popular, '/?q=punctuation%3A')
