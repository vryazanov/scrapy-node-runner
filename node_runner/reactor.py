from scrapy.utils.reactor import install_reactor

install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')


def get_reactor():
    from twisted.internet import reactor
    return reactor

