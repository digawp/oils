from django.conf import settings


class WorldCat(object):
    base_url = "http://www.worldcat.org/webservices/catalog/content/isbn/"
    def __init__(self):
        worldcat_settings = settings.WORLDCAT
        wskey = worldcat_settings.get('wskey')
        self.params = urllib.parse.urlencode({
            'wskey': wskey,
        })

    def lookup_by_isbn(self, isbn):
        url = urllib.parse.urljoin(WorldCat.base_url, isbn)
        parts = list(urllib.parse.urlsplit(url))
        parts[3] = self.params
        url = urllib.parse.urlunsplit(parts)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = self.process_response(response.read())
            return data

    def process_response(self, response):
        buff = io.BytesIO(response)
        records = pymarc.parse_xml_to_array(buff)
        try:
            record = records[0]
        except IndexError:
            fields = {}
        else:
            fields = {
                'title': record['245'].format_field(),
                'summary': record['520'].format_field(),
                'authors': record['100'].format_field(),
                'publisher': self.get_pubname(record),
                'year': self.get_pubyear(record),
                'subjects': record['650'].format_field()
            }
        return fields

    def get_pubname(self, record):
        return record['260']['b']

    def get_pubyear(self, record):
        matches = re.findall('\d{4}', record['260']['c'])
        try:
            return int(matches[0])
        except IndexError:
            return None
