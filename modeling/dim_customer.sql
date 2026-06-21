CREATE TABLE dim_customer (

    customer_key INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id VARCHAR(50) NOT NULL,

    country VARCHAR(100),

    plan VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);