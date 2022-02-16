import os


class SimpleCache:
    def __init__(self, filename):
        self.path = os.getcwd() + '/simplecache/' + str(filename)
        if not os.path.exists(os.getcwd() + '/simplecache/'):
            os.mkdir(os.getcwd() + '/simplecache/')

        if not os.path.exists(self.path):
            os.system(f"touch {self.path}")

    def cache(self, cache):
        cache = str(cache)
        os.system(f'echo {cache} > {self.path}')

    def fetch_cache(self):
        with open(self.path) as f:
            text = f.read()
            if text.strip() == "":
                return None
            else:
                return text
