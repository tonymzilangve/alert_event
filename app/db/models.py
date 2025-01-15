create_table_query = '''
CREATE TABLE IF NOT EXISTS messages (
    uuid UUID,
    name String,
    sensor_id String,
    description String,
    temperature Float64,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY timestamp
'''

insert_test_data = '''
INSERT INTO messages (uuid, name, sensor_id, description, temperature, timestamp)
VALUES (generateUUIDv4(), 'Passer', 'C55', 'Something went wrong!', 66.7, now())
'''
