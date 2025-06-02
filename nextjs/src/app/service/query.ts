export async function askQuestion(query: string) {
  const res = await fetch(
    `http://localhost:8000/user-query?query=${encodeURIComponent(query)}`,
    {
      method: "POST",
    }
  );

  if (!res.ok) throw new Error("질문 실패");

  return await res.json();
}
