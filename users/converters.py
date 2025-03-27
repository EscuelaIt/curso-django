class YearConverter:
    """
    Conversor personalizado para años entre 1900 y 2999
    """
    regex = '[1-2][0-9]{3}'
    
    def to_python(self, value):
        return int(value)
    
    def to_url(self, value):
        return str(value)
        
        
class SlugUsernameConverter:
    """
    Conversor para usernames que solo permite letras, números y guiones
    """
    regex = '[-a-zA-Z0-9_]+'
    
    def to_python(self, value):
        return value
    
    def to_url(self, value):
        return value 