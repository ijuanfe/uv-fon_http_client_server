#!/usr/bin/env python3

import argparse

import sys
import itertools
import socket
from socket import socket as Socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

# A simple web server

# Issues:
# Ignores CRLF requirement
# Header must be < 1024 bytes
# ...
# probabaly loads more


def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    #with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    # COMPLETE (1)
    #ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # The socket stays connected even after this script ends. So in order
    # to allow the immediate reuse of the socket (so that we can kill and
    # re-run the server while debugging) we set the following option. This
    # is potentially dangerous in real code: in rare cases you may get junk
    # data arriving at the socket.
    #ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # COMPLETE (2)
    endpoint = ('', args.port)

    # COMPLETE (3)
    #ss.bind(endpoint)
    #ss.listen(5)

    #print("server ready")

    '''while True:

         cs = ss.accept()[0]
         request = cs.recv(1024).decode('ascii')
         reply = http_handle(request)
         cs.send(reply.encode('ascii'))
         print reply

	 print request
         print("\n\nReceived request")
         print("======================")	--- USE LAS LIBRERIAS BaseHTTPServer PARA MI SOLUCION ---
         print(request.rstrip())
         print("======================")


         print("\n\nReplied with")
         print("======================")
         print(reply.rstrip())
         print("======================")

    return 0'''

    try:
	# Instancio el servidor web y defino el manejador
	# que se encargara de manejar los HTTP request
	server = HTTPServer(endpoint, http_handle)
	print 'Servidor HTTP iniciado en el puerto ' , args.port
	print 'Nota: solo existen 3 archivos en el servidor: /index.html, img_test.jpg y /gif_test.gif'
	# Le digo al servidor que espere siempre por HTTP requests
	server.serve_forever()

	# Si uso la tecla Ctrl + C, cerrara la conexion del servidor
    except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()


# Clase que se encarga de manejar los HTTP request
class http_handle(BaseHTTPRequestHandler):
    """Given a http requst return a response

    Both request and response are unicode strings with platform standard
    line endings.
    """

    #assert not isinstance(request_string, bytes)

    # Fill in the code to handle the http request here. You will probably want
    # to write additional functions to parse the http request into a nicer data
    # structure (eg a dict), and to easily create http responses.

    # COMPLETE (4)
    # esta funcion DEBE RETORNAR UNA CADENA que contenga el recurso (archivo)
    # que se consulta desde un navegador e.g. http://localhost:2080/index.html
    # En el ejemplo anterior se esta solicitando por el archivo 'index.html'
    # Referencias que pueden ser de utilidad
    # - https://www.acmesystems.it/python_http, muestra como enviar otros
    #                                           archivos ademas del HTML
    # - https://goo.gl/i7hJYP, muestra como construir un mensaje de respuesta
    #                          correcto en HTTP

    # Manejador para los GET requests
    def do_GET(request_string):

	# Dependiendo que archivo el browser solicite entonces
	# asignara la ruta donde esta ubicado el recurso solicitado
	if request_string.path=="/index.html":
		request_string.path="/index.html"
	if request_string.path=="/img_test.jpg":
                request_string.path="/img_test.jpg"
	if request_string.path=="/gif_test.gif":
                request_string.path="/gif_test.gif"

	try:
		# Configuramos que Content-type header fue solicitado
		# para asi mismo enviarlo en el reponse al browser
		sendReply = False
		if request_string.path.endswith(".html"):
			mimetype='text/html'
			sendReply = True
		if request_string.path.endswith(".jpg"):
			mimetype='image/jpg'
			sendReply = True
		if request_string.path.endswith(".gif"):
			mimetype='image/gif'
			sendReply = True
		if request_string.path.endswith(".js"):
			mimetype='application/javascript'
			sendReply = True
		if request_string.path.endswith(".css"):
			mimetype='text/css'
			sendReply = True

		if sendReply == True:
			# Una vez existe el recurso (archivo)
			# lo abrimos y lo enviamos al broser
			f = open(curdir + sep + request_string.path)
			request_string.send_response(200)
			request_string.send_header('Content-type',mimetype)
			request_string.end_headers()
			request_string.wfile.write(f.read())
			f.close()
		return
	# Se lanza una excepcion si el archivo no existe en las carpetas del servidor
	except IOError:
		request_string.send_error(404,'File Not Found: %s' % request_string.path)

if __name__ == "__main__":
    sys.exit(main())
