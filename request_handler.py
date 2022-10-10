import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_all_orders, get_all_sizes, get_all_styles, get_single_metal, get_single_order, get_single_size, get_single_style, create_order, delete_order, update_order


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  
        except ValueError:
            pass  

        return (resource, id)  # This is a tuple

    def do_GET(self):
        """Handles GET requests to the server """
        self._set_headers(200)

        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)
                if response is not None:
                    self._set_headers(200)
                else: 
                    self._set_headers(404)
                    response = {"message": f"{response} is not a metal kept in stock for jewelry."}
            else:
                response = get_all_metals()

        elif resource == "orders":
            if id is not None:
                response = get_single_order(id)
                if response is not None:
                    self._set_headers(200)
                else: 
                    self._set_headers(404)
                    response = {"message": "That order was never placed, or was cancelled."}

            else:
                response = get_all_orders()

        elif resource == "sizes":
            if id is not None:
                response = get_single_size(id)
                if response is not None:
                    self._set_headers(200)
                else: 
                    self._set_headers(404)
                    response = {"message": f"{response} is not a size kept in stock for jewelry."}
            else:
                response = get_all_sizes()

        elif resource == "styles":
            if id is not None:
                response = get_single_style(id)
                if response is not None:
                    self._set_headers(200)
                else: 
                    self._set_headers(404)
                    response = {"message": f"{response} is not a style kept in stock for jewelry."}
            else:
                response = get_all_styles()

        else:
            response = []

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        new_order = None

        if "metalId" in post_body and "sizeId" in post_body and "styleId" in post_body and "typeId" in post_body:
            self._set_headers(201)
            new_order = create_order(post_body)
        else:
            self._set_headers(400)
            new_order = {"message": f'{"Metal is required" if "metalId" not in post_body else""} {"Size is required" if "sizeId" not in post_body else ""} {"Style is required" if "styleId" not in post_body else ""} {"Type is required" if "typeId" not in post_body else ""}'}
        self.wfile.write(json.dumps(new_order).encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "orders":
            self._set_headers(405)
            response = {"message": "Editing an order requires contacting the company directly"}
        
        self.wfile.write(json.dumps(response).encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "orders":
            self._set_headers(405)
            response = {"message": "Cancelling an order requires contacting the company directly"}
        
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
