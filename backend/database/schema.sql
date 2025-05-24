-- USERS
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    registration_channel VARCHAR NOT NULL,
    channel_value TEXT,
    customer_segment VARCHAR,
    user_status VARCHAR NOT NULL CHECK (user_status IN ('active', 'inactive', 'suspended')),
    user_type VARCHAR NOT NULL CHECK (user_type IN ('group_leader', 'customer')),
    cohort_label VARCHAR,
    last_login TIMESTAMP
);

-- CATEGORIES
CREATE TABLE categories (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    status VARCHAR NOT NULL CHECK (status IN ('active', 'inactive')),
    parent_id UUID REFERENCES categories(id)
);

-- PRODUCTS
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    name_id UUID REFERENCES categories(id),
    status VARCHAR NOT NULL CHECK (status IN ('active', 'inactive', 'discontinued')),
    unit_price NUMERIC NOT NULL CHECK (unit_price >= 0)
);

-- GROUP DEALS
CREATE TABLE group_deals (
    id UUID PRIMARY KEY,
    product_id UUID REFERENCES products(id),
    max_group_member INTEGER NOT NULL CHECK (max_group_member > 0),
    group_price NUMERIC NOT NULL CHECK (group_price >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    effective_from TIMESTAMP NOT NULL,
    effective_to TIMESTAMP
);

-- GROUPS
CREATE TABLE groups (
    id UUID PRIMARY KEY,
    group_deals_id UUID REFERENCES group_deals(id),
    created_by UUID REFERENCES users(id),
    status VARCHAR NOT NULL CHECK (status IN ('open', 'completed', 'cancelled')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- ORDERS
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    groups_carts_id UUID REFERENCES groups(id),
    user_id UUID REFERENCES users(id),
    status VARCHAR NOT NULL CHECK (status IN ('pending', 'completed', 'cancelled')),
    total_amount NUMERIC NOT NULL CHECK (total_amount >= 0),
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    campaign_id UUID
);

-- ORDER ITEMS
CREATE TABLE order_items (
    id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders(id),
    product_id UUID REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price NUMERIC NOT NULL CHECK (price >= 0)
);

-- GROUP MEMBERS
CREATE TABLE group_members (
    id UUID PRIMARY KEY,
    group_id UUID REFERENCES groups(id),
    user_id UUID REFERENCES users(id),
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CAMPAIGNS
CREATE TABLE campaigns (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    channel VARCHAR NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    status VARCHAR NOT NULL CHECK (status IN ('active', 'inactive', 'completed'))
);

-- ======================
-- ✅ CREATE INDEXES
-- ======================

-- Users
CREATE INDEX ix_users_created_at ON users (created_at);
CREATE INDEX ix_users_registration_channel ON users (registration_channel);
CREATE INDEX ix_users_user_type ON users (user_type);

-- Products
CREATE INDEX ix_products_name_id ON products (name_id);
CREATE INDEX ix_products_status ON products (status);

-- Group Deals
CREATE INDEX ix_group_deals_effective_from ON group_deals (effective_from);
CREATE INDEX ix_group_deals_effective_to ON group_deals (effective_to);

-- Groups
CREATE INDEX ix_groups_created_by ON groups (created_by);
CREATE INDEX ix_groups_status ON groups (status);

-- Orders
CREATE INDEX ix_orders_order_date ON orders (order_date);
CREATE INDEX ix_orders_user_id ON orders (user_id);
CREATE INDEX ix_orders_groups_carts_id ON orders (groups_carts_id);
CREATE INDEX ix_orders_campaign_id ON orders (campaign_id);

-- Order Items
CREATE INDEX ix_order_items_order_id ON order_items (order_id);
CREATE INDEX ix_order_items_product_id ON order_items (product_id);

-- Group Members
CREATE INDEX ix_group_members_group_id ON group_members (group_id);
CREATE INDEX ix_group_members_user_id ON group_members (user_id);

-- Campaigns
CREATE INDEX ix_campaigns_start_date ON campaigns (start_date);
CREATE INDEX ix_campaigns_channel ON campaigns (channel);
CREATE INDEX ix_campaigns_status ON campaigns (status);
