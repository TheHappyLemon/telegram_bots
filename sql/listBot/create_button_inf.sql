CREATE TABLE BUTTON_INF (
  btn_id INT PRIMARY KEY,
  label VARCHAR(255),
  command VARCHAR(4096),
  status_inp VARCHAR(4096),
  status_out VARCHAR(4096),
  onlyData TINYINT
);
