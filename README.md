## KAIROS podcast
----
last update : 2025-05-29

고려대학교 생성형 AI Agent 학회 KAIROS 에서 진행한 MAS 개발과제입니다.

----

해당 프로젝트에서는 대학생을 위한 강의 팟캐스트 에이전트를 만들었습니다.

강의 pdf를 입력으로 받으면, 해당 내용을 페이지 별로 요약해 DB에 저장합니다.

QnA를 진행하면, 해당 내용 또한 DB에 저장합니다


이후 DB를 바탕으로 약 3분짜리의 팟캐스트를 생성합니다.

장점 : 다른 팟캐스트 에이전트와 달리 QnA데이터를 포함한 내용을 생성합니다. 이를 통해 유저의 더욱 개인화된 경험을 이끌어낼 수 있습니다.


----
특징:

RAG를 사용하기 위해 pinecone DB를 사용했습니다.
FastAPI로 백엔드를 구축했습니다.


----

MAS 워크플로우 : 


![workflow](https://github.com/jy6424/KAIROS_podcast/blob/main/workflow.png)
