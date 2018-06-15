import unittest, sys, json
sys.path.insert(0, '..')
from dashwithtables import app

class DashTablesTestCase(unittest.TestCase):
    response = app.serve_layout()
    raw = response.data
    str = raw.decode()
    children = json.loads(str)['props']['children']

    def test_dash_dropdown(self):
        self.assertEqual(self.response.status_code, 200)
        options = [{'label': 'Country', 'value': 'Country'}, {'label': 'Pho', 'value': 'Pho'}, {'label': 'Ramen', 'value': 'Ramen'}, {'label': 'Soba', 'value': 'Soba'}]
        self.assertEqual(self.children[0]['props']['options'], options)
        self.assertEqual(self.children[0]['props']['value'], 'Country')
        self.assertEqual(self.children[0]['type'], 'Dropdown')

    def test_dash_h3(self):
        title = 'Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018'
        self.assertEqual(self.children[1]['props']['children'], title)
        self.assertEqual(self.children[1]['type'], 'H3')

    def test_callback(self):
        container = app.callback_map
        callback = container['table-container.children']['callback']
        response = callback('Ramen')
        str = response.data.decode()
        data = json.loads(str)

        headers = data['response']['props']['children']['props']['children'][0]['props']['children']
        headers_list = [el['props']['children'] for el in headers]
        result = ['Country', 'Pho', 'Ramen', 'Soba']
        self.assertEqual(headers_list, result)

        order = data['response']['props']['children']['props']['children'][1:]
        ordered_countries = [el['props']['children'][0]['props']['children'] for el in order]
        correct = ['India', 'Canada', 'France', 'Australia', 'Russia', 'United States', 'United Kingdom', 'Germany', 'Poland', 'Netherlands', 'South Korea', 'China', 'Brazil', 'Thailand', 'Malaysia', 'Japan', 'Indonesia', 'Italy', 'Mexico', 'Singapore', 'Spain', 'Hong Kong', 'Philippines', 'Taiwan']
        self.assertEqual(ordered_countries, correct)
