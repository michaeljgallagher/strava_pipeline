ALTER SYSTEM
SET
    timezone = 'UTC';

CREATE DATABASE strava_etl_db;

\c strava_etl_db
\i create_activities_table.sql
\i create_history_table.sql