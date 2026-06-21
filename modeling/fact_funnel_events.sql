CREATE TABLE fact_funnel_events (

    event_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    customer_key INT NOT NULL,

    date_key INT NOT NULL,

    device_key INT NOT NULL,

    channel_key INT NOT NULL,

    stage_order INT NOT NULL,

    converted_paid INT NOT NULL,

    reached_trial INT NOT NULL,

    monthly_revenue DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key),

    CONSTRAINT fk_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT fk_device
        FOREIGN KEY (device_key)
        REFERENCES dim_device(device_key),

    CONSTRAINT fk_channel
        FOREIGN KEY (channel_key)
        REFERENCES dim_channel(channel_key)

);