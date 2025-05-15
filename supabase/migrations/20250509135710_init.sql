
-- ENUMs
CREATE TYPE urgency_status AS ENUM ('normal', 'mendesak');
CREATE TYPE payment_type AS ENUM ('bank_transfer', 'gopay', 'shopeepay', 'qris', 'credit_card', 'indomaret', 'alfamart');
CREATE TYPE campaign_status AS ENUM ('pending', 'approved', 'completed', 'rejected');
CREATE TYPE donation_status AS ENUM ('pending', 'paid', 'failed');
CREATE TYPE withdrawal_status AS ENUM ('pending', 'approved', 'completed', 'rejected');
CREATE TYPE transaction_status AS ENUM ('pending', 'settlement', 'cancel', 'expire');

-- Campaign types as separate table
CREATE TABLE campaign_types (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  nik TEXT,
  prodi TEXT,
  name TEXT,
  email TEXT,
  role TEXT,
  photo_url TEXT,
  total_donation INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT now()
);

-- Campaigns
CREATE TABLE campaigns (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  type_id INT REFERENCES campaign_types(id),
  image_url TEXT,
  target_amount NUMERIC NOT NULL,
  current_amount NUMERIC DEFAULT 0,
  status campaign_status DEFAULT 'pending',
  is_urgent urgency_status DEFAULT 'normal',
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT now()
);

-- Donations
CREATE TABLE donations (
  id SERIAL PRIMARY KEY,
  campaign_id INT REFERENCES campaigns(id),
  donor UUID REFERENCES users(id),
  amount NUMERIC NOT NULL,
  is_anonymous BOOLEAN DEFAULT FALSE,
  message TEXT,
  status donation_status DEFAULT 'pending',
  payment_id TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- Transactions
CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  order_id TEXT UNIQUE NOT NULL,
  donor_id UUID REFERENCES users(id),
  campaign_id INT REFERENCES campaigns(id),
  amount NUMERIC NOT NULL,
  payment_type payment_type,
  transaction_status transaction_status DEFAULT 'pending',
  transaction_time TIMESTAMP DEFAULT now(),
  settlement_time TIMESTAMP,
  va_numbers TEXT,
  fraud_status TEXT
);

-- Fund Withdrawals
CREATE TABLE fund_withdrawals (
  id SERIAL PRIMARY KEY,
  campaign_id INT REFERENCES campaigns(id),
  amount NUMERIC NOT NULL,
  withdrawal_date TIMESTAMP DEFAULT now(),
  created_by UUID REFERENCES users(id),
  status withdrawal_status DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT now()
);

-- Applications (permohonan bantuan)
CREATE TABLE applications (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  title TEXT,
  description TEXT,
  supporting_docs TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT now()
);
