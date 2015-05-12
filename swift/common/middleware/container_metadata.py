from swift.common.http import is_success
from swift.common.swob import wsgify, Response, Request
from swift.common.utils import split_path, get_logger
from swift.common.request_helpers import get_sys_meta_prefix
from swift.proxy.controllers.base import get_object_info

from eventlet import Timeout
from eventlet.green import urllib2

import json


class ContainerObjectMetadataMiddleware(object):
    """
    ContainerObjectMetadata Middleware will enrich normal container object response
    with each object's metadata.

    If the header contains optional "x-object-metadata" with true value, each
    object's metadata is sent along with the normal response.
    """

    def __init__(self, app, conf):
        self.app = app
        self.logger = get_logger(conf, log_route='containerobjectmetadata')

    @wsgify
    def __call__(self, req):
        obj = None
        logfile = open('/home/ubuntu/files/swiftmiddlewarelog.txt', 'wb+')
        try:
            (version, account, container) = split_path(req.path_info, 3, 3, True)
        except ValueError:
            pass

        resp = req.get_response(self.app)
        try:
            if container and is_success(resp.status_int) and req.method == 'GET' \
                    and req.headers['x-metadata-object'] == 'true':
                json_response = json.loads(resp.body)
                for item in json_response:
                    logfile.write(str(item) + '\n')
                    for obj_info_item in \
                            get_object_info(req.environ, self.app, req.path_info + '/'+item['name']).items():
                        logfile.write(str(obj_info_item))
                        if obj_info_item[0] == 'meta' or obj_info_item[0] == 'sysmeta':
                            item[obj_info_item[0]] = obj_info_item[1]
                            # logfile.write(str(obj_info_item) + '\n')
                    # logfile.write(str(item) + '\n')

                # logfile.write(str(json_response)+'\n')
                # logfile.write(str(resp.status_int)+'\n')
                # logfile.write(str(resp.headers)+'\n')
                resp.body = json.dumps(json_response)
        except Exception, e:
            # logfile.write(str(e))
            pass
        return resp


def container_object_metadata_factory(global_conf, **local_conf):
    # register_swift_info('container_metadata')
    conf = global_conf.copy()
    conf.update(local_conf)
    def container_object_metadata_filter(app):
        return ContainerObjectMetadataMiddleware(app, conf)
    return container_object_metadata_filter


