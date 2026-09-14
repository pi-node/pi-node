require 'openssl'
require 'socket'

class SecureCommunication
  def initialize(node_id, private_key, certificate)
    @node_id = node_id
    @private_key = private_key
    @certificate = certificate
  end

  def establish_connection(node_id)
    # Establish a secure connection using TLS
    socket = TCPSocket.new('node-' + node_id, 8080)
    ssl_socket = OpenSSL::SSL::SSLSocket.new(socket, @private_key, @certificate)
    ssl_socket.connect
    return ssl_socket
  end

  def send_data(ssl_socket, data)
    # Send encrypted data over the secure connection
    ssl_socket.write(data)
  end

  def receive_data(ssl_socket)
    # Receive encrypted data over the secure connection
    ssl_socket.read
  end
end
