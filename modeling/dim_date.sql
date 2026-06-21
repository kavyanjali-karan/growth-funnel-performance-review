CREATE TABLE dim_date (

    date_key INT PRIMARY KEY,

    full_date DATE NOT NULL,

    day_number INT,

    week_number INT,

    month_number INT,

    month_name VARCHAR(20),

    quarter_number INT,

    year_number INT

);