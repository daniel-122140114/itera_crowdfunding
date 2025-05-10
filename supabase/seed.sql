-- 1. Campaign Types
INSERT INTO campaign_types (name) VALUES 
  ('Kesehatan'),
  ('Bencana'),
  ('Pendidikan'),
  ('Lainnya');

-- 2. Users (UUID fiktif, ganti jika diperlukan)
INSERT INTO users (id, name, email, role) VALUES
  ('00000000-0000-0000-0000-000000000001', 'Andi Saputra', 'andi@itera.ac.id', 'user'),
  ('00000000-0000-0000-0000-000000000002', 'Budi Santoso', 'budi@itera.ac.id', 'user'),
  ('00000000-0000-0000-0000-000000000003', 'Citra Lestari', 'citra@itera.ac.id', 'user'),
  ('00000000-0000-0000-0000-000000000004', 'Dewi Permata', 'dewi@itera.ac.id', 'user'),
  ('00000000-0000-0000-0000-000000000005', 'Eka Pratama', 'eka@itera.ac.id', 'user'),
  ('00000000-0000-0000-0000-000000000099', 'Admin Kampus', 'admin@itera.ac.id', 'admin');

-- 3. Campaigns
INSERT INTO campaigns (title, description, type_id, image_url, target_amount, current_amount, status, is_urgent, created_by) VALUES
  ('Operasi Mahasiswa Gizi', 'Bantuan operasi patah tulang mahasiswa gizi.', 1, NULL, 8000000, 1200000, 'approved', 'mendesak', '00000000-0000-0000-0000-000000000001'),
  ('Korban Gempa Sumatera', 'Dukungan untuk warga terdampak gempa.', 2, NULL, 15000000, 6500000, 'approved', 'normal', '00000000-0000-0000-0000-000000000099'),
  ('Laptop Untuk Skripsi', 'Mahasiswa butuh laptop untuk skripsi.', 3, NULL, 6000000, 1000000, 'approved', 'mendesak', '00000000-0000-0000-0000-000000000003'),
  ('Obat untuk Anak Kost', 'Bantu mahasiswa isolasi mandiri.', 1, NULL, 3000000, 2000000, 'approved', 'normal', '00000000-0000-0000-0000-000000000002'),
  ('Banjir Lampung Tengah', 'Logistik untuk korban banjir.', 2, NULL, 12000000, 7000000, 'approved', 'mendesak', '00000000-0000-0000-0000-000000000099'),
  ('Wifi Mahasiswa Kurang Mampu', 'Subsidi wifi untuk kuliah online.', 4, NULL, 4000000, 2500000, 'approved', 'normal', '00000000-0000-0000-0000-000000000005'),
  ('Biaya Rawat Inap Gawat Darurat', 'Bantuan mendesak rawat inap mahasiswa.', 1, NULL, 10000000, 8000000, 'approved', 'mendesak', '00000000-0000-0000-0000-000000000004'),
  ('Donasi Buku Teknik Sipil', 'Pengadaan buku perpustakaan.', 3, NULL, 5000000, 1200000, 'approved', 'normal', '00000000-0000-0000-0000-000000000003'),
  ('Bantuan Yatim Mahasiswa', 'Bantuan biaya hidup mahasiswa yatim.', 1, NULL, 7000000, 2700000, 'approved', 'mendesak', '00000000-0000-0000-0000-000000000001'),
  ('Kebakaran Asrama', 'Asrama mahasiswa terbakar, butuh bantuan.', 2, NULL, 20000000, 9500000, 'approved', 'mendesak', '00000000-0000-0000-0000-000000000099');

-- 4. Donations
INSERT INTO donations (campaign_id, donor_id, amount, is_anonymous, message, status) VALUES
  (1, '00000000-0000-0000-0000-000000000099', 500000, FALSE, 'Semangat!', 'paid'),
  (2, '00000000-0000-0000-0000-000000000002', 1000000, TRUE, '', 'paid'),
  (3, '00000000-0000-0000-0000-000000000004', 750000, FALSE, 'Semoga cepat selesai skripsinya!', 'paid'),
  (4, '00000000-0000-0000-0000-000000000005', 200000, FALSE, 'Jangan menyerah!', 'paid'),
  (5, '00000000-0000-0000-0000-000000000001', 350000, TRUE, '', 'paid'),
  (6, '00000000-0000-0000-0000-000000000003', 500000, FALSE, 'Semoga membantu', 'paid'),
  (7, '00000000-0000-0000-0000-000000000099', 1500000, FALSE, 'Kami peduli.', 'paid'),
  (8, '00000000-0000-0000-0000-000000000004', 300000, FALSE, '', 'paid'),
  (9, '00000000-0000-0000-0000-000000000002', 500000, TRUE, '', 'paid'),
  (10,'00000000-0000-0000-0000-000000000005', 900000, FALSE, 'Semoga cepat pulih.', 'paid'),
  (1, '00000000-0000-0000-0000-000000000003', 600000, FALSE, '', 'paid'),
  (2, '00000000-0000-0000-0000-000000000005', 250000, TRUE, '', 'paid'),
  (3, '00000000-0000-0000-0000-000000000001', 400000, FALSE, '', 'paid'),
  (4, '00000000-0000-0000-0000-000000000002', 100000, TRUE, '', 'paid'),
  (5, '00000000-0000-0000-0000-000000000004', 500000, FALSE, 'Terus semangat!', 'paid');

-- 5. Transactions
INSERT INTO transactions (order_id, donor_id, campaign_id, amount, payment_type, transaction_status) VALUES
  ('ORD-1001', '00000000-0000-0000-0000-000000000002', 1, 500000, 'gopay', 'settlement'),
  ('ORD-1002', '00000000-0000-0000-0000-000000000004', 3, 750000, 'qris', 'settlement'),
  ('ORD-1003', '00000000-0000-0000-0000-000000000001', 5, 350000, 'shopeepay', 'settlement'),
  ('ORD-1004', '00000000-0000-0000-0000-000000000005', 900000, 'credit_card', 'settlement'),
  ('ORD-1005', '00000000-0000-0000-0000-000000000099', 1500000, 'bank_transfer', 'settlement');

-- 6. Fund Withdrawals
INSERT INTO fund_withdrawals (campaign_id, amount, created_by, status) VALUES
  (1, 3000000, '00000000-0000-0000-0000-000000000001', 'approved'),
  (5, 2000000, '00000000-0000-0000-0000-000000000099', 'approved');

-- 7. Applications (permohonan bantuan)
INSERT INTO applications (user_id, title, description, supporting_docs, status) VALUES
  ('00000000-0000-0000-0000-000000000001', 'Permohonan Biaya Operasi', 'Butuh dana untuk operasi usus buntu.', 'https://link.dokumen/1', 'pending'),
  ('00000000-0000-0000-0000-000000000004', 'Permohonan Laptop', 'Laptop rusak, butuh untuk menyelesaikan skripsi.', 'https://link.dokumen/2', 'pending');
