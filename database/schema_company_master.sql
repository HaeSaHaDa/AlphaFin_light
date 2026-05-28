-- TASK-034: KOSPI200 Company Master
CREATE TABLE IF NOT EXISTS company_master (
    id           BIGINT       NOT NULL AUTO_INCREMENT,
    ticker       VARCHAR(20)  NOT NULL COMMENT '종목코드',
    company_name VARCHAR(100) NOT NULL COMMENT '기업명',
    market       VARCHAR(20)  DEFAULT 'KOSPI' COMMENT '시장',
    corp_code    VARCHAR(20)  DEFAULT NULL COMMENT 'OpenDART corp_code',
    sector       VARCHAR(100) DEFAULT NULL COMMENT '섹터',
    industry     VARCHAR(100) DEFAULT NULL COMMENT '산업',
    aliases      JSON         DEFAULT NULL COMMENT '별칭 배열',
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_company_master_ticker (ticker),
    KEY idx_company_master_name (company_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='KOSPI200 종목 마스터';
