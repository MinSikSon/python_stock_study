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