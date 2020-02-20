# 주식 용어
* PER : Price Earning Ratio, 주가를 주당 순이익(EPS) 으로 나눈 값. 주가의 수익성 지표로 자주 활용 된다.
    * 높은 PER : 기업이 영업활동으로 벌어들인 이익에 비해 주가가 고평가 되고 있음을 의미한다.
    * 낮은 PER : 주가가 상대적으로 저평가되고 있음을 의미한다.
> 현재의 주가를 과거? 의 주당순이익(EPS) 로 나눈 값인 것에 유의하자.

* PSR : ?
* PBR : Price Book-value Ratio(주가순자산비율) = 현재 주식 가격 / 주당 순자산
    * PBR 은 현재 주당 순자산의 몇배로 매매되고 있는지를 보여주는 지표이다.
    * PBR 을 간단히 설명하면, 얼마나 튼튼하고 안정적인 기업인지를 판단하는 지표라고 생각하면 된다.
* BPS : Book-value Per Share(주당순자산) = 순자산 / 총 주식수

# 사전 준비
1. path 확인
* python 환경 변수(내컴퓨터..) 확인한다. 나중에 win32com 설치 시에 경로를 못 잡는 경우는.. "https://belitino.tistory.com/132" 요기 참고해서, regedit 수정이 필요하다.

2. win32com 설치
* 다운로드 : 
* python version 에 맞춰 줘야 한다.https://github.com/mhammond/pywin32/releases
* python 경로도 잘 맞춰줘야 한다.
* 그래서 win32com 다운 로드 후 설치 시 경로를 인식한다.

3. win32com 만 잘 설치하면,, 문제 없다
4. 증권사 api 사용해보려는 경우는, 관리자 권한으로 실행 해야한다!!


### 참고문헌
* https://wikidocs.net/2869
* https://excelsior-cjh.tistory.com/105

# 증권사 API 는,,,
* Python 32bit 가 필요하다
* [아나콘다 !!](https://wikidocs.net/2825)

* 만약 32bit python 을 사용하고 있다면 anaconda 사용할 필요 없다!!!

* 환경변수 path 에 conda 추가 : C:\Anaconda3\Scripts
* 재시작

* 설치 후.. 가상환경 생성
> $ conda create -n \[가상환경이름\] python=2.7 

* 위 처럼, 가상 환경 생성 후.. 
> $ activate \[가상환경이름\]

* conda 를 이용해 win32com 설치하자
> $ conda install pywin32

# python 과 COM
* COM : Compoent Object Model

# CREON 매수/매도 위해서 해야 할 작업
* 시스템 드레이딩 신청 해야한다
* 1. CYBOS 5 실행 시켜서 검색 창에 1846 입력 (시스템 트레이딩 이용신청) // CREON 은 거래 프로그램 화면?이 안뜬다
* 2. 실행 아이콘? 우클릭 하여 '주문 오브젝트 사용 동의' 클릭 하여 동의 신청? 해야한다.

# 참고 사이트
* http://cybosplus.github.io/
* 

# CybosPlus Communication
> 출처 : Creon Plus > 도움말 > CybosPlus Communication 검색
* 대신증권 통신 방식은 Request/Reply (RQ/RP) 와 Subscribe/Publish(SB/PB) 방식으로 나뉨
    * CybosPlus 의 각 통신 모듈은 이 두 가지 통신 모델 중 한 가지만 지원함

### 1. RQ/RP 와 SB/PB 방식 비교 (비동기식 asynchronous)
* input data 를 채워서 통신을 요청 (RQ 또는 SB) 하면 함수가 바로 반환 됨
    * 요청 날리는 함수가 BlockRequest 함수 인 듯?
* RQ/RP : 현 시점의 data 1회 통신 요청
    * [RQ]
    * 1. input 값 설정 (obj.SetInputValue)
    * 2. 통신을 요청 (obj.Request)
    * [RP]
    * 3. 통신 수신 이벤트 1회 발생 (obj.received)
    * 4. data 를 얻는다 (obj.GetHeaderValue, obj.GetDataValue ?)
* SB/PB : 실 시간 data 수신 요청
    * [SB]
    * 1. input 값 설정 (obj.SetInputValue)
    * 2. 통신을 요청 (obj.Subscribe)
    * [PB]
    * 3. data(현재가) 가 변경 될 때마다 event 수시 발생 (obj.received)
    * 4. data 를 얻는다 (obj.GetHeaderValue, obj.GetDataValue ?)

### 2. SB/PB 방식 (동기식 synchronous)
* input data 를 채워 넣고 BlockRequest 함수를 호출하면, 서버로 부터 응답이 완료 될 때까지 대기상태를 유지함.
* 데이터를 정상적으로 수신한 후에 함수 리턴 됨.
    * 30 초 동안 서버로부터 요청한 data 를 수신하지 못하면 time out 처리 됨.
* BlockRequest 함수의 리턴 값으로 통신 결과 상태를 확인할 수 있다.
* [RQ]
* 1. input 값 설정 (obj.SetInputValue)
* 2. 통신을 요청 (obj.BlockRequest)
* [RP]
* 3. data 를 얻는다. (obj.GetHeaderValue, obj.GetDataValue ?)

### 3. RQ/RP 의 연속 data 통신
* data 수신 시에는 효율성을 고려해, 적정 size 가 있음.
* 모든 data 를 한 번의 요청으로 얻는 것이 아니라, 여러 번의 요청으로 얻을 수 있음.
* 각 object 의 공통 속성 인 Continue 가 True 인 경우, 더 받을 data 가 있다는 것임.
    * Continue 속성을 check 해, True 일 경우, 이 상태에서 통신을 요청(BlockRequest) 하면 연속 data 를 얻을 수 있음.
* [RQ]
* 1. input 값 설정 (obj.SetInputValue)
* 2. 통신을 요청 (obj.BlockRequest)
* [RP]
* 3. data 를 얻는다 (obj.GetHeaderValue, obj.GetDataValue)
* 4. 연속 data 유무 판단 (obj.Continue 가 True 일 경우, 위 2. 3. 을 반복)

### 4. 세금
* 증권거래세
    * 코스피 : 0.1 % (농어촌특별세? 0.15 % 가 있다네;;)
    * 코스닥 : 0.25 %
    * 코넥스 : 0.1 %
    * K-OTC : 0.25 %
* 결국, 세금은 0.3 % 정도인 듯? 

> [출처](https://economiology.com/%EC%A3%BC%EC%8B%9D%EA%B1%B0%EB%9E%98-%EC%84%B8%EA%B8%88-%EC%88%98%EC%88%98%EB%A3%8C-%EC%A6%9D%EA%B6%8C%EA%B1%B0%EB%9E%98%EC%84%B8-%EC%96%91%EB%8F%84%EC%86%8C%EB%93%9D%EC%84%B8/)

* [증건거래세(나무위키)](https://namu.wiki/w/증권거래세)
    * 매도 금액 - 매수 금액 - 매수 수수료 - 매도 수수료 - 매도 세금 > 0
    * 크레온, 매도/매수 둘 다 0.015 % 라고 치면..;
    * 수익 = 11000 - 10000 - (10000 * 0.00015) - (11000 * 0.00015) - (11000 * 0.003) = 1000 - 1.5 - 1.65 - 33 = 963.85 원
    * 수익 = 9000 - 10000 - (10000 * 0.00015) - (9000 * 0.00015) - (9000 * 0.003) = -1000 - 1.5 - 1.35 - 27 = -1029.85 원



### 5. git
* 로컬에서 수정 사항 확인
> $ git diff

* 로그 확인
> $ git log -p

