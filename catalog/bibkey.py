

class Bibkey(object):
    def __init__(self, _type, _value):
        self._type = _type.lower()
        self._value = _value

    def __str__(self):
        return "{}:{}".format(self.bibtype, self.bibvalue)

    @property
    def bibtype(self):
        return self._type

    @property
    def bibvalue(self):
        return self._value
    
    @classmethod
    def parse_bibkeys(cls, bibkeys_str):
        """Return list of bibkey object from comma separated bibkey string"""
        return list(filter(None, 
                [cls.parse_bibkey(raw) for raw in bibkeys_str.split(',')]))

    @classmethod
    def parse_bibkey(cls, bibkey_str):
        """Return bibkey object from bibkey string"""
        try:
            return cls(*bibkey_str.split(':'))
        except TypeError:
            return None

    @classmethod
    def parse(cls, bibkey_str):
        """
        Return list of bibkey object from comma separated bibkey string
        or
        Return bibkey object from bibkey string
        """
        bibkeys = cls.parse_bibkeys(bibkey_str)
        if len(bibkeys) == 0:
            return None
        if len(bibkeys) == 1:
            return bibkeys[0]
        else:
            return bibkeys
