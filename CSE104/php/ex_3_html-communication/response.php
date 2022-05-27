<!DOCTYPE html>

<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title> PHP Response </title>
</head>

<body>

<h1> PHP response file </h1>

<?php
$name = $_GET['Name'];
$surname = $_GET['Surname'];
print "<p>Hello $name $surname</p>";
?>

</body>

</html>