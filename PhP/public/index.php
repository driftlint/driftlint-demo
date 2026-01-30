<?php
require_once __DIR__ . '/../src/Repository.php';

$repository = new Repository();

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$method = $_SERVER['REQUEST_METHOD'];

if ($path === '/health' && $method === 'GET') {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'ok']);
    exit;
}

if ($path === '/customers' && $method === 'GET') {
    header('Content-Type: application/json');
    echo json_encode($repository->listCustomers());
    exit;
}

if ($path === '/customers' && $method === 'POST') {
    $payload = json_decode(file_get_contents('php://input'), true) ?? [];
    if (!isset($payload['name'])) {
        http_response_code(400);
        echo json_encode(['error' => 'name is required']);
        exit;
    }

    $name = trim($payload['name']);
    if ($name === '') {
        http_response_code(400);
        echo json_encode(['error' => 'name cannot be empty']);
        exit;
    }

    $existing = $repository->findCustomerByName($name);
    if ($existing !== null) {
        http_response_code(409);
        echo json_encode(['error' => 'customer already exists', 'id' => $existing['id']]);
        exit;
    }

    $customer = $repository->createCustomer($name);
    header('Content-Type: application/json');
    http_response_code(201);
    echo json_encode($customer);
    exit;
}

http_response_code(404);
header('Content-Type: application/json');
echo json_encode(['error' => 'Not found']);
