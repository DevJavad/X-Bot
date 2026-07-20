from enum import StrEnum


class DatabaseDriver(StrEnum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"
    POSTGRESQL = "postgresql"

    MYSQL = "mysql"
    MYSQL_ASYNC = "mysql+asyncmy"
    MYSQL_AIOMYSQL = "mysql+aiomysql"

    SQLITE_AIOSQLITE = "sqlite+aiosqlite"

    POSTGRES_ASYNCPG = "postgres+asyncpg"
    POSTGRESQL_ASYNCPG = "postgresql+asyncpg"

    ORACLE = "oracle"

    MSSQL = "mssql"
    MSSQL_AIOODBC = "mssql+aioodbc"