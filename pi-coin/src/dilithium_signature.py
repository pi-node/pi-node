from pqcrypto.sign import dilithium2

def generate_keypair():
    """Generate a public and secret key pair using Dilithium."""
    public_key, secret_key = dilithium2.generate_keypair()
    return public_key, secret_key

def sign_message(message, secret_key):
    """Sign a message using the provided secret key."""
    signature = dilithium2.sign(message, secret_key)
    return signature

def verify_signature(signature, message, public_key):
    """Verify the signature of a message using the provided public key."""
    is_valid = dilithium2.verify(signature, message, public_key)
    return is_valid

def main():
    # Generate key pair
    public_key, secret_key = generate_keypair()
    print("Public Key:", public_key)
    print("Secret Key:", secret_key)

    # Define the message to be signed
    message = b"Transaction data"

    # Sign the message
    signature = sign_message(message, secret_key)
    print("Signature:", signature)

    # Verify the signature
    is_valid = verify_signature(signature, message, public_key)
    print("Is the signature valid?", is_valid)

if __name__ == "__main__":
    main()
