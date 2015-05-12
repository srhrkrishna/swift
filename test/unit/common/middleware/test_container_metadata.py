import unittest
from cStringIO import StringIO
from webob import Request, Response
from swift.common.middleware.container_metadata import ContainerObjectMetadataMiddleware


class FakeApp(object):
    def __call__(self, env, start_response):
        return Response(body="FAKE APP")(env, start_response)
 

class TestContainerObjectMetadataMiddleware(unittest.TestCase):
    def setUp(self):
        self.app = ContainerObjectMetadataMiddleware(FakeApp(), {})
 
    def test_get_empty(self):
        resp = Request.blank('/v1/account/container',
                             environ={
                                 'REQUEST_METHOD': 'GET',
                             }).get_response(self.app)
        self.assertEqual(resp.body, "FAKE APP")
 
    # def test_put_no_virus(self):
    #     resp = Request.blank('/v1/account/container/object',
    #                          environ={
    #                              'REQUEST_METHOD': 'PUT',
    #                              'wsgi.input': StringIO('foobar')
    #                          }).get_response(self.app)
    #     self.assertEqual(resp.body, "FAKE APP")
    #
    # def test_put_virus(self):
    #     resp = Request.blank('/v1/account/container/object',
    #                          environ={
    #                              'REQUEST_METHOD': 'PUT',
    #                              'wsgi.input': StringIO(pyclamd.EICAR)
    #                          }).get_response(self.app)
    #     self.assertEqual(resp.status_code, 403)