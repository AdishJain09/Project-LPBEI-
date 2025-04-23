<?php
// Connect to the database
include 'db_connect.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = $_POST['email'];
    $password = $_POST['password'];
    $email = $conn->real_escape_string($email);

    echo "Email submitted: " . $email . "<br>";
    echo "Password submitted: " . $password . "<br>";

    $sql = "SELECT id, email, password FROM users WHERE email = '$email'";
    $result = $conn->query($sql);

    echo "Number of rows found: " . $result->num_rows . "<br>";

    if ($result && $result->num_rows === 1) {
        $user = $result->fetch_assoc();
        echo "User data: ";
        var_dump($user);
        echo "<br>";

        $password_match = password_verify($password, $user['password']);
        echo "Password match: ";
        var_dump($password_match);
        echo "<br>";

        if ($password_match) {
            session_start();
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['email'] = $user['email'];
            echo "Session started. Redirecting to dashboard.php<br>";
            header('Location: dashboard.php');
            exit();
        } else {
            $error_message = "Invalid password!";
            echo "Error: " . $error_message . "<br>";
        }
    } else {
        $error_message = "No account found with this email!";
        echo "Error: " . $error_message . "<br>";
    }

    $conn->close();
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login / Sign In</title>
    <link rel="stylesheet" href="logincs.css">
</head>
<body>
    <div class="login-container">
        <img src="ChatGPT Image Apr 2, 2025, 01_17_05 PM.png" alt="TicketBazar Logo">

        <h2>Login</h2>
        <form action="login.php" method="post">
            <input type="text" name="email" placeholder="Email" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
        <?php
        if (isset($error_message)) {
            echo "<p style='color: red;'>$error_message</p>";
        }
        ?>

        <p>Don't have an account? <a href="#">Sign Up</a></p>
    </div>
    <script src="login.js"></script>
</body>
</html>