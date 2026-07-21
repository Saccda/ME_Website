"use client";

import { FormEvent, useState } from "react";
import { API_BASE_URL } from "@/lib/api";

type FormState = "idle" | "submitting" | "success" | "error";

export default function InquiryForm() {
  const [state, setState] = useState<FormState>("idle");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setState("submitting");
    const form = event.currentTarget;
    const payload = Object.fromEntries(new FormData(form).entries());

    try {
      const response = await fetch(`${API_BASE_URL}/inquiries/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error("Submission failed");
      form.reset();
      setState("success");
    } catch {
      setState("error");
    }
  }

  return (
    <form className="inquiry-form" onSubmit={handleSubmit}>
      <div className="field-row">
        <label>
          Your name
          <input name="name" required autoComplete="name" />
        </label>
        <label>
          Email address
          <input name="email" type="email" required autoComplete="email" />
        </label>
      </div>
      <label>
        I’m interested in
        <select name="inquiry_type" defaultValue="admission">
          <option value="admission">Admission</option>
          <option value="collaboration">Collaboration</option>
          <option value="general">General information</option>
        </select>
      </label>
      <label>
        Subject
        <input name="subject" required />
      </label>
      <label>
        Message
        <textarea name="message" rows={5} required />
      </label>
      <label className="honeypot" aria-hidden="true">
        Website
        <input name="website" tabIndex={-1} autoComplete="off" />
      </label>
      <button className="button button-gold" type="submit" disabled={state === "submitting"}>
        {state === "submitting" ? "Sending…" : "Send enquiry"} <span>↗</span>
      </button>
      <p className="form-status" aria-live="polite">
        {state === "success" && "Thank you. Your enquiry has been received."}
        {state === "error" &&
          "The form could not connect. Please email the program directly."}
      </p>
    </form>
  );
}
