from django.test import TestCase

from blogs.forms import PostForm, EMPTY_TOPIC_ERROR, EMPTY_CONTENT_ERROR, EMPTY_INTRO_ERROR, LONG_TOPIC_ERROR, LONG_CONTENT_ERROR, LONG_INTRO_ERROR

class PostFormTest(TestCase):

    def test_form_valid_for_blank_items(self):
        form = PostForm(data={'topic': '', 'intro':'', 'content':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['topic'], [EMPTY_TOPIC_ERROR])
        self.assertEqual(form.errors['intro'], [EMPTY_INTRO_ERROR])
        self.assertEqual(form.errors['content'], [EMPTY_CONTENT_ERROR])

    def test_form_valid_for_long_topic(self):
        form = PostForm(
            data={
                'topic': '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 
                'intro':'12345', 
                'content':'12345'}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['topic'], [LONG_TOPIC_ERROR])
        
    def test_form_valid_for_long_intro(self):
        form = PostForm(
            data={
                'topic': '12345', 
                'intro':'1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 
                'content':'12345'}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['intro'], [LONG_INTRO_ERROR])
        