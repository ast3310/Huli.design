import json

class Carousel():
    def __init__(self):
        self.carousel_data = {
            'type': 'carousel',
            'elements' : []
        }
    
    def add_element(self, title='', description='', photo_id='', buttons=[], action={}):
        element = {}
        
        if title != '':
            element['title'] = title

        if description != '':
            element['description'] = description
        
        if photo_id != '':
            element['photo_id'] = photo_id
        
        if buttons != []:
            element['buttons'] = buttons
        
        if action != {}:
            element['action'] = action

        if element != {}:
            self.carousel_data['elements'].append(element)
    

    def get_json(self):
        return json.dumps(self.carousel_data, ensure_ascii=False).encode('utf8')
    

    def get_dict(self):
        return self.carousel_data
