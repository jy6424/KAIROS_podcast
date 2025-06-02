export async function uploadPDF(file: File, lectureName: string) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("lecture_name", lectureName);

  const res = await fetch("http://localhost:8000/process-pdf", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("PDF 업로드 실패");

  return await res.json();
}
