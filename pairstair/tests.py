from django.test import TestCase
from django.test.client import Client
from pairstair.views import *

class TestPair(TestCase):
    def test_should_store_names_and_paired_times(self):
        pair = Pair(programmer_one = 'person1', programmer_two = 'person2', times =  0)

        self.assertEqual('person1', pair.programmer_one)
        self.assertEqual('person2', pair.programmer_two)
        self.assertEqual(0, pair.times)

    def test_the_default_paired_times_is_zero(self):
        pair = Pair(programmer_one = 'person1', programmer_two = 'person2')

        self.assertEqual(0, pair.times)


class ProgrammerTest(TestCase):
    def test_should_create_a_user_with_given_name(self):
        expectedName = 'personName'
        person = Programmer(name = expectedName)

        self.assertEqual(expectedName, person.name)

NAMES = ['programmer 1', 'programmer 2']

def format_names(names):
    return ', '.join(names)


class TestCreatePairs(TestCase):

    def test_should_be_able_to_link_to_create_pairs_page_and_use_the_right_template(self):
        response = Client().get('/createpairs/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_pairs.html')

    def test_should_create_right_number_of_programmers_based_names_submitted(self):
        Client().post('/createpairs/', {'programmer_names': format_names(NAMES)})
        self.assertEqual(2, Programmer.objects.count())

        Client().post('/createpairs/', {'programmer_names': format_names(NAMES)})
        self.assertEqual(2, Programmer.objects.count())

    def test_should_rise_an_exception_when_fewer_than_two_programmers_submitted(self):
        with self.assertRaises(FewerThanTwoProgrammersSubmitted):
          create_programmers_for_pair_stair(["programmer1"])

class TestPairStair(TestCase):
    def test_should_render_to_the_pair_stair_template_for_pair_stair_page(self):
        response = Client().get('/pairstair/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pair_stair.html')

    def test_should_include_all_submitted_programmer_on_stair(self):
        response = Client().post('/createpairs/', {'programmer_names': format_names(NAMES)}, follow=True)

        for name in NAMES:
            self.assertContains(response, name)

    def test_increase_one_for_pair_times_for_associated_pair(self):
        pair = Pair(programmer_one = 'm1', programmer_two = 'm2')
        pair.save()

        before_times = pair.times
        Client().get('/increase_pair_times/m1/m2/')

        pair = Pair.objects.filter(programmer_one = 'm1', programmer_two = 'm2')[0]
        self.assertEqual(pair.times, before_times + 1)
        

        