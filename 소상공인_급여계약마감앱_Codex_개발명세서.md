# 소상공인 급여·계약 마감앱 MVP 개발명세서

> 문서 목적: Codex 또는 개발자가 바로 구현을 시작할 수 있도록 제품 범위, 기술스택, DB 구조, API, 권한, 급여계산 로직, 테스트 기준을 정리한다.  
> 버전: MVP v0.1  
> 기준일: 2026-05-08  
> 제품 가칭: **사장님 급여마감**

---

## 0. 핵심 결론

이 프로젝트는 “종합 HR 앱”이 아니라 **소상공인을 위한 급여·근로계약·임금명세서 자동 마감도구**이다.

초기 MVP에서는 아래 4가지만 정확히 구현한다.

1. 직원 등록
2. 근로계약서 자동 생성
3. 주휴수당·최저임금 검증 포함 급여 기초계산
4. 임금명세서 및 임금대장 생성

---

## 1. 제품 정의

### 1.1 제품 한 줄 설명

직원 3~20명 사업장이 근로계약서, 주휴수당, 최저임금, 임금명세서, 임금대장을 한 번에 처리할 수 있는 소상공인용 급여·계약 마감 SaaS.

### 1.2 1차 사용자

| 역할 | 설명 |
|---|---|
| OWNER | 사업주. 회사 단위 모든 권한 보유 |
| STAFF | 직원. 본인 계약서·임금명세서 조회 |
| ADVISOR | 세무사/노무사. 지정 사업장 자료 읽기 및 다운로드 |
| SUPER_ADMIN | 서비스 운영자. 원칙적으로 고객 급여·개인정보 열람 제한 |

### 1.3 1차 타깃

| 항목 | 기준 |
|---|---|
| 사업장 규모 | 직원 3~20명 |
| 업종 | 음식점, 카페, 미용실, 편의점, 소매점 |
| 근로형태 | 시급제, 월급제, 단시간, 주말근무 |
| 핵심 문제 | 근로계약서, 주휴수당, 최저임금, 임금명세서, 임금대장 |

---

## 2. MVP 범위

## 2.1 Must Have

| 기능 | 설명 |
|---|---|
| 회사 등록 | 사업자번호, 상호, 대표자, 주소, 지급일, 상시근로자수 입력 |
| 직원 등록 | 이름, 휴대폰, 입사일, 근로형태, 급여유형, 시급/월급, 주소정근로시간 |
| 근로계약서 자동 생성 | 정규직, 단시간, 일용직, 기간제 템플릿 |
| 계약서 PDF 생성 | 생성일, 교부일, 해시값, 버전 관리 |
| 급여 기초계산 | 기본급, 근무시간, 주휴수당, 공제, 실수령액 |
| 최저임금 검증 | 2026년 시급 10,320원, 월 환산액 2,156,880원 기준 seed |
| 임금명세서 PDF | 필수 항목 누락 시 발급 차단 |
| 임금대장 엑셀 | 월별 직원별 지급·공제·실수령액 다운로드 |
| 알림톡/SMS | 계약서 확인 요청, 임금명세서 발급 안내 |
| 증빙 보관함 | 계약서, 명세서, 임금대장 다운로드 |
| 감사로그 | 개인정보 조회, 다운로드, 수정 이력 저장 |

## 2.2 Should Have

| 기능 | 설명 |
|---|---|
| 수기 근태 입력 | 일자별 근무시간 수기 입력 |
| 엑셀 업로드 | 직원별 근무시간 일괄 업로드 |
| 퇴사정산 미리보기 | 일할계산, 미지급 임금, 주휴수당 |
| ADVISOR 초대 | 세무사/노무사 읽기 권한 부여 |
| 4인 이하/5인 이상 법규 분기 | 가산수당, 연차 등 자동 안내 |

## 2.3 Out of Scope

아래 기능은 MVP에서 구현하지 않는다.

- GPS 출퇴근
- QR 출퇴근
- Wi-Fi 출퇴근
- 시프트 편성
- POS 연동
- 4대보험 EDI 직접 신고
- 홈택스 직접 신고
- 정부지원금 매칭
- 안전보건/MSDS
- 연말정산
- 외국인 비자관리
- 직장 내 괴롭힘 조사 워크플로우
- 일용직 공유 풀
- 모바일 네이티브 앱

---

## 3. 기술스택

## 3.1 Frontend

```text
React 18
Vite
TypeScript
Tailwind CSS
shadcn/ui
TanStack Query
Zustand
React Hook Form
Zod
```

