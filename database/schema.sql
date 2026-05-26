-- ============================================================
-- AlphaFin LTE - MariaDB 초기 스키마
-- TASK-005-design-mariadb-schema
--
-- 대상 DB  : MariaDB 10.6+
-- 인코딩   : utf8mb4 / utf8mb4_unicode_ci
-- 목적     : Raw 수집 데이터 저장을 위한 최소 관계형 구조
-- ============================================================

-- 중복 실행 방지를 위해 IF NOT EXISTS 사용

-- ------------------------------------------------------------
-- 1. companies  -  기업 기본 정보
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS companies (
    id           BIGINT       NOT NULL AUTO_INCREMENT,
    ticker       VARCHAR(20)  NOT NULL COMMENT '종목코드 (예: 005930)',
    corp_code    VARCHAR(20)  DEFAULT NULL COMMENT 'OpenDART 고유 기업코드 (예: 00126380)',
    company_name VARCHAR(100) NOT NULL COMMENT '기업명',
    market       VARCHAR(20)  DEFAULT NULL COMMENT '시장 구분 (KOSPI, KOSDAQ 등)',
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_companies_ticker (ticker),
    KEY idx_companies_corp_code (corp_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='기업 기본 정보';

-- ------------------------------------------------------------
-- 2. stock_prices  -  일봉 주가 데이터
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stock_prices (
    id           BIGINT        NOT NULL AUTO_INCREMENT,
    ticker       VARCHAR(20)   NOT NULL COMMENT '종목코드',
    trade_date   DATE          NOT NULL COMMENT '거래일',
    open_price   DECIMAL(18,2) DEFAULT NULL COMMENT '시가',
    high_price   DECIMAL(18,2) DEFAULT NULL COMMENT '고가',
    low_price    DECIMAL(18,2) DEFAULT NULL COMMENT '저가',
    close_price  DECIMAL(18,2) DEFAULT NULL COMMENT '종가',
    volume       BIGINT        DEFAULT NULL COMMENT '거래량',
    change_rate  DECIMAL(10,4) DEFAULT NULL COMMENT '등락률 (%)',
    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_stock_prices_ticker_date (ticker, trade_date),
    KEY idx_stock_prices_trade_date (trade_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='일봉 주가 데이터 (pykrx OHLCV)';

-- ------------------------------------------------------------
-- 3. dart_disclosures  -  OpenDART 공시 데이터
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dart_disclosures (
    id               BIGINT       NOT NULL AUTO_INCREMENT,
    corp_code        VARCHAR(20)  NOT NULL COMMENT 'OpenDART 기업코드',
    ticker           VARCHAR(20)  DEFAULT NULL COMMENT '종목코드',
    report_name      VARCHAR(500) DEFAULT NULL COMMENT '공시 보고서명',
    receipt_no       VARCHAR(30)  DEFAULT NULL COMMENT '접수번호',
    receipt_date     DATE         DEFAULT NULL COMMENT '접수일',
    disclosure_type  VARCHAR(10)  DEFAULT NULL COMMENT '공시 구분 (A=정기, B=주요 등)',
    raw_json         LONGTEXT     DEFAULT NULL COMMENT '원본 API 응답 JSON',
    raw_file_path    VARCHAR(500) DEFAULT NULL COMMENT 'Raw 파일 저장 경로',
    created_at       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_dart_receipt_no (receipt_no),
    KEY idx_dart_corp_date (corp_code, receipt_date),
    KEY idx_dart_ticker (ticker)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='OpenDART 공시 목록';

-- ------------------------------------------------------------
-- 4. news_articles  -  뉴스 데이터
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS news_articles (
    id            BIGINT        NOT NULL AUTO_INCREMENT,
    ticker        VARCHAR(20)   DEFAULT NULL COMMENT '관련 종목코드 (nullable)',
    keyword       VARCHAR(100)  DEFAULT NULL COMMENT '검색 키워드',
    title         VARCHAR(500)  DEFAULT NULL COMMENT '기사 제목',
    content       LONGTEXT      DEFAULT NULL COMMENT '기사 본문',
    source        VARCHAR(100)  DEFAULT NULL COMMENT '언론사',
    url           VARCHAR(1000) NOT NULL COMMENT '기사 URL',
    published_at  DATETIME      DEFAULT NULL COMMENT '기사 발행 시각',
    raw_file_path VARCHAR(500)  DEFAULT NULL COMMENT 'Raw JSON 파일 저장 경로',
    created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_news_url (url(255)),
    KEY idx_news_ticker_published (ticker, published_at),
    KEY idx_news_keyword (keyword)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='뉴스 기사 데이터';

-- ------------------------------------------------------------
-- 5. collection_logs  -  수집 실행 로그
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS collection_logs (
    id              BIGINT       NOT NULL AUTO_INCREMENT,
    collector_name  VARCHAR(50)  NOT NULL COMMENT '수집기 이름 (pykrx, opendart, news)',
    target          VARCHAR(100) DEFAULT NULL COMMENT '수집 대상 (종목코드, 키워드 등)',
    status          VARCHAR(20)  NOT NULL DEFAULT 'started' COMMENT '실행 상태 (started, success, failed)',
    started_at      DATETIME     DEFAULT NULL COMMENT '실행 시작 시각',
    finished_at     DATETIME     DEFAULT NULL COMMENT '실행 종료 시각',
    row_count       INT          DEFAULT NULL COMMENT '수집 건수',
    error_message   TEXT         DEFAULT NULL COMMENT '오류 메시지',
    created_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_logs_collector_started (collector_name, started_at),
    KEY idx_logs_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Collector 실행 로그';
