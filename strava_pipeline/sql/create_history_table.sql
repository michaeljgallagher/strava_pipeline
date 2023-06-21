CREATE TABLE start_date_history (
    id SERIAL PRIMARY KEY,
    inserted TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    last_start_date BIGINT NOT NULL
);

INSERT INTO
    start_date_history (last_start_date)
VALUES
    (946684800);