DROP TABLE IF EXISTS timer;

CREATE TABLE timer (
  elapsedTime TIMESTAMP NOT NULL,
  lastEndpointUsed VARCHAR(30) NOT NULL
);
