import { test, expect } from '@playwright/test';

test('landing page has title and header text', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await expect(page).toHaveTitle(/OrbitOS/);
  await expect(page.locator('h1')).toContainText('The Autonomous');
});

test('dashboard page has sidebar, metrics, and launcher', async ({ page }) => {
  await page.goto('http://localhost:3000/dashboard');
  
  // Sidebar items
  await expect(page.locator('text=Dashboard')).toBeVisible();
  await expect(page.locator('text=Goals')).toBeVisible();
  
  // Metric card labels
  await expect(page.locator('text=Active Goals')).toBeVisible();
  await expect(page.locator('text=Tasks Automated')).toBeVisible();

  // Launcher input and button
  await expect(page.locator('textarea')).toBeVisible();
  await expect(page.locator('button:has-text("Launch")')).toBeVisible();
});
