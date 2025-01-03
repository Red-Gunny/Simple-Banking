# 주요 설계 고려사항

## 1. 시스템 특성 고려 설계 방향
입출금 시스템의 경우, 정확하게 정보를 제시해야 하므로 **정합성**이 가장 우선되어야 합니다. 각 거래가 이루어지면서 **정합성**을 유지하기 위해 **시간에 따라 데이터 흐름을 기록**하였습니다. 따라서 서버로 수정 작업(CUD)을 요청하였을 때는 순서에 따라 요청 내용을 기록하였습니다. 이를 위해 타 시스템(FE 등)에서 서버로 요청할 때 내용에는 요청 시각을 반드시 포함하도록 설계하였습니다. 그리고 계좌 정보의 경우에도 시간에 따라서 어떻게 변화되는지 기록하였습니다. 이를 위해서는 현재 상태를 나타내는 `ACCOUNT_BASE`와 이력을 나타내는 `ACCOUNT_HIST` 2개의 테이블을 활용했습니다. 이러한 이력 관리를 통해 특정 시점에 시스템에서 오류가 나더라도 기본적으로 재현 가능하도록 하였습니다.

## 2. 무결성 보장에 대하여
위의 `ACCOUNT_BASE`와 `ACCOUNT_HIST`의 형태로 인해 작업이 진행되는 동안 일시적으로 데이터의 정합성이 어긋날 수 있습니다. 이는 작업이 진행되는 동안 상태를 기록하는 방법을 통해 해결하고자 하였습니다. 작업 이력 테이블(`JOB_HIST`) 내에 요청 시에는 `PROC_STAT_CD` 필드를 통해 진행 상태를 기록하고자 하였습니다. 이를 통해 작업이 최종적으로 완료되었을 때만 후속 연산을 진행할 수 있도록 하고자 하였습니다.

추가적으로 `ACCOUNT_BASE`의 현재 잔액(`Balance`)과 `ACCOUNT_HIST`의 거래 후 잔액(`Balance`)에 대해 시스템 설계 에러, 휴먼 에러 등의 사유로 두 개의 데이터가 어긋날 수 있습니다. 예를 들어 계좌 기본 테이블 내 현재 상태의 잔액과 계좌 이력 테이블 내 최신 이력의 거래 후 잔액은 반드시 같아야 합니다. 하지만 이러한 두 개의 데이터를 둠으로써 운용자로 하여금 계좌의 무결성 상태를 확인하는 역할을 합니다. 만약 문제에 주어진 조건 외에 또 다른 연산 작업이 시스템에 추가되는 상황을 가정할 때, 두 개의 데이터가 같지 않을 경우 해당 계좌의 무결성이 위배되었다고 간주하고, 연산 진행을 불가능하도록 막을 수 있습니다.

## 3. DB 설계 시 자료형에 대하여
입출금 시스템에서 자료형은 크게 금액, 날짜(일시), 일반 텍스트로 나눌 수 있습니다.

금액의 경우 먼저 `Double`, `Float` 실수 자료형의 경우 연산 시 오차가 발생할 수 있어 고려하지 않았습니다. 그리고 소수점 표기, 앞자리 0 표기 여부에 따라 명확하게 데이터를 인식하고 구분지을 수 있어야 합니다. 이에 소스 코드 레벨에서 연산과정과 DB 자료형을 제외하고는 **문자열**을 활용하였습니다.

날짜 자료형의 경우, 실제 시스템에서 연산하거나 작업할 때 사용하는 데이터와 DB의 레코드 생성시각/수정시각 데이터를 분리하였습니다. 데이터 가공 시 필요에 따라서 자료형을 변환해야 합니다. 그런데 `DATE` 자료형에 인덱스가 걸려있을 때 다른 자료형으로 변환하면 DB 인덱스를 사용할 수 없습니다. 또한 비교 연산 시 **문자열**과 `DATE` 자료형을 비교하는 과정에서 사용자의 실수로 올바르게 이루어지지 못할 수 있습니다. 따라서 시스템 연산 및 작업에 필요한 날짜 데이터는 **문자열**(`VARCHAR`)을 사용하였습니다. 반면에 DB 레코드 생성/수정 시각을 기록하는 목적의 데이터 자료형은 `TIMESTAMP`를 사용하였습니다.

일반 텍스트의 경우에는 확장 가능성만 고려하였습니다. 시스템을 운영하면서 향후 자료형을 변경하게 되면 여러 부작용이 발생할 수 있기 때문에 **적요 항목**의 경우 `TEXT` 자료형을 설정하였습니다. 그 외에 자료형은 `VARCHAR` 자료형을 사용했습니다.

