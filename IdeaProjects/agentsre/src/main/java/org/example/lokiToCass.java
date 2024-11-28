package org.example;
import io.github.cdimascio.dotenv.Dotenv;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.UUID; // Import the UUID class
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.apache.flink.shaded.zookeeper3.org.apache.zookeeper.server.admin.Commands;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;
import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.PreparedStatement;
import com.datastax.driver.core.Session;
import org.apache.flink.streaming.api.functions.source.RichSourceFunction;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.concurrent.TimeUnit;

public class lokiToCass {
    private static final Logger LOG = LoggerFactory.getLogger(lokiToCass.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final Dotenv dotenv = Dotenv.load();

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<String> stream = env.addSource(new LokiSourceFunction(), "Loki Source").uid("loki-source-id");

        // Print data received from Loki
        stream.map(value -> {
            System.out.println("Received from Loki: " + value);
            return value;
        });

        stream.addSink(new CassandraSinkFunction()).uid("Cassandra Sink");
        System.out.println("cassandraSinkFunction called");
        env.execute("Flink Loki to Cassandra");
    }

    public static class LokiSourceFunction extends RichSourceFunction<String> {
        private transient HttpClient httpClient;
        private transient HttpRequest httpRequest;
        private transient String lokiUrl;
        private transient String query;
        private transient long fetchInterval;

        @Override
        public void open(Configuration parameters) throws Exception {
            LOG.info("Initializing Loki source function...");
            System.out.println("Initializing Loki source function...");

            lokiUrl = dotenv.get("LOKI_URL");
            query = dotenv.get("QUERY");
            fetchInterval = Long.parseLong(dotenv.get("FETCH_INTERVAL"));

            httpClient = HttpClient.newHttpClient();
        }

        @Override
        public void run(SourceContext<String> ctx) throws Exception {
            while (true) {
                long endTime = System.currentTimeMillis();
                long startTime = endTime - fetchInterval;

                String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8);
                String url = lokiUrl + "?query=" + encodedQuery + "&start=" + (startTime / 1000) + "&end=" + (endTime / 1000) + "&step=1&limit=5000";

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(url))
                        .timeout(Duration.ofSeconds(10))
                        .GET()
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

                if (response.statusCode() == 200) {
                    String responseBody = response.body();
                    ctx.collect(responseBody);
                } else {
                    LOG.error("Error fetching data from Loki: {}", response.statusCode());
                }

