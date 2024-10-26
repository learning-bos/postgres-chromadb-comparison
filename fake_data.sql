create table test (
    id serial, 
    contract varchar, 
    amount0 int, 
    amount1 int, 
    price double precision
);

CREATE OR REPLACE FUNCTION random_amount()
  RETURNS int
  LANGUAGE sql VOLATILE PARALLEL SAFE AS
$func$
  SELECT ('[0:4]={50, 60, 80, 100, 200}'::int[])[trunc(random()  * (4 - 1 + 1) + 1)::int];
$func$;

CREATE OR REPLACE FUNCTION random_price()
  RETURNS int
  LANGUAGE sql VOLATILE PARALLEL SAFE AS
$func$
  (SELECT ('[0:3]={1.5, 1.8, 2.1, 2.5}'::float[])[trunc(random()  * (3 - 1 + 1) + 1)::int]);
$func$;

INSERT INTO test (amount0, amount1, price)
SELECT
  random_amount(), random_amount(), random_price()
FROM generate_series(1, 100);

select * from test;