/*
deployment_group: CUSTOMER_DATA
sequence: 10
*/

CREATE TABLE customer_hub (
    customer_id BIGINT,
    customer_name VARCHAR(100),
    record_source VARCHAR(50),
    load_date TIMESTAMP
);
