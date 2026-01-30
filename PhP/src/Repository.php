<?php
class Repository
{
    private array $customers = [];
    private int $nextId = 1;

    public function listCustomers(): array
    {
        return $this->customers;
    }

    public function createCustomer(string $name): array
    {
        $customer = [
            'id' => $this->nextId,
            'name' => $name,
            'created_at' => gmdate('c'),
        ];

        $this->customers[] = $customer;
        $this->nextId += 1;

        return $customer;
    }

    public function findCustomerByName(string $name): ?array
    {
        $needle = strtolower($name);
        foreach ($this->customers as $customer) {
            if (strtolower($customer['name']) === $needle) {
                return $customer;
            }
        }
        return null;
    }
}