                TimeUnit.MILLISECONDS.sleep(fetchInterval);
            }
        }

        @Override
        public void cancel() {
            // Cancel the HTTP client
            httpClient = null;
        }
    }

    public static class CassandraSinkFunction extends RichSinkFunction<String> {
        private transient Cluster cluster;
        private transient Session session;
        private transient PreparedStatement statement;

        @Override
        public void open(Configuration parameters) throws Exception {
            LOG.info("Establishing connection to Cassandra...");
            System.out.println("Establishing connection to Cassandra...");

            String cassandraHost = dotenv.get("CASSANDRA_HOST");
            int cassandraPort = Integer.parseInt(dotenv.get("CASSANDRA_PORT"));
            String cassandraUsername = dotenv.get("CASSANDRA_USERNAME");
            String cassandraPassword = dotenv.get("CASSANDRA_PASSWORD");
            String cassandraKeyspace = dotenv.get("CASSANDRA_KEYSPACE");
            String cassandraTable = dotenv.get("CASSANDRA_TABLE");

            cluster = Cluster.builder()
                    .addContactPoint(cassandraHost)
                    .withCredentials(cassandraUsername, cassandraPassword)
                    .withPort(cassandraPort)
                    .build();
            session = cluster.connect(cassandraKeyspace);
            statement = session.prepare("INSERT INTO " + cassandraTable + " (id, log_level, timestamp, message, app , container, namespace, filename, stream) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
            LOG.info("Connection to Cassandra established.");
        }

        @Override
        public void invoke(String value, Context context) {
            System.out.println("Processing in CassandraSinkFunction: " + value);
            try {
                JsonNode jsonNode = objectMapper.readTree(value);

                JsonNode result = jsonNode.get("data").get("result");
                if (result.isArray()) {
                    for (JsonNode stream : result) {
                        JsonNode values = stream.get("values");
                        if (values.isArray()) {
                            for (JsonNode valueNode : values) {
                                long timestampNs = Long.parseLong(valueNode.get(0).asText());
                                long timestampSec = timestampNs / 1_000_000_000; // Convert to seconds
                                Date timestampReal = new Date(timestampSec * 1000); // Convert to milliseconds

                                String msg = valueNode.get(1).asText();

                                String streamName = stream.get("stream").get("stream").asText();
                                String appName = stream.get("stream").get("app").asText();
                                String containerName = stream.get("stream").get("container").asText();
                                String filename = stream.get("stream").get("filename").asText();
                                String namespace = stream.get("stream").get("namespace").asText();

                                String level = streamName.equals("stderr") ? "ERROR" : "INFO";

                                LOG.info("Parsed values - Level: {}, Msg: {}, Timestamp: {}, Stream: {}, app: {}, container: {}, filename: {}, namespace: {}", level, msg, timestampReal, streamName, appName, containerName, filename, namespace);

                                // Generate a new UUID for the id field
                                UUID id = UUID.randomUUID();

                                // Insert into Cassandra
                                session.execute(statement.bind(id, level, timestampReal, msg, appName, containerName, namespace, filename, streamName));
                                // If the log level is ERROR, send an alert
                                if ("ERROR".equals(level)) {
                                //   sendTeamsAlert(msg, timestampReal);  // Send Teams alert
                                    sendAlertToAgent(msg, timestampReal);
                                }
                            }
                        }
                    }
                }
            } catch (JsonProcessingException e) {
                LOG.error("Failed to parse JSON log: {}", value, e);
            } catch (Exception e) {
                LOG.error("Error processing log: {}", value, e);
            }
        }

        @Override
        public void close() throws Exception {
            if (session != null) {
                session.close();
            }
            if (cluster != null) {
                cluster.close();
            }
        }

        private void sendTeamsAlert(String message, Date timestamp) { //adaptive card
            // Format the message for Teams (JSON)
            String payload = String.format("{\"@type\": \"MessageCard\", \"@context\": \"http://schema.org/extensions\", " +
                            "\"themeColor\": \"FF0000\", \"title\": \"*Error Alert*\", \"text\": \"Message: %s\\nTimestamp: %s\"}",
                    message, DateTimeFormatter.ISO_INSTANT.format(timestamp.toInstant()));

            try {
                String teamsWebhookUrl = dotenv.get("TEAMS_WEBHOOK_URL");  // Teams webhook URL
                HttpClient httpClient = HttpClient.newHttpClient();
                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(teamsWebhookUrl))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(payload))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

                if (response.statusCode() != 200) {
                    LOG.error("Failed to send Teams alert: {}", response.body());
                }
            } catch (Exception e) {
                LOG.error("Error sending Teams alert", e);
            }
        }
        private void sendAlertToAgent(String message, Date timestamp) {
            try {
                String agentUrl = dotenv.get("AGENT_URL");

                // Create the string payload with message and timestamp
                String payload = String.format("Message: %s\nTimestamp: %s", message, DateTimeFormatter.ISO_INSTANT.format(timestamp.toInstant()));
               // String payload = String.format("Message: %s\nTimestamp: %s", message, DateTimeFormatter.ISO_INSTANT.format(timestamp.toInstant()));

                String jsonPayload2 = String.format(
                        "{\"message\": \"%s\", \"timestamp\": \"%s\"}",
                        message,
                        DateTimeFormatter.ISO_INSTANT.format(timestamp.toInstant())
                );

                // Log the payload to ensure it's correct
                LOG.info("Sending alert to agent with payload: {}", payload);

                // Send the request with the string payload
                HttpClient httpClient = HttpClient.newHttpClient();
                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(agentUrl + "/alert"))
                        .version(HttpClient.Version.HTTP_1_1)
                        .header("Content-Type", "application/json")  // Set the content type to plain text
//                        .POST(HttpRequest.BodyPublishers.ofString(payload))  // Sending string payload
                        .POST(HttpRequest.BodyPublishers.ofString(jsonPayload2))  // Sending string payload
                        .build();
                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

                // Create the request with the JSON payload
//                HttpRequest request = HttpRequest.newBuilder()
//                        .uri(URI.create("http://127.0.0.1:8000/alert"))  // Replace with actual server URL
//                        .version(HttpClient.Version.HTTP_1_1)
//                        .header("Content-Type", "application/json")  // Set the content type to JSON
//                        .POST(HttpRequest.BodyPublishers.ofString(jsonPayload2))  // Send the JSON payload
//                        .build();
//
//                // Send the request and capture the response
//                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                // Check the response status
                if (response.statusCode() == 200) {
                    LOG.info("Successfully sent alert to the agent: {}", response.body());
                } else {
                    LOG.error("Failed to send alert to the agent. Status code: {}, Response: {}",
                            response.statusCode(), response.body());
                }
            } catch (Exception e) {
                LOG.error("Error sending alert to the agent", e);
            }
        }
    }
}