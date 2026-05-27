# CodeGenesis
[![Stars](https://img.shields.io/github/stars/jhofdsajkjh/ApexSpiral-backup-CodeGenesis?style=social)](https://github.com/jhofdsajkjh/ApexSpiral-backup-CodeGenesis)
Status: Stable | License: MIT

## Features
- 代码生成：基于输入需求自动生成代码片段
- 模块化：支持多语言后端扩展

## Installation
\`\`\`bash
git clone https://github.com/jhofdsajkjh/ApexSpiral-backup-CodeGenesis.git
cd ApexSpiral-backup-CodeGenesis
pip install -r requirements.txt
\`\`\`

## Usage
\`\`\`bash
python -m core.gen_cli  # 启动生成命令行
\`\`\`

## Architecture
- \`core/\`: 核心生成逻辑
- \`tests/\`: 单元测试

## Tests
\`\`\`bash
python -m pytest tests/ -v
\`\`\`

## Contributing
提交前通过测试，更新 README。

## License
MIT
