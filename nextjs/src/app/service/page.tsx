import { useState } from "react";

export default function WorkspacePage() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [init, setInit] = useState("");
  const [script, setScript] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [state, setState] = useState<any>(null);

  const handlePDFChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPdfFile(e.target.files[0]);
    }
  };

  const handlePDFUpload = async () => {
    if (!pdfFile) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      const res = await fetch("http://localhost:8000/process-pdf", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log("PDF 저장 완료:", data);
    } catch (err) {
      console.error("업로드 실패:", err);
    } finally {
      setUploading(false);
    }
  };

  const handleScriptToTTS = async () => {
    if (!init) return;
    try {
      const res = await fetch("http://localhost:8000/script-to-tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ init }),
      });
      const data = await res.json();
      setScript(data.script);
      setAudioUrl(data.audio_file);
      setState(data);
    } catch (err) {
      console.error("스크립트/TTS 실패:", err);
    }
  };

  return (
    <div style={{ padding: 20, maxWidth: 800, margin: "0 auto" }}>
      <h1 style={{ fontSize: "1.8rem", fontWeight: "bold", marginBottom: 16 }}>
        KAIROS 팟캐스트 작업공간
      </h1>

      {/* PDF 업로드 섹션 */}
      <div style={{ marginBottom: 24 }}>
        <h2>📄 PDF 업로드</h2>
        <input
          type="file"
          accept="application/pdf"
          onChange={handlePDFChange}
        />
        <button
          onClick={handlePDFUpload}
          disabled={uploading || !pdfFile}
          style={{ marginTop: 8 }}
        >
          {uploading ? "업로드 중..." : "VectorStore에 저장"}
        </button>
      </div>

      {/* Init 입력 & 스크립트 생성 */}
      <div style={{ marginBottom: 24 }}>
        <h2>🧠 팟캐스트 스크립트 생성</h2>
        <input
          type="text"
          placeholder="예: 강의 내용을 요약해서 팟캐스트 스크립트를 만들어줘"
          value={init}
          onChange={(e) => setInit(e.target.value)}
          style={{ width: "100%", padding: 8 }}
        />
        <button
          onClick={handleScriptToTTS}
          disabled={!init}
          style={{ marginTop: 8 }}
        >
          스크립트 생성 및 TTS 시작
        </button>
      </div>

      {/* 결과 출력 */}
      {script && (
        <div style={{ marginBottom: 24 }}>
          <h2>📝 생성된 스크립트</h2>
          <pre
            style={{
              whiteSpace: "pre-wrap",
              backgroundColor: "#f0f0f0",
              padding: 12,
            }}
          >
            {script}
          </pre>
        </div>
      )}

      {audioUrl && (
        <div>
          <h2>🎧 팟캐스트 오디오</h2>
          <audio controls src={audioUrl} style={{ width: "100%" }} />
        </div>
      )}
    </div>
  );
}
