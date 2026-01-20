# OpenSourceAnalyzer

## 项目简介

OpenSourceAnalyzer 是一个基于 Python 的开源软件仓库分析工具，
用于分析 GitHub 项目的代码演化、提交行为以及缺陷修复模式。
本项目为《开源软件基础》课程大作业，实现了从数据采集、静态分析
到结果可视化的完整流程。

---

## 功能特性

- GitHub 仓库自动克隆
- 提交历史统计与演化分析
- Bug 修复提交自动识别
- 作者贡献度分析
- 基于 AST 的静态代码分析
- 圈复杂度与代码异味检测
- 自动生成分析图表

---

## 项目结构
OpenSourceAnalyzer/
├── main.py
├── config.py
├── git_analyzer/
├── static_analysis/
├── visualization/
├── data/
├── figures/
└── README.md

---

## 环境依赖

- Python >= 3.8

安装依赖：

```bash
pip install gitpython pydriller pandas matplotlib
