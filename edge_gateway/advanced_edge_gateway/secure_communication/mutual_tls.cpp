// edge_gateway/secure_communication/mutual_tls.cpp
#include <openssl/ssl.h>
#include <openssl/err.h>

class MutualTLS {
public:
    MutualTLS(const char* cert_file, const char* key_file) {
        // Initialize SSL context
        SSL_CTX* ctx = SSL_CTX_new(TLS_client_method());
        SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, nullptr);

        // Load certificate and private key
        SSL_CTX_use_certificate_file(ctx, cert_file, SSL_FILETYPE_PEM);
        SSL_CTX_use_PrivateKey_file(ctx, key_file, SSL_FILETYPE_PEM);

        // Create SSL object
        ssl_ = SSL_new(ctx);
    }

    ~MutualTLS() {
        SSL_free(ssl_);
    }

    int connect(const char* hostname, int port) {
        // Establish connection to server
        BIO* bio = BIO_new_connect(hostname, port);
        SSL_set_bio(ssl_, bio, bio);

        // Perform mutual TLS handshake
        SSL_connect(ssl_);
        SSL_do_handshake(ssl_);

        return SSL_get_verify_result(ssl_) == X509_V_OK;
    }

    int send_data(const char* data) {
        // Send data over the secure connection
        return SSL_write(ssl_, data, strlen(data));
    }

    int receive_data(char* buffer, int buffer_size) {
        // Receive data over the secure connection
        return SSL_read(ssl_, buffer, buffer_size);
    }

private:
    SSL* ssl_;
};