## 3.2 Backend

```text
Supabase
Postgres
Supabase Auth
Supabase Storage
Supabase Edge Functions
PostgREST
```

## 3.3 External Services

```text
Solapi: 알림톡/SMS
Toss Payments: 정기결제, MVP 후순위
PDF Generator: 서버측 PDF 생성
Excel Export: xlsx 라이브러리
Sentry: 오류 모니터링
PostHog: 제품 분석
Better Stack: uptime 모니터링
```

## 3.4 권장 폴더 구조

```text
smallbiz-payroll-app/
  apps/
    web/
      src/
        app/
        components/
        features/
          auth/
          company/
          employees/
          contracts/
          payroll/
          payslips/
          documents/
          advisors/
        lib/
        routes/
        stores/
        types/
  supabase/
    migrations/
    functions/
      generate-contract-pdf/
      calculate-payroll/
      generate-payslips/
      export-payroll-ledger/
      send-notification/
    seed.sql
  packages/
    payroll-core/
      src/
        rules/
        calculators/
        validators/
        types/
      tests/
    contracts-core/
      templates/
      src/
  docs/
    DEVELOPMENT_SPEC.md
    LEGAL_RULE_MATRIX.md
    PAYROLL_TEST_CASES.md
```

---

## 4. 환경변수

```env
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=

SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_JWT_SECRET=

SOLAPI_API_KEY=
SOLAPI_API_SECRET=
SOLAPI_SENDER=
KAKAO_CHANNEL_ID=

PDF_STORAGE_BUCKET=documents

APP_BASE_URL=http://localhost:5173
NODE_ENV=development
```

---

## 5. 핵심 도메인 규칙

## 5.1 4인 이하 / 5인 이상 분기

```text
상시근로자수 < 5:
- 연장·야간·휴일 가산수당: 법정 가산 미적용
- 연차유급휴가: 법정 연차 미적용
- 부당해고 구제: 원칙적으로 미적용
- 단, 근로계약서, 임금지급, 주휴일, 휴게, 임금명세서는 적용

상시근로자수 >= 5:
- 연장·야간·휴일 가산수당 적용
- 연차유급휴가 적용
- 부당해고 구제 가능성 안내
```

## 5.2 최저임금

```text
2026년 최저임금:
- 시간급: 10,320원
- 월 환산액: 2,156,880원
- 월 환산 기준: 주 40시간, 월 209시간
```

저장 차단 조건:

```text
salary_type = HOURLY and hourly_rate < minimum_wage.hourly
salary_type = MONTHLY and ordinary_hourly < minimum_wage.hourly
```

## 5.3 주휴수당

MVP 기본 규칙:

```text
발생요건:
- 주 소정근로시간 15시간 이상
- 해당 주 소정근로일 개근

지급액:
- 1일 소정근로시간 × 통상시급

단시간 근로자:
- 1주 소정근로시간 / 40시간 × 8시간 × 통상시급
```

MVP에서는 결근 여부를 사용자가 입력한다.

## 5.4 임금명세서 필수 항목

임금명세서 생성 시 아래 항목이 없으면 발급을 차단한다.

1. 성명
2. 생년월일 또는 사원번호 등 식별정보
3. 임금지급일
4. 임금총액
5. 기본급, 수당, 상여금, 성과금 등 구성항목별 금액
6. 구성항목별 계산방법
7. 근로일수
8. 총 근로시간수
9. 연장·야간·휴일 근로시간수
10. 공제항목별 금액과 총액
11. 공제항목별 계산방법

---

## 6. 데이터베이스 설계

## 6.1 Enum

```sql
create type user_role as enum ('OWNER', 'STAFF', 'ADVISOR', 'SUPER_ADMIN');

create type employment_type as enum (
  'REGULAR',
  'CONTRACT',
  'PARTTIME',
  'DAILY',
  'INTERN'
);

create type salary_type as enum (
  'MONTHLY',
  'HOURLY',
  'DAILY',
  'ANNUAL'
);

create type contract_status as enum (
  'DRAFT',
  'SENT',
  'SIGNED',
  'TERMINATED'
);

create type payroll_status as enum (
  'DRAFT',
  'CALCULATED',
  'LOCKED',
  'PAID'
);

create type payslip_item_kind as enum (
  'EARNING',
  'DEDUCTION'
);

create type document_kind as enum (
  'CONTRACT',
  'PAYSLIP',
  'PAYROLL_LEDGER',
  'OTHER'
);
```

