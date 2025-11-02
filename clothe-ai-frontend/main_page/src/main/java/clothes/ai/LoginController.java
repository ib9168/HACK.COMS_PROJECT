package clothes.ai;

import java.io.IOException;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;

public class LoginController {

    @FXML private TextField usernameField;
    @FXML private PasswordField passwordField;
    @FXML private Label messageLabel;

    @FXML
    private void handleLogin() {
        String u = usernameField.getText();
        String p = passwordField.getText();
        if (u == null || u.isBlank() || p == null || p.isBlank()) {
            messageLabel.setText("Please enter both username and password.");
            return;
        }

        // For now just accept any non-empty credentials and return to primary view
        messageLabel.setText("Login successful.");
        try {
            App.setRoot("primary");
        } catch (IOException e) {
            messageLabel.setText("Error loading main view: " + e.getMessage());
        }
    }

    @FXML
    private void handleBack() {
        try {
            App.setRoot("primary");
        } catch (IOException e) {
            messageLabel.setText("Error navigating back: " + e.getMessage());
        }
    }
}