export async function api<T>(
  path: string,
  method = "GET",
  body?: unknown,
): Promise<T> {
  const response = await fetch("/api" + path, {
    method,
    headers: { "Content-Type": "application/json", "X-App-Request": "1" },
    body: body === undefined ? undefined : JSON.stringify(body),
    credentials: "same-origin",
    cache: "no-store",
  });
  if (!response.ok) {
    const data = await response
      .json()
      .catch(() => ({ detail: "Request failed. Please try again." }));
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Please check the form fields.",
    );
  }
  return response.json();
}
