package main

import (
	"context"
	"fmt"
	"log"

	"go.etcd.io/etcd/clientv3"
	"go.etcd.io/etcd/clientv3/concurrency"
)

type DistributedStorage struct {
	client *clientv3.Client
}

func NewDistributedStorage(endpoints []string) (*DistributedStorage, error) {
	client, err := clientv3.New(clientv3.Config{
		Endpoints:   endpoints,
		DialTimeout: 5 * time.Second,
	})
	if err != nil {
		return nil, err
	}
	return &DistributedStorage{client: client}, nil
}

func (ds *DistributedStorage) Put(key string, value string) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	_, err := ds.client.Put(ctx, key, value)
	return err
}

func (ds *DistributedStorage) Get(key string) (string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	resp, err := ds.client.Get(ctx, key)
	if err != nil {
		return "", err
	}
	return string(resp.Kvs[0].Value), nil
}

func (ds *DistributedStorage) Lock(key string) error {
	s, err := concurrency.NewSession(ds.client, concurrency.WithTTL(10))
	if err != nil {
		return err
	}
	defer s.Close()
	m := concurrency.NewMutex(s, key)
	if err := m.Lock(context.TODO()); err != nil {
		return err
	}
	return nil
}

func (ds *DistributedStorage) Unlock(key string) error {
	s, err := concurrency.NewSession(ds.client, concurrency.WithTTL(10))
	if err != nil {
		return err
	}
	defer s.Close()
	m := concurrency.NewMutex(s, key)
	if err := m.Unlock(context.TODO()); err != nil {
		return err
	}
	return nil
}

func main() {
	endpoints := []string{"localhost:2379"}
	ds, err := NewDistributedStorage(endpoints)
	if err != nil {
		log.Fatal(err)
	}
	err = ds.Put("key", "value")
	if err != nil {
		log.Fatal(err)
	}
	value, err := ds.Get("key")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(value)
	err = ds.Lock("lock")
	if err != nil {
		log.Fatal(err)
	}
	err = ds.Unlock("lock")
	if err != nil {
		log.Fatal(err)
	}
}
