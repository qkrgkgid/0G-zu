# 30HR 개발 기술스택 및 개발명세서

- 문서명: 30인 미만 사업장용 인원·급여·노무관리 앱 개발명세서
- 프로젝트명: `30HR`
- 작성일: 2026-04-27 KST
- 목적: Codex 또는 개발 에이전트가 MVP를 바로 구현할 수 있도록 기술스택, 아키텍처, 데이터모델, API, 계산로직, 화면, 작업 티켓을 정의한다.
- 법령 기준: 대한민국 근로기준법, 최저임금법, 개인정보 보호법, 4대보험 관련 고시·요율을 기준으로 하되, 실제 서비스 전 노무사·세무사·개인정보보호 담당자의 검수를 필수로 한다.

---

## 1. 제품 정의

### 1.1 한 줄 컨셉

`30HR`은 30인 미만 사업장이 근로계약서, 직원대장, 출퇴근, 휴가, 급여계산, 임금명세서, 법정 증빙을 한 번에 관리하도록 돕는 소규모 사업장 전용 HR·급여 컴플라이언스 앱이다.

### 1.2 핵심 사용자

| 사용자 | 설명 | 주요 니즈 |
|---|---|---|
| 사업주 | 1~29인 사업장 대표 | 급여 오류 방지, 노무 리스크 예방, 세무사 전달자료 생성 |
| 총무/관리자 | 전담 HR은 아니지만 급여·근태를 관리하는 직원 | 월급날 마감, 근로계약서, 휴가, 증빙 관리 |
| 직원 | 사업장 소속 근로자 | 출퇴근 기록, 휴가 신청, 임금명세서 조회 |
| 외부 세무사/노무사 | 선택적 협업 계정 | 급여자료 확인, 계약서/취업규칙/증빙 검토 |

### 1.3 MVP 목표

처음부터 대형 HR SaaS를 만들지 않는다. MVP는 다음 6개 문제만 해결한다.

1. 직원 정보와 입퇴사 이력 관리
2. 근로계약서 생성·서명·보관
3. 출퇴근 및 휴가 기록
4. 급여계산과 임금명세서 생성
5. 최저임금·연장/야간/휴일수당·주휴수당 위험 알림
6. 퇴사자·분쟁 대비 증빙팩 생성

---

## 2. 법령·컴플라이언스 요구사항

### 2.1 법 적용 구간

| 구간 | 앱 판정값 | 주요 기능 |
|---|---|---|
| 1~4인 | `UNDER_5` | 근로계약서, 임금명세서, 최저임금, 주휴수당, 퇴직금 중심 |
| 5~9인 | `BETWEEN_5_AND_9` | 연장·야간·휴일 가산수당, 연차, 해고·징계 증빙 강화 |
| 10~29인 | `BETWEEN_10_AND_29` | 취업규칙 작성·신고 알림, 규정 템플릿, 30인 도달 준비 |

### 2.2 필수 법정 기능

| 법정 이슈 | 구현 요구사항 |
|---|---|
| 근로조건 서면 명시 | 표준 근로계약서 생성, 전자서명, PDF 보관, 변경이력 저장 |
| 임금대장 | 월별 급여 실행 결과를 직원별·항목별로 저장 |
| 임금명세서 | 지급일, 총액, 항목별 금액, 계산방법, 공제내역을 자동 기재 |
| 최저임금 | 연도별 최저임금 설정값 기준으로 시급 환산 검증 |
| 연장·야간·휴일수당 | 5인 이상 여부, 근무시간, 휴일구분, 야간시간을 기준으로 계산 |
| 휴게시간 | 4시간 이상/8시간 이상 근무 시 휴게시간 누락 감지 |
| 연차 | 입사일 기준 우선. 회계연도 기준은 2차 개발 |
| 퇴직금 | 1년 이상·주 15시간 이상 여부를 기준으로 예상액 계산 |
| 개인정보 | 최소수집, 암호화, 접근권한, 접속기록, 파기정책, 처리방침 필요 |
| 증빙보존 | 계약서, 임금대장, 급여명세서, 근태, 휴가, 승인기록, 변경로그 보관 |

### 2.3 법률 고지 문구

서비스 화면과 약관에 다음 취지의 문구를 넣는다.

```text
본 서비스는 사업장의 인사·급여·노무 관리를 지원하기 위한 소프트웨어입니다.
서비스에서 제공하는 계산 결과와 리스크 알림은 입력값 및 설정값을 기준으로 한 참고자료이며,
개별 사건에 대한 법률자문 또는 노무자문을 대체하지 않습니다.
분쟁, 해고, 징계, 임금체불, 4대보험 신고 등 법적 판단이 필요한 사안은 공인노무사, 세무사, 변호사 등 전문가 검토를 받으시기 바랍니다.
```

---

## 3. 추천 기술스택

### 3.1 기본 원칙

- 1차 MVP는 `웹앱 + PWA`로 간다.
- 모바일 네이티브 앱은 2차 이후로 미룬다.
- 급여·노무 계산은 백엔드에서만 수행한다.
- 법령값과 요율은 코드에 하드코딩하지 않고 DB 설정값으로 버전관리한다.
- 멀티테넌트 SaaS 구조를 전제로 설계한다.

### 3.2 스택 요약

| 영역 | 추천 스택 | 선택 이유 |
|---|---|---|
| Monorepo | pnpm workspace + Turborepo | 웹/백엔드/공통 타입 공유 |
| Frontend | Next.js App Router + React + TypeScript | 서버 컴포넌트, 라우팅, SEO, PWA 확장 용이 |
| UI | Tailwind CSS + shadcn/ui | 관리자 SaaS UI를 빠르게 구축 |
| Form | React Hook Form + Zod | 급여/계약서 입력값 검증에 적합 |
| Data Fetching | TanStack Query | 서버 상태 캐싱, 낙관적 업데이트 |
| Backend | NestJS + TypeScript | 모듈형 구조, 테스트, DI, RBAC 구현 용이 |
| API | REST 우선, OpenAPI 자동 문서화 | Codex 구현과 외부 연동에 단순 |
| ORM | Prisma | 타입 안정성, 마이그레이션 관리 |
| DB | PostgreSQL | 급여·계약·감사로그 등 정합성 높은 업무 데이터에 적합 |
| Cache/Queue | Redis + BullMQ | 급여명세서 PDF 생성, 이메일 발송, 증빙팩 생성 |
| File Storage | S3 호환 스토리지 | 계약서 PDF, 임금명세서, 증빙팩 보관 |
| Auth | 자체 이메일 로그인 + JWT + Refresh Token + RBAC | 직원/관리자/세무사 권한 분리 |
| Notification | Email 우선, Slack Webhook 2차 | MVP에서는 이메일 발송 우선 |
| PDF | Playwright 또는 Puppeteer 기반 HTML-to-PDF | 근로계약서/임금명세서 서식 생성 |
| Test | Vitest/Jest + Playwright | 계산로직 단위테스트와 E2E 테스트 |
| Infra | Docker Compose local, AWS Seoul 또는 Naver Cloud | 국내 개인정보·지연시간 고려 |
| CI/CD | GitHub Actions | 테스트, 린트, 빌드, 배포 자동화 |
| Monitoring | Sentry + OpenTelemetry + CloudWatch/Grafana | 에러 추적, 성능 모니터링 |
| Analytics | PostHog 또는 자체 이벤트 로그 | 기능 사용률, 전환율 분석 |

