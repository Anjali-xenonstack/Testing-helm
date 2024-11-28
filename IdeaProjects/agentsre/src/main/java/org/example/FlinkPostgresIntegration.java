 package org.example;

 import com.fasterxml.jackson.databind.JsonNode;
 import com.fasterxml.jackson.databind.ObjectMapper;
 import com.fasterxml.jackson.core.JsonProcessingException;
 import org.apache.flink.api.common.serialization.SimpleStringSchema;
 import org.apache.flink.streaming.api.datastream.DataStream;
 import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
 import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
 import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
 import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
 import org.apache.flink.connector.jdbc.JdbcSink;
 import org.slf4j.Logger;
 import org.slf4j.LoggerFactory;

 import java.sql.Timestamp;
 import java.time.LocalDateTime;
 import java.time.format.DateTimeFormatter;
 import java.util.Properties;

 public class FlinkPostgresIntegration {
     private static final Logger LOG = LoggerFactory.getLogger(FlinkPostgresIntegration.class);
     private static final ObjectMapper objectMapper = new ObjectMapper();

     public static void main(String[] args) throws Exception {
         final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
         Properties consumerProperties = new Properties();
         consumerProperties.setProperty("bootstrap.servers", "localhost:9092");
         consumerProperties.setProperty("group.id", "flink-group");

         FlinkKafkaConsumer<String> kafkaConsumer = new FlinkKafkaConsumer<>(
                 "raw-logs",
                 new SimpleStringSchema(),
                 consumerProperties
         );

         DataStream<String> stream = env.addSource(kafkaConsumer);

         LOG.info("Connecting to PostgreSQL with URL: jdbc:postgresql://localhost:5432/Log_AI");
         LOG.info("Using username: postgres");

         stream.addSink(JdbcSink.sink(
                 "INSERT INTO log_data (level, msg, ts, stream) VALUES (?, ?, ?, ?)",
                 (statement, log) -> {
                     try {
                         JsonNode jsonArray = objectMapper.readTree(log);

                         for (JsonNode jsonNode : jsonArray) {
                             String level = jsonNode.has("level") ? jsonNode.get("level").asText() : null;
                             String msg = jsonNode.has("msg") ? jsonNode.get("msg").asText() : null;
                             String timestampStr = jsonNode.has("ts") ? jsonNode.get("ts").asText() : null;
                             String streamName = jsonNode.has("stream") ? jsonNode.get("stream").asText() : null;

                             LOG.info("Parsed values - Level: {}, Msg: {}, Timestamp: {}, Stream: {}", level, msg, timestampStr, streamName);
                             if (level == null || msg == null || timestampStr == null || streamName == null) {
                                 LOG.warn("Missing fields in log: {}", jsonNode.toString());
                                 continue;
                             }

                             DateTimeFormatter inputFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSSSSSSSS'Z'");
                             LocalDateTime dateTime = LocalDateTime.parse(timestampStr, inputFormatter);
                             Timestamp sqlTimestamp = Timestamp.valueOf(dateTime);

                             statement.setString(1, level);
                             statement.setString(2, msg);
                             statement.setTimestamp(3, sqlTimestamp);
                             statement.setString(4, streamName);
                             statement.addBatch(); // Add to batch
                         }
                     } catch (JsonProcessingException e) {
                         LOG.error("Failed to parse JSON log: {}", log, e);
                     } catch (Exception e) {
                         LOG.error("Error processing log: {}", log, e);
                     }
                 },
                 JdbcExecutionOptions.builder()
                         .withBatchSize(1000)
                         .withBatchIntervalMs(100)
                         .withMaxRetries(5)
                         .build(),
                 new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
                         .withUrl("jdbc:postgresql://localhost:5432/Log_AI")
                         .withDriverName("org.postgresql.Driver")
                         .withUsername("postgres")
                         .withPassword("postgres")
                         .build()
         ));

         env.execute("Flink Kafka to PostgreSQL");
     }
 }