import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.functions;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class PiAnalytics {
    public static void main(String[] args) {
        // Initialize SparkSession
        SparkSession spark = SparkSession.builder()
                .appName("PiAnalytics")
                .master("local[*]")
                .getOrCreate();

        // Read data from Kafka topic
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "pi-analytics");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Collections.singletonList("pi-data"));

        // Perform real-time analytics
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
            Dataset<Row> data = spark.read().json(records.records("pi-data").values());

            Dataset<Row> aggregatedData = data.groupBy(functions.window(data.col("timestamp"), "1 minute"))
                    .agg(functions.avg(data.col("value")));

            aggregatedData.write().mode("append").jdbc("jdbc:mysql://localhost:3306/pi_analytics", "aggregated_data", new Properties());
        }
    }
}
