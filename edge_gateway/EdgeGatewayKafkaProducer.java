// EdgeGatewayKafkaProducer.java
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

public class EdgeGatewayKafkaProducer {
    private static final String KAFKA_BROKERS = "localhost:9092";
    private static final String TOPIC_NAME = "edge_gateway_data";

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, KAFKA_BROKERS);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        KafkaProducer<String, String> producer = new KafkaProducer<>(props);

        // Produce data to Kafka topic
        while (true) {
            String data = generateData(); // Implement data generation logic here
            ProducerRecord<String, String> record = new ProducerRecord<>(TOPIC_NAME, data);
            producer.send(record);
            System.out.println("Sent data to Kafka topic: " + data);
        }
    }

    private static String generateData() {
        // Implement data generation logic here
        return "Sample data from Edge Gateway";
    }
}