### 3.3 권장 저장소 구조

```bash
30hr/
  apps/
    web/                       # Next.js 관리자/직원 웹앱
    api/                       # NestJS API 서버
  packages/
    shared/                    # 공통 타입, 상수, 유틸
    payroll-engine/            # 급여·수당 계산 순수 함수
    legal-config/              # 법령/요율 seed 데이터
    ui/                        # 공통 UI 컴포넌트
  infra/
    docker/
    terraform/
  docs/
    product/
    legal/
    api/
    test-cases/
  scripts/
    seed.ts
    generate-openapi.ts
  .github/
    workflows/
  package.json
  pnpm-workspace.yaml
  turbo.json
```

### 3.4 로컬 개발 환경

```bash
# 1. 의존성 설치
pnpm install

# 2. 로컬 인프라 실행
docker compose up -d postgres redis minio mailhog

# 3. DB 마이그레이션
pnpm --filter api prisma:migrate

# 4. 시드 데이터 입력
pnpm seed

# 5. 개발 서버 실행
pnpm dev
```

---

## 4. 시스템 아키텍처

### 4.1 논리 아키텍처

```text
[Web/PWA - Next.js]
        |
        | REST API / JSON
        v
[API Server - NestJS]
        |
        +--> [PostgreSQL] 업무 데이터
        +--> [Redis/BullMQ] 비동기 작업
        +--> [S3/MinIO] PDF·첨부파일
        +--> [Email Provider] 임금명세서/알림 발송
        +--> [Slack Webhook] 관리자 알림, 2차
```

### 4.2 멀티테넌트 원칙

- 모든 주요 테이블은 `tenant_id`를 가진다.
- 사용자 계정은 여러 사업장에 소속될 수 있다.
- API 요청 시 `tenant_id`와 사용자 권한을 항상 검증한다.
- 관리자 권한이 있어도 다른 tenant 데이터 조회는 불가하다.
- 감사로그는 tenant별로 분리 조회하되, 삭제 불가 정책을 둔다.

### 4.3 권한 모델

| Role | 설명 | 권한 |
|---|---|---|
| `OWNER` | 사업주 | 모든 기능 |
| `HR_ADMIN` | 총무/관리자 | 직원, 근태, 급여, 계약서 관리 |
| `MANAGER` | 팀장 | 소속 직원 근태/휴가 승인 |
| `EMPLOYEE` | 직원 | 본인 정보, 출퇴근, 휴가, 급여명세서 조회 |
| `ADVISOR` | 세무사/노무사 | 초대받은 사업장의 제한적 조회/검토 |
| `SUPER_ADMIN` | 서비스 운영자 | 고객지원용 제한 접근. 원칙적으로 개인정보 마스킹 |

---

## 5. 핵심 도메인 모듈

### 5.1 모듈 목록

| 모듈 | 기능 |
|---|---|
| Auth | 로그인, 토큰, 비밀번호 재설정, 2FA 확장 |
| Tenant | 사업장 정보, 상시근로자 수, 업종, 급여정책 |
| User | 로그인 계정, 역할, 초대 |
| Employee | 직원대장, 입퇴사, 고용형태, 급여정보 |
| Contract | 근로계약서 템플릿, 생성, 전자서명, PDF |
| Attendance | 출퇴근, 근무일정, 휴게시간, 연장근로 승인 |
| Leave | 연차, 휴가신청, 승인, 잔여일수 |
| Payroll | 급여마감, 수당계산, 공제계산, 임금대장 |
| PayStatement | 임금명세서 생성, 발송, 열람확인 |
| Compliance | 법정 리스크 감지, 알림 |
| Evidence | 직원별 증빙팩 생성 |
| Notification | 이메일, Slack, 앱 알림 |
| AuditLog | 변경이력, 접근이력, 다운로드 이력 |
| LegalConfig | 최저임금, 4대보험 요율, 법정 기준값 버전관리 |
| Integration | 세무사 제출용 엑셀, 외부 연동 |

---

## 6. 데이터베이스 설계

### 6.1 주요 테이블

#### tenants

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| name | varchar | 사업장명 |
| business_number | varchar | 사업자등록번호, 암호화 또는 부분 마스킹 |
| industry_code | varchar | 업종코드 |
| employee_count_snapshot | int | 최근 상시근로자 수 스냅샷 |
| payroll_cutoff_day | int | 급여산정 마감일 |
| payday | int | 급여지급일 |
| timezone | varchar | 기본 `Asia/Seoul` |
| created_at | timestamptz | 생성일 |
| updated_at | timestamptz | 수정일 |

#### users

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| email | varchar | 로그인 이메일 |
| password_hash | varchar | 비밀번호 해시 |
| name | varchar | 이름 |
| phone | varchar | 휴대전화, 선택 |
| status | enum | ACTIVE, INVITED, SUSPENDED |
| created_at | timestamptz | 생성일 |

#### tenant_users

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| tenant_id | uuid | FK |
| user_id | uuid | FK |
| role | enum | OWNER, HR_ADMIN, MANAGER, EMPLOYEE, ADVISOR |
| employee_id | uuid | 직원 계정인 경우 연결 |
| created_at | timestamptz | 생성일 |

#### employees

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| tenant_id | uuid | FK |
| employee_no | varchar | 사번 |
| name | varchar | 성명 |
| birth_date | date | 생년월일. 주민등록번호 수집 지양 |
| phone | varchar | 연락처 |
| email | varchar | 이메일 |
| employment_type | enum | REGULAR, CONTRACT, PART_TIME, DAILY |
| status | enum | ACTIVE, ON_LEAVE, RESIGNED |
| hire_date | date | 입사일 |
| resignation_date | date | 퇴사일 |
| weekly_contract_hours | decimal | 주 소정근로시간 |
| monthly_base_salary | int | 월 기본급 |
| hourly_wage | int | 시급 |
| bank_name | varchar | 급여계좌 은행 |
| bank_account_encrypted | text | 암호화된 계좌번호 |
| created_at | timestamptz | 생성일 |
| updated_at | timestamptz | 수정일 |

