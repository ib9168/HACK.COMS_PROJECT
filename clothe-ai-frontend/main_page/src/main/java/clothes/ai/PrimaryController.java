package clothes.ai;

import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;
import java.util.concurrent.CompletableFuture;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;

public class PrimaryController {

    @FXML private TextField garmentInput;
    @FXML private TextArea resultArea;

    private static final String BACKEND_URL = "http://127.0.0.1:8000";  // Changed to default FastAPI port

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
    private void handleOpenLogin() {
        try {
            App.setRoot("login");
        } catch (IOException e) {
            // show a brief message in the result area if navigation fails
            resultArea.setText("Error opening login page: " + e.getMessage());
        }
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
                String json = String.format("{\"userId\": \"user\", \"text\": \"%s\"}", 
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

                // Extract the idea text from response JSON
                String result = "";
                if (response.contains("\"idea\":")) {
                    result = response.substring(response.indexOf("\"idea\":"))
                                  .replaceAll(".*\"idea\":\\s*\"(.+?)\".*", "$1")
                                  .replace("\\n", "\n");
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
