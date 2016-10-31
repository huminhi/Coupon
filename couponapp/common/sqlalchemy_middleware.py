'''
Created on Oct 11, 2013

@author: Duc Le
'''
from django.conf import settings

class MySQLAlchemySessionMiddleware(object):
    def process_request(self, request):
        request.db_session = settings.SESSION_DEFAULT

    def process_response(self, request, response):
        try:
            session = request.db_session
        except AttributeError:
            return response
        try:
            session.commit()
            #session.close()
            return response
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def process_exception(self, request, exception):
        try:
            session = request.db_session
        except AttributeError:
            return
        except Exception:
            return
        session.rollback()