![erd](https://github.com/user-attachments/assets/634c8379-b300-42df-889e-4e17f90afac0)


# API Endpoint 설명

## 1. 거래내역 조회 API

### (1) 개요
- **설명**: 고객의 계좌에 대해 특정 기간 동안의 거래 내역을 조회하는 API
- **버전**: v1

### (2) 요청
#### 요청 정보
- **HTTP 메소드**: GET
- **URL**: `/api/v1/{account_id}/transactions`

### URL 경로 변수

| 필드명     | 타입   | 필수 여부 | 설명                        |
|------------|--------|------------|-----------------------------|
| account_id | String | Y          | 조회하고자 하는 계좌의 식별자 |

### 쿼리 파라미터

| 필드명        | 타입   | 필수 여부 | 설명                              |
|---------------|--------|------------|-----------------------------------|
| customer_id   | String | Y          | 고객 식별자                        |
| search_from_dt| String | N          | 조회할 거래내역의 시작일시 (yyyy-MM-dd) |
| search_to_dt  | String | N          | 조회할 거래내역의 종료일시 (yyyy-MM-dd) |
| filter_action | String | N          | 거래 항목(0001: 입금, 0002: 출금)     |

#### 요청 예시
```
GET http://127.0.0.1:5000/api/v1/123/transactions?customer_id=hong&search_from_dt=2024-09-01&search_to_dt=2024-11-01&filter_action=0001
```

### (3) 응답

#### 응답 본문 형식 (Response Body)
- **Content-Type**: application/json

#### 응답 속성
##### 거래내역(Bakings) 항목

| 필드명      | 타입               |  설명                                |
|-------------|--------------------|------------------------------------|
| account_id  | String             | 조회하고자 하는 계좌의 식별자        |
| Bakings     | Array of Objects   | 거래 내역 리스트                     |
| customer_id | String             | 고객 식별자                          |
| banking_cnt | Integer            | 반환된 거래 내역의 총 개수            |
| request_dttm| String             | 거래내역 요청이 발생한 시간 (형식: YYYY-MM-DD HH:MM:SS) |

##### 거래내역(Bakings) 항목

| 필드명        | 타입      | 설명                                   |
|---------------|-----------|----------------------------------------|
| banking_seq   | Integer   | 거래내역의 순서 (역순 정렬)              |
| banking_div   | String    | 거래 유형 (0001: 입금, 0002: 출금)       |
| banking_amount| String    | 거래 금액                               |
| after_balance | String    | 거래 후 잔액                            |
| banking_dttm  | String    | 거래 발생 일시 (형식: YYYY-MM-DD HH:MM:SS)|
| etc           | String    | 기타 정보 (거래 메모나 설명 등)           |


#### 응답 예시
```json
{
    "Bakings": [
        {
            "after_balance": "42000",
            "banking_amount": "10000",
            "banking_div": "0001",
            "banking_dttm": "2024-10-16 20:21:49",
            "banking_seq": 1,
            "etc": "etc"
        },
        {
            "after_balance": "32000",
            "banking_amount": "10000",
            "banking_div": "0001",
            "banking_dttm": "2024-10-16 20:21:20",
            "banking_seq": 2,
            "etc": "etc"
        },
        {
            "after_balance": "22000",
            "banking_amount": "10000",
            "banking_div": "0001",
            "banking_dttm": "2024-10-16 20:20:24",
            "banking_seq": 3,
            "etc": "etc"
        },
        {
            "after_balance": "12000",
            "banking_amount": "10000",
            "banking_div": "0001",
            "banking_dttm": "2024-10-16 20:18:27",
            "banking_seq": 4,
            "etc": "etc"
        }
    ],
    "account_id": "123",
    "banking_cnt": 4,
    "customer_id": "hong",
    "request_dttm": "2024-10-16 21:08:03"
}
```

#### 주요 예외사항
조회결과 거래내역이 없는 경우 -> Bankings는 빈 리스트이며, banking_cnt는 0으로 세팅

## 2. 입금 API

### (1) 개요
- **설명**: 고객이 요청한 금액을 계좌에서 입금하는 API
- **버전**: v1

### (2) 요청

#### 요청 정보
- **HTTP 메소드**: POST
- **URL**: `/api/v1/deposit`

#### 요청 헤더
- **Content-Type**: application/json

#### 요청 속성


| 필드명            | 타입       | 필수 여부 | 설명                              |
|---------------|------------|------|----------------------------------|
| account_id    | String     |Y     | 출금 대상 계좌 식별자                        |
| customer_id   | String     |Y     | 고객 식별자                                    |
| amount        | String     |Y     | 입금 금액                                     |
| etc           | String     |N     | 적요                                         |
| request_time  | String     |Y     |    요청 시각 (형식: YYYY-MM-DD HH:MM:SS)             |

#### 요청 예시
```
{
    "account_id" : "123",
    "customer_id" : "hong",
    "amount" : "10000",
    "etc" : "etc",
    "request_time" : "2024-10-16 20:04:00"
}

```

### (3) 응답

#### 응답 헤더
- **Content-Type**: application/json

#### 응답 속성

| 필드명      | 타입               |  설명                                |
|-------------|--------------------|---------------------------|
| account_id  | String             | 입금 대상 계좌 식별자                                |
| customer_id | String             | 고객 식별자                                      |
| proc_id     | String             | 작업 요청 식별자                                 |
| stat_cd     | String             | 처리 상태 코드 (0000: 성공, 9999: 실패)            |

#### 응답 예시
#### 성공
```json
{
    "account_id": "123",
    "customer_id": "hong",
    "proc_id": "req123456",
    "stat_cd": "0000"
}

```
#### 실패
```json
{
    "account_id": "123",
    "customer_id": "hong",
    "proc_id": "req123456",
    "stat_cd": "9999"
}

```

## 3. 출금 API

### (1) 개요
- **설명**: 고객이 요청한 금액을 계좌에서 출금하는 API
- **버전**: v1

### (2) 요청

#### 요청 정보
- **HTTP 메소드**: POST
- **URL**: `/api/v1/withdraw`

#### 요청 헤더
- **Content-Type**: application/json

#### 요청 속성

| 필드명            | 타입       | 필수 여부 | 설명                              |
|---------------|------------|------|----------------------------------|
| account_id    | String     |Y     | 출금 대상 계좌 식별자                        |
| customer_id   | String     |Y     | 고객 식별자                                    |
| amount        | String     |Y     | 입금 금액                                     |
| etc           | String     |N     | 적요                                         |
| request_time  | String     |Y     |   요청 시각 (형식: YYYY-MM-DD HH:MM:SS)             |

#### 요청 예시
```
{
    "account_id" : "123",
    "customer_id" : "hong",
    "amount" : "10000",
    "etc" : "etc",
    "request_time" : "2024-10-16 20:04:00"
}

```

### (3) 응답

#### 응답 헤더
- **Content-Type**: application/json

#### 응답 속성

| 필드명      | 타입               |  설명                                |
|-------------|--------------------|---------------------------|
| account_id  | String             | 출금 대상 계좌 식별자                                |
| customer_id | String             | 고객 식별자                                      |
| proc_id     | String             | 작업 요청 식별자                                 |
| stat_cd     | String             | 처리 상태 코드 (0000: 성공, 9999: 실패)            |

#### 응답 예시
#### 성공
```json
{
    "account_id": "123",
    "customer_id": "hong",
    "proc_id": "온라인 요청 식별자",
    "stat_cd": "0000"
}

```
#### 실패
```json
{
    "account_id": "123",
    "customer_id": "hong",
    "proc_id": "온라인 요청 식별자",
    "stat_cd": "9999"
}
```

#### 주요 상태코드 정보
0000 - 정상 출금  /  9999 - 계좌 잔고 부족

## 4. 주요 예외처리 사항

### (1) API 공통 사항 -  고객에 해당하는 계좌가 존재하지 않을 경우
에러코드 : 4444 / 에러사유 : 고객 계좌번호 미보유

```json
{
    "account_id" : "요청 계좌번호",
    "customer_id" : "요청 고객번호",
    "error_cd": "4444",
    "error_reason": "고객 계좌번호 미보유"
}
```

### (2) API 공통 사항 -  JSON 내용 포맷이 잘못된 경우
```json
{
    "error_cd": "9999",
    "error_reason": "JSON 객체 오류"
}
```
### (3) 거래내역 조회 API -  조회 결과 거래내역이 없는 경우
빈 거래리스트와 banking count는 0으로 반환함

### (4) 출금 API - 출금 진행 시 계좌 잔고가 부족할 경우
```json
{
    "account_id": "요청 계좌번호",
    "customer_id": "요청 고객번호",
    "proc_id": "온라인 요청 식별자",
    "stat_cd": "9999"
}
```
