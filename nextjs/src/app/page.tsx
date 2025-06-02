"use client";

import { useState, useEffect } from "react";
import { uploadPDF } from "./service/upload";
import { generateContent } from "./service/generate";
import { askQuestion } from "./service/query";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [lectureName, setLectureName] = useState("");
  const [lectureOptions, setLectureOptions] = useState<string[]>([]);
  const [newLecture, setNewLecture] = useState("");

  const [uploadResult, setUploadResult] = useState("");

  const [initText, setInitText] = useState("");
  const [generateResult, setGenerateResult] = useState("");
  const [generateResultObj, setGenerateResultObj] = useState<any>(null);

  const [question, setQuestion] = useState("");
  const [answerResult, setAnswerResult] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAsking, setIsAsking] = useState(false);

  const addLecture = () => {
    const trimmed = newLecture.trim();
    if (trimmed && !lectureOptions.includes(trimmed)) {
      const updated = [...lectureOptions, trimmed];
      setLectureOptions(updated);
      setNewLecture("");
      localStorage.setItem("lectureOptions", JSON.stringify(updated));
    }
  };

  const removeLecture = (lecture: string) => {
    const updated = lectureOptions.filter((l) => l !== lecture);
    setLectureOptions(updated);
    if (lectureName === lecture) {
      setLectureName("");
      localStorage.removeItem("lectureName");
    }
    localStorage.setItem("lectureOptions", JSON.stringify(updated));
  };

  const handleLectureSelect = (value: string) => {
    setLectureName(value);
    localStorage.setItem("lectureName", value);
  };

  const handleUpload = async () => {
    if (!file || !lectureName) return;
    setIsUploading(true);
    try {
      const res = await uploadPDF(file, lectureName);
      setUploadResult("done!");
    } catch (err: any) {
      setUploadResult("에러: " + err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleGenerate = async () => {
    if (!initText) return;
    setIsGenerating(true); // 시작 시 true
    try {
      const res = await generateContent(initText);
      console.log("📦 generateContent 응답:", res);
      setGenerateResult("아래에서 팟캐스트를 재생하세요!"); // ✅ 간단하게 Done 표시
      setGenerateResultObj(res);
    } catch (err: any) {
      setGenerateResult("에러: " + err.message);
      setGenerateResultObj(null);
    } finally {
      setIsGenerating(false); // 끝나면 false
    }
  };

  const handleAsk = async () => {
    if (!question) return;
    setIsAsking(true); // 질문 시작
    try {
      const res = await askQuestion(question);
      setAnswerResult(res.answer ?? "Done");
    } catch (err: any) {
      setAnswerResult("에러: " + err.message);
    } finally {
      setIsAsking(false); // 질문 끝
    }
  };

  useEffect(() => {
    const storedOptions = localStorage.getItem("lectureOptions");
    const storedName = localStorage.getItem("lectureName");

    if (storedOptions) {
      try {
        setLectureOptions(JSON.parse(storedOptions));
      } catch (e) {
        console.error("Invalid lectureOptions in localStorage");
      }
    }

    if (storedName) {
      setLectureName(storedName);
    }
  }, []);

  useEffect(() => {
    setGenerateResultObj({
      audio_url: "/static/audio/podcast_script.mp3",
    });
  }, []);

  return (
    <main className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8 text-center">KAIROS Podcast</h1>
      <h2 className="text-xl mb-6 text-center">
        업로드한 강의 PDF를 바탕으로 팟캐스트 생성 및 질문할 수 있습니다.
        <br />
        질문은 다음 팟캐스트에 반영됩니다!
      </h2>

      {/* 1. PDF 업로드 */}
      <section className="mb-10">
        <h2 className="text-xl font-semibold mb-4">강의PDF 업로드</h2>
        <div className="space-y-4">
          {/* 파일 선택 */}
          <label className="inline-block bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 cursor-pointer transition">
            파일 선택
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              className="hidden"
            />
          </label>
          {file && (
            <p className="text-sm text-gray-600">선택된 파일: {file.name}</p>
          )}

          {/* Lecture name 입력 및 선택 */}
          {/* 드롭다운 + 삭제 버튼 */}
          <div className="flex items-center gap-2">
            <select
              value={lectureName}
              onChange={(e) => {
                setLectureName(e.target.value);
                localStorage.setItem("lectureName", e.target.value);
              }}
              className="flex-grow px-3 py-2 border rounded-md"
            >
              <option value="">
                {lectureOptions.length === 0
                  ? "추가된 강의가 없습니다"
                  : "강의를 선택하세요"}
              </option>
              {lectureOptions.map((lecture) => (
                <option key={lecture} value={lecture}>
                  {lecture}
                </option>
              ))}
            </select>

            {lectureName && (
              <button
                onClick={() => {
                  const updated = lectureOptions.filter(
                    (l) => l !== lectureName
                  );
                  setLectureOptions(updated);
                  setLectureName("");
                  localStorage.setItem(
                    "lectureOptions",
                    JSON.stringify(updated)
                  );
                  localStorage.removeItem("lectureName");
                }}
                className="text-red-500 hover:text-red-700 text-sm font-semibold border border-red-300 px-3 py-2 rounded-md"
              >
                삭제
              </button>
            )}
          </div>

          <div className="flex items-center gap-2">
            <input
              type="text"
              placeholder="새 Lecture 추가"
              value={newLecture}
              onChange={(e) => setNewLecture(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault(); // 폼 submit 방지
                  addLecture(); // 엔터로 강의 추가
                }
              }}
              className="px-3 py-2 border rounded-md w-full"
            />
            <button
              onClick={addLecture}
              className="bg-green-600 text-white px-3 py-2 rounded-md hover:bg-green-700 transition whitespace-nowrap"
            >
              추가
            </button>
          </div>

          <button
            onClick={handleUpload}
            disabled={isUploading}
            className={`${
              isUploading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            } text-white px-4 py-2 rounded-md transition`}
          >
            {isUploading ? "업로드 중..." : "업로드"}
          </button>

          <pre className="bg-gray-100 p-3 rounded whitespace-pre-wrap">
            {uploadResult}
          </pre>
        </div>
      </section>
      {/* 2. 콘텐츠 생성 */}
      <section className="mb-10">
        <h2 className="text-xl font-semibold mb-4">팟캐스트</h2>
        <div className="space-y-2">
          <input
            type="text"
            placeholder="init 입력"
            value={initText}
            onChange={(e) => setInitText(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
          />
          <button
            onClick={handleGenerate}
            disabled={isGenerating}
            className={`${
              isGenerating
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            } text-white px-4 py-2 rounded-md transition`}
          >
            {isGenerating ? "생성 중..." : "생성하기"}
          </button>

          <pre className="bg-gray-100 p-3 rounded whitespace-pre-wrap">
            {generateResult}
          </pre>

          {generateResultObj?.audio_url && (
            <div>
              <audio
                controls
                src={`http://localhost:8000${generateResultObj.audio_url}`}
                className="mt-2 w-full"
              />
            </div>
          )}
        </div>
      </section>
      {/* 3. 질문 */}
      <section>
        <h2 className="text-xl font-semibold mb-4">질문하기</h2>
        <div className="space-y-2">
          <input
            type="text"
            placeholder="질문 입력"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
          />
          <button
            onClick={handleAsk}
            disabled={isAsking}
            className={`${
              isAsking
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            } text-white px-4 py-2 rounded-md transition`}
          >
            {isAsking ? "질문 중..." : "질문"}
          </button>
          <pre className="bg-gray-100 p-3 rounded whitespace-pre-wrap">
            {answerResult}
          </pre>
        </div>
      </section>
    </main>
  );
}
