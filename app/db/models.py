drop_table_query = '''
DROP TABLE IF EXISTS alert_messages
'''


create_table_query = '''
CREATE TABLE IF NOT EXISTS alert_messages (
    uuid UUID,
    ts DateTime,
    type String,
    severity String,
    message String,
    source String,
    payload String,
    acknowledged Boolean DEFAULT false
) ENGINE = MergeTree()
ORDER BY ts
'''
