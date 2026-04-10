const { test, expect } = require("@playwright/test");

const username = process.env.E2E_USERNAME;
const password = process.env.E2E_PASSWORD;

test("login page smoke check", async ({ page }) => {
  await page.goto("/login/");

  await expect(page.locator("form")).toBeVisible();
  await expect(page.locator('input[name="username"]')).toBeVisible();
  await expect(page.locator('input[name="password"]')).toBeVisible();
  await expect(page.getByRole("button", { name: /sign in/i })).toBeVisible();
});

test("staff dashboard smoke flow", async ({ page }) => {
  test.skip(!username || !password, "Set E2E_USERNAME and E2E_PASSWORD for a staff account.");

  await page.goto("/login/");
  await page.locator('input[name="username"]').fill(username);
  await page.locator('input[name="password"]').fill(password);
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/dashboard\/$/);
  await expect(page.locator("body")).toContainText("Total Books");

  await page.goto("/books/");
  await expect(page.locator("body")).toContainText("Books");

  await page.goto("/issues/");
  await expect(page.locator("body")).toContainText("Issues");

  await page.goto("/notifications/");
  await expect(page.locator("body")).toContainText("Notifications");

  await page.goto("/reports/");
  await expect(page.locator("body")).toContainText("Reports");
});
