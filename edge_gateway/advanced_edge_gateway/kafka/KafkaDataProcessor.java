// edge_gateway/kafka/KafkaDataProcessor.java
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

public class KafkaDataProcessor {
    private KafkaConsumer<String, String> consumer;
    private KafkaProducer<String, String> producer;

    public KafkaDataProcessor(String bootstrapServers, String groupId) {
        Properties props = new Properties();
        props.put("bootstrap.servers", bootstrapServers);
        props.put("group.id", groupId);
        props.put("key.deserializer", StringDeserializer.class.getName());
        props.put("value.deserializer", StringDeserializer.class.getName());

        consumer = new KafkaConsumer<>(props);
        producer = new KafkaProducer<>(props);
    }

    public void processMessage(String topic, String message) {
        // Process message using Apache Flink or Apache Spark
        // ...

        // Produce processed message to another topic
        producer.send(new ProducerRecord<>(topic + "-processed", message));
    }

    public void subscribeToTopic(String topic) {
        consumer.subscribe(Collections.singleton(topic));
    }

    public void startConsuming() {
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(100);
            for (ConsumerRecord<String, String> record : records) {
                processMessage(record.topic(), record.value());
            }
        }
    }
}
