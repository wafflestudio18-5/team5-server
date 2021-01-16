# team5-server

Team5 - 김유진(Front), 우현민(Front), 정대용(Back), 정민수(Back), 김기완(PM)
team5는 trello를 clone합니다.

- api documentation: [LINK](https://docs.google.com/document/d/1-1lXespTjti7DgOsNiLmjI6QkhyT5TzljXeTluanZKk/edit?usp=sharing)

endpoint : 

POST /api/v1/user/ (회원가입)  
PUT /api/v1/user/login/ (로그인)  
PUT /api/v1/user/logout/ (로그아웃)  
GET /api/v1/user/{id}/ (유저 정보)  
PUT /api/v1/user/update/ (유저 업데이트)  
GET /api/v1/user/list/ (유저 리스트)  
GET /api/v1/user/ (유저 리스트)  
POST /api/v1/board/ (보드 생성)  
GET /api/v1/board/boardlist/ (유저가 속한 보드확인)  
GET /api/v1/board/?key={key} (보드 정보)  
GET /api/v1/board/?id={id} (보드 정보)  
DELETE /api/v1/board/ (보드 삭제)  
POST /api/v1/board/invite/ (보드 초대)  
GET /api/v1/board/userlist/?board_id={board_id} (보드 내 유저 리스트)  
PUT /api/v1/board/ (보드 수정)  
POST /api/v1/list/ (리스트 생성)  
DELETE /api/v1/list/ (리스트 삭제)  
PUT /api/v1/list/ (리스트 수정)  
POST /api/v1/card/ (카드 생성)  
GET /api/v1/card/?key={key} (카드 정보)  
GET /api/v1/card/?id={id} (카드 정보)  
PUT /api/v1/card/ (카드 수정)  
DELETE  /api/v1/card/ (카드 삭제)  
POST /api/v1/activity/ (엑티비티 생성)  
PUT /api/v1/activity/ (엑티비티 수정)  
DELETE /api/v1/activity/ (엑티비티 삭제)  
