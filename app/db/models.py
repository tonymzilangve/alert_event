drop_table_query = """
DROP TABLE IF EXISTS alert_messages
"""


create_table_query = """
CREATE TABLE IF NOT EXISTS alert_messages (
    uuid UUID,
    ts DateTime,
    type Enum('user' = 1, 'device' = 2, 'system' = 3),
    severity Enum('critical' = 1, 'warning' = 2, 'info' = 3),
    message String,
    source String,
    payload String,
    acknowledged Boolean DEFAULT false
) ENGINE = MergeTree()
ORDER BY ts
"""
