"""Project scanner — detects existing code structure and generates spec drafts."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rich.console import Console

console = Console()

# File extensions grouped by language/framework
LANG_EXTENSIONS = {
    "python": [".py"],
    "javascript": [".js", ".jsx", ".mjs"],
    "typescript": [".ts", ".tsx"],
    "go": [".go"],
    "rust": [".rs"],
    "java": [".java"],
    "csharp": [".cs"],
    "ruby": [".rb"],
    "php": [".php"],
    "swift": [".swift"],
    "kotlin": [".kt"],
    "html": [".html", ".htm"],
    "css": [".css", ".scss", ".sass", ".less"],
    "sql": [".sql"],
    "yaml": [".yaml", ".yml"],
    "markdown": [".md"],
}

# Directories to always skip
SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "env",
    ".env", "dist", "build", ".next", ".nuxt", ".svelte-kit",
    "target", "vendor", ".tox", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", "coverage", ".coverage", "htmlcov", "eggs",
    "*.egg-info", ".sdd", "specs", "agents", "sprints",
}


def scan_project(root: Path) -> Dict:
    """Scan a project directory and return structured analysis."""
    result = {
        "root": str(root),
        "languages": {},
        "directories": [],
        "frameworks": [],
        "entry_points": [],
        "readme_sections": [],
        "total_files": 0,
    }

    # Scan directory structure
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and entry.name not in SKIP_DIRS and not entry.name.startswith("."):
            dir_info = _scan_directory(entry)
            if dir_info["file_count"] > 0:
                result["directories"].append(dir_info)
                result["total_files"] += dir_info["file_count"]
                for lang, count in dir_info["languages"].items():
                    result["languages"][lang] = result["languages"].get(lang, 0) + count

    # Also scan root-level files
    root_files = []
    for f in sorted(root.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            root_files.append(f)
            lang = _detect_language(f)
            if lang:
                result["languages"][lang] = result["languages"].get(lang, 0) + 1
            result["total_files"] += 1

    # Detect frameworks
    result["frameworks"] = _detect_frameworks(root)

    # Detect entry points
    result["entry_points"] = _detect_entry_points(root)

    # Parse README if exists
    readme = _find_readme(root)
    if readme:
        result["readme_sections"] = _parse_readme_sections(readme)

    return result


def _scan_directory(dir_path: Path) -> Dict:
    """Scan a single directory recursively."""
    info = {
        "name": dir_path.name,
        "path": str(dir_path),
        "file_count": 0,
        "languages": {},
        "files": [],
    }

    for root, dirs, files in os.walk(dir_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]

        for fname in files:
            fpath = Path(root) / fname
            if fname.startswith("."):
                continue
            info["file_count"] += 1
            info["files"].append(str(fpath.relative_to(dir_path.parent)))
            lang = _detect_language(fpath)
            if lang:
                info["languages"][lang] = info["languages"].get(lang, 0) + 1

    return info


def _detect_language(file_path: Path) -> Optional[str]:
    """Detect programming language from file extension."""
    ext = file_path.suffix.lower()
    for lang, exts in LANG_EXTENSIONS.items():
        if ext in exts:
            return lang
    return None


def _detect_frameworks(root: Path) -> List[str]:
    """Detect frameworks from config files."""
    frameworks = []

    indicators = {
        "requirements.txt": "Python (pip)",
        "pyproject.toml": "Python (modern)",
        "setup.py": "Python (setuptools)",
        "Pipfile": "Python (pipenv)",
        "package.json": "Node.js",
        "tsconfig.json": "TypeScript",
        "Cargo.toml": "Rust",
        "go.mod": "Go",
        "pom.xml": "Java (Maven)",
        "build.gradle": "Java (Gradle)",
        "Gemfile": "Ruby",
        "composer.json": "PHP",
        "Dockerfile": "Docker",
        "docker-compose.yml": "Docker Compose",
        "docker-compose.yaml": "Docker Compose",
        ".github/workflows": "GitHub Actions",
        "vercel.json": "Vercel",
        "netlify.toml": "Netlify",
        "next.config.js": "Next.js",
        "next.config.ts": "Next.js",
        "nuxt.config.ts": "Nuxt",
        "svelte.config.js": "SvelteKit",
        "angular.json": "Angular",
        "vite.config.ts": "Vite",
        "vite.config.js": "Vite",
        "webpack.config.js": "Webpack",
        "tailwind.config.js": "Tailwind CSS",
        "tailwind.config.ts": "Tailwind CSS",
        "prisma/schema.prisma": "Prisma",
        "manage.py": "Django",
        "app.py": "Flask/FastAPI",
        "main.py": "Python app",
    }

    for indicator, framework in indicators.items():
        if (root / indicator).exists():
            if framework not in frameworks:
                frameworks.append(framework)

    # Check package.json for specific frameworks
    pkg_json = root / "package.json"
    if pkg_json.exists():
        try:
            import json
            with open(pkg_json) as f:
                pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "react" in deps:
                frameworks.append("React")
            if "vue" in deps:
                frameworks.append("Vue.js")
            if "express" in deps:
                frameworks.append("Express.js")
            if "fastify" in deps:
                frameworks.append("Fastify")
            if "@nestjs/core" in deps:
                frameworks.append("NestJS")
        except (json.JSONDecodeError, OSError):
            pass

    return frameworks


def _detect_entry_points(root: Path) -> List[str]:
    """Detect likely entry point files."""
    candidates = [
        "main.py", "app.py", "server.py", "index.py",
        "index.js", "index.ts", "server.js", "server.ts", "app.js", "app.ts",
        "main.go", "main.rs",
        "src/main.py", "src/app.py", "src/index.ts", "src/index.js",
        "src/main.ts", "src/main.js",
        "cmd/main.go",
    ]
    found = []
    for c in candidates:
        if (root / c).exists():
            found.append(c)
    return found


def _find_readme(root: Path) -> Optional[Path]:
    """Find README file."""
    for name in ["README.md", "readme.md", "README.rst", "README.txt", "README"]:
        p = root / name
        if p.exists():
            return p
    return None


def _parse_readme_sections(readme_path: Path) -> List[str]:
    """Extract section headings from README."""
    sections = []
    try:
        content = readme_path.read_text(encoding="utf-8", errors="replace")
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                heading = stripped.lstrip("#").strip()
                if heading:
                    sections.append(heading)
    except OSError:
        pass
    return sections


def generate_spec_drafts(scan_result: Dict, project_name: str, owner: str) -> List[Dict]:
    """Generate spec draft metadata from scan results."""
    drafts = []
    spec_num = 1

    for dir_info in scan_result["directories"]:
        dir_name = dir_info["name"]

        # Skip test directories — they aren't features
        if dir_name in ("tests", "test", "__tests__", "spec"):
            continue

        # Estimate story points from file count
        fc = dir_info["file_count"]
        if fc <= 3:
            sp = 1
        elif fc <= 8:
            sp = 3
        elif fc <= 15:
            sp = 5
        else:
            sp = 5  # Cap at 5 — should be split

        langs = ", ".join(dir_info["languages"].keys()) if dir_info["languages"] else "unknown"
        files_list = dir_info["files"][:10]  # Limit to 10 files in spec

        drafts.append({
            "id": f"ROOT-{spec_num:03d}",
            "title": _dir_to_title(dir_name),
            "dir_name": dir_name,
            "story_points": sp,
            "languages": langs,
            "file_count": fc,
            "files": files_list,
            "status": "DRAFT",
        })
        spec_num += 1

    return drafts


def write_spec_file(spec_dir: Path, draft: Dict, project_name: str, owner: str) -> Path:
    """Write a single spec draft file and return its path."""
    spec_id = draft["id"]
    slug = draft["dir_name"].lower().replace(" ", "-").replace("_", "-")
    filename = f"{spec_id}-{slug}.spec.md"
    filepath = spec_dir / filename

    files_section = "\n".join(f"- {f}" for f in draft["files"])

    content = f"""# {spec_id}: {draft["title"]}

## [SUMMARY]
- App: {project_name}
- Epic owner: {{{{ADVISOR}}}}
- Status: {draft["status"]}
- Priority: S2
- Story points: {draft["story_points"]}

## [STORY]
As a user, I can use the {draft["title"].lower()} module
so that [FILL IN the business value].

## [TECH SPEC]
- Languages: {draft["languages"]}
- Files detected: {draft["file_count"]}
- [FILL IN technical details, APIs, data models]

### Files Touched
{files_section}

## [ACCEPTANCE CRITERIA]
AC-001: Given [precondition], when [action], then [expected result].
AC-002: [FILL IN additional criteria]

## [CHANGE LOG]
- {_today()}: Spec auto-generated by specag init (scanner v0.2.0)
"""
    filepath.write_text(content)
    return filepath


def _dir_to_title(name: str) -> str:
    """Convert directory name to a human-readable title."""
    return name.replace("_", " ").replace("-", " ").title()


def _today() -> str:
    """Return today's date as YYYY-MM-DD."""
    from datetime import date
    return date.today().isoformat()
