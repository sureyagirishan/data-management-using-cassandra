# Data Management Using Cassandra

A comprehensive guide and implementation for managing data using Apache Cassandra, a highly scalable and distributed NoSQL database system.

## Overview

This project demonstrates data management operations using Apache Cassandra, including connecting to a Cassandra cluster, creating keyspaces and tables, and performing CRUD (Create, Read, Update, Delete) operations. Cassandra is designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure.

## What is Apache Cassandra?

Apache Cassandra is a free and open-source, distributed, wide-column store, NoSQL database management system designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure.

### Key Features:

- **Distributed Architecture**: Data is automatically distributed across multiple nodes
- **High Availability**: No single point of failure with peer-to-peer architecture
- **Linear Scalability**: Add more nodes to increase throughput linearly
- **Fault Tolerance**: Data is replicated across multiple nodes
- **Tunable Consistency**: Choose between consistency and availability
- **Fast Writes**: Optimized for write-heavy workloads

## Basic Concepts

### Keyspace
A keyspace in Cassandra is similar to a database in relational database systems. It defines how data is replicated across nodes.

### Column Family (Table)
A column family is similar to a table in relational databases. It contains rows and columns.

### Primary Key
Uniquely identifies each row in a table. Can be simple (single column) or composite (multiple columns).

### Partition Key
Determines which node stores the data. Important for data distribution.

### Clustering Key
Determines the order of data within a partition.

## Prerequisites

Before running this project, ensure you have the following installed:

1. **Python 3.6+**
   ```bash
   python --version
   ```

2. **Apache Cassandra** (Local installation or cloud-based like DataStax Astra)
   - Download from: https://cassandra.apache.org/download/
   - Or use Docker: `docker run --name cassandra -p 9042:9042 -d cassandra:latest`

3. **Cassandra Python Driver**
   ```bash
   pip install cassandra-driver
   ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sureyagirishan/data-management-using-cassandra.git
   cd data-management-using-cassandra
   ```

2. Install required dependencies:
   ```bash
   pip install cassandra-driver
   ```

3. Ensure Cassandra is running:
   ```bash
   # Check if Cassandra is running
   nodetool status
   ```

## Usage

### Running the Main Script

```bash
python main.py
```

This will:
1. Connect to your local Cassandra instance
2. Create a keyspace named `data_management`
3. Create a `users` table
4. Insert sample user records
5. Query and display all users
6. Query a specific user by ID

### Expected Output

```
================================================================================
Cassandra Data Management System
================================================================================
Successfully connected to Cassandra!
Keyspace 'data_management' created successfully!
Table 'users' created successfully!

Inserting sample users...
User 'john_doe' inserted successfully!
User 'jane_smith' inserted successfully!
User 'bob_wilson' inserted successfully!

Users in database:
--------------------------------------------------------------------------------
ID: 123e4567-e89b-12d3-a456-426614174000 | Username: john_doe | Email: john@example.com | Created: 2024-01-01 10:30:00
ID: 223e4567-e89b-12d3-a456-426614174001 | Username: jane_smith | Email: jane@example.com | Created: 2024-01-01 10:30:01
ID: 323e4567-e89b-12d3-a456-426614174002 | Username: bob_wilson | Email: bob@example.com | Created: 2024-01-01 10:30:02
--------------------------------------------------------------------------------

Found user: john_doe (john@example.com)

================================================================================
Data management operations completed successfully!
================================================================================

Connection closed.
```

## Project Structure

```
data-management-using-cassandra/
│
├── main.py                 # Main application script
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies (optional)
```

## Configuration

### Local Cassandra Connection
The default configuration connects to a local Cassandra instance:
```python
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
```

### Cloud-Based Cassandra (DataStax Astra)
For cloud-based Cassandra, update the connection settings:
```python
auth_provider = PlainTextAuthProvider(
    username='your_username',
    password='your_password'
)
cluster = Cluster(
    ['your_cassandra_host'],
    auth_provider=auth_provider
)
```

## Data Model

The `users` table schema:
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username TEXT,
    email TEXT,
    created_at TIMESTAMP
);
```

## Common Operations

### Insert Data
```python
query = "INSERT INTO users (user_id, username, email, created_at) VALUES (%s, %s, %s, toTimestamp(now()))"
session.execute(query, (user_id, username, email))
```

### Query Data
```python
# Query all users
rows = session.execute("SELECT * FROM users")

# Query specific user
query = "SELECT * FROM users WHERE user_id = %s"
rows = session.execute(query, (user_id,))
```

### Update Data
```python
query = "UPDATE users SET email = %s WHERE user_id = %s"
session.execute(query, (new_email, user_id))
```

### Delete Data
```python
query = "DELETE FROM users WHERE user_id = %s"
session.execute(query, (user_id,))
```

## Best Practices

1. **Design for Query Patterns**: Design your data model based on how you will query the data
2. **Avoid Hot Spots**: Distribute data evenly across partitions
3. **Use Prepared Statements**: For better performance and security
4. **Set Appropriate Replication Factor**: Balance between availability and performance
5. **Monitor Performance**: Use tools like nodetool and DataStax OpsCenter
6. **Handle Errors Gracefully**: Implement proper error handling and retry logic

## Troubleshooting

### Connection Refused
- Ensure Cassandra is running: `nodetool status`
- Check if port 9042 is open
- Verify firewall settings

### Authentication Errors
- Check username and password
- Ensure authentication is properly configured in cassandra.yaml

### Timeout Errors
- Increase connection timeout in cluster configuration
- Check network connectivity
- Verify Cassandra cluster health

## Resources

- [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/)
- [DataStax Python Driver Documentation](https://docs.datastax.com/en/developer/python-driver/)
- [Cassandra Data Modeling Best Practices](https://cassandra.apache.org/doc/latest/data_modeling/)
- [CQL (Cassandra Query Language) Reference](https://cassandra.apache.org/doc/latest/cql/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Sureya Girishan**
- GitHub: [@sureyagirishan](https://github.com/sureyagirishan)

## Acknowledgments

- Apache Cassandra Community
- DataStax for excellent documentation and resources
- Python Cassandra Driver contributors
