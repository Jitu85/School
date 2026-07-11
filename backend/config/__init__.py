try:
    import django.template.context as dj_context
    from copy import copy

    # Monkeypatch Django BaseContext.__copy__ for Python 3.14+ compatibility
    # In Python 3.14+, copy(super()) returns a super object, causing attribute assignment crashes.
    # We bypass this by manually constructing the copy via object.__new__
    def patched_basecontext_copy(self):
        duplicate = object.__new__(self.__class__)
        for k, v in self.__dict__.items():
            if k != 'dicts':
                duplicate.__dict__[k] = copy(v)
        duplicate.dicts = self.dicts[:]
        return duplicate

    dj_context.BaseContext.__copy__ = patched_basecontext_copy
except ImportError:
    pass
