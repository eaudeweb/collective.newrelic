import newrelic.agent
import newrelic.api

from Products.ZCatalog.ZCatalog import ZCatalog
from collective.newrelic.utils import logger

ZCatalog.original_zope_catalogtool_searchResults = ZCatalog.searchResults


def newrelic_searchResults(self, REQUEST=None, **kw):
    trans = newrelic.agent.current_transaction()

    with newrelic.api.database_trace.DatabaseTrace(trans, str(kw), self):
        result = self.original_zope_catalogtool_searchResults(REQUEST, **kw)

    return result

ZCatalog.searchResults = newrelic_searchResults
logger.info("Patched Products.ZCatalog.ZCatalog:ZCatalog.searchResults with instrumentation")
