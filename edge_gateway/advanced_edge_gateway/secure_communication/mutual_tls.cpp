#include <iostream>
#include <fstream>
#include <string>
#include <openssl/ssl.h>
#include <openssl/err.h>

// Define constants for certificate and private key files
const std::string CERT_FILE = "client.crt";
const std::string KEY_FILE = "client.key";
const std::string CA_FILE = "ca.crt";

// Function to load certificates and private keys
SSL_CTX* load_certificates(SSL_CTX* ctx) {
    // Load client certificate
    if (SSL_CTX_use_certificate_file(ctx, CERT_FILE.c_str(), SSL_FILETYPE_PEM) <= 0) {
        ERR_print_errors_fp(stderr);
        return NULL;
    }

    // Load client private key
    if (SSL_CTX_use_PrivateKey_file(ctx, KEY_FILE.c_str(), SSL_FILETYPE_PEM) <= 0) {
        ERR_print_errors_fp(stderr);
        return NULL;
    }

    // Load CA certificate
    if (SSL_CTX_load_verify_locations(ctx, CA_FILE.c_str(), NULL) <= 0) {
        ERR_print_errors_fp(stderr);
        return NULL;
    }

    return ctx;
}

// Function to verify peer certificate
int verify_peer_certificate(SSL* ssl, X509* cert) {
    // Get the subject and issuer names
    X509_NAME* subject = X509_get_subject_name(cert);
    X509_NAME* issuer = X509_get_issuer_name(cert);

    // Verify the certificate chain
    if (SSL_get_verify_result(ssl) != X509_V_OK) {
        std::cerr << "Certificate verification failed." << std::endl;
        return 0;
    }

    return 1;
}

int main() {
    // Initialize OpenSSL
    SSL_library_init();
    SSL_load_error_strings();
    ERR_load_BIO_strings();

    // Create an SSL context
    SSL_CTX* ctx = SSL_CTX_new(TLS_client_method());
    if (ctx == NULL) {
        ERR_print_errors_fp(stderr);
        return 1;
    }

    // Load certificates and private keys
    ctx = load_certificates(ctx);
    if (ctx == NULL) {
        return 1;
    }

    // Create an SSL object
    SSL* ssl = SSL_new(ctx);
    if (ssl == NULL) {
        ERR_print_errors_fp(stderr);
        return 1;
    }

    // Connect to the server
    BIO* bio = BIO_new_connect("localhost:8080");
    if (bio == NULL) {
        ERR_print_errors_fp(stderr);
        return 1;
    }

    SSL_set_bio(ssl, bio, bio);

    // Establish the TLS connection
    if (SSL_connect(ssl) <= 0) {
        ERR_print_errors_fp(stderr);
        return 1;
    }

    // Verify the peer certificate
    X509* cert = SSL_get_peer_certificate(ssl);
    if (cert == NULL) {
        std::cerr << "No peer certificate available." << std::endl;
        return 1;
    }

    if (!verify_peer_certificate(ssl, cert)) {
        return 1;
    }

    // Send and receive data
    const char* request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n";
    SSL_write(ssl, request, strlen(request));

    char buffer[1024];
    int bytes_received = SSL_read(ssl, buffer, 1024);
    if (bytes_received <= 0) {
        ERR_print_errors_fp(stderr);
        return 1;
    }

    std::cout << "Received response: " << buffer << std::endl;

    // Clean up
    SSL_free(ssl);
    SSL_CTX_free(ctx);
    BIO_free(bio);

    return 0;
}
