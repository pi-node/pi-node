use rand::Rng;
use rust_crypto::aes::{Aes128, Aes256};
use rust_crypto::block_modes::{BlockMode, Cbc};
use rust_crypto::hash::{Hmac, HmacSha256};
use rust_crypto::mac::{Mac, MacError};

struct QuantumEncryption {
    key: [u8; 32],
    iv: [u8; 16],
}

impl QuantumEncryption {
    fn new(key: [u8; 32], iv: [u8; 16]) -> Self {
        QuantumEncryption { key, iv }
    }

    fn encrypt(&self, plaintext: &[u8]) -> Vec<u8> {
        let cipher = Aes256::new_var(self.key, self.iv).unwrap();
        let encrypted = cipher.encrypt_vec(plaintext).unwrap();
        encrypted
    }

    fn decrypt(&self, ciphertext: &[u8]) -> Vec<u8> {
        let cipher = Aes256::new_var(self.key, self.iv).unwrap();
        let decrypted = cipher.decrypt_vec(ciphertext).unwrap();
        decrypted
    }
}
