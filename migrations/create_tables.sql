DROP TABLE IF EXISTS ships;
DROP TABLE IF EXISTS cargo;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS location_traits;
DROP TABLE IF EXISTS systems;
DROP TABLE IF EXISTS ship_types;
DROP TABLE IF EXISTS good_types;

CREATE TABLE IF NOT EXISTS ships (
  id VARCHAR(255) PRIMARY KEY,
  location VARCHAR(255),
  x INTEGER,
  y INTEGER,
  spaceAvailable INTEGER
);

CREATE TABLE IF NOT EXISTS cargo (
  ship_id VARCHAR(255),
  good VARCHAR(255),
  quantity INTEGER,
  PRIMARY KEY (ship_id, good)
);

CREATE TABLE IF NOT EXISTS locations (
  symbol VARCHAR(255) PRIMARY KEY,
  type VARCHAR(255),
  name VARCHAR(255),
  x INTEGER,
  y INTEGER,
  allowsConstruction BOOLEAN
);

CREATE TABLE IF NOT EXISTS location_traits (
  location_symbol VARCHAR(255),
  trait VARCHAR(255),
  PRIMARY KEY (location_symbol, trait)
);

CREATE TABLE IF NOT EXISTS systems (
  symbol VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS good_types (
  symbol VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) UNIQUE,
  volumePerUnit INTEGER
);

CREATE TABLE IF NOT EXISTS ship_types (
  class VARCHAR(255),
  manufacturer VARCHAR(255),
  maxCargo INTEGER,
  plating INTEGER,
  speed INTEGER,
  type VARCHAR(255) PRIMARY KEY,
  weapons INTEGER
);