#### employment_contracts

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| tenant_id | uuid | FK |
| employee_id | uuid | FK |
| contract_type | enum | STANDARD, PART_TIME, FIXED_TERM |
| start_date | date | 계약시작일 |
| end_date | date | 계약종료일, 기간제만 |
| work_place | varchar | 근무장소 |
| job_description | text | 업무내용 |
| wage_terms | jsonb | 임금 조건 |
| work_time_terms | jsonb | 근로시간 조건 |
| status | enum | DRAFT, SENT, SIGNED, CANCELLED |
| signed_at | timestamptz | 서명일 |
| pdf_file_id | uuid | PDF 파일 |
| created_by | uuid | 작성자 |
| created_at | timestamptz | 생성일 |

#### attendance_records

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| tenant_id | uuid | FK |
| employee_id | uuid | FK |
| work_date | date | 근무일 |
| clock_in_at | timestamptz | 출근시각 |
| clock_out_at | timestamptz | 퇴근시각 |
| break_minutes | int | 휴게시간 |
| source | enum | MANUAL, WEB, MOBILE, IMPORT |
| approval_status | enum | PENDING, APPROVED, REJECTED |
| approved_by | uuid | 승인자 |
| created_at | timestamptz | 생성일 |

#### leave_requests

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| tenant_id | uuid | FK |
| employee_id | uuid | FK |
| leave_type | enum | ANNUAL, HALF_DAY, SICK, UNPAID, FAMILY_CARE |
| start_date | date | 시작일 |
| end_date | date | 종료일 |
| leave_units | decimal | 차감일수 |
| reason | text | 사유 |
| status | enum | REQUESTED, APPROVED, REJECTED, CANCELLED |
| approved_by | uuid | 승인자 |
| created_at | timestamptz | 생성일 |

#### payroll_runs

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| tenant_id | uuid | FK |
| payroll_month | char(7) | 예: 2026-04 |
| period_start | date | 산정 시작일 |
| period_end | date | 산정 종료일 |
| status | enum | DRAFT, CALCULATED, CONFIRMED, PAID, CANCELLED |
| total_gross_pay | int | 총 지급액 |
| total_deductions | int | 총 공제액 |
| total_net_pay | int | 실지급액 |
| confirmed_by | uuid | 확정자 |
| confirmed_at | timestamptz | 확정일 |
| created_at | timestamptz | 생성일 |

#### payroll_items

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| payroll_run_id | uuid | FK |
| employee_id | uuid | FK |
| item_type | enum | BASE, OVERTIME, NIGHT, HOLIDAY, WEEKLY_HOLIDAY, MEAL, BONUS, DEDUCTION |
| item_name | varchar | 항목명 |
| amount | int | 금액 |
| calculation_basis | text | 계산식 설명 |
| taxable | boolean | 과세 여부 |
| created_at | timestamptz | 생성일 |

#### pay_statements

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| payroll_run_id | uuid | FK |
| employee_id | uuid | FK |
| statement_no | varchar | 명세서 번호 |
| gross_pay | int | 지급총액 |
| deductions | int | 공제총액 |
| net_pay | int | 실지급액 |
| pdf_file_id | uuid | PDF |
| sent_at | timestamptz | 발송일 |
| viewed_at | timestamptz | 열람일 |
| created_at | timestamptz | 생성일 |

#### legal_configs

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| key | varchar | 예: MINIMUM_WAGE_HOURLY |
| value | jsonb | 값 |
| effective_from | date | 적용 시작일 |
| effective_to | date | 적용 종료일 |
| source_name | varchar | 출처명 |
| source_url | text | 출처 URL |
| created_at | timestamptz | 생성일 |

#### compliance_alerts

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| tenant_id | uuid | FK |
| employee_id | uuid | 선택 |
| alert_type | enum | CONTRACT_MISSING, MIN_WAGE_RISK, OVERTIME_RISK, PAYSTATEMENT_MISSING, BREAK_MISSING, RULES_OF_EMPLOYMENT |
| severity | enum | INFO, WARNING, CRITICAL |
| title | varchar | 제목 |
| message | text | 설명 |
| status | enum | OPEN, RESOLVED, IGNORED |
| detected_at | timestamptz | 감지일 |
| resolved_at | timestamptz | 해결일 |

#### audit_logs

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | uuid | PK |
| tenant_id | uuid | FK |
| actor_user_id | uuid | 행위자 |
| action | varchar | 예: EMPLOYEE_UPDATED |
| resource_type | varchar | 대상 종류 |
| resource_id | uuid | 대상 ID |
| before | jsonb | 변경 전 |
| after | jsonb | 변경 후 |
| ip_address | inet | IP |
| user_agent | text | UA |
| created_at | timestamptz | 생성일 |

### 6.2 Prisma 모델 예시

```prisma
model Tenant {
  id                    String   @id @default(uuid())
  name                  String
  businessNumber        String?
  industryCode          String?
  employeeCountSnapshot Int      @default(0)
  payrollCutoffDay      Int      @default(31)
  payday                Int      @default(25)
  timezone              String   @default("Asia/Seoul")
  createdAt             DateTime @default(now())
  updatedAt             DateTime @updatedAt

  employees             Employee[]
  payrollRuns           PayrollRun[]
}

model Employee {
  id                  String   @id @default(uuid())
  tenantId            String
  employeeNo          String?
  name                String
  birthDate           DateTime?
  phone               String?
  email               String?
  employmentType      EmploymentType
  status              EmployeeStatus @default(ACTIVE)
  hireDate            DateTime
  resignationDate     DateTime?
  weeklyContractHours Decimal?
  monthlyBaseSalary   Int?
  hourlyWage          Int?
  createdAt           DateTime @default(now())
  updatedAt           DateTime @updatedAt

  tenant              Tenant @relation(fields: [tenantId], references: [id])
  attendanceRecords   AttendanceRecord[]
  payrollItems        PayrollItem[]

  @@index([tenantId, status])
}

enum EmploymentType {
  REGULAR
  CONTRACT
  PART_TIME
  DAILY
}

enum EmployeeStatus {
  ACTIVE
  ON_LEAVE
  RESIGNED
}
```

