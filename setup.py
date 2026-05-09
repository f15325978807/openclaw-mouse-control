from setuptools import setup, find_packages

setup(
    name="openclaw-mouse",
    version="1.0.0",
    description="OpenClaw 智能鼠标控制技能 - 赋予 AI Agent 完全控制用户电脑鼠标的能力",
    author="OpenClaw",
    packages=find_packages(),
    install_requires=[
        "pyautogui>=0.9.54",
        "typer>=0.9.0",
        "pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "openclaw-mouse=openclaw_mouse:app_cli",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
