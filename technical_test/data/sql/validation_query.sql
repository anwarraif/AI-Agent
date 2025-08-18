select * from id_jk
limit 1;

-- 1. Total kasus Maret 2020
SELECT SUM(new_confirmed) AS total_kasus
FROM id_jk
WHERE TO_DATE("date", 'MM/DD/YYYY') 
      BETWEEN '2020-03-01' AND '2020-03-31';

     
-- 2. Total kematian baru akibat Covid di Jakarta pada bulan august 2021
SELECT SUM(new_deceased)
FROM id_jk
WHERE EXTRACT(MONTH FROM TO_DATE(date, 'MM/DD/YYYY')) = 8
  AND EXTRACT(YEAR FROM TO_DATE(date, 'MM/DD/YYYY')) = 2021;
     
-- 3. Rata-rata kasus baru per hari pada April 2020
SELECT AVG(new_confirmed) AS rata2_kasus_baru
FROM id_jk
WHERE TO_DATE("date", 'MM/DD/YYYY') 
      BETWEEN '2020-04-01' AND '2020-04-30';
     
-- 4. Jumlah kasus harian tertinggi (max new_confirmed) + tanggalnya
SELECT "date", MAX(COALESCE(new_confirmed, 0)) AS max_kasus_baru
FROM id_jk
GROUP BY "date"
ORDER BY max_kasus_baru DESC
LIMIT 1;
--2/6/2022	15825

SELECT SUM(new_confirmed) AS total_kasus
FROM id_jk
WHERE TO_DATE(date, 'MM/DD/YYYY') BETWEEN '2021-07-01' AND '2021-07-31';

SELECT SUM(new_confirmed)
FROM id_jk
WHERE TO_DATE(date, 'MM/DD/YYYY')
BETWEEN TO_DATE('07/01/2021','MM/DD/YYYY') AND TO_DATE('07/31/2021','MM/DD/YYYY');

-- Kasus baru, kematian baru, dan curah hujan rata-rata pada bulan tertentu
SELECT 
    SUM(new_confirmed) AS total_kasus,
    SUM(new_deceased) AS total_kematian,
    AVG(rainfall_mm) AS rata_rainfall
FROM id_jk
WHERE EXTRACT(MONTH FROM TO_DATE(date, 'MM/DD/YYYY')) = 8
  AND EXTRACT(YEAR FROM TO_DATE(date, 'MM/DD/YYYY')) = 2021;