---

## 7. API 명세

### 7.1 공통 규칙

- Base URL: `/api/v1`
- 인증: `Authorization: Bearer <access_token>`
- 멀티테넌트 헤더: `X-Tenant-Id: <tenant_uuid>`
- 응답 형식:

```json
{
  "data": {},
  "meta": {},
  "error": null
}
```

- 에러 형식:

```json
{
  "data": null,
  "meta": {},
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "입력값을 확인해 주세요.",
    "details": []
  }
}
```

### 7.2 Auth

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/auth/register` | 사업장 최초 가입 |
| POST | `/auth/login` | 로그인 |
| POST | `/auth/refresh` | 토큰 재발급 |
| POST | `/auth/logout` | 로그아웃 |
| POST | `/auth/invitations` | 사용자 초대 |
| POST | `/auth/invitations/:token/accept` | 초대 수락 |

### 7.3 Tenant

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/tenants/current` | 현재 사업장 정보 |
| PATCH | `/tenants/current` | 사업장 정보 수정 |
| GET | `/tenants/current/compliance-profile` | 법 적용 구간 조회 |
| PATCH | `/tenants/current/payroll-policy` | 급여정책 수정 |

### 7.4 Employee

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/employees` | 직원 목록 |
| POST | `/employees` | 직원 등록 |
| GET | `/employees/:id` | 직원 상세 |
| PATCH | `/employees/:id` | 직원 수정 |
| POST | `/employees/:id/resign` | 퇴사 처리 |
| GET | `/employees/:id/evidence-pack` | 직원별 증빙 목록 |

### 7.5 Contract

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/contract-templates` | 계약서 템플릿 목록 |
| POST | `/contracts` | 계약서 생성 |
| GET | `/contracts/:id` | 계약서 상세 |
| POST | `/contracts/:id/send` | 서명 요청 |
| POST | `/contracts/:id/sign` | 전자서명 |
| GET | `/contracts/:id/pdf` | PDF 다운로드 |

### 7.6 Attendance

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/attendance/clock-in` | 출근 |
| POST | `/attendance/clock-out` | 퇴근 |
| GET | `/attendance` | 근태 목록 |
| POST | `/attendance/manual` | 수기 입력 |
| PATCH | `/attendance/:id/approve` | 근태 승인 |
| GET | `/attendance/summary` | 월별 근태 요약 |

### 7.7 Leave

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/leaves/balances` | 연차 잔여현황 |
| POST | `/leaves/requests` | 휴가 신청 |
| PATCH | `/leaves/requests/:id/approve` | 휴가 승인 |
| PATCH | `/leaves/requests/:id/reject` | 휴가 반려 |

### 7.8 Payroll

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/payroll-runs` | 급여 실행 생성 |
| POST | `/payroll-runs/:id/calculate` | 급여 계산 |
| GET | `/payroll-runs/:id` | 급여 실행 상세 |
| POST | `/payroll-runs/:id/confirm` | 급여 확정 |
| POST | `/payroll-runs/:id/pay-statements/generate` | 임금명세서 생성 |
| POST | `/payroll-runs/:id/pay-statements/send` | 임금명세서 발송 |
| GET | `/payroll-runs/:id/export` | 세무사 제출용 엑셀 다운로드 |

### 7.9 Compliance

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/compliance/alerts` | 리스크 알림 목록 |
| POST | `/compliance/scan` | 수동 리스크 검사 |
| PATCH | `/compliance/alerts/:id/resolve` | 알림 해결 처리 |
| PATCH | `/compliance/alerts/:id/ignore` | 알림 제외 처리 |

### 7.10 Evidence

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/evidence-packs` | 증빙팩 생성 요청 |
| GET | `/evidence-packs/:id` | 생성 상태 조회 |
| GET | `/evidence-packs/:id/download` | ZIP 다운로드 |

---

## 8. 급여·노무 계산 로직

### 8.1 계산 엔진 원칙

- 계산로직은 `packages/payroll-engine`에 순수 함수로 분리한다.
- DB 접근, API 호출, 날짜 조회를 계산 함수 내부에서 하지 않는다.
- 모든 계산 함수는 입력값과 legal config를 인자로 받는다.
- 계산 결과는 금액, 계산식 설명, 경고를 함께 반환한다.
- 법령값 변경에 대비하여 테스트케이스를 연도별로 분리한다.

### 8.2 legal_config 예시

```json
[
  {
    "key": "MINIMUM_WAGE_HOURLY",
    "value": { "amount": 10320, "currency": "KRW" },
    "effective_from": "2026-01-01",
    "effective_to": "2026-12-31",
    "source_name": "고용노동부 2026년 최저임금 고시"
  },
  {
    "key": "MONTHLY_STANDARD_HOURS",
    "value": { "hours": 209 },
    "effective_from": "2026-01-01",
    "effective_to": "2026-12-31",
    "source_name": "고용노동부 최저임금 월 환산 기준"
  },
  {
    "key": "NATIONAL_PENSION_RATE",
    "value": { "total": 0.095, "employee": 0.0475, "employer": 0.0475 },
    "effective_from": "2026-01-01",
    "effective_to": "2026-12-31",
    "source_name": "국민연금공단"
  },
  {
    "key": "HEALTH_INSURANCE_RATE",
    "value": { "total": 0.0719, "employee": 0.03595, "employer": 0.03595 },
    "effective_from": "2026-01-01",
    "effective_to": "2026-12-31",
    "source_name": "보건복지부"
  }
]
```

### 8.3 최저임금 검증

입력값:

```ts
type MinimumWageInput = {
  year: number;
  monthlyWage: number;
  monthlyContractHours: number;
  includedWageItems: PayrollItem[];
  excludedWageItems: PayrollItem[];
  minimumHourlyWage: number;
};
```

처리:

```text
최저임금 산입 임금 = includedWageItems 합계
환산시급 = 최저임금 산입 임금 / 월 소정근로시간
위반 가능성 = 환산시급 < 해당연도 최저시급
```

출력:

```ts
type MinimumWageResult = {
  hourlyEquivalent: number;
  minimumHourlyWage: number;
  isBelowMinimumWage: boolean;
  shortageAmountPerHour: number;
  warnings: string[];
};
```

### 8.4 주휴수당

MVP 기준:

```text
대상 후보:
- 주 소정근로시간 15시간 이상
- 소정근로일 개근
- 시급제 또는 일급제 중심

