export async function generateContent(init: string) {
  const res = await fetch(
    `http://localhost:8000/generate-content?init=${encodeURIComponent(init)}`,
    {
      method: "POST",
    }
  );

  if (!res.ok) throw new Error("콘텐츠 생성 실패");

  return await res.json();
}
