# OLE-Fuzzing
### OLE 구조를 사용하는 소프트웨어(한컴오피스 NEO)의 제로데이 취약점을 찾기 위한 퍼징 코드
### 개발일자 : 2017.08

## Author: Tackhyun Jung

## Status: 완료

### 핵심목표
1) OLE 구조를 사용하는 소프트웨어가 메모리에 적재될 때, 퍼징을 시도하는 코드 구현 (완료)
2) 퍼징간의 이벤트 코드가 access violation 등 타겟 이벤트가 발생하면 메모리 덤프를 뜨는 코드 구현 (완료)
---

### 사용된 기술
* Reverse Engineering
* Fuzzing

---

### Requirement
* Python 3x
* ctypes
* optparse
* itemgetter
* utils
* itemgetter
* shutil
* time
* pickle
* hashlib
* re
* OleFileIO_PL as OLE
* random import sample, uniform, choice
* winappdbg import *
* threading import Thread

---

### Usage

```
> python fuzzer.py
```

---