기본 계산:
주휴수당 = 1일 소정근로시간 × 시급
```

주의:

- 월급제는 기본급에 주휴수당이 포함된 구조인지 급여정책에서 설정해야 한다.
- 결근, 무급휴가, 지각·조퇴에 따른 개근 판단은 정책값으로 분리한다.

### 8.5 연장근로수당

MVP 기준:

```text
5인 이상 사업장:
연장근로수당 = 연장근로시간 × 통상시급 × 1.5

5인 미만 사업장:
근로기준법상 가산수당 적용 여부가 다르므로 기본값은 별도 표시한다.
앱에서는 "가산수당 자동적용 안 함"으로 설정하되, 사업장 약정에 따라 적용 가능하게 옵션 제공.
```

### 8.6 야간근로수당

```text
야간근로시간 = 22:00~06:00 사이 근무시간
야간근로수당 = 야간근로시간 × 통상시급 × 0.5
단, 실제 지급 항목 구성 시 연장·휴일과 중복되는 경우 합산 가산율을 계산한다.
```

### 8.7 휴일근로수당

```text
8시간 이내 휴일근로:
휴일근로수당 = 휴일근로시간 × 통상시급 × 1.5

8시간 초과 휴일근로:
8시간 이내분 = 8 × 통상시급 × 1.5
8시간 초과분 = 초과시간 × 통상시급 × 2.0
```

### 8.8 휴게시간 누락 감지

```text
근무시간 4시간 이상 8시간 미만: 휴게 30분 이상 필요
근무시간 8시간 이상: 휴게 60분 이상 필요
```

출력 알림:

```json
{
  "alert_type": "BREAK_MISSING",
  "severity": "WARNING",
  "message": "김OO 직원의 2026-04-15 근무기록에 휴게시간이 부족합니다."
}
```

### 8.9 월중 입퇴사 일할계산

초기에는 사업장 정책을 선택하게 한다.

| 정책값 | 계산 방식 |
|---|---|
| `CALENDAR_DAYS` | 월급 × 재직일수 / 해당월 총일수 |
| `WORKING_DAYS` | 월급 × 실제 근무일수 / 해당월 소정근무일수 |
| `FIXED_30_DAYS` | 월급 × 재직일수 / 30 |

MVP 기본값: `CALENDAR_DAYS`

### 8.10 퇴직금 예상액

MVP에서는 예상액만 제공한다.

```text
퇴직금 예상액 = 1일 평균임금 × 30일 × 계속근로연수
```

주의:

- 평균임금 산정 기간, 제외기간, 상여금·연차수당 반영은 2차 고도화에서 상세 구현.
- 화면에는 “예상액”으로 표시한다.

---

## 9. 화면 명세

### 9.1 관리자 대시보드

목적: 이번 달 해야 할 일을 한 화면에서 보여준다.

구성:

- 이번 달 급여마감 상태
- 미서명 계약서
- 미발송 임금명세서
- 최저임금 위험 직원
- 휴게시간 누락
- 연장근로 과다
- 입사/퇴사 예정자
- 10인 이상/30인 임박 알림

### 9.2 직원대장

기능:

- 직원 목록
- 검색: 이름, 사번, 상태, 고용형태
- 필터: 재직/퇴사/휴직
- 직원 상세
- 입사 처리
- 퇴사 처리
- 급여정보 변경
- 변경이력 조회

### 9.3 근로계약서

기능:

- 템플릿 선택
- 직원 선택
- 근로조건 입력
- 미리보기
- 서명 요청
- 직원 전자서명
- PDF 보관
- 변경계약서 생성

### 9.4 출퇴근

관리자:

- 일자별 근태현황
- 직원별 수정
- 연장근로 승인
- 근태마감

직원:

- 출근
- 퇴근
- 내 근무기록 조회
- 수정 요청

### 9.5 휴가

관리자:

- 휴가 신청 목록
- 승인/반려
- 연차 잔여현황
- 연차 조정

직원:

- 휴가 신청
- 신청내역 조회
- 잔여연차 조회

### 9.6 급여마감 마법사

단계:

```text
1. 급여월 선택
2. 직원·재직기간 확인
3. 근태 마감 확인
4. 수당 계산
5. 공제 계산
6. 최저임금·수당 오류 검사
7. 임금대장 생성
8. 임금명세서 생성
9. 발송
10. 세무사 제출용 엑셀 다운로드
```

### 9.7 임금명세서

직원 화면:

- 지급일
- 산정기간
- 지급항목
- 공제항목
- 계산방법
- 실지급액
- PDF 다운로드

### 9.8 증빙팩

관리자 화면:

- 직원 선택
- 기간 선택
- 포함 자료 선택
- ZIP 생성
- 다운로드 이력 저장

포함 자료:

```text
- 직원대장
- 근로계약서
- 임금명세서
- 임금대장
- 출퇴근기록
- 연장근로 승인기록
- 휴가 신청/승인기록
- 급여 변경이력
- 알림 해결이력
- 감사로그 요약
```

---

## 10. 프론트엔드 개발명세

### 10.1 라우트 구조

```bash
apps/web/app/
  (public)/
    login/page.tsx
    register/page.tsx
    invitation/[token]/page.tsx
  (app)/
    dashboard/page.tsx
    employees/page.tsx
    employees/[id]/page.tsx
    contracts/page.tsx
    attendance/page.tsx
    leaves/page.tsx
    payroll/page.tsx
    payroll/[runId]/page.tsx
    pay-statements/page.tsx
    compliance/page.tsx
    evidence-packs/page.tsx
    settings/page.tsx
  employee/
    home/page.tsx
    attendance/page.tsx
    leaves/page.tsx
    pay-statements/page.tsx
```

### 10.2 공통 컴포넌트

```bash
packages/ui/
  Button.tsx
  DataTable.tsx
  DatePicker.tsx
  MoneyInput.tsx
  EmployeeSelect.tsx
  StatusBadge.tsx
  ConfirmDialog.tsx
  Stepper.tsx
  RiskAlertCard.tsx
  PayrollItemTable.tsx
```

### 10.3 입력 검증 예시

```ts
import { z } from "zod";

