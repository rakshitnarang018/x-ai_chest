# Frontend Setup

## Prerequisites

Ensure **Node.js v18.x** is installed.

Check version:

```bash
node -v
```

If not using v18:

```bash
nvm install 18
nvm use 18
```

---

## Installation Steps

### 1. Navigate to Project Folder

```bash
cd xai-frontend
```

### 2. Clean Existing Dependencies

```bash
rm -rf node_modules package-lock.json
```

**Windows PowerShell**

```powershell
rd /s /q node_modules
del package-lock.json
```

### 3. Fix Project Dependencies

```bash
npm uninstall @tailwindcss/vite
npm install react@18 react-dom@18
```

### 4. Install Packages

```bash
npm install
```

### 5. Run the Frontend

```bash
npm run dev
```

---

## Notes

* Uses **React 18**
* Removes problematic `@tailwindcss/vite` dependency
* Clean reinstall resolves common dependency/build issues
