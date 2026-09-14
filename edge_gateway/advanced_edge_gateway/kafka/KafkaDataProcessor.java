import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Collections;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

public class KafkaDataProcessor {
    private static final Logger logger = Logger.getLogger(KafkaDataProcessor.class.getName());
    private KafkaConsumer<String, String> consumer;
    private KafkaProducer<String, String> producer;
    private String inputTopic;
    private String outputTopic;

    public KafkaDataProcessor(String configFile) {
        loadConfig(configFile);
        setupConsumer();
        setupProducer();
    }

    private void loadConfig(String configFile) {
        Properties properties = new Properties();
        try (InputStream input = new FileInputStream(configFile)) {
            properties.load(input);
            inputTopic = properties.getProperty("input.topic");
            outputTopic = properties.getProperty("output.topic");
            logger.info("Configuration loaded successfully.");
        } catch (IOException e) {
            logger.log(Level.SEVERE, "Error loading configuration file: " + e.getMessage(), e);
        }
    }

    private void setupConsumer() {
        Properties consumerProps = new Properties();
        consumerProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        consumerProps.put(ConsumerConfig.GROUP_ID_CONFIG, "data-processor-group");
        consumerProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        consumerProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        consumer = new KafkaConsumer<>(consumerProps);
        consumer.subscribe(Collections.singletonList(inputTopic));
        logger.info("Consumer set up and subscribed to topic: " + inputTopic);
    }

    private void setupProducer() {
        Properties producerProps = new Properties();
        producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        producerProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        producerProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        producer = new KafkaProducer<>(producerProps);
        logger.info("Producer set up for topic: " + outputTopic);
    }

    public void processMessages() {
        try {
            while (true) {
                var records = consumer.poll(100);
                for (ConsumerRecord<String, String> record : records) {
                    logger.info("Received message: " + record.value());
                    // Process the message (this is where your processing logic goes)
                    String processedMessage = processMessage(record.value());
                    // Send the processed message to the output topic
                    producer.send(new ProducerRecord<>(outputTopic, processedMessage));
                    logger.info("Sent processed message: " + processedMessage);
                }
            }
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Error processing messages: " + e.getMessage(), e);
        } finally {
            consumer.close();
            producer.close();
            logger.info("Consumer and producer closed.");
        }
    }

    private String processMessage(String message) {
        // Implement your message processing logic here
        return message.toUpperCase(); // Example processing: convert to uppercase
    }

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Please provide the configuration file path.");
            System.exit(1);
        }
        KafkaDataProcessor processor = new KafkaDataProcessor(args[0]);
        processor.processMessages();
    }
    }
