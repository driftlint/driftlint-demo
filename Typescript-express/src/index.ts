import express from 'express';
import { InvoiceStore } from './store';

const app = express();
const store = new InvoiceStore();

app.use(express.json());

app.get('/health', (_req, res) => {
  res.json({ status: 'ok' });
});

app.get('/invoices', (_req, res) => {
  res.json(store.list());
});

app.post('/invoices', (req, res) => {
  const { client, amountCents } = req.body ?? {};

  if (!client || typeof amountCents !== 'number') {
    res.status(400).json({ error: 'client and amountCents required' });
    return;
  }

  const duplicate = store.findRecentDuplicate(client, amountCents, 60);
  if (duplicate) {
    res.status(409).json({
      error: 'duplicate invoice created recently',
      id: duplicate.id,
    });
    return;
  }

  const invoice = store.create(client, amountCents);
  res.status(201).json(invoice);
});

const port = process.env.PORT ? Number(process.env.PORT) : 3000;
app.listen(port, () => {
  console.log(`API listening on ${port}`);
});
