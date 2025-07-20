DROP TABLE IF EXISTS timer;

CREATE TABLE timer (
  id INTEGER NOT NULL,
  elapsedTime VARCHAR(30) NOT NULL,
  lastEndpointUsed VARCHAR(30) NOT NULL,
  memory FLOAT NOT NULL,
  threads int NOT NULL
);
