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

