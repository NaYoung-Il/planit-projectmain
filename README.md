# planit-backend
AX Academy 4기 3팀 중간프로젝트 Planit  백엔드 Repository
developer 브랜치 : 여기서 개발 중인 내용 합칠 것

- main 브랜치: 🚢 실제 배포 가능한 버전만 관리하는 가장 깨끗하고 안정적인 브랜치입니다. 이곳에는 팀원 모두가 테스트를 완료한 develop 브랜치의 내용만 병합(merge)합니다. 개인 브랜치를 main에 바로 합치는 것은 금물입니다.

- develop 브랜치: 🏗️ 개발 중인 내용들을 통합하는 브랜치입니다. 각자 만든 기능(feature) 브랜치들은 모두 이 develop 브랜치로 합쳐서 기능들이 서로 잘 동작하는지 확인하는 용도로 사용합니다.

# DB 수정사항
-- 세부 일정 (place_name, place_address 정규화 필요)
CREATE TABLE schedule (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_day_id BIGINT,                     
    place_id BIGINT,        -- place_name, place_address 삭제 + places 테이블과 FK로 연결
    schedule_content TEXT,                  
    start_time TIME,                        
    end_time TIME,                          
    schedule_datetime DATETIME NOT NULL,    
    FOREIGN KEY (trip_day_id) REFERENCES trip_day(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE SET NULL     -- places 테이블과 FK로 연결
);

-- 준비물 체크리스트
CREATE TABLE checklist_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT,     -- trip_day에서 trip으로 연결 테이블 변경
    item_name VARCHAR(255) NOT NULL,
    is_checked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (trip_id) REFERENCES trip(id) on delete cascade
);

# 패키지 자동 업데이트 
새로 추가된 npm 의존성만 자동으로 설치하거나 업데이트 하려면 
프론트/ 백엔드 디렉토리(fastapi/ npm 실행 디렉토리)에서 아래 명령어를 실행합니다
### 프론트엔드
```bash
node update_packages.js
```

### 백엔드
```bash
python update_requirements.py
```
