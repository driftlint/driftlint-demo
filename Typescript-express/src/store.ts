export type Invoice = {
  id: number;
  client: string;
  amountCents: number;
  createdAt: string;
};

export class InvoiceStore {
  private invoices: Invoice[] = [];
  private nextId = 1;

  list(): Invoice[] {
    return [...this.invoices];
  }

  create(client: string, amountCents: number): Invoice {
    const invoice: Invoice = {
      id: this.nextId,
      client,
      amountCents,
      createdAt: new Date().toISOString(),
    };

    this.invoices.push(invoice);
    this.nextId += 1;
    return invoice;
  }

  findRecentDuplicate(
    client: string,
    amountCents: number,
    windowSeconds: number,
  ): Invoice | null {
    const cutoff = Date.now() - windowSeconds * 1000;
    for (const invoice of this.invoices) {
      if (invoice.client !== client || invoice.amountCents !== amountCents) {
        continue;
      }
      if (Date.parse(invoice.createdAt) >= cutoff) {
        return invoice;
      }
    }
    return null;
  }
}
