import requests
import unittest

from sure import expect


class APICreateTest(unittest.TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super(APICreateTest, self).__init__(*args, **kwargs)

        header = requests.api.post('https://regions-test.2gis.com/v1/auth/tokens').headers['Set-Cookie']
        self.token = header[header.find('=') + 1 : header.find(';')]
    
    def create(self, data: dict):
        return requests.api.post('https://regions-test.2gis.com/v1/favorites',
                    data=data, 
                    cookies={'token' : f'{self.token}'})



    def test_title(self):
        """
        Тестирование различных типов данных для поля title
        """
        
        try:
            TEST_DATA = {'title':'Home, sweet home', 'lat':0.0001, 'lon':0.0001}
            response = self.create(TEST_DATA).json()
            expect(response).equal_to({
                'color': None,
                'created_at': f'{response["created_at"]}',
                'id': response["id"],
                'lat': TEST_DATA["lat"], 
                'lon': TEST_DATA["lon"], 
                'title': str(TEST_DATA["title"])
            })
            
            TEST_DATA['title']=23.2
            response = self.create(TEST_DATA).json()
            expect(response).equal_to({
                'color': None,
                'created_at': f'{response["created_at"]}',
                'id': response["id"],
                'lat': TEST_DATA["lat"], 
                'lon': TEST_DATA["lon"], 
                'title': str(TEST_DATA["title"])
            })
        except KeyError:
            return self.fail(f'Unable to create favourite place with title = {TEST_DATA["title"]} type: {type(TEST_DATA["title"])}')


    def test_lat_lon_length(self):
        """
        Тестирование достоверности значений для координат
        """

        try:
            TEST_DATA = {'title':'Home, sweet home', 'lat':0.022000000001, 'lon':66666661 }
            response = self.create(TEST_DATA).json()
            expect(response).equal_to({
                'color': None,
                'created_at': f'{response["created_at"]}',
                'id': response["id"],
                'lat': TEST_DATA["lat"], 
                'lon': TEST_DATA["lon"], 
                'title': TEST_DATA["title"]
            })
        except KeyError:
            return self.fail(f'Unable to create favourite place with lat = {TEST_DATA["lat"]} length: {len(str(TEST_DATA["lat"]))} and with lon = {TEST_DATA["lon"]} length: {len(str(TEST_DATA["lon"]))}')

    
    def test_lat_lon(self):
        """
        Тестирование иного типа данных для координат
        """

        try:
            TEST_DATA = {'title':'Home, sweet home', 'lat':0, 'lon':'666' }
            response = self.create(TEST_DATA).json()
            expect(response).equal_to({
                'color': None,
                'created_at': f'{response["created_at"]}',
                'id': response["id"],
                'lat': TEST_DATA["lat"], 
                'lon': TEST_DATA["lon"], 
                'title': TEST_DATA["title"]
            })
        except KeyError:
            return self.fail(f'Unable to create favourite place with lat = {TEST_DATA["lat"]} type: {type(TEST_DATA["lat"])} and with lon = {TEST_DATA["lon"]} type: {type(TEST_DATA["lon"])}')
    

    def test_color(self):
        """
        Тестирование на допуск опечатки при ввода цвета
        """
        try:
            TEST_DATA = {'title':'Home, sweet home', 'lat':0.0001, 'lon':0.1, 'color':'R3D' }

            response = self.create(TEST_DATA).json()
            expect(response).equal_to({
                'color': TEST_DATA["color"],
                'created_at': f'{response["created_at"]}',
                'id': response["id"],
                'lat': TEST_DATA["lat"], 
                'lon': TEST_DATA["lon"], 
                'title': TEST_DATA["title"]
            })

        except KeyError:
            return self.fail(f'Unable to create favourite place with color = {TEST_DATA["color"]} type: {type(TEST_DATA["color"])}')
        

    def test_numeric_color(self):
        """
        Тестирование иного типа данных для поля color
        """
        try:
            TEST_DATA = {'title':'Home, sweet home', 'lat':0.0001, 'lon':0.1, 'color':1 }

            response = self.create(TEST_DATA).json()
            expect(response).equal_to({
                'color': TEST_DATA["color"],
                'created_at': f'{response["created_at"]}',
                'id': response["id"],
                'lat': TEST_DATA["lat"], 
                'lon': TEST_DATA["lon"], 
                'title': TEST_DATA["title"]
            })

        except KeyError:
            return self.fail(f'Unable to create favourite place with color = {TEST_DATA["color"]} type: {type(TEST_DATA["color"])}')


if __name__ == '__main__':
    
   unittest.main()
   