CREATE TABLE task_parameter_numeric (
	ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	TASK_ID INTEGER NOT NULL,
	PARAMETER_ID INTEGER NOT NULL,
	VALUE REAL NOT NULL,
	LSL REAL,
	USL REAL
);