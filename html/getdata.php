<?php
header('Content-Type: application/json; charset=utf-8');

// Connexion à la base de données
$conn = new mysqli('localhost', 'pi', 'pipi', 'wifi_bl');

// Vérification de la connexion
if ($conn->connect_error) {
    die("Connexion échouée : " . $conn->connect_error);
}

$conn->set_charset("utf8"); // Définit l'encodage des résultats de la requête

// Récupération des nouvelles données à partir du fichier
$newData = array_map('str_getcsv', file('/var/lib/mysql-files/messages.csv'));

// Préparation de la requête d'insertion
$sql = "INSERT INTO donnees (timestamp, type_capteur, valeur, salle) VALUES (?, ?, ?, ?)";
$stmt = $conn->prepare($sql);

// Préparation de la requête de vérification
$checkSql = "SELECT COUNT(*) FROM donnees WHERE timestamp = ? AND type_capteur = ? AND valeur = ? AND salle = ?";
$checkStmt = $conn->prepare($checkSql);

function isNotNullOrEmptyString($value) {
    return !(is_null($value) || $value === '');
}

foreach ($newData as $row) {
    // Ignore les rangées contenant des valeurs nulles
    if (!isNotNullOrEmptyString($row[0]) || !isNotNullOrEmptyString($row[1]) || !isNotNullOrEmptyString($row[2]) || !isNotNullOrEmptyString($row[3])) {
        continue;
    }

    $checkStmt->bind_param("ssis", $row[0], $row[1], $row[2], $row[3]);
    $checkStmt->execute();
    $checkStmt->store_result();
    $checkStmt->bind_result($count);
    $checkStmt->fetch();

    // Si les données n'existent pas déjà, insérer les nouvelles données
    if ($count == 0) {
        $stmt->bind_param("ssis", $row[0], $row[1], $row[2], $row[3]);
        if ($stmt->execute() === FALSE) {
            die("Erreur lors de l'insertion des nouvelles données : " . $stmt->error);
        }
    }

    $checkStmt->free_result();
}

// Récupération des données de la table
$sql = "SELECT * FROM donnees";
$result = $conn->query($sql);

// Construction du tableau de données pour le retour
$data = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
} else {
    $data = ["message" => "Aucune donnée disponible."];
}

// Fermeture de la connexion
$conn->close();

// Renvoi du tableau de données
echo json_encode($data, JSON_UNESCAPED_UNICODE);
?>