export const employeeCreateSchema = z.object({
  name: z.string().min(1, "성명을 입력해 주세요."),
  hireDate: z.string().min(1, "입사일을 입력해 주세요."),
  employmentType: z.enum(["REGULAR", "CONTRACT", "PART_TIME", "DAILY"]),
  weeklyContractHours: z.number().min(0).max(52).optional(),
  monthlyBaseSalary: z.number().int().nonnegative().optional(),
  hourlyWage: z.number().int().nonnegative().optional(),
});
```

### 10.4 UX 원칙

- 사장/총무가 쓰는 앱이므로 HR 용어를 과도하게 쓰지 않는다.
- 모든 금액은 KRW 콤마 표시.
- 날짜는 `YYYY-MM-DD`.
- 급여 확정, 임금명세서 발송, 계약서 삭제는 확인 모달 필수.
- 계산 결과에는 항상 “계산근거 보기”를 제공한다.
- 위험 알림은 `해결`, `나중에`, `전문가 문의` 액션을 제공한다.

---

## 11. 백엔드 개발명세

### 11.1 NestJS 모듈 구조

```bash
apps/api/src/
  main.ts
  app.module.ts
  common/
    guards/
    decorators/
    filters/
    interceptors/
  auth/
  tenants/
  users/
  employees/
  contracts/
  attendance/
  leaves/
  payroll/
  pay-statements/
  compliance/
  evidence/
  files/
  notifications/
  legal-config/
  audit-logs/
```

### 11.2 서비스 레이어 원칙

- Controller: 요청/응답 DTO만 처리
- Service: 유스케이스 처리
- Repository 또는 PrismaService: DB 접근
- PayrollEngine: 순수 계산 함수
- ComplianceScanner: 리스크 탐지
- AuditLogInterceptor: 변경 작업 자동 기록

### 11.3 DTO 예시

```ts
export class CreatePayrollRunDto {
  payrollMonth!: string; // YYYY-MM
  periodStart!: string;  // YYYY-MM-DD
  periodEnd!: string;    // YYYY-MM-DD
}

