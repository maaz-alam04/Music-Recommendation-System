import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet; // Import ResultSet class
import java.sql.SQLException;
import java.util.Scanner;

public class EventManagementSystem {

    private static final String URL = "jdbc:mysql://localhost:3306/event_management";
    private static final String USER = "root";
    private static final String PASSWORD = "";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Welcome to Event Management System");
        while (true) {
            System.out.println("\nSelect an option:");
            System.out.println("1. Add User");
            System.out.println("2. Add Event");
            System.out.println("3. Make Reservation");
            System.out.println("4. List Events");
            System.out.println("5. Exit");

            int choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline character
            
            switch (choice) {
                case 1:
                    addUser(scanner);
                    break;
                case 2:
                    addEvent(scanner);
                    break;
                case 3:
                    makeReservation(scanner);
                    break;
                case 4:
                    listEvents();
                    break;
                case 5:
                    System.out.println("Exiting...");
                    scanner.close();
                    return;
                default:
                    System.out.println("Invalid option. Please choose again.");
            }
        }
    }

    private static void addUser(Scanner scanner) {
        System.out.println("Enter user ID:");
        int userId = scanner.nextInt();
        scanner.nextLine(); // Consume newline character

        System.out.println("Enter user name:");
        String name = scanner.nextLine();
        
        System.out.println("Enter user email:");
        String email = scanner.nextLine();
        
        String sql = "INSERT INTO users (user_id, name, email) VALUES (?, ?, ?)";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, userId);
            pstmt.setString(2, name);
            pstmt.setString(3, email);
            int rowsAffected = pstmt.executeUpdate();
            
            if (rowsAffected > 0) {
                System.out.println("User added successfully!");
            } else {
                System.out.println("Failed to add user.");
            }
        } catch (SQLException e) {
            System.out.println("Error adding user: " + e.getMessage());
        }
    }

    private static void addEvent(Scanner scanner) {
        System.out.println("Enter event ID:");
        int eventId = scanner.nextInt();
        scanner.nextLine(); // Consume newline character
        
        System.out.println("Enter event name:");
        String eventName = scanner.nextLine();
        
        System.out.println("Enter event date (YYYY-MM-DD):");
        String eventDate = scanner.nextLine();
        
        System.out.println("Enter event location:");
        String location = scanner.nextLine();
        
        String sql = "INSERT INTO events (event_id, event_name, event_date, location) VALUES (?, ?, ?, ?)";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, eventId);
            pstmt.setString(2, eventName);
            pstmt.setString(3, eventDate);
            pstmt.setString(4, location);
            
            int rowsAffected = pstmt.executeUpdate();
            if (rowsAffected > 0) {
                System.out.println("Event added successfully!");
            } else {
                System.out.println("Failed to add event.");
            }
        } catch (SQLException e) {
            System.out.println("Error adding event: " + e.getMessage());
        }
    }

    private static void makeReservation(Scanner scanner) {
        System.out.println("Enter user ID for reservation:");
        int userId = scanner.nextInt();
        scanner.nextLine(); // Consume newline character
        
        System.out.println("Enter event ID:");
        int eventId = scanner.nextInt();
        scanner.nextLine(); // Consume newline character
        
        System.out.println("Enter reservation date (YYYY-MM-DD):");
        String reservationDate = scanner.nextLine();
        
        String sql = "INSERT INTO reservations (user_id, event_id, reservation_date) VALUES (?, ?, ?)";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, userId);
            pstmt.setInt(2, eventId);
            pstmt.setString(3, reservationDate);
            
            int rowsAffected = pstmt.executeUpdate();
            if (rowsAffected > 0) {
                System.out.println("Reservation made successfully!");
            } else {
                System.out.println("Failed to make reservation.");
            }
        } catch (SQLException e) {
            System.out.println("Error making reservation: " + e.getMessage());
        }
    }

    private static void listEvents() {
        String sql = "SELECT * FROM events";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement pstmt = conn.prepareStatement(sql);
             ResultSet rs = pstmt.executeQuery()) {
            System.out.println("List of Events:");
            while (rs.next()) {
                System.out.println("Event ID: " + rs.getInt("event_id"));
                System.out.println("Event Name: " + rs.getString("event_name"));
                System.out.println("Event Date: " + rs.getString("event_date"));
                System.out.println("Location: " + rs.getString("location"));
                System.out.println("---------------------------");
            }
        } catch (SQLException e) {
            System.out.println("Error listing events: " + e.getMessage());
        }
    }
}
					




