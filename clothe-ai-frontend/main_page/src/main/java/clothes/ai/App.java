// Source code is decompiled from a .class file using FernFlower decompiler (from Intellij IDEA).
package clothes.ai;

import java.io.IOException;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class App extends Application {
   private static Scene scene;

   public App() {
   }

   public void start(Stage stage) throws IOException {
      scene = new Scene(loadFXML("primary"), 640.0, 480.0);
      stage.setScene(scene);
      stage.show();
   }

   static void setRoot(String fxml) throws IOException {
      scene.setRoot(loadFXML(fxml));
   }

   private static Parent loadFXML(String fxml) throws IOException {
      FXMLLoader fxmlLoader = new FXMLLoader(App.class.getResource(fxml + ".fxml"));
      return (Parent)fxmlLoader.load();
   }

   public static void main(String[] args) {
      launch(new String[0]);
   }
}
