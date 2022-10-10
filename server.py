import json
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from repository import all, retrieve, create, update, delete


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = url_components.query.split("&")
        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id, query_params)

    def get_all_or_single(self, resource, id, query_params):
        if id is not None:
            response = retrieve(resource, id, query_params)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = f'This {resource[:-1]} cannot be found'
        else:
            self._set_headers(200)
            response = all(resource)

        return response


    def do_GET(self):
        response = {}
        (resource, id, query_params) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id, query_params)
        self.wfile.write(json.dumps(response).encode())


    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)

        new_order = None

        if resource == "orders":
            if "metalId" in post_body and "sizeId" in post_body and "styleId" in post_body and "typeId" in post_body:
                self._set_headers(201)
                new_order = create(resource, post_body)
            else:
                self._set_headers(400)
                new_order = {"message": f'{"Metal is required" if "metalId" not in post_body else""} {"Size is required" if "sizeId" not in post_body else ""} {"Style is required" if "styleId" not in post_body else ""}'}
        else:
            new_order = {"message": f'A {resource[:-1]} cannot be created by a customer'}

        self.wfile.write(json.dumps(new_order).encode())

    def do_PUT(self):
        response = ""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            self._set_headers(204)
            update(resource, id, post_body)
        else:
            self._set_headers(405)
            response = {"message": "Editing an order requires contacting the company directly"}

        self.wfile.write(json.dumps(response).encode())


    def do_DELETE(self):
        self._set_headers(405)
        (resource, id) = self.parse_url(self.path)

        response = {"message": "Deletions are not permitted"}
        
        self.wfile.write(json.dumps(response).encode())


    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
