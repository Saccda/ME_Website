import { test, expect } from "@playwright/test";

test("teacher generation, review, approval, and edit invalidation", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByRole("button", { name: "Teacher studio", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: /A stronger foundation/ }),
  ).toBeVisible();
  await page.screenshot({
    path: "test-results/teacher-overview.png",
    fullPage: true,
  });
  await page
    .getByRole("button", { name: "Generation studio", exact: true })
    .click();
  await page.getByLabel("Number of questions").fill("1");
  await page.getByRole("button", { name: "Generate original drafts" }).click();
  await expect(page.getByRole("status")).toContainText("1 original drafts");
  await page.locator(".question-link").first().click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.getByRole("button", { name: "Send for review" }).click();
  await page.getByRole("checkbox", { name: /I checked the wording/ }).check();
  await page.getByRole("button", { name: "Approve", exact: true }).click();
  await expect(
    page.getByRole("dialog").locator(".question-meta"),
  ).toContainText("Approved");
  await page
    .getByRole("button", { name: "Edit question", exact: true })
    .click();
  await page
    .getByLabel("Question stem")
    .fill(
      "Original teacher revision: " +
        (await page.getByLabel("Question stem").inputValue()),
    );
  await page.getByRole("button", { name: "Save as draft" }).click();
  await expect(
    page.getByRole("dialog").locator(".question-meta"),
  ).toContainText("Draft");
  await page.getByRole("button", { name: "Close dialog" }).click();
  await page
    .getByRole("button", { name: "Student workspace", exact: true })
    .click();
});

test("student guided practice, results and insights", async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByRole("button", { name: "Generation studio" }),
  ).toHaveCount(0);
  await page
    .getByRole("button", { name: "Student practice", exact: true })
    .click();
  await page.getByLabel("Question count").fill("2");
  await page.getByRole("button", { name: "Start guided practice" }).click();
  await expect(
    page.getByRole("heading", { name: "Focused practice" }),
  ).toBeVisible();
  await expect(page.locator(".explanation")).toHaveCount(0);
  await page.locator(".answer-options button").first().click();
  await page.getByRole("button", { name: "Check answer", exact: true }).click();
  await expect(page.locator(".explanation")).toBeVisible();
  await page.screenshot({
    path: "test-results/student-feedback.png",
    fullPage: true,
  });
  await page.getByRole("button", { name: "Next", exact: true }).click();
  await page.locator(".answer-options button").nth(1).click();
  await page.getByRole("button", { name: "Check answer", exact: true }).click();
  await page.getByRole("button", { name: "Finish & see results" }).click();
  await page
    .getByRole("button", { name: "Submit session", exact: true })
    .click();
  await expect(
    page.getByText("SESSION COMPLETE", { exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Back to workspace" }).click();
  await page
    .getByRole("button", { name: "Learning insights", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Accuracy by topic" }),
  ).toBeVisible();
});

test("exam feedback is delayed and mock exam starts", async ({ page }) => {
  await page.goto("/");
  await page
    .getByRole("button", { name: "Student practice", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Exam practice", exact: true })
    .click();
  await page.getByLabel("Question count").fill("1");
  await page.getByRole("button", { name: "Start exam practice" }).click();
  await page.locator(".answer-options button").first().click();
  await page.getByRole("button", { name: "Save answer", exact: true }).click();
  await expect(page.locator(".explanation")).toHaveCount(0);
  await page.getByRole("button", { name: "Finish & see results" }).click();
  await page
    .getByRole("button", { name: "Submit session", exact: true })
    .click();
  await expect(page.locator(".explanation")).toBeVisible();
  await page.getByRole("button", { name: "Back to workspace" }).click();
  await page.getByRole("button", { name: "Mock exams", exact: true }).click();
  await page
    .getByRole("button", { name: "Start mock exam", exact: true })
    .first()
    .click();
  await expect(page.locator(".timer")).toBeVisible();
});

test("mobile layout and navigation fit the viewport", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: /A stronger foundation/ }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.screenshot({
    path: "test-results/mobile-overview.png",
    fullPage: true,
  });
  await page.getByRole("button", { name: "Open menu" }).click();
  await page
    .getByRole("button", { name: "Student practice", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Practice the reasoning." }),
  ).toBeVisible();
});

test("no login screen and browser progress survives workspace switches and reload", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: /A stronger foundation/ }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: /sign in|log in|register/i }),
  ).toHaveCount(0);
  await page
    .getByRole("button", { name: "Student practice", exact: true })
    .click();
  await page.getByLabel("Question count").fill("1");
  await page.getByRole("button", { name: "Start guided practice" }).click();
  await page.locator(".answer-options button").first().click();
  await page.getByRole("button", { name: "Check answer", exact: true }).click();
  await page
    .getByRole("button", { name: "Save and leave", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Teacher studio", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Generation studio", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Student workspace", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Resume", exact: true }),
  ).toBeVisible();
  await page.reload();
  await page.getByRole("button", { name: "Resume", exact: true }).click();
  await expect(page.locator(".explanation")).toBeVisible();
});

test("checked textbook selection includes attribution and immediate feedback", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByRole("button", { name: "Student practice", exact: true })
    .click();
  await page.getByLabel("Question source").selectOption("textbook");
  const count = await page
    .locator("p.help")
    .filter({ hasText: "approved questions match" })
    .innerText();
  test.skip(
    count.startsWith("0 "),
    "Private selection is optional in portable installs",
  );
  await expect(page.getByLabel("Question count")).toHaveValue("3");
  await page.getByRole("button", { name: "Start guided practice" }).click();
  await expect(page.getByText(/From LearningExpress/)).toBeVisible();
  await expect(page.locator(".answer-options button")).toHaveCount(4);
  await page.locator(".answer-options button").first().click();
  await page.getByRole("button", { name: "Check answer", exact: true }).click();
  await expect(page.locator(".explanation")).toBeVisible();
});
