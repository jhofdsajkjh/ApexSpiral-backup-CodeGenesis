# agent-skills 全流程标准｜Addy Osmani 工程规范

## 标准六阶段：DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP

### 1. DEFINE（定义）/spec
- 输出：PRD、目标、用户、命令、结构、代码风格、测试要求、边界
- 解决：AI脑补需求、边界不清、后期大量返工

### 2. PLAN（规划）/plan
- 输出：原子任务、依赖顺序、验收标准（AC）
- 原则：小到可Review、小到可回滚、小到可验证

### 3. BUILD（构建）/build
- 薄切片纵向实现：一条可运行链路优先
- 安全默认、特性开关、友好回滚
- 禁止一次性大面积重构

### 4. VERIFY（验证）/test
- TDD测试驱动、单元测试、边界测试
- 错误恢复、DevTools调试、网络/日志/性能检查

### 5. REVIEW（评审）/review
- 三维度检查：资深工程师 + QA + 安全专家
- 清单：简化、安全、性能、可访问性、规范

### 6. SHIP（上线）
- 可监控、可回滚、可灰度、可快速修复
