package clothes.ai;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;
import java.util.concurrent.CompletableFuture;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;

public class SecondaryController {

    @FXML private Label userLabel;
    @FXML private TextField garmentInput;
    @FXML private TextArea resultArea;

    private static final String BACKEND_URL = "http://localhost:8000";

    @FXML
    private void initialize() {
        // This is now just an alternate view, no login required
    }

    @FXML
    private void handleAnalyze() {
        String text = garmentInput.getText();
        if (text == null || text.isBlank()) {
            resultArea.setText("Please enter a clothing description first.");
            return;
        }

        resultArea.setText("Analyzing...");
        callBackend("/api/outfits/analyze", text);
    }

    @FXML
    private void handleFindIdeas() {
        String text = garmentInput.getText();
        if (text == null || text.isBlank()) {
            resultArea.setText("Please enter a clothing description first.");
            return;
        }

        resultArea.setText("Finding outfit ideas...");
        callBackend("/api/outfits/find-ideas", text);
    }

    @FXML
    private void handleListGarments() {
        String text = garmentInput.getText();
        if (text == null || text.isBlank()) {
            resultArea.setText("Please enter a type of garment first.");
            return;
        }

        resultArea.setText("Listing garments...");
        callBackend("/api/garments/", text);
    }

    @FXML
    private void handleAddGarment() {
        String garment = garmentInput.getText();
        if (garment == null || garment.isBlank()) {
            resultArea.setText("Please enter a type of garment first.");
            return;
        }

        resultArea.setText("Adding garment...");
        callBackend("/api/garments/{garment_id}", garment);
    }

    private void callBackend(String endpoint, String text) {
        CompletableFuture.runAsync(() -> {
            try {
                URL url = URI.create(BACKEND_URL + endpoint).toURL();
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);

                // Create request JSON
                String json = String.format(
                    "{\"userId\": \"guest\", \"text\": \"%s\"}", 
                    text.replace("\"", "\\\"") // Escape quotes in input
                );

                // Send request
                try (OutputStream os = conn.getOutputStream()) {
                    os.write(json.getBytes(StandardCharsets.UTF_8));
                }

                // Read response
                String response;
                try (Scanner s = new Scanner(conn.getInputStream()).useDelimiter("\\A")) {
                    response = s.hasNext() ? s.next() : "";
                }

                // Extract the relevant part from response JSON
                String result = "";
                if (endpoint.endsWith("/analyze")) {
                    // For analyze endpoint, show parsed attributes
                    if (response.contains("\"parsed\":")) {
                        result = response.substring(response.indexOf("\"parsed\":"))
                                      .replaceAll(".*\\{|\\}.*", "") // Keep just the parsed object content
                                      .replace("\"", "")
                                      .replace(",", "\n")
                                      .replace(":", ": ");
                    }
                } else {
                    // For find-ideas endpoint, show the idea text
                    if (response.contains("\"idea\":")) {
                        result = response.substring(response.indexOf("\"idea\":"))
                                      .replaceAll(".*\"idea\":\\s*\"(.+?)\".*", "$1")
                                      .replace("\\n", "\n");
                    }
                }

                final String displayText = result.isEmpty() ? 
                    "Error: Unexpected response format" : result;

                Platform.runLater(() -> resultArea.setText(displayText));

            } catch (Exception e) {
                Platform.runLater(() -> resultArea.setText(
                    "Error connecting to backend:\n" + e.getMessage() + 
                    "\n\nMake sure the backend is running at " + BACKEND_URL));
            }
        });
    }
}