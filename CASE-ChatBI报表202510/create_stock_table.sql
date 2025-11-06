CREATE DATABASE IF NOT EXISTS stock_data_db;
USE stock_data_db;

CREATE TABLE stock_daily_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ts_code VARCHAR(20) NOT NULL COMMENT '股票代码',
    trade_date VARCHAR(10) NOT NULL COMMENT '交易日期',
    stock_name VARCHAR(50) NOT NULL COMMENT '股票名称',
    open DECIMAL(10, 3) NOT NULL COMMENT '开盘价',
    high DECIMAL(10, 3) NOT NULL COMMENT '最高价',
    low DECIMAL(10, 3) NOT NULL COMMENT '最低价',
    close DECIMAL(10, 3) NOT NULL COMMENT '收盘价',
    pre_close DECIMAL(10, 3) COMMENT '昨收价（除权价，前复权）',
    change DECIMAL(10, 3) COMMENT '涨跌额',
    pct_chg DECIMAL(10, 4) COMMENT '涨跌幅（基于除权昨收计算）',
    vol BIGINT COMMENT '成交量（手）',
    amount DECIMAL(20, 2) COMMENT '成交额（千元）',
    INDEX idx_trade_date (trade_date),
    INDEX idx_ts_code (ts_code),
    INDEX idx_stock_name (stock_name),
    INDEX idx_trade_stock (trade_date, ts_code)
) COMMENT='股票日线数据表';