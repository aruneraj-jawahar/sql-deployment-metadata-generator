/*
deployment_group: CUSTOMER_DATA
sequence: 20
*/

INSERT INTO customer_hub (
    customer_id,
    customer_name,
    record_source,
    load_date
)
SELECT
    customer_id,
    customer_name,
    record_source,
    CURRENT_TIMESTAMP
FROM customer_source;