export class CalculatePayrollDto {
  employeeIds?: string[];
  includeDraftAttendance?: boolean;
}
```

### 11.4 감사로그 대상 액션

반드시 기록:

- 직원 생성/수정/퇴사
- 급여정보 변경
- 근로계약서 생성/발송/서명/취소
- 출퇴근 수기수정
- 휴가 승인/반려
- 급여계산/확정/취소
- 임금명세서 생성/발송/다운로드
- 증빙팩 생성/다운로드
- 권한 변경
- 개인정보 다운로드

---

## 12. 보안·개인정보 설계

### 12.1 개인정보 최소수집

MVP에서는 주민등록번호 전체를 수집하지 않는다.

| 정보 | MVP 수집 여부 | 비고 |
|---|---|---|
| 성명 | 수집 | 필수 |
| 생년월일 | 선택 | 주민번호 대체 |
| 휴대전화 | 선택 | 알림용 |
| 이메일 | 수집 | 로그인/명세서 |
| 주소 | 선택 | 계약서 필요 시 |
| 주민등록번호 | 원칙적 미수집 | 4대보험 신고 직접대행 전까지 제외 |
| 계좌번호 | 선택 | 암호화 저장 |
| 가족정보 | 미수집 | 급여공제 고도화 전 제외 |

### 12.2 보안 요구사항

| 항목 | 요구사항 |
|---|---|
| 비밀번호 | Argon2 또는 bcrypt 해시 |
| 전송구간 | HTTPS 필수 |
| 중요정보 | 계좌번호 등 필드 레벨 암호화 |
| 접근권한 | RBAC + tenant 검증 |
| 세션 | Refresh Token Rotation |
| 로그 | 개인정보 본문 로그 금지 |
| 다운로드 | 계약서/명세서/증빙팩 다운로드 이력 저장 |
| 파일 | Private bucket, signed URL, 만료시간 적용 |
| 백업 | DB 일일 백업, 복구 테스트 |
| 삭제 | 퇴사자/해지 고객 데이터 보존·파기 정책 분리 |
| 운영자 접근 | 고객지원 목적, 마스킹, 접근사유 기록 |

### 12.3 개인정보 처리방침에 반영할 항목

- 처리하는 개인정보 항목
- 처리 목적
- 보유 및 이용기간
- 제3자 제공 여부
- 처리위탁
- 정보주체 권리
- 파기 절차
- 안전성 확보조치
- 개인정보 보호책임자
- 권익침해 구제방법

---

## 13. 알림 정책

### 13.1 관리자 알림

| 이벤트 | 채널 | 시점 |
|---|---|---|
| 계약서 미서명 | 앱/이메일 | 생성 후 3일 |
| 급여마감 예정 | 앱/이메일 | 지급일 5일 전 |
| 임금명세서 미발송 | 앱/이메일 | 지급일 당일 |
| 최저임금 위험 | 앱 | 급여계산 즉시 |
| 휴게시간 누락 | 앱 | 근태마감 전 |
| 10인 이상 도달 | 앱/이메일 | 월 1회 스캔 |
| 30인 임박 | 앱/이메일 | 25명 이상부터 |

### 13.2 직원 알림

| 이벤트 | 채널 |
|---|---|
| 계약서 서명 요청 | 이메일 |
| 휴가 승인/반려 | 이메일 |
| 임금명세서 발송 | 이메일 |
| 출퇴근 누락 | 앱/이메일 |

---

## 14. 엑셀 내보내기 명세

### 14.1 세무사 제출용 급여 엑셀

컬럼:

```text
급여월
사번
성명
입사일
퇴사일
기본급
주휴수당
연장수당
야간수당
휴일수당
식대
상여
기타지급
지급총액
국민연금
건강보험
장기요양
고용보험
소득세
지방소득세
기타공제
공제총액
실지급액
계산오류여부
비고
```

### 14.2 근태 엑셀

```text
일자
사번
성명
출근시각
퇴근시각
휴게시간
총근무시간
소정근로시간
연장근로시간
야간근로시간
휴일근로시간
승인상태
수정자
수정사유
```

---

## 15. 테스트 명세

### 15.1 단위 테스트 필수 케이스

#### 최저임금

| 케이스 | 입력 | 기대 |
|---|---|---|
| 2026년 월 209시간, 월급 2,156,880원 | 2,156,880 / 209 | 위반 아님 |
| 2026년 월 209시간, 월급 2,000,000원 | 2,000,000 / 209 | 위반 가능 |
| 시급 10,320원 | 10,320 | 위반 아님 |
| 시급 10,000원 | 10,000 | 위반 가능 |

#### 연장수당

| 케이스 | 입력 | 기대 |
|---|---|---|
| 5인 이상, 통상시급 12,000원, 연장 2시간 | 2 × 12,000 × 1.5 | 36,000원 |
| 5인 미만, 통상시급 12,000원, 연장 2시간 | 정책값 확인 | 기본 가산 미적용 또는 약정 적용 |

#### 야간수당

| 케이스 | 입력 | 기대 |
|---|---|---|
| 22:00~24:00, 통상시급 12,000원 | 2 × 12,000 × 0.5 | 12,000원 |
| 21:00~23:00 | 야간 1시간 | 6,000원 |

#### 휴게시간

| 케이스 | 입력 | 기대 |
|---|---|---|
| 6시간 근무, 휴게 0분 | 경고 |
| 6시간 근무, 휴게 30분 | 정상 |
| 9시간 근무, 휴게 30분 | 경고 |
| 9시간 근무, 휴게 60분 | 정상 |

### 15.2 E2E 테스트 시나리오

```text
1. 사업주가 가입한다.
2. 사업장을 생성한다.
3. 직원 3명을 등록한다.
4. 근로계약서를 생성하고 서명한다.
5. 직원이 출퇴근한다.
6. 직원이 휴가를 신청하고 관리자가 승인한다.
7. 관리자가 2026-04 급여를 생성한다.
8. 급여를 계산한다.
9. 최저임금 위험 알림이 표시된다.
10. 관리자가 급여를 수정한다.
11. 급여를 확정한다.
12. 임금명세서를 생성하고 발송한다.
13. 직원이 임금명세서를 조회한다.
14. 관리자가 세무사 제출용 엑셀을 다운로드한다.
15. 퇴사자 증빙팩을 생성한다.
```

---

## 16. MVP 작업 티켓

### EPIC 1. 프로젝트 초기화

#### TICKET 1-1. Monorepo 생성

- pnpm workspace 설정
- apps/web, apps/api, packages/shared 생성
- ESLint, Prettier, TypeScript 설정
- Docker Compose로 postgres, redis, minio, mailhog 구성

완료조건:

- `pnpm dev`로 web/api 동시 실행
- `pnpm lint`, `pnpm test` 실행 가능

#### TICKET 1-2. DB/Prisma 초기 설정

- Prisma 설치
- PostgreSQL 연결
- 기본 schema 생성
- migration 실행
- seed 스크립트 작성

완료조건:

- tenants, users, employees 기본 테이블 생성
- seed로 테스트 사업장/관리자/직원 생성

---

### EPIC 2. 인증·권한

#### TICKET 2-1. 로그인/회원가입

- 이메일/비밀번호 가입
- 비밀번호 해시
- JWT access token
- refresh token
- 로그아웃

완료조건:

- 로그인 후 관리자 대시보드 접근 가능
- 토큰 만료 시 refresh 가능

#### TICKET 2-2. Tenant RBAC

- tenant_users 테이블 구현
- Role guard 구현
- X-Tenant-Id 검증
- 다른 tenant 데이터 접근 차단

완료조건:

- A 사업장 사용자가 B 사업장 직원 API 접근 시 403 반환

---

### EPIC 3. 직원대장

#### TICKET 3-1. 직원 CRUD

- 직원 등록
- 목록
- 상세
- 수정
- 퇴사 처리

완료조건:

- 관리자 화면에서 직원 등록/수정 가능
- 퇴사자는 기본 목록에서 분리 표시

#### TICKET 3-2. 직원 변경 감사로그

- 직원 정보 변경 전/후 기록
- 급여정보 변경 시 별도 로그
- 퇴사 처리 로그

완료조건:

- 직원 상세에서 변경이력 확인 가능

---

### EPIC 4. 근로계약서

#### TICKET 4-1. 계약서 템플릿

- 표준/단시간/기간제 템플릿 seed
- 템플릿 변수 치환
- 미리보기

완료조건:

- 직원 정보로 계약서 초안 생성 가능

#### TICKET 4-2. 전자서명 및 PDF

- 서명 요청
- 직원 서명 화면
- 서명 완료 PDF 생성
- 파일 저장

완료조건:

- 계약서 상태가 DRAFT → SENT → SIGNED로 변경
- PDF 다운로드 가능

---

### EPIC 5. 근태

#### TICKET 5-1. 출퇴근 기록

- 직원 출근/퇴근 API
- 직원 화면
- 관리자 목록

완료조건:

- 직원별 일자별 출퇴근 기록 조회 가능

#### TICKET 5-2. 근태 수정/승인

- 관리자 수기 수정
- 수정사유 필수
- 승인상태 관리
- 감사로그 기록

완료조건:

- 수정 전/후 이력이 저장됨

---

### EPIC 6. 휴가

#### TICKET 6-1. 휴가 신청/승인

- 휴가 신청
- 관리자 승인/반려
- 휴가 차감

완료조건:

- 승인된 휴가는 근태와 급여계산에 반영 가능

#### TICKET 6-2. 기본 연차 계산

- 입사일 기준 연차 발생
- 1년 미만 월차
- 잔여일수 표시

완료조건:

- 직원별 연차 잔여일수 조회 가능

---

### EPIC 7. 급여계산

#### TICKET 7-1. Payroll Engine

- 최저임금 검증 함수
- 주휴수당 함수
- 연장/야간/휴일수당 함수
- 휴게시간 검증 함수
- 단위 테스트 작성

완료조건:

- 테스트 케이스 90% 이상 통과
- 계산 결과에 calculation_basis 포함

#### TICKET 7-2. 급여실행 생성/계산

- 급여월 생성
- 직원별 급여 계산
- 지급항목/공제항목 생성
- 경고 반환

완료조건:

- 관리자가 급여월 선택 후 직원별 계산 결과 확인 가능

#### TICKET 7-3. 급여확정

- DRAFT → CALCULATED → CONFIRMED 상태 전환
- 확정 후 수정 제한
- 취소 시 감사로그

완료조건:

- 확정된 급여는 임금명세서 생성 가능

---

### EPIC 8. 임금명세서

#### TICKET 8-1. 임금명세서 생성

- 급여확정 결과 기반 명세서 생성
- 지급/공제/계산방법 표시
- PDF 생성

완료조건:

- 직원별 PDF 생성 가능

#### TICKET 8-2. 임금명세서 발송/열람

- 이메일 발송
- 직원 화면 조회
- 열람일 저장

완료조건:

- 발송일/열람일 기록

---

### EPIC 9. 컴플라이언스 알림

#### TICKET 9-1. 리스크 스캐너

- 계약서 미작성
- 임금명세서 미발송
- 최저임금 미달
- 휴게시간 누락
- 10인 이상 취업규칙 알림
- 30인 임박 알림

완료조건:

- 대시보드에 위험 알림 표시

#### TICKET 9-2. 알림 처리

- 해결 처리
- 무시 처리
- 처리자/처리일 저장

완료조건:

- 알림 상태 변경 가능

---

### EPIC 10. 증빙팩

#### TICKET 10-1. 증빙팩 생성

- 직원/기간 선택
- 자료 수집
- PDF/엑셀/JSON 묶음 ZIP 생성
- 비동기 작업 처리

완료조건:

- 증빙팩 다운로드 가능

#### TICKET 10-2. 다운로드 이력

- 다운로드 사용자
- 다운로드 일시
- IP
- 파일 ID 저장

완료조건:

- 민감자료 다운로드 이력 조회 가능

---

## 17. Codex 작업 지시 프롬프트

### 17.1 초기 생성 프롬프트

```text
You are building a production-ready SaaS MVP called 30HR for Korean small businesses under 30 employees.

