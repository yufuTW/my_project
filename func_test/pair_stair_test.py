from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from pairstair.models import Programmer, Pair

FEWERTHANTWOERROR = u"There should be two or more programmers for pair stair."

class PairStairTest(TestCase):


    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_should_link_to_pair_creating_page_and_redirect_to_pair_stair_page_after_submission(self):
        names = ', '.join(['programmer 1', 'programmer 2'])
        self.create_pairs_with_programmers_names(names)

        self.assertEqual(self.driver.title, 'Pair Stair')

    def test_should_get_an_error_message_if_number_of_programmers_submitted_fewer_than_two(self):
        names = 'programmer1'
        self.create_pairs_with_programmers_names(names)
        self.element = self.driver.find_element_by_id("errormassage")
        self.error_message = self.element.text

        self.assertEqual(self.error_message, FEWERTHANTWOERROR)

    def create_pairs_with_programmers_names(self,names ):
        self.driver.get('http://localhost:8000/createpairs/')
        self.assertEqual(self.driver.title, 'Create Pairs')
        self.element = self.driver.find_element(By.CSS_SELECTOR, '#programmer_names')
        self.element.send_keys(names)
        self.driver.find_element(By.CSS_SELECTOR, '#add_programmers').click()

    def convert_to_text_list(self, elements):
        self.names = []
        for self.element in elements:
            self.names.append(self.element.text)
        return self.names

    def test_should_create_a_new_set_of_pairs_based_on_the_latest_submission(self):
        names1 = ', '.join(['programmer 1', 'programmer 2'])
        self.create_pairs_with_programmers_names(names1)

        names2 = ', '.join(['programmer3', 'programmer4'])
        self.create_pairs_with_programmers_names(names2)
        self.cols = self.driver.find_elements(By.CLASS_NAME, 'name_col')

        names = self.convert_to_text_list(self.cols)

        self.assertEqual(2, len(self.cols))
        for name in names2.split(', '):
            self.assertIn(name, names)

    def test_should_display_programmer_names_for_pair_stair_column_in_right_order(self):
        self.names = ', '.join(['pro1', 'pro2', 'pro3'])
        self.create_pairs_with_programmers_names(self.names)

        self.col_elements = self.driver.find_elements(By.CLASS_NAME, 'name_col')
        self.names_col = self.convert_to_text_list(self.col_elements)

        self.names_list = self.names
        for col_index in range(0, len(self.names_list)):
            self.assertEqual(self.names_list[col_index], self.names_col[col_index])

    def test_should_display_programmer_names_for_pair_stair_row_in_right_order(self):
        self.names = ', '.join(['pro1', 'pro2', 'pro3'])
        self.create_pairs_with_programmers_names(self.names)

        self.row_elements = self.driver.find_elements(By.CLASS_NAME, 'name_row')
        self.names_row = self.convert_to_text_list(self.row_elements)
        
        self.names_list = ['pro3', 'pro2']

        for row_index in range(len(self.names_list),0):
            self.assertEqual(self.names_list[row_index], self.names_row[row_index])


    def test_should_increase_pair_times(self):
        programmers = [Programmer(name = 'm1'), Programmer(name = 'm2')]
        pair = Pair(programmer_one = programmers[0].name, programmer_two = programmers[1].name, times = 0)
        pair.save()
        self.driver.get('http://localhost:8000/increase_pair_times/m1/m2/')
        pair = Pair.objects.filter(programmer_one = 'm1', programmer_two = 'm2')[0]
        self.assertEqual(1, pair.times)