## 6.2 companies

```sql
create table companies (
  id uuid primary key default gen_random_uuid(),
  biz_no varchar(12) not null unique,
  name text not null,
  representative text not null,
  address text,
  industry_code varchar(10),
  headcount int not null default 0,
  payday int not null default 25,
  fiscal_year_start date not null default '2026-01-01',
  leave_basis text not null default 'JOIN_DATE',
  settings_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

## 6.3 profiles

```sql
create table profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  company_id uuid references companies(id),
  role user_role not null default 'STAFF',
  name text not null,
  phone text,
  email text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

## 6.4 employees

```sql
create table employees (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  user_id uuid references auth.users(id),
  employee_no text,
  name_kr text not null,
  birth_date date,
  phone text,
  email text,
  address text,
  bank_code text,
  bank_account_encrypted bytea,
  bank_holder text,
  hire_date date not null,
  retire_date date,
  employment_type employment_type not null,
  position text,
  department text,
  weekly_contract_hours numeric(5,2) not null default 40,
  weekly_work_days numeric(3,1) not null default 5,
  is_active boolean generated always as (retire_date is null) stored,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(company_id, employee_no)
);
```

## 6.5 salary_setups

```sql
create table salary_setups (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  employee_id uuid not null references employees(id) on delete cascade,
  effective_from date not null,
  salary_type salary_type not null,
  base_amount numeric(12,0) not null,
  fixed_allowances_json jsonb not null default '[]'::jsonb,
  is_minimum_wage_checked boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

## 6.6 employment_contracts

```sql
create table employment_contracts (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  employee_id uuid not null references employees(id) on delete cascade,
  version int not null default 1,
  contract_type text not null,
  period_start date not null,
  period_end date,
  workplace text,
  job_description text,
  working_hours_json jsonb not null default '{}'::jsonb,
  weekly_off_days text[] not null default array['SUNDAY'],
  salary_type salary_type not null,
  base_amount numeric(12,0) not null,
  allowances_json jsonb not null default '[]'::jsonb,
  payday int not null,
  status contract_status not null default 'DRAFT',
  pdf_storage_key text,
  pdf_hash_sha256 text,
  issued_at timestamptz,
  signed_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

## 6.7 work_entries

MVP에서는 GPS/QR 근태가 아니라 수기 입력 또는 엑셀 업로드 기반이다.

```sql
create table work_entries (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  employee_id uuid not null references employees(id) on delete cascade,
  work_date date not null,
  work_minutes int not null default 0,
  break_minutes int not null default 0,
  paid_minutes int not null default 0,
  absent boolean not null default false,
  note text,
  created_by uuid references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(employee_id, work_date)
);
```

## 6.8 payroll_runs

```sql
create table payroll_runs (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  period_year int not null,
  period_month int not null,
  period_start date not null,
  period_end date not null,
  pay_date date not null,
  status payroll_status not null default 'DRAFT',
  total_gross_pay numeric(12,0) not null default 0,
  total_deductions numeric(12,0) not null default 0,
  total_net_pay numeric(12,0) not null default 0,
  calculated_at timestamptz,
  locked_at timestamptz,
  locked_by uuid references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(company_id, period_year, period_month)
);
```

## 6.9 payslips

```sql
create table payslips (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  run_id uuid not null references payroll_runs(id) on delete cascade,
  employee_id uuid not null references employees(id) on delete cascade,
  period_start date not null,
  period_end date not null,
  pay_date date not null,
  gross_pay numeric(12,0) not null default 0,
  deductions numeric(12,0) not null default 0,
  net_pay numeric(12,0) not null default 0,
  total_work_days numeric(5,1) not null default 0,
  total_work_hours numeric(8,2) not null default 0,
  overtime_hours numeric(8,2) not null default 0,
  night_hours numeric(8,2) not null default 0,
  holiday_hours numeric(8,2) not null default 0,
  calc_basis_json jsonb not null default '{}'::jsonb,
  pdf_storage_key text,
  pdf_hash_sha256 text,
  issued_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

## 6.10 payslip_items

```sql
create table payslip_items (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  payslip_id uuid not null references payslips(id) on delete cascade,
  kind payslip_item_kind not null,
  code varchar(30) not null,
  name text not null,
  amount numeric(12,0) not null,
  calculation_method text,
  calc_basis_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
```

## 6.11 documents

```sql
create table documents (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  employee_id uuid references employees(id),
  kind document_kind not null,
  storage_key text not null,
  filename text not null,
  mime text not null,
  size_bytes int,
  hash_sha256 text,
  retention_until date,
  created_by uuid references auth.users(id),
  created_at timestamptz not null default now()
);
```

## 6.12 advisor_grants

```sql
create table advisor_grants (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  advisor_user_id uuid not null references auth.users(id) on delete cascade,
  can_view_contracts boolean not null default true,
  can_view_payslips boolean not null default true,
  can_download_payroll_ledger boolean not null default true,
  expires_at timestamptz,
  created_by uuid references auth.users(id),
  created_at timestamptz not null default now()
);
```

## 6.13 audit_logs

```sql
create table audit_logs (
  id bigserial primary key,
  company_id uuid references companies(id),
  actor_id uuid references auth.users(id),
  action text not null,
  target_table text,
  target_id uuid,
  before_json jsonb,
  after_json jsonb,
  ip inet,
  user_agent text,
  at timestamptz not null default now()
);
```

## 6.14 reference tables

```sql
create table reference_minimum_wages (
  year int primary key,
  hourly numeric(12,0) not null,
  monthly_209h numeric(12,0) not null,
  effective_from date not null
);

insert into reference_minimum_wages(year, hourly, monthly_209h, effective_from)
values (2026, 10320, 2156880, '2026-01-01');

create table reference_insurance_rates (
  id uuid primary key default gen_random_uuid(),
  effective_from date not null,
  kind text not null,
  employee_rate numeric(8,6) not null,
  employer_rate numeric(8,6) not null,
  note text
);

create table reference_tax_tables (
  id uuid primary key default gen_random_uuid(),
  year int not null,
  version text not null,
  table_json jsonb not null,
  effective_from date not null
);
```

---

## 7. RLS 정책 원칙

## 7.1 기본 원칙

모든 업무 테이블은 `company_id`를 갖는다.

```text
OWNER:
- 같은 company_id 전체 읽기/쓰기

STAFF:
- 본인 employee_id 관련 데이터만 읽기
- 기본정보 일부 수정 가능

ADVISOR:
- advisor_grants에 허용된 company_id 및 자료만 읽기/다운로드

SUPER_ADMIN:
- 원칙적으로 고객 개인정보·급여정보 직접 조회 금지
- 운영상 필요한 경우 별도 support_access_grants 설계
```

## 7.2 RLS 예시

```sql
alter table employees enable row level security;

create policy "owner can read company employees"
on employees for select
using (
  company_id = (
    select company_id
    from profiles
    where id = auth.uid()
  )
  and exists (
    select 1
    from profiles
    where id = auth.uid()
    and role in ('OWNER')
  )
);

create policy "staff can read own employee"
on employees for select
using (
  user_id = auth.uid()
);

create policy "owner can insert employees"
on employees for insert
with check (
  company_id = (
    select company_id
    from profiles
    where id = auth.uid()
  )
  and exists (
    select 1
    from profiles
    where id = auth.uid()
    and role = 'OWNER'
  )
);
```

---

## 8. Edge Functions

## 8.1 generate-contract-pdf

### 목적

직원과 급여조건을 기반으로 근로계약서 PDF를 생성한다.

### Input

```json
{
  "employee_id": "uuid",
  "contract_type": "PARTTIME",
  "period_start": "2026-05-01",
  "period_end": null,
  "workplace": "서울시 송파구 ...",
  "job_description": "카페 매장 업무",
  "working_hours": {
    "mon": {"start": "09:00", "end": "15:00", "break_minutes": 30},
    "tue": {"start": "09:00", "end": "15:00", "break_minutes": 30}
  },
  "weekly_off_days": ["SUNDAY"],
  "salary_type": "HOURLY",
  "base_amount": 11000,
  "payday": 10
}
```

### 처리

1. OWNER 권한 확인
2. 직원/회사 조회
3. 최저임금 검증
4. 계약서 필수항목 검증
5. 템플릿 변수 치환
6. PDF 생성
7. SHA-256 hash 생성
8. Supabase Storage 저장
9. employment_contracts 생성 또는 업데이트
10. documents 생성
11. audit_logs 기록

### Output

```json
{
  "contract_id": "uuid",
  "document_id": "uuid",
  "pdf_url": "signed-url",
  "hash": "sha256"
}
```

---

## 8.2 calculate-payroll

### 목적

해당 월의 직원별 급여를 계산하고 payslips, payslip_items를 생성한다.

### Input

```json
{
  "year": 2026,
  "month": 5
}
```

### 처리

1. OWNER 권한 확인
2. payroll_runs 생성 또는 기존 DRAFT 조회
3. 대상 직원 조회
4. salary_setups 조회
5. work_entries 집계
6. 기본급/시급 계산
7. 주휴수당 계산
8. 최저임금 검증
9. 4대보험 공제 계산
10. 소득세/지방소득세 계산
11. payslips 생성
12. payslip_items 생성
13. payroll_runs 합계 업데이트
14. audit_logs 기록

### Output

```json
{
  "run_id": "uuid",
  "status": "CALCULATED",
  "total_gross_pay": 12400000,
  "total_deductions": 1320000,
  "total_net_pay": 11080000,
  "employee_count": 7
}
```

---

## 8.3 generate-payslips

### 목적

계산 완료된 payslip을 PDF로 생성하고 Storage에 저장한다.

### Input

```json
{
  "run_id": "uuid"
}
```

### 처리

1. OWNER 권한 확인
2. payroll_run 상태 확인: CALCULATED만 허용
3. payslip별 필수항목 검증
4. PDF 생성
5. hash 생성
6. Storage 저장
7. documents 생성
8. payslips.issued_at 업데이트
9. audit_logs 기록

---

## 8.4 export-payroll-ledger

### 목적

세무사 전달용 임금대장 엑셀 파일을 생성한다.

### Input

```json
{
  "run_id": "uuid"
}
```

### Output columns

```text
귀속연월
지급일
사번
성명
입사일
퇴사일
급여유형
기본급
주휴수당
기타수당
비과세
국민연금
건강보험
장기요양
고용보험
소득세
지방소득세
공제합계
지급총액
실수령액
계산근거
```

---

## 8.5 send-notification

### 목적

계약서 확인 요청 또는 임금명세서 발급 안내를 Solapi로 발송한다.

### Input

```json
{
  "recipient_type": "STAFF",
  "employee_id": "uuid",
  "template_code": "PAYSLIP_ISSUED",
  "payload": {
    "month": "2026년 5월",
    "net_pay": "2,194,300원",
    "link": "https://..."
  }
}
```

---

## 9. 급여계산 패키지

## 9.1 패키지 위치

```text
packages/payroll-core
```

## 9.2 주요 함수

```ts
export function calculateOrdinaryHourly(input: OrdinaryHourlyInput): number;

export function validateMinimumWage(input: MinimumWageInput): MinimumWageResult;

export function calculateWeeklyHolidayPay(input: WeeklyHolidayPayInput): number;

export function calculateHourlyPayroll(input: HourlyPayrollInput): PayrollResult;

export function calculateMonthlyPayroll(input: MonthlyPayrollInput): PayrollResult;

export function calculateDeductions(input: DeductionInput): DeductionResult;

export function validatePayslipRequiredFields(input: PayslipDraft): ValidationResult;
```

## 9.3 타입 예시

```ts
export type SalaryType = 'MONTHLY' | 'HOURLY' | 'DAILY' | 'ANNUAL';

export interface MinimumWageInput {
  year: number;
  salaryType: SalaryType;
  baseAmount: number;
  weeklyContractHours: number;
  monthlyStandardHours?: number;
}

export interface PayrollResult {
  grossPay: number;
  deductions: number;
  netPay: number;
  items: PayrollItem[];
  calcBasis: Record<string, unknown>;
  warnings: PayrollWarning[];
}

export interface PayrollItem {
  kind: 'EARNING' | 'DEDUCTION';
  code: string;
  name: string;
  amount: number;
  calculationMethod: string;
  calcBasis: Record<string, unknown>;
}

export interface PayrollWarning {
  code: string;
  message: string;
  severity: 'INFO' | 'WARN' | 'BLOCK';
}
```

## 9.4 주휴수당 의사코드

```ts
export function calculateWeeklyHolidayPay(input: {
  ordinaryHourly: number;
  weeklyContractHours: number;
  weeklyWorkDays: number;
  isAbsent: boolean;
}): number {
  if (input.weeklyContractHours < 15) return 0;
  if (input.isAbsent) return 0;

  const dailyContractHours = Math.min(
    8,
    input.weeklyContractHours / Math.max(input.weeklyWorkDays, 1)
  );

  if (input.weeklyContractHours < 40) {
    return Math.round((input.weeklyContractHours / 40) * 8 * input.ordinaryHourly);
  }

  return Math.round(dailyContractHours * input.ordinaryHourly);
}
```

## 9.5 최저임금 검증 의사코드

```ts
export function validateMinimumWage(input: {
  salaryType: SalaryType;
  baseAmount: number;
  weeklyContractHours: number;
  minimumHourly: number;
}): {
  ok: boolean;
  ordinaryHourly: number;
  message?: string;
} {
  const monthlyHours = getMonthlyStandardHours(input.weeklyContractHours);

  const ordinaryHourly =
    input.salaryType === 'MONTHLY'
      ? Math.floor(input.baseAmount / monthlyHours)
      : input.baseAmount;

  if (ordinaryHourly < input.minimumHourly) {
    return {
      ok: false,
      ordinaryHourly,
      message: `최저임금 미달: 산정 통상시급 ${ordinaryHourly.toLocaleString()}원, 기준 ${input.minimumHourly.toLocaleString()}원`
    };
  }

  return { ok: true, ordinaryHourly };
}
```

---

## 10. 화면 설계

## 10.1 Owner Dashboard

### 주요 카드

```text
오늘 처리할 일
- 계약서 미발송 2건
- 5월 급여 미마감
- 최저임금 미달 의심 1건
- 임금명세서 미발급 3건
```

### 주요 CTA

```text
[직원 추가]
[계약서 만들기]
[급여 계산하기]
[임금명세서 발급]
[임금대장 다운로드]
```

---

## 10.2 직원 등록 화면

필드:

```text
성명
휴대폰
이메일
입사일
근로형태
급여유형
시급 또는 월급
주 소정근로시간
주 근무일수
지급일
```

검증:

```text
성명 필수
입사일 필수
시급제인 경우 시급 필수
월급제인 경우 월급 필수
주 소정근로시간 0 초과
최저임금 미달 저장 차단
```

---

## 10.3 계약서 생성 화면

단계:

```text
1. 직원 선택
2. 계약유형 선택
3. 근무장소/업무 입력
4. 근무시간 입력
5. 임금조건 확인
6. PDF 미리보기
7. 발송 또는 저장
```

---

## 10.4 급여 마감 화면

단계:

```text
1. 귀속월 선택
2. 근무시간 입력/업로드
3. 급여 계산
4. 이상치 확인
5. 임금명세서 생성
6. 임금대장 다운로드
7. 마감 잠금
```

---

## 10.5 임금명세서 화면

표시 항목:

```text
직원명
귀속월
지급일
지급총액
공제총액
실수령액
지급항목별 금액
공제항목별 금액
계산방법
근로일수
총 근로시간
연장/야간/휴일근로시간
```

---

## 11. API 설계

Supabase PostgREST를 기본으로 사용하되, 도메인 로직은 Edge Functions로 구현한다.

## 11.1 Company

```http
GET /rest/v1/companies
POST /rest/v1/companies
PATCH /rest/v1/companies?id=eq.{id}
```

## 11.2 Employees

```http
GET /rest/v1/employees?company_id=eq.{company_id}
POST /rest/v1/employees
PATCH /rest/v1/employees?id=eq.{id}
```

## 11.3 Contracts

```http
POST /functions/v1/generate-contract-pdf
GET /rest/v1/employment_contracts?employee_id=eq.{employee_id}
POST /functions/v1/send-notification
```

## 11.4 Work Entries

```http
GET /rest/v1/work_entries?employee_id=eq.{employee_id}&work_date=gte.{start}
POST /rest/v1/work_entries
PATCH /rest/v1/work_entries?id=eq.{id}
```

## 11.5 Payroll

```http
POST /functions/v1/calculate-payroll
POST /functions/v1/generate-payslips
GET /rest/v1/payroll_runs?company_id=eq.{company_id}
GET /rest/v1/payslips?run_id=eq.{run_id}
GET /functions/v1/export-payroll-ledger?run_id={run_id}
```

---

## 12. 테스트 기준

## 12.1 Unit Test

```text
payroll-core:
- 최저임금 검증
- 주휴수당 계산
- 월급제 통상시급 환산
- 시급제 급여계산
- 공제계산
- 임금명세서 필수항목 검증
```

## 12.2 Integration Test

```text
- 직원 등록 후 계약서 PDF 생성
- 급여계산 후 payslip/payslip_items 생성
- 임금명세서 PDF 생성 후 documents 저장
- 임금대장 엑셀 다운로드
- ADVISOR 권한으로 지정 자료 조회
- STAFF 권한으로 본인 명세서만 조회
```

## 12.3 E2E Test

```text
Owner 회원가입
회사 등록
직원 등록
계약서 생성
근무시간 입력
급여 계산
임금명세서 생성
임금대장 다운로드
마감 잠금
```

## 12.4 Golden Test Case 최소 수량

| 영역 | 최소 개수 |
|---|---:|
| 시급제 주휴수당 | 20 |
| 월급제 최저임금 검증 | 20 |
| 4인 이하/5인 이상 분기 | 20 |
| 입사·퇴사 월 일할계산 | 20 |
| 공제 계산 | 20 |
| 임금명세서 필수항목 | 20 |
| 합계 | 120 |

---

## 13. 수용 기준

## 13.1 회사 등록

```text
Given OWNER가 로그인되어 있을 때
When 사업자번호, 상호, 대표자, 지급일을 입력하고 저장하면
Then companies row가 생성되고 OWNER profile에 company_id가 연결되어야 한다.
```

## 13.2 직원 등록

```text
Given OWNER가 회사에 속해 있을 때
When 직원명, 입사일, 급여유형, 급여액, 주소정근로시간을 입력하면
Then employees와 salary_setups가 생성되어야 한다.

And 최저임금 미달이면 저장이 차단되어야 한다.
```

## 13.3 계약서 생성

```text
Given 직원과 급여정보가 등록되어 있을 때
When OWNER가 계약서 생성을 요청하면
Then employment_contracts row와 documents row가 생성되고 PDF가 Storage에 저장되어야 한다.
```

## 13.4 급여계산

```text
Given 직원, salary_setups, work_entries가 있을 때
When OWNER가 calculate-payroll을 실행하면
Then payroll_runs, payslips, payslip_items가 생성되어야 한다.

And 지급총액 - 공제총액 = 실수령액이어야 한다.
```

## 13.5 임금명세서

```text
Given payroll_run이 CALCULATED 상태일 때
When generate-payslips를 실행하면
Then 각 직원별 PDF가 생성되어야 한다.

And 필수항목 누락 시 PDF 생성이 차단되어야 한다.
```

---

## 14. 보안 요구사항

## 14.1 개인정보 최소수집

MVP에서는 주민등록번호 전체 수집을 원칙적으로 제외한다.  
불가피하게 필요한 경우 후속 버전에서 별도 암호화 구조를 설계한다.

## 14.2 마스킹

```text
휴대폰: 010-****-1234
계좌번호: 123-****-****-45
생년월일: 1990-**-**
```

## 14.3 다운로드 로그

아래 행위는 반드시 audit_logs에 기록한다.

```text
계약서 PDF 다운로드
임금명세서 PDF 다운로드
임금대장 엑셀 다운로드
직원 개인정보 수정
급여계산 실행
급여마감 잠금
ADVISOR 권한 부여
```

## 14.4 Signed URL

문서 다운로드 URL은 5분 이하 만료시간을 둔다.

---

## 15. 운영자 기능

MVP 운영자 기능은 최소화한다.

```text
- 가입 회사 목록
- 구독상태 조회
- 오류로그 조회
- 기준값 테이블 관리
- 고객 데이터 직접 조회 금지
```

기준값 관리 대상:

```text
최저임금
4대보험 요율
간이세액표
공휴일
```

---

## 16. 개발 단계

## Phase 1. 프로젝트 세팅

```text
- Vite React 프로젝트 생성
- Supabase 프로젝트 생성
- DB migration 구조 설정
- Auth 설정
- 기본 Layout 설정
- shadcn/ui 설치
```

## Phase 2. DB/RLS

```text
- companies
- profiles
- employees
- salary_setups
- employment_contracts
- work_entries
- payroll_runs
- payslips
- payslip_items
- documents
- advisor_grants
- audit_logs
- reference tables
- RLS policy
```

## Phase 3. Payroll Core

```text
- 최저임금 검증
- 통상시급 산정
- 주휴수당 계산
- 시급제 급여계산
- 월급제 급여계산
- 공제계산 stub
- 임금명세서 필수항목 검증
- Unit test 120개
```

## Phase 4. Owner UI

```text
- 회사 등록
- 직원 목록
- 직원 등록/수정
- 계약서 생성
- 근무시간 입력
- 급여마감
- 임금명세서 조회
- 임금대장 다운로드
```

## Phase 5. Edge Functions

```text
- generate-contract-pdf
- calculate-payroll
- generate-payslips
- export-payroll-ledger
- send-notification
```

## Phase 6. Beta QA

```text
- 20개 테스트 사업장 데이터 입력
- 월 급여마감 검증
- 임금명세서 필수항목 검증
- PDF/엑셀 다운로드 검증
- RLS 권한 테스트
```

---

## 17. Codex 작업 지시문

Codex에 아래 방식으로 순차 지시한다.

## 17.1 첫 번째 지시

```text
Create a React + Vite + TypeScript + Supabase project for a Korean small business payroll and employment contract SaaS.

Use the DEVELOPMENT_SPEC.md as the source of truth.

Implement only MVP v0.1:
- Company registration
- Employee registration
- Salary setup
- Employment contract PDF generation placeholder
- Manual work entries
- Payroll calculation
- Payslip data generation
- Payroll ledger export placeholder
- RLS-ready database schema

Do not implement:
- GPS attendance
- QR attendance
- Shift scheduling
- POS integration
- EDI
- Government subsidies
- Year-end tax settlement
```

## 17.2 두 번째 지시

```text
Implement the Supabase migration files based on section 6 of DEVELOPMENT_SPEC.md.

Requirements:
- Create all enum types
- Create all MVP tables
- Add indexes
- Enable RLS
- Add basic RLS policies for OWNER and STAFF
- Seed 2026 minimum wage
- Add updated_at trigger function
```

## 17.3 세 번째 지시

```text
Implement packages/payroll-core.

Required functions:
- calculateOrdinaryHourly
- validateMinimumWage
- calculateWeeklyHolidayPay
- calculateHourlyPayroll
- calculateMonthlyPayroll
- calculateDeductions
- validatePayslipRequiredFields

Add unit tests for at least:
- hourly worker above minimum wage
- hourly worker below minimum wage
- monthly worker below minimum wage
- weekly holiday pay for 40h worker
- weekly holiday pay for part-time worker under 40h
- no weekly holiday pay under 15h
- no weekly holiday pay if absent
```

## 17.4 네 번째 지시

```text
Implement Owner UI pages.

Pages:
- /onboarding/company
- /employees
- /employees/new
- /employees/:id
- /contracts/new
- /payroll
- /payroll/:runId
- /documents

Use:
- React Hook Form
- Zod validation
- TanStack Query
- shadcn/ui components
```

## 17.5 다섯 번째 지시

```text
Implement Supabase Edge Functions.

Functions:
- calculate-payroll
- generate-contract-pdf
- generate-payslips
- export-payroll-ledger
- send-notification

For PDF and Excel generation, placeholders are acceptable in the first pass, but the function signatures and DB writes must be complete.
```

---

## 18. 완료 정의

MVP 완료 기준은 아래와 같다.

```text
1. OWNER가 회원가입 후 회사 등록 가능
2. OWNER가 직원 등록 가능
3. 최저임금 미달 직원 저장 차단
4. 직원별 근로계약서 PDF 생성 가능
5. 직원별 근무시간 수기 입력 가능
6. 월 급여계산 가능
7. 임금명세서 데이터 생성 가능
8. 임금명세서 PDF 생성 가능
9. 임금대장 엑셀 다운로드 가능
10. STAFF는 본인 자료만 조회 가능
11. OWNER는 회사 자료만 조회 가능
12. ADVISOR는 grant 받은 회사 자료만 조회 가능
13. 주요 다운로드/수정 행위 audit_logs 기록
14. Unit test와 RLS test 통과
```

---

## 19. 개발 시 주의사항

```text
- 법령 기준값을 코드 상수로 박지 말 것.
- 최저임금, 보험요율, 세액표는 reference table에서 읽을 것.
- 급여계산 결과에는 반드시 calc_basis_json을 저장할 것.
- PDF 생성 시 hash_sha256을 저장할 것.
- 임금명세서 필수항목 누락 시 발급 차단할 것.
- SUPER_ADMIN이 고객 급여·개인정보를 기본 조회하지 못하게 할 것.
- STAFF가 타 직원 명세서를 볼 수 없게 RLS 테스트할 것.
- MVP에서 GPS/QR/시프트/POS/EDI를 구현하지 말 것.
```

---

## 20. 다음 문서

추가로 작성할 문서:

```text
LEGAL_RULE_MATRIX.md
PAYROLL_TEST_CASES.md
UI_WIREFRAME.md
SUPABASE_RLS_POLICY.md
CONTRACT_TEMPLATE_VARIABLES.md
PAYSLIP_TEMPLATE_SPEC.md
```
