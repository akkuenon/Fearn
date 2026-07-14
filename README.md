<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Minimal IPA Signer Hub</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {
      --bg: #05060a;
      --card: #0c0f18;
      --accent: #4f8cff;
      --accent-soft: rgba(79, 140, 255, 0.12);
      --text: #f5f7ff;
      --muted: #9aa0b8;
      --border: #1a1f2b;
      --danger: #ff4f6a;
      --radius: 14px;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text",
        "Segoe UI", sans-serif;
      background: radial-gradient(circle at top, #101528 0, #05060a 55%);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      padding: 32px 16px;
    }
    .shell {
      width: 100%;
      max-width: 960px;
      border-radius: 24px;
      background: linear-gradient(145deg, #05060a 0, #090b12 40%, #05060a 100%);
      border: 1px solid rgba(255, 255, 255, 0.02);
      box-shadow:
        0 40px 80px rgba(0, 0, 0, 0.75),
        0 0 0 1px rgba(255, 255, 255, 0.02);
      padding: 24px 24px 28px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .logo {
      display: inline-flex;
      align-items: center;
      gap: 10px;
    }
    .cube {
      width: 32px;
      height: 32px;
      border-radius: 10px;
      background:
        conic-gradient(
          from 210deg,
          #4f8cff,
          #7b5cff,
          #4f8cff,
          #4f8cff
        );
      position: relative;
      box-shadow:
        0 0 0 1px rgba(255, 255, 255, 0.18),
        0 12px 30px rgba(0, 0, 0, 0.8);
      overflow: hidden;
    }
    .cube::before {
      content: "";
      position: absolute;
      inset: 6px;
      border-radius: 7px;
      background: radial-gradient(circle at 30% 20%, #ffffff33 0, transparent 40%);
      border: 1px solid rgba(5, 6, 10, 0.7);
    }
    .cube::after {
      content: "";
      position: absolute;
      inset: 11px 9px;
      border-radius: 6px;
      border: 2px solid rgba(5, 6, 10, 0.9);
      transform: rotate(45deg);
    }
    .brand {
      display: flex;
      flex