Use:
- pnpm workspace + Turborepo
- apps/web: Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui
- apps/api: NestJS, TypeScript, Prisma, PostgreSQL
- packages/payroll-engine: pure TypeScript payroll calculation functions
- Redis + BullMQ for async jobs
- S3-compatible storage for generated PDFs

Implement the repository skeleton, Docker Compose for postgres/redis/minio/mailhog, shared TypeScript config, ESLint, Prettier, and basic CI.

Do not implement incomplete mock business logic inside controllers. Put calculation functions in packages/payroll-engine and cover them with unit tests.
```

### 17.2 급여 엔진 구현 프롬프트

```text
Implement packages/payroll-engine with pure TypeScript functions.

Required functions:
1. checkMinimumWage(input)
2. calculateWeeklyHolidayAllowance(input)
3. calculateOvertimeAllowance(input)
4. calculateNightWorkAllowance(input)
5. calculateHolidayWorkAllowance(input)
6. validateBreakTime(input)
7. calculateProratedMonthlySalary(input)

Every function must:
- accept legal config as explicit input
- return amount, calculationBasis, warnings
- avoid DB calls and Date.now()
- include unit tests for Korean payroll scenarios
- handle KRW integer rounding explicitly
```

### 17.3 직원대장 구현 프롬프트

```text
Implement the Employee module in NestJS and Next.js.

Backend:
- CRUD APIs
- tenant isolation using X-Tenant-Id
- RBAC guard
- audit log on create/update/resign
- DTO validation

Frontend:
- employee list page
- create/edit form
- detail page
- resignation action with confirmation dialog
- use React Hook Form and Zod
```

### 17.4 급여마감 구현 프롬프트

```text
Implement Payroll Run flow.

Steps:
1. Create payroll run for YYYY-MM
2. Load active employees for the period
3. Summarize approved attendance records
4. Call payroll-engine functions
5. Store payroll_items with calculation_basis
6. Generate compliance alerts for risks
7. Confirm payroll run
8. Generate pay statements

Do not allow pay statement generation before payroll confirmation.
Do not allow editing a confirmed payroll run without explicit cancel/reopen action and audit log.
```

---

## 18. 운영·배포 전략

### 18.1 MVP 배포

1. Staging
   - 테스트 사업장 3~5개
   - 실제 급여자료를 익명화하여 검증
   - 노무사 검수

2. Production
   - 한국 리전 우선
   - DB 암호화
   - 자동 백업
   - 접근로그 보관
   - 장애 알림

### 18.2 백업 정책

| 데이터 | 백업주기 | 보관 |
|---|---|---|
| PostgreSQL | 매일 | 30일 |
| 파일스토리지 | 매일 | 30일 |
| 감사로그 | 삭제 금지 원칙 | 계약/약관에 따른 보존 |
| 설정값 | 변경 시 스냅샷 | 영구 |

### 18.3 릴리즈 정책

- `main`: 운영 배포
- `develop`: 개발 통합
- `feature/*`: 기능 개발
- PR 필수 체크:
  - lint
  - test
  - build
  - migration 검증
  - payroll-engine test 통과

---

## 19. 1차 개발 우선순위

| 순위 | 기능 | 이유 |
|---:|---|---|
| 1 | 직원대장 | 모든 기능의 기준 데이터 |
| 2 | 인증/RBAC/tenant | SaaS 기본 보안 |
| 3 | 급여 엔진 | 제품 차별화 핵심 |
| 4 | 임금명세서 | 유료 전환 가능성이 높음 |
| 5 | 근로계약서 | 법정 리스크 해결 |
| 6 | 근태 | 급여계산 근거 |
| 7 | 컴플라이언스 알림 | 차별화 |
| 8 | 증빙팩 | 분쟁 대응 차별화 |

---

## 20. 개발 제외 범위

MVP에서 제외한다.

| 제외 기능 | 제외 사유 |
|---|---|
| 네이티브 iOS/Android | PWA로 충분히 검증 가능 |
| 성과평가 | 구매동기가 약함 |
| 채용 ATS | 30인 미만 MVP와 거리 있음 |
| 4대보험 직접 신고대행 | 신고대행·개인정보·위임 리스크 큼 |
| AI 노무상담 자동답변 | 법률자문 오인 리스크 |
| 복잡한 교대근무 스케줄러 | 2차 기능 |
| 회계/ERP 연동 | 초기 범위 과다 |

---

## 21. 공식 참고자료

- 근로기준법 제48조 임금대장 및 임금명세서: 국가법령정보센터
- 근로기준법 제17조 근로조건 명시: 국가법령정보센터
- 개인정보 보호법 제29조 안전조치의무: 국가법령정보센터
- 2026년 최저임금 시간급 10,320원, 월 환산액 2,156,880원: 고용노동부
- 국민연금 보험료율 단계적 인상: 국민연금공단
- 2026년 건강보험료율 7.19%: 보건복지부
- 2026년 평균 산재보험료율 1.47%: 고용노동부
- Next.js App Router 및 TypeScript: Next.js 공식문서
- NestJS TypeScript 기반 서버 프레임워크: NestJS 공식문서

---

## 22. 최종 개발 방향

`30HR`의 1차 승부처는 “예쁜 HR 앱”이 아니다.

핵심은 다음이다.

```text
소규모 사업장이 월급날마다 틀리기 쉬운 급여·근태·계약·명세서·증빙을
법 기준에 맞게 자동 점검하고,
세무사/노무사에게 바로 전달 가능한 형태로 정리해주는 것.
```

따라서 Codex 개발 우선순위는 다음 순서로 고정한다.

```text
1. 멀티테넌트 + 권한
2. 직원대장
3. 법령 설정값 버전관리
4. 급여계산 엔진
5. 임금명세서
6. 근로계약서
7. 근태/휴가
8. 컴플라이언스 알림
9. 증빙팩
```
