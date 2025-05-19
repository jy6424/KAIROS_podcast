```snippets
graph TD
    A[사용자 입력: PDF 파일, 팟캐스트 설정 주제, 톤앤매너, 목표 청취자 등] --> B(Podcast_Orchestrator_Agent);

    subgraph "팟캐스트 생성 파이프라인"
        B --> C(PDF_전처리_에이전트);
        C --> D(콘텐츠_분석_에이전트);
        D --> E(스토리_구성_에이전트);
        E --> F(대본_작성_에이전트);
        F --> G(대본_검토_개선_에이전트);
        G -- 수정된 대본 --> H(음성_합성_에이전트);
        G -- 피드백/재작성 요청 --> F;
        H --> I(오디오_후반작업_에이전트);
        I --> J(최종_패키징_에이전트);
    end

    B -- 전체 조율 및 상태 관리 --> K((Langfuse 대시보드));
    C -- 처리 데이터 로깅 --> K;
    D -- 분석 결과 로깅 --> K;
    E -- 스토리 구조 로깅 --> K;
    F -- 대본 초안 로깅 --> K;
    G -- 검토/수정 과정 로깅 --> K;
    H -- TTS 작업 로깅 --> K;
    I -- 오디오 편집 로그 로깅 --> K;
    J -- 최종 패키지 정보 로깅 --> K;

    J --> L[최종 팟캐스트 파일 및 메타데이터];
```

```snippets
graph TD
    A[사용자 입력: PDF 파일, 팟캐스트 설정 (주제, 톤앤매너, 목표 청취자 등)] --> B(Podcast_Orchestrator_Agent);

    subgraph "팟캐스트 생성 파이프라인"
        B --> C(PDF_Preprocessor_Agent);
        C --> D(Content_Analysis_Agent);
        D --> E(Story_Structuring_Agent);
        E --> F(Scriptwriting_Agent);
        F --> G(Script_Review_Enhancement_Agent);
        G -- 수정된 대본 --> H(TTS_Generation_Agent);
        G -- 피드백/재작성 요청 --> F;
        H --> I(Audio_Postproduction_Agent);
        I --> J(Final_Podcast_Package_Agent);
    end

    B -- 전체 조율 및 상태 관리 --> K((Langfuse 대시보드));
    C -- 처리 데이터 로깅 --> K;
    D -- 분석 결과 로깅 --> K;
    E -- 스토리 구조 로깅 --> K;
    F -- 대본 초안 로깅 --> K;
    G -- 검토/수정 과정 로깅 --> K;
    H -- TTS 작업 로깅 --> K;
    I -- 오디오 편집 로그 로깅 --> K;
    J -- 최종 패키지 정보 로깅 --> K;

    J --> L[최종 팟캐스트 파일 및 메타데이터];
```
