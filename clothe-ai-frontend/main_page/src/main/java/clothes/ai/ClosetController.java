package clothes.ai;

import java.io.IOException;

import javafx.fxml.FXML;
import javafx.scene.control.Label;

public class ClosetController {
    @FXML private Label messageLabel;
    
    @FXML
    private void handleBack() {
        try {
            App.setRoot("primary");
        } catch (IOException e) {
            messageLabel.setText("Error navigating back: " + e.getMessage());
        }
    }    
}
