package main

import (
	"crypto/ecdsa"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"

	"github.com/hyperledger/fabric-sdk-go/pkg/client/msp"
)

type BlockchainAuth struct {
	mspClient *msp.Client
}

func NewBlockchainAuth(mspClient *msp.Client) *BlockchainAuth {
	return &BlockchainAuth{mspClient: mspClient}
}

func (ba *BlockchainAuth) AuthenticateNode(nodeId string) error {
	// Generate a random nonce
	nonce, err := rand.Read(make([]byte, 32))
	if err != nil {
		return err
	}

	// Create a signature using the node's private key
	signature, err := ecdsa.Sign(rand.Reader, &nodeId, nonce)
	if err != nil {
		return err
	}

	// Verify the signature using the node's public key
	pubKey, err := ba.mspClient.GetPublicKey(nodeId)
	if err != nil {
		return err
	}
	if !ecdsa.Verify(pubKey, nonce, signature) {
		return fmt.Errorf("invalid signature")
	}

	return nil
}
